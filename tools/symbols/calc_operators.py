"""Calculator key operators (calc-*), drawn in code on the symbol grid (docs/symbol-format.md).

Ink spans 17 u end to end at every weight so the keys match the 16-17 pt digits of Inter 24
Semibold. Run from the repository root: python3 tools/symbols/calc_operators.py
"""
import os
W = {'light': 1.18, 'regular': 1.5, 'semibold': 2.15}
def L(x1,y1,x2,y2): return f'<path d="M{x1} {y1} L{x2} {y2}"/>'
def dot(cx,cy,r): return f'<path d="M{cx-r} {cy}A{r} {r} 0 1 0 {cx+r} {cy}A{r} {r} 0 1 0 {cx-r} {cy}Z" fill="currentColor" stroke="none"/>'
def ring(cx,cy,r): return f'<path d="M{cx-r} {cy}A{r} {r} 0 1 0 {cx+r} {cy}A{r} {r} 0 1 0 {cx-r} {cy}Z"/>'
def glyphs(w):
    h = w/2
    a, b = 3.5 + h, 20.5 - h          # 17 pt of ink end to end at any weight
    return {
     'calc-add': L(a,12,b,12) + L(12,a,12,b),
     'calc-subtract': L(a,12,b,12),
     'calc-multiply': L(6.5,6.5,17.5,17.5) + L(17.5,6.5,6.5,17.5),
     'calc-divide': L(a,12,b,12) + dot(12,6.25,1.25+h*0.6) + dot(12,17.75,1.25+h*0.6),
     'calc-equal': L(a+0.5,8.75,b-0.5,8.75) + L(a+0.5,15.25,b-0.5,15.25),
     'calc-percent': ring(7.25,7.25,2.75) + ring(16.75,16.75,2.75) + L(18,5,6,19),
     'calc-plus-minus': L(4.5,8,11.5,8) + L(8,4.5,8,11.5) + L(17.5,4.5,6.5,19.5) + L(12.5,16,19.5,16),
    }
for wt, w in W.items():
    for name, body in glyphs(w).items():
        open(f'symbols/{wt}/{name}.svg','w').write(f'''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
  <g fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">
    {body}
  </g>
</svg>
''')
