#!/usr/bin/env python3
"""Tests for tools/graphify.py."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure graphify is importable.
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import graphify


class TestMermaidHelpers(unittest.TestCase):
    def test_to_mermaid_id_escapes_special_chars(self):
        self.assertEqual(graphify.to_mermaid_id("foo/bar"), "foo_bar")
        self.assertEqual(graphify.to_mermaid_id("foo.bar"), "foo_bar")
        self.assertEqual(graphify.to_mermaid_id("foo-bar"), "foo_bar")

    def test_to_mermaid_id_leading_digit(self):
        self.assertEqual(graphify.to_mermaid_id("123abc"), "n_123abc")

    def test_to_mermaid_id_empty_string(self):
        self.assertEqual(graphify.to_mermaid_id(""), "n_empty")

    def test_unique_mermaid_id_deduplicates(self):
        used: set[str] = set()
        self.assertEqual(graphify._unique_mermaid_id("foo", used), "foo")
        self.assertEqual(graphify._unique_mermaid_id("foo", used), "foo_1")
        self.assertEqual(graphify._unique_mermaid_id("foo", used), "foo_2")

    def test_escape_mermaid_label(self):
        self.assertEqual(graphify._escape_mermaid_label('say "hi"'), 'say \\"hi\\"')
        self.assertEqual(graphify._escape_mermaid_label("a\\b"), "a\\\\b")


class TestExclusions(unittest.TestCase):
    def test_is_cache_or_artifact_dir(self):
        self.assertTrue(graphify._is_cache_or_artifact_dir("__pycache__"))
        self.assertTrue(graphify._is_cache_or_artifact_dir("node_modules"))
        self.assertTrue(graphify._is_cache_or_artifact_dir(".mypy_cache"))
        self.assertFalse(graphify._is_cache_or_artifact_dir("src"))
        self.assertFalse(graphify._is_cache_or_artifact_dir("models"))

    def test_should_include_in_tree(self):
        self.assertFalse(graphify.should_include_in_tree(Path(".venv")))
        self.assertFalse(graphify.should_include_in_tree(Path("src/__pycache__")))
        self.assertTrue(graphify.should_include_in_tree(Path("src/models")))


class TestSafeReadSource(unittest.TestCase):
    def test_reads_utf8(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write("# hello\n")
            name = f.name
        try:
            result = graphify._safe_read_source(Path(name))
            self.assertEqual(result, "# hello\n")
        finally:
            os.unlink(name)

    def test_missing_file_returns_none(self):
        result = graphify._safe_read_source(Path("/nonexistent/path/file.py"))
        self.assertIsNone(result)


class TestModuleResolution(unittest.TestCase):
    def test_file_to_canonical_module(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "pkg" / "subpkg").mkdir(parents=True)
            (root / "pkg" / "__init__.py").write_text("")
            (root / "pkg" / "subpkg" / "__init__.py").write_text("")
            (root / "pkg" / "subpkg" / "mod.py").write_text("")

            package_dirs = {root / "pkg", root / "pkg" / "subpkg"}
            mod = graphify.file_to_canonical_module(
                root.resolve(), root / "pkg" / "subpkg" / "mod.py", package_dirs
            )
            self.assertEqual(mod, "pkg.subpkg.mod")

    def test_file_to_canonical_module_no_package(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "standalone.py").write_text("")
            mod = graphify.file_to_canonical_module(
                root.resolve(), root / "standalone.py", set()
            )
            self.assertIsNone(mod)


class TestParseImports(unittest.TestCase):
    def test_simple_import(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("import os\nimport sys\n")
            name = f.name
        try:
            refs = graphify.parse_imports(Path(name))
            kinds = [r.kind for r in refs]
            self.assertEqual(kinds, ["import", "import"])
            self.assertEqual(refs[0].names, ("os",))
            self.assertEqual(refs[1].names, ("sys",))
        finally:
            os.unlink(name)

    def test_from_import(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("from collections import OrderedDict\n")
            name = f.name
        try:
            refs = graphify.parse_imports(Path(name))
            self.assertEqual(len(refs), 1)
            self.assertEqual(refs[0].kind, "from")
            self.assertEqual(refs[0].module, "collections")
            self.assertEqual(refs[0].names, ("OrderedDict",))
        finally:
            os.unlink(name)

    def test_syntax_error_returns_empty(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("def foo(\n")  # incomplete
            name = f.name
        try:
            refs = graphify.parse_imports(Path(name))
            self.assertEqual(refs, [])
        finally:
            os.unlink(name)


class TestResolveRelativeImport(unittest.TestCase):
    def test_absolute(self):
        self.assertEqual(graphify.resolve_relative_import("pkg.mod", "os", 0), "os")

    def test_relative_same_level(self):
        self.assertEqual(graphify.resolve_relative_import("pkg.mod", "utils", 1), "pkg.utils")

    def test_relative_parent(self):
        self.assertEqual(graphify.resolve_relative_import("pkg.sub.mod", None, 2), "pkg")

    def test_relative_too_deep(self):
        self.assertIsNone(graphify.resolve_relative_import("pkg", "x", 2))


class TestCollectTreeNodes(unittest.TestCase):
    def test_smoke(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "src" / "models").mkdir(parents=True)
            (root / "src" / "main.py").write_text("")
            (root / "README.md").write_text("")
            (root / ".venv" / "bin").mkdir(parents=True)
            (root / ".venv" / "bin" / "python").write_text("")

            nodes, edges = graphify.collect_tree_nodes(root)
            self.assertIn("./", nodes)
            self.assertIn("src/", nodes)
            self.assertIn("src/main.py", nodes)
            self.assertIn("README.md", nodes)
            self.assertNotIn(".venv/", nodes)
            self.assertNotIn(".venv/bin/", nodes)
            self.assertNotIn(".venv/bin/python", nodes)


class TestBuildGraphIntegration(unittest.TestCase):
    def test_on_actual_repo(self):
        repo_root = Path(__file__).resolve().parents[1]
        graph = graphify.build_graph(repo_root)

        self.assertTrue(graph["python"]["nodes"])
        self.assertIn("tools/graphify.py", graph["python"]["nodes"])
        self.assertIn("./", graph["tree"]["nodes"])

        # Every edge endpoint must reference an existing node.
        for section in ("python", "tree"):
            node_set = set(graph[section]["nodes"])
            for edge in graph[section]["edges"]:
                self.assertIn(edge["from"], node_set, f"Missing node for edge.from in {section}")
                self.assertIn(edge["to"], node_set, f"Missing node for edge.to in {section}")

    def test_root_validation_missing(self):
        with self.assertRaises(FileNotFoundError):
            graphify.build_graph(Path("/definitely/does/not/exist"))

    def test_root_validation_not_dir(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            name = f.name
        try:
            with self.assertRaises(NotADirectoryError):
                graphify.build_graph(Path(name))
        finally:
            os.unlink(name)


class TestRenderMermaidNoCollisions(unittest.TestCase):
    def test_colliding_paths(self):
        graph: graphify.GraphDict = {
            "root": "/tmp",
            "python": {"nodes": [], "edges": []},
            "tree": {
                "nodes": ["Assets/Judicial precedent/", "Assets/Judicial_precedent/"],
                "edges": [],
            },
        }
        output = graphify.render_tree_mermaid(graph)
        ids = [line.split("[")[0].strip() for line in output.splitlines() if "[" in line]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate Mermaid IDs detected")


class TestWarnIfOversized(unittest.TestCase):
    def test_warning_emitted(self):
        graph: graphify.GraphDict = {
            "root": "/tmp",
            "python": {"nodes": ["a"] * 600, "edges": [{"from": "a", "to": "b"}]},
            "tree": {"nodes": [], "edges": []},
        }
        # Should not raise.
        graphify._warn_if_oversized(graph)


class TestSchemaVersion(unittest.TestCase):
    def test_json_has_schema_version(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "a.py").write_text("")
            graph = graphify.build_graph(root)

            json_path = root / "out.json"
            graphify.write_outputs(graph, root / "out.md", json_path)
            data = json.loads(json_path.read_text())
            self.assertEqual(data.get("schema_version"), "1.0")


if __name__ == "__main__":
    unittest.main()

