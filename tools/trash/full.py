import io, re, base64, math
from pathlib import Path
import resvg_py
from PIL import Image, ImageFilter
from render import *
PROTO = Path(__file__).resolve().parent  # old-full*.svg: the contents of the earlier Trash
M = 'matrix(1.122616,0,0,1.122616,-62.779292,-102.070845)'
def pieces(dark):
    s = (PROTO / ('old-full-dark.svg' if dark else 'old-full.svg')).read_text()
    lines = s.split('\n')
    i = next(k for k, l in enumerate(lines) if 'id="Document"' in l)
    j = next(k for k, l in enumerate(lines) if 'id="Folder"' in l)
    j = next(k for k in range(j, len(lines)) if lines[k].strip() == '</g>')
    cont = '\n'.join(lines[i:j + 1])
    defs = s[s.index('<defs>') + 6:s.index('</defs>')]
    doc = re.search(r'(<g id="Document".*?</g>)\s*<g id="Photo"', cont, re.S).group(1)
    photo = re.search(r'(<g id="Photo".*?</g>)\s*<g id="Folder"', cont, re.S).group(1)
    folder = re.search(r'(<g id="Folder".*?</g>\s*)$', cont, re.S).group(1)
    return defs, cont, doc, photo, folder
def heap(dark, dy, deep=True):
    defs, cont, doc, photo, folder = pieces(dark)
    C = {'doc': (167, 170), 'photo': (435, 150), 'folder': (315, 180)}
    Pm = {'doc': doc, 'photo': photo, 'folder': folder}
    layout = [('doc', 110, 700, 28), ('folder', 300, 720, -6), ('photo', 470, 690, 18), ('doc', 420, 600, -22),
              ('photo', 130, 560, -12), ('folder', 250, 520, 10), ('doc', 500, 470, 8), ('photo', 330, 420, -20),
              ('doc', 90, 380, -8), ('folder', 460, 330, -12), ('doc', 260, 300, 16)] if deep else []
    place = lambda p, dx, dy_, r, s=1.0: f'<g transform="translate({dx},{dy_}) rotate({r} 292 300) translate(315 180) scale({s}) translate(-315 -180)">{p}</g>'
    top = place(doc, 34, -10, -12) + place(photo, -40, -8, 12) + place(folder, 0, 30, 0, 1.18)
    inner = ''.join(place(Pm[k], tx - C[k][0], ty - C[k][1], r) for k, tx, ty, r in layout) + top
    return defs, f'<g transform="translate(512,{dy}) scale(1.0) translate(-512,0)"><g transform="{M}"><g transform="translate(220,96.6083)">{inner}</g></g></g>'
def full_svg(dark, dy=0, blur=32, op=0.3):
    _, _, g = build(dark)
    P, front, xi, yi, wall = g['P'], g['front'], g['xi'], g['yi'], g['wall']
    arc = [P(xi[i], yi[i], H) for i in front]
    allx = [P(xi[i], yi[i], H)[0] for i in range(len(xi))]
    lx, rx = min(allx) + 6, max(allx) - 6
    arc = [(min(max(x, lx), rx), y) for x, y in arc]
    above = [(lx, 0), (rx, 0), (rx, arc[-1][1]), *reversed(arc), (lx, arc[0][1])]
    cdefs, sharp = heap(dark, dy, deep=False)
    sdefs, scene = heap(dark, dy, deep=True)
    scene_svg = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1024 1024" width="1024" height="1024"><defs>{sdefs}</defs>{scene}</svg>'
    im = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=scene_svg, width=1024, height=1024)))).convert('RGBA')
    im = im.filter(ImageFilter.GaussianBlur(blur))
    xs = [p[0] for p in wall]; ys = [p[1] for p in wall]
    box = (int(min(xs)), int(min(ys)), int(math.ceil(max(xs))), int(math.ceil(max(ys))))
    crop = im.crop(box)
    crop.putalpha(crop.getchannel('A').point(lambda v: int(v * op)))
    small = crop.resize((crop.width // 4, crop.height // 4), Image.LANCZOS)
    buf = io.BytesIO(); small.save(buf, 'PNG', optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    extra = cdefs + '<clipPath id="above">' + poly(above) + '</clipPath>'
    sharp_g = f'<g id="Contents" clip-path="url(#above)">{sharp}</g>'
    blurred = (f'<g id="Contents-through" clip-path="url(#wallclip)"><image x="{box[0]}" y="{box[1]}" width="{box[2]-box[0]}" height="{box[3]-box[1]}" '
               f'preserveAspectRatio="none" xlink:href="data:image/png;base64,{b64}"/></g>')
    s = svg(dark, sharp_g, extra)
    # the blurred pile shows through the wall: right after the wall fill
    s = s.replace('<path d="', '<!--W-->', 0)
    k = s.index('fill="url(#foot)"/>') + len('fill="url(#foot)"/>')
    return s[:k] + blurred + s[k:], small
if __name__ == '__main__':
    sheet([(False, svg(False)), (False, full_svg(False)[0]), (True, svg(True)), (True, full_svg(True)[0])], 'full.png', size=420)
