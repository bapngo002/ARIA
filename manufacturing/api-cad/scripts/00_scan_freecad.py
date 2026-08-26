#!/usr/bin/env python3
"""Read an FCStd file and emit a deterministic object inventory.

Run with FreeCADCmd. This script never saves or changes the source document.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import FreeCAD as App
except ImportError as exc:  # pragma: no cover - requires FreeCAD runtime
    raise SystemExit(
        "FreeCAD module is unavailable. Run this script with FreeCADCmd."
    ) from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def vector(value: Any) -> list[float]:
    return [round(float(value.x), 6), round(float(value.y), 6), round(float(value.z), 6)]


def placement_payload(obj: Any) -> dict[str, Any] | None:
    placement = getattr(obj, "Placement", None)
    if placement is None:
        return None
    rotation = placement.Rotation
    quaternion = rotation.Q
    return {
        "base_mm": vector(placement.Base),
        "quaternion_xyzw": [round(float(component), 9) for component in quaternion],
    }


def shape_payload(obj: Any) -> dict[str, Any]:
    shape = getattr(obj, "Shape", None)
    if shape is None:
        return {"has_shape": False, "is_null": None, "bounding_box_mm": None}

    try:
        is_null = bool(shape.isNull())
        if is_null:
            return {"has_shape": True, "is_null": True, "bounding_box_mm": None}
        bounds = shape.BoundBox
        return {
            "has_shape": True,
            "is_null": False,
            "bounding_box_mm": {
                "min": [
                    round(float(bounds.XMin), 6),
                    round(float(bounds.YMin), 6),
                    round(float(bounds.ZMin), 6),
                ],
                "max": [
                    round(float(bounds.XMax), 6),
                    round(float(bounds.YMax), 6),
                    round(float(bounds.ZMax), 6),
                ],
                "size": [
                    round(float(bounds.XLength), 6),
                    round(float(bounds.YLength), 6),
                    round(float(bounds.ZLength), 6),
                ],
            },
        }
    except Exception as exc:  # pragma: no cover - depends on malformed CAD
        return {
            "has_shape": True,
            "is_null": None,
            "bounding_box_mm": None,
            "shape_error": f"{type(exc).__name__}: {exc}",
        }


def object_payload(obj: Any) -> dict[str, Any]:
    parents = sorted(parent.Name for parent in getattr(obj, "InList", []) if parent)
    children = sorted(child.Name for child in getattr(obj, "OutList", []) if child)
    return {
        "name": obj.Name,
        "label": obj.Label,
        "type_id": obj.TypeId,
        "parents": parents,
        "children": children,
        "visibility": bool(getattr(getattr(obj, "ViewObject", None), "Visibility", True)),
        "placement": placement_payload(obj),
        "shape": shape_payload(obj),
    }


def bbox_signature(item: dict[str, Any]) -> tuple[float, float, float] | None:
    bounds = item["shape"].get("bounding_box_mm")
    if not bounds:
        return None
    return tuple(bounds["size"])


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "Usage: FreeCADCmd 00_scan_freecad.py <input.FCStd> <report.json>",
            file=sys.stderr,
        )
        return 2

    source = Path(argv[1]).expanduser().resolve()
    report_path = Path(argv[2]).expanduser().resolve()
    if not source.is_file():
        print(f"Input file not found: {source}", file=sys.stderr)
        return 2

    document = None
    try:
        document = App.openDocument(str(source))
        document.recompute()
        objects = sorted((object_payload(obj) for obj in document.Objects), key=lambda item: item["name"])

        label_counts = Counter(item["label"] for item in objects)
        duplicate_labels = {
            label: sorted(item["name"] for item in objects if item["label"] == label)
            for label, count in sorted(label_counts.items())
            if count > 1
        }

        bboxes: dict[tuple[float, float, float], list[str]] = defaultdict(list)
        for item in objects:
            signature = bbox_signature(item)
            if signature is not None:
                bboxes[signature].append(item["name"])
        duplicate_bbox_sizes = [
            {"size_mm": list(size), "object_names": sorted(names)}
            for size, names in sorted(bboxes.items())
            if len(names) > 1
        ]

        report = {
            "schema_version": "1.0.0",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "freecad_version": ".".join(str(part) for part in App.Version()),
            "source": {
                "path": str(source),
                "sha256": sha256_file(source),
                "size_bytes": source.stat().st_size,
            },
            "document": {
                "name": document.Name,
                "label": document.Label,
                "object_count": len(objects),
            },
            "duplicate_labels": duplicate_labels,
            "duplicate_bounding_box_sizes": duplicate_bbox_sizes,
            "objects": objects,
        }
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Scanned {len(objects)} objects -> {report_path}")
        return 0
    except Exception as exc:  # pragma: no cover - depends on input CAD
        print(f"FreeCAD scan failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    finally:
        if document is not None:
            App.closeDocument(document.Name)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
