#!/usr/bin/env python3
"""Build catalog-specific 3D-like specimen thumbnails from documented colors.

Generated pictures are *procedural approximations*, not photographs, color
measurements, Autodesk Fusion screenshots, or physically calibrated PBR renders.
Only solid colors with a numeric source are illustrated. Multi-color products
retain their original swatches instead of inventing a spatial arrangement.
"""
from __future__ import annotations

import math
import re
from functools import lru_cache
from io import BytesIO
from pathlib import Path

import cairosvg

import numpy as np
from PIL import Image

IMAGE_SIZE = (256, 192)
_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
BRAND_LOGO = Path(__file__).resolve().parents[1] / "demo/assets/brand/4fusionlab-logo.svg"


@lru_cache(maxsize=1)
def logo_backdrop() -> np.ndarray:
    """Official 4FusionLab avatar, centrally placed at a fixed size for every material.

    The SVG is copied verbatim from 4FusionLab/.github/assets/avatar.svg; rasterization
    is deterministic. A single backdrop makes relative transparency comparable.
    """
    if not BRAND_LOGO.is_file():
        raise FileNotFoundError(f"Missing official 4FusionLab logo: {BRAND_LOGO}")
    picture = cairosvg.svg2png(url=str(BRAND_LOGO), output_width=176, output_height=176)
    with Image.open(BytesIO(picture)) as source_logo:
        icon = source_logo.convert("RGBA")
    backdrop = Image.new("RGBA", IMAGE_SIZE, (24, 30, 27, 255))
    backdrop.alpha_composite(icon, ((IMAGE_SIZE[0] - icon.width) // 2,
                                    (IMAGE_SIZE[1] - icon.height) // 2))
    return np.asarray(backdrop.convert("RGB"), dtype=np.float32) / 255


def numeric_color(color: dict) -> str | None:
    if color.get("color_mode") in ("gradient", "multicolor"):
        return None
    if (color.get("rgba_swatches") or []) and len(color["rgba_swatches"]) > 1:
        return None
    measured = (color.get("measured_sample") or {}).get("hex")
    if isinstance(measured, str) and _COLOR_RE.fullmatch(measured):
        return measured
    hexadecimal = color.get("hex")
    if isinstance(hexadecimal, str) and _COLOR_RE.fullmatch(hexadecimal):
        return hexadecimal
    swatches = color.get("rgba_swatches") or []
    if len(swatches) == 1 and re.fullmatch(r"#[0-9A-Fa-f]{8}", swatches[0]):
        if swatches[0][-2:].upper() == "FF":
            return swatches[0][:7]
    return None


def resolve_appearance(preset: dict, line: dict | None = None, color: dict | None = None) -> dict:
    """Merge optical fields and texture references, matching the browser resolver."""
    base = dict(preset or {})
    for override in (line or {}, color or {}):
        for key, value in override.items():
            if key == "textures":
                base[key] = {**base.get(key, {}), **value}
            else:
                base[key] = value
    transmission = base.get("transmission", 0)
    if transmission > 0 and base.get("surface_type") != "transparent":
        raise ValueError("Transmissive appearance must use surface_type=transparent")
    return base


def preview_tint(color: dict, appearance: dict) -> str | None:
    """Use source-backed color, or neutral *render-only* tint for verified clear swatch."""
    value = numeric_color(color)
    if value is not None:
        return value
    swatches = color.get("rgba_swatches") or []
    if (appearance.get("surface_type") == "transparent"
            and appearance.get("transmission", 0) > 0
            and color.get("color_mode", "solid") == "solid"
            and len(swatches) == 1
            and isinstance(swatches[0], str)
            and re.fullmatch(r"#[0-9A-Fa-f]{6}00", swatches[0])):
        # Optical rendering convention only. Never write a fictitious HEX.
        return "#F6F9F7"
    return None


def preview_path(line_id: str, color_id: str) -> str:
    """A deterministic path, using existing validated repository identifiers."""
    if not re.fullmatch(r"[a-z0-9-]+/[a-z0-9-]+", line_id):
        raise ValueError(f"Invalid line ID: {line_id}")
    if not re.fullmatch(r"[a-z0-9-]+", color_id):
        raise ValueError(f"Invalid color ID: {color_id}")
    return f"assets/material-previews/{line_id}/{color_id}.webp"


def prepare_specimen(normal_path: Path, rough_path: Path, roughness_offset: float = 0.0) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return diffuse, specular and edge masks for one preset at a fixed camera."""
    with Image.open(normal_path) as image:
        normals = np.asarray(image.convert("RGB"), dtype=np.float32) / 255 * 2 - 1
    with Image.open(rough_path) as image:
        rough = np.asarray(image.convert("L"), dtype=np.float32) / 255

    width, height = IMAGE_SIZE
    yy, xx = np.mgrid[0:height, 0:width].astype(np.float32)
    radius = 69.0
    cx, cy = width / 2, height / 2 + 1
    x = (xx - cx) / radius
    y = -(yy - cy) / radius
    r2 = x*x + y*y
    inside = r2 <= 1
    z = np.sqrt(np.maximum(1 - r2, 0))
    # 30-mm-diameter reference specimen. An 8-mm material tile repeats over
    # the approximate physical arc lengths, not arbitrary texture pixels.
    u = (np.arctan2(x, np.maximum(z, 1e-6)) / (2 * np.pi) + 0.5) * (2 * np.pi * 15 / 8)
    v = (np.arccos(np.clip(y, -1, 1)) / np.pi) * (np.pi * 15 / 8)
    tx = np.floor(u * normals.shape[1]).astype(np.int32) % normals.shape[1]
    ty = np.floor(v * normals.shape[0]).astype(np.int32) % normals.shape[0]
    bump = normals[ty, tx]
    roughness = np.clip(rough[ty, tx] + roughness_offset, 0.03, 1)

    # Local tangent-space map -> approximate sphere-space normal.
    tangent = np.stack([z, np.zeros_like(x), -x], axis=-1)
    tangent /= np.maximum(np.linalg.norm(tangent, axis=-1, keepdims=True), 1e-5)
    surface = np.stack([x, y, z], axis=-1)
    bitangent = np.cross(surface, tangent)
    n = tangent * bump[..., 0:1] + bitangent * bump[..., 1:2] + surface * bump[..., 2:3]
    n /= np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-5)

    key = np.array([-0.45, 0.58, 0.68], dtype=np.float32)
    key /= np.linalg.norm(key)
    fill = np.array([0.75, 0.08, 0.65], dtype=np.float32)
    fill /= np.linalg.norm(fill)
    half = key + np.array([0, 0, 1], dtype=np.float32)
    half /= np.linalg.norm(half)
    ndl = np.maximum(0, np.sum(n * key, axis=-1))
    fill_dot = np.maximum(0, np.sum(n * fill, axis=-1))
    ndh = np.clip(np.sum(n * half, axis=-1), 0, 1)
    # Deliberate preview shading, not a calibrated BRDF.
    diffuse = 0.19 + 0.72 * ndl + 0.13 * fill_dot
    exponent = 3 + (1 - roughness) ** 3 * 145
    specular = np.power(ndh, exponent) * (0.10 + 0.27 * (1 - roughness))
    specular += np.power(np.clip(1 - z, 0, 1), 5) * 0.11
    edge = np.clip((1 - np.sqrt(r2)) * radius / 1.5, 0, 1)
    return diffuse.astype(np.float32), specular.astype(np.float32), np.where(inside, edge, 0).astype(np.float32), z.astype(np.float32)


def make_thumbnail(
    hex_rgb: str,
    prepared: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    appearance: dict | None = None,
) -> Image.Image:
    """Render the same fixed 30-mm specimen; transparent profiles use a 2-mm shell."""
    diffuse, specular, edge, face_cosine = prepared
    appearance = appearance or {}
    transmission = float(appearance.get("transmission", 0))
    base = np.array([int(hex_rgb[i:i+2], 16) / 255 for i in (1, 3, 5)], dtype=np.float32)
    linear = np.where(base <= 0.04045, base / 12.92, ((base + 0.055) / 1.055) ** 2.4)
    lit = np.clip(linear[None, None, :] * diffuse[..., None] + specular[..., None], 0, 1)
    srgb = np.where(lit <= 0.0031308, lit * 12.92, 1.055 * np.power(lit, 1 / 2.4) - 0.055)

    # Every sample is placed in front of the *same* official 4FusionLab logo.
    # It remains hidden by opaque plastic and progressively visible through
    # translucent and clear grades, with no arbitrary reference stripes.
    backdrop = logo_backdrop()
    if transmission > 0:
        # Optical behavior is approximate and explicitly thickness-dependent.
        # At grazing angles the same 2-mm shell absorbs more light.
        distance = float(appearance.get("attenuation_distance_mm", 9.0))
        wall_path_mm = 2.0 / np.maximum(face_cosine, 0.24)
        transmitted = transmission * np.exp(-wall_path_mm / max(distance, 1e-6))
        tint = 0.36 + 0.64 * np.power(base, 0.6)
        mix = transmitted[..., None] * 0.92
        # Retain reflective highlights even for nearly clear plastics.
        sphere = np.clip(srgb * (1 - mix) + backdrop * tint * mix
                         + specular[..., None] * 0.10, 0, 1)
        composite = sphere * edge[..., None] + backdrop * (1 - edge[..., None])
    else:
        composite = srgb * edge[..., None] + backdrop * (1 - edge[..., None])
    return Image.fromarray(np.uint8(np.rint(np.clip(composite, 0, 1) * 255)), mode="RGB")


def build_material_previews(payload: dict, out: Path) -> int:
    cached: dict[tuple[str, float], tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = {}
    created = 0
    for line in payload["lines"]:
        preset = line.get("appearance_preset")
        if preset not in payload["presets"]:
            continue
        base = payload["presets"][preset]["appearance"]
        for color in line["colors"]:
            relative = color.get("preview_image")
            if not relative:
                continue
            resolved = resolve_appearance(base, line.get("appearance"), color.get("appearance"))
            rgb = preview_tint(color, resolved)
            if rgb is None:
                raise ValueError(f"Unexpected preview on unresolved/multicolor record {line['id']}/{color['id']}")
            delta = round(resolved.get("roughness", base["roughness"]) - base["roughness"], 4)
            key = (preset, delta)
            if key not in cached:
                maps = resolved.get("textures") or {}
                try:
                    normal_path = out / maps["normal_gl"]
                    rough_path = out / maps["roughness"]
                except KeyError as exc:
                    raise ValueError(f"Missing PBR map in {preset}") from exc
                cached[key] = prepare_specimen(normal_path, rough_path, roughness_offset=delta)
            path = out / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            make_thumbnail(rgb, cached[key], resolved).save(path, "WEBP", quality=81, method=2)
            created += 1
    return created
