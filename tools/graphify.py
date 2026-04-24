#!/usr/bin/env python3
"""Generate a lightweight repo graph (Mermaid + JSON) for NexLexHub.

This module walks a repository, discovers Python files, resolves internal
import relationships, and renders both a directory tree and a Python import
graph as Mermaid diagrams.
"""
from __future__ import annotations

import argparse
import ast
import json
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Literal, TypedDict

logger = logging.getLogger("graphify")

IDENT_RE = re.compile(r"^[A-Za-z_]\w*$")

# Directory / file names that should never appear in the graph.
_EXCLUDED_PARTS: frozenset[str] = frozenset({
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".graphify",
    ".pytest_cache",
    ".mypy_cache",
    ".tox",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
})

_FILE_EXTS: frozenset[str] = frozenset({
    ".py", ".php", ".md", ".txt", ".yml", ".yaml", ".json",
})

# Extra file names that are always included regardless of extension.
_EXTRA_FILENAMES: frozenset[str] = frozenset({"requirements.txt"})


# ---------------------------------------------------------------------------
# TypedDict types for the graph structure
# ---------------------------------------------------------------------------
class EdgeDict(TypedDict):
    from_: str  # serialized as "from" in JSON
    to: str


class PythonGraphDict(TypedDict):
    nodes: list[str]
    edges: list[EdgeDict]


class TreeGraphDict(TypedDict):
    nodes: list[str]
    edges: list[EdgeDict]


class GraphDict(TypedDict):
    root: str
    python: PythonGraphDict
    tree: TreeGraphDict


# ---------------------------------------------------------------------------
# Import reference model
# ---------------------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class ImportRef:
    kind: Literal["import", "from"]
    module: str | None
    level: int
    names: tuple[str, ...]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _is_cache_or_artifact_dir(part: str) -> bool:
    """Return True if *part* is a directory/file name that should be skipped."""
    return part in _EXCLUDED_PARTS


def _resolve_root(path: str | Path) -> Path:
    """Validate that *path* exists and is a directory, then resolve it once."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Root path does not exist: {p}")
    if not p.is_dir():
        raise NotADirectoryError(f"Root path is not a directory: {p}")
    return p.resolve()


def _safe_read_source(py_file: Path) -> str | None:
    """Read a Python source file with robust encoding fallback.

    Returns ``None`` when the file cannot be read at all. Logs a warning
    for encoding issues but does not raise.
    """
    try:
        return py_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        logger.warning("Encoding fallback for %s", py_file)
        try:
            return py_file.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            logger.warning("Cannot read %s: %s", py_file, exc)
            return None
    except OSError as exc:
        logger.warning("Cannot read %s: %s", py_file, exc)
        return None


def _escape_mermaid_label(label: str) -> str:
    """Escape quotes and backslashes so Mermaid parses the label safely."""
    return label.replace("\\", "\\\\").replace('"', '\\"')


def _warn_if_oversized(graph: GraphDict, *, max_nodes: int = 500, max_edges: int = 1000) -> None:
    """Warn when graph dimensions may exceed typical Mermaid renderer limits."""
    for section in ("python", "tree"):
        n = len(graph[section]["nodes"])  # type: ignore[literal-required]
        e = len(graph[section]["edges"])  # type: ignore[literal-required]
        if n > max_nodes or e > max_edges:
            logger.warning(
                "Section %r is large (%d nodes, %d edges). "
                "Some Mermaid renderers may struggle.",
                section, n, e,
            )


def is_python_identifier_segment(segment: str) -> bool:
    return bool(IDENT_RE.match(segment))


# ---------------------------------------------------------------------------
# Python file discovery
# ---------------------------------------------------------------------------
def iter_python_files(root: Path) -> Iterator[Path]:
    """Yield every ``*.py`` file under *root*, skipping cache/artifact dirs."""
    for path in root.rglob("*.py"):
        if any(_is_cache_or_artifact_dir(part) for part in path.parts):
            continue
        if path.is_file():
            yield path


# ---------------------------------------------------------------------------
# Module name derivation
# ---------------------------------------------------------------------------
def file_to_canonical_module(
    root_resolved: Path,
    file_path: Path,
    package_dirs: set[Path],
) -> str | None:
    """Derive a likely import name for a file.

    This assumes the parent of the top-level package dir is on ``sys.path``.
    It intentionally ignores non-identifier directories above the package
    root (e.g. ``Assets/ai-legal-news-agent/ai/...`` → ``ai.*``).
    """
    file_path = file_path.resolve()
    if root_resolved not in file_path.parents and file_path != root_resolved:
        return None

    if file_path.name == "__init__.py":
        leaf_name = None
        current_dir = file_path.parent
    else:
        leaf_name = file_path.stem
        current_dir = file_path.parent

    package_parts: list[str] = []
    while current_dir in package_dirs and is_python_identifier_segment(current_dir.name):
        package_parts.append(current_dir.name)
        current_dir = current_dir.parent

    if not package_parts:
        return None

    package_parts.reverse()
    if leaf_name:
        package_parts.append(leaf_name)
    return ".".join(package_parts)


# ---------------------------------------------------------------------------
# Import parsing
# ---------------------------------------------------------------------------
def parse_imports(py_file: Path) -> list[ImportRef]:
    """Parse ``import`` / ``from ... import`` statements from a Python file."""
    source = _safe_read_source(py_file)
    if source is None:
        return []

    try:
        tree = ast.parse(source, filename=str(py_file))
    except SyntaxError as exc:
        logger.warning("Syntax error in %s: %s", py_file, exc)
        return []

    imports: list[ImportRef] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = tuple(alias.name for alias in node.names if alias.name)
            if names:
                imports.append(ImportRef(kind="import", module=None, level=0, names=names))
        elif isinstance(node, ast.ImportFrom):
            names = tuple(alias.name for alias in node.names if alias.name)
            imports.append(
                ImportRef(
                    kind="from",
                    module=node.module,
                    level=int(node.level or 0),
                    names=names,
                )
            )
    return imports


# ---------------------------------------------------------------------------
# Import resolution
# ---------------------------------------------------------------------------
def resolve_relative_import(from_module: str, module: str | None, level: int) -> str | None:
    if level <= 0:
        return module

    base_parts = from_module.split(".")
    if len(base_parts) < level:
        return None
    prefix = base_parts[: len(base_parts) - level]
    if module:
        prefix.extend(module.split("."))
    return ".".join(prefix) if prefix else None


def module_prefixes(module: str) -> Iterable[str]:
    parts = module.split(".")
    for i in range(len(parts), 0, -1):
        yield ".".join(parts[:i])


# ---------------------------------------------------------------------------
# Mermaid rendering helpers
# ---------------------------------------------------------------------------
def to_mermaid_id(text: str) -> str:
    """Sanitize *text* into a valid Mermaid node identifier."""
    safe = re.sub(r"[^A-Za-z0-9_]", "_", text)
    if not safe:
        return "n_empty"
    if safe[0].isdigit():
        safe = f"n_{safe}"
    return safe


def _unique_mermaid_id(base: str, used: set[str]) -> str:
    """Return a unique Mermaid ID, suffixing with ``_1``, ``_2`` on collision."""
    uid = base
    counter = 0
    while uid in used:
        counter += 1
        uid = f"{base}_{counter}"
    used.add(uid)
    return uid


def mermaid_node(node_id: str, label: str) -> str:
    escaped = _escape_mermaid_label(label)
    return f'{node_id}["{escaped}"]'


# ---------------------------------------------------------------------------
# Tree collection
# ---------------------------------------------------------------------------
def should_include_in_tree(path: Path) -> bool:
    if _is_cache_or_artifact_dir(path.name):
        return False
    if any(_is_cache_or_artifact_dir(part) for part in path.parts):
        return False
    return True


def collect_tree_nodes(root: Path) -> tuple[set[str], list[tuple[str, str]]]:
    """Collect directory-tree nodes and edges relative to *root*.

    Returns:
        - *nodes*: set of path strings (directories end with ``"/"``)
        - *edges*: list of ``(parent, child)`` tuples
    """
    nodes: set[str] = set()
    edges: list[tuple[str, str]] = []

    nodes.add("./")
    for dirpath, dirnames, filenames in os.walk(root):
        dpath = Path(dirpath)
        if not should_include_in_tree(dpath):
            dirnames[:] = []
            continue

        dirnames[:] = sorted([d for d in dirnames if should_include_in_tree(dpath / d)])
        filenames = sorted([f for f in filenames if should_include_in_tree(dpath / f)])

        rel_dir = dpath.relative_to(root)
        parent = "./" if str(rel_dir) == "." else f"{rel_dir.as_posix().rstrip('/')}/"
        nodes.add(parent)

        for d in dirnames:
            child = f"{(rel_dir / d).as_posix().rstrip('/')}/"
            nodes.add(child)
            edges.append((parent, child))

        for f in filenames:
            ext = Path(f).suffix.lower()
            if ext not in _FILE_EXTS and Path(f).name not in _EXTRA_FILENAMES:
                continue
            child = (rel_dir / f).as_posix()
            nodes.add(child)
            edges.append((parent, child))

    edges.sort()
    return nodes, edges


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------
def build_graph(root: Path) -> GraphDict:
    """Build the full repository graph for *root*."""
    root_resolved = _resolve_root(root)
    py_files = sorted(iter_python_files(root_resolved))

    logger.info("Found %d Python files under %s", len(py_files), root_resolved)

    package_dirs: set[Path] = set()
    for py_file in py_files:
        if py_file.name == "__init__.py":
            package_dirs.add(py_file.parent.resolve())

    module_to_paths: dict[str, set[str]] = {}
    path_to_module: dict[str, str] = {}
    for py_file in py_files:
        rel = py_file.relative_to(root_resolved).as_posix()
        mod = file_to_canonical_module(root_resolved, py_file, package_dirs)
        if not mod:
            continue
        module_to_paths.setdefault(mod, set()).add(rel)
        # If there are collisions, keep the first one deterministically.
        path_to_module.setdefault(rel, mod)

    nodes: set[str] = set(p.relative_to(root_resolved).as_posix() for p in py_files)
    edges: set[tuple[str, str]] = set()

    for idx, py_file in enumerate(py_files, start=1):
        src = py_file.relative_to(root_resolved).as_posix()
        from_mod = path_to_module.get(src)
        imports = parse_imports(py_file)

        for imp in imports:
            if imp.kind == "import":
                for name in imp.names:
                    for candidate in module_prefixes(name):
                        targets = module_to_paths.get(candidate)
                        if targets:
                            for t in targets:
                                edges.add((src, t))
                            break
            else:
                if imp.level and from_mod:
                    base = resolve_relative_import(from_mod, imp.module, imp.level)
                else:
                    base = imp.module
                if not base:
                    continue

                # Prefer linking ``from pkg import mod`` to ``pkg.mod`` if available.
                tried: list[str] = []
                for name in imp.names:
                    if name == "*":
                        continue
                    tried.append(f"{base}.{name}")
                tried.append(base)

                for raw in tried:
                    for candidate in module_prefixes(raw):
                        targets = module_to_paths.get(candidate)
                        if targets:
                            for t in targets:
                                edges.add((src, t))
                            break
                    else:
                        continue
                    break

        if idx % 50 == 0:
            logger.info("Processed %d/%d Python files", idx, len(py_files))

    tree_nodes, tree_edges = collect_tree_nodes(root_resolved)

    graph: GraphDict = {
        "root": str(root_resolved),
        "python": {
            "nodes": sorted(nodes),
            "edges": sorted(
                [{"from": a, "to": b} for (a, b) in edges],
                key=lambda x: (x["from"], x["to"]),
            ),
        },
        "tree": {
            "nodes": sorted(tree_nodes),
            "edges": [{"from": a, "to": b} for (a, b) in tree_edges],
        },
    }

    _warn_if_oversized(graph)
    return graph


# ---------------------------------------------------------------------------
# Mermaid rendering
# ---------------------------------------------------------------------------
def render_tree_mermaid(graph: GraphDict) -> str:
    nodes = graph["tree"]["nodes"]
    edges = graph["tree"]["edges"]

    used_ids: set[str] = set()
    node_ids: dict[str, str] = {}
    for p in nodes:
        node_ids[p] = _unique_mermaid_id(to_mermaid_id(f"tree_{p}"), used_ids)

    lines = ["flowchart LR"]
    for p in nodes:
        label = p
        lines.append(f"  {mermaid_node(node_ids[p], label)}")
    for e in edges:
        lines.append(f"  {node_ids[e['from']]} --> {node_ids[e['to']]}")
    return "\n".join(lines)


def render_python_mermaid(graph: GraphDict) -> str:
    nodes = graph["python"]["nodes"]
    edges = graph["python"]["edges"]

    used_ids: set[str] = set()
    node_ids: dict[str, str] = {}
    for p in nodes:
        node_ids[p] = _unique_mermaid_id(to_mermaid_id(f"py_{p}"), used_ids)

    lines = ["flowchart LR"]
    for p in nodes:
        lines.append(f"  {mermaid_node(node_ids[p], p)}")
    for e in edges:
        if e["from"] in node_ids and e["to"] in node_ids:
            lines.append(f"  {node_ids[e['from']]} --> {node_ids[e['to']]}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------
def write_outputs(graph: GraphDict, out_md: Path, out_json: Path | None) -> None:
    out_md.parent.mkdir(parents=True, exist_ok=True)
    if out_json:
        out_json.parent.mkdir(parents=True, exist_ok=True)

    py_nodes = len(graph["python"]["nodes"])
    py_edges = len(graph["python"]["edges"])
    tree_nodes = len(graph["tree"]["nodes"])
    tree_edges = len(graph["tree"]["edges"])

    md = [
        "# NexLexHub Graph",
        "",
        f"Generated by ``tools/graphify.py``.",
        "",
        "## Summary",
        "",
        f"- Repo tree: {tree_nodes} nodes, {tree_edges} edges",
        f"- Python imports: {py_nodes} files, {py_edges} edges",
        "",
        "## Repo Tree (filtered)",
        "",
        "```mermaid",
        render_tree_mermaid(graph),
        "```",
        "",
        "## Python Import Graph (internal only)",
        "",
        "```mermaid",
        render_python_mermaid(graph),
        "```",
        "",
    ]
    out_md.write_text("\n".join(md), encoding="utf-8")

    if out_json:
        payload = {
            "schema_version": "1.0",
            **graph,  # type: ignore[typeddict-item]
        }
        out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a lightweight repo graph (Mermaid + JSON).")
    parser.add_argument("--root", default=".", help="Root directory to graphify.")
    parser.add_argument("--out", default="GRAPH.md", help="Markdown output path.")
    parser.add_argument("--json", default=".graphify/graph.json", help="Optional JSON output path.")
    parser.add_argument("--no-json", action="store_true", help="Disable JSON output.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
    args = parser.parse_args(argv)

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    root = Path(args.root)
    out_md = Path(args.out)
    out_json = None if args.no_json else Path(args.json)

    try:
        graph = build_graph(root)
    except (FileNotFoundError, NotADirectoryError) as exc:
        logger.error("%s", exc)
        return 2

    write_outputs(graph, out_md, out_json)
    logger.info("Graph written to %s", out_md)
    if out_json:
        logger.info("JSON written to %s", out_json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

