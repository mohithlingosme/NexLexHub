# Implementation Plan: Refactor `tools/graphify.py`

## Overview
Refactor `tools/graphify.py` into a production-quality, maintainable module with robust error handling, comprehensive type safety, progress observability, and automated tests.

The current script works for small-to-medium repos but silently drops broken Python files, lacks type safety for its output contract, redundantly resolves filesystem paths, and omits common cache/artifact directories from exclusion lists. This plan addresses all identified issues while preserving backward-compatible CLI behavior.

## Types

### `GraphDict` (TypedDict)
```python
class GraphDict(TypedDict):
    root: str
    python: PythonGraphDict
    tree: TreeGraphDict
```

### `PythonGraphDict` (TypedDict)
```python
class PythonGraphDict(TypedDict):
    nodes: list[str]
    edges: list[EdgeDict]
```

### `TreeGraphDict` (TypedDict)
```python
class TreeGraphDict(TypedDict):
    nodes: list[str]
    edges: list[EdgeDict]
```

### `EdgeDict` (TypedDict)
```python
class EdgeDict(TypedDict):
    from_: str  # Note: serialized as "from" in JSON
    to: str
```

### `ImportRef` (existing dataclass — enhanced)
```python
@dataclass(frozen=True, slots=True)
class ImportRef:
    kind: Literal["import", "from"]
    module: str | None
    level: int
    names: tuple[str, ...]
```

## Files

- **`tools/graphify.py`** — Complete refactor with all changes listed below.
- **`tools/test_graphify.py`** — New test suite covering unit and integration scenarios.
- **`tools/implementation_plan.md`** — This document (read-only after creation).

## Functions

### New Functions

| Name | Signature | Purpose |
|------|-----------|---------|
| `_resolve_root` | `(path: str \| Path) -> Path` | Validate root exists, is a directory, resolve once, cache result. |
| `_is_cache_or_artifact_dir` | `(part: str) -> bool` | Centralized check for excluded directory names (`.venv`, `node_modules`, `.mypy_cache`, etc.). |
| `_safe_read_source` | `(py_file: Path) -> str \| None` | Read file with robust encoding fallback; log warnings on failure; return None instead of empty list. |
| `_escape_mermaid_label` | `(label: str) -> str` | Escape quotes **and** backslashes for Mermaid compatibility. |
| `_warn_if_oversized` | `(graph: GraphDict) -> None` | Emit warnings if node/edge counts exceed safe Mermaid renderer limits. |

### Modified Functions

| Name | Changes |
|------|---------|
| `iter_python_files` | Use `_is_cache_or_artifact_dir` instead of inline set; add `.mypy_cache`, `.tox`, `node_modules`, `.idea`, `dist`, `build`, `*.egg-info` to exclusions. |
| `should_include_in_tree` | Use `_is_cache_or_artifact_dir`; remove redundant `path.parts` check. |
| `file_to_canonical_module` | Accept pre-resolved `root_resolved: Path` parameter to avoid re-resolving inside the hot loop. |
| `parse_imports` | Use `_safe_read_source`; log warning with filepath on SyntaxError instead of silent return. |
| `collect_tree_nodes` | Remove unnecessary `add_node` inner function; inline `nodes.add(p)`. |
| `to_mermaid_id` | Handle empty-string input: return `"n_empty"` instead of `"n_"`. |
| `build_graph` | Accept optional `logger` parameter; add progress logging every 50 files; call `_warn_if_oversized` before return. |
| `render_tree_mermaid` | Use `_escape_mermaid_label` for labels. |
| `render_python_mermaid` | Use `_escape_mermaid_label` for labels. |
| `write_outputs` | Add JSON schema version key `"schema_version": "1.0"` to output. |

### Removed Functions

| Name | Reason |
|------|--------|
| `add_node` (inner) | Trivial one-liner wrapper adds no abstraction value. |

## Classes

No new classes. `ImportRef` gains `slots=True` for memory efficiency. `frozen=True` is retained.

## Dependencies

No new external packages required. The refactor uses only standard library additions:
- `typing.TypedDict` (Python 3.8+)
- `typing.Literal` (Python 3.8+)
- `logging` (standard library)

## Testing

### `tools/test_graphify.py` — New Test Suite

1. **test_to_mermaid_id_escapes** — Verify special characters, leading digits, empty string.
2. **test_unique_mermaid_id_deduplicates** — Verify `_1`, `_2` suffix generation.
3. **test_is_cache_or_artifact_dir** — Verify all excluded patterns are caught.
4. **test_safe_read_source_missing_file** — Returns None, no exception.
5. **test_safe_read_source_bad_encoding** — Falls back to replacement characters.
6. **test_file_to_canonical_module** — Verify package detection, non-identifier skip, root file handling.
7. **test_parse_imports_syntax_error** — Logs warning, returns empty list.
8. **test_parse_imports_complex_imports** — Handles `import a.b.c`, `from . import x`, `from ..pkg import y`.
9. **test_build_graph_smoke** — Integration test on the actual repo; asserts node counts > 0, all edges reference existing nodes.
10. **test_mermaid_render_no_collisions** — Generate Mermaid for a synthetic graph with colliding paths; assert no duplicate IDs in output.
11. **test_escape_mermaid_label** — Quotes and backslashes are properly escaped.

## Implementation Order

1. Add `TypedDict` types and `Literal` imports at top of file.
2. Add `_is_cache_or_artifact_dir`, `_resolve_root`, `_safe_read_source`, `_escape_mermaid_label`, `_warn_if_oversized` helpers.
3. Update `ImportRef` to use `slots=True` and `Literal`.
4. Refactor `iter_python_files` and `should_include_in_tree` to use new helper.
5. Refactor `file_to_canonical_module` to accept cached resolved root.
6. Update `parse_imports` with `_safe_read_source` and logging.
7. Inline `add_node` in `collect_tree_nodes`; simplify.
8. Fix `to_mermaid_id` empty-string edge case.
9. Add progress logging to `build_graph`.
10. Update both `render_*_mermaid` functions with `_escape_mermaid_label`.
11. Add schema version to JSON output in `write_outputs`.
12. Create `tools/test_graphify.py` with full test suite.
13. Run tests and `py_compile` to verify.
14. Regenerate `GRAPH.md` and `.graphify/graph.json` to validate end-to-end.

