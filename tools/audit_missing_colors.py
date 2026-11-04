#!/usr/bin/env python3
"""List every PLA/PETG color without a numeric appearance source.

This research backlog is separate from public color records: it never guesses RGB
from names and never modifies brand/line JSON files.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANDS = ROOT / "catalog" / "brands"


def research_status(line: dict, color: dict) -> tuple[str, str]:
    brand, name, shade = line["brand"], line["name"].lower(), color["name"].lower()
    if brand == "deeplee":
        return "identity_unconfirmed", "Verify manufacturer and exact product/color listing"
    if "silk" in name and any(part in shade for part in
                              ("black green", "black purple", "black red",
                               "blue green", "blue purple", "blue magenta",
                               "green red", "yellow purple")):
        return "multicolor_underdetermined", "Need exact component swatches and coextrusion geometry"
    if "rainbow" in shade:
        return "gradient_underdetermined", "Need actual spool gradient stops and change period"
    if "translucent" in name or "transparent" in shade or "cmyk" in name:
        return "transmission_underdetermined", "Need exact color reference and volumetric transmission details"
    if "glow" in name:
        return "emission_underdetermined", "Need normal-light color; glow emission is a separate effect"
    if "hyper-petg-cf" in name and shade in ("night gray tea", "rocks red milk"):
        return "variant_alias_unverified", "Retailer name differs from official variant: require SKU mapping"
    if "lightweight" in name:
        return "foamed_sample_unverified", "Foamed finish needs product-specific sample/color"
    return "numeric_swatch_not_found", "Look for exact-SKU store/distributor swatch or measured sample"


def scan() -> list[dict]:
    missing = []
    for folder in sorted(BRANDS.iterdir()):
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.json")):
            if path.name == "brand.json":
                continue
            line = json.loads(path.read_text(encoding="utf-8"))
            if line.get("polymer") not in ("PLA", "PETG"):
                continue
            for color in line.get("colors", []):
                if color.get("hex") or color.get("rgba_swatches") or color.get("measured_sample"):
                    continue
                reason, next_step = research_status(line, color)
                # A verified SKU does not imply a numeric color swatch.
                sku_evidence = [
                    e for e in color.get("evidence", [])
                    if e.get("claim") == "sku_verified" and e.get("url")
                ]
                manufacturer_skus = [
                    v["sku"] for v in color.get("variants", [])
                    if isinstance(v.get("sku"), str) and v["sku"]
                ] if sku_evidence else []
                if manufacturer_skus and reason == "numeric_swatch_not_found":
                    next_step = "SKU verified; find per-SKU swatch or physical-sample measurement"
                missing.append({
                    "full_id": line["id"] + "/" + color["id"],
                    "manufacturer": line["brand"],
                    "polymer": line["polymer"],
                    "line": line["name"],
                    "color": color["name"],
                    "reason": reason,
                    "next_step": next_step,
                    "manufacturer_skus": manufacturer_skus,
                    "sku_evidence_urls": sorted({e["url"] for e in sku_evidence}),
                    "official_url": color.get("source_url") or line.get("source_url"),
                })
    return missing


def as_markdown(items: list[dict]) -> str:
    by_line = defaultdict(list)
    for item in items:
        by_line[(item["manufacturer"], item["polymer"], item["line"])].append(item)
    summary = Counter(item["manufacturer"] for item in items)
    reasons = Counter(item["reason"] for item in items)
    text = [
        "# Filamentra — unresolved PLA/PETG colors",
        "",
        "Generated from existing source JSON. No suggested color below is inferred from its name.",
        "",
        f"**Unresolved: {len(items)}** across {len(by_line)} lines.",
        f"**Unresolved with independently linked SKU:** {sum(bool(i['manufacturer_skus']) for i in items)}.",
        "",
        "## Manufacturer counts",
        "",
        "| Manufacturer | Without color |",
        "| --- | ---: |",
    ]
    text.extend(f"| {brand} | {count} |" for brand, count in sorted(summary.items()))
    text += ["", "## Missing-data reasons", "", "| Reason | Entries |", "| --- | ---: |"]
    text.extend(f"| \`{reason}\` | {count} |" for reason, count in sorted(reasons.items()))
    text += ["", "## Exhaustive list by manufacturer / polymer / line", ""]
    for key, colors in sorted(by_line.items()):
        brand, polymer, line = key
        text += [f"### {brand} → {polymer} → {line} ({len(colors)})", "",
                 "| Existing color ID | SKU verified | Reason | Next evidence |",
                 "| --- | --- | --- | --- |"]
        for entry in colors:
            skus = ', '.join(entry['manufacturer_skus']) or '—'
            text.append(f"| \`{entry['full_id']}\` | {skus} | \`{entry['reason']}\` | {entry['next_step']} |")
        text.append("")
    text += ["## Caveats", "",
             "- Manufacturer product URLs remain in individual JSON records and are included in the JSON audit output.",
             "- A name-only listing is a legitimate research record, **not** a ready Fusion appearance.",
             "- Search results with conflicting product-line, region, SKU, or coextrusion mappings are insufficient evidence.",
             "- Do not assign one HEX to a multicolor, translucent or phosphorescent filament to meet a completeness target.",
             ""]
    return "\n".join(text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=["markdown", "json", "summary"], default="summary")
    parser.add_argument("--out", type=Path, help="Optional destination; otherwise stdout")
    args = parser.parse_args()
    items = scan()
    if args.format == "markdown":
        output = as_markdown(items)
    elif args.format == "json":
        output = json.dumps({"total": len(items), "items": items},
                            ensure_ascii=False, indent=2) + "\n"
    else:
        counts = Counter(item["manufacturer"] for item in items)
        sku_count = sum(bool(i["manufacturer_skus"]) for i in items)
        output = f"Unresolved PLA/PETG: {len(items)}\n"
        output += f"Exact SKU verified: {sku_count}\n"
        output += "\n".join(f"{k}: {v}" for k, v in sorted(counts.items())) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
        print(f"Wrote {args.out}: {len(items)} unresolved colors")
    else:
        print(output, end="" if output.endswith("\n") else "\n")


if __name__ == "__main__":
    main()
