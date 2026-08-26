#!/usr/bin/env python3
"""Validate ARIA CAD workspace structure and release readiness."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
CONSTRAINTS_PATH = WORKSPACE / "ARIA-CONSTRAINTS.json"
OBJECT_MAP_PATH = WORKSPACE / "ARIA-OBJECT-MAP.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing required file: {path.relative_to(REPO_ROOT)}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON {path.relative_to(REPO_ROOT)}:{exc.lineno}:{exc.colno}: {exc.msg}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"top-level JSON must be an object: {path.relative_to(REPO_ROOT)}")
        return {}
    return value


def require(mapping: dict[str, Any], key: str, location: str, errors: list[str]) -> Any:
    if key not in mapping:
        errors.append(f"missing {location}.{key}")
        return None
    return mapping[key]


def validate_constraints(constraints: dict[str, Any], errors: list[str]) -> None:
    for key in ("schema_version", "document_id", "units", "repo_baseline", "execution_policy"):
        require(constraints, key, "constraints", errors)
    if constraints.get("units") != "mm":
        errors.append("constraints.units must be 'mm'")
    policy = constraints.get("execution_policy", {})
    if not isinstance(policy, dict) or policy.get("stop_on_critical_unknown") is not True:
        errors.append("execution_policy.stop_on_critical_unknown must be true")
    if isinstance(policy, dict) and policy.get("allow_unmapped_legacy_cad") is not False:
        errors.append("execution_policy.allow_unmapped_legacy_cad must be false")


def validate_object_map(
    object_map: dict[str, Any],
    errors: list[str],
    warnings: list[str],
) -> list[str]:
    resolver = object_map.get("resolver_policy", {})
    if resolver.get("match_key") != "FreeCAD Object.Name":
        errors.append("resolver_policy.match_key must be 'FreeCAD Object.Name'")
    if resolver.get("fuzzy_matching_allowed") is not False:
        errors.append("resolver_policy.fuzzy_matching_allowed must be false")

    documents = object_map.get("documents")
    if not isinstance(documents, list):
        errors.append("object map documents must be a list")
        documents = []
    document_ids: set[str] = set()
    for index, document in enumerate(documents):
        if not isinstance(document, dict):
            errors.append(f"documents[{index}] must be an object")
            continue
        document_id = document.get("document_id")
        if not document_id:
            errors.append(f"documents[{index}].document_id missing")
        elif document_id in document_ids:
            errors.append(f"duplicate document_id: {document_id}")
        else:
            document_ids.add(document_id)

    objects = object_map.get("objects")
    if not isinstance(objects, list):
        errors.append("object map objects must be a list")
        return []

    allowed_states = {"CAD_EXACT", "ASSEMBLY_LOCKED", "ENVELOPE_ONLY", "PENDING", "DESIGN_NEW"}
    object_ids: set[str] = set()
    critical_blockers: list[str] = []
    for index, item in enumerate(objects):
        location = f"objects[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{location} must be an object")
            continue
        object_id = item.get("object_id")
        if not object_id:
            errors.append(f"{location}.object_id missing")
            continue
        if object_id in object_ids:
            errors.append(f"duplicate object_id: {object_id}")
        object_ids.add(object_id)

        state = item.get("design_state")
        if state not in allowed_states:
            errors.append(f"{object_id}: invalid design_state {state!r}")
        if item.get("freecad_document") not in document_ids:
            errors.append(f"{object_id}: unknown freecad_document {item.get('freecad_document')!r}")
        names = item.get("freecad_object_names")
        if not isinstance(names, list):
            errors.append(f"{object_id}: freecad_object_names must be a list")
        elif len(names) != len(set(names)):
            errors.append(f"{object_id}: duplicate FreeCAD object names")

        source_files = item.get("source_files", [])
        if not isinstance(source_files, list):
            errors.append(f"{object_id}: source_files must be a list")
            continue
        for source_index, source in enumerate(source_files):
            if not isinstance(source, dict) or not source.get("path"):
                errors.append(f"{object_id}: source_files[{source_index}] missing path")
                continue
            path = REPO_ROOT / source["path"]
            if not path.is_file():
                errors.append(f"{object_id}: mapped repo source missing: {source['path']}")
                continue
            expected_hash = source.get("sha256")
            if expected_hash and expected_hash not in {"PENDING", "UNKNOWN"}:
                actual_hash = sha256_file(path)
                if actual_hash != str(expected_hash).upper():
                    errors.append(
                        f"{object_id}: SHA-256 mismatch for {source['path']}: "
                        f"expected {expected_hash}, got {actual_hash}"
                    )

        blockers = item.get("release_blockers", [])
        if not isinstance(blockers, list):
            errors.append(f"{object_id}: release_blockers must be a list")
            blockers = []
        if item.get("critical") is True and blockers:
            critical_blockers.extend(f"{object_id}: {blocker}" for blocker in blockers)

    if not any(item.get("design_state") == "ASSEMBLY_LOCKED" for item in objects if isinstance(item, dict)):
        errors.append("object map must contain the locked main compute/display assembly")
    if not any(item.get("design_state") == "DESIGN_NEW" for item in objects if isinstance(item, dict)):
        errors.append("object map must contain design-new geometry")
    if critical_blockers:
        warnings.append(f"{len(critical_blockers)} critical release blocker(s) remain")
    return critical_blockers


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-pending",
        action="store_true",
        help="validate structure but report critical release blockers as expected warnings",
    )
    args = parser.parse_args(argv[1:])

    errors: list[str] = []
    warnings: list[str] = []
    constraints = load_json(CONSTRAINTS_PATH, errors)
    object_map = load_json(OBJECT_MAP_PATH, errors)
    if constraints:
        validate_constraints(constraints, errors)
    blockers = validate_object_map(object_map, errors, warnings) if object_map else []

    result = {
        "workspace": str(WORKSPACE),
        "mode": "STRUCTURE_ALLOW_PENDING" if args.allow_pending else "STRICT_RELEASE_PREFLIGHT",
        "errors": errors,
        "warnings": warnings,
        "critical_release_blockers": blockers,
        "structure_valid": not errors,
        "release_ready": not errors and not blockers,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if errors:
        return 1
    if blockers and not args.allow_pending:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
