"""Esporta un SVG per simbolo e per peso in symbols/<peso>/<nome>.svg a partire da symbols.py.

Uso (dalla cartella tools/symbols):
    python export_svg.py            # scrive ../../symbols/{light,regular,semibold}/*.svg
    python export_svg.py --check    # verifica che i file su disco siano aggiornati

Formato (docs/symbol-format.md, "File nel repository"): viewBox 0 0 24 24, tratto del peso
(Light 1,18 · Regular 1,5 · Semibold 2,15), terminali e giunzioni rotondi, colore currentColor,
livelli secondari con opacity 0.35. Un elemento <path> per sottotracciato, nello stesso ordine
dei livelli in Sketch. Per ogni peso symbols.py si ricarica con SILICA_SYMBOL_WEIGHT: il disegno
non cambia, i tagli delle barre e dei badge si ricalcolano perché la luce resti 1,5 u.
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
        print("file fuori dalle cartelle dei pesi:", " ".join(loose))
        bad = True
    if bad:
        sys.exit(1)
    print(f"{'ok' if CHECK else 'scritti'}: {total} file")


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
    tag = f"{S.WEIGHT} (tratto {S.f(S.WSW)})"
    if check and (stale or extra):
        print(f"{tag}: non aggiornati:", " ".join(stale), "| senza sorgente:", " ".join(extra))
        return len(S.SYM), False
    if extra:
        print(f"{tag}: senza sorgente:", " ".join(extra))
        return len(S.SYM), False
    print(f"{tag}: {len(S.SYM)} simboli in {os.path.normpath(out)}")
    return len(S.SYM), True


if __name__ == "__main__":
    main()
