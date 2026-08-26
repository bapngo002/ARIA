# CAD workspace scripts

- `00_scan_freecad.py`: read-only FCStd scan. Run with `FreeCADCmd`, not ordinary Python.
- `01_validate_workspace.py`: validates both JSON files, repo-backed file hashes/paths and release blockers. It uses Python standard library only.

Examples from `manufacturing/api-cad/`:

```text
FreeCADCmd scripts/00_scan_freecad.py input/cad/ARIA-final-working.FCStd output/reports/freecad-scan.json
python scripts/01_validate_workspace.py --allow-pending
python scripts/01_validate_workspace.py
```

The final command is strict release preflight and must remain non-zero while critical blockers exist.
