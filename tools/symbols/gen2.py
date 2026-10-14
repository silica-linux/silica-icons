"""Generates the Sketch MCP script (run_code) that creates the symbol artboards.

Usage (from the tools/symbols folder, with a venv that has pillow and resvg-py):
    python gen2.py wifi,bluetooth > /tmp/batch.js
The content must be passed to mcp__sketch__run_code. Positions from gen.positions():
x = column * 144, y = category_index * 960 + 96 + row * 160 (12 columns).
The document id is in tpl.js: update it if it changes (it changes after a "Save As").
sheet.py renders a local check sheet; compose_sheet.py recomposes the PNGs exported
from Sketch (export/png folder) next to Inter.
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
