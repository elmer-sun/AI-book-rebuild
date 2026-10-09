# -*- coding: utf-8 -*-
"""Redraw Ziman, Principles of the Theory of Solids (2nd ed.), Chapter 4
figures 67-75 as black-and-white vector graphics (matplotlib).

Book page / PDF-page mapping (PDF page = book page + 14):
  Fig. 67  p.119  (p133)   (a)+(b)
  Fig. 68  p.121  (p135)
  Fig. 69  p.121  (p135)   (a)+(b)
  Fig. 70  p.122  (p136)
  Fig. 71  p.123  (p137)   (a)+(b)
  Fig. 72  p.124  (p138)
  Fig. 73  p.125  (p139)
  Fig. 74  p.126  (p140)   (a)+(b)+(c)
  Fig. 75  p.127  (p141)
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Polygon, Circle, Rectangle, Arc

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
    'hatch.linewidth': 0.8,
})

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(ROOT, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)


def save(fig, key):
    fig.savefig(os.path.join(FIGDIR, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREVDIR, 'fig_%s.png' % key),
                dpi=200, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)
    print('saved fig_%s' % key)


# ----------------------------------------------------------------- helpers
def arrow(ax, p0, p1, lw=1.1, ms=10, zorder=6, ls='-'):
    ax.annotate('', xy=p1, xytext=p0, zorder=zorder,
                arrowprops=dict(arrowstyle='-|>', lw=lw, mutation_scale=ms,
                                color='k', linestyle=ls, shrinkA=0, shrinkB=0))


def line(ax, xs, ys, lw=1.1, ls='-', zorder=5):
    ax.plot(xs, ys, color='k', lw=lw, ls=ls, solid_capstyle='butt',
            zorder=zorder)


def hatched_rect(ax, x0, y0, x1, y1, hatch, zorder=2):
    """Region filled with hatch only (no border)."""
    r = Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor='none',
                  edgecolor='k', lw=0.0, hatch=hatch, zorder=zorder)
    ax.add_patch(r)
    return r


def brace(ax, x, y0, y1, w, side='right', lw=1.0, zorder=6):
    """Vertical curly brace; ends at (x,y0),(x,y1), cusp toward 'side'."""
    sgn = 1.0 if side == 'right' else -1.0
    h = y1 - y0
    ym = 0.5 * (y0 + y1)
    verts = [(x, y1)]
    codes = [Path.MOVETO]
    seg = [((1.10, 0.16), (0.55, 0.30)),
           ((0.55, 0.44), (1.00, 0.50)),
           ((0.55, 0.56), (0.55, 0.70)),
           ((1.10, 0.84), (0.00, 1.00))]
    for (fc, fy), (fe, ey) in seg:
        verts.append((x + sgn * w * fc, y1 - h * fy))
        codes.append(Path.CURVE3)
        verts.append((x + sgn * w * fe, y1 - h * ey))
        codes.append(Path.CURVE3)
    pp = PathPatch(Path(verts, codes), facecolor='none', edgecolor='k',
                   lw=lw, capstyle='round', joinstyle='round', zorder=zorder)
    ax.add_patch(pp)
    return pp


def poly_area(pts):
    p = np.asarray(pts, float)
    x, y = p[:, 0], p[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def stipple(ax, verts, density, seed, srange=(0.4, 1.5), zorder=3):
    """Fill polygon verts with random fine dots (~textbook stipple)."""
    verts = np.asarray(verts, float)
    poly = Path(verts, closed=True)
    bb = poly.get_extents()
    rng = np.random.default_rng(seed)
    n = int(density * poly_area(verts)) + 8
    pts = rng.uniform((bb.x0, bb.y0), (bb.x1, bb.y1),
                      size=(int(n * 2.5) + 40, 2))
    keep = pts[poly.contains_points(pts)][:n]
    if len(keep) == 0:
        return
    ss = rng.uniform(srange[0], srange[1], keep.shape[0])
    ax.scatter(keep[:, 0], keep[:, 1], s=ss, c='k', linewidths=0,
               zorder=zorder)


def stipple_seg(ax, p0, p1, halfw, density, seed, zorder=3):
    """Stippled band (rectangle) from p0 to p1 with half-width halfw."""
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    d = p1 - p0
    L = np.hypot(*d)
    u = d / L
    nvec = np.array([-u[1], u[0]])
    a = p0 + nvec * halfw; b = p1 + nvec * halfw
    c = p1 - nvec * halfw; e = p0 - nvec * halfw
    stipple(ax, [a, b, c, e], density, seed, zorder=zorder)


def double_line(ax, p0, p1, gap, lw=0.9, ls='-', zorder=4):
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    d = p1 - p0
    L = np.hypot(*d)
    nvec = np.array([-d[1], d[0]]) / L * gap
    for s in (+1, -1):
        a = p0 + nvec * s; b = p1 + nvec * s
        line(ax, [a[0], b[0]], [a[1], b[1]], lw=lw, ls=ls, zorder=zorder)


def bond_polygon(p0, p1, r, hw_a, hw_m, hw_b, bulge=None):
    """Bowtie-ish polygon between atom edges (r=atom radius).
    hw_a/hw_b: half-widths at the two ends; hw_m at the waist.
    bulge: (side, frac, extra) -> extra half-width on side (+1|-1) at
    fraction frac along the way from that end, giving a curved fat lobe."""
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    d = p1 - p0
    L = np.hypot(*d)
    u = d / L
    nvec = np.array([-u[1], u[0]])
    a = p0 + u * r
    b = p1 - u * r
    m = 0.5 * (a + b)
    def pt(t):
        return a + (b - a) * t
    # sequence of (point, halfwidth) along the +normal side, a->b
    top = [(a, hw_a)]
    if bulge is not None:
        side, f, extra = bulge
        if side > 0:
            top.append((pt(f), max(hw_a, hw_m) * 0.6 + extra))
    top.append((m, hw_m))
    if bulge is not None:
        side, f, extra = bulge
        if side < 0:
            top.append((pt(f), max(hw_b, hw_m) * 0.6 + extra))
    top.append((b, hw_b))
    pts = [p + nvec * hw for p, hw in top]
    pts += [p - nvec * hw for p, hw in reversed(top)]
    return pts


def atom(ax, p, r, lw=1.1, face='white', hatch=None, zorder=8):
    c = Circle(p, r, facecolor=face, edgecolor='k', lw=lw, hatch=hatch,
               zorder=zorder)
    ax.add_patch(c)
    return c


def dot(ax, p, r=0.035, zorder=9):
    ax.add_patch(Circle(p, r, facecolor='k', edgecolor='k', lw=0,
                        zorder=zorder))


def ell_axes(ax, x, ybot, ytop):
    """Vertical energy axis with arrowhead + script-E label."""
    arrow(ax, (x, ybot), (x, ytop), lw=1.2, ms=12)
    ax.text(x - 0.09, ytop, r'$\mathcal{E}$', ha='right', va='center',
            fontsize=12)


# ------------------------------------------------------------------ fig 67
def fig_67():
    fig, ax = plt.subplots(figsize=(3.9, 4.9))
    ax.set_xlim(-0.55, 3.05)
    ax.set_ylim(-0.25, 5.45)
    ax.axis('off')
    ax.set_aspect('equal')

    # ---------------- panel (a), shifted up by 2.80
    y0 = 2.80
    ell_axes(ax, 0.12, y0 + 0.20, y0 + 2.42)
    # conduction band (single hatch), gap, valence band (cross hatch)
    hatched_rect(ax, 0.12, y0 + 1.85, 1.50, y0 + 2.28, '///')
    hatched_rect(ax, 0.12, y0 + 0.55, 1.50, y0 + 1.38, 'xxx')
    line(ax, [0.12, 1.50], [y0 + 1.85] * 2)          # bottom of cond. band
    line(ax, [0.12, 1.50], [y0 + 1.38] * 2)          # top of valence band
    # excitations: hole -> electron + horizontal arrow
    for xc in (0.62, 1.18):
        atom(ax, (xc, y0 + 1.12), 0.042, lw=1.0)
        arrow(ax, (xc, y0 + 1.10), (xc, y0 + 2.00), lw=1.1, ms=9)
        dot(ax, (xc, y0 + 2.04), 0.037)
        arrow(ax, (xc + 0.05, y0 + 2.04), (xc + 0.33, y0 + 2.04), lw=1.1, ms=9)
    brace(ax, 1.60, y0 + 1.38, y0 + 1.85, 0.07, 'right')
    ax.text(1.76, y0 + 1.615, 'Energy gap', ha='left', va='center',
            fontsize=10)
    ax.text(1.66, y0 + 2.06, 'Conduction band', ha='left', va='center',
            fontsize=10)
    ax.text(1.66, y0 + 0.97, 'Valence band', ha='left', va='center',
            fontsize=10)
    ax.text(0.10, y0 - 0.22, r'$(a)$', ha='left', va='center')

    # ---------------- panel (b)
    ell_axes(ax, 0.12, 0.15, 2.15)
    hatched_rect(ax, 0.12, 1.38, 1.50, 1.85, '///')
    hatched_rect(ax, 0.12, 0.85, 1.50, 1.38, 'xxx')
    line(ax, [0.12, 1.50], [1.85] * 2)
    line(ax, [0.12, 1.50], [1.38] * 2)
    line(ax, [0.12, 1.50], [0.85] * 2)
    brace(ax, 0.02, 0.85, 1.85, 0.07, 'left')
    ax.text(-0.16, 1.35, 'Band', ha='right', va='center', fontsize=10)
    brace(ax, 1.60, 0.85, 1.38, 0.07, 'right')
    ax.text(1.76, 1.115, 'Occupied states', ha='left', va='center',
            fontsize=10)
    for xc in (0.72, 1.15):
        dot(ax, (xc, 1.52), 0.037)
        arrow(ax, (xc + 0.05, 1.52), (xc + 0.33, 1.52), lw=1.1, ms=9)
    ax.text(-0.04, 0.50, r'$(b)$', ha='right', va='center')
    save(fig, '67')


# ------------------------------------------------------------------ fig 68
def fig_68():
    fig, ax = plt.subplots(figsize=(3.9, 1.75))
    ax.set_xlim(-0.15, 4.15)
    ax.set_ylim(0.0, 2.3)
    ax.axis('off')
    # three strips (left/right edges open)
    hatched_rect(ax, 0.0, 1.32, 2.45, 2.10, '///')
    hatched_rect(ax, 0.0, 1.00, 2.45, 1.32, 'xxx')
    hatched_rect(ax, 0.0, 0.20, 2.45, 1.00, '///')
    for yb in (2.10, 1.32, 1.00, 0.20):
        line(ax, [0.0, 2.45], [yb] * 2)
    line(ax, [0.0, 2.45], [1.16] * 2, ls=(0, (5, 4)))   # dashed mid-line
    brace(ax, 2.60, 0.20, 1.32, 0.08, 'right')
    ax.text(2.78, 0.76, 'Occupied states', ha='left', va='center',
            fontsize=10)
    save(fig, '68')


# ------------------------------------------------------------------ fig 69
def fig_69():
    fig, ax = plt.subplots(figsize=(3.5, 4.9))
    ax.set_xlim(-2.75, 3.35)
    ax.set_ylim(-5.85, 2.55)
    ax.axis('off')
    ax.set_aspect('equal')

    # ================= panel (a): extended zone scheme
    rho = 0.62          # corner-carve arc radius
    bulge = 0.10        # outward bulge across each face centre
    y0l, apex = 0.33, 1.36   # lobe hood: half-base / apex distance
    corners = [np.array([np.cos(np.pi / 4 + k * np.pi / 2),
                         np.sin(np.pi / 4 + k * np.pi / 2)]) * np.sqrt(2)
               for k in range(4)]                    # (1,1) (-1,1) (-1,-1) (1,-1)
    faces = [np.array([np.cos(k * np.pi / 2), np.sin(k * np.pi / 2)])
             for k in range(4)]                      # +x +y -x -y
    # ---- central occupied patch (cross hatch)
    central = []
    for k in range(4):
        a0 = np.deg2rad(-90 + 90 * k)
        tt = np.linspace(a0, a0 - np.pi / 2, 30)
        central += [(corners[k][0] + rho * np.cos(t),
                     corners[k][1] + rho * np.sin(t)) for t in tt]
        p_end = np.array(central[-1])
        p_next = np.array([corners[(k + 1) % 4][0] +
                           rho * np.cos(np.deg2rad(-90 + 90 * (k + 1))),
                           corners[(k + 1) % 4][1] +
                           rho * np.sin(np.deg2rad(-90 + 90 * (k + 1)))])
        fm = faces[(k + 1) % 4] * (1 + bulge)
        ctrl = 2 * fm - 0.5 * (p_end + p_next)
        for f in np.linspace(0, 1, 20)[1:]:
            p = (1 - f) ** 2 * p_end + 2 * f * (1 - f) * ctrl + f ** 2 * p_next
            central.append(tuple(p))
    ax.add_patch(Polygon(central, closed=True, facecolor='none',
                         edgecolor='k', lw=0.0, hatch='xxx', zorder=2))
    # ---- lobes across the four faces (single hatch)
    cx = (1 + y0l ** 2 - apex ** 2) / (2 * (1 - apex))
    lobe_R = np.hypot(1 - cx, y0l)
    for k in range(4):
        nvec = faces[k]
        pvec = np.array([-nvec[1], nvec[0]])
        p1 = nvec * 1 + pvec * y0l
        p2 = nvec * 1 - pvec * y0l
        cen = nvec * cx
        ta = np.arctan2(*(p1 - cen)[::-1])
        tb = np.arctan2(*(p2 - cen)[::-1])
        if tb > ta:
            tb -= 2 * np.pi
        tt = np.linspace(ta, tb, 40)
        hood = [(cen[0] + lobe_R * np.cos(t), cen[1] + lobe_R * np.sin(t))
                for t in tt]
        ax.add_patch(Polygon(hood + [tuple(nvec)], closed=True,
                             facecolor='none', edgecolor='k', lw=0.0,
                             hatch='///', zorder=2))
        hl = np.array(hood)
        ax.plot(hl[:, 0], hl[:, 1], color='k', lw=1.0, zorder=5)
        cen2 = nvec * (cx + 0.16)
        tt = np.linspace(0, 2 * np.pi, 60)
        ax.plot(cen2[0] + 0.115 * np.cos(tt), cen2[1] + 0.115 * np.sin(tt),
                color='k', lw=0.9, zorder=5)
    # ---- central constant-energy contours
    tt = np.linspace(0, 2 * np.pi, 90)
    for r in (0.33, 0.62):
        ax.plot(r * np.cos(tt), r * np.sin(tt), color='k', lw=0.9, zorder=5)
    # ---- zone boundaries
    ax.add_patch(Polygon([(-1, -1), (1, -1), (1, 1), (-1, 1)], closed=True,
                         facecolor='none', edgecolor='k', lw=1.3, zorder=6))
    ax.add_patch(Polygon([(2, 0), (0, 2), (-2, 0), (0, -2)], closed=True,
                         facecolor='none', edgecolor='k', lw=1.0, zorder=6))
    # ---- axes: 100 horizontal, 110 diagonal, A at right face centre
    arrow(ax, (0, 0), (2.30, 0), lw=1.1, ms=11, zorder=8)
    ax.text(2.30, -0.22, '100', ha='center', va='top', fontsize=10)
    arrow(ax, (0, 0), (1.03, 1.03), lw=1.0, ms=10, zorder=8)
    ax.text(1.14, 1.10, '110', ha='left', va='center', fontsize=10)
    arrow(ax, (1.38, -0.40), (1.04, -0.05), lw=0.9, ms=8, zorder=8)
    ax.text(1.45, -0.48, r'$A$', ha='left', va='center', fontsize=11)
    ax.text(0.0, -2.45, r'$(a)$', ha='center', va='center')

    # ================= panel (b): eps(k) in reduced zone (scaled x S)
    S = 1.5
    yb = -5.05
    def X(x):
        return x * S
    def Y(y):
        return yb + y * S
    E1, E2, EA, Et, Emin = 0.62, 0.56, 0.42, 1.00, 0.02
    xL, xR, xc0, xc1 = 0.0, 1.0, 1.18, 1.78
    line(ax, [X(xL), X(xL)], [Y(0), Y(0.90)])
    line(ax, [X(xL), X(xR)], [Y(0)] * 2)
    line(ax, [X(xR), X(xR)], [Y(0), Y(0.72)])
    xs_l = np.linspace(0, 0.5, 60)
    xs_r = np.linspace(0.5, 1.0, 60)
    upper_l = E1 + (Et - E1) * np.sin(np.pi / 2 * xs_l / 0.5) ** 1.2
    upper_r = E2 + (Et - E2) * np.cos(np.pi / 2 * (xs_r - 0.5) / 0.5) ** 1.3
    lower_l = Emin + (E1 - Emin) * (1 - xs_l / 0.5) ** 1.3
    lower_r = Emin + (EA - Emin) * np.sin(np.pi / 2 * (xs_r - 0.5) / 0.5) ** 1.4
    line(ax, X(xL + xs_l), Y(upper_l))
    line(ax, X(xL + xs_r), Y(upper_r))
    line(ax, X(xL + xs_l), Y(lower_l))
    line(ax, X(xL + xs_r), Y(lower_r))
    line(ax, [X(0.5), X(0.5)], [Y(0), Y(Et)], ls=(0, (6, 4)))
    line(ax, [X(xL), X(xc1)], [Y(E1)] * 2, ls=(0, (1.5, 2.5)))
    line(ax, [X(0.5), X(xc0)], [Y(Et)] * 2, ls=(0, (1.5, 2.5)))
    line(ax, [X(xR), X(xc1)], [Y(E2)] * 2)
    line(ax, [X(xR), X(xc0)], [Y(0)] * 2, ls=(0, (1.5, 2.5)))
    hatched_rect(ax, X(xc0), Y(0), X(xc1), Y(Et), '///', zorder=2)
    hatched_rect(ax, X(xc0), Y(E2), X(xc1), Y(E1), 'xxx', zorder=3)
    line(ax, [X(xc0), X(xc1)], [Y(Et)] * 2)
    line(ax, [X(xc0), X(xc1)], [Y(0)] * 2)
    line(ax, [X(xc0), X(xc1)], [Y(E2)] * 2, zorder=6)
    ax.text(X(0.56), Y(0.80), r'$\mathcal{E}_k$', ha='left', va='center',
            fontsize=11)
    ax.text(X(1.035), Y(EA - 0.02), r'$A$', ha='left', va='center',
            fontsize=11)
    for xt, lab, fnt in ((xL, '110', 9), (0.30, r'$\boldsymbol{k}$', 9),
                         (0.5, r'$O$', 9), (0.68, r'$\boldsymbol{k}$', 9),
                         (1.02, '(100)', 9)):
        ax.text(X(xt), Y(0) - 0.07, lab, ha='center', va='top', fontsize=fnt)
    ax.text(X(0.5), Y(0) - 0.55, r'$(b)$', ha='center', va='center')
    save(fig, '69')


def fig_70():
    fig, ax = plt.subplots(figsize=(3.3, 3.3))
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.55, 1.55)
    ax.axis('off')
    ax.set_aspect('equal')
    Rf = 1.28                       # free-electron sphere (dashed)
    rho = 0.27                      # corner cutout radius
    # stippled occupied region = square minus 4 corner disks
    rng = np.random.default_rng(7)
    n = 2600
    pts = rng.uniform(-1, 1, size=(n * 3, 2))
    keep = np.ones(len(pts), bool)
    for cx_ in (-1, 1):
        for cy_ in (-1, 1):
            keep &= (np.hypot(pts[:, 0] - cx_, pts[:, 1] - cy_) > rho)
    keep &= (np.abs(pts).max(axis=1) <= 1)
    pts = pts[keep][:n]
    ax.scatter(pts[:, 0], pts[:, 1], s=rng.uniform(0.4, 1.5, len(pts)),
               c='k', linewidths=0, zorder=2)
    # corner cutout arcs (quarter arcs just inside the square corners)
    for cx_ in (-1, 1):
        for cy_ in (-1, 1):
            a_x = np.pi if cx_ > 0 else 0.0        # inward-x direction
            a_y = 1.5 * np.pi if cy_ > 0 else 0.5 * np.pi  # inward-y
            d0 = a_y - a_x
            if d0 > np.pi:
                d0 -= 2 * np.pi
            elif d0 < -np.pi:
                d0 += 2 * np.pi
            th = np.linspace(a_x, a_x + d0, 30)
            ax.plot(cx_ + rho * np.cos(th), cy_ + rho * np.sin(th),
                    color='k', lw=1.1, zorder=5)
    # caps outside each face (hood arcs) + light stipple
    cap_hw, cap_apex = 0.34, 1.24
    cx = (1 - cap_apex ** 2 + cap_hw ** 2) / (2 * (1 - cap_apex))
    Rc = np.hypot(1 - cx, cap_hw)
    u0 = np.arctan2(cap_hw, 1 - cx)
    faces70 = [np.array([np.cos(k * np.pi / 2), np.sin(k * np.pi / 2)])
               for k in range(4)]
    for k in range(4):
        nvec = faces70[k]
        pvec = np.array([-nvec[1], nvec[0]])
        uu = np.linspace(-u0, u0, 40)
        pts = []
        for u in uu:
            rad = cx + Rc * np.cos(u)
            off = Rc * np.sin(u)
            pts.append((rad * nvec[0] + off * pvec[0],
                        rad * nvec[1] + off * pvec[1]))
        pl = np.array(pts)
        ax.plot(pl[:, 0], pl[:, 1], color='k', lw=1.1, zorder=5)
        stipple(ax, pts + [tuple(nvec)], 260, 100 + k,
                srange=(0.4, 1.3), zorder=2)
    # zone boundary square
    ax.add_patch(Polygon([(-1, -1), (1, -1), (1, 1), (-1, 1)], closed=True,
                         facecolor='none', edgecolor='k', lw=1.3, zorder=6))
    # free-electron sphere, dashed
    tt = np.linspace(0, 2 * np.pi, 200)
    ax.plot(Rf * np.cos(tt), Rf * np.sin(tt), color='k', lw=1.1,
            ls=(0, (6, 4)), zorder=6)
    save(fig, '70')


# ------------------------------------------------------------------ fig 71
def fig_71():
    fig, ax = plt.subplots(figsize=(4.8, 2.0))
    ax.set_xlim(-0.75, 8.10)
    ax.set_ylim(-0.35, 2.05)
    ax.axis('off')

    for xoff, noble in ((0.0, False), (4.35, True)):
        xb0, xb1 = 0.75 + xoff, 1.65 + xoff     # band width
        ytop_s = 1.72          # top of s-band
        if not noble:
            yst = 1.30         # top of occupied stack (top of d-band)
            yd1, yd2 = 1.06, yst
            ybot = 0.30
            hatched_rect(ax, xb0, yd1, xb1, yd2, 'xxx')
            hatched_rect(ax, xb0, ybot, xb1, yd1, '///')
            line(ax, [xb0, xb1], [yst] * 2)
            line(ax, [xb0, xb1], [yd1] * 2)
            line(ax, [xb0, xb1], [ybot] * 2)
            brace(ax, xb0 - 0.04, ybot, yst, 0.065, 'left')
            ax.text(xb0 - 0.20, 0.5 * (ybot + yst), 'Occupied\nstates',
                    ha='right', va='center', fontsize=10)
            brace(ax, xb1 + 0.04, yd1, yd2, 0.05, 'right', lw=0.9)
            ax.text(xb1 + 0.16, 0.5 * (yd1 + yd2), r'$d$-' + '\n' + 'band',
                    ha='left', va='center', fontsize=10)
        else:
            yF = 1.30          # Fermi level (dashed)
            yd1, yd2 = 0.78, 1.02
            ybot = 0.30
            hatched_rect(ax, xb0, yd2, xb1, yF, '///')
            hatched_rect(ax, xb0, yd1, xb1, yd2, 'xxx')
            hatched_rect(ax, xb0, ybot, xb1, yd1, '///')
            line(ax, [xb0, xb1], [ybot] * 2)
            line(ax, [xb0, xb1], [yd1] * 2)
            line(ax, [xb0, xb1], [yd2] * 2)
            line(ax, [xb0, xb1], [yF] * 2, ls=(0, (5, 4)))
            ax.text(0.5 * (xb0 + xb1), yF + 0.09, 'Fermi level',
                    ha='center', va='bottom', fontsize=10)
            brace(ax, xb0 - 0.04, ybot, yF, 0.065, 'left')
            ax.text(xb0 - 0.20, 0.5 * (ybot + yF), 'Occupied\nstates',
                    ha='right', va='center', fontsize=10)
            brace(ax, xb1 + 0.04, yd1, yd2, 0.05, 'right', lw=0.9)
            ax.text(xb1 + 0.16, 0.5 * (yd1 + yd2), r'$d$-band',
                    ha='left', va='center', fontsize=10)
        line(ax, [xb0, xb1], [ytop_s] * 2)
        brace(ax, xb1 + 1.18, ybot, ytop_s, 0.07, 'right')
        ax.text(xb1 + 1.33, 0.5 * (ybot + ytop_s), r'$S$ band',
                ha='left', va='center', fontsize=11)
        ax.text(xb0 - 0.05, -0.22, r'$(a)$' if not noble else r'$(b)$',
                ha='center', va='center')
    save(fig, '71')


# ------------------------------------------------------------------ fig 72
def fig_72():
    fig, ax = plt.subplots(figsize=(3.3, 3.95))
    ax.set_xlim(-0.35, 1.90)
    ax.set_ylim(-2.60, 0.40)
    ax.axis('off')
    ax.set_aspect('equal')

    c1 = np.array([0.95, -0.15])       # screen vector of (1,0,0)
    c2 = np.array([0.60, -0.60])       # screen vector of (0,1,0)
    w = np.array([0.00, -1.45])        # screen vector of (0,0,-1)
    A = np.array([0.0, 0.0])           # atom A at cube corner (0,0,1)

    def P(p):
        return A + p[0] * c1 + p[1] * c2 + (1 - p[2]) * w

    r = 0.105
    corners = {(i, j, k): P((i, j, k))
               for i in (0, 1) for j in (0, 1) for k in (0, 1)}
    faces = {f: P(f) for f in
             [(0.5, 0.5, 1), (0.5, 0.5, 0), (0.5, 0, 0.5),
              (0.5, 1, 0.5), (0, 0.5, 0.5), (1, 0.5, 0.5)]}
    Bsub = {b: P(b) for b in
            [(0.25, 0.25, 0.75), (0.75, 0.75, 0.75),
             (0.75, 0.25, 0.25), (0.25, 0.75, 0.25)]}
    Bb = (0.25, 0.25, 0.75)
    hatched = [(0.5, 0.5, 1), (0.5, 0, 0.5), (0, 0.5, 0.5)]
    A_lab = (0, 0, 1)
    bonds = {
        (0.25, 0.25, 0.75): [(0, 0, 1), (0.5, 0.5, 1), (0.5, 0, 0.5),
                             (0, 0.5, 0.5)],
        (0.75, 0.75, 0.75): [(1, 1, 1), (0.5, 0.5, 1), (1, 0.5, 0.5),
                             (0.5, 1, 0.5)],
        (0.75, 0.25, 0.25): [(1, 0, 0), (0.5, 0.5, 0), (0.5, 0, 0.5),
                             (1, 0.5, 0.5)],
        (0.25, 0.75, 0.25): [(0, 1, 0), (0.5, 1, 0.5), (0.5, 0.5, 0),
                             (0, 0.5, 0.5)],
    }
    # ---- cube edges (all except the hidden back vertical)
    edges = []
    for (i, j, k) in corners:
        for d in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            q = (i + d[0], j + d[1], k + d[2])
            if max(q) <= 1 and (q, (i, j, k)) not in edges:
                edges.append(((i, j, k), q))
    for e in edges:
        if set(e) == {(0, 1, 0), (0, 1, 1)}:
            continue
        p, q = corners[e[0]], corners[e[1]]
        line(ax, [p[0], q[0]], [p[1], q[1]], lw=0.9, zorder=3)
    # ---- framework bonds (thin double lines)
    allpos = {}
    allpos.update(corners)
    allpos.update(faces)
    for b, ns in bonds.items():
        if b == Bb:
            continue
        p = Bsub[b]
        for nb in ns:
            q = allpos[nb]
            double_line(ax, p, q, 0.016, lw=0.8, zorder=4)
    # ---- tetrahedral bonds of B (thick double lines)
    pB = Bsub[Bb]
    pA = corners[A_lab]
    double_line(ax, pB, pA, 0.028, lw=1.2, zorder=5)
    stipple_seg(ax, pB, pA, 0.026, 900, seed=42, zorder=5)
    double_line(ax, pB, faces[(0.5, 0, 0.5)], 0.028, lw=1.2,
                ls=(0, (4, 3)), zorder=5)
    for nb in [(0.5, 0.5, 1), (0, 0.5, 0.5)]:
        double_line(ax, pB, faces[nb], 0.028, lw=1.2, zorder=5)
    # ---- atoms
    for p in corners.values():
        atom(ax, tuple(p), r, lw=1.0)
    for f, p in faces.items():
        if f in hatched:
            atom(ax, tuple(p), r, lw=1.0, hatch='///')
        else:
            atom(ax, tuple(p), r, lw=1.0)
    for b, p in Bsub.items():
        if b == Bb:
            atom(ax, tuple(p), r, lw=1.0, face='black')
        else:
            atom(ax, tuple(p), r, lw=2.0)
    ax.text(pA[0] + 0.10, pA[1] + 0.08, r'$A$', ha='left', va='bottom',
            fontsize=12, zorder=11)
    ax.text(pB[0] + 0.13, pB[1] + 0.04, r'$B$', ha='left', va='center',
            fontsize=12, zorder=11)
    save(fig, '72')


# ------------------------------------------------------- figs 73/74/75 grid
def ion_grid(ax, ox, oy, labels, bold_flags, bonds, seed0,
             r=0.30, sp=1.0, dens=1150):
    """3x3 ionic grid. labels: dict {(i,j): text}; bold_flags: Sb/S circles.
    bonds: None (bare ions) | 'band' (rect stipple, Ge) |
    'sym' (symmetric bowtie) | 'pol' (polarized bowtie, fat at bold atom)."""
    pos = {}
    for i in range(3):
        for j in range(3):
            pos[(i, j)] = (ox + i * sp, oy + j * sp)

    def hw_pair(i1, j1, i2, j2):
        b1, b2 = bold_flags[(i1, j1)], bold_flags[(i2, j2)]
        if bonds == 'band':
            return (0.16, 0.16, 0.16, None)
        if bonds == 'sym':
            return (0.17, 0.05, 0.17, None)
        if bonds == 'pol':
            if b1 and not b2:
                return (0.22, 0.05, 0.12, +1)
            if b2 and not b1:
                return (0.12, 0.05, 0.22, -1)
        return (0.17, 0.05, 0.17, None)

    def draw_bond(p1, p2, tag, n):
        if bonds is None:
            return
        hwa, hwm, hwb, side = hw_pair(tag[0], tag[1], tag[2], tag[3])
        bulge = None
        if bonds == 'pol' and side is not None:
            bulge = (side, 0.45, 0.07)
        verts = bond_polygon(p1, p2, r * 0.92, hwa, hwm, hwb, bulge=bulge)
        ax.add_patch(Polygon(verts, closed=True, facecolor='none',
                             edgecolor='k', lw=0.0, zorder=2))
        stipple(ax, verts, dens, seed0 * 31 + n, srange=(0.5, 2.0), zorder=2)
        # electron dots (two pairs)
        p1 = np.array(p1, float); p2 = np.array(p2, float)
        d = p2 - p1
        L = np.hypot(*d)
        nv = np.array([-d[1], d[0]]) / L
        if bonds == 'band':
            tpair = (0.38, 0.62)
        elif hwa > hwb:
            tpair = (0.38, 0.68)
        else:
            tpair = (0.62, 0.32)
        for t in tpair:
            c = p1 + d * t
            for s in (+0.058, -0.058):
                dot(ax, (c[0] + nv[0] * s, c[1] + nv[1] * s), 0.048)

    def draw_stub(p, q, ij, n):
        if bonds is None:
            return
        hw = 0.21 if bold_flags[ij] else 0.14
        verts = bond_polygon(p, q, r * 0.92, hw, 0.055, 0.045)
        ax.add_patch(Polygon(verts, closed=True, facecolor='none',
                             edgecolor='k', lw=0.0, zorder=2))
        stipple(ax, verts, dens, seed0 * 31 + 100 + n, srange=(0.5, 2.0),
                zorder=2)
        p = np.array(p, float); q = np.array(q, float)
        c = p + (q - p) * 0.70
        d = q - p
        nv = np.array([-d[1], d[0]]) / np.hypot(*d)
        for s in (+0.052, -0.052):
            dot(ax, (c[0] + nv[0] * s, c[1] + nv[1] * s), 0.048)

    n = 0
    for j in range(3):
        for i in range(2):
            draw_bond(pos[(i, j)], pos[(i + 1, j)], (i, j, i + 1, j), n)
            n += 1
    for i in range(3):
        for j in range(2):
            draw_bond(pos[(i, j)], pos[(i, j + 1)], (i, j, i, j + 1), n)
            n += 1
    for j in range(3):
        for i, sgn in ((0, -1), (2, +1)):
            p = pos[(i, j)]
            draw_stub(p, (p[0] + sgn * 0.75, p[1]), (i, j), n)
            n += 1
    for i in range(3):
        for j, sgn in ((0, -1), (2, +1)):
            p = pos[(i, j)]
            draw_stub(p, (p[0], p[1] + sgn * 0.75), (i, j), n)
            n += 1
    for (i, j), p in pos.items():
        lw = 2.1 if bold_flags[(i, j)] else 1.0
        atom(ax, p, r, lw=lw)
        ax.text(p[0], p[1], labels[(i, j)], ha='center', va='center',
                fontsize=9, zorder=10)


def fig_73():
    fig, ax = plt.subplots(figsize=(3.15, 3.25))
    ax.set_xlim(-1.15, 3.15)
    ax.set_ylim(-1.15, 3.15)
    ax.axis('off')
    ax.set_aspect('equal')
    labels = {(i, j): 'Ge' for i in range(3) for j in range(3)}
    bold = {(i, j): False for i in range(3) for j in range(3)}
    ion_grid(ax, 0, 0, labels, bold, 'band', seed0=5, dens=1500)
    save(fig, '73')


def fig_74():
    fig, ax = plt.subplots(figsize=(4.8, 4.45))
    ax.set_xlim(-1.25, 6.70)
    ax.set_ylim(-4.55, 2.90)
    ax.axis('off')
    ax.set_aspect('equal')
    lab_a = {(0, 0): r'In$^{3+}$', (1, 0): r'Sb$^{5+}$', (2, 0): r'In$^{3+}$',
             (0, 1): r'Sb$^{5+}$', (1, 1): r'In$^{3+}$', (2, 1): r'Sb$^{5+}$',
             (0, 2): r'In$^{3+}$', (1, 2): r'Sb$^{5+}$', (2, 2): r'In$^{3+}$'}
    bold = {(i, j): (i + j) % 2 == 1
            for i in range(3) for j in range(3)}
    ion_grid(ax, 0, 0, lab_a, bold, None, seed0=11)
    ax.text(1.0, -0.95, r'$(a)$', ha='center', va='center')
    lab_b = {(0, 0): r'In$^-$', (1, 0): r'Sb$^+$', (2, 0): r'In$^-$',
             (0, 1): r'Sb$^+$', (1, 1): r'In$^-$', (2, 1): r'Sb$^+$',
             (0, 2): r'In$^-$', (1, 2): r'Sb$^+$', (2, 2): r'In$^-$'}
    ion_grid(ax, 3.7, 0, lab_b, bold, 'sym', seed0=17)
    ax.text(4.7, -0.95, r'$(b)$', ha='center', va='center')
    lab_c = {(0, 0): 'In', (1, 0): 'Sb', (2, 0): 'In',
             (0, 1): 'Sb', (1, 1): 'In', (2, 1): 'Sb',
             (0, 2): 'In', (1, 2): 'Sb', (2, 2): 'In'}
    ion_grid(ax, 1.85, -3.35, lab_c, bold, 'pol', seed0=23)
    ax.text(2.85, -4.30, r'$(c)$', ha='center', va='center')
    save(fig, '74')


def fig_75():
    fig, ax = plt.subplots(figsize=(3.15, 3.25))
    ax.set_xlim(-1.15, 3.15)
    ax.set_ylim(-1.15, 3.15)
    ax.axis('off')
    ax.set_aspect('equal')
    labels = {(0, 0): 'Zn', (1, 0): 'S', (2, 0): 'Zn',
              (0, 1): 'S', (1, 1): 'Zn', (2, 1): 'S',
              (0, 2): 'Zn', (1, 2): 'S', (2, 2): 'Zn'}
    bold = {(i, j): (i + j) % 2 == 1
            for i in range(3) for j in range(3)}
    ion_grid(ax, 0, 0, labels, bold, 'pol', seed0=29)
    save(fig, '75')


if __name__ == '__main__':
    for f in (fig_67, fig_68, fig_69, fig_70, fig_71, fig_72, fig_73,
              fig_74, fig_75):
        f()
