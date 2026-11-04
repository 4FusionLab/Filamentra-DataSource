#!/usr/bin/env python3
"""Deterministic, tileable, uncalibrated Filamentra normal/roughness maps.

These procedural surface *archetypes* are not photos, measurements or manufacturer maps.
Requires numpy and Pillow. No trained model, remote assets or random global state.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SIZE = 384
TILE_MM = 8.0
# kind, approximate RMS surface height (um), microstructure scale (mm), variation in roughness
# These are artistic/engineering assumptions, not measurements of any filament brand.
RECIPES = {
    "fiber-matte":          ("fiber",    7.0, 0.17, 0.055),
    "petg-matte":           ("matte",    2.8, 0.22, 0.040),
    "petg-standard":        ("smooth",   0.8, 0.32, 0.018),
    "petg-translucent":     ("smooth",   0.4, 0.40, 0.012),
    "pla-foam":             ("foam",     6.0, 0.65, 0.055),
    "pla-galaxy":           ("flakes",   1.9, 0.20, 0.052),
    "pla-glossy":           ("smooth",   0.4, 0.38, 0.012),
    "pla-glow":             ("matte",    2.4, 0.25, 0.036),
    "pla-lite-matte":      ("matte",    1.7, 0.26, 0.030),
    "pla-marble":           ("marble",   2.6, 0.35, 0.042),
    "pla-matte":            ("matte",    2.4, 0.20, 0.040),
    "pla-metallic-effect": ("smooth",   0.7, 0.30, 0.024),
    "pla-photochromic":    ("smooth",   1.2, 0.26, 0.021),
    "pla-silk-plus":       ("silk",     0.6, 0.35, 0.018),
    "pla-silk":            ("silk",     0.7, 0.35, 0.022),
    "pla-translucent":     ("smooth",   0.6, 0.40, 0.016),
    "pla-wood":            ("wood",     5.2, 0.35, 0.060),
    "sparkle-polymer":     ("flakes",   2.0, 0.24, 0.055),
}


def smooth_noise(rng: np.random.Generator, size: int, sigma: float) -> np.ndarray:
    """Periodic Gaussian-filtered white noise (FFT circular boundary)."""
    white = rng.normal(size=(size, size))
    freqs = np.fft.fftfreq(size)
    k2 = freqs[:, None] ** 2 + freqs[None, :] ** 2
    filt = np.exp(-2 * (np.pi ** 2) * sigma ** 2 * k2)
    field = np.fft.ifft2(np.fft.fft2(white) * filt).real
    return (field / max(float(field.std()), 1e-9)).astype(np.float32)


def speckles(rng: np.random.Generator, size: int, count: int, radius: float) -> np.ndarray:
    impulses = np.zeros((size, size), dtype=np.float32)
    y = rng.integers(0, size, size=count)
    x = rng.integers(0, size, size=count)
    impulses[y, x] = rng.uniform(0.6, 1.0, size=count)
    freqs = np.fft.fftfreq(size)
    k2 = freqs[:, None] ** 2 + freqs[None, :] ** 2
    spot = np.fft.ifft2(np.fft.fft2(impulses) *
                        np.exp(-2 * np.pi ** 2 * radius ** 2 * k2)).real
    return np.clip(spot / max(float(np.percentile(spot, 99.5)), 1e-9), 0, 1).astype(np.float32)


def generate_arrays(ident: str, roughness: float, size: int = SIZE) -> tuple[np.ndarray, np.ndarray]:
    if ident not in RECIPES:
        raise ValueError(f"Missing texture recipe for {ident}")
    kind, height_um, wavelength_mm, spread = RECIPES[ident]
    seed = int.from_bytes(hashlib.sha256(f"filamentra-v1:{ident}".encode()).digest()[:8], "big")
    rng = np.random.default_rng(seed)
    sigma_px = max(1.5, wavelength_mm * size / TILE_MM / 2)
    fine = smooth_noise(rng, size, max(1.4, sigma_px * 0.35))
    coarse = smooth_noise(rng, size, sigma_px)
    broad = smooth_noise(rng, size, sigma_px * 3)
    height = 0.45 * fine + 0.40 * coarse + 0.15 * broad
    rough_mod = 0.68 * fine + 0.32 * coarse

    if kind == "fiber":
        fibers = speckles(rng, size, 1100, 1.15)
        # Fine fibers affect microheight but are not an invented color/albedo map.
        height += 0.9 * fibers
        rough_mod += 0.75 * fibers
    elif kind == "flakes":
        flakes = speckles(rng, size, 340, 1.20)
        height += 0.58 * flakes
        rough_mod -= 1.5 * flakes  # smoother reflective inclusions
    elif kind == "marble":
        chips = speckles(rng, size, 200, 1.7)
        height += 0.75 * chips
        rough_mod += 0.28 * chips
    elif kind == "wood":
        yy, xx = np.mgrid[:size, :size].astype(np.float32)
        # Wrapped directional grain: integer cycle count avoids a seam.
        warped = 10 * xx / size + 0.17 * np.sin(2 * np.pi * (yy / size) * 3)
        grain = np.sin(2 * np.pi * warped)
        height += 0.65 * grain
        rough_mod += 0.4 * grain
    elif kind == "foam":
        porous = smooth_noise(rng, size, max(3, sigma_px * 0.8))
        height += 0.55 * np.maximum(0, porous - 0.5)
        rough_mod += 0.45 * porous
    elif kind == "silk":
        # Low relief; silk appearance is driven primarily by roughness.
        height *= 0.42

    # Convert physical microns to millimetres; derivatives in mm/mm.
    height *= (height_um * 0.001) / max(float(height.std()), 1e-9)
    step_mm = TILE_MM / size
    dx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) / (2 * step_mm)
    dy = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) / (2 * step_mm)
    vector = np.stack((-dx, -dy, np.ones_like(dx)), axis=-1)
    vector /= np.maximum(np.linalg.norm(vector, axis=-1, keepdims=True), 1e-9)
    normal = np.clip(np.rint((vector * 0.5 + 0.5) * 255), 0, 255).astype(np.uint8)
    rmap = np.clip(np.rint((roughness + spread * rough_mod) * 255), 0, 255).astype(np.uint8)
    # Explicitly stitch border texels for reliable tiling in viewers.
    normal[-1] = normal[0]
    normal[:, -1] = normal[:, 0]
    rmap[-1] = rmap[0]
    rmap[:, -1] = rmap[:, 0]
    return normal, rmap


def render_preview(normal: np.ndarray, rmap: np.ndarray) -> Image.Image:
    """Neutral sphere under fixed directional lighting; a *visual aid*, not Fusion output."""
    n = normal.shape[0]
    w, h = 320, 208
    yy, xx = np.mgrid[:h, :w]
    px = (xx - w / 2) / 87
    py = (yy - h / 2) / 87
    rr = px * px + py * py
    inside = rr < 1
    zz = np.sqrt(np.maximum(1 - rr, 1e-6))
    # Avoid UV seams by using screen-space sampling for visual *demonstration* only.
    tx = ((xx * 1.72).astype(int) % n)
    ty = ((yy * 1.72).astype(int) % n)
    txnorm = normal[ty, tx].astype(np.float32) / 255 * 2 - 1
    r = rmap[ty, tx].astype(np.float32) / 255
    base = np.stack((px, py, zz), axis=-1)
    tangent_x = np.stack((zz, np.zeros_like(px), -px), axis=-1)
    tangent_y = np.stack((np.zeros_like(py), zz, -py), axis=-1)
    vec = txnorm[..., 0, None] * tangent_x + txnorm[..., 1, None] * tangent_y + txnorm[..., 2, None] * base
    vec /= np.maximum(np.linalg.norm(vec, axis=-1, keepdims=True), 1e-8)
    light = np.array([-0.50, -0.58, 0.65]); light /= np.linalg.norm(light)
    halfway = light + np.array([0, 0, 1]); halfway /= np.linalg.norm(halfway)
    lambert = np.clip(np.sum(vec * light, axis=-1), 0, 1)
    nh = np.clip(np.sum(vec * halfway, axis=-1), 0, 1)
    shininess = 2 + 160 * ((1 - r) ** 3)
    highlight = ((1 - r * 0.62) * np.power(nh, shininess))
    shade = 0.12 + 0.65 * lambert + 0.56 * highlight
    background = np.zeros((h, w, 3), dtype=np.uint8)
    background[:] = [27, 32, 30]
    values = np.clip(205 * shade, 0, 245).astype(np.uint8)
    for c, scale in enumerate((0.86, 0.97, 0.88)):
        background[..., c][inside] = (values * scale)[inside].astype(np.uint8)
    return Image.fromarray(background, "RGB")


def build_textures(output: Path, presets_dir: Path = ROOT / "catalog" / "presets", size: int = SIZE) -> list[dict]:
    presets = sorted(presets_dir.glob("*.json"))
    expected = {p.stem for p in presets}
    if expected != set(RECIPES):
        raise ValueError(f"Texture recipes and presets differ: missing={expected-set(RECIPES)}, orphan={set(RECIPES)-expected}")
    items: list[dict] = []
    for path in presets:
        preset = json.loads(path.read_text(encoding="utf-8"))
        ident = preset["id"]
        appearance = preset["appearance"]
        roughness = appearance.get("roughness")
        if roughness is None:
            raise ValueError(f"Preset {ident} lacks base roughness")
        normal, rmap = generate_arrays(ident, roughness, size)
        relative = Path("assets") / "presets" / ident
        directory = output / relative
        directory.mkdir(parents=True, exist_ok=True)
        Image.fromarray(normal, "RGB").save(directory / "normal_gl.png", optimize=True)
        Image.fromarray(rmap, "L").save(directory / "roughness.png", optimize=True)
        render_preview(normal, rmap).save(directory / "preview.png", optimize=True)
        declared = appearance.get("textures", {})
        for key, file in (("normal_gl", "normal_gl.png"), ("roughness", "roughness.png")):
            expected_ref = str(relative / file)
            if declared.get(key) != expected_ref:
                raise ValueError(f"{ident} textures.{key}: expected {expected_ref}, got {declared.get(key)}")
        if declared.get("tile_width_mm") != TILE_MM or declared.get("tile_height_mm") != TILE_MM:
            raise ValueError(f"{ident} tile scale inconsistent with generator: expected {TILE_MM} mm")
        kind, height_um, wavelength_mm, spread = RECIPES[ident]
        items.append({"id": ident, "name": preset["name"], "kind": kind,
                      "roughness": roughness, "height_um": height_um,
                      "wavelength_mm": wavelength_mm, "roughness_spread": spread,
                      "tile_mm": TILE_MM, "resolution": size,
                      "normal_gl": str(relative / "normal_gl.png"),
                      "roughness_map": str(relative / "roughness.png"),
                      "preview": str(relative / "preview.png"),
                      "origin": "filamentra_procedural_estimate_v1", "calibrated": False})
    (output / "data").mkdir(parents=True, exist_ok=True)
    (output / "data" / "textures.json").write_text(
        json.dumps({"version": 1, "items": items}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    build_gallery(output, items)
    return items


def build_gallery(output: Path, items: list[dict]) -> None:
    cards = []
    for item in items:
        title = html.escape(item["name"])
        ident = html.escape(item["id"])
        cards.append(f'''<article class="card"><div class="preview"><img src="{item['preview']}" alt="Синтетический предпросмотр {title}" loading="lazy"></div><div class="inner"><div class="eyebrow">{ident}</div><h2>{title}</h2><p>Тип: {item['kind']} · roughness {item['roughness']:.2f} · фактура ≈ {item['height_um']:.1f} µm</p><div class="maps"><figure><img src="{item['normal_gl']}" alt="OpenGL normal map" loading="lazy"><figcaption>Normal (+Y)</figcaption></figure><figure><img src="{item['roughness_map']}" alt="Grayscale roughness map" loading="lazy"><figcaption>Roughness</figcaption></figure></div></div></article>''')
    markup = '''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#121514"><title>Фактуры — Filamentra</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#121514;color:#f0f2ed;font:14px/1.5 system-ui,sans-serif}a{color:inherit;text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:1440px;margin:auto;padding:24px clamp(20px,4vw,56px) 72px}.head{display:flex;align-items:center;justify-content:space-between;gap:20px;border-bottom:1px solid #303734;padding-bottom:22px}.logo{font-weight:700;letter-spacing:-.04em;font-size:23px}.logo b{color:#c6e79e}h1{font-size:clamp(36px,5vw,60px);font-weight:600;letter-spacing:-.04em;line-height:1.07;margin:35px 0 12px}p{color:#aeb8af;max-width:720px}.summary{margin-bottom:33px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px}.card{border:1px solid #303734;border-radius:14px;overflow:hidden;background:#1b1e1c}.preview{background:#1b201d}.preview img{display:block;width:100%;height:auto}.inner{padding:18px}.eyebrow{color:#93a094;font-size:12px;font-family:ui-monospace,monospace}h2{font-size:19px;margin:6px 0}.card p{font-size:12px;margin:0 0 15px;min-height:35px}.maps{display:grid;grid-template-columns:1fr 1fr;gap:10px}.maps figure{margin:0}.maps img{width:100%;aspect-ratio:1;display:block;object-fit:cover;border-radius:7px;border:1px solid #414a43}.maps figcaption{margin-top:6px;color:#aeb8af;font-size:11px}.tag{color:#c6e79e}
</style></head><body><main class="wrap"><header class="head"><a class="logo" href="./">F<b>.</b> Filamentra</a><a href="./">← Каталог цветов</a></header><div class="summary"><div class="eyebrow tag">FILAMENTRA / PROCEDURAL TEXTURES</div><h1>Фактура материала.<br>Без выдуманных измерений.</h1><p>18 типовых карт Normal и Roughness, сгенерированных детерминированно по семействам филамента. Рендеры ниже — нейтральные иллюстрации процедурного профиля, а не результат Autodesk Fusion и не измерения конкретного производителя.</p><p>Общий физический масштаб текстур: 8 × 8 мм. Цвет в данном предпросмотре нейтрален; реальные цвета применяются отдельно по данным каталога.</p></div><section class="grid">''' + "".join(cards) + '''</section></main></body></html>'''
    (output / "textures.html").write_text(markup, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    parser.add_argument("--size", type=int, default=SIZE)
    args = parser.parse_args()
    if args.size < 128 or args.size > 2048:
        parser.error("size must be 128..2048")
    files = build_textures(args.out.resolve(), size=args.size)
    print(f"Built {len(files)} texture profiles ({args.size} x {args.size}) in {args.out}")


if __name__ == "__main__":
    main()
