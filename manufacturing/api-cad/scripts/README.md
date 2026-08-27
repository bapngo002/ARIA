# CAD workspace scripts

- `00_scan_freecad.py`: read-only FCStd scan. Run with `FreeCADCmd`, not ordinary Python.
- `01_validate_workspace.py`: validates both JSON files, repo-backed file hashes/paths, layout fallbacks and true final-manufacturing blockers. It uses Python standard library only.

Examples from `manufacturing/api-cad/`:

```text
FreeCADCmd scripts/00_scan_freecad.py input/cad/ARIA-final-working.FCStd output/reports/freecad-scan.json
python scripts/01_validate_workspace.py --stage structure
python scripts/01_validate_workspace.py --stage layout
python scripts/01_validate_workspace.py --stage final-release
```

The layout command must pass when every object has an assembly, envelope, constraint placeholder or adjustable/open interface. The final-release command remains non-zero only while `TRUE_BLOCKER` data required for dependent manufacturing interfaces is unresolved.
