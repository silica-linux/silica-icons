import math

PHI = (1 + 5 ** 0.5) / 2
SW = 1.5
GAP = SW * PHI * PHI
C = 12.0


def f(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def P(x, y):
    return f"{f(x)} {f(y)}"


def line(*pts):
    return "M" + " L".join(P(x, y) for x, y in pts)


def poly(*pts):
    return line(*pts) + "Z"


def circle(cx, cy, r):
    return f"M{P(cx - r, cy)}A{f(r)} {f(r)} 0 1 0 {P(cx + r, cy)}A{f(r)} {f(r)} 0 1 0 {P(cx - r, cy)}Z"


def arc(cx, cy, r, a0, a1):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{P(x0, y0)}A{f(r)} {f(r)} 0 {large} 1 {P(x1, y1)}"


def rrect(x, y, w, h, r):
    return (f"M{P(x + r, y)}H{f(x + w - r)}A{f(r)} {f(r)} 0 0 1 {P(x + w, y + r)}"
            f"V{f(y + h - r)}A{f(r)} {f(r)} 0 0 1 {P(x + w - r, y + h)}"
            f"H{f(x + r)}A{f(r)} {f(r)} 0 0 1 {P(x, y + h - r)}"
            f"V{f(y + r)}A{f(r)} {f(r)} 0 0 1 {P(x + r, y)}Z")


def dot(x, y, r=0.35):
    return circle(x, y, r)


S, F, FO = "s", "f", "F"

SYM = {}
CAT = {}


def add(cat, name, *els):
    SYM[name] = list(els)
    CAT[name] = cat


# Status & Connectivity -----------------------------------------------------
WIFI_O = (12, 18.6)
WIFI_R3 = 13.4
WIFI_R = [WIFI_R3 - 2 * GAP, WIFI_R3 - GAP, WIFI_R3]


def wifi(level):
    els = [(F if level >= 1 else F + "2", dot(WIFI_O[0], WIFI_O[1], 1.0))]
    for i, r in enumerate(WIFI_R):
        els.append((S if level >= i + 1 else S + "2", arc(WIFI_O[0], WIFI_O[1], r, -135, -45)))
    return els


add("status", "wifi-0", *wifi(0))
add("status", "wifi-1", *wifi(1))
add("status", "wifi-2", *wifi(2))
add("status", "wifi", *wifi(3))
add("status", "bluetooth",
    (S, line((6.8, 7.6), (16.6, 16.4), (12, 20.6), (12, 3.4), (16.6, 7.6), (6.8, 16.4))))

BAT_X, BAT_W = 2.75, 16.5
BAT_H = (BAT_W + SW) / PHI - SW
BAT_Y = C - BAT_H / 2
BAT_IN = BAT_X + 0.75 + 1.25
BAT_FULL = BAT_W - 1.5 - 2.5


def battery(level, extra=None):
    els = [(S, rrect(BAT_X, BAT_Y, BAT_W, BAT_H, 3.0)),
           (S, line((21.4, C - 1.9), (21.4, C + 1.9)))]
    if level:
        w = BAT_FULL * level
        els.append((FO, rrect(BAT_IN, BAT_Y + 2, w, BAT_H - 4, 1.4)))
    if extra:
        els.append(extra)
    return els


add("status", "battery", *battery(1))
add("status", "battery-50", *battery(1 / PHI))
add("status", "battery-10", *battery(1 / PHI ** 3))
add("status", "battery-charging",
    *battery(0, (FO, poly((12.9, 7.9), (8.4, 12.7), (11.5, 12.7), (10.9, 16.1), (15.4, 11.3), (12.3, 11.3)))))

SPK = poly((3.25, 9.4), (6.1, 9.4), (10.1, 5.9), (10.1, 18.1), (6.1, 14.6), (3.25, 14.6))
VOL_O = (9.4, 12)
VOL_R = [4.8, 4.8 + GAP, 4.8 + 2 * GAP]


def volume(level):
    els = [(F, SPK)]
    spans = [(-38, 38), (-44, 44), (-47, 47)]
    for i, r in enumerate(VOL_R):
        a0, a1 = spans[i]
        els.append((S if level >= i + 1 else S + "2", arc(VOL_O[0], VOL_O[1], r, a0, a1)))
    return els


add("status", "volume-slash",
    (F, SPK), (S, line((14.2, 9.2), (19.8, 14.8))), (S, line((19.8, 9.2), (14.2, 14.8))))
add("status", "volume-1", *volume(1))
add("status", "volume-2", *volume(2))
add("status", "volume", *volume(3))
add("status", "control-center",
    (S, rrect(3.75, 4.75, 16.5, 5.5, 2.75)), (F, dot(6.5, 7.5, 1.0)),
    (S, rrect(3.75, 13.75, 16.5, 5.5, 2.75)), (F, dot(17.5, 16.5, 1.0)))
GLASS_R = 10 / PHI - 0.75
add("status", "search",
    (S, circle(10.2, 10.2, GLASS_R)),
    (S, line((10.2 + GLASS_R * 0.7071, 10.2 + GLASS_R * 0.7071), (20.25, 20.25))))
add("status", "clock",
    (S, circle(C, C, 9.25)),
    (S, line((C, 12 - 9.25 / PHI), (C, C), (C + 9.25 / PHI ** 2 * 1.2, C + 9.25 / PHI ** 2 * 0.9))))
KB_W = 18.5
KB_H = 12.36 - 1.5
kby = C - KB_H / 2
add("status", "keyboard",
    (S, rrect(2.75, kby, KB_W, KB_H, 2.4)),
    *[(F, dot(x, kby + 3.35, 0.3)) for x in (6.6, 9.8, 13, 16.2)],
    *[(F, dot(x, kby + 3.35 + 2.6, 0.3)) for x in (8.2, 11.4, 14.6, 17.8)],
    (F, dot(6.6, kby + 5.95, 0.3)),
    (S, line((8.6, kby + 8.15), (15.4, kby + 8.15))))

# Control Center & Media ----------------------------------------------------
MR = 8.6
mo = MR / PHI
mc2 = (C + 2.0 + mo * 0.7071, C - 2.0 - mo * 0.7071)
cx1, cy1 = C, C


def crescent():
    r1 = MR
    r2 = MR / PHI * 1.12
    d = math.dist((cx1, cy1), mc2)
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(max(r1 ** 2 - a ** 2, 0))
    ux, uy = (mc2[0] - cx1) / d, (mc2[1] - cy1) / d
    px, py = cx1 + a * ux, cy1 + a * uy
    p1 = (px + h * uy, py - h * ux)
    p2 = (px - h * uy, py + h * ux)
    return (f"M{P(*p1)}A{f(r1)} {f(r1)} 0 1 0 {P(*p2)}"
            f"A{f(r2)} {f(r2)} 0 0 1 {P(*p1)}Z")


add("control", "moon", (F, crescent()))


def sun(cx, cy, rc, r0, r1, n=8, start=-90, only=None):
    els = [(S, circle(cx, cy, rc))]
    for i in range(n):
        a = math.radians(start + i * 360 / n)
        if only and i not in only:
            continue
        els.append((S, line((cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
                            (cx + r1 * math.cos(a), cy + r1 * math.sin(a)))))
    return els


SUN_RC = 10 / PHI ** 2 + 0.2
add("control", "sun", *sun(C, C, SUN_RC, SUN_RC + GAP, 9.25))
add("control", "screen-cast",
    (S, f"M7.6 17.2H5.15A2.4 2.4 0 0 1 2.75 14.8V5.6A2.4 2.4 0 0 1 5.15 3.2H18.85A2.4 2.4 0 0 1 21.25 5.6V14.8A2.4 2.4 0 0 1 18.85 17.2H16.4"),
    (F, poly((12, 14.6), (15.4, 19.9), (8.6, 19.9))))
add("control", "share-nearby",
    (S, circle(C - (10 - 10 / PHI), C, 10 / PHI - 0.75)), (S, circle(C + (10 - 10 / PHI), C, 10 / PHI - 0.75)))
add("control", "keyboard-brightness",
    (S, rrect(4.75, 14.75, 14.5, 5.5, 2.2)),
    *[(S, line((C + 4.4 * math.cos(math.radians(a)), 13.2 + 4.4 * math.sin(math.radians(a))),
               (C + 8.2 * math.cos(math.radians(a)), 13.2 + 8.2 * math.sin(math.radians(a)))))
      for a in (-90, -144, -36)])
add("control", "night-shift",
    (S, line((3.0, 16.4), (21.0, 16.4))),
    (S, arc(C, 16.4, 10 / PHI ** 2 + 0.6, 180, 360)),
    *[(S, line((C + 7.2 * math.cos(math.radians(a)), 16.4 + 7.2 * math.sin(math.radians(a))),
               (C + 9.6 * math.cos(math.radians(a)), 16.4 + 9.6 * math.sin(math.radians(a)))))
      for a in (-90, -135, -45, -162, -18)])
add("control", "play", (F, poly((8.0, 5.0), (19.0, 12.0), (8.0, 19.0))))
add("control", "pause", (F, rrect(6.5, 5.25, 3.0, 13.5, 0.6)), (F, rrect(14.5, 5.25, 3.0, 13.5, 0.6)))
add("control", "forward",
    (F, poly((3.5, 7.0), (11.4, 12.0), (3.5, 17.0))), (F, poly((12.6, 7.0), (20.5, 12.0), (12.6, 17.0))))
add("control", "backward",
    (F, poly((20.5, 7.0), (12.6, 12.0), (20.5, 17.0))), (F, poly((11.4, 7.0), (3.5, 12.0), (11.4, 17.0))))
add("control", "airplane",
    (F, "M12 3.1C12.8 3.1 13.15 4.1 13.15 5.3V9.9L20.6 14.2V15.9L13.15 13.6V17.6L15.6 19.3V20.8L12 19.9L8.4 20.8V19.3L10.85 17.6V13.6L3.4 15.9V14.2L10.85 9.9V5.3C10.85 4.1 11.2 3.1 12 3.1Z"))
HC = (12, 9.6)
add("control", "hotspot",
    (F, dot(HC[0], HC[1], 1.0)), (S, line((HC[0], HC[1] + GAP), (HC[0], 20.6))),
    (S, arc(HC[0], HC[1], 1.0 + GAP - 0.4, 135, 225)), (S, arc(HC[0], HC[1], 1.0 + GAP - 0.4, -45, 45)),
    (S, arc(HC[0], HC[1], 1.0 + 2 * GAP - 0.4, 140, 220)), (S, arc(HC[0], HC[1], 1.0 + 2 * GAP - 0.4, -40, 40)))

# Windows & Navigation ------------------------------------------------------
add("windows", "close", (S, circle(C, C, 9.25)),
    (S, line((C - 3.3, C - 3.3), (C + 3.3, C + 3.3))), (S, line((C + 3.3, C - 3.3), (C - 3.3, C + 3.3))))
add("windows", "minimize", (S, circle(C, C, 9.25)), (S, line((C - 4.4, C), (C + 4.4, C))))
add("windows", "fullscreen",
    (S, line((13.6, 10.4), (19.6, 4.4))), (S, line((14.2, 4.4), (19.6, 4.4), (19.6, 9.8))),
    (S, line((10.4, 13.6), (4.4, 19.6))), (S, line((4.4, 14.2), (4.4, 19.6), (9.8, 19.6))))
SB_H = (20 / PHI) - 1.5
sby = C - SB_H / 2
sbx = 2.75 + 18.5 / PHI ** 2
add("windows", "sidebar",
    (S, rrect(2.75, sby, 18.5, SB_H, 2.4)),
    (S, line((sbx, sby), (sbx, sby + SB_H))),
    (S, line((5.4, sby + 2.9), (sbx - 2.6, sby + 2.9))), (S, line((5.4, sby + 5.5), (sbx - 2.6, sby + 5.5))))
CH = 6.6
CD = CH * 0.786
add("windows", "chevron-right", (S, line((C - CD / 2, C - CH), (C + CD - CD / 2, C), (C - CD / 2, C + CH))))
add("windows", "chevron-left", (S, line((C + CD / 2, C - CH), (C - CD + CD / 2, C), (C + CD / 2, C + CH))))
add("windows", "chevron-down", (S, line((C - CH, C - CD / 2), (C, C + CD - CD / 2), (C + CH, C - CD / 2))))
add("windows", "chevron-up", (S, line((C - CH, C + CD / 2), (C, C - CD + CD / 2), (C + CH, C + CD / 2))))
add("windows", "ellipsis", *[(F, dot(x, C, 0.55)) for x in (5.2, 12, 18.8)])

# Editing & Text ------------------------------------------------------------
add("editing", "plus", (S, line((C, 4.0), (C, 20.0))), (S, line((4.0, C), (20.0, C))))
add("editing", "minus", (S, line((4.0, C), (20.0, C))))
add("editing", "checkmark", (S, line((4.6, 12.6), (9.4, 17.6), (19.4, 6.4))))
add("editing", "xmark", (S, line((5.6, 5.6), (18.4, 18.4))), (S, line((18.4, 5.6), (5.6, 18.4))))

# Files & Documents ----------------------------------------------------------
FD_W = 18.5
FD_H = FD_W / PHI
fdy = C - FD_H / 2 + 0.9
add("files", "folder",
    (S, f"M2.75 {f(fdy - 0.3)}V{f(fdy + FD_H - 2.4)}A2.4 2.4 0 0 0 5.15 {f(fdy + FD_H)}H18.85A2.4 2.4 0 0 0 21.25 {f(fdy + FD_H - 2.4)}V{f(fdy + 2.4)}A2.4 2.4 0 0 0 18.85 {f(fdy)}H11.2L9.6 {f(fdy - 2.0)}C9.3 {f(fdy - 2.4)} 9 {f(fdy - 2.5)} 8.5 {f(fdy - 2.5)}H4.95A2.2 2.2 0 0 0 2.75 {f(fdy - 0.3)}Z"),
    (S, line((2.75, fdy + 2.6), (21.25, fdy + 2.6))))
DOC_W = 20 / PHI - 1.5 + 1.6
DOC_X = C - DOC_W / 2
DOC_F = DOC_W / PHI ** 2 + 1.0
add("files", "doc",
    (S, f"M{P(DOC_X + DOC_W - DOC_F, 2.75)}H{f(DOC_X + 2.2)}A2.2 2.2 0 0 0 {P(DOC_X, 4.95)}V19.05A2.2 2.2 0 0 0 {P(DOC_X + 2.2, 21.25)}H{f(DOC_X + DOC_W - 2.2)}A2.2 2.2 0 0 0 {P(DOC_X + DOC_W, 19.05)}V{f(2.75 + DOC_F)}Z"),
    (S, line((DOC_X + DOC_W - DOC_F, 2.75), (DOC_X + DOC_W - DOC_F, 2.75 + DOC_F), (DOC_X + DOC_W, 2.75 + DOC_F))))
add("files", "trash",
    (S, line((3.6, 6.4), (20.4, 6.4))),
    (S, f"M9.1 6.4V5.2A1.7 1.7 0 0 1 10.8 3.5H13.2A1.7 1.7 0 0 1 14.9 5.2V6.4"),
    (S, "M5.6 6.4L6.6 18.9A2.1 2.1 0 0 0 8.7 20.8H15.3A2.1 2.1 0 0 0 17.4 18.9L18.4 6.4"),
    (S, line((10.0, 10.0), (10.0, 16.8))), (S, line((14.0, 10.0), (14.0, 16.8))))
add("files", "share",
    (S, "M8.6 9.4H7.15A2.4 2.4 0 0 0 4.75 11.8V18.45A2.4 2.4 0 0 0 7.15 20.85H16.85A2.4 2.4 0 0 0 19.25 18.45V11.8A2.4 2.4 0 0 0 16.85 9.4H15.4"),
    (S, line((C, 3.2), (C, 14.4))), (S, line((8.6, 6.6), (C, 3.2), (15.4, 6.6))))
add("files", "download",
    (S, line((C, 3.4), (C, 15.4))), (S, line((7.4, 10.8), (C, 15.4), (16.6, 10.8))),
    (S, line((4.4, 20.4), (19.6, 20.4))))
add("files", "upload",
    (S, line((C, 15.4), (C, 3.4))), (S, line((7.4, 8.0), (C, 3.4), (16.6, 8.0))),
    (S, line((4.4, 20.4), (19.6, 20.4))))
add("files", "link",
    (S, "M10.9 7.1L12.6 5.4A4.1 4.1 0 0 1 18.6 11.4L16.9 13.1"),
    (S, "M13.1 16.9L11.4 18.6A4.1 4.1 0 0 1 5.4 12.6L7.1 10.9"),
    (S, line((9.4, 14.6), (14.6, 9.4))))

# Communication --------------------------------------------------------------
add("communication", "bell",
    (S, "M12 3.4A6.1 6.1 0 0 0 5.9 9.5V14.6L4.1 17.1H19.9L18.1 14.6V9.5A6.1 6.1 0 0 0 12 3.4Z"),
    (S, "M9.6 19.9A2.5 2.5 0 0 0 14.4 19.9"))

# People & Security ----------------------------------------------------------
add("people", "person",
    (S, circle(C, 7.8, 10 / PHI ** 2 + 0.2)),
    (S, "M4.6 20.6C4.6 16.6 7.9 13.9 12 13.9C16.1 13.9 19.4 16.6 19.4 20.6Z"))
LK_W = 14.5
LK_H = (LK_W + 1.5) / PHI - 1.5
lky = 20.4 - LK_H
add("people", "lock",
    (S, rrect(C - LK_W / 2, lky, LK_W, LK_H, 2.4)),
    (S, f"M8.2 {f(lky)}V7.4A3.8 3.8 0 0 1 15.8 7.4V{f(lky)}"),
    (F, dot(C, lky + LK_H / 2, 0.6)))
add("people", "lock-open",
    (S, rrect(C - LK_W / 2, lky, LK_W, LK_H, 2.4)),
    (S, f"M15.8 {f(lky)}V7.4A3.8 3.8 0 0 0 8.2 7.4V8.2"),
    (F, dot(C, lky + LK_H / 2, 0.6)))

# Shapes & Indicators --------------------------------------------------------
add("shapes", "info", (S, circle(C, C, 9.25)), (F, dot(C, 7.9, 0.55)), (S, line((C, 11.0), (C, 16.6))))
add("shapes", "warning",
    (S, "M10.4 4.4A1.85 1.85 0 0 1 13.6 4.4L21.0 17.5A1.85 1.85 0 0 1 19.4 20.3H4.6A1.85 1.85 0 0 1 3.0 17.5Z"),
    (S, line((C, 9.4), (C, 13.6))), (F, dot(C, 16.7, 0.55)))
SR = 9.9
SRI = SR / PHI ** 2
star = []
for i in range(10):
    r = SR if i % 2 == 0 else SRI
    a = math.radians(-90 + i * 36)
    star.append((C + r * math.cos(a), C + 0.85 + r * math.sin(a)))
add("shapes", "star", (S, poly(*star)))
add("shapes", "heart",
    (S, "M12 19.6C6 15.6 3.1 12.4 3.1 8.9C3.1 6.2 5.1 4.3 7.6 4.3C9.5 4.3 11 5.4 12 7C13 5.4 14.5 4.3 16.4 4.3C18.9 4.3 20.9 6.2 20.9 8.9C20.9 12.4 18 15.6 12 19.6Z"))

# Settings -------------------------------------------------------------------


def gear():
    n = 8
    ro, ri = 9.4, 9.4 - 10 / PHI ** 3 - 0.1
    pts = []
    for i in range(n):
        base = i * 360 / n - 90
        for da, r in ((-11, ro), (11, ro), (22.5 - 9, ri), (22.5 + 9, ri)):
            a = math.radians(base + da)
            pts.append((C + r * math.cos(a), C + r * math.sin(a)))
    return poly(*pts)


add("settings", "gear", (S, gear()), (S, circle(C, C, 10 / PHI ** 2 - 0.2)))
add("settings", "power",
    (S, arc(C, 12.8, 8.1, -55, 235)), (S, line((C, 3.2), (C, 11.6))))
add("settings", "zoom-in",
    (S, circle(10.2, 10.2, GLASS_R)),
    (S, line((10.2 + GLASS_R * 0.7071, 10.2 + GLASS_R * 0.7071), (20.25, 20.25))),
    (S, line((10.2, 7.4), (10.2, 13.0))), (S, line((7.4, 10.2), (13.0, 10.2))))

# ===========================================================================
# Fase 2. Primitive per tagli e rotazioni: un tracciato si descrive come
# lista di segmenti ("L" retta, "A" arco in senso orario, "C" cubica), così le
# varianti -slash e i badge tagliano i tratti con la luce minima della specifica.
# ===========================================================================
CUT = 0.75 + 1.5 + 0.75  # asse del taglio -> asse del tratto tagliato (luce 1,5)


def pL(*pts):
    return ("L", [tuple(p) for p in pts])


def pA(cx, cy, r, a0, a1):
    while a1 <= a0:
        a1 += 360
    return ("A", cx, cy, r, a0, a1)


def pAr(cx, cy, r, a0, a1):
    """Arco in senso antiorario da a0 ad a1 (viene invertito)."""
    p = pA(cx, cy, r, a1, a0)
    return ("R",) + p[1:]


def pC(p0, p1, p2, p3):
    return ("C", tuple(p0), tuple(p1), tuple(p2), tuple(p3))


def p_rrect(x, y, w, h, r):
    return [pL((x + r, y), (x + w - r, y)), pA(x + w - r, y + r, r, -90, 0),
            pL((x + w, y + r), (x + w, y + h - r)), pA(x + w - r, y + h - r, r, 0, 90),
            pL((x + w - r, y + h), (x + r, y + h)), pA(x + r, y + h - r, r, 90, 180),
            pL((x, y + h - r), (x, y + r)), pA(x + r, y + r, r, 180, 270)]


def p_circle(cx, cy, r):
    return [pA(cx, cy, r, 0, 180), pA(cx, cy, r, 180, 360)]


def _split(pr):
    if pr[0] == "L" and len(pr[1]) > 2:
        return [pL(a, b) for a, b in zip(pr[1], pr[1][1:])]
    return [pr]


def ppt(pr, t):
    k = pr[0]
    if k == "L":
        (x0, y0), (x1, y1) = pr[1][0], pr[1][-1]
        return (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
    if k in "AR":
        a = pr[4] + (pr[5] - pr[4]) * (t if k == "A" else 1 - t)
        a = math.radians(a)
        return (pr[1] + pr[3] * math.cos(a), pr[2] + pr[3] * math.sin(a))
    p0, p1, p2, p3 = pr[1:]
    u = 1 - t
    return tuple(u ** 3 * p0[i] + 3 * u * u * t * p1[i] + 3 * u * t * t * p2[i] + t ** 3 * p3[i] for i in range(2))


def _csplit(p, t):
    p0, p1, p2, p3 = p

    def lerp(a, b):
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    a, b, c = lerp(p0, p1), lerp(p1, p2), lerp(p2, p3)
    d, e = lerp(a, b), lerp(b, c)
    m = lerp(d, e)
    return (p0, a, d, m), (m, e, c, p3)


def psub(pr, t0, t1):
    k = pr[0]
    if k == "L":
        return pL(ppt(pr, t0), ppt(pr, t1))
    if k == "A":
        s = pr[5] - pr[4]
        return ("A", pr[1], pr[2], pr[3], pr[4] + s * t0, pr[4] + s * t1)
    if k == "R":
        s = pr[5] - pr[4]
        return ("R", pr[1], pr[2], pr[3], pr[5] - s * t1, pr[5] - s * t0)
    left, _ = _csplit(pr[1:], t1)
    _, mid = _csplit(left, t0 / t1 if t1 else 0)
    return ("C",) + mid


def plen(pr, n=24):
    pts = [ppt(pr, i / n) for i in range(n + 1)]
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def cut(prims, keep, n=400, minlen=0.5):
    out = []
    for pr in [q for p in prims for q in _split(p)]:
        flags = [keep(*ppt(pr, i / n)) for i in range(n + 1)]
        i = 0
        while i <= n:
            if not flags[i]:
                i += 1
                continue
            j = i
            while j < n and flags[j + 1]:
                j += 1
            t0, t1 = i / n, j / n
            if i > 0:
                lo, hi = (i - 1) / n, i / n
                for _ in range(30):
                    m = (lo + hi) / 2
                    lo, hi = (lo, m) if keep(*ppt(pr, m)) else (m, hi)
                t0 = hi
            if j < n:
                lo, hi = j / n, (j + 1) / n
                for _ in range(30):
                    m = (lo + hi) / 2
                    lo, hi = (m, hi) if keep(*ppt(pr, m)) else (lo, m)
                t1 = lo
            piece = psub(pr, t0, t1) if (t0, t1) != (0, 1) else pr
            if plen(piece) >= minlen:
                out.append(piece)
            i = j + 1
    return out


def _end(pr):
    return ppt(pr, 1)


def paths(prims):
    """Unisce i segmenti contigui e restituisce un tracciato per sottotracciato."""
    subs, cur, first, last = [], "", None, None
    for pr in prims:
        s, e = ppt(pr, 0), ppt(pr, 1)
        if last is None or math.dist(last, s) > 1e-3:
            if cur:
                subs.append(cur + ("Z" if math.dist(first, last) < 1e-3 else ""))
            cur, first = "M" + P(*s), s
        k = pr[0]
        if k == "L":
            cur += "".join("L" + P(*q) for q in pr[1][1:])
        elif k in "AR":
            sw = pr[5] - pr[4]
            fl = "1" if k == "A" else "0"
            if sw >= 359.9:
                mid = ppt(pr, 0.5)
                cur += f"A{f(pr[3])} {f(pr[3])} 0 0 {fl} {P(*mid)}"
            cur += f"A{f(pr[3])} {f(pr[3])} 0 {1 if 180 < sw < 359.9 else 0} {fl} {P(*e)}"
        else:
            cur += "C" + " ".join(P(*q) for q in pr[2:])
        last = e
    if cur:
        subs.append(cur + ("Z" if math.dist(first, last) < 1e-3 else ""))
    return subs


def E(mode, prims):
    return [(mode, d) for d in paths(prims)]


def rot_prims(prims, ang, c=(C, C), dx=0.0, dy=0.0):
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))

    def R(p):
        x, y = p[0] - c[0], p[1] - c[1]
        return (c[0] + x * ca - y * sa + dx, c[1] + x * sa + y * ca + dy)
    out = []
    for pr in prims:
        k = pr[0]
        if k == "L":
            out.append(pL(*[R(p) for p in pr[1]]))
        elif k in "AR":
            cx, cy = R((pr[1], pr[2]))
            out.append((k, cx, cy, pr[3], pr[4] + ang, pr[5] + ang))
        else:
            out.append(pC(*[R(p) for p in pr[1:]]))
    return out


def seg_dist(p, a, b):
    ax, ay, bx, by = *a, *b
    vx, vy = bx - ax, by - ay
    L2 = vx * vx + vy * vy
    t = 0 if L2 == 0 else max(0, min(1, ((p[0] - ax) * vx + (p[1] - ay) * vy) / L2))
    return math.dist(p, (ax + vx * t, ay + vy * t))


SLASH = ((4.25, 4.25), (19.75, 19.75))


def slashed(prims, a=SLASH[0], b=SLASH[1], d=CUT):
    return cut(prims, lambda x, y: seg_dist((x, y), a, b) >= d)


def sample(prims, n=48):
    pts = []
    for pr in prims:
        pts += [ppt(pr, i / n) for i in range(n + 1)]
    return pts


def inside(p, poly_pts):
    x, y = p
    c = False
    for (x0, y0), (x1, y1) in zip(poly_pts, poly_pts[1:] + poly_pts[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            c = not c
    return c


def outside_shape(shape_prims, d=CUT):
    pts = sample(shape_prims)
    segs = list(zip(pts, pts[1:]))

    def keep(x, y):
        if inside((x, y), pts):
            return False
        return min(seg_dist((x, y), a, b) for a, b in segs) >= d
    return keep


def unit(dx, dy):
    n = math.hypot(dx, dy)
    return dx / n, dy / n


def head(tip, d, leg=6.2, spread=45):
    ux, uy = unit(*d)
    pts = []
    for s in (spread, -spread):
        a = math.radians(s)
        bx, by = -ux, -uy
        pts.append((tip[0] + leg * (bx * math.cos(a) - by * math.sin(a)),
                    tip[1] + leg * (bx * math.sin(a) + by * math.cos(a))))
    return line(pts[0], tip, pts[1])


def arrow(a, b, leg=6.2):
    return [(S, line(a, b)), (S, head(b, (b[0] - a[0], b[1] - a[1]), leg))]


def arc_head(cx, cy, r, a, cw=True, leg=4.4):
    t = math.radians(a)
    tip = (cx + r * math.cos(t), cy + r * math.sin(t))
    d = (-math.sin(t), math.cos(t)) if cw else (math.sin(t), -math.cos(t))
    return head(tip, d, leg)


def shifted(prims, dx, dy):
    return rot_prims(prims, 0, dx=dx, dy=dy)


def cloud_prims(s=1.0, dx=0.0, dy=0.0):
    lc, lr = (7.15, 14.75), 3.5
    bc, br = (12.4, 10.9), 5.4
    rc, rr = (17.05, 14.35), 3.9
    base = 18.25

    def X(c1, r1, c2, r2):
        d = math.dist(c1, c2)
        a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(max(r1 ** 2 - a ** 2, 0))
        ux, uy = (c2[0] - c1[0]) / d, (c2[1] - c1[1]) / d
        px, py = c1[0] + a * ux, c1[1] + a * uy
        p1, p2 = (px + h * uy, py - h * ux), (px - h * uy, py + h * ux)
        return p1 if p1[1] < p2[1] else p2
    i1, i2 = X(lc, lr, bc, br), X(bc, br, rc, rr)

    def ang(c, p):
        return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))
    pr = [pA(*lc, lr, 90, ang(lc, i1)), pA(*bc, br, ang(bc, i1), ang(bc, i2)),
          pA(*rc, rr, ang(rc, i2), 90), pL((rc[0], base), (lc[0], base))]
    T = lambda p: (C + (p[0] - C) * s + dx, C + (p[1] - C) * s + dy)
    out = []
    for q in pr:
        if q[0] == "L":
            out.append(pL(*[T(p) for p in q[1]]))
        else:
            cx, cy = T((q[1], q[2]))
            out.append(("A", cx, cy, q[3] * s, q[4], q[5]))
    return out


def crescent_prims(cx, cy, r1, oc, r2):
    d = math.dist((cx, cy), oc)
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(max(r1 ** 2 - a ** 2, 0))
    ux, uy = (oc[0] - cx) / d, (oc[1] - cy) / d
    px, py = cx + a * ux, cy + a * uy
    p1, p2 = (px + h * uy, py - h * ux), (px - h * uy, py + h * ux)

    def ang(c, p):
        return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))
    return [pAr(cx, cy, r1, ang((cx, cy), p1), ang((cx, cy), p2)), pA(*oc, r2, ang(oc, p2), ang(oc, p1))]


# Status & Connectivity (fase 2) ----------------------------------------------
def wifi_prims():
    return [pA(WIFI_O[0], WIFI_O[1], r, -135, -45) for r in WIFI_R]


add("status", "wifi-slash",
    (F, dot(WIFI_O[0], WIFI_O[1], 1.0)), *E(S, slashed(wifi_prims())), (S, line(*SLASH)))
BT = [(6.8, 7.6), (16.6, 16.4), (12, 20.6), (12, 3.4), (16.6, 7.6), (6.8, 16.4)]
add("status", "bluetooth-slash", *E(S, slashed([pL(*BT)])), (S, line(*SLASH)))
add("status", "battery-0", *battery(0))
add("status", "volume-0", *volume(0))


def signal(level):
    els = []
    w, gap = 1.4 + 1.5, SW * PHI
    x0 = C - (4 * w + 3 * gap) / 2
    for i in range(4):
        top = 19.25 - (5.5 + 3.0 * i)
        x = x0 + i * (w + gap)
        els.append((F if level > i else F + "2", rrect(x + 0.75, top + 0.75, 1.4, 19.25 - 0.75 - top - 0.75, 0.7)))
    return els


add("status", "signal-1", *signal(1))
add("status", "signal-2", *signal(2))
add("status", "signal-3", *signal(3))
add("status", "signal", *signal(4))
add("status", "ethernet",
    (S, "M6.15 4.75H17.85A2.4 2.4 0 0 1 20.25 7.15V15.5H16.5V19.25H7.5V15.5H3.75V7.15A2.4 2.4 0 0 1 6.15 4.75Z"),
    *[(S, line((x, 8.5), (x, 10.75))) for x in (8.6, 12, 15.4)])
add("status", "network",
    (S, rrect(9.25, 3.75, 5.5, 4.4, 1.2)), (S, rrect(3.75, 15.85, 5.5, 4.4, 1.2)), (S, rrect(14.75, 15.85, 5.5, 4.4, 1.2)),
    (S, line((C, 8.15), (C, 12))), (S, line((6.5, 15.85), (6.5, 12), (17.5, 12), (17.5, 15.85))))
GL = math.sqrt(9.25 ** 2 - 4.6 ** 2)
add("status", "globe",
    (S, circle(C, C, 9.25)), (S, "M12 2.75A4 9.25 0 0 0 12 21.25A4 9.25 0 0 0 12 2.75Z"),
    (S, line((2.75, C), (21.25, C))), (S, line((C - GL, 7.4), (C + GL, 7.4))), (S, line((C - GL, 16.6), (C + GL, 16.6))))
LOC = [(19.9, 4.1), (4.1, 10.9), (11.1, 12.9), (13.1, 19.9)]
add("status", "location", (S, poly(*LOC)))
add("status", "location-fill", (F, poly(*LOC)))
MIC = p_rrect(8.75, 2.75, 6.5, 11.5, 3.25)
MIC_ST = [pA(C, 10.75, 6.25, 0, 180), pL((C, 17.0), (C, 20.75))]
add("status", "mic", *E(S, MIC), *E(S, MIC_ST))
add("status", "mic-fill", (F, rrect(8.75, 2.75, 6.5, 11.5, 3.25)), *E(S, MIC_ST))
add("status", "mic-slash", *E(S, slashed(MIC + MIC_ST)), (S, line(*SLASH)))
BOLT = [(14.1, 3.4), (4.65, 13.45), (11.15, 13.45), (9.9, 20.6), (19.35, 10.55), (12.85, 10.55)]
add("status", "bolt", (S, poly(*BOLT)))
add("status", "bolt-fill", (F, poly(*BOLT)))
add("status", "plug",
    (S, line((9.75, 3.25), (9.75, 7.75))), (S, line((14.25, 3.25), (14.25, 7.75))),
    (S, "M7.25 7.75H16.75V11.25A4.75 4.75 0 0 1 7.25 11.25Z"), (S, line((C, 16.0), (C, 20.75))))
add("status", "screen-share",
    (S, rrect(2.75, 3.75, 18.5, 12.5, 2.4)), (S, line((C, 16.25), (C, 20.25))), (S, line((8.25, 20.25), (15.75, 20.25))),
    (S, line((C, 13.25), (C, 7.25))), (S, line((9.25, 10.0), (C, 7.25), (14.75, 10.0))))

RA = 8.25

# Control Center & Media (fase 2) ---------------------------------------------
add("control", "stop", (F, rrect(6.0, 6.0, 12.0, 12.0, 1.2)))
add("control", "record", (F, circle(C, C, 6.5)))
add("control", "record-circle", (S, circle(C, C, 9.25)), (F, circle(C, C, 10 / PHI ** 2 / 2 * 2 - 0.75)))
add("control", "eject", (F, poly((C, 5.5), (19.0, 13.0), (5.0, 13.0))), (F, rrect(5.0, 17.25, 14.0, 1.25, 0.5)))
add("control", "play-pause",
    (F, poly((3.75, 7.0), (10.5, 12.0), (3.75, 17.0))),
    (F, rrect(13.5, 7.0, 1.75, 10.0, 0.5)), (F, rrect(18.25, 7.0, 1.75, 10.0, 0.5)))
add("control", "play-circle", (S, circle(C, C, 9.25)), (F, poly((10.0, 8.0), (16.0, 12.0), (10.0, 16.0))))
add("control", "pause-circle", (S, circle(C, C, 9.25)),
    (F, rrect(8.75, 8.0, 1.75, 8.0, 0.4)), (F, rrect(13.5, 8.0, 1.75, 8.0, 0.4)))
add("control", "skip-forward", (F, poly((4.5, 6.0), (14.75, 12.0), (4.5, 18.0))), (F, rrect(17.75, 6.0, 1.75, 12.0, 0.5)))
add("control", "skip-backward", (F, poly((19.5, 6.0), (9.25, 12.0), (19.5, 18.0))), (F, rrect(4.5, 6.0, 1.75, 12.0, 0.5)))
RP = [(S, "M4.75 12.8V9.6A3 3 0 0 1 7.75 6.6H19.25"), (S, line((16.75, 4.1), (19.25, 6.6), (16.75, 9.1))),
      (S, "M19.25 11.2V14.4A3 3 0 0 1 16.25 17.4H4.75"), (S, line((7.25, 14.9), (4.75, 17.4), (7.25, 19.9)))]
add("control", "repeat", *RP)
add("control", "repeat-1", *RP, (S, line((10.9, 10.7), (12.4, 9.6), (12.4, 14.4))))
add("control", "shuffle",
    (S, "M3.75 7.25H6.5C10.6 7.25 12.9 16.75 17 16.75H20.25"), (S, "M3.75 16.75H6.5C10.6 16.75 12.9 7.25 17 7.25H20.25"),
    (S, line((17.75, 4.75), (20.25, 7.25), (17.75, 9.75))), (S, line((17.75, 14.25), (20.25, 16.75), (17.75, 19.25))))
add("control", "music-note",
    (F, circle(7.0, 17.25, 2.25)), (F, circle(17.0, 15.25, 2.25)),
    (S, line((9.25, 17.25), (9.25, 6.25), (19.25, 4.25), (19.25, 15.25))), (S, line((9.25, 9.75), (19.25, 7.75))))
add("control", "music-list",
    (S, line((3.75, 4.75), (15.25, 4.75))), (S, line((3.75, 9.25), (13.25, 9.25))), (S, line((3.75, 13.75), (10.25, 13.75))),
    (F, circle(15.75, 17.25, 2.0)), (S, line((17.75, 17.25), (17.75, 8.25), (20.5, 9.25))))
WV = [1.75, 4.5, 8.0, 5.25, 8.25, 4.0, 1.75]
add("control", "waveform", *[(S, line((3.0 + 3 * i, C - h), (3.0 + 3 * i, C + h))) for i, h in enumerate(WV)])
CAP_H = 12.36 - 1.5
add("control", "captions",
    (S, rrect(2.75, C - CAP_H / 2, 18.5, CAP_H, 2.4)), (S, arc(8.7, C, 2.4, 45, 315)), (S, arc(15.3, C, 2.4, 45, 315)))
add("control", "sun-min", (S, circle(C, C, SUN_RC)),
    *[(F, dot(C + 7.6 * math.cos(math.radians(a)), C + 7.6 * math.sin(math.radians(a)), 0.45)) for a in range(-90, 270, 45)])
add("control", "keyboard-brightness-min",
    (S, rrect(4.75, 14.75, 14.5, 5.5, 2.2)),
    *[(F, dot(C + 6.6 * math.cos(math.radians(a)), 13.2 + 6.6 * math.sin(math.radians(a)), 0.45)) for a in (-90, -144, -36)])
add("control", "appearance", (S, circle(C, C, 9.25)), (F, "M12 2.75A9.25 9.25 0 0 0 12 21.25Z"))
add("control", "rotation-lock",
    (S, arc(C, C, RA, 20, 330)), (S, arc_head(C, C, RA, 330, cw=True)),
    (S, rrect(8.5, 11.0, 7.0, 5.0, 1.4)), (S, "M10 11V9.6A2 2 0 0 1 14 9.6V11"))

# Windows & Navigation (fase 2) -----------------------------------------------
add("windows", "arrow-up", *arrow((C, 20.0), (C, 4.0)))
add("windows", "arrow-down", *arrow((C, 4.0), (C, 20.0)))
add("windows", "arrow-left", *arrow((20.0, C), (4.0, C)))
add("windows", "arrow-right", *arrow((4.0, C), (20.0, C)))
DG = 5.9
add("windows", "arrow-up-right", *arrow((C - DG, C + DG), (C + DG, C - DG), 8.2))
add("windows", "arrow-up-left", *arrow((C + DG, C + DG), (C - DG, C - DG), 8.2))
add("windows", "arrow-down-right", *arrow((C - DG, C - DG), (C + DG, C + DG), 8.2))
add("windows", "arrow-down-left", *arrow((C + DG, C - DG), (C - DG, C + DG), 8.2))
RA = 8.25
add("windows", "arrow-clockwise", (S, arc(C, C, RA, 20, 330)), (S, arc_head(C, C, RA, 330, cw=True)))
add("windows", "arrow-counterclockwise", (S, arc(C, C, RA, 210, 520)), (S, arc_head(C, C, RA, 210, cw=False)))
add("windows", "arrow-left-right",
    (S, line((4.0, 8.0), (20.0, 8.0))), (S, line((16.75, 4.75), (20.0, 8.0), (16.75, 11.25))),
    (S, line((20.0, 16.0), (4.0, 16.0))), (S, line((7.25, 12.75), (4.0, 16.0), (7.25, 19.25))))
add("windows", "arrow-up-down",
    (S, line((8.0, 20.0), (8.0, 4.0))), (S, line((4.75, 7.25), (8.0, 4.0), (11.25, 7.25))),
    (S, line((16.0, 4.0), (16.0, 20.0))), (S, line((12.75, 16.75), (16.0, 20.0), (19.25, 16.75))))
add("windows", "chevron-up-down", (S, line((8.0, 9.5), (C, 5.5), (16.0, 9.5))), (S, line((8.0, 14.5), (C, 18.5), (16.0, 14.5))))
add("windows", "ellipsis-vertical", *[(F, dot(C, y, 0.55)) for y in (5.2, 12, 18.8)])
add("windows", "ellipsis-circle", (S, circle(C, C, 9.25)), *[(F, dot(x, C, 0.5)) for x in (7.9, 12, 16.1)])
add("windows", "exit-fullscreen",
    (S, line((19.6, 4.4), (13.6, 10.4))), (S, line((13.6, 5.0), (13.6, 10.4), (19.0, 10.4))),
    (S, line((4.4, 19.6), (10.4, 13.6))), (S, line((10.4, 19.0), (10.4, 13.6), (5.0, 13.6))))
WN = (2.75, 4.25, 18.5, 15.5)
add("windows", "window", (S, rrect(*WN, 2.4)), (S, line((2.75, 8.25), (21.25, 8.25))))
add("windows", "window-stack",
    (S, rrect(2.75, 7.25, 15.0, 13.0, 2.4)), (S, line((2.75, 11.0), (17.75, 11.0))),
    (S, "M6.25 7.25V6.15A2.4 2.4 0 0 1 8.65 3.75H18.85A2.4 2.4 0 0 1 21.25 6.15V14.35A2.4 2.4 0 0 1 18.85 16.75H17.75"))
add("windows", "window-split", (S, rrect(*WN, 2.4)), (S, line((C, 4.25), (C, 19.75))))
sbx_r = 21.25 - 18.5 / PHI ** 2
add("windows", "sidebar-right",
    (S, rrect(2.75, sby, 18.5, SB_H, 2.4)), (S, line((sbx_r, sby), (sbx_r, sby + SB_H))),
    (S, line((sbx_r + 2.6, sby + 2.9), (18.6, sby + 2.9))), (S, line((sbx_r + 2.6, sby + 5.5), (18.6, sby + 5.5))))
pby = sby + SB_H - SB_H / PHI ** 2
add("windows", "panel-bottom", (S, rrect(2.75, sby, 18.5, SB_H, 2.4)), (S, line((2.75, pby), (21.25, pby))))
add("windows", "square-grid-2x2", *[(S, rrect(x, y, 6.75, 6.75, 1.6)) for x in (3.75, 13.5) for y in (3.75, 13.5)])
add("windows", "circle-grid-3x3", *[(F, dot(x, y, 1.15)) for y in (5.0, 12, 19.0) for x in (5.0, 12, 19.0)])
add("windows", "dock", (S, rrect(*WN, 2.4)), (S, line((7.5, 16.25), (16.5, 16.25))))
add("windows", "menubar", (S, rrect(*WN, 2.4)), (F, "M2.75 7.75V6.65A2.4 2.4 0 0 1 5.15 4.25H18.85A2.4 2.4 0 0 1 21.25 6.65V7.75Z"))
add("windows", "tabs", (S, rrect(*WN, 2.4)), (S, line((2.75, 8.75), (21.25, 8.75))),
    (S, line((9.0, 4.25), (9.0, 8.75))), (S, line((15.25, 4.25), (15.25, 8.75))))
add("windows", "pip", (S, rrect(*WN, 2.4)), (F, rrect(12.25, 12.0, 6.0, 4.75, 1.0)))
HOUSE = "M5.75 8.9V17.85A2.4 2.4 0 0 0 8.15 20.25H15.85A2.4 2.4 0 0 0 18.25 17.85V8.9"
add("windows", "house", (S, line((3.25, 11.0), (C, 3.5), (20.75, 11.0))), (S, HOUSE),
    (S, "M10 20.25V15.4A1 1 0 0 1 11 14.4H13A1 1 0 0 1 14 15.4V20.25"))
add("windows", "house-fill", (S, line((3.25, 11.0), (C, 3.5), (20.75, 11.0))),
    (F, "M12 3.5L18.25 8.86V17.85A2.4 2.4 0 0 1 15.85 20.25H8.15A2.4 2.4 0 0 1 5.75 17.85V8.86Z"))
add("windows", "line-3", *[(S, line((4.0, y), (20.0, y))) for y in (6.0, 12.0, 18.0)])
add("windows", "compass", (S, circle(C, C, 9.25)),
    (S, poly((16.0, 8.0), (13.4, 13.4), (8.0, 16.0), (10.6, 10.6))), (F, poly((16.0, 8.0), (13.4, 13.4), (10.6, 10.6))))

# Editing & Text (fase 2) -------------------------------------------------------


def pencil(L0=10.5, L1=8.25, w=2.6, cone=5.0, band=3.75, ang=-45, c=(C, C), dx=0.0, dy=0.0, r=1.2):
    x0, x1, yc = c[0] - L0, c[0] + L1, c[1]
    pr = [pL((x0, yc), (x0 + cone, yc - w), (x1 - r, yc - w)), pA(x1 - r, yc - w + r, r, -90, 0),
          pL((x1, yc - w + r), (x1, yc + w - r)), pA(x1 - r, yc + w - r, r, 0, 90),
          pL((x1 - r, yc + w), (x0 + cone, yc + w), (x0, yc))]
    extra = [pL((x0 + cone, yc - w), (x0 + cone, yc + w))]
    if band:
        extra.append(pL((x1 - band, yc - w), (x1 - band, yc + w)))
    return rot_prims(pr, ang, c, dx, dy), rot_prims(extra, ang, c, dx, dy)


pa, pb = pencil()
add("editing", "pencil", *E(S, pa), *E(S, pb))
pa, pb = pencil(L0=7.6, L1=5.4, w=2.0, cone=3.6, band=0, c=(14.5, 9.5), r=1.0)
add("editing", "compose",
    (S, "M10.5 4.25H6.15A2.4 2.4 0 0 0 3.75 6.65V17.85A2.4 2.4 0 0 0 6.15 20.25H17.35A2.4 2.4 0 0 0 19.75 17.85V13.5"),
    *E(S, pa), *E(S, pb))
add("editing", "scissors", (S, circle(6.75, 17.25, 2.75)), (S, circle(17.25, 17.25, 2.75)),
    (S, line((8.7, 15.3), (17.5, 3.75))), (S, line((15.3, 15.3), (6.5, 3.75))))
add("editing", "copy", (S, rrect(3.75, 7.25, 12.5, 13.0, 2.4)),
    (S, "M7.75 7.25V6.15A2.4 2.4 0 0 1 10.15 3.75H17.85A2.4 2.4 0 0 1 20.25 6.15V14.35A2.4 2.4 0 0 1 17.85 16.75H16.25"))
add("editing", "clipboard",
    (S, "M8.75 4.75H7.15A2.4 2.4 0 0 0 4.75 7.15V18.35A2.4 2.4 0 0 0 7.15 20.75H16.85A2.4 2.4 0 0 0 19.25 18.35V7.15A2.4 2.4 0 0 0 16.85 4.75H15.25"),
    (S, rrect(8.75, 3.25, 6.5, 3.25, 1.2)))
add("editing", "undo", (S, "M4.25 9.25H14.5A5 5 0 0 1 14.5 19.25H9.5"), (S, line((8.25, 5.25), (4.25, 9.25), (8.25, 13.25))))
add("editing", "redo", (S, "M19.75 9.25H9.5A5 5 0 0 0 9.5 19.25H14.5"), (S, line((15.75, 5.25), (19.75, 9.25), (15.75, 13.25))))
add("editing", "text-bold",
    (S, "M6.85 4.5H12.35A3.5 3.5 0 0 1 12.35 11.5H6.85Z"), (S, "M6.85 11.5H13.1A4 4 0 0 1 13.1 19.5H6.85Z"))
add("editing", "text-italic", (S, line((13.75, 4.5), (10.25, 19.5))), (S, line((10.5, 4.5), (17.0, 4.5))), (S, line((7.0, 19.5), (13.5, 19.5))))
add("editing", "text-underline", (S, "M7.75 4.25V11.25A4.25 4.25 0 0 0 16.25 11.25V4.25"), (S, line((5.75, 20.0), (18.25, 20.0))))
add("editing", "text-strikethrough",
    (S, "M16.1 6.9C15.4 5.2 13.9 4.25 12 4.25C9.6 4.25 7.9 5.6 7.9 7.6C7.9 9.3 9.2 10.4 11.6 11.0"),
    (S, "M15.4 13.6C16 14.3 16.3 15.1 16.3 16C16.3 18.3 14.5 19.75 12 19.75C9.8 19.75 8.2 18.8 7.5 17.1"),
    (S, line((4.5, C), (19.5, C))))
add("editing", "text-size", (S, line((2.75, 19.5), (7.4, 4.5), (12.05, 19.5))), (S, line((4.4, 14.25), (10.4, 14.25))),
    (S, line((15.0, 19.5), (18.0, 10.5), (21.0, 19.5))), (S, line((16.1, 16.25), (19.9, 16.25))))
add("editing", "text-cursor", (S, line((C, 5.5), (C, 18.5))),
    (S, "M9 4.25C10.6 4.25 12 4.75 12 6.25C12 4.75 13.4 4.25 15 4.25"),
    (S, "M9 19.75C10.6 19.75 12 19.25 12 17.75C12 19.25 13.4 19.75 15 19.75"))
TY = (5.25, 9.75, 14.25, 18.75)


def lines(spans):
    return [(S, line((a, y), (b, y))) for y, (a, b) in zip(TY, spans)]


add("editing", "text-align-left", *lines([(4, 20), (4, 14), (4, 20), (4, 14)]))
add("editing", "text-align-center", *lines([(4, 20), (7, 17), (4, 20), (7, 17)]))
add("editing", "text-align-right", *lines([(4, 20), (10, 20), (4, 20), (10, 20)]))
add("editing", "text-justify", *lines([(4, 20), (4, 20), (4, 20), (4, 14)]))
add("editing", "list-bullet", *[(F, dot(5.0, y, 0.55)) for y in (6.0, 12, 18.0)],
    *[(S, line((9.0, y), (20.0, y))) for y in (6.0, 12, 18.0)])
add("editing", "checklist", *[(S, line((3.75, y), (5.4, y + 1.6), (8.4, y - 1.6))) for y in (6.0, 12, 18.0)],
    *[(S, line((11.5, y), (20.25, y))) for y in (6.0, 12, 18.0)])
add("editing", "indent", (S, line((4, 5.25), (20, 5.25))), (S, line((11, 9.75), (20, 9.75))), (S, line((11, 14.25), (20, 14.25))),
    (S, line((4, 18.75), (20, 18.75))), (F, poly((4.25, 9.5), (7.5, 12), (4.25, 14.5))))
add("editing", "outdent", (S, line((4, 5.25), (20, 5.25))), (S, line((11, 9.75), (20, 9.75))), (S, line((11, 14.25), (20, 14.25))),
    (S, line((4, 18.75), (20, 18.75))), (F, poly((7.5, 9.5), (4.25, 12), (7.5, 14.5))))
add("editing", "code", (S, line((7.75, 7.25), (3.25, 12), (7.75, 16.75))), (S, line((16.25, 7.25), (20.75, 12), (16.25, 16.75))),
    (S, line((13.9, 4.5), (10.1, 19.5))))
BR = [pC((C - 10.25, C), (C - 8.0, C - 0.2), (C - 6.25, C - 2.4), (C - 3.5, C - 2.4)), pL((C - 3.5, C - 2.4), (C - 3.5, C + 2.4)),
      pC((C - 3.5, C + 2.4), (C - 6.25, C + 2.4), (C - 8.0, C + 0.2), (C - 10.25, C))]
add("editing", "paintbrush", *E(F, rot_prims(BR, -45)), *E(S, rot_prims(p_rrect(C - 3.5, C - 2.4, 4.0, 4.8, 0.6), -45)),
    *E(S, rot_prims([pL((C + 0.5, C), (C + 10.0, C))], -45)))
ED = [pL((C - 10.0, C), (C - 6.5, C - 1.5), (C + 1.5, C - 1.5)), pL((C + 1.5, C + 1.5), (C - 6.5, C + 1.5), (C - 10.0, C))]
add("editing", "eyedropper", *E(S, rot_prims(ED, -45)), *E(S, rot_prims([pL((C + 1.5, C - 3.4), (C + 1.5, C + 3.4))], -45)),
    *E(S, rot_prims([pL((C + 1.5, C - 2.25), (C + 6.75, C - 2.25)), pA(C + 6.75, C, 2.25, -90, 90),
                     pL((C + 6.75, C + 2.25), (C + 1.5, C + 2.25))], -45)))
add("editing", "crop", (S, line((7.0, 3.75), (7.0, 17.0), (20.25, 17.0))), (S, line((3.75, 7.0), (17.0, 7.0), (17.0, 20.25))))
add("editing", "wand", (S, line((4.25, 19.75), (14.5, 9.5))),
    (S, line((18.75, 3.5), (18.75, 7.5))), (S, line((16.75, 5.5), (20.75, 5.5))),
    (F, dot(13.0, 4.5, 0.5)), (F, dot(19.75, 11.25, 0.5)))
add("editing", "eraser", *E(S, rot_prims(p_rrect(C - 8.0, C - 3.5, 16.0, 7.0, 1.6), -45, (C, 11.6))),
    *E(S, rot_prims([pL((C - 1.5, C - 3.5), (C - 1.5, C + 3.5))], -45, (C, 11.6))), (S, line((14.5, 20.25), (20.25, 20.25))))
SEL = "M3.75 7V6.15A2.4 2.4 0 0 1 6.15 3.75H7"
add("editing", "selection",
    *[(S, d) for d in (SEL, "M17 3.75H17.85A2.4 2.4 0 0 1 20.25 6.15V7", "M20.25 17V17.85A2.4 2.4 0 0 1 17.85 20.25H17",
                       "M7 20.25H6.15A2.4 2.4 0 0 1 3.75 17.85V17")],
    (S, line((10.25, 3.75), (13.75, 3.75))), (S, line((10.25, 20.25), (13.75, 20.25))),
    (S, line((3.75, 10.25), (3.75, 13.75))), (S, line((20.25, 10.25), (20.25, 13.75))))
add("editing", "sort", (S, line((3.75, 6.0), (12.25, 6.0))), (S, line((3.75, 12.0), (10.0, 12.0))), (S, line((3.75, 18.0), (7.75, 18.0))),
    (S, line((17.25, 4.25), (17.25, 19.5))), (S, line((14.0, 16.25), (17.25, 19.5), (20.5, 16.25))))
add("editing", "filter", (S, poly((3.75, 4.75), (20.25, 4.75), (14.0, 12.5), (14.0, 18.25), (10.0, 20.25), (10.0, 12.5))))
add("editing", "return", (S, "M19.5 5.5V11.75A3 3 0 0 1 16.5 14.75H4.75"), (S, line((8.5, 11.0), (4.75, 14.75), (8.5, 18.5))))
add("editing", "delete-left",
    (S, "M20.25 7.65V16.35A2.4 2.4 0 0 1 17.85 18.75H8.5L3.25 12L8.5 5.25H17.85A2.4 2.4 0 0 1 20.25 7.65Z"),
    (S, line((11.75, 9.75), (16.25, 14.25))), (S, line((16.25, 9.75), (11.75, 14.25))))
add("editing", "shift", (S, poly((C, 3.75), (20.25, 12.25), (15.75, 12.25), (15.75, 19.75), (8.25, 19.75), (8.25, 12.25), (3.75, 12.25))))

# Files & Documents (fase 2) ----------------------------------------------------
FOLDER = SYM["folder"][0][1]
DOC = SYM["doc"][0][1]
add("files", "folder-fill", (F, FOLDER))
fpc = fdy + FD_H / 2 - 0.15
add("files", "folder-plus", (S, FOLDER), (S, line((C, fpc - 2.5), (C, fpc + 2.5))), (S, line((C - 2.5, fpc), (C + 2.5, fpc))))
add("files", "doc-fill", (F, DOC))
dfy = 2.75 + DOC_F
add("files", "doc-text", *SYM["doc"], *[(S, line((DOC_X + 3.0, y), (DOC_X + DOC_W - 3.0, y))) for y in (dfy + 3.25, dfy + 6.25, dfy + 9.25)])
add("files", "doc-plus", *SYM["doc"], (S, line((C, 12.5), (C, 17.5))), (S, line((C - 2.5, 15.0), (C + 2.5, 15.0))))
add("files", "archive", (S, rrect(2.75, 4.25, 18.5, 4.5, 1.2)),
    (S, "M4.75 8.75V17.85A2.4 2.4 0 0 0 7.15 20.25H16.85A2.4 2.4 0 0 0 19.25 17.85V8.75"), (S, line((9.75, 12.5), (14.25, 12.5))))
add("files", "tray",
    (S, "M6.6 4.25H17.4L20.25 13V17.85A2.4 2.4 0 0 1 17.85 20.25H6.15A2.4 2.4 0 0 1 3.75 17.85V13Z"),
    (S, line((3.75, 13.0), (8.5, 13.0), (9.75, 15.5), (14.25, 15.5), (15.5, 13.0), (20.25, 13.0))))
add("files", "paperclip", (S, "M10.5 8.5V15A1.5 1.5 0 0 0 13.5 15V6.75A2.5 2.5 0 0 0 8.5 6.75V15.75A3.5 3.5 0 0 0 15.5 15.75V7.75"))
BM = "M6.57 20.75V5.15A2.4 2.4 0 0 1 8.97 2.75H15.03A2.4 2.4 0 0 1 17.43 5.15V20.75L12 16.6Z"
add("files", "bookmark", (S, BM))
add("files", "bookmark-fill", (F, BM))
add("files", "tag", (S, "M3.25 12L8.6 5.25H18.85A2.4 2.4 0 0 1 21.25 7.65V16.35A2.4 2.4 0 0 1 18.85 18.75H8.6Z"), (F, dot(9.0, C, 0.6)))
add("files", "photo", (S, rrect(*WN, 2.4)), (S, circle(15.75, 8.75, 1.6)),
    (S, line((2.75, 17.0), (8.5, 11.25), (13.25, 16.0))), (S, line((11.6, 14.35), (15.5, 13.25), (21.25, 17.0))))
add("files", "film", (S, rrect(*WN, 2.4)), (S, line((6.75, 4.25), (6.75, 19.75))), (S, line((17.25, 4.25), (17.25, 19.75))),
    (S, line((6.75, C), (17.25, C))),
    *[(S, line((a, y), (b, y))) for y in (8.25, 15.75) for a, b in ((2.75, 6.75), (17.25, 21.25))])
add("files", "book", (S, "M12 6.25C10 4.75 7 4.25 3.75 4.5V18.25C7 18 10 18.5 12 20C14 18.5 17 18 20.25 18.25V4.5C17 4.25 14 4.75 12 6.25Z"),
    (S, line((C, 6.25), (C, 20.0))))
CL = cloud_prims(1.0, -0.15, 0.3)
add("files", "cloud-upload", *E(S, CL), (S, line((C, 15.25), (C, 9.75))), (S, line((9.6, 12.15), (C, 9.75), (14.4, 12.15))))
add("files", "cloud-download", *E(S, CL), (S, line((C, 9.5), (C, 15.0))), (S, line((9.6, 12.6), (C, 15.0), (14.4, 12.6))))
add("files", "trash-fill", (S, line((3.6, 6.4), (20.4, 6.4))),
    (S, "M9.1 6.4V5.2A1.7 1.7 0 0 1 10.8 3.5H13.2A1.7 1.7 0 0 1 14.9 5.2V6.4"),
    (F, "M5.6 6.4L6.6 18.9A2.1 2.1 0 0 0 8.7 20.8H15.3A2.1 2.1 0 0 0 17.4 18.9L18.4 6.4Z"))
add("files", "history", (S, arc(C, C, RA, 210, 520)), (S, arc_head(C, C, RA, 210, cw=False)),
    (S, line((C, 7.5), (C, C), (15.0, 14.0))))
add("files", "terminal", (S, rrect(*WN, 2.4)), (S, line((6.75, 9.0), (9.75, 12.0), (6.75, 15.0))), (S, line((11.75, 15.0), (16.75, 15.0))))
add("files", "chart-bar", (S, rrect(3.75, 12.25, 3.5, 8.0, 1.0)), (S, rrect(10.25, 3.75, 3.5, 16.5, 1.0)), (S, rrect(16.75, 8.75, 3.5, 11.5, 1.0)))
add("files", "chart-pie", (S, circle(C, C, 9.25)), (S, line((C, 2.75), (C, C), (C + 6.54, C + 6.54))))

# Communication (fase 2) ----------------------------------------------------------
BELL = "M12 3.4A6.1 6.1 0 0 0 5.9 9.5V14.6L4.1 17.1H19.9L18.1 14.6V9.5A6.1 6.1 0 0 0 12 3.4Z"
BELL_P = [pA(C, 9.5, 6.1, 180, 360), pL((18.1, 9.5), (18.1, 14.6), (19.9, 17.1), (4.1, 17.1), (5.9, 14.6), (5.9, 9.5))]
add("communication", "bell-fill", (F, BELL), (S, "M9.6 19.9A2.5 2.5 0 0 0 14.4 19.9"))
add("communication", "bell-slash", *E(S, slashed(BELL_P + [pA(C, 19.2, 2.5, 16.26, 163.74)])), (S, line(*SLASH)))
BADGE = (18.5, 5.0, 2.6)
add("communication", "bell-badge",
    *E(S, cut(BELL_P, lambda x, y: math.dist((x, y), BADGE[:2]) >= BADGE[2] + 1.5 + 0.75)),
    (S, "M9.6 19.9A2.5 2.5 0 0 0 14.4 19.9"), (FO, circle(*BADGE)))
add("communication", "envelope", (S, rrect(2.75, 5.25, 18.5, 13.5, 2.4)), (S, line((3.75, 6.75), (C, 12.75), (20.25, 6.75))))
add("communication", "envelope-open",
    (S, "M2.75 10L12 3.75L21.25 10V17.85A2.4 2.4 0 0 1 18.85 20.25H5.15A2.4 2.4 0 0 1 2.75 17.85Z"),
    (S, line((3.5, 10.6), (C, 16.0), (20.5, 10.6))))
MSG = "M6.15 3.75H17.85A3.4 3.4 0 0 1 21.25 7.15V13.85A3.4 3.4 0 0 1 17.85 17.25H11L6.75 20.75V17.25H6.15A3.4 3.4 0 0 1 2.75 13.85V7.15A3.4 3.4 0 0 1 6.15 3.75Z"
add("communication", "message", (S, MSG))
add("communication", "message-fill", (F, MSG))
add("communication", "message-2",
    (S, "M5.15 8.75H13.35A2.4 2.4 0 0 1 15.75 11.15V15.85A2.4 2.4 0 0 1 13.35 18.25H9L5.75 20.75V18.25H5.15A2.4 2.4 0 0 1 2.75 15.85V11.15A2.4 2.4 0 0 1 5.15 8.75Z"),
    (S, "M7.25 8.75V5.65A2.4 2.4 0 0 1 9.65 3.25H18.85A2.4 2.4 0 0 1 21.25 5.65V11.35A2.4 2.4 0 0 1 18.85 13.75H15.75"))
add("communication", "message-ellipsis", (S, MSG), *[(F, dot(x, 10.5, 0.5)) for x in (7.9, 12, 16.1)])
PHONE = ("M8.6 3.6L10.3 7.4C10.6 8.1 10.4 8.9 9.8 9.4L8.6 10.4C9.7 12.7 11.3 14.3 13.6 15.4L14.6 14.2C15.1 13.6 15.9 13.4 16.6 13.7"
         "L20.4 15.4C20.9 15.7 21.2 16.2 21.1 16.8L20.7 18.9C20.5 19.9 19.6 20.6 18.6 20.5C10.4 20 4 13.6 3.5 5.4C3.4 4.4 4.1 3.5 5.1 3.3"
         "L7.2 2.9C7.8 2.8 8.3 3.1 8.6 3.6Z")
add("communication", "phone", (S, PHONE))
add("communication", "phone-fill", (F, PHONE))
add("communication", "phone-down", (S, "M3 14.2C3 12.5 3.6 10.9 5.2 10C9.4 7.7 14.6 7.7 18.8 10C20.4 10.9 21 12.5 21 14.2V15C21 15.7 20.4 16.2 19.7 16.1"
                                        "L16.6 15.6C16 15.5 15.5 15 15.5 14.4V12.5C13.2 11.8 10.8 11.8 8.5 12.5V14.4C8.5 15 8 15.5 7.4 15.6"
                                        "L4.3 16.1C3.6 16.2 3 15.7 3 15Z"))
VID_B = p_rrect(2.75, 6.25, 12.5, 11.5, 2.4)
VID_L = [pL((15.25, 10.25), (21.25, 6.9), (21.25, 17.1), (15.25, 13.75))]
add("communication", "video", *E(S, VID_B), *E(S, VID_L))
add("communication", "video-fill", (F, rrect(2.75, 6.25, 12.5, 11.5, 2.4)), (F, poly((15.25, 10.25), (21.25, 6.9), (21.25, 17.1), (15.25, 13.75))))
add("communication", "video-slash", *E(S, slashed(VID_B + VID_L)), (S, line(*SLASH)))
PP = [(3.25, 3.75), (21.0, C), (3.25, 20.25), (6.5, C)]
add("communication", "paperplane", (S, poly(*PP)), (S, line((6.5, C), (13.0, C))))
add("communication", "paperplane-fill", (F, poly(*PP)))
add("communication", "at", (S, circle(C, C, 3.75)),
    (S, f"M15.75 12V13.5A2.5 2.5 0 0 0 20.75 13.5V12A8.75 8.75 0 1 0 {P(C + 8.75 * math.cos(math.radians(50)), C + 8.75 * math.sin(math.radians(50)))}"))
add("communication", "megaphone", (S, poly((3.75, 10.0), (7.25, 10.0), (17.0, 5.0), (17.0, 19.0), (7.25, 14.0), (3.75, 14.0))),
    (S, line((7.0, 14.0), (8.5, 19.25))), (S, line((20.25, 9.75), (20.25, 14.25))))
add("communication", "reply", (S, "M3.75 10.75H12.5A7.5 7.5 0 0 1 20 18.25"), (S, line((8.25, 6.25), (3.75, 10.75), (8.25, 15.25))))
add("communication", "reply-all", (S, "M8.25 10.75H13A7 7 0 0 1 20 17.75"), (S, line((12.25, 6.75), (8.25, 10.75), (12.25, 14.75))),
    (S, line((7.25, 6.75), (3.25, 10.75), (7.25, 14.75))))
add("communication", "voicemail", (S, circle(6.75, C, 3.5)), (S, circle(17.25, C, 3.5)), (S, line((6.75, 15.5), (17.25, 15.5))))
add("communication", "feed", (F, dot(6.0, 18.0, 1.0)), (S, arc(4.5, 19.5, 8.0, -90, 0)), (S, arc(4.5, 19.5, 15.0, -90, 0)))

# People & Security (fase 2) --------------------------------------------------
HEAD_R = 10 / PHI ** 2 + 0.2
BODY = "M4.6 20.6C4.6 16.6 7.9 13.9 12 13.9C16.1 13.9 19.4 16.6 19.4 20.6Z"
add("people", "person-fill", (F, circle(C, 7.8, HEAD_R)), (F, BODY))
add("people", "person-2", (S, circle(8.75, 8.25, 3.07)), (S, "M2.75 20.25C2.75 16.6 5.4 14.25 8.75 14.25C12.1 14.25 14.75 16.6 14.75 20.25Z"),
    (S, circle(17.25, 7.25, 2.6)), (S, "M16.0 12.9C16.4 12.8 16.8 12.75 17.25 12.75C19.6 12.75 21.25 14.6 21.25 17.25"))
add("people", "person-plus", (S, circle(9.5, 7.8, 3.07)), (S, "M2.75 20.25C2.75 16.4 5.7 13.9 9.5 13.9C13.3 13.9 16.25 16.4 16.25 20.25Z"),
    (S, line((18.5, 7.0), (18.5, 12.0))), (S, line((16.0, 9.5), (21.0, 9.5))))
add("people", "person-circle", (S, circle(C, C, 9.25)), (S, circle(C, 9.5, 2.9)),
    (S, "M5.9 18.6C7.1 16.4 9.4 15 12 15C14.6 15 16.9 16.4 18.1 18.6"))
add("people", "contact-card", (S, rrect(*WN, 2.4)), (S, circle(8.5, 10.25, 2.0)),
    (S, "M5.5 16C5.8 14.4 7 13.5 8.5 13.5C10 13.5 11.2 14.4 11.5 16"), (S, line((14.25, 10.0), (18.0, 10.0))), (S, line((14.25, 13.5), (18.0, 13.5))))
add("people", "lock-fill", (F, rrect(C - LK_W / 2, lky, LK_W, LK_H, 2.4)), (S, f"M8.2 {f(lky)}V7.4A3.8 3.8 0 0 1 15.8 7.4V{f(lky)}"))
add("people", "key", (S, circle(7.5, C, 4.25)), (F, dot(6.25, C, 0.6)), (S, line((11.75, C), (20.75, C), (20.75, 14.75))),
    (S, line((17.5, C), (17.5, 15.25))))
SHIELD = "M12 2.75L19.75 5.5V11.5C19.75 16 16.6 19.4 12 21.25C7.4 19.4 4.25 16 4.25 11.5V5.5Z"
add("people", "shield", (S, SHIELD))
add("people", "shield-check", (S, SHIELD), (S, line((8.6, 12.0), (11.0, 14.4), (15.6, 9.4))))
EYE = [pC((2.75, C), (5, 7.5), (8.25, 5.25), (C, 5.25)), pC((C, 5.25), (15.75, 5.25), (19, 7.5), (21.25, C)),
       pC((21.25, C), (19, 16.5), (15.75, 18.75), (C, 18.75)), pC((C, 18.75), (8.25, 18.75), (5, 16.5), (2.75, C))]
add("people", "eye", *E(S, EYE), (S, circle(C, C, 3.07)))
add("people", "eye-slash", *E(S, slashed(EYE + p_circle(C, C, 3.07))), (S, line(*SLASH)))
FPC = (C, 12.5)
add("people", "fingerprint",
    (S, arc(*FPC, 8.4, 195, 345)), (S, arc(*FPC, 5.4, 180, 360)), (S, arc(*FPC, 2.4, 180, 360)),
    (S, line((6.6, 12.5), (6.6, 17.5))), (S, line((17.4, 12.5), (17.4, 15.0))),
    (S, line((9.6, 12.5), (9.6, 20.25))), (S, line((14.4, 12.5), (14.4, 18.75))), (S, line((C, 12.5), (C, 16.5))))
add("people", "password", (S, rrect(2.75, 7.25, 18.5, 9.5, 4.75)), *[(F, dot(x, C, 0.7)) for x in (7.75, 12, 16.25)])
add("people", "smiley", (S, circle(C, C, 9.25)), (F, dot(8.75, 9.5, 0.7)), (F, dot(15.25, 9.5, 0.7)), (S, arc(C, C, 5.0, 30, 150)))
add("people", "accessibility", (S, circle(C, C, 9.25)), (F, dot(C, 6.9, 0.9)),
    (S, line((7.25, 9.5), (C, 10.5), (16.75, 9.5))), (S, line((C, 10.5), (C, 13.75))),
    (S, line((9.25, 17.75), (C, 13.75), (14.75, 17.75))))
add("people", "logout", (S, "M10.5 3.75H6.15A2.4 2.4 0 0 0 3.75 6.15V17.85A2.4 2.4 0 0 0 6.15 20.25H10.5"),
    *arrow((9.25, C), (20.25, C), 5.3))
add("people", "login", (S, "M13.5 3.75H17.85A2.4 2.4 0 0 1 20.25 6.15V17.85A2.4 2.4 0 0 1 17.85 20.25H13.5"),
    *arrow((3.75, C), (14.75, C), 5.3))

# Devices (fase 2) ----------------------------------------------------------------
add("devices", "laptop", (S, rrect(4.25, 4.75, 15.5, 10.5, 2.0)), (S, line((2.75, 18.75), (21.25, 18.75))))
DSP = (2.75, 3.75, 18.5, 12.5)
add("devices", "display", (S, rrect(*DSP, 2.4)), (S, line((C, 16.25), (C, 20.25))), (S, line((8.25, 20.25), (15.75, 20.25))))
add("devices", "display-2", (S, rrect(2.75, 7.25, 13.5, 9.25, 2.0)),
    (S, "M7.25 7.25V5.75A2 2 0 0 1 9.25 3.75H19.25A2 2 0 0 1 21.25 5.75V11.25A2 2 0 0 1 19.25 13.25H16.25"),
    (S, line((9.5, 16.5), (9.5, 20.25))), (S, line((6.25, 20.25), (12.75, 20.25))))
add("devices", "smartphone", (S, rrect(6.57, 2.75, 10.86, 18.5, 2.8)), (S, line((10.75, 5.75), (13.25, 5.75))))
add("devices", "tablet", (S, rrect(3.75, 2.75, 16.5, 18.5, 2.4)), (F, dot(C, 18.25, 0.45)))
add("devices", "smartwatch", (S, rrect(6.25, 6.25, 11.5, 11.5, 3.0)),
    (S, line((8.75, 6.25), (9.25, 3.25), (14.75, 3.25), (15.25, 6.25))), (S, line((8.75, 17.75), (9.25, 20.75), (14.75, 20.75), (15.25, 17.75))))
add("devices", "mouse", (S, rrect(6.57, 2.75, 10.86, 18.5, 5.43)), (S, line((C, 6.25), (C, 9.25))))
add("devices", "printer",
    (S, "M7.25 16.5H5.15A2.4 2.4 0 0 1 2.75 14.1V10.15A2.4 2.4 0 0 1 5.15 7.75H18.85A2.4 2.4 0 0 1 21.25 10.15V14.1A2.4 2.4 0 0 1 18.85 16.5H16.75"),
    (S, line((7.25, 7.75), (7.25, 3.75), (16.75, 3.75), (16.75, 7.75))), (S, poly((7.25, 13.25), (16.75, 13.25), (16.75, 20.25), (7.25, 20.25))),
    (F, dot(17.75, 10.6, 0.55)))
add("devices", "camera",
    (S, "M5.15 6.25H8L9.5 4.25H14.5L16 6.25H18.85A2.4 2.4 0 0 1 21.25 8.65V17.35A2.4 2.4 0 0 1 18.85 19.75H5.15A2.4 2.4 0 0 1 2.75 17.35V8.65A2.4 2.4 0 0 1 5.15 6.25Z"),
    (S, circle(C, 12.85, 3.6)))
add("devices", "headphones", (S, arc(C, 12.75, 8.5, 180, 360)),
    (S, rrect(3.5, 12.5, 4.5, 7.75, 1.6)), (S, rrect(16.0, 12.5, 4.5, 7.75, 1.6)))
add("devices", "speaker", (S, rrect(5.25, 2.75, 13.5, 18.5, 2.4)), (S, circle(C, 14.5, 3.5)), (F, dot(C, 7.0, 0.75)))
add("devices", "gamecontroller",
    (S, "M7.5 6.75H16.5C19.2 6.75 20.6 8.6 21 11.4L21.6 15.4C21.9 17.6 19.7 19.1 17.9 17.6L15.9 15.75H8.1L6.1 17.6C4.3 19.1 2.1 17.6 2.4 15.4L3 11.4C3.4 8.6 4.8 6.75 7.5 6.75Z"),
    (S, line((7.75, 9.25), (7.75, 13.25))), (S, line((5.75, 11.25), (9.75, 11.25))), (F, dot(15.5, 10.0, 0.5)), (F, dot(17.5, 12.25, 0.5)))
add("devices", "drive", (S, rrect(2.75, 7.25, 18.5, 9.5, 2.4)), (F, dot(17.0, C, 0.6)), (S, line((6.25, C), (11.75, C))))
add("devices", "usb-drive", (S, rrect(6.75, 9.25, 10.5, 11.5, 2.4)), (S, line((9.0, 9.25), (9.0, 3.25), (15.0, 3.25), (15.0, 9.25))),
    (F, dot(10.9, 6.0, 0.45)), (F, dot(13.1, 6.0, 0.45)))
add("devices", "sd-card", (S, "M9.25 2.75H16.85A2.4 2.4 0 0 1 19.25 5.15V18.85A2.4 2.4 0 0 1 16.85 21.25H7.15A2.4 2.4 0 0 1 4.75 18.85V7.25Z"),
    *[(S, line((x, 6.0), (x, 8.5))) for x in (10.0, 13.0, 16.0)])
add("devices", "cpu", (S, rrect(6.25, 6.25, 11.5, 11.5, 2.0)), (S, rrect(9.25, 9.25, 5.5, 5.5, 1.0)),
    *[(S, line(a, b)) for v in (9.75, 14.25) for a, b in (((v, 3.0), (v, 6.25)), ((v, 17.75), (v, 21.0)), ((3.0, v), (6.25, v)), ((17.75, v), (21.0, v)))])
add("devices", "server", (S, rrect(2.75, 4.25, 18.5, 6.25, 2.0)), (S, rrect(2.75, 13.5, 18.5, 6.25, 2.0)),
    (F, dot(6.5, 7.375, 0.6)), (F, dot(6.5, 16.625, 0.6)), (S, line((13.0, 7.375), (17.75, 7.375))), (S, line((13.0, 16.625), (17.75, 16.625))))
add("devices", "tv", (S, rrect(2.75, 4.25, 18.5, 12.5, 2.4)), (S, line((7.5, 19.75), (16.5, 19.75))))
add("devices", "router", (S, rrect(2.75, 12.75, 18.5, 7.0, 2.0)), (S, line((6.75, 12.75), (5.5, 4.25))), (S, line((17.25, 12.75), (18.5, 4.25))),
    (F, dot(7.0, 16.25, 0.6)), (F, dot(10.25, 16.25, 0.6)))
add("devices", "disc", (S, circle(C, C, 9.25)), (S, circle(C, C, 2.4)))
add("devices", "webcam", (S, circle(C, 9.0, 6.25)), (S, circle(C, 9.0, 2.4)), (S, line((C, 15.25), (C, 20.25))), (S, line((7.75, 20.25), (16.25, 20.25))))

# Weather & Time (fase 2) ---------------------------------------------------------
CLW = cloud_prims(1.0, -0.15, 0.3)
add("weather", "cloud", *E(S, CLW))
add("weather", "cloud-fill", *E(F, CLW))
CLS = cloud_prims(0.84, -0.15, -3.0)
add("weather", "cloud-rain", *E(S, CLS), *[(S, line((x, 16.75), (x - 1.25, 20.25))) for x in (8.5, 12.75, 17.0)])
add("weather", "cloud-snow", *E(S, CLS), *[(F, dot(x, y, 0.4)) for x, y in ((8.0, 17.5), (12.0, 17.5), (16.0, 17.5), (10.0, 20.6), (14.0, 20.6))], )
BOLT_S = [(C + (x - C) * 0.5 - 0.3, 16.5 + (y - C) * 0.5) for x, y in BOLT]
add("weather", "cloud-bolt", *E(S, cut(CLS, outside_shape([pL(*BOLT_S, BOLT_S[0])], CUT))), (F, poly(*BOLT_S)))


def sun_prims(cx, cy, rc, r0, r1, n=8, start=-90):
    pr = p_circle(cx, cy, rc)
    for i in range(n):
        a = math.radians(start + i * 360 / n)
        pr.append(pL((cx + r0 * math.cos(a), cy + r0 * math.sin(a)), (cx + r1 * math.cos(a), cy + r1 * math.sin(a))))
    return pr


CLR = cloud_prims(0.78, 2.4, 3.1)
add("weather", "cloud-sun", *E(S, cut(sun_prims(9.5, 9.9, 2.4, 5.4, 6.75), outside_shape(CLR))), *E(S, CLR))
add("weather", "cloud-moon", *E(S, cut(crescent_prims(9.0, 9.0, 5.75, (13.2, 4.8), 4.4), outside_shape(CLR))), *E(S, CLR))
add("weather", "cloud-fog", *E(S, CLS), (S, line((4.75, 17.0), (19.25, 17.0))), (S, line((7.25, 20.5), (16.75, 20.5))))
add("weather", "wind", (S, "M3.75 10H13.5A2.75 2.75 0 1 0 10.75 7.25"), (S, "M3.75 14H17.5A2.75 2.75 0 1 1 14.75 16.75"),
    (S, line((3.75, 18.0), (10.5, 18.0))))
SNOW = []
for k in range(3):
    a = math.radians(90 + 60 * k)
    ux, uy = math.cos(a), math.sin(a)
    SNOW.append((S, line((C - 9.0 * ux, C - 9.0 * uy), (C + 9.0 * ux, C + 9.0 * uy))))
    for sgn in (1, -1):
        bx, by = C + sgn * 5.6 * ux, C + sgn * 5.6 * uy
        px, py = -uy, ux
        SNOW.append((S, line((bx + sgn * 2.4 * ux + 2.4 * px, by + sgn * 2.4 * uy + 2.4 * py), (bx, by),
                             (bx + sgn * 2.4 * ux - 2.4 * px, by + sgn * 2.4 * uy - 2.4 * py))))
add("weather", "snowflake", *SNOW)
add("weather", "drop", (S, "M12 3C12 3 5.75 9.75 5.75 14.25A6.25 6.25 0 0 0 18.25 14.25C18.25 9.75 12 3 12 3Z"))
UMB_Y = 11.75
add("weather", "umbrella", (S, f"M3.25 {f(UMB_Y)}A8.75 8.75 0 0 1 20.75 {f(UMB_Y)}" +
                            "".join(f"A2.92 2.92 0 0 0 {P(20.75 - 5.833 * (i + 1), UMB_Y)}" for i in range(3))),
    (S, f"M12 {f(UMB_Y)}V18.25A1.75 1.75 0 0 1 8.5 18.25"))
TB = 4.0
TBY = 17.25 - math.sqrt(TB ** 2 - 4)
add("weather", "thermometer", (S, f"M10 {f(TBY)}V5.25A2 2 0 0 1 14 5.25V{f(TBY)}A{f(TB)} {f(TB)} 0 1 1 10 {f(TBY)}Z"), (F, dot(C, 17.25, 1.0)))
add("weather", "sunrise", (S, line((3.0, 19.25), (21.0, 19.25))), (S, arc(C, 19.25, 4.5, 180, 360)),
    (S, line((C, 11.5), (C, 4.0))), (S, line((9.25, 6.75), (C, 4.0), (14.75, 6.75))),
    *[(S, line((C + 7.25 * math.cos(math.radians(a)), 19.25 + 7.25 * math.sin(math.radians(a))),
               (C + 9.25 * math.cos(math.radians(a)), 19.25 + 9.25 * math.sin(math.radians(a))))) for a in (-150, -30)])
add("weather", "sunset", (S, line((3.0, 19.25), (21.0, 19.25))), (S, arc(C, 19.25, 4.5, 180, 360)),
    (S, line((C, 4.0), (C, 11.5))), (S, line((9.25, 8.75), (C, 11.5), (14.75, 8.75))),
    *[(S, line((C + 7.25 * math.cos(math.radians(a)), 19.25 + 7.25 * math.sin(math.radians(a))),
               (C + 9.25 * math.cos(math.radians(a)), 19.25 + 9.25 * math.sin(math.radians(a))))) for a in (-150, -30)])
add("weather", "calendar", (S, rrect(3.75, 4.75, 16.5, 15.5, 2.4)), (S, line((3.75, 9.25), (20.25, 9.25))),
    (S, line((8.25, 3.0), (8.25, 6.25))), (S, line((15.75, 3.0), (15.75, 6.25))),
    *[(F, dot(x, y, 0.55)) for y in (13.0, 16.5) for x in (8.25, 12, 15.75)])
add("weather", "alarm", (S, circle(C, 12.75, 7.5)), (S, line((C, 8.75), (C, 12.75), (14.5, 14.25))),
    (S, line((3.5, 6.0), (6.0, 3.5))), (S, line((20.5, 6.0), (18.0, 3.5))),
    (S, line((7.7, 18.9), (6.25, 20.75))), (S, line((16.3, 18.9), (17.75, 20.75))))
add("weather", "timer", (S, arc(C, C, 9.25, -90, 210)), (S, line((C, 2.75), (C, 6.25))), (F, dot(C, C, 0.9)), (S, line((C, C), (8.25, 8.25))))
add("weather", "stopwatch", (S, circle(C, 13.25, 7.75)), (S, line((C, 5.5), (C, 2.75))), (S, line((9.75, 2.75), (14.25, 2.75))),
    (S, line((C, 13.25), (C, 9.0))), (S, line((18.0, 6.25), (19.25, 7.5))))
add("weather", "hourglass", (S, line((6.25, 3.25), (17.75, 3.25))), (S, line((6.25, 20.75), (17.75, 20.75))),
    (S, "M7.5 3.25V5.75C7.5 8.25 12 10 12 12C12 14 7.5 15.75 7.5 18.25V20.75"),
    (S, "M16.5 3.25V5.75C16.5 8.25 12 10 12 12C12 14 16.5 15.75 16.5 18.25V20.75"))


def sparkle(cx, cy, r, k=0.16):
    q = r * k
    return (f"M{P(cx, cy - r)}Q{P(cx + q, cy - q)} {P(cx + r, cy)}Q{P(cx + q, cy + q)} {P(cx, cy + r)}"
            f"Q{P(cx - q, cy + q)} {P(cx - r, cy)}Q{P(cx - q, cy - q)} {P(cx, cy - r)}Z")


add("weather", "moon-stars", *E(S, crescent_prims(10.5, 13.25, 7.6, (16.6, 7.4), 5.6)), (F, sparkle(18.0, 5.5, 2.5)), (F, dot(20.25, 11.5, 0.55)))

# Shapes & Indicators (fase 2) -----------------------------------------------------
add("shapes", "circle", (S, circle(C, C, 9.25)))
add("shapes", "circle-fill", (F, circle(C, C, 9.25)))
add("shapes", "square", (S, rrect(3.75, 3.75, 16.5, 16.5, 3.0)))
add("shapes", "square-fill", (F, rrect(3.75, 3.75, 16.5, 16.5, 3.0)))
add("shapes", "triangle", (S, SYM["warning"][0][1]))
add("shapes", "diamond", (S, poly((C, 2.75), (21.25, C), (C, 21.25), (2.75, C))))
add("shapes", "star-fill", (F, poly(*star)))
add("shapes", "heart-fill", (F, SYM["heart"][0][1]))
add("shapes", "checkmark-circle", (S, circle(C, C, 9.25)), (S, line((7.75, 12.25), (10.75, 15.25), (16.25, 9.0))))
add("shapes", "plus-circle", (S, circle(C, C, 9.25)), (S, line((C, C - 4.4), (C, C + 4.4))), (S, line((C - 4.4, C), (C + 4.4, C))))
add("shapes", "question", (S, circle(C, C, 9.25)), (S, "M9.4 9.6A2.7 2.7 0 1 1 13.4 12C12.5 12.5 12 13 12 14V14.4"), (F, dot(C, 17.2, 0.55)))
add("shapes", "checkmark-square", (S, rrect(3.75, 3.75, 16.5, 16.5, 2.4)), (S, line((7.75, 12.25), (10.75, 15.25), (16.25, 9.0))))
add("shapes", "circle-dot", (S, circle(C, C, 9.25)), (F, circle(C, C, 3.07)))
FLAG = [(5.25, 4.25), (18.25, 4.25), (15.75, 8.75), (18.25, 13.25), (5.25, 13.25)]
add("shapes", "flag", (S, line((5.25, 3.25), (5.25, 20.75))), (S, line(*FLAG)))
add("shapes", "flag-fill", (S, line((5.25, 3.25), (5.25, 20.75))), (F, poly(*FLAG)))
add("shapes", "pin", (S, line((8.25, 3.25), (15.75, 3.25))), (S, line((9.25, 3.25), (9.25, 8.75), (6.75, 12.75), (17.25, 12.75), (14.75, 8.75), (14.75, 3.25))),
    (S, line((C, 12.75), (C, 20.75))))
add("shapes", "sparkles", (F, sparkle(10.0, 13.5, 7.25)), (F, sparkle(18.0, 5.5, 3.0)))
add("shapes", "lightbulb", (S, "M9 18V15C9 13.6 6.25 12 6.25 8.5A5.75 5.75 0 0 1 17.75 8.5C17.75 12 15 13.6 15 15V18Z"),
    (S, line((10.0, 21.0), (14.0, 21.0))))
add("shapes", "scope", (S, circle(C, C, 7.25)), (S, line((C, 2.75), (C, 8.25))), (S, line((C, 15.75), (C, 21.25))),
    (S, line((2.75, C), (8.25, C))), (S, line((15.75, C), (21.25, C))), (F, dot(C, C, 0.6)))
add("shapes", "number", (S, line((10.0, 3.75), (8.5, 20.25))), (S, line((15.5, 3.75), (14.0, 20.25))),
    (S, line((4.75, 9.0), (19.75, 9.0))), (S, line((4.25, 15.0), (19.25, 15.0))))
add("shapes", "progress", (S + "2", arc(C, C, 9.25, -90 + 360 / PHI ** 2, 270)), (S, arc(C, C, 9.25, -90, -90 + 360 / PHI ** 2)))
SEAL = []
for i in range(16):
    r = 9.25 if i % 2 == 0 else 7.9
    a = math.radians(-90 + i * 22.5)
    SEAL.append((C + r * math.cos(a), C + r * math.sin(a)))
add("shapes", "seal-check", (S, poly(*SEAL)), (S, line((8.4, 12.2), (10.9, 14.7), (15.6, 9.6))))

# Settings (fase 2) ---------------------------------------------------------------
add("settings", "sliders", *[(S, line((3.75, y), (20.25, y))) for y in (6.0, 12.0, 18.0)],
    *[(F, circle(x, y, 1.75)) for x, y in ((15.0, 6.0), (8.0, 12.0), (13.5, 18.0))])
SW_R = (2.75, 6.25, 18.5, 11.5, 5.75)
add("settings", "switch", (S, rrect(*SW_R)), (S, circle(8.5, C, 2.75)))
add("settings", "switch-on", (S, rrect(*SW_R)), (F, circle(15.5, C, 2.75)))
add("settings", "wrench", (S, arc(15.75, 8.25, 4.5, -10, 280)), (S, line((16.53, 3.82), (15.0, 7.0), (17.0, 9.0), (20.18, 7.47))),
    (S, line((12.57, 11.43), (4.5, 19.5))))
add("settings", "restart", (S, arc(C, 12.5, 8.25, -60, 240)), (S, arc_head(C, 12.5, 8.25, -60, cw=False, leg=4.0)), (S, line((C, 8.0), (C, 13.0))))
add("settings", "gauge", (S, arc(C, 14.25, 9.0, 150, 390)), (S, line((C, 14.25), (16.0, 10.25))), (F, dot(C, 14.25, 1.0)))
add("settings", "leaf", (S, "M4.75 19.25C4.75 10 9.5 4.75 19.25 4.75C19.25 14.5 14 19.25 4.75 19.25Z"), (S, line((4.75, 19.25), (13.5, 10.5))))
add("settings", "palette",
    (S, "M12 2.75A9.25 9.25 0 0 0 12 21.25C13.2 21.25 13.8 20.5 13.8 19.5C13.8 18.4 13 17.9 13 16.9C13 15.8 13.8 15.25 15 15.25H17A4.25 4.25 0 0 0 21.25 11C21.25 6.4 17.1 2.75 12 2.75Z"),
    *[(F, dot(x, y, 0.85)) for x, y in ((7.25, 12.5), (8.5, 8.0), (12.75, 6.5), (16.75, 8.5))])
add("settings", "puzzle", (S, "M3.75 7.25H8.25A2.25 2.25 0 1 1 12.25 7.25H16.75V11.75A2.25 2.25 0 1 1 16.75 15.75V20.25H3.75Z"))
add("settings", "cube", (S, poly((C, 2.75), (20.0, 7.25), (20.0, 16.75), (C, 21.25), (4.0, 16.75), (4.0, 7.25))),
    (S, line((4.0, 7.25), (C, 11.75), (20.0, 7.25))), (S, line((C, 11.75), (C, 21.25))))
add("settings", "zoom-out", (S, circle(10.2, 10.2, GLASS_R)),
    (S, line((10.2 + GLASS_R * 0.7071, 10.2 + GLASS_R * 0.7071), (20.25, 20.25))), (S, line((7.4, 10.2), (13.0, 10.2))))
add("settings", "arrow-down-circle", (S, circle(C, C, 9.25)), (S, line((C, 7.0), (C, 16.75))), (S, line((8.0, 12.75), (C, 16.75), (16.0, 12.75))))
add("settings", "bug", (S, rrect(7.5, 7.25, 9.0, 12.5, 4.5)), (S, arc(C, 7.25, 3.0, 180, 360)), (S, line((C, 11.75), (C, 19.75))),
    *[(S, line(a, b)) for a, b in (((7.5, 11.75), (4.0, 10.25)), ((16.5, 11.75), (20.0, 10.25)), ((7.5, 15.75), (4.0, 17.25)), ((16.5, 15.75), (20.0, 17.25)))])
add("settings", "pointer", (S, poly((6.0, 3.25), (6.0, 18.5), (9.9, 14.9), (12.5, 20.6), (15.1, 19.4), (12.5, 13.8), (17.75, 13.5))))

CATS = [
    ("status", "Status & Connectivity"),
    ("control", "Control Center & Media"),
    ("windows", "Windows & Navigation"),
    ("editing", "Editing & Text"),
    ("files", "Files & Documents"),
    ("communication", "Communication"),
    ("people", "People & Security"),
    ("devices", "Devices"),
    ("weather", "Weather & Time"),
    ("shapes", "Shapes & Indicators"),
    ("settings", "Settings"),
]


def svg(name, sw=SW, color="#000", size=24, sec=0.35):
    out = []
    for mode, d in SYM[name]:
        op = f" opacity='{sec}'" if mode.endswith("2") else ""
        m = mode[0]
        if m == "s":
            out.append(f"<path d='{d}'{op}/>")
        elif m == "f":
            out.append(f"<path d='{d}' fill='{color}'{op}/>")
        else:
            out.append(f"<path d='{d}' fill='{color}' stroke='none'{op}/>")
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{size}' height='{size}' viewBox='0 0 24 24'>"
            f"<g fill='none' stroke='{color}' stroke-width='{f(sw)}' stroke-linecap='round' stroke-linejoin='round'>"
            + "".join(out) + "</g></svg>")
