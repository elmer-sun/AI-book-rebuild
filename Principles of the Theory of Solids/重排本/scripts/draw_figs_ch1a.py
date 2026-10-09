# -*- coding: utf-8 -*-
"""
Redraw Ziman, Principles of the Theory of Solids (2nd ed.), Chapter 1, Figs. 1-8.
Black-and-white textbook-style vector figures.

Outputs (written immediately after each figure is drawn):
    figures/fig_{n}.pdf
    figures/preview/fig_{n}.png
"""
import os
import itertools

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE, 'figures')
PREV_DIR = os.path.join(FIG_DIR, 'preview')
os.makedirs(PREV_DIR, exist_ok=True)


def save(fig, key):
    """Save one figure to PDF + preview PNG immediately."""
    fig.savefig(os.path.join(FIG_DIR, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV_DIR, 'fig_%s.png' % key),
                bbox_inches='tight', pad_inches=0.03, dpi=200)
    plt.close(fig)
    print('saved fig_%s' % key)


def arrow(ax, p0, p1, lw=1.3, ms=11):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


# ======================================================================
# Fig. 1  2-D point lattice with basis vectors a1, a2 and translation l
# ======================================================================
def fig_1():
    fig, ax = plt.subplots(figsize=(3.6, 1.95))
    dx, dy = 1.0, 0.47          # rectangular lattice spacings (as in original)
    for i in range(4):
        for j in range(4):
            ax.add_patch(Circle((i * dx, j * dy), 0.026, fc='k', ec='k'))
    O = (0.0, 0.0)
    arrow(ax, O, (0.80 * dx, 0.0))
    arrow(ax, O, (0.0, 0.80 * dy))
    arrow(ax, O, (0.95 * dx, 0.90 * dy))          # l : a1 + 2 a2
    ax.text(-0.22 * dx, -0.17 * dy, r'$O$', fontsize=12)
    ax.text(0.38 * dx, -0.24 * dy, r'$\mathbf{a}_1$')
    ax.text(-0.36 * dx, 0.36 * dy, r'$\mathbf{a}_2$')
    ax.text(0.26 * dx, 0.55 * dy, r'$\mathbf{\mathit{l}}$', fontsize=12)
    ax.set_xlim(-0.38, 3.15)
    ax.set_ylim(-0.26, 3 * dy + 0.16)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 1)


# ======================================================================
# Fig. 2  Alternative unit cells (solid grid + shifted dashed cells,
#         one hatched atom per cell)
# ======================================================================
def fig_2():
    fig, ax = plt.subplots(figsize=(3.6, 2.1))
    a, b = 1.0, 0.8                       # cell size (x, y)
    xs = [i * a for i in range(5)]        # solid verticals
    ys = [j * b for j in range(4)]        # solid horizontals
    # solid grid
    for x in xs:
        ax.plot([x, x], [0.0, 3 * b], color='k', lw=1.0)
    for y in ys:
        ax.plot([0.0, 4 * a], [y, y], color='k', lw=1.0)
    # dashed grid: verticals through the large dots, horizontals shifted up
    for i in range(5):
        x = (i + 0.5) * a
        ax.plot([x, x], [-0.14, 3 * b + 0.16], color='k', lw=1.0,
                ls=(0, (5, 4)))
    for j in range(4):
        y = j * b + 0.16
        ax.plot([-0.16, 4 * a + 0.16], [y, y], color='k', lw=1.0,
                ls=(0, (5, 4)))
    # small dots at solid intersections
    for x in xs:
        for y in ys:
            ax.add_patch(Circle((x, y), 0.024, fc='k', ec='k'))
    # large dots midway along the horizontal lines (on the dashed verticals)
    for i in range(4):
        for j in range(4):
            ax.add_patch(Circle(((i + 0.5) * a, j * b), 0.044, fc='k',
                                ec='k'))
    # hatched atoms, one per cell, clear of every line
    for i in range(4):
        for j in range(3):
            ax.add_patch(Circle(((i + 0.72) * a, j * b + 0.42), 0.125,
                                fc='white', ec='k', lw=1.1, hatch='///'))
    ax.set_xlim(-0.28, 4.72)
    ax.set_ylim(-0.24, 3 * b + 0.26)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 2)


# ======================================================================
# Fig. 3  Wigner-Seitz cell of an oblique (~triangular) 2-D lattice
# ======================================================================
def fig_3():
    fig, ax = plt.subplots(figsize=(4.0, 3.0))
    s = 1.12                                   # lattice constant
    a1 = np.array([s, 0.0])
    a2 = np.array([0.5 * s, 0.866 * s])
    C = np.array([0.0, 0.0])                   # WS centre

    # --- dashed conventional cell (above C) and its extensions ---------
    dash = dict(color='k', lw=1.0, ls=(0, (5, 4)))
    A, B = C - a1, C                            # mid row (left of C)
    T1, T2 = C - a1 + a2, C + a2                # top edge of dashed cell
    ax.plot([A[0] - 1.9 * s, B[0]], [A[1], B[1]], **dash)         # mid row
    ax.plot([B[0], B[0] + a1[0]], [B[1], B[1]], **dash)           # C -> C+a1
    ax.plot([T1[0], T2[0]], [T1[1], T2[1]], **dash)               # top edge
    L0 = C - a1 - a2                                              # lower-left
    ax.plot([L0[0], T1[0]], [L0[1], T1[1]], **dash)               # long a2 edge
    ax.plot([L0[0], (C + a1 - a2)[0]], [L0[1], (C + a1 - a2)[1]],
            **dash)                                               # bottom row
    # dashed construction rays through C: along a2 (also a cell edge),
    # along a1 and along a1-a2
    ax.plot([C[0] - 1.6 * a2[0], C[0] + 2.1 * a2[0]],
            [C[1] - 1.6 * a2[1], C[1] + 2.1 * a2[1]], **dash)
    fine = dict(color='k', lw=0.9, ls=(0, (2.5, 2.5)))
    ax.plot([C[0] - 2.1 * s, C[0] + 2.1 * s], [C[1], C[1]], **fine)
    u = (a1 - a2) / s
    ax.plot([C[0] - 1.55 * u[0] * s, C[0] + 1.55 * u[0] * s],
            [C[1] - 1.55 * u[1] * s, C[1] + 1.55 * u[1] * s], **fine)

    # --- shaded Wigner-Seitz hexagon ----------------------------------
    R = s / np.sqrt(3.0)                       # circumradius
    hexv = [C + R * np.array([np.cos(np.radians(30 + 60 * k)),
                              np.sin(np.radians(30 + 60 * k))])
            for k in range(6)]
    ax.add_patch(Polygon(hexv, closed=True, fc='0.90', ec='none', zorder=1))

    # --- perpendicular-bisector strokes (extend past hexagon) ----------
    t = 0.46 * s
    for u in (a1, a2, a1 - a2):
        for sgn in (1, -1):
            m = C + sgn * u / 2.0
            w = np.array([-u[1], u[0]]) / np.linalg.norm(u)   # unit perp
            ax.plot([m[0] - t * w[0], m[0] + t * w[0]],
                    [m[1] - t * w[1], m[1] + t * w[1]],
                    color='k', lw=1.5, solid_capstyle='round', zorder=3)
    ax.add_patch(Polygon(hexv, closed=True, fc='none', ec='k', lw=1.7,
                         zorder=4))

    # --- lattice sites: hatched atoms with a small dot on top ----------
    for i in range(-2, 3):
        for j in range(-1, 3):
            p = C + i * a1 + j * a2
            if -2.5 * s < p[0] < 2.9 * s and -1.45 * s < p[1] < 1.5 * s:
                ax.add_patch(Circle(tuple(p), 0.10 * s, fc='white',
                                    ec='k', lw=1.0, hatch='///', zorder=5))
                ax.add_patch(Circle(tuple(p), 0.024, fc='k', ec='k',
                                    zorder=6))

    # --- conventional cell (solid, below C) with a1, a2 arrows ----------
    bl = C + a1 - a2
    br = C + 2 * a1 - a2
    tl = C + a1
    tr = C + 2 * a1
    lw = 1.6
    ax.plot([bl[0], br[0]], [bl[1], br[1]], color='k', lw=lw, zorder=4)
    ax.plot([tl[0], tr[0]], [tl[1], tr[1]], color='k', lw=lw, zorder=4)
    ax.plot([tr[0], br[0]], [tr[1], br[1]], color='k', lw=lw, zorder=4)
    ax.plot([bl[0], tl[0]], [bl[1], tl[1]], color='k', lw=lw, zorder=4)
    mid = bl + 0.5 * a1
    arrow(ax, (mid[0] - 0.17, mid[1]), (mid[0] + 0.17, mid[1]), lw=1.6)
    ax.text(mid[0] - 0.06 * s, mid[1] - 0.34 * s, r'$\mathbf{a}_1$')
    m2 = bl + 0.62 * a2
    a2u = a2 / np.linalg.norm(a2)                     # unit along the edge
    arrow(ax, tuple(m2 - 0.15 * a2u * s), tuple(m2 + 0.15 * a2u * s), lw=1.6)
    ax.text(m2[0] + 0.16 * s, m2[1] - 0.04 * s, r'$\mathbf{a}_2$')

    ax.set_xlim(-2.15 * s, 2.75 * s)
    ax.set_ylim(-1.62 * s, 1.72 * s)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 3)


# ======================================================================
# 3-D helpers (shared by Figs. 4 and 5)
# ----------------------------------------------------------------------
# Oblique axonometric projection: +x right, +y receding up-right, +z up.
def proj(x, y, z):
    return (x + 0.62 * y, 0.33 * y + z)


# Direction from scene towards the viewer (consistent with proj()).
VVIEW = np.array([0.62, -1.0, 0.33])


def depth(p):
    """Larger = farther from the viewer (painter's algorithm key)."""
    return 10.0 * p[1] - p[0] - p[2]


def cube_edges(p0, p1):
    """The 12 edges of an axis-aligned box with opposite corners p0, p1."""
    edges = []
    for k in range(3):
        others = [i for i in range(3) if i != k]
        for v0 in (p0[others[0]], p1[others[0]]):
            for v1 in (p0[others[1]], p1[others[1]]):
                a = [None, None, None]
                b = [None, None, None]
                a[others[0]] = b[others[0]] = v0
                a[others[1]] = b[others[1]] = v1
                a[k], b[k] = p0[k], p1[k]
                edges.append((tuple(a), tuple(b)))
    return edges


def draw_grid(ax, ranges, lw=0.8):
    """Thin cubic lattice lines through the given coordinate values."""
    xs, ys, zs = ranges
    lines = []
    for x in xs:
        for y in ys:
            lines.append(((x, y, zs[0]), (x, y, zs[-1])))
    for y in ys:
        for z in zs:
            lines.append(((xs[0], y, z), (xs[-1], y, z)))
    for x in xs:
        for z in zs:
            lines.append(((x, ys[0], z), (x, ys[-1], z)))
    for p, q in lines:
        pp, qq = proj(*p), proj(*q)
        ax.plot([pp[0], qq[0]], [pp[1], qq[1]], color='k', lw=lw)


def TO_faces(center):
    """Truncated octahedron inscribed in cube [c-1,c+1]^3.
    Returns list of (vertices, outward normal, kind)."""
    c = np.array(center, float)
    verts = set()
    for p in set(itertools.permutations((1, 2, 0))):
        for sx in (1, -1):
            for sy in (1, -1):
                for sz in (1, -1):
                    verts.add((sx * p[0], sy * p[1], sz * p[2]))
    verts = [np.array(v, float) for v in verts]
    faces = []
    normals = []
    for ax_ in range(3):
        for sgn in (1, -1):
            n = np.zeros(3)
            n[ax_] = sgn
            normals.append((n, 'square'))
    for sg in itertools.product((1, -1), repeat=3):
        normals.append((np.array(sg, float), 'hex'))
    for n, kind in normals:
        vals = [np.dot(v, n) for v in verts]
        mx = max(vals)
        fv = [v for v, val in zip(verts, vals) if abs(val - mx) < 1e-6]
        n2 = n / np.linalg.norm(n)
        tmp = np.array([0.0, 0.0, 1.0])
        if abs(np.dot(tmp, n2)) > 0.9:
            tmp = np.array([1.0, 0.0, 0.0])
        e1 = np.cross(n2, tmp)
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(n2, e1)
        ang = [np.arctan2(np.dot(v, e2), np.dot(v, e1)) for v in fv]
        fv = np.array([v for _, v in sorted(zip(ang, fv))])
        faces.append((c + 0.5 * fv, n2, kind))
    return faces


def draw_TO(ax, center, hatched=(), lw=1.4, plain_lw=1.0):
    """Draw a truncated octahedron; only front faces, sorted back-to-front.
    `hatched` is a set of kinds to fill with hatching ('hex', 'square')."""
    faces = TO_faces(center)
    vis = []
    for vv, n, kind in faces:
        if np.dot(n, VVIEW) > 0.05:
            vis.append((depth(np.mean(vv, axis=0)), vv, kind))
    vis.sort(key=lambda t: -t[0])                 # far first
    for _, vv, kind in vis:
        pts = [proj(*v) for v in vv]
        if kind in hatched:
            ax.add_patch(Polygon(pts, closed=True, fc='white', ec='k',
                                 lw=lw, hatch='///' if kind == 'hex' else 'xx',
                                 zorder=3))
        else:
            ax.add_patch(Polygon(pts, closed=True, fc='white', ec='k',
                                 lw=plain_lw, zorder=3))


# ======================================================================
# Fig. 4  b.c.c. lattice: (a) cubic cell, (b) generators, (c) WS cell
# ======================================================================
def fig_4():
    fig = plt.figure(figsize=(3.5, 8.6))
    gs = fig.add_gridspec(3, 1, height_ratios=[1.0, 1.15, 0.92],
                          hspace=0.16)

    # ---------------- (a) cubic unit cell, atoms on all b.c.c. points --
    ax = fig.add_subplot(gs[0])
    xs, ys, zs = list(range(4)), list(range(3)), list(range(3))
    draw_grid(ax, (xs, ys, zs), lw=0.8)
    # star: lines from one body centre to the 8 corners of its cube
    cstar = (2.5, 1.5, 1.5)
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                p = (2 + dx, 1 + dy, 1 + dz)
                ax.plot([proj(*cstar)[0], proj(*p)[0]],
                        [proj(*cstar)[1], proj(*p)[1]], color='k', lw=0.8)
    # thick unit cell (0..1)^3
    for p, q in cube_edges((0, 0, 0), (1, 1, 1)):
        pp, qq = proj(*p), proj(*q)
        ax.plot([pp[0], qq[0]], [pp[1], qq[1]], color='k', lw=2.3)
    # atoms
    small = [(i + 0.5, j + 0.5, k + 0.5) for i in range(3) for j in range(2)
             for k in range(2)]
    corners = [(x, y, z) for x in xs for y in ys for z in zs]
    corners.sort(key=depth, reverse=True)
    thick = set(itertools.product((0, 1), repeat=3))
    for p in corners:
        fc = '0.75' if p in thick else 'white'
        ax.add_patch(Circle(proj(*p), 0.085, fc=fc, ec='k', lw=1.0, zorder=7))
    for p in sorted(small, key=depth, reverse=True):
        ax.add_patch(Circle(proj(*p), 0.052, fc='white', ec='k', lw=0.9,
                            zorder=7))
    # a_x, a_y, a_z arrows on the thick cell
    O = proj(0, 0, 0)
    arrow(ax, O, proj(0.85, 0, 0), lw=2.0, ms=14)
    ax.text(proj(0.38, 0, 0)[0] - 0.04, O[1] - 0.26, r'$\mathbf{a}_x$')
    arrow(ax, O, proj(0, 0.72, 0), lw=2.0, ms=14)
    ax.text(proj(0, 0.80, 0)[0] + 0.09, proj(0, 0.72, 0)[1] - 0.05,
            r'$\mathbf{a}_y$')
    arrow(ax, O, proj(0, 0, 0.85), lw=2.0, ms=14)
    ax.text(O[0] - 0.36, proj(0, 0, 0.8)[1] - 0.06, r'$\mathbf{a}_z$')
    ax.set_xlim(-0.62, 4.45)
    ax.set_ylim(-0.62, 3.05)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(0.52, 0.0, '$(a)$', transform=ax.transAxes)

    # ---------------- (b) generators of the Bravais lattice ------------
    ax = fig.add_subplot(gs[1])
    grid = (list(range(0, 7, 2)), list(range(0, 7, 2)), list(range(0, 7, 2)))
    draw_grid(ax, grid, lw=0.7)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                p = (2 * i + 1, 2 * j + 1, 2 * k + 1)
                ax.add_patch(Circle(proj(*p), 0.10, fc='white', ec='k',
                                    lw=0.8, zorder=7))
    corners = [(x, y, z) for x in grid[0] for y in grid[1] for z in grid[2]]
    for p in sorted(corners, key=depth, reverse=True):
        ax.add_patch(Circle(proj(*p), 0.13, fc='white', ec='k', lw=1.0,
                            zorder=7))
    # primitive (rhombohedral) cell
    P0 = np.array([2.0, 2.0, 2.0])
    e1 = np.array([-1.0, 1.0, 1.0])
    e2 = np.array([1.0, -1.0, 1.0])
    e3 = np.array([1.0, 1.0, -1.0])
    ctr = P0 + (e1 + e2 + e3) / 2.0
    cornerlist = [P0, P0 + e1, P0 + e2, P0 + e3,
                  P0 + e1 + e2, P0 + e1 + e3, P0 + e2 + e3,
                  P0 + e1 + e2 + e3]
    # hidden edges: the 3 meeting at the farthest vertex (drawn dashed on
    # top, as in the original)
    far = max(cornerlist, key=depth)
    gens = [e1, e2, e3]
    hidden = []
    for v in cornerlist:
        d = np.array(v) - np.array(far)
        if any(np.allclose(d, g) or np.allclose(d, -g) for g in gens):
            hidden.append((far, v))
    # white faces to occlude, back to front, then visible edges thick
    faces = []
    for i, (u, v) in enumerate(((e1, e2), (e1, e3), (e2, e3))):
        w = [g for g in gens if g is not u and g is not v][0]
        for o in (P0, P0 + w):
            quad = [o, o + u, o + u + v, o + v]
            nrm = np.cross(u, v)
            if np.dot(nrm, np.mean(quad, axis=0) - ctr) < 0:
                nrm = -nrm
            faces.append((depth(np.mean(quad, axis=0)), quad, nrm))
    faces.sort(key=lambda t: -t[0])
    for _, quad, nrm in faces:
        if np.dot(nrm, VVIEW) <= 0.03:
            continue
        pts = [proj(*v) for v in quad]
        ax.add_patch(Polygon(pts, closed=True, fc='white', ec='none',
                             zorder=5))
    for _, quad, nrm in faces:
        if np.dot(nrm, VVIEW) <= 0.03:
            continue
        pts = [proj(*v) for v in quad] + [proj(*quad[0])]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color='k', lw=2.2,
                zorder=6)
    # dashed hidden edges on top of the faces, then solid vertex dots
    for fa, v in hidden:
        pp, qq = proj(*fa), proj(*v)
        ax.plot([pp[0], qq[0]], [pp[1], qq[1]], color='k', lw=2.0,
                ls=(0, (5, 4)), zorder=7)
    # solid dots at the cell vertices
    for v in cornerlist:
        ax.add_patch(Circle(proj(*v), 0.12, fc='k', ec='k', zorder=8))
    # arrows a1, a2, a3 from P0
    tip1 = P0 + 0.72 * e1
    arrow(ax, proj(*P0), proj(*tip1), lw=2.0, ms=14)
    ax.text(proj(*tip1)[0] - 0.58, proj(*tip1)[1] + 0.06, r'$\mathbf{a}_1$')
    tip2 = P0 + 0.72 * e2
    arrow(ax, proj(*P0), proj(*tip2), lw=2.0, ms=14)
    ax.text(proj(*tip2)[0] + 0.14, proj(*tip2)[1] - 0.12, r'$\mathbf{a}_2$')
    tip3 = P0 + 0.72 * e3
    arrow(ax, proj(*P0), proj(*tip3), lw=2.0, ms=14)
    ax.text(proj(*tip3)[0] + 0.16, proj(*tip3)[1] - 0.34, r'$\mathbf{a}_3$')
    ax.set_xlim(-0.15, 9.05)
    ax.set_ylim(-0.55, 8.35)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(0.52, 0.0, '$(b)$', transform=ax.transAxes)

    # ---------------- (c) Wigner-Seitz cell of the b.c.c. lattice ------
    ax = fig.add_subplot(gs[2])
    for p, q in cube_edges((0, 0, 0), (2, 2, 2)):
        pp, qq = proj(*p), proj(*q)
        ax.plot([pp[0], qq[0]], [pp[1], qq[1]], color='k', lw=0.9)
    cen = (1.0, 1.0, 1.0)
    # 3-fold axes first (they get covered by the cell faces, as in the
    # original: only the parts outside the polyhedron remain visible)
    for d in ((0, 0, 0), (2, 2, 2), (2, 2, 0), (0, 0, 2)):
        ax.plot([proj(*cen)[0], proj(*d)[0]],
                [proj(*cen)[1], proj(*d)[1]], color='k', lw=0.8, zorder=2)
    draw_TO(ax, cen, hatched=('hex',), lw=1.5)
    ax.add_patch(Circle(proj(*cen), 0.09, fc='k', ec='k', zorder=8))
    for p in itertools.product((0, 2), repeat=3):
        ax.add_patch(Circle(proj(*p), 0.11, fc='k', ec='k', zorder=8))
    ax.set_xlim(-0.35, 3.85)
    ax.set_ylim(-0.62, 3.25)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(0.52, 0.0, '$(c)$', transform=ax.transAxes)

    save(fig, 4)


# ======================================================================
# Fig. 5  Stacking of the Wigner-Seitz cells of the b.c.c. lattice
# ======================================================================
def fig_5():
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    draw_grid(ax, (list(range(0, 7, 2)), list(range(0, 5, 2)),
                   list(range(0, 5, 2))), lw=0.7)
    # back cell plain, two front cells hatched; painter order by depth
    cells = [(4, 2, 2), (2, 2, 2), (3, 3, 1)]
    cells.sort(key=depth, reverse=True)
    for i, c in enumerate(cells):
        if i == 0:
            draw_TO(ax, c, hatched=(), lw=0.9, plain_lw=0.9)
        else:
            draw_TO(ax, c, hatched=('hex',), lw=1.4)
    # lattice dots on top for clarity
    for x in range(0, 7, 2):
        for y in range(0, 5, 2):
            for z in range(0, 5, 2):
                ax.add_patch(Circle(proj(x, y, z), 0.07, fc='k', ec='k',
                                    zorder=8))
    ax.set_xlim(-0.35, 9.1)
    ax.set_ylim(-0.95, 5.85)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 5)


# ======================================================================
# Fig. 6  Multiply periodic function (contour blobs around atoms)
# ======================================================================
def rounded_hex(r, rounds=2):
    """Rounded hexagon (pointy left-right), nominal 'radius' r."""
    pts = np.array([[r * np.cos(np.radians(60 * k)),
                     r * np.sin(np.radians(60 * k))] for k in range(6)])
    for _ in range(rounds):
        new = []
        n = len(pts)
        for i in range(n):
            p0, p1 = pts[i], pts[(i + 1) % n]
            new.append(0.78 * p0 + 0.22 * p1)
            new.append(0.22 * p0 + 0.78 * p1)
        pts = np.array(new)
    return pts / (0.91 ** rounds)          # compensate corner-cutting


def atom(ax, cx, cy):
    ax.add_patch(Circle((cx, cy), 0.026, fc='white', ec='k', lw=0.9))
    for r in (0.075, 0.13, 0.185, 0.245):
        ax.add_patch(Circle((cx, cy), r, fc='none', ec='k', lw=0.9))
    hexpts = rounded_hex(0.33)
    ax.plot(hexpts[:, 0] + cx, hexpts[:, 1] + cy, color='k', lw=1.0)


def fig_6():
    fig, ax = plt.subplots(figsize=(3.7, 1.75))
    dx, dy = 0.70, 0.585
    for j, yrow in enumerate((dy / 2, -dy / 2)):
        off = 0.0 if j == 0 else dx / 2
        i = -1
        while off + i * dx < 3.2:
            atom(ax, off + i * dx, yrow)
            i += 1
    ax.set_xlim(-0.42, 2.62)
    ax.set_ylim(-dy / 2 - 0.375, dy / 2 + 0.375)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 6)


# ======================================================================
# Fig. 7  One-dimensional periodic function
# ======================================================================
def fig_7():
    fig, ax = plt.subplots(figsize=(3.6, 1.9))
    x = np.linspace(-0.55, 2.75, 1600)
    xr = np.mod(x, 1.0)
    dashed = 0.32 + 0.27 * np.cos(2 * np.pi * (x - 0.32))
    solid = (0.28 + 0.20 * np.cos(2 * np.pi * (x - 0.15))
             + 0.38 * np.exp(-((xr - 0.40) / 0.030) ** 2)
             + 0.14 * np.exp(-((xr - 0.52) / 0.055) ** 2))
    ax.plot(x, dashed, color='k', lw=1.0, ls=(0, (4, 3)))
    ax.plot(x, solid, color='k', lw=1.5)
    # lattice points and the period a
    for i in range(3):
        ax.add_patch(Circle((i, -0.44), 0.028, fc='k', ec='k'))
    for i in (0, 1):
        ax.plot([i, i], [-0.52, -0.68], color='k', lw=1.0)
    ax.annotate('', xy=(1.0, -0.60), xytext=(0.0, -0.60),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.0,
                                mutation_scale=9))
    ax.text(0.5, -0.53, r'$a$', fontsize=12, ha='center')
    ax.set_xlim(-0.62, 2.85)
    ax.set_ylim(-0.74, 1.06)
    ax.axis('off')
    save(fig, 7)


# ======================================================================
# Fig. 8  The reciprocal-lattice construction
# ======================================================================
def fig_8():
    fig, ax = plt.subplots(figsize=(3.7, 3.1))
    n = np.array([3.0, 2.0]) / np.sqrt(13.0)     # unit normal (along g)
    # lattice dots
    for i in range(7):
        for j in range(6):
            ax.add_patch(Circle((i, j), 0.045, fc='k', ec='k'))
    # dashed lattice planes 3x+2y = 7 (through l), 14 (through l''),
    # 21 (a third parallel plane)
    dpar = np.array([2.0, -3.0]) / np.sqrt(13.0)
    for c in (7.0, 14.0, 21.0):
        p0 = np.array([c / 3.0, 0.0]) - 8.0 * dpar
        p1 = np.array([c / 3.0, 0.0]) + 8.0 * dpar
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color='k', lw=1.0,
                ls=(0, (6, 4)))
    # arrows l, l', l'' from the origin
    origin = (0.0, 0.0)
    arrow(ax, origin, (0.90, 1.80), lw=1.6, ms=12)
    ax.text(0.48, 1.72, r'$\mathbf{\mathit{l}}$', fontsize=12)
    arrow(ax, origin, (2.78, 1.85), lw=1.6, ms=12)
    ax.text(1.70, 1.50, r'$\mathbf{\mathit{l}}^{\prime}$', fontsize=12)
    arrow(ax, origin, (3.85, 0.96), lw=1.6, ms=12)
    ax.text(2.60, 0.58, r'$\mathbf{\mathit{l}}^{\prime\prime}$',
            fontsize=12)
    # g arrow, normal to the planes, drawn crossing the lattice
    g0 = np.array([0.75, -0.85])
    g1 = g0 + 5.0 * n
    arrow(ax, tuple(g0), tuple(g1), lw=1.6, ms=12)
    ax.text(g1[0] + 0.10, g1[1] + 0.05, r'$\mathbf{g}$', fontsize=12)
    # spacing arrows d (one interplanar gap) and d'' (two gaps), both
    # starting on the first dashed plane
    gap = 7.0 / np.sqrt(13.0)
    pA = np.array([0.85, (7.0 - 3 * 0.85) / 2.0])   # point on plane 7
    pB = pA + gap * n                               # one gap -> plane 14
    ax.annotate('', xy=tuple(pB), xytext=tuple(pA),
                arrowprops=dict(arrowstyle='<->', color='k', lw=0.9,
                                mutation_scale=9))
    mid1 = 0.5 * (pA + pB)
    ax.text(mid1[0] - 0.46, mid1[1] + 0.30, r'$\mathbf{\mathit{d}}$',
            fontsize=12)
    base2 = np.array([0.30, (7.0 - 3 * 0.30) / 2.0])  # point on plane 7
    pE = base2 + 2 * gap * n
    ax.annotate('', xy=tuple(pE), xytext=tuple(base2),
                arrowprops=dict(arrowstyle='<->', color='k', lw=0.9,
                                mutation_scale=9))
    mid2 = 0.5 * (base2 + pE)
    ax.text(mid2[0] - 0.58, mid2[1] + 0.18,
            r'$\mathbf{\mathit{d}}^{\prime\prime}$', fontsize=12)
    ax.set_xlim(-1.05, 6.35)
    ax.set_ylim(-1.35, 5.65)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 8)


# ----------------------------------------------------------------------
if __name__ == '__main__':
    for f in (fig_1, fig_2, fig_3, fig_4, fig_5, fig_6, fig_7, fig_8):
        f()
    print('all done')
