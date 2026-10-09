# -*- coding: utf-8 -*-
"""Redraw Chapter 1 figures of Carroll, Spacetime and Geometry
as black-and-white textbook-style vector graphics.

Figures: 1.1 - 1.8 (Special Relativity and Flat Spacetime).
Output:  figures/fig_<key>.pdf  and  figures/preview/fig_<key>.png
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Ellipse, Polygon

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVIEW = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVIEW, exist_ok=True)


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def save_fig(key, fig):
    fig.savefig(os.path.join(FIGDIR, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREVIEW, 'fig_%s.png' % key),
                dpi=200, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


def arrow(ax, p0, p1, lw=1.2, ms=13, color='k', style='-|>', zorder=6):
    """straight arrow via annotate; p0,p1 = (x, y)"""
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0),
                zorder=zorder)


def catmull_rom(points, n=24, closed=False):
    """Catmull-Rom spline through `points`; returns dense (N,2) array."""
    pts = np.asarray(points, float)
    if closed:
        idx = lambda i: pts[i % len(pts)]
        segs = len(pts)
    else:
        pts = np.vstack([pts[0], pts, pts[-1]])
        idx = lambda i: pts[i]
        segs = len(pts) - 3
    out = []
    for i in range(segs):
        p0, p1, p2, p3 = idx(i), idx(i + 1), idx(i + 2), idx(i + 3)
        t = np.linspace(0.0, 1.0, n, endpoint=False)[:, None]
        q = 0.5 * (2 * p1 + (-p0 + p2) * t
                   + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                   + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)
        out.append(q)
    out = np.vstack(out)
    if not closed:
        out = np.vstack([out, idx(segs + 2)])
    return out


def brace(ax, p0, p1, depth=0.16, side=1, color='k', lw=1.0, zorder=5):
    """Curly brace from p0 to p1, bulging to the side (side=+1 -> left of
    the p0->p1 direction)."""
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    d = p1 - p0
    L = float(np.hypot(*d))
    u = d / L
    v = np.array([-u[1], u[0]]) * side
    a = depth

    def T(f, b):
        return p0 + u * (f * L) + v * b

    verts = [T(0.0, 0.0)]
    codes = [Path.MOVETO]

    def C(*pts):
        verts.extend(pts)
        codes.extend([Path.CURVE4] * 3)

    C(T(0.005, -0.28 * a), T(0.05, -0.52 * a), T(0.13, -0.55 * a))
    C(T(0.24, -0.58 * a), T(0.34, -0.52 * a), T(0.50, -a))
    C(T(0.66, -0.52 * a), T(0.76, -0.58 * a), T(0.87, -0.55 * a))
    C(T(0.95, -0.52 * a), T(0.995, -0.28 * a), T(1.0, 0.0))
    ax.add_patch(PathPatch(Path(verts, codes), fill=False, edgecolor=color,
                           lw=lw, zorder=zorder))


def pointer(ax, p0, p1, color='0.45', lw=0.7, zorder=4):
    """thin pointer line used by labels"""
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, lw=lw, zorder=zorder)


def light_cone(ax, x0, y0, a=0.45, h=0.68, ry=0.14, lw=0.7):
    """double light cone (hourglass) centred at its apex (x0,y0);
    drawn with elliptical rims for a 3-D look, grey shading."""
    th = np.linspace(0, 2 * np.pi, 100)
    # lower cone
    ax.add_patch(Polygon([(x0, y0), (x0 - a, y0 - h), (x0 + a, y0 - h)],
                         closed=True, facecolor='0.80', edgecolor='none',
                         zorder=3))
    ax.add_patch(Ellipse((x0, y0 - h), 2 * a, 2 * ry,
                         facecolor='0.88', edgecolor='k', lw=lw, zorder=3))
    # upper cone
    ax.add_patch(Polygon([(x0, y0), (x0 - a, y0 + h), (x0 + a, y0 + h)],
                         closed=True, facecolor='0.86', edgecolor='none',
                         zorder=3))
    ax.add_patch(Ellipse((x0, y0 + h), 2 * a, 2 * ry,
                         facecolor='0.80', edgecolor='k', lw=lw, zorder=3))
    # silhouette edges
    ax.plot([x0 - a, x0, x0 + a], [y0 + h, y0, y0 + h], color='k', lw=lw,
            zorder=4)
    ax.plot([x0 - a, x0, x0 + a], [y0 - h, y0, y0 - h], color='k', lw=lw,
            zorder=4)


# ----------------------------------------------------------------------
# Figure 1.1  Newtonian spacetime: absolute slicing, particle worldline
# ----------------------------------------------------------------------
def fig_1_1():
    fig, ax = plt.subplots(figsize=(4.2, 3.5))
    ax.set_xlim(0.4, 10.9)
    ax.set_ylim(-0.1, 8.2)
    ax.set_aspect('equal')
    ax.axis('off')

    # t axis
    arrow(ax, (2.2, 0.25), (2.2, 7.8), lw=1.1, ms=12)
    ax.text(2.5, 7.55, r'$t$', fontsize=12)

    # the three "spaces" (parallelograms, oblique projection)
    W, S, H = 5.2, 1.4, 1.55
    for T in (6.2, 4.05, 1.9):
        L = 3.0
        poly = [(L, T), (L + W, T), (L + W - S, T - H), (L - S, T - H)]
        ax.add_patch(Polygon(poly, closed=True, facecolor='0.87',
                             edgecolor='0.75', lw=0.5, zorder=1))

    # particle worldline (smooth curve through the three slices)
    wl_pts = [(7.95, 0.15), (7.6, 0.9), (7.3, 1.45), (7.05, 2.4),
              (6.88, 3.3), (7.02, 3.72), (7.3, 4.5), (7.55, 5.3),
              (7.42, 5.95), (7.38, 6.7)]
    wl = catmull_rom(wl_pts, n=30)
    ax.plot(wl[:, 0], wl[:, 1], color='k', lw=2.0, zorder=5)
    arrow(ax, wl[-3], wl[-1] + (0.0, 0.32), lw=2.0, ms=17, zorder=5)

    # dots where the worldline pierces the slices
    for p in [(7.28, 1.42), (7.02, 3.72), (7.46, 5.62)]:
        ax.plot(*p, marker='o', ms=4.5, color='k', zorder=6)

    # small x,y,z axes drawn on the middle slice (two arrows crossing)
    arrow(ax, (4.35, 3.42), (5.45, 3.35), lw=1.0, ms=10)
    arrow(ax, (4.45, 3.28), (5.0, 4.2), lw=1.0, ms=10)

    # labels
    ax.text(3.0, 6.85, 'particle worldline', fontsize=10.5)
    pointer(ax, (5.62, 6.92), (7.28, 6.42))

    ax.text(8.05, 4.28, r'$x, y, z$', fontsize=11)
    pointer(ax, (8.0, 4.1), (7.7, 3.35))

    ax.text(8.15, 2.92, 'space at a fixed time', fontsize=10.5)
    pointer(ax, (8.1, 3.12), (7.05, 2.72))

    save_fig('1.1', fig)


# ----------------------------------------------------------------------
# Figure 1.2  SR: light cones attached to events along a worldline
# ----------------------------------------------------------------------
def fig_1_2():
    fig, ax = plt.subplots(figsize=(4.0, 3.7))
    ax.set_xlim(0.2, 10.2)
    ax.set_ylim(-0.2, 7.8)
    ax.set_aspect('equal')
    ax.axis('off')

    # worldline
    wl_pts = [(5.65, 0.05), (5.85, 0.85), (6.15, 1.55), (6.5, 2.5),
              (6.85, 3.5), (7.15, 4.5), (7.42, 5.35), (7.6, 6.1),
              (7.68, 6.75)]
    wl = catmull_rom(wl_pts, n=30)
    ax.plot(wl[:, 0], wl[:, 1], color='k', lw=2.0, zorder=5)
    arrow(ax, wl[-3], wl[-1] + (0.0, 0.3), lw=2.0, ms=17, zorder=5)

    # light cones: two sit on the worldline, two float freely
    light_cone(ax, 7.47, 5.82)
    light_cone(ax, 3.35, 4.35)
    light_cone(ax, 8.75, 3.05)
    light_cone(ax, 6.13, 1.57)

    # labels
    ax.text(1.35, 6.45, 'particle worldline', fontsize=10.5)
    pointer(ax, (4.05, 6.52), (7.63, 6.68))

    ax.text(8.3, 5.4, 'light cones', fontsize=10.5)
    pointer(ax, (8.45, 5.3), (7.72, 5.95))
    pointer(ax, (8.6, 5.17), (8.52, 3.86))

    save_fig('1.2', fig)


# ----------------------------------------------------------------------
# Figure 1.3  Euclidean plane, two coordinate systems, invariant distance
# ----------------------------------------------------------------------
def fig_1_3():
    th = np.deg2rad(20.0)
    ct, st = np.cos(th), np.sin(th)
    up = np.array([ct, st])          # unit vector along x'
    wp = np.array([-st, ct])         # unit vector along y'

    fig, ax = plt.subplots(figsize=(4.0, 3.9))
    ax.set_xlim(-1.75, 4.35)
    ax.set_ylim(-0.95, 3.95)
    ax.set_aspect('equal')
    ax.axis('off')
    O = np.array([0.0, 0.0])

    # black axes
    arrow(ax, (-0.12, 0), (4.0, 0), lw=1.2, ms=12)
    arrow(ax, (0, -0.12), (0, 3.65), lw=1.2, ms=12)
    ax.text(4.02, -0.3, r'$x$', fontsize=12)
    ax.text(0.18, 3.5, r'$y$', fontsize=12)

    # gray rotated axes
    g = '0.55'
    arrow(ax, (0, 0), 3.7 * up, lw=1.3, ms=12, color=g)
    arrow(ax, (0, 0), 3.25 * wp, lw=1.3, ms=12, color=g)
    ax.text(3.55 * up[0] + 0.1, 3.55 * up[1] - 0.22, r"$x'$", fontsize=12,
            color=g)
    ax.text(3.30 * wp[0] - 0.05, 3.30 * wp[1] + 0.1, r"$y'$", fontsize=12,
            color=g)

    # the two points and the invariant segment
    P1 = np.array([0.95, 2.60])
    P2 = np.array([1.90, 1.45])
    ax.plot([P1[0], P2[0]], [P1[1], P2[1]], color='k', lw=2.2, zorder=5)
    for P in (P1, P2):
        ax.plot(*P, marker='o', ms=4.5, color='k', zorder=6)

    # black dashed projections onto the (x, y) axes
    for P in (P1, P2):
        ax.plot([P[0], P[0]], [0, P[1]], 'k--', lw=0.9, dashes=(5, 3.2),
                zorder=2)
        ax.plot([0, P[0]], [P[1], P[1]], 'k--', lw=0.9, dashes=(5, 3.2),
                zorder=2)

    # gray dashed projections onto the (x', y') axes
    def foot(P, axdir, axisdir):
        # intersection of P + s*axdir with the line spanned by axisdir
        A = np.column_stack([axdir, -axisdir])
        s, _ = np.linalg.solve(A, P)
        return P - s * axdir

    for P in (P1, P2):
        A = foot(P, up, wp)   # on the y' axis (came in parallel to x')
        B = foot(P, wp, up)   # on the x' axis (came in parallel to y')
        ax.plot([P[0], A[0]], [P[1], A[1]], color=g, lw=0.9,
                dashes=(5, 3.2), zorder=2)
        ax.plot([P[0], B[0]], [P[1], B[1]], color=g, lw=0.9,
                dashes=(5, 3.2), zorder=2)

    A1, A2 = foot(P1, up, wp), foot(P2, up, wp)
    B1, B2 = foot(P1, wp, up), foot(P2, wp, up)

    # braces
    brace(ax, (P1[0], -0.10), (P2[0], -0.10), depth=0.17, side=1, lw=1.0)
    ax.text(0.5 * (P1[0] + P2[0]), -0.72, r'$\Delta x$', fontsize=12)

    brace(ax, (-0.10, P2[1]), (-0.10, P1[1]), depth=0.17, side=1, lw=1.0)
    ax.text(-0.78, 0.5 * (P1[1] + P2[1]), r'$\Delta y$', fontsize=12)

    nwp = np.array([-wp[1], wp[0]])   # points away from the y' axis
    p0 = A2 + 0.13 * nwp
    p1 = A1 + 0.13 * nwp
    brace(ax, p0, p1, depth=0.20, side=-1, color=g, lw=1.0)
    m = 0.5 * (p0 + p1) + 0.85 * nwp
    ax.text(m[0], m[1], r"$\Delta y'$", fontsize=12, color=g,
            rotation=np.rad2deg(th))

    nup = np.array([-up[1], up[0]])   # points above the x' axis
    p0 = B1 + 0.13 * nup
    p1 = B2 + 0.13 * nup
    brace(ax, p0, p1, depth=0.20, side=-1, color=g, lw=1.0)
    ax.text(2.25, 0.98, r"$\Delta x'$", fontsize=12, color=g,
            rotation=np.rad2deg(th))

    save_fig('1.3', fig)


# ----------------------------------------------------------------------
# Figure 1.4  Synchronizing clocks with a light beam
# ----------------------------------------------------------------------
def fig_1_4():
    fig, ax = plt.subplots(figsize=(3.6, 3.4))
    ax.set_xlim(-0.55, 3.15)
    ax.set_ylim(-0.42, 3.45)
    ax.set_aspect('equal')
    ax.axis('off')

    arrow(ax, (-0.3, -0.1), (-0.3, 3.25), lw=1.1, ms=12)
    arrow(ax, (-0.42, 0), (3.0, 0), lw=1.1, ms=12)
    ax.text(-0.12, 3.12, r'$t$', fontsize=12)
    ax.text(2.88, -0.3, r'$x$', fontsize=12)

    # the two clock worldlines
    for xc in (1.0, 2.0):
        ax.plot([xc, xc], [0, 3.08], color='k', lw=1.0, zorder=2)
    ax.text(1.0, -0.34, '1', fontsize=11, ha='center')
    ax.text(2.0, -0.34, '2', fontsize=11, ha='center')

    t1, t2, t1p = 0.35, 1.60, 2.90
    ax.plot([1, 2, 1], [t1, t2, t1p], color='k', lw=2.2, zorder=5)

    ax.text(0.78, t1 - 0.02, r'$t_1$', fontsize=12, ha='right')
    ax.text(0.78, t1p + 0.02, r"$t_1'$", fontsize=12, ha='right')
    ax.text(2.18, t2 - 0.02, r'$t_2$', fontsize=12)

    save_fig('1.4', fig)


# ----------------------------------------------------------------------
# Figure 1.5  The light cone with timelike / null / spacelike directions
# ----------------------------------------------------------------------
def fig_1_5():
    fig, ax = plt.subplots(figsize=(3.9, 4.3))
    ax.set_xlim(-2.5, 3.55)
    ax.set_ylim(-3.25, 3.35)
    ax.set_aspect('equal')
    ax.axis('off')

    w, h, ry = 1.75, 2.2, 0.40   # rim half-width, cone height, rim minor axis

    def cone_body(sign, base, shade):
        # sign=+1 upper cone, -1 lower; base grey + darker right half
        t = np.linspace(0, np.pi, 60)
        rim_lo = np.column_stack([w * np.cos(t), sign * h - sign * ry * np.sin(t)])
        # keep the arc on the far side of the apex
        verts = np.vstack([[[0, 0]], [[-w, sign * h]], rim_lo, [[w, sign * h]]])
        ax.add_patch(Polygon(verts, closed=True, facecolor=base,
                             edgecolor='none', zorder=2))
        # darker shading on one half
        t2 = np.linspace(0, np.pi / 2, 40)
        rim_half = np.column_stack([w * np.cos(t2),
                                    sign * h - sign * ry * np.sin(t2)])
        verts2 = np.vstack([[[0, 0]], rim_half])
        ax.add_patch(Polygon(verts2, closed=True, facecolor=shade,
                             edgecolor='none', zorder=2))
        # rim ellipse
        ax.add_patch(Ellipse((0, sign * h), 2 * w, 2 * ry, facecolor='0.90',
                             edgecolor='k', lw=0.8, zorder=3))
        # silhouette
        ax.plot([-w, 0, w], [sign * h, 0, sign * h], color='k', lw=0.8,
                zorder=4)

    cone_body(-1, '0.88', '0.78')
    cone_body(+1, '0.85', '0.74')

    # axes (drawn on top of the cone)
    arrow(ax, (0, -3.05), (0, 3.15), lw=1.1, ms=12, zorder=6)
    arrow(ax, (-2.35, 0), (3.35, 0), lw=1.1, ms=12, zorder=6)
    ax.text(0.2, 2.95, r'$t$', fontsize=12, zorder=6)
    ax.text(3.18, -0.32, r'$x$', fontsize=12, zorder=6)

    # null direction (along the cone edge)
    pn = (0.70 * w, 0.70 * h)
    ax.plot([0, pn[0]], [0, pn[1]], color='k', lw=2.2, zorder=6)
    ax.plot(*pn, marker='o', ms=4.5, color='k', zorder=6)
    ax.text(pn[0] + 0.2, pn[1] - 0.14, 'null', fontsize=12, zorder=6)

    # spacelike direction (outside the cone, below the x axis)
    ps = (2.0, -0.62)
    ax.plot([0, ps[0]], [0, ps[1]], color='k', lw=2.2, zorder=6)
    ax.plot(*ps, marker='o', ms=4.5, color='k', zorder=6)
    ax.text(ps[0] + 0.1, ps[1] - 0.38, 'spacelike', fontsize=12, zorder=6)

    # timelike direction (inside the cone), faint arrow + pointer
    arrow(ax, (0.02, 0.02), (0.18, 1.55), lw=1.4, ms=10, color='0.55',
          zorder=5)
    ax.text(-1.7, 0.55, 'timelike', fontsize=12, zorder=6)
    pointer(ax, (-0.62, 0.66), (0.07, 0.85), color='0.4', lw=0.7)

    save_fig('1.5', fig)


# ----------------------------------------------------------------------
# Figure 1.6  The twin paradox
# ----------------------------------------------------------------------
def fig_1_6():
    fig, ax = plt.subplots(figsize=(3.6, 4.0))
    ax.set_xlim(-0.85, 2.65)
    ax.set_ylim(-0.4, 3.35)
    ax.set_aspect('equal')
    ax.axis('off')

    arrow(ax, (-0.55, -0.12), (-0.55, 3.2), lw=1.1, ms=12)
    arrow(ax, (-0.68, 0), (2.5, 0), lw=1.1, ms=12)
    ax.text(-0.4, 3.08, r'$t$', fontsize=12)
    ax.text(2.36, -0.32, r'$x$', fontsize=12)

    A = (0.0, 0.0)
    B = (0.0, 1.45)
    C = (0.0, 2.90)
    Bp = (0.85, 1.45)

    # thin full vertical line, thick worldline on top
    ax.plot([0, 0], [-0.1, 3.02], color='k', lw=1.0, zorder=2)
    ax.plot([A[0], Bp[0], C[0]], [A[1], Bp[1], C[1]], color='k', lw=2.2,
            zorder=5)
    ax.plot([A[0], C[0]], [A[1], C[1]], color='k', lw=2.2, zorder=5)
    for P in (A, B, C, Bp):
        ax.plot(*P, marker='o', ms=4.5, color='k', zorder=6)

    ax.text(0.09, 0.10, r'$A$', fontsize=12)
    ax.text(0.10, 1.42, r'$B$', fontsize=12)
    ax.text(0.11, 2.97, r'$C$', fontsize=12)
    ax.text(0.96, 1.42, r"$B'$", fontsize=12)

    # Delta t (vertical double arrow, left of the worldline)
    arrow(ax, (-0.3, A[1]), (-0.3, C[1]), lw=0.9, ms=10,
          style='<|-|>', zorder=4)
    ax.text(-0.44, 1.45, r'$\Delta t$', fontsize=12, rotation=-90,
            ha='center', va='center')

    # Delta x (horizontal double arrow with end ticks)
    for xt in (0.0, Bp[0]):
        ax.plot([xt, xt], [1.68, 1.84], color='k', lw=0.8, zorder=4)
    arrow(ax, (0.0, 1.76), (Bp[0], 1.76), lw=0.9, ms=10, style='<|-|>',
          zorder=4)
    ax.text(0.425, 1.94, r'$\Delta x$', fontsize=12, ha='center')

    save_fig('1.6', fig)


# ----------------------------------------------------------------------
# Figure 1.7  Lorentz transformation; light cones unchanged
# ----------------------------------------------------------------------
def fig_1_7():
    beta = 0.5
    nt = np.array([beta, 1.0]) / np.hypot(beta, 1.0)   # unit vector along t'
    nx = np.array([1.0, beta]) / np.hypot(beta, 1.0)   # unit vector along x'
    fig, ax = plt.subplots(figsize=(4.5, 3.3))
    ax.set_xlim(-3.75, 3.15)
    ax.set_ylim(-1.65, 3.55)
    ax.set_aspect('equal')
    ax.axis('off')

    # light rays (45 degrees, invariant)
    ax.plot([-1.35, 2.2], [-1.35, 2.2], color='k', lw=1.3, zorder=3)
    ax.plot([-2.95, 1.05], [2.95, -1.05], color='k', lw=1.3, zorder=3)
    ax.text(2.02, 2.38, r'$x = t$' + '\n' + r"$x' = t'$", fontsize=10.5)
    ax.text(-3.0, 3.05, r'$x = -t$' + '\n' + r"$x' = -t'$", fontsize=10.5)

    # original axes
    arrow(ax, (0, -1.3), (0, 3.35), lw=1.2, ms=12, zorder=5)
    arrow(ax, (-0.5, 0), (2.95, 0), lw=1.2, ms=12, zorder=5)
    ax.text(0.12, 3.2, r'$t$', fontsize=12)
    ax.text(2.82, -0.32, r'$x$', fontsize=12)

    # boosted axes (gray): t' steep (closer to t), x' shallow (closer to x)
    g = '0.5'
    Lt, Lx = 2.15, 3.05
    arrow(ax, (0, 0), Lt * nt, lw=1.4, ms=12, color=g, zorder=4)
    arrow(ax, (0, 0), Lx * nx, lw=1.4, ms=12, color=g, zorder=4)
    ax.text(Lt * nt[0] + 0.08, Lt * nt[1] + 0.05, r"$t'$", fontsize=12,
            color=g)
    ax.text(Lx * nx[0] + 0.05, Lx * nx[1] - 0.3, r"$x'$", fontsize=12,
            color=g)

    # one event on the future light cone; coordinates in both systems
    P = np.array([1.35, 1.35])
    ax.plot([0, P[0]], [P[1], P[1]], color='k', lw=0.8, zorder=4)
    ax.plot([P[0], P[0]], [0, P[1]], color='k', lw=0.8, zorder=4)
    A = np.column_stack([nx, -nt])
    s, _ = np.linalg.solve(A, P)      # P = s*nx + u*nt -> foot on t' axis
    Ft = P - s * nx
    A2 = np.column_stack([nt, -nx])
    r, _ = np.linalg.solve(A2, P)
    Fx = P - r * nt
    ax.plot([P[0], Ft[0]], [P[1], Ft[1]], color=g, lw=0.9, zorder=3)
    ax.plot([P[0], Fx[0]], [P[1], Fx[1]], color=g, lw=0.9, zorder=3)

    save_fig('1.7', fig)


# ----------------------------------------------------------------------
# Figure 1.8  Manifold with tangent space T_P at point P
# ----------------------------------------------------------------------
def fig_1_8():
    fig, ax = plt.subplots(figsize=(4.6, 3.5))
    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(-2.45, 2.0)
    ax.set_aspect('equal')
    ax.axis('off')

    # tangent plane (parallelogram)
    TL = np.array([-3.25, 1.25])
    TR = np.array([2.90, 1.45])
    BR = np.array([2.10, 0.15])
    BL = np.array([-2.00, -0.05])
    plane_poly = [TL, TR, BR, BL]

    # manifold outline (closed Catmull-Rom spline), tall "beret" shape
    outline = [(-2.55, -0.5), (-2.9, -1.3), (-2.3, -1.95), (-1.1, -1.75),
               (0.2, -2.0), (1.5, -2.1), (2.5, -1.6), (2.9, -0.8),
               (2.8, 0.05), (2.2, 0.5), (1.0, 0.68), (0.0, 0.70),
               (-1.0, 0.6), (-1.9, 0.25)]
    path_pts = catmull_rom(outline, n=26, closed=True)
    from matplotlib.path import Path as MplPath
    dome_path = MplPath(path_pts)
    dome_clip = PathPatch(dome_path, transform=ax.transData)

    # dome part in front of the plane: outline intersected with y <= ycap
    ycap = 0.56
    front = []
    n = len(path_pts)
    for i in range(n):
        p, q = path_pts[i], path_pts[(i + 1) % n]
        if p[1] <= ycap:
            front.append(p)
        if (p[1] <= ycap) != (q[1] <= ycap):
            t = (ycap - p[1]) / (q[1] - p[1])
            front.append(p + t * (q - p))
    front_path = MplPath(np.array(front))
    # keep only the part where the plane passes in front (right of x = -0.9)
    clipped = []
    m = len(front)
    for i in range(m):
        p, q = front[i], front[(i + 1) % m]
        if p[0] >= -0.9:
            clipped.append(p)
        if (p[0] >= -0.9) != (q[0] >= -0.9):
            t = (-0.9 - p[0]) / (q[0] - p[0])
            clipped.append(p + t * (q - p))
    front_clip = PathPatch(MplPath(np.array(clipped)), transform=ax.transData)

    # 1) plane (opaque, light)
    ax.add_patch(Polygon(plane_poly, closed=True, facecolor='0.93',
                         edgecolor='0.55', lw=0.8, zorder=1))
    # 2) manifold (opaque, with grey shading) -- hides the plane behind it
    ax.add_patch(PathPatch(dome_path, facecolor='0.86', edgecolor='0.35',
                           lw=0.8, zorder=2))
    for centre, wdt, hgt, ang, col, al in [
            ((-1.8, -0.6), 2.2, 2.0, -25, '0.78', 0.5),
            ((2.0, -0.6), 1.4, 1.8, 20, '0.79', 0.45),
            ((0.2, 0.1), 2.4, 1.0, 5, '0.93', 0.8)]:
        e = Ellipse(centre, wdt, hgt, angle=ang, facecolor=col, alpha=al,
                    edgecolor='none', zorder=2)
        e.set_clip_path(dome_clip)
        ax.add_patch(e)
    # 3) translucent plane over the front of the dome (peak stays clear)
    ax.add_patch(Polygon(plane_poly, closed=True, facecolor='0.97',
                         alpha=0.45, edgecolor='none', zorder=3))
    ax.add_patch(Polygon(plane_poly, closed=True, facecolor='none',
                         edgecolor='0.55', lw=0.8, zorder=3))
    for patch in ax.patches[-2:]:
        patch.set_clip_path(front_clip)

    # 4) tangent vectors at P (on the dome peak, in front of the plane)
    P = (0.0, 0.64)
    arrow(ax, P, (0.9, 1.12), lw=2.0, ms=15, zorder=6)
    arrow(ax, P, (1.1, 0.3), lw=2.0, ms=15, zorder=6)
    ax.plot(*P, marker='o', ms=4.5, color='k', zorder=7)

    ax.text(-0.28, 0.8, r'$P$', fontsize=12, zorder=7)
    ax.text(2.35, 0.85, r'$T_P$', fontsize=13, zorder=7)
    ax.text(-0.95, -1.15, r'Manifold $M$', fontsize=11, zorder=7)

    save_fig('1.8', fig)


# ----------------------------------------------------------------------
if __name__ == '__main__':
    for key, fn in [('1.1', fig_1_1), ('1.2', fig_1_2), ('1.3', fig_1_3),
                    ('1.4', fig_1_4), ('1.5', fig_1_5), ('1.6', fig_1_6),
                    ('1.7', fig_1_7), ('1.8', fig_1_8)]:
        fn()
        print('fig_%s done' % key)
