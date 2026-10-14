import math, io
import numpy as np
from bin3d import *

def unit(v):
    v = np.asarray(v, float); return v / np.linalg.norm(v)
L = unit([-0.55, -0.75, 0.95])
V = unit([0, -math.cos(PITCH), math.sin(PITCH)])
HV = unit(L + V)

def hull(pts):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))
    def cross(o, a, b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]

PAL = {
    False: dict(wall_lo='#97a0ad', wall_hi='#ffffff', inner_lo='#8c94a1', inner_hi='#dde1e7', floor='#a3aab6',
                rim_lo='#dfe3e9', rim_hi='#ffffff', alpha=0.84, edge='#000000', eop=0.12, fres=0.30, foot=0.10, hl=0.95),
    True: dict(wall_lo='#24252b', wall_hi='#70737e', inner_lo='#121316', inner_hi='#34363d', floor='#17181b',
               rim_lo='#55575f', rim_hi='#a3a5b0', alpha=0.82, edge='#ffffff', eop=0.16, fres=0.14, foot=0.30, hl=0.55),
}

def horiz_gradient(gid, idxs, xs, colour):
    x0, x1 = min(xs), max(xs)
    st = []
    for k, (i, sx) in enumerate(zip(idxs, xs)):
        if k % 4 and k != len(idxs) - 1: continue
        c, a = colour(i)
        st.append(f'<stop offset="{(sx - x0) / (x1 - x0):.4f}" stop-color="{c}" stop-opacity="{a:.3f}"/>')
    return f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x0:.1f}" y1="0" x2="{x1:.1f}" y2="0">{"".join(st)}</linearGradient>'

def build(dark=False):
    C = PAL[dark]
    fit = Fit()
    P = lambda x, y, z: fit(*project(x, y, z))
    t, xo, yo = ring(TOP); _, xb, yb = ring(BOT)
    _, xr, yr = ring(TOP * LIP)
    _, xi, yi = ring(TOP - WALL); _, xf, yf = ring(BOT - WALL)
    nx, ny = normals(xo, yo)
    slope = (TOP - BOT) / H
    n = len(t)
    defs, out = [], []
    back = sorted([i for i in range(n) if 0 <= t[i] <= math.pi], key=lambda i: -t[i])   # left → right along the back
    front = sorted([i for i in range(n) if math.pi <= t[i] < 2 * math.pi] + [0], key=lambda i: t[i] if i else 2 * math.pi)
    # inside: back wall and floor (seen through the opening and the glass)
    inner = [P(xi[i], yi[i], H) for i in back] + [P(xf[i], yf[i], WALL) for i in reversed(back)]
    def inner_col(i):
        nn = unit([-nx[i], -ny[i], slope]); lit = max(0, float(nn @ L))
        return mix(C['inner_lo'], C['inner_hi'], 0.2 + 0.8 * lit), 1
    defs.append(horiz_gradient('inner', back, [P(xi[i], yi[i], H)[0] for i in back], inner_col))
    defs.append(f'<linearGradient id="deep" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000000" stop-opacity="0"/><stop offset="1" stop-color="#000000" stop-opacity="{0.35 if dark else 0.18}"/></linearGradient>')
    # the back of the bin (outer back wall), seen through the glass: the whole silhouette,
    # so nothing behind the front shows the background
    shell = hull([P(xo[i], yo[i], H) for i in range(n)] + [P(xb[i], yb[i], 0) for i in range(n)])
    out.append(poly(shell, fill='url(#inner)'))
    out.append(poly(shell, fill='url(#deep)'))
    out.append(poly([P(xf[i], yf[i], WALL) for i in range(n)], fill=C['floor']))
    # the opening is entirely inner wall seen from above: fill the whole inner ring too,
    # so the side walls reach the front rim instead of stopping at the back half
    opening = [P(xi[i], yi[i], H) for i in range(n)]
    for shape_ in (inner, opening):
        out.append(poly(shape_, fill='url(#inner)'))
        out.append(poly(shape_, fill='url(#deep)'))
    # rim, whole ring, behind the contents
    ring_d = lambda xs_, ys_: 'M' + ' L'.join(f'{P(xs_[i], ys_[i], H)[0]:.1f},{P(xs_[i], ys_[i], H)[1]:.1f}' for i in range(n)) + ' Z'
    ry0, ry1 = P(0, TOP, H)[1], P(0, -TOP, H)[1]
    defs.append(f'<linearGradient id="rim" gradientUnits="userSpaceOnUse" x1="0" y1="{ry0:.1f}" x2="0" y2="{ry1:.1f}"><stop offset="0" stop-color="{C["rim_lo"]}"/><stop offset="1" stop-color="{C["rim_hi"]}"/></linearGradient>')
    out.append(f'<path d="{ring_d(xr, yr)} {ring_d(xi, yi)}" fill="url(#rim)" fill-rule="evenodd"/>')
    out.append('<!--CONTENTS-->')
    # outer wall: silhouette = hull of top and bottom rings, shaded from the model
    sil = hull([P(xo[i], yo[i], H) for i in range(n)] + [P(xb[i], yb[i], 0) for i in range(n)])
    # cut the silhouette at the rim: the wall is what lies below the outer ring's front arc
    wall = [P(xo[i], yo[i], H) for i in front] + [p for p in reversed(sil) if p[1] > P(xo[front[0]], yo[front[0]], H)[1] - 0.5 and p[1] > 0][0:0]
    wall = [P(xo[i], yo[i], H) for i in front] + [P(xb[i], yb[i], 0) for i in reversed(front)]
    def wall_col(i):
        nn = unit([nx[i], ny[i], slope])
        dif = max(0, float(nn @ L)); spec = max(0, float(nn @ HV)) ** 50; fres = (1 - abs(float(nn @ V))) ** 2
        c = mix(C['wall_lo'], C['wall_hi'], min(1, 0.05 + 0.95 * dif))
        c = mix(c, '#ffffff', min(1, 0.6 * spec + C['fres'] * fres))
        return c, min(1, C['alpha'] + 0.15 * fres)
    xs = [P(xo[i], yo[i], H)[0] * 0.5 + P(xb[i], yb[i], 0)[0] * 0.5 for i in front]
    defs.append(horiz_gradient('wall', front, xs, wall_col))
    defs.append(f'<linearGradient id="foot" x1="0" y1="0" x2="0" y2="1"><stop offset="0.7" stop-color="#000000" stop-opacity="0"/><stop offset="1" stop-color="#000000" stop-opacity="{C["foot"]}"/></linearGradient>')
    defs.append('<clipPath id="wallclip">' + poly(wall) + '</clipPath>')
    out.append(poly(wall, fill='url(#wall)'))
    out.append(poly(wall, fill='url(#foot)'))
    out.append(poly(wall, fill='none', stroke=C['edge'], stroke_opacity=C['eop'], stroke_width='2'))
    # rim front half on top, with a light top face and a bright outer edge
    rimf = [P(xr[i], yr[i], H) for i in front] + [P(xi[i], yi[i], H) for i in reversed(front)]
    out.append(poly(rimf, fill='url(#rim)'))
    edge = [P(xr[i], yr[i], H) for i in front]
    out.append('<path d="M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in edge) + f'" fill="none" stroke="#ffffff" stroke-opacity="{C["hl"]}" stroke-width="3" stroke-linecap="round"/>')
    out.append(f'<path d="{ring_d(xr, yr)}" fill="none" stroke="{C["edge"]}" stroke-opacity="{C["eop"]}" stroke-width="1.5"/>')
    return ''.join(defs), '\n'.join(out), dict(fit=fit, P=P, front=front, xi=xi, yi=yi, xo=xo, yo=yo, wall=wall)

def svg(dark=False, contents='', extra_defs=''):
    defs, body, _ = build(dark)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1024 1024" width="1024" height="1024">'
            f'<defs>{defs}{extra_defs}</defs>{body.replace("<!--CONTENTS-->", contents)}</svg>')

def sheet(svgs, name, size=520):
    import resvg_py
    from PIL import Image
    o = Image.new('RGBA', (len(svgs) * (size + 20), size + 20))
    for k, (dark, s) in enumerate(svgs):
        bg = Image.new('RGBA', (size + 20, size + 20), (40, 40, 44, 255) if dark else (236, 236, 240, 255))
        im = Image.open(io.BytesIO(bytes(resvg_py.svg_to_bytes(svg_string=s, width=size, height=size)))).convert('RGBA')
        bg.alpha_composite(im, (10, 10)); o.paste(bg, (k * (size + 20), 0))
    o.save(name)

if __name__ == '__main__':
    sheet([(False, svg(False)), (True, svg(True))], 'empty.png')
