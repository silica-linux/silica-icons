const sketch = require('sketch')
const doc = sketch.Document.getDocuments().find(d => d.id === '8555075F-FB9C-4177-9687-3FB1A399AAB0')
const page = doc.pages.find(p => p.name === '__PAGE__')
const size = __SIZE__
const items = __ITEMS__
const made = []
const skipped = []
items.forEach(it => {
  if (page.layers.find(l => l.name === it[0])) { skipped.push(it[0]); return }
  const body = it[3].map(e => {
    const op = e[0].length > 1 ? " opacity='0.35'" : ''
    const m = e[0][0]
    const extra = m === 'f' ? " fill='#000'" : (m === 'F' ? " fill='#000' stroke='none'" : '')
    return "<path d='" + e[1] + "'" + extra + op + '/>'
  }).join('')
  const svg = "<svg xmlns='http://www.w3.org/2000/svg' width='" + size + "' height='" + size + "' viewBox='0 0 24 24'><g fill='none' stroke='#000' stroke-width='__SW__' stroke-linecap='round' stroke-linejoin='round'>" + body + '</g></svg>'
  const ab = new sketch.Artboard({ name: it[0], parent: page, frame: new sketch.Rectangle(it[1], it[2], size, size) })
  ab.background.enabled = false
  const g = sketch.createLayerFromData(svg, 'svg')
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
  made.push([it[0], leaves.length])
})
doc.save()
console.log(JSON.stringify({ ok: true, made: made.length, skipped: skipped }))
