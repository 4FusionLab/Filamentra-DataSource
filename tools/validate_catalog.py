#!/usr/bin/env python3
"""Validate Filamentra manufacturer data, visual presets, and stable IDs.

Requires: pip install jsonschema
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def validate_schema(schema_path: Path, data: dict, label: str, errors: list[str]) -> None:
    schema = read_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for problem in sorted(validator.iter_errors(data), key=lambda issue: str(issue.path)):
        path = "/".join(str(piece) for piece in problem.path) or "<root>"
        errors.append(f"{label} ({path}): {problem.message}")


def main() -> int:
    errors: list[str] = []
    line_schema = CATALOG / "schema" / "line.schema.json"
    preset_schema = CATALOG / "schema" / "preset.schema.json"
    brands_dir = CATALOG / "brands"
    presets_dir = CATALOG / "presets"

    brands: set[str] = set()
    lines: set[str] = set()
    full_colors: set[str] = set()
    presets: set[str] = set()

    for path in sorted(presets_dir.glob("*.json")):
        try:
            obj = read_json(path)
            validate_schema(preset_schema, obj, str(path.relative_to(ROOT)), errors)
            ident = obj.get("id")
            if ident != path.stem:
                errors.append(f"{path}: preset ID must equal filename")
            if ident in presets:
                errors.append(f"{path}: duplicate preset ID {ident}")
            presets.add(ident)
        except Exception as exc:
            errors.append(f"{path}: cannot parse/validate preset: {exc}")

    for directory in sorted(brands_dir.iterdir()):
        if not directory.is_dir():
            continue
        brand_path = directory / "brand.json"
        try:
            brand = read_json(brand_path)
            ident = brand.get("id")
            if ident != directory.name:
                errors.append(f"{brand_path}: brand ID must equal directory name")
            if not isinstance(brand.get("name"), str) or not brand["name"].strip():
                errors.append(f"{brand_path}: missing manufacturer name")
            if not str(brand.get("website", "")).startswith("https://"):
                errors.append(f"{brand_path}: brand website must be HTTPS")
            if ident in brands:
                errors.append(f"{brand_path}: duplicate brand ID {ident}")
            brands.add(ident)
        except Exception as exc:
            errors.append(f"{brand_path}: missing or invalid manufacturer: {exc}")
            continue

        for path in sorted(directory.glob("*.json")):
            if path.name == "brand.json":
                continue
            try:
                obj = read_json(path)
                rel = str(path.relative_to(ROOT))
                validate_schema(line_schema, obj, rel, errors)
                line_id = obj.get("id")
                if line_id != f"{ident}/{path.stem}":
                    errors.append(f"{rel}: line ID must equal brand/filename")
                if obj.get("brand") != ident:
                    errors.append(f"{rel}: unknown or mismatched manufacturer")
                if line_id in lines:
                    errors.append(f"{rel}: duplicate line ID {line_id}")
                lines.add(line_id)
                profile_id = obj.get("appearance_preset")
                if profile_id is not None and profile_id not in presets:
                    errors.append(f"{rel}: unknown visual preset {profile_id}")
                for scope in [obj] + obj.get("colors", []):
                    overrides = scope.get("appearance") or {}
                    sources = scope.get("appearance_sources") or {}
                    for field in overrides:
                        if field not in sources:
                            errors.append(f"{rel}: override {field!r} missing appearance_sources entry")
                    for field in sources:
                        if field not in overrides:
                            errors.append(f"{rel}: orphan appearance_sources field {field!r}")
                color_codes: set[str] = set()
                for color in obj.get("colors", []):
                    color_id = color.get("id")
                    full_id = f"{line_id}/{color_id}"
                    if full_id in full_colors:
                        errors.append(f"{rel}: duplicate full color ID {full_id}")
                    full_colors.add(full_id)
                    code = color.get("manufacturer_color_code")
                    if code is not None:
                        if code in color_codes:
                            errors.append(f"{rel}: duplicate manufacturer color code {code}")
                        color_codes.add(code)
                    if color.get("hex_source") == "manufacturer" and not color.get("source_url"):
                        errors.append(f"{rel}: manufacturer HEX without source URL: {full_id}")
                    visual_status = color.get("visual_data_status")
                    has_hex = "hex" in color
                    swatches = color.get("rgba_swatches") or []
                    mode = color.get("color_mode")
                    if visual_status == "name_only" and (has_hex or swatches):
                        errors.append(f"{rel}: name_only color has numeric swatch: {full_id}")
                    if visual_status == "manufacturer_swatch" and not (has_hex or swatches):
                        errors.append(f"{rel}: manufacturer_swatch color missing numeric swatch: {full_id}")
                    if visual_status == "manufacturer_swatch" and color.get("hex_source") in ("estimated", "measured"):
                        errors.append(f"{rel}: claimed manufacturer swatch has incompatible HEX provenance: {full_id}")
                    if visual_status in ("estimated", "measured") and has_hex and color.get("hex_source") != visual_status:
                        errors.append(f"{rel}: visual status disagrees with HEX source: {full_id}")
                    if mode == "solid" and len(swatches) > 1:
                        errors.append(f"{rel}: solid shade has several RGBA swatches: {full_id}")
                    if mode in ("gradient", "multicolor") and has_hex:
                        errors.append(f"{rel}: multicolor shade must not be reduced to one primary HEX: {full_id}")
                    if len(swatches) == 1 and has_hex and swatches[0][:7].upper() != color["hex"].upper():
                        errors.append(f"{rel}: HEX disagrees with manufacturer RGBA swatch: {full_id}")
            except Exception as exc:
                errors.append(f"{path}: cannot parse/validate line: {exc}")

    if errors:
        print("Catalog validation failed:")
        for item in errors:
            print(" -", item)
        return 1
    print(f"Catalog OK: {len(brands)} manufacturers, {len(lines)} product lines, "
          f"{len(full_colors)} color variants, {len(presets)} visual presets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
