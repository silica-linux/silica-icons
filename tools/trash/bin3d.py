"""A rounded-square bin modelled in 3D and projected to SVG polygons (no filters)."""
import math, io
import numpy as np

N = 4.6          # superellipse exponent: rounded square
TOP = 1.0        # half side at the rim
BOT = 0.80       # half side at the base
H = 2.3         # height
PITCH = math.radians(13)
STEPS = 96
WALL = 0.07      # rim thickness (inset of the inner ring)

def ring(half, steps=STEPS):
    t = np.linspace(0, 2 * math.pi, steps, endpoint=False)
    c, s = np.cos(t), np.sin(t)
    x = half * np.sign(c) * np.abs(c) ** (2 / N)
    y = half * np.sign(s) * np.abs(s) ** (2 / N)
    return t, x, y

def normals(x, y):
    # outward normal in the xy plane from the ring tangent
    dx = np.roll(x, -1) - np.roll(x, 1)
    dy = np.roll(y, -1) - np.roll(y, 1)
    nx, ny = dy, -dx
    l = np.hypot(nx, ny)
    return nx / l, ny / l

def project(x, y, z):
    persp = 1 - 0.06 * y            # farther = a little narrower
    sx = x * persp
    sy = -(z * math.cos(PITCH) + y * math.sin(PITCH))
    return sx, sy

class Fit:
    """World → 1024 canvas, fitted to the Trash keyline (656 × 824 at (184, 100))."""
    def __init__(self):
        _, x, y = ring(TOP)
        pts = [project(x, y, H), project(*ring(BOT)[1:], 0)]
        xs = np.concatenate([p[0] for p in pts]); ys = np.concatenate([p[1] for p in pts])
        self.k = min(656 / (xs.max() - xs.min()), 824 / (ys.max() - ys.min()))
        self.ox = 512 - self.k * (xs.max() + xs.min()) / 2
        self.oy = 924 - self.k * ys.max()
    def __call__(self, sx, sy):
        return self.ox + self.k * sx, self.oy + self.k * sy

def poly(pts, **attrs):
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ' Z'
    a = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<path d="{d}" {a}/>'

def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(a[i] + (b[i] - a[i]) * t):02x}' for i in range(3))
