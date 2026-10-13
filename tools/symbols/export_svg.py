"""Esporta un SVG per simbolo in symbols/<nome>.svg a partire da symbols.py.

Uso (dalla cartella tools/symbols):
    python export_svg.py            # scrive ../../symbols/*.svg
    python export_svg.py --check    # verifica che i file su disco siano aggiornati

Formato (docs/symbol-format.md, "File nel repository"): viewBox 0 0 24 24, tratto 1,5,
terminali e giunzioni rotondi, colore currentColor, livelli secondari con opacity 0.35.
Un elemento <path> per sottotracciato, nello stesso ordine dei livelli in Sketch.
"""
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
            f'  <g fill="none" stroke="currentColor" stroke-width="{S.f(S.SW)}" stroke-linecap="round" stroke-linejoin="round">\n'
            + "\n".join(rows) + "\n  </g>\n</svg>\n")


def main():
    check = "--check" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    stale = []
    for name in S.SYM:
        path = os.path.join(OUT, name + ".svg")
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
    extra = sorted(f[:-4] for f in os.listdir(OUT) if f.endswith(".svg") and f[:-4] not in S.SYM)
    if check:
        if stale or extra:
            print("non aggiornati:", " ".join(stale), "| senza sorgente:", " ".join(extra))
            sys.exit(1)
        print(f"ok: {len(S.SYM)} simboli")
    else:
        print(f"scritti {len(S.SYM)} file in {os.path.normpath(OUT)}" + (f"; senza sorgente: {' '.join(extra)}" if extra else ""))


if __name__ == "__main__":
    main()
