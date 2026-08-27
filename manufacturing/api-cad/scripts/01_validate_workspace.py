#!/usr/bin/env python3
"""Validate ARIA CAD workspace structure, layout readiness and final release gates."""

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
    for key in (
        "schema_version",
        "document_id",
        "units",
        "repo_baseline",
        "execution_policy",
        "readiness",
    ):
        require(constraints, key, "constraints", errors)
    if constraints.get("units") != "mm":
        errors.append("constraints.units must be 'mm'")

    policy = constraints.get("execution_policy", {})
    if not isinstance(policy, dict):
        errors.append("execution_policy must be an object")
        return
    if policy.get("pending_does_not_imply_blocking") is not True:
        errors.append("execution_policy.pending_does_not_imply_blocking must be true")
    if policy.get("continue_layout_with_approved_placeholder") is not True:
        errors.append("execution_policy.continue_layout_with_approved_placeholder must be true")
    if policy.get("placeholder_may_drive_final_mating_geometry") is not False:
        errors.append("execution_policy.placeholder_may_drive_final_mating_geometry must be false")
    if policy.get("allow_unmapped_legacy_cad") is not False:
        errors.append("execution_policy.allow_unmapped_legacy_cad must be false")

    readiness = constraints.get("readiness", {})
    if readiness.get("layout") != "READY_WITH_PLACEHOLDERS":
        errors.append("constraints.readiness.layout must be READY_WITH_PLACEHOLDERS")


def validate_repo_sources(object_id: str, sources: Any, errors: list[str]) -> None:
    if sources is None:
        return
    if not isinstance(sources, list):
        errors.append(f"{object_id}: source_files must be a list")
        return
    for index, source in enumerate(sources):
        if not isinstance(source, dict) or not source.get("path"):
            errors.append(f"{object_id}: source_files[{index}] missing path")
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


def dependency_ids(raw: Any) -> list[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        return [part.strip() for part in raw.split(",") if part.strip()]
    if isinstance(raw, list) and all(isinstance(item, str) for item in raw):
        return raw
    return []


def validate_object_map(
    object_map: dict[str, Any],
    errors: list[str],
    warnings: list[str],
) -> tuple[list[str], list[str], int]:
    resolver = object_map.get("resolver_policy", {})
    if resolver.get("exact_import_match_key") != "FreeCAD Object.Name":
        errors.append("resolver_policy.exact_import_match_key must be 'FreeCAD Object.Name'")
    if resolver.get("fuzzy_matching_allowed") is not False:
        errors.append("resolver_policy.fuzzy_matching_allowed must be false")

    gate_policy = object_map.get("gate_policy", {})
    if gate_policy.get("pending_is_automatically_blocking") is not False:
        errors.append("gate_policy.pending_is_automatically_blocking must be false")
    if gate_policy.get("final_blocking_field") != "true_blockers_final":
        errors.append("gate_policy.final_blocking_field must be true_blockers_final")

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
        return [], [], 0

    allowed_states = {"CAD_EXACT", "ASSEMBLY_LOCKED", "ENVELOPE_ONLY", "PENDING", "DESIGN_NEW"}
    ready_states = {
        "READY_WITH_REAL_ASSEMBLY_OR_PLACEHOLDER",
        "READY_WITH_APPROVED_PLACEHOLDER",
        "READY_WITH_DERIVED_PLACEHOLDER",
        "READY_WITH_LOCKED_ENVELOPE",
        "READY_WITH_LOCKED_INTERFACE",
        "READY_TO_DESIGN_PARAMETRIC",
    }
    blocked_state = "BLOCKED_NO_AUTHORITY_OR_FALLBACK"
    object_ids: set[str] = set()
    pending_dependencies: list[tuple[str, str]] = []
    layout_blockers: list[str] = []
    true_blockers: list[str] = []
    non_blocking_count = 0

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

        if "critical" in item or "release_blockers" in item:
            errors.append(f"{object_id}: legacy critical/release_blockers fields are forbidden")

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

        readiness = item.get("layout_readiness")
        if readiness == blocked_state:
            layout_blockers.append(f"{object_id}: no assembly, envelope, constraint or fallback")
        elif readiness not in ready_states:
            errors.append(f"{object_id}: invalid layout_readiness {readiness!r}")
        else:
            non_blocking_count += 1
            if not item.get("placeholder") and state != "CAD_EXACT":
                errors.append(f"{object_id}: ready item must define placeholder/authority")

        blockers = item.get("true_blockers_final")
        if not isinstance(blockers, list) or not all(isinstance(value, str) for value in blockers):
            errors.append(f"{object_id}: true_blockers_final must be a string list")
            blockers = []
        true_blockers.extend(f"{object_id}: {blocker}" for blocker in blockers)

        validate_repo_sources(object_id, item.get("source_files"), errors)
        for dependency in dependency_ids(item.get("depends_on_verified_definition")):
            pending_dependencies.append((object_id, dependency))

    for object_id, dependency in pending_dependencies:
        if dependency not in object_ids:
            errors.append(f"{object_id}: unknown depends_on_verified_definition {dependency!r}")

    if layout_blockers:
        warnings.append(f"{len(layout_blockers)} layout blocker(s) remain")
    else:
        warnings.append("layout gate is ready: every object has an approved authority or fallback")
    if true_blockers:
        warnings.append(f"{len(true_blockers)} true blocker(s) remain for dependent final manufacture")
    return layout_blockers, true_blockers, non_blocking_count


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stage",
        choices=("structure", "layout", "final-release"),
        default="layout",
        help="gate to evaluate; default is layout",
    )
    args = parser.parse_args(argv[1:])

    errors: list[str] = []
    warnings: list[str] = []
    constraints = load_json(CONSTRAINTS_PATH, errors)
    object_map = load_json(OBJECT_MAP_PATH, errors)
    if constraints:
        validate_constraints(constraints, errors)
    if object_map:
        layout_blockers, true_blockers, non_blocking_count = validate_object_map(
            object_map, errors, warnings
        )
    else:
        layout_blockers, true_blockers, non_blocking_count = [], [], 0

    layout_ready = not errors and not layout_blockers
    final_release_ready = layout_ready and not true_blockers
    result = {
        "workspace": str(WORKSPACE),
        "stage": args.stage,
        "errors": errors,
        "warnings": warnings,
        "non_blocking_layout_objects": non_blocking_count,
        "layout_blockers": layout_blockers,
        "true_blockers_final": true_blockers,
        "structure_valid": not errors,
        "layout_ready": layout_ready,
        "final_release_ready": final_release_ready,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if errors:
        return 1
    if args.stage == "layout" and layout_blockers:
        return 2
    if args.stage == "final-release" and (layout_blockers or true_blockers):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
