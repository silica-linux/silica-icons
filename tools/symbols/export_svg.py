"""Exports one SVG per symbol and per weight to symbols/<weight>/<name>.svg from symbols.py.

Usage (from the tools/symbols folder):
    python export_svg.py            # writes ../../symbols/{light,regular,semibold}/*.svg
    python export_svg.py --check    # verifies that the files on disk are up to date

Format (docs/symbol-format.md, "Files in the repository"): viewBox 0 0 24 24, stroke of the weight
(Light 1.18 · Regular 1.5 · Semibold 2.15), round terminals and joins, color currentColor,
secondary layers with opacity 0.35. One <path> element per subpath, in the same order
as the layers in Sketch. For each weight symbols.py is reloaded with SILICA_SYMBOL_WEIGHT: the
drawing does not change, the cuts of bars and badges are recomputed so the gap stays 1.5 u.
"""
import importlib
import os
import sys

import symbols as S

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "symbols")


def svg(name):
    rows = []
    for mode, d in S.SYM[name]:
        attrs = f'd="{d}"'
        m = mode[0]
        if m == "f":
            attrs += ' fill="currentColor"'
        elif m == "F":
            attrs += ' fill="currentColor" stroke="none"'
        if mode.endswith("2"):
            attrs += ' opacity="0.35"'
        rows.append(f"    <path {attrs}/>")
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">\n'
            f'  <g fill="none" stroke="currentColor" stroke-width="{S.f(S.WSW)}" stroke-linecap="round" stroke-linejoin="round">\n'
            + "\n".join(rows) + "\n  </g>\n</svg>\n")


def weight(w):
    global S
    os.environ["SILICA_SYMBOL_WEIGHT"] = w
    S = importlib.reload(S)
    return export(os.path.join(OUT, w))


def main():
    total, bad = 0, False
    for w in ("light", "regular", "semibold"):
        n, ok = weight(w)
        total += n
        bad = bad or not ok
    os.environ.pop("SILICA_SYMBOL_WEIGHT", None)
    loose = sorted(f for f in os.listdir(OUT) if f.endswith(".svg"))
    if loose:
        print("files outside the weight folders:", " ".join(loose))
        bad = True
    if bad:
        sys.exit(1)
    print(f"{'ok' if CHECK else 'written'}: {total} files")


CHECK = "--check" in sys.argv


def export(out):
    check = CHECK
    os.makedirs(out, exist_ok=True)
    stale = []
    for name in S.SYM:
        path = os.path.join(out, name + ".svg")
        data = svg(name)
        if check:
            try:
                with open(path) as fh:
                    if fh.read() != data:
                        stale.append(name)
            except FileNotFoundError:
                stale.append(name)
        else:
            with open(path, "w") as fh:
                fh.write(data)
    extra = sorted(f[:-4] for f in os.listdir(out) if f.endswith(".svg") and f[:-4] not in S.SYM)
    tag = f"{S.WEIGHT} (stroke {S.f(S.WSW)})"
    if check and (stale or extra):
        print(f"{tag}: out of date:", " ".join(stale), "| without source:", " ".join(extra))
        return len(S.SYM), False
    if extra:
        print(f"{tag}: without source:", " ".join(extra))
        return len(S.SYM), False
    print(f"{tag}: {len(S.SYM)} symbols in {os.path.normpath(out)}")
    return len(S.SYM), True


if __name__ == "__main__":
    main()
