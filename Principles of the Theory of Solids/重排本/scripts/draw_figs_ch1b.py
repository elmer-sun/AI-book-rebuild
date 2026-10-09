# -*- coding: utf-8 -*-
"""Redraw Ziman, Principles of the Theory of Solids, 2nd ed., Chapter 1, Figs. 9-15.
Black-and-white textbook-style vector figures. One function per figure;
each function saves PDF + PNG immediately.
"""
import os
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.path import Path

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
    'hatch.linewidth': 0.5,
})

BASE = r'E:\AI整理书籍\齐曼\重排本'
OUT = os.path.join(BASE, 'figures')
PRE = os.path.join(OUT, 'preview')
os.makedirs(PRE, exist_ok=True)

BLACK = 'k'


def save(fig, key):
    fig.savefig(os.path.join(OUT, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRE, 'fig_%s.png' % key),
                bbox_inches='tight', pad_inches=0.03, dpi=170)
    plt.close(fig)
    print('saved fig_%s' % key)


def arrow(ax, p0, p1, lw=1.4, ms=10, zorder=5, style='-|>'):
    ax.annotate('', xy=p1, xytext=p0, zorder=zorder,
                arrowprops=dict(arrowstyle=style, lw=lw, color=BLACK,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def dline(ax, p0, p1, lw=1.1, dashes=(4, 3), zorder=2):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=BLACK, lw=lw,
            linestyle=(0, dashes), zorder=zorder)


def brace(ax, p0, p1, depth=0.1, side=1, lw=1.0):
    """Curly brace from p0 to p1; tooth points to side (±1) of p0->p1."""
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    L = p1 - p0
    el = np.hypot(*L)
    lh = L / el
    nh = np.array([-lh[1], lh[0]]) * side
    w = el
    xm = 0.5 * el
    e = 0.045 * w
    d = depth
    # local coordinates along (lh, nh), origin at p0
    def loc(t, s):
        return p0 + lh * t + nh * s
    verts = [loc(0, 0)]
    codes = [Path.MOVETO]
    segs = [
        (0.25 * w, 0.08 * d, xm - e, 0.5 * d),   # ctrl, ctrl?, end ...
    ]
    # two quadratic curves per half: A->B, B->T, T->C, C->E
    pts = [
        ('C', 0.25 * w, 0.05 * d, xm - e, 0.5 * d),
        ('C', xm - 0.3 * e, 0.95 * d, xm, d),
        ('C', xm + 0.3 * e, 0.95 * d, xm + e, 0.5 * d),
        ('C', 0.75 * w, 0.05 * d, w, 0.0),
    ]
    for kind, ct, cs, et, es in pts:
        verts.append(loc(ct, cs)); codes.append(Path.CURVE3)
        verts.append(loc(et, es)); codes.append(Path.CURVE3)
    path = Path(verts, codes)
    ax.add_patch(matplotlib.patches.PathPatch(
        path, facecolor='none', edgecolor=BLACK, lw=lw, zorder=4))


def hull(points):
    """Convex hull (monotone chain)."""
    pts = sorted(set(map(tuple, points)))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def point_in_poly(pt, poly):
    x, y = pt
    n = len(poly)
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]; xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


# ---------------------------------------------------------------- fig 9
def fig_9():
    """Spacing of planes with large Miller indices vs principal planes."""
    fig, ax = plt.subplots(figsize=(3.8, 3.6))
    ax.set_aspect('equal'); ax.axis('off')

    # lattice dots (5 columns x 4 rows)
    dots = [(i, j) for i in range(5) for j in range(4)]
    # bold vertical lines = (100) planes, spacing d1 = a
    for i in range(5):
        top = 4.45 if i >= 3 else 4.25
        ax.plot([i, i], [-1.35, top], color=BLACK, lw=1.5, zorder=3)
    # thin diagonal lines = (310) planes: 3x + y = m, spacing d2 = a/sqrt(10)
    xmin, xmax, ymin, ymax = -0.62, 5.15, -1.45, 4.35
    tops = {3: 4.75, 4: 4.75}   # two leftmost lines extend higher
    for m in range(-1, 17):
        # param along direction (-1, 3)/sqrt(10); line: 3x+y=m
        # intersect with box: x = (m - y)/3
        ytop = tops.get(m, ymax)
        xs, ys = [], []
        for y in (ymin, ytop):
            x = (m - y) / 3.0
            if xmin - 0.2 <= x <= xmax + 0.2:
                xs.append(x); ys.append(y)
        for x in (xmin, xmax):
            y = m - 3 * x
            if ymin - 0.2 <= y <= ytop + 0.2:
                xs.append(x); ys.append(y)
        if len(xs) >= 2:
            ax.plot(xs[:2], ys[:2], color=BLACK, lw=0.65, zorder=1)
    # dots on top
    dx, dy = zip(*dots)
    ax.plot(dx, dy, 'o', ms=4.6, mfc=BLACK, mec=BLACK, zorder=5)

    # d1 brace between 3rd and 4th verticals (x=3..4) at top
    brace(ax, (3.02, 4.55), (3.98, 4.55), depth=0.16, side=-1, lw=1.0)
    ax.text(3.5, 4.78, r'$\mathbf{d}_1$', ha='center', va='bottom', fontsize=12)
    # d2 brace, tilted perpendicular to the two leftmost diagonal lines,
    # near their top ends (as in the original)
    ya = 4.42
    pa = np.array([(3 - ya) / 3.0, ya])
    pb = np.array([(4 - ya) / 3.0, ya])
    mid = 0.5 * (pa + pb)
    nperp = np.array([3.0, 1.0]) / np.sqrt(10.0) * 0.17
    brace(ax, mid - nperp, mid + nperp, depth=0.15, side=-1, lw=1.0)
    ax.text(mid[0] - 0.30, mid[1] + 0.18, r'$\mathbf{d}_2$', ha='right',
            va='bottom', fontsize=12)

    # g2 arrow, normal to the (310) planes: direction (3,1)/sqrt(10)
    arrow(ax, (3.72, 1.55), (4.65, 1.86), lw=1.5, ms=13)
    ax.text(4.75, 1.93, r'$\mathbf{g}_2=(3,\,1,\,0)$', ha='left',
            va='center', fontsize=11)
    # g1 arrow, horizontal
    arrow(ax, (4.03, 1.05), (5.25, 1.05), lw=1.5, ms=13)
    ax.text(5.3, 0.82, r'$\mathbf{g}_1=(1,\,0,\,0)$', ha='left',
            va='center', fontsize=11)

    ax.set_xlim(-1.15, 7.6)
    ax.set_ylim(-1.7, 5.5)
    save(fig, 9)


# ------------------------------------------------------- 3D projections
def proj_a(p):
    """Oblique projection, depth axis up-right (fig 10a)."""
    x, y, z = p
    return np.array([x + 0.378 * y, z + 0.245 * y])


def proj_b(p):
    """Oblique projection, depth up and slightly left (fig 10b)."""
    x, y, z = p
    return np.array([x - 0.06 * y, -0.10 * x + 0.38 * y + z])


def proj_c(p):
    """Oblique projection, depth up-right (fig 11)."""
    x, y, z = p
    return np.array([x + 0.36 * y, -0.08 * x + 0.21 * y + z])


def face_grid(ax, proj, o, u, v, n=13, z=3):
    """White-filled parallelogram face with fine grid, given 3D corner+edges."""
    corners = [proj(o), proj(np.array(o)+u), proj(np.array(o)+u+v),
               proj(np.array(o)+v)]
    ax.add_patch(Polygon(corners, closed=True, facecolor='white',
                         edgecolor='none', zorder=z))
    u = np.array(u); v = np.array(v); o = np.array(o)
    for k in range(1, n):
        t = float(k) / n
        a1, b1 = proj(o+u*t), proj(o+u*t+v)
        ax.plot([a1[0], b1[0]], [a1[1], b1[1]], color=BLACK, lw=0.4, zorder=z)
        a2, b2 = proj(o+v*t), proj(o+v*t+u)
        ax.plot([a2[0], b2[0]], [a2[1], b2[1]], color=BLACK, lw=0.4, zorder=z)


def draw_seg_visible(ax, p3a, p3b, hidden, lw=0.75, zorder=1, n=24):
    """Draw 3D segment keeping only screen parts not 'hidden'."""
    ts = np.linspace(0, 1, n)
    pts = [tuple(np.array(p3a) * (1-t) + np.array(p3b) * t) for t in ts]
    run = []
    segs = []
    for p in pts:
        if not hidden(p):
            run.append(proj_a(p))
        else:
            if len(run) > 1:
                segs.append(run)
            run = []
    if len(run) > 1:
        segs.append(run)
    for s in segs:
        xs = [q[0] for q in s]; ys = [q[1] for q in s]
        ax.plot(xs, ys, color=BLACK, lw=lw, zorder=zorder)


# --------------------------------------------------------------- fig 10
def fig_10():
    """Face-centred cubic lattice: (a) four interpenetrating sublattices,
    (b) as Bravais lattice."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(3.9, 6.9),
                                   gridspec_kw=dict(height_ratios=[1, 1.02]))
    # ---------------- panel (a)
    ax = ax1
    ax.set_aspect('equal'); ax.axis('off')
    sil = hull([proj_a(c) for c in
                [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]])

    def hidden(p):
        return p[1] > 1.02 and point_in_poly(proj_a(p), sil)

    # neighbor cubes sharing faces: +/-x, +/-z, +y (behind)
    neigh = [(1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0)]
    circ = set()
    for D in neigh:
        corners = [(D[0]+i, D[1]+j, D[2]+k)
                   for i in (0, 1) for j in (0, 1) for k in (0, 1)]
        for c in corners:
            if any(cc not in (0, 1) for cc in c):
                circ.add(c)
        # edges of the neighbor cube
        for a in corners:
            for d in range(3):
                b = list(a); b[d] += 1; b = tuple(b)
                if b not in corners:
                    continue
                mid = tuple(0.5 * (a[k] + b[k]) for k in range(3))
                if all(0 <= m <= 1 for m in mid):
                    continue  # edge on the central cube surface
                draw_seg_visible(ax, a, b, hidden, lw=0.75, zorder=1)
    # central cube faces (white + fine grid) occlude wireframe behind
    face_grid(ax, proj_a, (0, 0, 0), (1, 0, 0), (0, 0, 1))   # front y=0
    face_grid(ax, proj_a, (1, 0, 0), (0, 1, 0), (0, 0, 1))   # right x=1
    face_grid(ax, proj_a, (0, 0, 1), (1, 0, 0), (0, 1, 0))   # top z=1
    # bold outline of the three visible faces
    for o, u, v in [((0, 0, 0), (1, 0, 0), (0, 0, 1)),
                    ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                    ((0, 0, 1), (1, 0, 0), (0, 1, 0))]:
        o = np.array(o); u = np.array(u); v = np.array(v)
        ps = [proj_a(o), proj_a(o+u), proj_a(o+u+v), proj_a(o+v),
              proj_a(o)]
        ax.plot([p[0] for p in ps], [p[1] for p in ps], color=BLACK,
                lw=1.5, zorder=4)
    # open circles at neighbor-cube corners (fcc sites of adjacent cells)
    for c in sorted(circ):
        if hidden(c):
            continue
        q = proj_a(c)
        ax.plot([q[0]], [q[1]], 'o', ms=7.5, mfc='white', mec=BLACK,
                mew=1.2, zorder=2)
    # filled dots: 8 corners + 6 face centres of the central cube
    sites = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    sites += [(0.5, 0.5, 0), (0.5, 0.5, 1), (0.5, 0, 0.5), (0.5, 1, 0.5),
              (0, 0.5, 0.5), (1, 0.5, 0.5)]
    for s in sites:
        q = proj_a(s)
        ax.plot([q[0]], [q[1]], 'o', ms=6.5 if s in sites[:8] else 9,
                mfc=BLACK, mec=BLACK, zorder=6)
    ax.text(0.7, -1.75, '$(a)$', ha='center', va='top', fontsize=12)
    ax.set_xlim(-1.45, 2.85)
    ax.set_ylim(-2.15, 2.75)

    # ---------------- panel (b)
    ax = ax2
    ax.set_aspect('equal'); ax.axis('off')
    O = np.array([0., 0., 0.])
    a1 = np.array([0., .5, .5])
    a2 = np.array([.5, 0., .5])
    a3 = np.array([.5, .5, 0.])
    f = np.array([1., 1., 1.])
    # thin cube edges
    corners = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    for c in corners:
        for d in range(3):
            e = list(c); e[d] += 1
            if e[d] > 1:
                continue
            p, q = proj_b(c), proj_b(e)
            ax.plot([p[0], q[0]], [p[1], q[1]], color=BLACK, lw=0.9, zorder=2)
    # dashed face diagonals (12)
    diags = [((0, 0, 0), (1, 1, 0)), ((1, 0, 0), (0, 1, 0)),
             ((0, 0, 1), (1, 1, 1)), ((1, 0, 1), (0, 1, 1)),
             ((0, 0, 0), (1, 0, 1)), ((0, 1, 0), (1, 1, 1)),
             ((1, 0, 0), (0, 0, 1)), ((1, 1, 0), (0, 1, 1)),
             ((0, 0, 0), (0, 1, 1)), ((1, 0, 0), (1, 1, 1)),
             ((0, 1, 0), (0, 0, 1)), ((1, 1, 0), (1, 0, 1))]
    for p, q in diags:
        p, q = proj_b(p), proj_b(q)
        dline(ax, p, q, lw=0.9, dashes=(4, 3), zorder=2)
    # bold primitive rhombohedron
    rb = [(a1, a1+a2), (a2, a1+a2), (a2, a2+a3), (a3, a2+a3),
          (a1, a1+a3), (a3, a1+a3),
          (a1+a2, f), (a1+a3, f), (a2+a3, f)]
    for p, q in rb:
        p, q = proj_b(p), proj_b(q)
        ax.plot([p[0], q[0]], [p[1], q[1]], color=BLACK, lw=1.9,
                zorder=4, solid_capstyle='round')
    # bold arrows along a1, a2, a3 from the origin
    arrow(ax, proj_b(O), proj_b(a1), lw=1.9, ms=13, zorder=5)
    arrow(ax, proj_b(O), proj_b(a2), lw=1.9, ms=13, zorder=5)
    arrow(ax, proj_b(O), proj_b(a3), lw=1.9, ms=13, zorder=5)
    # open circles: 8 corners + 6 face centres
    fc = [(0.5, 0.5, 0), (0.5, 0.5, 1), (0.5, 0, 0.5), (0.5, 1, 0.5),
          (0, 0.5, 0.5), (1, 0.5, 0.5)]
    for c in corners + fc:
        q = proj_b(c)
        ax.plot([q[0]], [q[1]], 'o', ms=6.5, mfc='white', mec=BLACK,
                mew=1.1, zorder=6)
    # labels
    m = proj_b(O)*0.42 + proj_b(a1)*0.58
    ax.text(m[0]-0.17, m[1]+0.02, r'$\mathbf{a}_1$', ha='center',
            va='center', fontsize=12, zorder=6)
    ax.text(0.38, 0.21, r'$\mathbf{a}_2$', ha='center', va='center',
            fontsize=12, zorder=6)
    ax.text(0.53, 0.02, r'$\mathbf{a}_3$', ha='center', va='center',
            fontsize=12, zorder=6)
    ax.text(0.5, -0.42, '$(b)$', ha='center', va='top', fontsize=12)
    ax.set_xlim(-0.42, 1.42)
    ax.set_ylim(-0.8, 1.78)
    save(fig, 10)


# --------------------------------------------------------------- fig 11
def fig_11():
    """(a) {111} planes of the f.c.c. lattice; (b) reciprocal lattice cell."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4.9, 2.95),
                                   gridspec_kw=dict(width_ratios=[1, 1.28]))
    # ---------------- panel (a): small cube with hatched (111) planes
    ax = ax1
    ax.set_aspect('equal'); ax.axis('off')
    s = 0.78
    P = lambda p: proj_c(p) * s
    corners = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    for c in corners:
        for d in range(3):
            e = list(c); e[d] += 1
            if e[d] > 1:
                continue
            p, q = P(c), P(e)
            ax.plot([p[0], q[0]], [p[1], q[1]], color=BLACK, lw=0.9, zorder=2)
    # hatched {111} planes: x+y+z = 1 and 2
    tri1 = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    tri2 = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]
    for tri in (tri1, tri2):
        ps = [P(t) for t in tri]
        ax.add_patch(Polygon(ps, closed=True, facecolor='none',
                             edgecolor='none', hatch='/////', zorder=3))
        ps += [ps[0]]
        ax.plot([p[0] for p in ps], [p[1] for p in ps], color=BLACK,
                lw=0.7, zorder=3)
    # interplanar spacing d between the two planes (centroids)
    p1, p2 = P((1/3., 1/3., 1/3.)), P((2/3., 2/3., 2/3.))
    dv = p2 - p1
    arrow(ax, p1 + 0.12 * dv, p1 + 0.45 * dv, lw=0.9, ms=8, zorder=6)
    arrow(ax, p2 - 0.12 * dv, p2 - 0.45 * dv, lw=0.9, ms=8, zorder=6)
    mid = 0.5 * (p1 + p2)
    ax.text(mid[0] - 0.09, mid[1] + 0.06, '$d$', ha='center', fontsize=12,
            zorder=6)
    # normal arrow on top face
    t0 = P((0.5, 0.5, 1.0)); t1 = P((0.78, 0.78, 1.30))
    arrow(ax, t0, t1, lw=0.9, ms=9, zorder=6)
    # sites: 8 corners + 6 face centres
    sites = corners + [(0.5, 0.5, 0), (0.5, 0.5, 1), (0.5, 0, 0.5),
                       (0.5, 1, 0.5), (0, 0.5, 0.5), (1, 0.5, 0.5)]
    for c in sites:
        q = P(c)
        ax.plot([q[0]], [q[1]], 'o', ms=4.2, mfc=BLACK, mec=BLACK, zorder=6)
    # lattice parameter a on the right of the back vertical edge
    xa = P((1, 1, 0))[0] + 0.13
    y0, y1 = P((1, 1, 0))[1], P((1, 1, 1))[1]
    ym = 0.5 * (y0 + y1)
    arrow(ax, (xa, ym), (xa, y1), lw=0.9, ms=8)
    arrow(ax, (xa, ym), (xa, y0), lw=0.9, ms=8)
    for yv in (y0, y1):
        ax.plot([xa - 0.05, xa + 0.02], [yv, yv], color=BLACK, lw=0.9)
    ax.text(xa + 0.06, ym, '$a$', ha='left', va='center', fontsize=12)
    ax.text(0.55, -0.28, '$(a)$', ha='center', va='top', fontsize=12)
    ax.set_xlim(-0.28, 1.52)
    ax.set_ylim(-0.52, 1.32)

    # ---------------- panel (b): reciprocal cell, vectors (100) (010) (001)
    ax = ax2
    ax.set_aspect('equal'); ax.axis('off')
    s = 1.18
    P = lambda p: proj_c(p) * s
    corners = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    for c in corners:
        for d in range(3):
            e = list(c); e[d] += 1
            if e[d] > 1:
                continue
            p, q = P(c), P(e)
            ax.plot([p[0], q[0]], [p[1], q[1]], color=BLACK, lw=0.9, zorder=2)
    # filled dot at the body centre
    q = P((0.5, 0.5, 0.5))
    ax.plot([q[0]], [q[1]], 'o', ms=6.5, mfc=BLACK, mec=BLACK, zorder=6)
    # bold reciprocal vectors from the origin corner
    arrow(ax, P((0, 0, 0)), P((1, 0, 0)), lw=2.0, ms=15, zorder=5)
    arrow(ax, P((0, 0, 0)), P((0, 1, 0)), lw=2.0, ms=15, zorder=5)
    arrow(ax, P((0, 0, 0)), P((0, 0, 1)), lw=2.0, ms=15, zorder=5)
    arrow(ax, P((0, 0, 0)), P((0.5, 0.5, 0.5)), lw=2.0, ms=15, zorder=5)
    ax.text(P((0.45, 0, 0))[0], P((0.45, 0, 0))[1] - 0.11,
            r'$\mathbf{(100)}$', ha='center', va='top', fontsize=11)
    q = P((0, 0.42, 0))
    ax.text(q[0] + 0.10, q[1] - 0.05, r'$\mathbf{(010)}$', ha='left',
            va='center', fontsize=11)
    q = P((0, 0, 0.62))
    ax.text(q[0] - 0.07, q[1], r'$\mathbf{(001)}$', ha='right',
            va='center', fontsize=11)
    q = P((0.30, 0.30, 0.30))
    ax.text(q[0] - 0.02, q[1] + 0.12, r'$\mathbf{(111)}$', ha='right',
            va='bottom', fontsize=11)
    # 4*pi/a dimension on the right
    xa = P((1, 1, 0))[0] + 0.16
    yb = P((0, 0, 0))[1]
    yt = P((0, 0, 1))[1]
    for yv in (yb, yt):
        ax.plot([xa - 0.07, xa + 0.05], [yv, yv], color=BLACK, lw=1.0)
    arrow(ax, (xa, 0.5 * (yb + yt)), (xa, yt), lw=1.0, ms=9)
    arrow(ax, (xa, 0.5 * (yb + yt)), (xa, yb), lw=1.0, ms=9)
    ax.text(xa + 0.09, 0.5 * (yb + yt), r'$4\pi/a$', ha='left',
            va='center', fontsize=12)
    ax.text(0.75, -0.42, '$(b)$', ha='center', va='top', fontsize=12)
    ax.set_xlim(-0.35, 1.85)
    ax.set_ylim(-0.62, 1.45)
    save(fig, 11)


# --------------------------------------------------------------- fig 12
def fig_12():
    """Points k all reduce to k' in the one-dimensional reciprocal lattice."""
    fig, ax = plt.subplots(figsize=(4.7, 2.35))
    ax.set_aspect('auto'); ax.axis('off')
    # main axis
    ax.plot([-3.15, 4.95], [0, 0], color=BLACK, lw=1.2, zorder=2)
    # labelled ticks
    for x in (-2, -1, 1, 2, 4):
        ax.plot([x, x], [0, 0.07], color=BLACK, lw=1.1, zorder=2)
    # small companion ticks
    for x in (-1.82, 2.15, 4.15):
        ax.plot([x, x], [0, 0.045], color=BLACK, lw=1.0, zorder=2)
    # k' tick just left of the bold origin line
    ax.plot([-0.15, -0.15], [0, 0.1], color=BLACK, lw=1.1, zorder=2)
    # zone boundary verticals
    ax.plot([0, 0], [0, 0.85], color=BLACK, lw=2.4, zorder=3)
    for x in (-1, 1):
        dline(ax, (x, 0), (x, 0.8), lw=1.2, dashes=(4, 3))
    dline(ax, (3, 0), (3, 0.95), lw=1.2, dashes=(4, 3))
    # "reduced zone" brace
    brace(ax, (-1, 1.0), (1, 1.0), depth=0.13, side=-1, lw=1.2)
    ax.text(0, 1.17, 'reduced zone', ha='center', va='bottom', fontsize=10.5)
    # tick labels
    lab = [(-2.08, r'$-2\pi/a$'), (-1, r'$-\pi/a$'), (0, r'$O$'),
           (1, r'$\pi/a$'), (2, r'$2\pi/a$'), (4, r'$4\pi/a$')]
    for x, s in lab:
        ax.text(x, -0.13, s, ha='center', va='top', fontsize=10.5)
    # k labels
    for x in (-2, 2, 4):
        ax.text(x, 0.115, '$k$', ha='center', va='bottom', fontsize=12)
    ax.text(-0.22, 0.14, "$k'$", ha='right', va='bottom', fontsize=12)
    # upper g double arrow (between 2pi/a and 4pi/a, broken at 3pi/a)
    y = 0.45
    arrow(ax, (2.85, y), (2.3, y), lw=1.1, ms=10, style='-|>')
    arrow(ax, (3.15, y), (3.8, y), lw=1.1, ms=10, style='-|>')
    ax.text(2.96, y, '$g$', ha='right', va='center', fontsize=12)
    # lower g double arrow spanning the reduced zone
    y = -0.36
    arrow(ax, (-0.28, y), (-0.95, y), lw=1.1, ms=10, style='-|>')
    arrow(ax, (0.28, y), (0.95, y), lw=1.1, ms=10, style='-|>')
    ax.text(0, y, '$g$', ha='center', va='center', fontsize=12)
    ax.set_xlim(-3.35, 5.15)
    ax.set_ylim(-0.62, 1.38)
    save(fig, 12)


# --------------------------------------------------------------- fig 13
def fig_13():
    """Wave-vectors k all reduce to k', which lies in the Brillouin zone."""
    fig, ax = plt.subplots(figsize=(4.35, 3.1))
    ax.set_aspect('equal'); ax.axis('off')
    bx, by = 1.0, 0.74          # drawn lattice periods (anisotropic as original)
    ext = 0.38                  # extension of zone-edge lines past corners
    # thin grid: lines through lattice points
    for x in (-1, 0, 1):
        ax.plot([x, x], [-by - 0.5 * by, by + 0.5 * by], color=BLACK,
                lw=0.7, zorder=1)
    for y in (-by, 0, by):
        ax.plot([-1.75, 1.75], [y, y], color=BLACK, lw=0.7, zorder=1)
    # zone-edge lines (extended past the zone)
    for x in (-0.5, 0.5):
        ax.plot([x, x], [-0.5 * by - ext * by, 0.5 * by + ext * by],
                color=BLACK, lw=0.7, zorder=1)
    for y in (-0.5 * by, 0.5 * by):
        ax.plot([-0.5 - ext, 0.5 + ext], [y, y], color=BLACK, lw=0.7,
                zorder=1)
    # hatched Brillouin zone (Wigner-Seitz cell)
    ax.add_patch(Polygon([(-0.5, -0.5 * by), (0.5, -0.5 * by),
                          (0.5, 0.5 * by), (-0.5, 0.5 * by)], closed=True,
                         facecolor='none', edgecolor=BLACK, lw=0.9,
                         hatch='////', zorder=2))
    # bold reciprocal lattice vectors (heads stop short of the sites,
    # thin grid lines continue to the lattice points, as in the original)
    arrow(ax, (0, 0), (0.62 * bx, 0), lw=2.0, ms=14, zorder=5)
    arrow(ax, (0, 0), (0, 0.73 * by), lw=2.0, ms=14, zorder=5)
    ax.text(0.68, -0.12, r'$\mathbf{g}_1$', ha='left', va='center',
            fontsize=12, zorder=6)
    ax.text(0.06, 0.62, r'$\mathbf{g}_2$', ha='left', va='center',
            fontsize=12, zorder=6)
    # reduced vector k'
    kp = (0.12, -0.30)
    arrow(ax, (0, 0), kp, lw=1.8, ms=11, zorder=5)
    ax.text(kp[0] + 0.07, kp[1] - 0.05, r"$\mathbf{k}'$", ha='left',
            va='center', fontsize=12, zorder=6)
    # outer k vectors = g + k'
    kd1 = (-1 + kp[0], by + kp[1])
    kd2 = (1 + kp[0], by + kp[1])
    for kd in (kd1, kd2):
        ax.annotate('', xy=kd, xytext=(0, 0), zorder=4,
                    arrowprops=dict(arrowstyle='-|>', lw=1.0, color=BLACK,
                                    mutation_scale=11, shrinkA=0, shrinkB=0))
        ax.plot([kd[0]], [kd[1]], 'o', ms=4.5, mfc=BLACK, mec=BLACK,
                zorder=6)
        ax.text(kd[0] + 0.07, kd[1] + 0.03, '$k$', ha='left', va='center',
                fontsize=12, zorder=6)
    # dashed fold arrows from lattice points g to the k points
    for start, end in (((-1, by), kd1), ((1, by), kd2)):
        ar = matplotlib.patches.FancyArrowPatch(
            start, end, arrowstyle='-|>', mutation_scale=10, lw=1.0,
            color=BLACK, linestyle=(0, (4, 3)), shrinkA=0, shrinkB=0,
            zorder=4)
        ax.add_patch(ar)
    # lattice dots
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            ax.plot([i * bx], [j * by], 'o', ms=4.5, mfc=BLACK, mec=BLACK,
                    zorder=6)
    ax.set_xlim(-2.0, 1.85)
    ax.set_ylim(-1.45, 1.45)
    save(fig, 13)


# --------------------------------------------------------------- fig 14
def fig_14():
    """Energy of free electrons in the reduced zone."""
    fig, ax = plt.subplots(figsize=(4.8, 3.25))
    ax.set_aspect('auto'); ax.axis('off')
    e = lambda k: k * k / 9.0     # in units of eps(3pi/a)
    # horizontal axis
    ax.plot([-3.25, 3.25], [0, 0], color=BLACK, lw=1.2)
    for x, s in [(-3, r'$-3\pi/a$'), (-1, r'$-\pi/a$'), (0, r'$O$'),
                 (1, r'$\pi/a$'), (3, r'$3\pi/a$')]:
        ax.text(x, -0.055, s, ha='center', va='top', fontsize=11.5)
    ax.text(0.35, -0.055, '$k$', ha='center', va='top', fontsize=10.5)
    arrow(ax, (0.43, -0.052), (0.58, -0.052), lw=0.9, ms=8)
    # vertical lines
    for x in (-1, 1):
        ax.plot([x, x], [0, 1.02], color=BLACK, lw=0.9, zorder=1)
    for x in (-3, 3):
        dline(ax, (x, 0), (x, 1.02), lw=1.15, dashes=(5, 4))
    ax.plot([0, 0], [0, 1.04], color=BLACK, lw=0.9, zorder=1)
    arrow(ax, (0, 1.04), (0, 1.12), lw=0.9, ms=8)
    ax.text(0.07, 1.06, r'$\mathcal{E}$', ha='left', va='center',
            fontsize=13)
    # free-electron parabola: solid inside the zone, dashed outside
    xs = np.linspace(-1, 1, 200)
    ax.plot(xs, e(xs), color=BLACK, lw=1.4, zorder=3)
    for seg in (np.linspace(-3, -1, 120), np.linspace(1, 3, 120)):
        ax.plot(seg, e(seg), color=BLACK, lw=1.4, linestyle=(0, (5, 4)),
                zorder=3)
    # translated branches (reduced-zone scheme)
    xs = np.linspace(-1, 1, 200)
    ax.plot(xs, e(xs - 2), color=BLACK, lw=1.7, zorder=4)   # C -> A
    ax.plot(xs, e(xs + 2), color=BLACK, lw=1.7, zorder=4)   # A' -> B'
    # labels C, C', B, B', A, A'
    ax.text(-3.1, 1.03, "$C'$", ha='right', va='bottom', fontsize=12)
    ax.text(-1.1, 1.03, '$C$', ha='right', va='bottom', fontsize=12)
    ax.text(1.1, 1.03, "$B'$", ha='left', va='bottom', fontsize=12)
    ax.text(3.1, 1.03, '$B$', ha='left', va='bottom', fontsize=12)
    ax.text(-1.09, 0.115, "$A'$", ha='right', va='center', fontsize=12)
    ax.text(1.09, 0.115, '$A$', ha='left', va='center', fontsize=12)
    # g double arrow between pi/a and 3pi/a
    y = 0.9
    arrow(ax, (1.8, y), (1.05, y), lw=1.0, ms=9)
    arrow(ax, (2.2, y), (2.95, y), lw=1.0, ms=9)
    ax.text(2.0, y, '$g$', ha='center', va='center', fontsize=12)
    # formula
    ax.text(1.12, 0.67, r'$\mathcal{E}=\hbar^2 k^2/2m$', ha='left',
            va='center', fontsize=10)
    ax.set_xlim(-3.6, 3.75)
    ax.set_ylim(-0.17, 1.22)
    save(fig, 14)


# --------------------------------------------------------------- fig 15
def fig_15():
    """Brillouin zone covers the same area as the parallelepiped unit cell;
    contains just N allowed k-vectors."""
    fig, ax = plt.subplots(figsize=(4.6, 3.95))
    ax.set_aspect('equal'); ax.axis('off')
    e1 = np.array([1.0, 0.0])
    e2 = 0.95 * np.array([np.cos(np.radians(72)), np.sin(np.radians(72))])
    M = lambda i, j: i * e1 + j * e2
    # fine cross-hatched mesh over the crystallite
    I0, I1, J0, J1 = -2.35, 2.35, -1.8, 1.8
    for k in range(-19, 20):
        i = k / 8.0
        p0, p1 = M(i, J0), M(i, J1)
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=BLACK, lw=0.32,
                zorder=1)
    for k in range(-15, 16):
        j = k / 8.0
        p0, p1 = M(I0, j), M(I1, j)
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=BLACK, lw=0.32,
                zorder=1)
    # dashed construction: perpendicular bisectors of the four neighbours.
    # The bisectors of the b1 neighbours are drawn as short segments around
    # the zone; those of the b2 neighbours run the full length (as original).
    dline(ax, M(-0.5, -1.05), M(-0.5, 1.05), lw=0.9, dashes=(5, 4))
    dline(ax, M(0.5, -1.05), M(0.5, 1.05), lw=0.9, dashes=(5, 4))
    nperp = np.array([-e2[1], e2[0]])
    nperp /= np.hypot(*nperp)
    for j in (0.5, -0.5):
        c = M(0, j)
        p0, p1 = c - 3.1 * nperp, c + 3.1 * nperp
        dline(ax, p0, p1, lw=0.9, dashes=(5, 4))
    # long dashed diagonal through O (as in the original)
    dline(ax, M(-1.5, 1.5), M(1.5, -1.5), lw=0.9, dashes=(5, 4))
    # bold lattice axes through O (b1 row and b2 column), as in the original
    ax.plot([M(-1.85, 0)[0], M(1, 0)[0]], [M(-1.85, 0)[1], M(1, 0)[1]],
            color=BLACK, lw=1.9, zorder=4, solid_capstyle='round')
    ax.plot([M(0, -1.78)[0], M(0, 1)[0]], [M(0, -1.78)[1], M(0, 1)[1]],
            color=BLACK, lw=1.9, zorder=4, solid_capstyle='round')
    # remaining bold edges of the parallelepiped unit cell
    for p, q in [(M(1, 0), M(1, 1)), (M(1, 1), M(0, 1))]:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=BLACK, lw=1.9, zorder=4,
                solid_capstyle='round')
    # mid-edge arrowheads on the two cell edges from O
    arrow(ax, M(0.45, 0), M(0.68, 0), lw=1.9, ms=13, zorder=5)
    arrow(ax, M(0, 0.45), M(0, 0.68), lw=1.9, ms=13, zorder=5)
    ax.text(M(0.78, -0.21)[0], M(0.78, -0.21)[1], r'$2\pi\mathbf{b}_1$',
            ha='center', va='top', fontsize=12, zorder=6)
    q = M(0.24, 1.26)
    ax.text(q[0], q[1], r'$2\pi\mathbf{b}_2$', ha='left',
            va='center', fontsize=12, zorder=6)
    ax.text(-0.10, -0.12, '$O$', ha='right', va='top', fontsize=12,
            zorder=6)
    # lattice dots (3 x 3)
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            p = M(i, j)
            ax.plot([p[0]], [p[1]], 'o', ms=6, mfc=BLACK, mec=BLACK,
                    zorder=6)
    # braces marking L1 (bottom) and L2 (right)
    p0 = M(0, -1) + np.array([0.0, -0.24])
    p1 = M(1, -1) + np.array([0.0, -0.24])
    brace(ax, p0, p1, depth=0.16, side=-1, lw=1.0)
    mid = 0.5 * (p0 + p1)
    ax.text(mid[0], mid[1] - 0.32, '$L_1$', ha='center', va='top',
            fontsize=12)
    off = np.array([0.28, 0.0])
    p0 = M(1, 0) + off
    p1 = M(1, 1) + off
    brace(ax, p0, p1, depth=0.16, side=-1, lw=1.0)
    mid = 0.5 * (p0 + p1)
    ax.text(mid[0] + 0.26, mid[1], '$L_2$', ha='left', va='center',
            fontsize=12)
    ax.set_xlim(-2.6, 3.05)
    ax.set_ylim(-2.25, 2.15)
    save(fig, 15)


if __name__ == '__main__':
    for fn in (fig_9, fig_10, fig_11, fig_12, fig_13, fig_14, fig_15):
        fn()
