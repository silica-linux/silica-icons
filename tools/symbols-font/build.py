#!/usr/bin/env python3
"""Build the Silica Symbols icon fonts from symbols/<weight>/*.svg.

Strokes are outlined with Skia (round caps and joins), filled sub-paths are kept, every
path is merged with a nonzero-winding union so glyphs have no overlaps. Secondary layers
(opacity 0.35) are dropped, unless a symbol has nothing else: a monochrome font has no opacity.

Outputs (in fonts/): SilicaSymbols-{Light,Regular,Semibold}.{otf,woff2}, codepoints.json,
flutter/silica_symbols.dart, and SilicaSymbols-VF.{otf,woff2} when the outlines of the three
weights are point-compatible.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pathops
from fontTools.designspaceLib import (AxisDescriptor, DesignSpaceDocument,
                                      SourceDescriptor)
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.misc.transform import Transform
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[2]
SYMBOLS = ROOT / "symbols"
FONTS = ROOT / "fonts"
FAMILY = "Silica Symbols"
UPM = 2400            # 1 em = 24 u canvas, 100 font units per u
UNIT = UPM // 24
PUA_START = 0xE000
WEIGHTS = {  # name: (usWeightClass, stroke in u as in the SVGs)
    "Light": 300,
    "Regular": 400,
    "Semibold": 600,
}
SVG_NS = "{http://www.w3.org/2000/svg}"
DART_RESERVED = {
    "abstract", "as", "assert", "async", "await", "break", "case", "catch", "class", "const",
    "continue", "covariant", "default", "deferred", "do", "dynamic", "else", "enum", "export",
    "extends", "extension", "external", "factory", "false", "final", "finally", "for",
    "function", "get", "hide", "if", "implements", "import", "in", "interface", "is", "late",
    "library", "mixin", "new", "null", "on", "operator", "part", "required", "rethrow",
    "return", "set", "show", "static", "super", "switch", "sync", "this", "throw", "true",
    "try", "typedef", "var", "void", "while", "with", "yield", "values", "hashCode",
    "runtimeType", "toString",
}


def glyph_path(svg_file):
    """Return (pathops.Path outline in font units, number of dropped secondary layers)."""
    root = ET.parse(svg_file).getroot()
    result = pathops.Path()
    dropped = 0
    all_paths = list(root.iter(SVG_NS + "path"))
    # A symbol made only of secondary layers (wifi-0, volume-0 ...) would be an empty glyph:
    # keep its layers at full ink instead.
    keep_secondary = all(float(e.get("opacity", "1")) < 1 for e in all_paths)
    for group in root.iter(SVG_NS + "g"):
        stroke_w = float(group.get("stroke-width", "0"))
        for el in group.findall(SVG_NS + "path"):
            if float(el.get("opacity", "1")) < 1 and not keep_secondary:
                dropped += 1
                continue
            p = pathops.Path()
            # y flip and scale: SVG (0..24, y down) -> font (0..UPM, y up), baseline at canvas bottom
            parse_path(el.get("d"), TransformPen(p.getPen(), Transform(UNIT, 0, 0, -UNIT, 0, UPM)))
            filled = el.get("fill", group.get("fill", "none")) != "none"
            stroked = el.get("stroke", group.get("stroke", "none")) != "none"
            parts = []
            if filled:
                f = pathops.Path(p)
                f.simplify(fix_winding=True)
                parts.append(f)
            if stroked:
                s = pathops.Path(p)
                s.stroke(stroke_w * UNIT, pathops.LineCap.ROUND_CAP, pathops.LineJoin.ROUND_JOIN, 4)
                s.convertConicsToQuads(0.1)
                s.simplify(fix_winding=True)
                parts.append(s)
            for part in parts:
                result = pathops.op(result, part, pathops.PathOp.UNION, fix_winding=True)
    result.simplify(fix_winding=True)
    return result, dropped


def to_charstring(path, width):
    pen = T2CharStringPen(width, None, roundTolerance=0.5)
    path.draw(pen)
    return pen.getCharString()


def recorded(path):
    pen = RecordingPen()
    path.draw(pen)
    return pen.value


def structure(path):
    return [(op, len(args)) for op, args in recorded(path)]


def load_codepoints(names):
    f = FONTS / "codepoints.json"
    cps = json.loads(f.read_text()) if f.exists() else {}
    used = {int(v, 16) for v in cps.values()}
    nxt = max(used, default=PUA_START - 1) + 1
    for n in sorted(names):
        if n not in cps:
            cps[n] = format(nxt, "04X")
            nxt += 1
    if nxt > 0xF8FF + 1:
        sys.exit("BMP PUA exhausted")
    # Names that disappeared from the sources keep their entry (stability), but no glyph.
    return dict(sorted(cps.items()))


def glyph_name(n):
    return n.replace("-", "_")


LETTERS = {c: c for c in "abcdefghijklmnopqrstuvwxyz"}
DIGITS = dict(zip("0123456789", "zero one two three four five six seven eight nine".split()))
CHAR_GLYPHS = {**LETTERS, **DIGITS, "-": "hyphen"}


def fea(names):
    """Ligatures: typing the symbol name renders the glyph. Longest names first."""
    rules = []
    for n in sorted(names, key=lambda s: (-len(s), s)):
        seq = " ".join(CHAR_GLYPHS[c] for c in n)
        rules.append(f"    sub {seq} by {glyph_name(n)};")
    return "languagesystem DFLT dflt;\nlanguagesystem latn dflt;\n\nfeature liga {\n" + "\n".join(rules) + "\n} liga;\n"


def name_table(weight):
    ps = f"SilicaSymbols-{weight}"
    base = {1: FAMILY, 2: "Regular", 3: f"{FAMILY} {weight} 1.0", 4: f"{FAMILY} {weight}",
            5: "Version 1.0", 6: ps, 13: "CC BY-SA 4.0, derived from the Silica symbols",
            14: "https://creativecommons.org/licenses/by-sa/4.0/",
            0: "Copyright the Silica project. CC BY-SA 4.0",
            16: FAMILY, 17: weight}
    if weight != "Regular":
        base[1] = f"{FAMILY} {weight}"   # RIBBI-style family for legacy apps
        base[2] = "Regular"
    return base


def build_font(weight, glyphs, cps, ligature_names, vf_name=None):
    """glyphs: name -> pathops.Path."""
    order = [".notdef", "space"] + sorted(CHAR_GLYPHS.values(), key=str) + [glyph_name(n) for n in sorted(glyphs)]
    order = list(dict.fromkeys(order))
    fb = FontBuilder(UPM, isTTF=False)
    fb.setupGlyphOrder(order)
    cmap = {0x20: "space"}
    for ch, g in CHAR_GLYPHS.items():
        cmap[ord(ch)] = g
        if ch.isalpha():
            cmap[ord(ch.upper())] = g      # typing "WiFi" works too
    for n in glyphs:
        cmap[int(cps[n], 16)] = glyph_name(n)
    fb.setupCharacterMap(cmap)
    empty = pathops.Path()
    charstrings, metrics = {}, {}
    for g in order:
        if g in {glyph_name(n) for n in glyphs}:
            path = glyphs[[n for n in glyphs if glyph_name(n) == g][0]]
            w = UPM
        elif g == "space":
            path, w = empty, UPM // 4
        else:
            path, w = empty, 0   # ligature input components: no ink, no advance
        charstrings[g] = to_charstring(path, w)
        bounds = path.bounds if path.bounds != (0, 0, 0, 0) else None
        metrics[g] = (w, int(round(bounds[0])) if bounds else 0)
    fb.setupCFF(f"SilicaSymbols-{weight}", {"FullName": f"{FAMILY} {weight}", "FamilyName": FAMILY, "Weight": weight},
                charstrings, {})
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=UPM, descent=0, lineGap=0)
    nm = name_table(weight)
    fb.setupNameTable(nm, mac=False)
    fb.setupOS2(sTypoAscender=UPM, sTypoDescender=0, sTypoLineGap=0, usWinAscent=UPM, usWinDescent=0,
                usWeightClass=WEIGHTS[weight], fsType=0, achVendID="SLCA",
                fsSelection=(1 << 6 if weight == "Regular" else 0) | (1 << 7),  # REGULAR / USE_TYPO_METRICS
                sxHeight=0, sCapHeight=0, version=4)
    fb.setupPost(isFixedPitch=0)
    fb.font["head"].macStyle = 0
    fb.font["OS/2"].fsSelection |= 0   # not bold/italic
    fb.save(str(FONTS / f"SilicaSymbols-{weight}.otf"))
    font = TTFont(str(FONTS / f"SilicaSymbols-{weight}.otf"))
    addOpenTypeFeaturesFromString(font, fea(ligature_names))
    font.save(str(FONTS / f"SilicaSymbols-{weight}.otf"))
    return font


def woff2(src):
    f = TTFont(str(src))
    f.flavor = "woff2"
    f.save(str(src.with_suffix(".woff2")))


def camel(n):
    parts = n.split("-")
    s = parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])
    if s in DART_RESERVED or not (s[0].isalpha()):
        s += "Symbol"
    return s


def write_dart(cps, names):
    lines = [
        "// GENERATED by tools/symbols-font/build.py - do not edit.",
        "//",
        "// Silica system symbols as Flutter icons. CC BY-SA 4.0.",
        "//",
        "// fontPackage: when the fonts are bundled in a package (for example `silica_icons`),",
        "// set [kSilicaSymbolsPackage] to its name; leave it null when the app itself declares",
        "// the fonts in its pubspec.yaml (see docs/symbol-format.md, section Font).",
        "//",
        "// Static fonts: Flutter's Icon widget cannot pick a weight from a static font, so each",
        "// weight is its own family and its own class: SilicaSymbols (Regular), SilicaSymbolsLight,",
        "// SilicaSymbolsSemibold. The codepoints are identical in the three.",
        "// dart format off",
        "import 'package:flutter/widgets.dart';",
        "",
        "const String? kSilicaSymbolsPackage = null;",
        "",
    ]
    for cls, fam in (("SilicaSymbols", "SilicaSymbols"), ("SilicaSymbolsLight", "SilicaSymbolsLight"),
                     ("SilicaSymbolsSemibold", "SilicaSymbolsSemibold")):
        lines += [f"/// Silica symbols, {cls[len('SilicaSymbols'):] or 'Regular'} weight.",
                  f"abstract final class {cls} {{"]
        for n in names:
            lines.append(f"  static const IconData {camel(n)} = IconData(0x{cps[n].lower()}, "
                         f"fontFamily: '{fam}', fontPackage: kSilicaSymbolsPackage);")
        lines += ["}", ""]
    (FONTS / "flutter").mkdir(parents=True, exist_ok=True)
    (FONTS / "flutter" / "silica_symbols.dart").write_text("\n".join(lines))


def try_variable(per_weight, names, cps):
    """Build a wght-axis font if every glyph has the same segment structure in the 3 weights."""
    bad = [n for n in names
           if not (structure(per_weight["Light"][n]) == structure(per_weight["Regular"][n])
                   == structure(per_weight["Semibold"][n]))]
    return bad


def main():
    FONTS.mkdir(exist_ok=True)
    names = sorted(p.stem for p in (SYMBOLS / "regular").glob("*.svg"))
    for w in ("light", "semibold"):
        assert names == sorted(p.stem for p in (SYMBOLS / w).glob("*.svg")), f"{w} set differs"
    for n in names:
        assert re.fullmatch(r"[a-z0-9-]+", n), n
        assert glyph_name(n) not in set(CHAR_GLYPHS.values()) | {"space", ".notdef"}, n
    cps = load_codepoints(names)
    (FONTS / "codepoints.json").write_text(json.dumps(cps, indent=1) + "\n")

    per_weight, dropped_report, empty = {}, {}, {}
    for weight in WEIGHTS:
        glyphs = {}
        for n in names:
            path, dropped = glyph_path(SYMBOLS / weight.lower() / f"{n}.svg")
            glyphs[n] = path
            if dropped:
                dropped_report.setdefault(n, dropped)
            if not len(list(path.segments)):
                empty.setdefault(weight, []).append(n)
        per_weight[weight] = glyphs
        build_font(weight, glyphs, cps, names)
        woff2(FONTS / f"SilicaSymbols-{weight}.otf")
        print(f"{weight}: {len(glyphs)} glyphs")
    write_dart(cps, names)
    print("secondary layers dropped:", json.dumps(dropped_report))
    print("empty glyphs:", json.dumps(empty))
    bad = try_variable(per_weight, names, cps)
    print(f"point-incompatible across weights: {len(bad)} of {len(names)}")
    (FONTS / "build-report.json").write_text(json.dumps(
        {"secondary_layers_dropped": dropped_report, "empty_glyphs": empty,
         "variable_incompatible": bad}, indent=1) + "\n")
    if bad:
        print("variable font skipped")


if __name__ == "__main__":
    main()
