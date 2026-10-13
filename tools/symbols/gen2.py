"""Genera lo script per Sketch MCP (run_code) che crea gli artboard dei simboli.

Uso (dalla cartella tools/symbols, con un venv che abbia pillow e resvg-py):
    python gen2.py wifi,bluetooth > /tmp/batch.js
Il contenuto va passato a mcp__sketch__run_code. Posizioni da gen.positions():
x = colonna * 144, y = indice_categoria * 960 + 96 + riga * 160 (12 colonne).
L'id del documento è in tpl.js: aggiornarlo se cambia (cambia dopo un "Salva con nome").
sheet.py rende un foglio di controllo locale; compose_sheet.py ricompone i PNG esportati
da Sketch (cartella export/png) accanto a Inter.
"""
import json, sys
import symbols as S, gen
TPL = open('tpl.js').read()
def script(names, page='Symbols', sw=1.5, size=96, pos=None, suffix=''):
    pos = pos or gen.positions()
    items=[[n+suffix, pos[n][0], pos[n][1], [[m, d] for m, d in S.SYM[n]]] for n in names]
    return TPL.replace('__PAGE__', page).replace('__SW__', str(sw)).replace('__SIZE__', str(size)).replace('__ITEMS__', json.dumps(items, separators=(',',':')))
if __name__=='__main__':
    print(script(sys.argv[1].split(',')))
