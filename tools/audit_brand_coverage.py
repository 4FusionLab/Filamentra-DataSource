#!/usr/bin/env python3
"""Auditable per-brand completeness counts, separate from manufacturer market coverage.

No web data, names-as-colors, guessed HEX, or catalog mutations.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANDS = ROOT / "catalog" / "brands"


def _is_numeric(color: dict) -> bool:
    return bool(color.get("hex") or color.get("rgba_swatches") or color.get("measured_sample"))


def scan() -> dict:
    brands: list[dict] = []
    for folder in sorted(BRANDS.iterdir()):
        if not folder.is_dir():
            continue
        metadata = folder / "brand.json"
        if not metadata.is_file():
            continue
        brand = json.loads(metadata.read_text(encoding="utf-8"))
        item = {
            "id": brand["id"],
            "name": brand["name"],
            "lines": 0,
            "colors": 0,
            "manufacturer_swatch": 0,
            "measured": 0,
            "estimated": 0,
            "name_only": 0,
            "has_sku": 0,
            "line_details": [],
        }
        for path in sorted(folder.glob("*.json")):
            if path.name == "brand.json":
                continue
            line = json.loads(path.read_text(encoding="utf-8"))
            if line.get("polymer") not in ("PLA", "PETG"):
                continue
            counts = {"colors": 0, "manufacturer_swatch": 0, "measured": 0,
                      "estimated": 0, "name_only": 0, "has_sku": 0}
            for color in line.get("colors", []):
                counts["colors"] += 1
                visual = color.get("visual_data_status")
                # Legacy official Bambu/eSUN/SUNLU swatches may omit
                # visual_data_status; derive quality from source fields, just
                # as build_demo.py does. Measurement wins over official RGB
                # when a record contains both (avoid double counting).
                if not _is_numeric(color):
                    counts["name_only"] += 1
                elif color.get("measured_sample"):
                    counts["measured"] += 1
                elif color.get("rgba_swatches") or color.get("hex_source") == "manufacturer":
                    counts["manufacturer_swatch"] += 1
                elif color.get("hex_source") == "estimated" or visual == "estimated":
                    counts["estimated"] += 1
                else:
                    raise ValueError(f"Unrecognized numeric quality: {path}: {color['id']} ({visual})")
                if any(variant.get("sku") for variant in color.get("variants", [])):
                    counts["has_sku"] += 1
            if counts["colors"] != (counts["manufacturer_swatch"] + counts["measured"]
                                    + counts["estimated"] + counts["name_only"]):
                raise ValueError(f"Overlapping/unknown quality states: {path}")
            item["lines"] += 1
            for key, value in counts.items():
                item[key] += value
            item["line_details"].append({
                "id": line["id"], "name": line["name"], "polymer": line["polymer"],
                **counts
            })
        item["numeric_coverage_pct"] = (
            round(100 * (item["colors"] - item["name_only"]) / item["colors"], 1)
            if item["colors"] else None
        )
        item["curated_coverage_pct"] = (
            round(100 * (item["manufacturer_swatch"] + item["measured"]) / item["colors"], 1)
            if item["colors"] else None
        )
        brands.append(item)
    totals = {key: sum(b[key] for b in brands) for key in
              ("lines", "colors", "manufacturer_swatch", "measured",
               "estimated", "name_only", "has_sku")}
    totals["brands"] = len(brands)
    totals["brands_with_lines"] = sum(b["lines"] > 0 for b in brands)
    if sum(totals[key] for key in ("manufacturer_swatch", "measured", "estimated", "name_only")) != totals["colors"]:
        raise ValueError("Quality counts do not sum to catalog color count")
    return {"method": "Counts among imported PLA/PETG variant records only. "
                       "Not the percentage of a manufacturer's complete commercial assortment. "
                       "manufacturer_swatch/measured are curated-eligible; estimated is a separate opt-in tier.",
            "totals": totals, "brands": brands}


def markdown(data: dict) -> str:
    totals, brands = data["totals"], data["brands"]
    text = [
        "# Filamentra — existing-brand color coverage",
        "",
        data["method"],
        "",
        f"**{totals['brands']} brands**, {totals['brands_with_lines']} with material lines, "
        f"**{totals['lines']} lines**, **{totals['colors']} color records**.",
        "",
        "| Brand | PLA/PETG lines | Colors | Curated | Estimated | Name-only | With SKU |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for b in sorted(brands, key=lambda x: (-x["name_only"], x["name"].lower())):
        curated = b["manufacturer_swatch"] + b["measured"]
        text.append(f"| {b['name']} | {b['lines']} | {b['colors']} | {curated} | "
                    f"{b['estimated']} | {b['name_only']} | {b['has_sku']} |")
    text += ["", "## Per-line coverage", "",
             "| Material line | Variants | Curated | Estimated | Name-only |",
             "| --- | ---: | ---: | ---: | ---: |"]
    for b in brands:
        for line in b["line_details"]:
            curated = line["manufacturer_swatch"] + line["measured"]
            text.append(f"| `{line['id']}` | {line['colors']} | {curated} | "
                        f"{line['estimated']} | {line['name_only']} |")
    text += ["", "## Interpretation", "",
             "- A record with an exact official SKU but no numeric source is still name-only.",
             "- A numeric estimated shade remains excluded from strict curated preview.",
             "- A zero line count flags a known brand **not yet imported**.",
             "- A full 100% numeric share among imported records **does not mean** "
             "that all colors or product lines offered by the maker are in this catalog.",
             "- Optical transmission and multicolor geometry need additional evidence; "
             "a HEX is not a physical calibration.",
             ""]
    return "\n".join(text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("markdown", "json", "summary"), default="summary")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    result = scan()
    if args.format == "json":
        output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    elif args.format == "markdown":
        output = markdown(result)
    else:
        n = result["totals"]
        output = (f"Brand coverage: {n['brands']} manufacturers, {n['brands_with_lines']} with lines, "
                  f"{n['lines']} lines, {n['colors']} variants\n"
                  f"Manufacturer or measured: {n['manufacturer_swatch'] + n['measured']}\n"
                  f"Estimated: {n['estimated']}\n"
                  f"Name-only: {n['name_only']}\n"
                  f"Has SKU: {n['has_sku']}\n")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        print(output, end="" if output.endswith("\n") else "\n")


if __name__ == "__main__":
    main()
