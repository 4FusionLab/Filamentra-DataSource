#!/usr/bin/env python3
"""Generate a static browsable Filamentra catalog from validated JSON sources."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from generate_material_previews import build_material_previews, numeric_color, preview_path
from generate_texture_maps import build_textures

from generate_texture_maps import build_textures

ROOT = Path(__file__).resolve().parents[1]
BRANDS = ROOT / "catalog" / "brands"
DEMO = ROOT / "demo"


def public_color(color: dict, line_id: str, preset_id: str | None) -> dict:
    swatches = color.get("rgba_swatches") or []
    hexadecimal = color.get("hex")
    status = color.get("visual_data_status") or (
        "manufacturer_swatch" if hexadecimal or swatches else "name_only"
    )
    fields = ("id", "name", "hex", "rgba_swatches", "color_mode",
              "hex_source", "manufacturer_color_code",
              "manufacturer_palette_code", "source_url", "verified_on",
              "visual_note", "color_reference_url", "color_reference_note",
              "measured_sample", "evidence",
              "appearance", "appearance_sources")
    result = {key: color[key] for key in fields if key in color}
    result["visual_data_status"] = status
    if preset_id and numeric_color(result):
        result["preview_image"] = preview_path(line_id, result["id"])
    return result


def make_catalog() -> dict:
    brands = []
    lines = []
    presets = {}

    for path in sorted((ROOT / "catalog" / "presets").glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        presets[doc["id"]] = {
            "name": doc.get("name", doc["id"]),
            "status": doc.get("status", "uncalibrated"),
            "appearance": doc.get("appearance", {}),
        }

    for folder in sorted(BRANDS.iterdir()):
        if not folder.is_dir() or not (folder / "brand.json").exists():
            continue
        brand = json.loads((folder / "brand.json").read_text(encoding="utf-8"))
        brands.append({
            "id": brand["id"], "name": brand["name"],
            "website": brand.get("website"),
        })
        for file in sorted(folder.glob("*.json")):
            if file.name == "brand.json":
                continue
            line = json.loads(file.read_text(encoding="utf-8"))
            lines.append({
                "id": line["id"], "brand": line["brand"],
                "name": line["name"], "polymer": line["polymer"],
                "finish": line.get("finish", "standard"),
                "effects": line.get("effects", []),
                "appearance_preset": line.get("appearance_preset"),
                "source_url": line.get("source_url"),
                "catalog_status": line.get("catalog_status", "unknown"),
                "appearance": line.get("appearance", {}),
                "colors": [public_color(c, line["id"], line.get("appearance_preset")) for c in line["colors"]],
            })

    # Research-only manufacturers are not shown until a numeric color-bearing line exists.
    active_brands = {line["brand"] for line in lines}
    brands = [brand for brand in brands if brand["id"] in active_brands]

    favored = {"bambu-lab": 0, "esun": 1, "sunlu": 2}
    brands.sort(key=lambda item: (favored.get(item["id"], 9), item["name"].lower()))
    positions = {brand["id"]: index for index, brand in enumerate(brands)}
    lines.sort(key=lambda item: (
        positions[item["brand"]], item["polymer"], item["name"].lower()))
    colors = [color for line in lines for color in line["colors"]]
    with_swatch = sum(bool(c.get("hex") or c.get("rgba_swatches") or c.get("measured_sample")) for c in colors)
    estimated = sum(c.get("hex_source") == "estimated" and not c.get("measured_sample") for c in colors)
    manufacturer = sum(bool(c.get("rgba_swatches")) or c.get("hex_source") == "manufacturer" for c in colors)
    measured = sum(bool(c.get("measured_sample")) for c in colors)
    curated = sum(bool(c.get("measured_sample")) or bool(c.get("rgba_swatches")) or c.get("hex_source") == "manufacturer" for c in colors)
    multicolor = sum(c.get("color_mode") in ("multicolor", "gradient") for c in colors)
    return {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "distribution": "validated GitHub Pages CI snapshot",
            "counts": {
                "brands": len(brands), "lines": len(lines), "colors": len(colors),
                "with_swatch": with_swatch,
                "manufacturer_swatch": manufacturer,
                "measured_samples": measured,
                "curated_preview": curated,
                "estimated": estimated,
                "name_only": len(colors) - with_swatch,
                "multicolor": multicolor,
            },
        },
        "brands": brands, "lines": lines, "presets": presets,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    destination = args.out.resolve()
    if destination == ROOT or ROOT not in destination.parents:
        parser.error("Output directory must be inside the repository and not its root")
    payload = make_catalog()
    if not payload["lines"]:
        raise SystemExit("Catalog is empty; refusing to build demo")

    destination.mkdir(parents=True, exist_ok=True)
    (destination / "assets").mkdir(exist_ok=True)
    (destination / "data").mkdir(exist_ok=True)
    shutil.copy2(DEMO / "index.html", destination / "index.html")
    shutil.copy2(DEMO / "app.css", destination / "assets" / "app.css")
    shutil.copy2(DEMO / "app.js", destination / "assets" / "app.js")
    build_textures(destination)
    preview_count = build_material_previews(payload, destination)
    payload["meta"]["counts"]["material_previews"] = preview_count
    (destination / "data" / "catalog.json").write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    (destination / ".nojekyll").write_text("", encoding="utf-8")
    print("Filamentra demo:", payload["meta"]["counts"], "->", destination)


if __name__ == "__main__":
    main()
