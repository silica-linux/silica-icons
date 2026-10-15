import json, sys
import symbols as S
DOC='A14E5E90-0F0B-4291-8A35-897B3221F260'
COLW, ROWH, BAND, TOP = 144, 160, 960, 96
CATIDX = {k:i for i,(k,_) in enumerate(S.CATS)}
def positions():
    pos={}; cnt={}
    for n in S.SYM:
        c=S.CAT[n]; i=cnt.get(c,0); cnt[c]=i+1
        pos[n]=(i%12*COLW, CATIDX[c]*BAND+TOP+(i//12)*ROWH)
    return pos
HEAD = """const sketch = require('sketch')
const doc = sketch.Document.getDocuments().find(d => d.id === '%s')
const page = doc.pages.find(p => p.name === '%s')
const items = %s
const made = []
items.forEach(it => {
  const ab = new sketch.Artboard({ name: it[0], parent: page, frame: new sketch.Rectangle(it[1], it[2], it[4], it[4]) })
  ab.background.enabled = false
  const g = sketch.createLayerFromData(it[3], 'svg')
  g.parent = ab
  const leaves = sketch.find('*', g).filter(l => (l.type === 'ShapePath' && l.parent.type !== 'Shape') || l.type === 'Shape')
  leaves.forEach(l => {
    let x = l.frame.x
    let y = l.frame.y
    let p = l.parent
    while (p && p.id !== ab.id) { x += p.frame.x; y += p.frame.y; p = p.parent }
    const w = l.frame.width
    const h = l.frame.height
    l.parent = ab
    l.frame = new sketch.Rectangle(x, y, w, h)
    l.name = l.style.opacity < 1 ? 'secondary' : 'primary'
  })
  g.remove()
  made.push([it[0], ab.id, leaves.length])
})
console.log(JSON.stringify({ ok: true, made: made }))"""
def script(names, page='Symbols', sw=S.SW, size=96, pos=None, suffix=''):
    pos = pos or positions()
    items=[[n+suffix, pos[n][0], pos[n][1], S.svg(n, sw=sw, size=size), size] for n in names]
    return HEAD % (DOC, page, json.dumps(items))
if __name__=='__main__':
    names=sys.argv[1].split(',')
    print(script(names))
