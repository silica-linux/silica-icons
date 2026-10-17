#!/usr/bin/env python3
"""Render every glyph of each built font next to its source SVG (resvg) at 24 and 96 px,
report pixel differences and write a contact sheet PNG per weight into OUTDIR.

The reference SVG is rendered without its secondary layers (opacity 0.35), which the font
drops by design, except for symbols that consist only of secondary layers.
"""
import io
import json
import re
import sys
from pathlib import Path

import numpy as np
import resvg_py
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
cps = json.loads((ROOT / "fonts" / "codepoints.json").read_text())
SIZES = (24, 96)
THRESH = 128  # alpha difference counted as a hard mismatch


def reference(svg_path, size):
    s = svg_path.read_text()
    paths = re.findall(r"<path[^>]*/>", s)
    if not all('opacity="0.35"' in p for p in paths):
        s = re.sub(r"\s*<path[^>]*opacity=\"0\.35\"[^>]*/>", "", s)
    else:
        s = s.replace(' opacity="0.35"', "")
    s = s.replace("currentColor", "#000000")
    png = resvg_py.svg_to_bytes(svg_string=s, width=size, height=size)
    return np.array(Image.open(io.BytesIO(png)).convert("RGBA"))[:, :, 3].astype(int)


def rendered(font, ch, size):
    img = Image.new("L", (size, size), 0)
    # ascent = 1 em, descent ~0: the baseline is the bottom edge of the box
    ImageDraw.Draw(img).text((0, size), ch, font=font, fill=255, anchor="ls")
    return np.array(img).astype(int)


report = {}
for weight in ("Light", "Regular", "Semibold"):
    rows, mism = [], []
    for size in SIZES:
        font = ImageFont.truetype(str(ROOT / "fonts" / f"SilicaSymbols-{weight}.otf"), size)
        for name, cp in cps.items():
            svg = ROOT / "symbols" / weight.lower() / f"{name}.svg"
            if not svg.exists():
                continue
            ref, got = reference(svg, size), rendered(font, chr(int(cp, 16)), size)
            d = np.abs(ref - got)
            m = {"name": name, "size": size, "mean": float(d.mean()) / 255,
                 "hard_px": int((d > THRESH).sum()), "hard_frac": float((d > THRESH).mean()),
                 "ink_ref": int((ref > 0).sum()), "ink_font": int((got > 0).sum())}
            rows.append((m, ref, got))
    report[weight] = [r[0] for r in rows]
    for size in SIZES:
        sel = [r for r in rows if r[0]["size"] == size]
        cell, cols = size * 3 + 8, 8 if size == 96 else 16
        sheet_rows = (len(sel) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell, sheet_rows * (cell + 12)), "white")
        dr = ImageDraw.Draw(sheet)
        for i, (m, ref, got) in enumerate(sel):
            x, y = (i % cols) * cell, (i // cols) * (cell + 12)
            diff = np.abs(ref - got)
            for k, a in enumerate((ref, got, diff)):
                rgb = np.stack([255 - a] * 3, -1).astype(np.uint8) if k < 2 else \
                    np.stack([255 - a, 255 - a // 2 * 0 - 0 * a, 255 - a], -1).astype(np.uint8)
                if k == 2:
                    rgb = np.stack([np.full_like(a, 255), 255 - a, 255 - a], -1).astype(np.uint8)
                sheet.paste(Image.fromarray(rgb), (x + k * size + 2, y))
            if m["hard_frac"] > 0.004:
                dr.rectangle([x, y, x + cell - 2, y + size], outline=(255, 0, 0))
            if size == 96:
                dr.text((x + 2, y + size + 1), m["name"][:36], fill=(0, 0, 0))
        sheet.save(out / f"contact-{weight.lower()}-{size}.png")
(out / "diff-report.json").write_text(json.dumps(report, indent=1))

print("weight size  glyphs  worst-by-hard-pixel-fraction")
for weight, rows in report.items():
    for size in SIZES:
        sel = sorted((r for r in rows if r["size"] == size), key=lambda r: -r["hard_frac"])
        print(weight, size, len(sel), [(r["name"], round(r["hard_frac"] * 100, 2), round(r["mean"] * 100, 2)) for r in sel[:6]])
        flagged = [r for r in sel if r["hard_frac"] > 0.004]
        print("   flagged (>0.4% hard pixels):", len(flagged), [r["name"] for r in flagged])

# Ligatures: typing every symbol name must shape to exactly its glyph (HarfBuzz, liga on).
import uharfbuzz as hb

bad = []
for weight in ("Light", "Regular", "Semibold"):
    f = hb.Font(hb.Face(hb.Blob.from_file_path(str(ROOT / "fonts" / f"SilicaSymbols-{weight}.otf"))))
    for name in cps:
        b = hb.Buffer()
        b.add_str(name)
        b.guess_segment_properties()
        hb.shape(f, b, {"liga": True})
        got = [f.glyph_to_string(i.codepoint) for i in b.glyph_infos]
        if got != [name.replace("-", "_")]:
            bad.append((weight, name, got))
print("ligature failures:", bad)
