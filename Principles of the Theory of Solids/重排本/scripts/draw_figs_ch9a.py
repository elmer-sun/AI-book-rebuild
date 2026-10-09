# -*- coding: utf-8 -*-
"""Redraw Ziman, Principles of the Theory of Solids, 2nd ed., Chapter 9, Figs. 153-163.
Black-and-white textbook-style vector figures. One function per figure."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import numpy as np
from pathlib import Path

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
    'hatch.linewidth': 0.6,
})

BASE = Path(__file__).resolve().parents[1]
FIGDIR = BASE / 'figures'
PREV = FIGDIR / 'preview'
PREV.mkdir(parents=True, exist_ok=True)

Path_ = mpath.Path
PathPatch = mpatches.PathPatch


def _smooth(pts, n=400, passes=3):
    """Catmull-Rom-like smoothing of a polyline through waypoints."""
    pts = np.asarray(pts, float)
    if len(pts) < 3:
        t = np.linspace(0, 1, n)
        return np.column_stack([np.interp(t, [0, 1], pts[:, 0]),
                                np.interp(t, [0, 1], pts[:, 1])])
    # sample each segment with Catmull-Rom
    out = []
    P = np.vstack([pts[0], pts, pts[-1]])
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n // (len(P) - 3), endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(pts[-1])
    return np.array(out)


def _arrow(ax, p0, p1, lw=1.2, ms=9, style='-|>', color='black', zorder=5):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, lw=lw, color=color,
                                mutation_scale=ms, shrinkA=0, shrinkB=0),
                zorder=zorder)


def _tangent_arrow(ax, curve, theta, span=0.10, lw=1.3, ms=9):
    """Small arrowhead tangent to parametric curve at 'theta'."""
    p0 = curve(theta - span)
    p1 = curve(theta + span)
    _arrow(ax, p0, p1, lw=lw, ms=ms)


def _brace(ax, x, y0, y1, w, side='right', lw=0.9):
    """Curly brace. side='right' draws '}' (bulge pointing right)."""
    h, m = y1 - y0, 0.5 * (y0 + y1)
    s = 1.0 if side == 'right' else -1.0
    verts = [(x, y0),
             (x + 0.9 * s * w, y0 + 0.06 * h), (x + 0.60 * s * w, y0 + 0.28 * h), (x + 0.30 * s * w, m - 0.001 * h),
             (x + 0.30 * s * w, m + 0.001 * h),
             (x + 0.60 * s * w, y1 - 0.28 * h), (x + 0.9 * s * w, y1 - 0.06 * h), (x, y1)]
    codes = [Path_.MOVETO, Path_.CURVE4, Path_.CURVE4, Path_.CURVE4,
             Path_.LINETO,
             Path_.CURVE4, Path_.CURVE4, Path_.CURVE4]
    ax.add_patch(PathPatch(Path_(verts, codes), fill=False, lw=lw,
                           capstyle='round', joinstyle='round'))


def _newfig(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    return fig, ax


def _save(fig, key):
    fig.savefig(FIGDIR / f'fig_{key}.pdf', bbox_inches='tight', pad_inches=0.03)
    fig.savefig(PREV / f'fig_{key}.png', bbox_inches='tight', pad_inches=0.03, dpi=170)
    plt.close(fig)
    print('saved', key)


# ---------------------------------------------------------------- Fig. 153
def fig_153():
    fig, ax = _newfig(3.3, 4.3, (-1.25, 1.45), (-1.72, 1.68))
    # hatched plane normal to H (parallelogram in perspective)
    plane = [(-0.12, 1.09), (0.73, 1.52), (0.83, -1.07), (-0.02, -1.55)]
    ax.add_patch(mpatches.Polygon(plane, closed=True, facecolor='white',
                                  edgecolor='black', lw=1.1, hatch='////', zorder=2))
    # Fermi sphere
    ax.add_patch(mpatches.Circle((0, 0), 1.0, fill=False, lw=1.3, zorder=4))
    # orbit = intersection ellipse; front (left) solid, back (right) dashed
    t = np.linspace(-np.pi / 2, np.pi / 2, 100)          # right half (behind)
    xe, ye = 0.36 + 0.33 * np.cos(t), -0.02 + 0.92 * np.sin(t)
    ax.plot(xe, ye, ls=(0, (4, 2.6)), lw=1.1, color='black', zorder=5)
    t = np.linspace(np.pi / 2, 3 * np.pi / 2, 100)       # left half (front)
    xe, ye = 0.36 + 0.33 * np.cos(t), -0.02 + 0.92 * np.sin(t)
    ax.plot(xe, ye, lw=1.4, color='black', zorder=5)
    # k, v at top of orbit
    pk = (0.37, 0.895)
    _arrow(ax, pk, (0.71, 1.29), lw=1.2, ms=10)
    _arrow(ax, pk, (0.05, 1.12), lw=1.2, ms=10)
    ax.text(0.50, 1.12, r'$\mathbf{k}$', fontsize=12)
    ax.text(0.12, 0.84, r'$\mathbf{v}$', fontsize=12)
    # H direction: horizontal from k point to the right
    _arrow(ax, pk, (1.28, 0.895), lw=1.1, ms=10)
    ax.text(1.35, 0.83, r'$\mathbf{H}$', fontsize=12)
    _save(fig, 153)


# ---------------------------------------------------------------- Fig. 154
def fig_154():
    fig, ax = _newfig(4.6, 2.15, (-2.05, 2.55), (-1.02, 0.98))
    a, b = 1.55, 0.55
    # inner orbit (energy E), stippled -> light grey
    ax.add_patch(mpatches.Ellipse((0, 0), 2 * a, 2 * b, facecolor='0.85',
                                  edgecolor='black', lw=1.4, zorder=2))
    # outer dashed orbit (E + dE)
    A, B = 1.86, 0.66
    ax.add_patch(mpatches.Ellipse((0, 0), 2 * A, 2 * B, fill=False,
                                  edgecolor='black', lw=1.1, ls=(0, (4, 2.6)), zorder=3))
    # element of area between the two orbits at the top (straight-sided box)
    hx = 0.17
    yin = lambda x: b * np.sqrt(1 - (x / a) ** 2)
    yout = lambda x: B * np.sqrt(1 - (x / A) ** 2)
    ax.add_patch(mpatches.Polygon(
        [(-hx, yout(-hx)), (hx, yout(hx)), (hx, yin(hx)), (-hx, yin(-hx))],
        closed=True, facecolor='0.72', edgecolor='black', lw=0.9, zorder=4))
    # dk_perp arrow (outward through the left side of the element)
    _arrow(ax, (-hx, yin(-hx) - 0.02), (-hx, yout(-hx) + 0.05), lw=1.0, ms=8)
    ax.text(-0.85, 0.47, r'$dk_\perp$', fontsize=11)
    ax.text(0.02, 0.80, r'$d\mathcal{E}$', fontsize=11)
    ax.text(0.03, 0.40, r'$\mathbf{dk}$', fontsize=12)
    ax.text(0.0, -0.40, r'$\mathcal{E}$', fontsize=12)
    ax.text(0.0, -0.92, r'$\mathcal{E}+d\mathcal{E}$', fontsize=11)
    # v_perp arrow, normal to the orbit
    th = np.radians(24)
    p0 = (a * np.cos(th), b * np.sin(th))
    p1 = (p0[0] + 0.72, p0[1] + 0.52)
    _arrow(ax, p0, p1, lw=1.5, ms=11)
    ax.text(p1[0] + 0.06, p1[1] + 0.02, r'$\mathbf{v}_\perp$', fontsize=12)
    _save(fig, 154)


# ---------------------------------------------------------------- Fig. 155
def fig_155():
    fig, ax = _newfig(4.1, 3.05, (-1.25, 2.05), (-1.25, 1.25))
    R = 1.0
    c2 = (0.25, -0.02)  # displaced centre
    # 1) solid disk, stipple -> grey  (region occupied in undisplaced distribution)
    ax.add_patch(mpatches.Circle((0, 0), R, facecolor='0.82', edgecolor='none', zorder=1))
    # 2) displaced disk, white + hatching drawn over it
    ax.add_patch(mpatches.Circle(c2, R, facecolor='white', edgecolor='none',
                                 hatch='////', zorder=2))
    # 3) outlines
    ax.add_patch(mpatches.Circle((0, 0), R, fill=False, edgecolor='black', lw=1.3, zorder=4))
    ax.add_patch(mpatches.Circle(c2, R, fill=False, edgecolor='black', lw=1.0,
                                 ls=(0, (4, 2.6)), zorder=4))
    # J arrow (from centre, mid + end arrowheads)
    Jend = (0.86, 0.76)
    ax.plot([0, Jend[0]], [0, Jend[1]], lw=1.3, color='black', zorder=5)
    _arrow(ax, (0.44, 0.39), Jend, lw=1.3, ms=10)
    ax.text(0.92, 0.80, r'$\mathbf{J}$', fontsize=12)
    # E dashed arrow to the right
    _arrow(ax, (0, 0), (0.16, 0), lw=1.1, ms=9)
    ax.plot([0.16, 1.62], [0, 0], ls=(0, (4, 2.6)), lw=1.1, color='black', zorder=5)
    _arrow(ax, (1.62, 0), (1.80, 0), lw=1.1, ms=10)
    ax.text(1.87, -0.03, r'$\mathbf{E}$', fontsize=12)
    # omega arc (rotation of the displacement), ccw arrowhead
    t = np.linspace(np.radians(16), np.radians(50), 40)
    ax.plot(1.36 * np.cos(t), 1.36 * np.sin(t), lw=1.1, color='black', zorder=5)
    te = np.radians(50)
    _arrow(ax, (1.36 * np.cos(te - 0.05), 1.36 * np.sin(te - 0.05)),
           (1.36 * np.cos(te + 0.02), 1.36 * np.sin(te + 0.02)), lw=1.1, ms=9)
    ax.text(1.42, 0.80, r'$\omega$', fontsize=12)
    _save(fig, 155)


# ---------------------------------------------------------------- Fig. 156
def fig_156():
    fig, ax = _newfig(4.5, 2.3, (-2.5, 2.75), (-1.15, 1.42))
    y0, y1 = 0.62, 1.06
    # skin-depth bar (hatched), bottom edge dashed
    ax.add_patch(mpatches.Rectangle((-2.25, y0), 4.5, y1 - y0, facecolor='white',
                                    edgecolor='none', hatch='////', zorder=2))
    ax.plot([-2.25, 2.25], [y1, y1], lw=1.2, color='black', zorder=3)
    ax.plot([-2.25, -2.25], [y0, y1], lw=1.2, color='black', zorder=3)
    ax.plot([2.25, 2.25], [y0, y1], lw=1.2, color='black', zorder=3)
    ax.plot([-2.25, 2.25], [y0, y0], ls=(0, (4, 2.6)), lw=1.0, color='black', zorder=3)
    _brace(ax, 2.34, y0, y1, 0.16, side='right')
    ax.text(2.58, y0 + 0.14, r'$\delta$', fontsize=12)
    # axis along H
    _arrow(ax, (-1.85, 0), (1.95, 0), lw=1.1, ms=10)
    ax.text(2.05, -0.04, r'$\mathbf{H}$', fontsize=12)
    # helical path drawn as overlapping loops
    R, b = 0.85, 0.47
    S = 1.02                      # advance per turn
    c = S / (2 * np.pi)
    th = np.linspace(-np.pi / 2, 13 * np.pi / 2, 700)
    X = c * th + b * np.cos(th) - 0.15
    Y = -R * np.sin(th)
    ax.plot(X, Y, lw=1.4, color='black', zorder=4)
    f = lambda t: (c * t + b * np.cos(t) - 0.15, -R * np.sin(t))
    for tc in (0, 2 * np.pi, 4 * np.pi):        # small arrows at axis crossings
        _tangent_arrow(ax, f, tc, span=0.13, lw=1.2, ms=8)
    _tangent_arrow(ax, f, 13 * np.pi / 2, span=0.40, lw=1.4, ms=11)  # end arrow
    _save(fig, 156)


# ---------------------------------------------------------------- Fig. 157
def fig_157():
    fig, ax = _newfig(4.8, 2.85, (-2.9, 4.35), (-1.6, 1.75))
    ox = -1.35                       # panel (a) origin at circle centre
    # ---- (a) real space: helical path section
    ya, yt = 0.72, 1.02              # skin band: bottom / top
    ax.add_patch(mpatches.Rectangle((ox - 1.35, ya), 2.75, yt - ya,
                                    facecolor='0.85', edgecolor='none', zorder=1))
    ax.plot([ox - 1.35, ox + 1.40], [yt, yt], lw=1.0, color='black', zorder=2)
    ax.plot([ox - 1.35, ox + 1.40], [ya, ya], lw=1.0, color='black', zorder=2)
    _brace(ax, ox - 1.44, ya, yt, 0.14, side='left')
    ax.text(ox - 1.72, ya + 0.06, r"$\delta'$", fontsize=12)
    # E_x above the band
    _arrow(ax, (ox - 0.30, 1.52), (ox + 0.62, 1.52), lw=1.1, ms=10)
    ax.text(ox - 0.66, 1.46, r'$E_x$', fontsize=12)
    # circular orbit, thick inside the skin
    R = 1.0
    ax.add_patch(mpatches.Circle((ox, 0), R, fill=False, lw=1.3, zorder=3))
    th1, th2 = np.arcsin(ya / R), np.pi - np.arcsin(ya / R)
    tt = np.linspace(th1, th2, 80)
    ax.plot(ox + R * np.cos(tt), R * np.sin(tt), lw=2.6, color='black', zorder=4)
    f = lambda t: (ox + R * np.cos(t), R * np.sin(t))
    _tangent_arrow(ax, f, np.radians(76), span=-0.09, lw=1.8, ms=10)   # v_x on arc
    ax.text(ox + 0.80, 0.83, r'$v_x$', fontsize=12)
    # dashed radii bounding phi_m
    for s in (1, -1):
        ax.plot([ox, ox + s * R * np.cos(th1)], [0, ya], ls=(0, (4, 2.6)),
                lw=1.0, color='black', zorder=2)
    t = np.linspace(th1, th2, 30)
    ax.plot(ox + 0.30 * np.cos(t), 0.30 * np.sin(t), lw=0.9, color='black', zorder=2)
    ax.plot([ox + 0.28, ox + 0.40], [0.24, 0.30], lw=0.9, color='black')
    ax.text(ox + 0.44, 0.24, r'$\phi_m$', fontsize=12)
    # radius R
    _arrow(ax, (ox, 0), (ox - 0.98, 0), lw=1.1, ms=10)
    ax.text(ox - 0.50, 0.07, r'$R$', fontsize=12)
    # x, z axes
    _arrow(ax, (ox + 1.05, 0.57), (ox + 1.52, 0.57), lw=1.0, ms=9)
    ax.text(ox + 1.24, 0.64, r'$x$', fontsize=12)
    _arrow(ax, (ox + 1.08, 0.46), (ox + 1.08, 0.02), lw=1.0, ms=9)
    ax.text(ox + 1.15, 0.18, r'$z$', fontsize=12)
    ax.text(ox + 0.52, -1.28, r'$(a)$', fontsize=12)
    # ---- (b) k-space: orbit on Fermi surface
    ox2, Rb = 1.95, 0.72
    ax.add_patch(mpatches.Circle((ox2, 0), Rb, facecolor='0.85',
                                 edgecolor='black', lw=1.3, zorder=2))
    hw = np.radians(26)
    ax.plot([ox2, ox2 + Rb * np.cos(hw), ox2 + Rb * np.cos(-hw)],
            [0, Rb * np.sin(hw), Rb * np.sin(-hw)], lw=2.0, color='black', zorder=3)
    t = np.linspace(-hw, hw, 30)
    ax.plot(ox2 + Rb * np.cos(t), Rb * np.sin(t), lw=2.0, color='black', zorder=3)
    t = np.linspace(-hw, hw, 30)
    ax.plot(ox2 + 0.30 * np.cos(t), 0.30 * np.sin(t), lw=0.9, color='black', zorder=3)
    ax.text(ox2 + 0.22, -0.13, r'$\phi_m$', fontsize=12)
    _arrow(ax, (ox2 + Rb, 0), (ox2 + Rb + 0.52, 0), lw=1.3, ms=10)
    ax.text(ox2 + Rb + 0.38, -0.18, r'$v_x$', fontsize=12)
    _arrow(ax, (ox2 + 0.30, 1.12), (ox2 + 0.88, 1.12), lw=1.0, ms=9)
    ax.text(ox2 + 0.48, 1.20, r'$k_x$', fontsize=12)
    _arrow(ax, (ox2 + 1.00, 0.92), (ox2 + 1.00, 0.42), lw=1.0, ms=9)
    ax.text(ox2 + 0.80, 0.62, r'$k_z$', fontsize=12)
    ax.text(ox2, -1.28, r'$(b)$', fontsize=12)
    _save(fig, 157)


# ---------------------------------------------------------------- Fig. 158
def fig_158():
    fig, ax = _newfig(4.7, 2.55, (-1.75, 2.75), (-1.12, 1.12))
    ctrl = [(-1.50, 0.375), (-1.30, 0.300), (-1.10, 0.240), (-0.97, 0.200),
            (-0.75, 0.330), (-0.45, 0.620), (-0.15, 0.880), (0.15, 1.000),
            (0.45, 0.980), (0.80, 0.905), (1.15, 0.800), (1.45, 0.690),
            (1.61, 0.640), (1.95, 0.650), (2.33, 0.720)]
    C = np.array(ctrl, float)
    xs = np.linspace(C[0, 0], C[-1, 0], 500)
    rs = np.interp(xs, C[:, 0], C[:, 1])
    for _ in range(60):                       # smooth the profile
        rs[1:-1] = 0.25 * rs[:-2] + 0.5 * rs[1:-1] + 0.25 * rs[2:]
    def r(x):
        return float(np.interp(x, xs, rs))
    f = 0.28                                  # foreshortening of latitude circles
    # silhouette
    ax.plot(xs, rs, lw=1.4, color='black')
    ax.plot(xs, -rs, lw=1.4, color='black')
    # latitude circles
    for xq in (-1.50, -1.28, -0.97, -0.60, -0.15, 0.50, 1.00, 1.45,
               1.90, 2.33):
        rq = r(xq)
        t = np.linspace(0, 2 * np.pi, 120)
        ax.plot(xq + f * rq * np.cos(t), rq * np.sin(t), lw=0.9, color='black')
    # extremal-orbit bands (hatched): min at the neck, max at the belly
    def band(x1, x2):
        t = np.linspace(0, -np.pi, 60)         # left half of ellipse 1, top->bottom
        left = np.column_stack([x1 + f * r(x1) * np.sin(t), r(x1) * np.cos(t)])
        t2 = np.linspace(np.pi, 0, 60)         # right half of ellipse 2, bottom->top
        right = np.column_stack([x2 + f * r(x2) * np.sin(t2), r(x2) * np.cos(t2)])
        xs1 = np.linspace(x1, x2, 30)
        top = np.column_stack([xs1, [r(x) for x in xs1]])
        bot = np.column_stack([xs1[::-1], [-r(x) for x in xs1[::-1]]])
        poly = np.vstack([top, right[::-1], bot, left[::-1]])
        ax.add_patch(mpatches.Polygon(poly, closed=True, facecolor='white',
                                      edgecolor='black', lw=1.0, hatch='///', zorder=3))
    band(-1.18, -0.80)
    band(-0.02, 0.50)
    # small direction arrows on the bands
    _arrow(ax, (-1.02, -0.02), (-1.06, 0.16), lw=1.1, ms=8)
    _arrow(ax, (0.22, 0.08), (0.22, 0.40), lw=1.2, ms=9)
    _save(fig, 158)


# ---------------------------------------------------------------- Fig. 159
def fig_159():
    fig, ax = _newfig(4.1, 2.35, (-2.55, 2.55), (-1.65, 1.45))
    # (a) electron orbit: filled disk, ccw arrow at top
    c1, R = (-1.30, 0), 0.98
    ax.add_patch(mpatches.Circle(c1, R, facecolor='0.85', edgecolor='black',
                                 lw=1.4, zorder=2))
    _arrow(ax, (c1[0] + 0.30, R * 0.985), (c1[0] - 0.30, R * 0.985), lw=1.5, ms=11)
    ax.text(c1[0], -1.48, r'$(a)$', fontsize=12)
    # (b) hole orbit: annulus, cw arrow at top of the inner circle
    c2 = (1.30, 0)
    ax.add_patch(mpatches.Circle(c2, 1.22, facecolor='0.85', edgecolor='0.45',
                                 lw=0.7, zorder=1))
    ax.add_patch(mpatches.Circle(c2, 0.63, facecolor='white', edgecolor='black',
                                 lw=1.4, zorder=2))
    _arrow(ax, (c2[0] - 0.22, 0.655), (c2[0] + 0.22, 0.655), lw=1.5, ms=11)
    ax.text(c2[0], -1.48, r'$(b)$', fontsize=12)
    _save(fig, 159)


# ---------------------------------------------------------------- Fig. 160
def fig_160():
    fig, ax = _newfig(4.9, 2.6, (-5.15, 5.45), (-0.85, 4.45))
    # ---------------- panel (a): reduced zone (one cell, landscape)
    W, H = 1.2, 1.0                     # cell half-width, half-height
    cx0, cy0 = -3.35, 2.05              # cell centre
    rx, ry = 0.85 * W, 0.80 * H         # pocket arc semi-axes
    ax.add_patch(mpatches.Rectangle((cx0 - W, cy0 - H), 2 * W, 2 * H,
                                    facecolor='0.85', edgecolor='black', lw=1.2, zorder=1))
    # white corner pockets bounded by quarter-ellipse arcs (inward quadrants)
    t = np.linspace(0, np.pi / 2, 40)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = cx0 + sx * W, cy0 + sy * H
            vv = [(cx, cy), (cx - sx * rx, cy),
                  *[(cx - sx * rx * np.cos(u), cy - sy * ry * np.sin(u)) for u in t[1:]],
                  (cx, cy - sy * ry), (cx, cy)]
            codes = [Path_.MOVETO] + [Path_.LINETO] * (len(vv) - 2) + [Path_.CLOSEPOLY]
            ax.add_patch(PathPatch(Path_(vv, codes), facecolor='white',
                                   edgecolor='black', lw=1.2, zorder=2))
    # motion arrows (clockwise about the cell centre)
    def P_tl(s):   # A' -> B
        u = np.pi / 2 * s
        return (cx0 - W + rx * np.sin(u), cy0 + H - ry * np.cos(u))
    def P_tr(s):   # D' -> A
        u = np.pi / 2 * s
        return (cx0 + W - rx * np.sin(u), cy0 + H - ry * np.cos(u))
    def P_bl(s):   # B' -> C
        u = np.pi / 2 * s
        return (cx0 - W + rx * np.sin(u), cy0 - H + ry * np.cos(u))
    def P_br(s):   # C' -> D
        u = np.pi / 2 * s
        return (cx0 + W - rx * np.sin(u), cy0 - H + ry * np.cos(u))
    for f in (P_tl, P_tr, P_bl, P_br):
        _arrow(ax, f(0.42), f(0.60), lw=1.4, ms=10)
    # dashed translation lines with single arrowheads
    yA, yC = cy0 + 0.20 * H, cy0 - 0.20 * H
    xB, xD = cx0 - 0.15 * W, cx0 + 0.15 * W
    for yq in (yA, yC):
        ax.plot([cx0 - W + 0.02, cx0 + W - 0.02], [yq, yq],
                ls=(0, (4, 2.6)), lw=0.9, color='black', zorder=3)
        _arrow(ax, (cx0 - 0.30, yq), (cx0 - 0.06, yq), lw=1.0, ms=8)
    for xq in (xB, xD):
        ax.plot([xq, xq], [cy0 - H + 0.02, cy0 + H - 0.02],
                ls=(0, (4, 2.6)), lw=0.9, color='black', zorder=3)
        _arrow(ax, (xq, cy0 + 0.28), (xq, cy0 + 0.04), lw=1.0, ms=8)
    # labels
    ax.text(xB - 0.10, cy0 + H + 0.14, r'$B$', fontsize=12)
    ax.text(xD - 0.12, cy0 + H + 0.14, r"$D'$", fontsize=12)
    ax.text(cx0 - W - 0.42, yA - 0.05, r"$A'$", fontsize=12)
    ax.text(cx0 - W - 0.30, yC - 0.07, r'$C$', fontsize=12)
    ax.text(cx0 + W + 0.14, yA - 0.05, r'$A$', fontsize=12)
    ax.text(cx0 + W + 0.14, yC - 0.07, r"$C'$", fontsize=12)
    ax.text(xB - 0.12, cy0 - H - 0.30, r"$B'$", fontsize=12)
    ax.text(xD - 0.10, cy0 - H - 0.30, r'$D$', fontsize=12)
    ax.text(cx0, cy0 - H - 0.74, r'$(a)$', fontsize=12)
    # ---------------- panel (b): repeated zone (2x2 cells)
    ox, oy = 0.35, 0.05
    CW, CH = 2 * W, 2 * H
    W2, H2 = 2 * CW, 2 * CH
    block = mpatches.Rectangle((ox, oy), W2, H2, facecolor='0.85',
                               edgecolor='black', lw=1.2, zorder=1)
    ax.add_patch(block)
    # zone-boundary lines through the centre
    ax.plot([ox + W2 / 2, ox + W2 / 2], [oy, oy + H2], lw=0.8, color='black', zorder=3)
    ax.plot([ox, ox + W2], [oy + H2 / 2, oy + H2 / 2], lw=0.8, color='black', zorder=3)
    # pockets at every grid vertex (ellipses), clipped to the block
    pc = (ox + W2 / 2, oy + H2 / 2)
    for i in range(3):
        for j in range(3):
            vx, vy = ox + i * CW, oy + j * CH
            if (vx, vy) == pc:
                continue
            e = mpatches.Ellipse((vx, vy), 2 * rx, 2 * ry, facecolor='white',
                                 edgecolor='black', lw=1.2, zorder=2)
            ax.add_patch(e)
            e.set_clip_path(block)
    # centre pocket: white with bold edge = the continuous orbit, cw arrows
    ax.add_patch(mpatches.Ellipse(pc, 2 * rx, 2 * ry, facecolor='white',
                                  edgecolor='black', lw=2.2, zorder=4))
    for ang in (45, 135, 225, 315):
        a = np.radians(ang)
        p = lambda s: (pc[0] + (rx + 0.02) * np.cos(a + s), pc[1] + (ry + 0.02) * np.sin(a + s))
        _arrow(ax, p(-0.16), p(0.16), lw=1.5, ms=10)
    # labels: pairs straddling the zone lines
    ax.text(pc[0] - 0.34, pc[1] + ry + 0.16, r"$C'$", fontsize=12)
    ax.text(pc[0] + 0.10, pc[1] + ry + 0.16, r'$C$', fontsize=12)
    ax.text(pc[0] - rx - 0.50, pc[1] + 0.16, r'$D$', fontsize=12)
    ax.text(pc[0] - rx - 0.48, pc[1] - 0.32, r"$D'$", fontsize=12)
    ax.text(pc[0] + rx + 0.16, pc[1] + 0.16, r"$B'$", fontsize=12)
    ax.text(pc[0] + rx + 0.18, pc[1] - 0.32, r'$B$', fontsize=12)
    ax.text(pc[0] - 0.34, pc[1] - ry - 0.44, r'$A$', fontsize=12)
    ax.text(pc[0] + 0.10, pc[1] - ry - 0.44, r"$A'$", fontsize=12)
    ax.text(pc[0], oy - 0.48, r'$(b)$', fontsize=12)
    _save(fig, 160)


# ---------------------------------------------------------------- Fig. 161
def fig_161():
    fig, ax = _newfig(4.3, 3.3, (-0.35, 4.75), (-0.45, 3.75))
    # cube wireframe (thin): front face + offset back face
    f = [(0, 0), (3.5, 0), (3.5, 2.7), (0, 2.7)]
    dx, dy = 0.95, 0.62
    bk = [(x + dx, y + dy) for (x, y) in f]
    for i in range(4):
        j = (i + 1) % 4
        ax.plot([f[i][0], f[j][0]], [f[i][1], f[j][1]], lw=0.7, color='black')
        ax.plot([bk[i][0], bk[j][0]], [bk[i][1], bk[j][1]], lw=0.7, color='black')
        ax.plot([f[i][0], bk[i][0]], [f[i][1], bk[i][1]], lw=0.7, color='black')
    # multiply-connected surface: rounded-square tube ring around the front face
    def rrect(w, h, r):
        v = [(r, 0), (w - r, 0), (w, r), (w, h - r), (w - r, h), (r, h),
             (0, h - r), (0, r), (r, 0)]
        c = [Path_.MOVETO, Path_.CURVE4, Path_.CURVE4, Path_.CURVE4] * 1 + \
            [Path_.CURVE4, Path_.CURVE4, Path_.CURVE4] * 1 + \
            [Path_.CURVE4, Path_.CURVE4, Path_.CURVE4] * 1 + \
            [Path_.CURVE4, Path_.CURVE4, Path_.CURVE4] * 1 + [Path_.CLOSEPOLY]
        return Path_(v, c)
    outer = mpatches.FancyBboxPatch((0.14, 0.14), 3.22, 2.42,
                                    boxstyle='round,pad=0,rounding_size=0.62',
                                    facecolor='0.88', edgecolor='black', lw=1.1, zorder=2)
    inner = mpatches.FancyBboxPatch((0.46, 0.46), 2.58, 1.78,
                                    boxstyle='round,pad=0,rounding_size=0.48',
                                    facecolor='white', edgecolor='black', lw=1.1, zorder=3)
    ax.add_patch(outer)
    ax.add_patch(inner)
    # tube cross-sections (dark stippled disks) on the front face
    for cxy in ((1.15, 1.35), (2.45, 1.35)):
        ax.add_patch(mpatches.Circle(cxy, 0.40, facecolor='0.80',
                                     edgecolor='black', lw=1.0, zorder=4))
    # tube end at the left edge
    ax.add_patch(mpatches.Ellipse((0.30, 1.35), 0.40, 0.92, facecolor='0.88',
                                  edgecolor='black', lw=1.0, zorder=4))
    # top-face hole opening (rounded quad ring in perspective)
    ho = mpatches.FancyBboxPatch((1.30, 2.58), 1.80, 0.62,
                                 boxstyle='round,pad=0,rounding_size=0.28',
                                 facecolor='white', edgecolor='black', lw=1.3, zorder=4)
    ax.add_patch(ho)
    # dashed ellipse inside the hole + leader + label
    ax.add_patch(mpatches.Ellipse((2.62, 2.86), 0.72, 0.20, fill=False,
                                  edgecolor='black', lw=0.9, ls=(0, (3, 2)), zorder=5))
    ax.text(1.62, 2.80, 'Hole', fontsize=12, zorder=6)
    ax.plot([2.12, 2.32], [2.86, 2.86], lw=0.8, color='black', zorder=6)
    ax.text(1.80, 2.36, r'$P$', fontsize=12, zorder=6)
    # electron orbit segment going round the front-right vertical tube
    t = np.linspace(0, 1, 60)
    xe = 2.02 + 1.42 * t ** 0.85
    ye = 2.28 - 1.42 * t
    ax.plot(xe, ye, lw=2.0, color='black', zorder=6)
    _arrow(ax, (xe[-8], ye[-8]), (xe[-1], ye[-1]), lw=1.6, ms=10)
    ax.text(3.48, 1.50, 'Electron', fontsize=11, rotation=68, zorder=6)
    # small opening top-left
    ax.add_patch(mpatches.Ellipse((0.92, 3.10), 0.85, 0.28, facecolor='white',
                                  edgecolor='black', lw=1.0, zorder=4))
    _save(fig, 161)


# ---------------------------------------------------------------- Fig. 162
def fig_162():
    fig, ax = _newfig(4.6, 2.45, (-2.25, 2.55), (-1.30, 1.30))
    s = 1.15
    Hb = 0.70          # band half-height (pocket centres sit on these edges)
    rp = 0.40          # pocket radius
    X0, X1 = -2.15, 2.50
    # grey band with rounded tongues reaching out between the pockets
    xs = np.linspace(X0, X1, 600)
    tongue = 0.36 * np.abs(np.sin(np.pi * (xs - s / 2) / s)) ** 1.3
    ytop = Hb + tongue
    ybot = -Hb - tongue
    poly = np.vstack([np.column_stack([xs, ytop]),
                      np.column_stack([xs[::-1], ybot[::-1]])])
    ax.add_patch(mpatches.Polygon(poly, closed=True, facecolor='0.85',
                                  edgecolor='none', zorder=1))
    # pockets: top row at x = k s, bottom row offset by s/2
    for k in (-1, 0, 1, 2):
        ax.add_patch(mpatches.Circle((k * s, Hb), rp, facecolor='white',
                                     edgecolor='black', lw=1.2, zorder=3))
    for k in (-2, -1, 0, 1):
        ax.add_patch(mpatches.Circle((k * s + s / 2, -Hb), rp, facecolor='white',
                                     edgecolor='black', lw=1.2, zorder=3))
    # dark occupied disks at x = k s + s/2
    for k in (-2, -1, 0, 1):
        ax.add_patch(mpatches.Circle((k * s + s / 2, 0), 0.33, facecolor='0.12',
                                     edgecolor='none', zorder=4))
    # open orbit: dashed sinusoid grazing the pockets
    A = Hb - rp + 0.001
    xx = np.linspace(X0, 2.40, 600)
    yy = A * np.cos(2 * np.pi * xx / s)
    ax.plot(xx, yy, ls=(0, (4, 2.8)), lw=1.1, color='black', zorder=5)
    for xa in (-1.90, -0.85, 0.30, 1.40, 2.15):
        p = lambda u: (u, A * np.cos(2 * np.pi * u / s))
        _arrow(ax, p(xa - 0.035), p(xa + 0.035), lw=1.2, ms=9)
    _save(fig, 162)


# ---------------------------------------------------------------- Fig. 163
def fig_163():
    fig, ax = _newfig(4.5, 3.6, (-0.95, 2.90), (-1.52, 1.66))
    s = 1.0
    cols = (-0.6, 0.4, 1.4, 2.4)
    rows = (1.1, 0.1, -0.9)
    pw, ph, cr = 0.30, 0.28, 0.13      # pocket half sizes
    X0, X1, Y0, Y1 = -0.75, 2.62, -1.08, 1.32
    # grey web everywhere first
    web = mpatches.Rectangle((X0, Y0), X1 - X0, Y1 - Y0, facecolor='0.85',
                             edgecolor='none', zorder=1)
    ax.add_patch(web)
    # bold open-orbit (divide) curve
    divide = [(1.03, Y1), (0.99, 1.28), (0.80, 1.02), (0.62, 0.86),
              (0.80, 0.71), (1.20, 0.645), (1.52, 0.575), (1.18, 0.505),
              (0.80, 0.44), (0.66, 0.36), (0.98, 0.27), (1.06, 0.10),
              (1.03, -0.08), (0.84, -0.20), (0.68, -0.30), (0.60, -0.42),
              (0.66, -0.56), (0.80, -0.68), (0.88, -0.85), (0.84, -1.05),
              (0.86, Y0)]
    div = _smooth(divide, n=500)
    # white region right of the divide
    right = np.vstack([div, [(X1, Y0), (X1, Y1)]])
    ax.add_patch(mpatches.Polygon(right, closed=True, facecolor='white',
                                  edgecolor='none', zorder=2))
    # pockets (white, rounded squares) in both regions, clipped to the frame
    for cx in cols:
        for cy in rows:
            e = mpatches.FancyBboxPatch(
                (cx - pw, cy - ph), 2 * pw, 2 * ph,
                boxstyle='round,pad=0,rounding_size=0.12',
                facecolor='white', edgecolor='black', lw=1.2, zorder=3)
            ax.add_patch(e)
            e.set_clip_path(web)
    # grey circles (hole orbits) + radiating ticks
    for cx, cy in ((1.9, 0.6), (0.9, -0.4), (1.9, -0.4)):
        ax.add_patch(mpatches.Circle((cx, cy), 0.265, facecolor='0.78',
                                     edgecolor='black', lw=1.2, zorder=4))
        for a in np.linspace(0, 2 * np.pi, 15, endpoint=False) + 0.11:
            r1, r2 = 0.30, 0.40
            ax.plot([cx + r1 * np.cos(a), cx + r2 * np.cos(a)],
                    [cy + r1 * np.sin(a), cy + r2 * np.sin(a)],
                    lw=0.55, color='black', zorder=4)
    # bold divide on top + direction arrows
    ax.plot(div[:, 0], div[:, 1], lw=2.2, color='black', zorder=6,
            solid_capstyle='round')
    # wedge arrows: in along the top, out along the bottom
    _arrow(ax, (0.86, 0.700), (1.18, 0.645), lw=1.4, ms=10)
    _arrow(ax, (1.10, 0.490), (0.82, 0.452), lw=1.4, ms=10)
    _arrow(ax, (0.87, -0.92), (0.86, -1.10), lw=1.4, ms=10)
    _save(fig, 163)


# ----------------------------------------------------------------
if __name__ == '__main__':
    for fn in (fig_153, fig_154, fig_155, fig_156, fig_157, fig_158,
               fig_159, fig_160, fig_161, fig_162, fig_163):
        fn()
