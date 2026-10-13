"""Compone le icone a livelli come farebbe la shell (maschera del corpo, ordine dei livelli)
e scrive un foglio di controllo. Uso: python tools/compose.py [--dark] [--size N] [--out file.png]

La cartella generica (`folder-symbol`) si compone con `compose_folder(dir, size, dark, symbol,
tint)`: livello base, simbolo inciso e tinta, con le stesse regole della shell.

Dipendenze: pillow, resvg-py. Il font Inter va passato con --fonts se gli SVG contengono testo.
"""
import argparse
import io
import json
from pathlib import Path

import re

import numpy as np
import resvg_py
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parent.parent


def render(path: Path, size: int, fonts: list[str]) -> Image.Image:
    data = resvg_py.svg_to_bytes(svg_path=str(path), width=size, height=size, font_dirs=fonts)
    return Image.open(io.BytesIO(bytes(data))).convert("RGBA")


def body_mask(size: int) -> Image.Image:
    # Approssimazione con rettangolo arrotondato; la shell usa la superellisse della specifica.
    m = Image.new("L", (size, size), 0)
    s = size / 1024
    ImageDraw.Draw(m).rounded_rectangle((100 * s, 100 * s, 924 * s, 924 * s), radius=215 * s, fill=255)
    return m


def layer_file(icon_dir: Path, name: str, dark: bool) -> Path:
    if dark:
        stem, ext = name.rsplit(".", 1)
        candidate = icon_dir / f"{stem}-dark.{ext}"
        if candidate.exists():
            return candidate
    return icon_dir / name


def compose(icon_dir: Path, size: int, dark: bool, fonts: list[str]) -> Image.Image:
    manifest = json.loads((icon_dir / "icon.json").read_text())
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    for layer in manifest["layers"]:
        out.alpha_composite(render(layer_file(icon_dir, layer["file"], dark), size, fonts))
    dyn = manifest.get("dynamic") or {}
    if dyn.get("type") == "clock":
        for hand in dyn["hands"]:
            out.alpha_composite(render(layer_file(icon_dir, hand["file"], dark), size, fonts))
        out.alpha_composite(render(layer_file(icon_dir, dyn["cap"], dark), size, fonts))
    if manifest["kind"] == "app":
        out.putalpha(ImageChops.multiply(out.split()[3], body_mask(size)))
    return out


def render_string(svg: str, size: int, fonts: list[str]) -> Image.Image:
    data = resvg_py.svg_to_bytes(svg_string=svg, width=size, height=size, font_dirs=fonts)
    return Image.open(io.BytesIO(bytes(data))).convert("RGBA")


def folder_band(dyn: dict, side: float) -> dict | None:
    """La fascia di `symbol.sizes` per un'icona di lato `side` (corpo, in pt): la prima con
    `min_size` <= side; None sotto l'ultima (niente simbolo)."""
    for band in sorted(dyn["symbol"]["sizes"], key=lambda b: -b["min_size"]):
        if side >= band["min_size"]:
            return band
    return None


def tint_matrix(tint: str, ramp: dict) -> np.ndarray:
    """Matrice 3 × 4 (RGB → RGB + scostamento, valori 0–1): la luminanza del disegno va da
    tinta × shade (a luminance[0]) a tinta schiarita verso il bianco di glow (a luminance[1])."""
    t = np.array([int(tint[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    shade = t * ramp["shade"]
    glow = t + (1 - t) * ramp["glow"]
    lo, hi = ramp["luminance"]
    k = (glow - shade) / (hi - lo)
    lum = np.array([0.2126, 0.7152, 0.0722])
    return np.column_stack([np.outer(k, lum), shade - k * lo])


def apply_tint(img: Image.Image, m: np.ndarray) -> Image.Image:
    a = np.asarray(img).astype(np.float64) / 255
    rgb = a[..., :3] @ m[:, :3].T + m[:, 3]
    a[..., :3] = np.clip(rgb, 0, 1)
    return Image.fromarray((a * 255 + 0.5).astype(np.uint8), "RGBA")


def compose_folder(icon_dir: Path, size: int, dark: bool, symbol: str | None = None,
                   tint: str | None = None, fonts: list[str] | None = None) -> Image.Image:
    """La cartella generica a `size` px di tela: base, simbolo inciso (fascia scelta sul lato
    del corpo, size × 824 / 1024) e tinta. `tint` è un colore #rrggbb o il nome di un'etichetta."""
    fonts = fonts or []
    manifest = json.loads((icon_dir / "icon.json").read_text())
    dyn = manifest["dynamic"]
    out = render(layer_file(icon_dir, manifest["layers"][0]["file"], dark), size, fonts)
    band = folder_band(dyn, size * 824 / 1024)
    sym_file = ROOT / "symbols" / (band or {}).get("weight", "regular") / f"{symbol}.svg"
    if symbol and band and sym_file.exists():
        fx = dyn["effect"]["dark" if dark else "light"]
        x, y, w, h = dyn["symbol"]["box"]
        sc = band["scale"]
        cx, cy = x + w / 2, y + h / 2
        w, h = w * sc, h * sc
        inner = re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", sym_file.read_text(), flags=re.S)

        def layer(color: str, opacity: float, dy: float) -> str:
            return (f'<g opacity="{opacity}" transform="translate({cx - w / 2},{cy - h / 2 + dy}) '
                    f'scale({w / 24},{h / 24})">' + inner.replace("currentColor", color) + "</g>")

        glow = (layer(fx["highlight"], fx["highlight_opacity"], max(fx["offset"], 0.5 * 1024 / size))
                if band.get("highlight", True) else "")
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">'
               + glow + layer(fx["color"], fx["opacity"], 0) + "</svg>")
        out.alpha_composite(render_string(svg, size, fonts))
    if tint:
        colors = dyn["tint"]["labels"]
        tint = colors.get(tint, tint)
        out = apply_tint(out, tint_matrix(tint, dyn["tint"]["dark" if dark else "light"]))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dark", action="store_true")
    ap.add_argument("--size", type=int, default=192)
    ap.add_argument("--fonts", action="append", default=[])
    ap.add_argument("--out", default="build/contact-sheet.png")
    a = ap.parse_args()
    dirs = sorted(p.parent for p in ROOT.glob("*/*/icon.json"))
    cols = 8
    cell = a.size + 24
    rows = (len(dirs) + cols - 1) // cols
    bg = (40, 40, 44, 255) if a.dark else (236, 236, 240, 255)
    sheet = Image.new("RGBA", (cols * cell, rows * (cell + 16)), bg)
    draw = ImageDraw.Draw(sheet)
    for i, d in enumerate(dirs):
        x, y = (i % cols) * cell + 12, (i // cols) * (cell + 16) + 8
        sheet.alpha_composite(compose(d, a.size, a.dark, a.fonts), (x, y))
        draw.text((x, y + a.size + 4), d.name, fill=(255, 255, 255, 255) if a.dark else (40, 40, 44, 255))
    out = ROOT / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
