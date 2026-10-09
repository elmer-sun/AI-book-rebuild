# -*- coding: utf-8 -*-
"""Redraw Ziman, Principles of the Theory of Solids, 2nd ed., Chapter 10,
Figs. 175-186. Black-and-white textbook-style vector figures.
One function per figure; each figure is saved (PDF + PNG) immediately."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
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


# ----------------------------------------------------------------- helpers
def _smooth(pts, n=300):
    """Catmull-Rom smoothing of a polyline through waypoints."""
    pts = np.asarray(pts, float)
    if len(pts) < 3:
        t = np.linspace(0, 1, n)
        return np.column_stack([np.interp(t, [0, 1], pts[:, 0]),
                                np.interp(t, [0, 1], pts[:, 1])])
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


def _arrow(ax, p0, p1, lw=1.2, ms=9, style='-|>', color='black', ls='-', z=5):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, lw=lw, color=color,
                                mutation_scale=ms, shrinkA=0, shrinkB=0, ls=ls),
                zorder=z)


def _bezier(p0, p1, p2, n=100):
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 2) * np.asarray(p0) + 2 * t * (1 - t) * np.asarray(p1) \
        + (t ** 2) * np.asarray(p2)


def _thick(ax, pts, lw=2.4, z=4):
    """thick 'wavy' (d-spin) line, drawn as a slightly wiggled polyline."""
    pts = np.asarray(pts, float)
    if len(pts) == 3:
        xy = _bezier(pts[0], pts[1], pts[2])
    else:
        xy = _smooth(pts)
    ax.plot(xy[:, 0], xy[:, 1], color='k', lw=lw, solid_capstyle='round', zorder=z)


def _save(fig, key):
    fig.savefig(FIGDIR / f'fig_{key}.pdf', bbox_inches='tight', pad_inches=0.03)
    fig.savefig(PREV / f'fig_{key}.png', bbox_inches='tight', pad_inches=0.03, dpi=200)
    plt.close(fig)
    print('saved', key)


def _brace(ax, x, y0, y1, w, lw=0.9):
    """Curly brace spanning (y0,y1) at abscissa x; w>0 -> mouth faces +x."""
    s = np.sign(w)
    w = abs(w)
    c = 0.5 * (y0 + y1)
    t = (y1 - y0)
    verts = [(x, y1),
             (x - s * w, y1 - 0.08 * t), (x - s * 0.30 * w, c - 0.14 * t),
             (x - s * 0.30 * w, c - 0.14 * t), (x - s * 0.62 * w, c - 0.05 * t),
             (x - s * w, c),
             (x - s * 0.62 * w, c + 0.05 * t), (x - s * 0.30 * w, c + 0.14 * t),
             (x - s * 0.30 * w, c + 0.14 * t), (x - s * w, y0 + 0.08 * t),
             (x, y0)]
    codes = [Path_.MOVETO] + [Path_.CURVE3] * 10
    ax.add_patch(PathPatch(Path_(verts, codes), fill=False, lw=lw,
                           edgecolor='k', capstyle='round'))


def _hatch_poly(ax, xy, hatch, fc='white', lw=0.0, z=2):
    ax.add_patch(mpatches.Polygon(xy, closed=True, facecolor=fc, edgecolor='k',
                                  lw=lw, hatch=hatch, zorder=z))


def _spin_dot_circle(ax, xy, r, up=True, hatch='\\\\', arrow_lw=1.7, ms=12,
                     alen=None, fc='white', z=3):
    ax.add_patch(mpatches.Circle(xy, r, facecolor=fc, edgecolor='k', lw=1.0,
                                 hatch=hatch, zorder=z))
    alen = alen if alen is not None else 1.15 * r
    if up:
        _arrow(ax, (xy[0], xy[1] - 0.5 * alen), (xy[0], xy[1] + 0.55 * alen),
               lw=arrow_lw, ms=ms, z=z + 1)
    else:
        _arrow(ax, (xy[0], xy[1] + 0.5 * alen), (xy[0], xy[1] - 0.55 * alen),
               lw=arrow_lw, ms=ms, z=z + 1)


# ------------------------------------------------------------------ Fig 175
def fig_175():
    key = 175
    fig, ax = plt.subplots(figsize=(3.9, 3.05))
    a = 0.85
    zeta, h = 1.0, 0.22
    ytop = 1.78
    # parabolas: solid = shifted, dashed = zero-field (vertices on the axis)
    # left (down-spin) solid shifted UP by h; right (up-spin) solid shifted DOWN
    yl = np.linspace(h, ytop, 200)
    yr = np.linspace(-h, ytop, 200)
    yd = np.linspace(0.001, ytop - 2 * h, 200)
    # fills (stippled), drawn first
    yfl = np.linspace(h, zeta, 200)
    _hatch_poly(ax, list(zip(-a * np.sqrt(yfl - h), yfl)) + [(0, zeta)],
                '...', fc='0.97')
    yfr = np.linspace(-h, zeta, 200)
    _hatch_poly(ax, [(0, zeta)] + list(zip(a * np.sqrt(yfr + h), yfr)),
                '...', fc='0.97')
    # Fermi level lines
    ax.plot([-a * np.sqrt(zeta - h), 0], [zeta, zeta], 'k-', lw=1.3, zorder=3)
    ax.plot([0, a * np.sqrt(zeta + h)], [zeta, zeta], 'k-', lw=1.3, zorder=3)
    ax.text(a * np.sqrt(zeta + h) + 0.06, zeta, r'$\zeta$', va='center')
    ax.plot([-a * np.sqrt(zeta + h), 0], [zeta + h, zeta + h], 'k--', lw=0.9)
    ax.plot([0, a * np.sqrt(zeta - h)], [zeta - h, zeta - h], 'k--', lw=0.9)
    # parabola outlines on top of fills
    ax.plot(-a * np.sqrt(yl - h), yl, 'k-', lw=1.4, zorder=3)
    ax.plot(a * np.sqrt(yr + h), yr, 'k-', lw=1.4, zorder=3)
    ax.plot(-a * np.sqrt(yd), yd, 'k--', lw=1.0)
    ax.plot(a * np.sqrt(yd), yd, 'k--', lw=1.0)
    # axes
    _arrow(ax, (0, -0.78), (0, 1.95), lw=1.1, ms=11)
    ax.text(0.0, 2.02, r'$\mathcal{E}$', ha='center')
    _arrow(ax, (-1.5, 0), (1.6, 0), lw=1.1, ms=11)
    ax.text(1.66, 0.0, r'$\mathcal{N}(\mathcal{E})$', va='center')
    # mu_0 H brace
    _brace(ax, -0.10, -h, 0, 0.12)
    ax.text(-0.55, -0.14, r'$\mu_0 H$', ha='center', va='center')
    # curved shift arrow
    ax.annotate('', xy=(0.36, 1.06), xytext=(-0.40, 1.40),
                arrowprops=dict(arrowstyle='-|>', lw=1.1, color='k',
                                connectionstyle='arc3,rad=-0.55'), zorder=5)
    # spin arrows inside fills
    _arrow(ax, (-0.36, 0.74), (-0.36, 0.48), lw=1.8, ms=13)
    _arrow(ax, (0.38, 0.48), (0.38, 0.74), lw=1.8, ms=13)
    ax.set_xlim(-1.75, 2.15)
    ax.set_ylim(-0.85, 2.25)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, key)


# ------------------------------------------------------------------ Fig 176
def fig_176():
    key = 176
    fig, ax = plt.subplots(figsize=(3.0, 2.15))
    _arrow(ax, (0, 0), (0, 1.14), lw=1.2, ms=11)
    _arrow(ax, (0, 0), (1.32, 0), lw=1.2, ms=11)
    ax.text(-0.05, 1.12, r'$M(0)$', ha='right', va='top')
    ax.text(1.30, -0.10, r'$T$', ha='center')
    t = np.linspace(0, 1, 200)
    ax.plot(t, np.sqrt(1 - t ** 4), 'k-', lw=1.5)
    ax.plot([1, 1], [0, 0.012], 'k-', lw=1.2)
    ax.text(1.0, -0.10, r'$T_{\rm c}$', ha='center')
    ax.text(0.66, 0.80, r'$M$')
    ax.set_xlim(-0.42, 1.45)
    ax.set_ylim(-0.22, 1.28)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, key)


# ------------------------------------------------------------------ Fig 177
def fig_177():
    key = 177
    fig = plt.figure(figsize=(3.6, 4.7))
    gs = fig.add_gridspec(2, 1, height_ratios=[2.25, 1.2], hspace=0.42)
    axa = fig.add_subplot(gs[0])
    axb = fig.add_subplot(gs[1])

    # ---- (a) band ferromagnetism
    zeta = 1.0
    left = [(0.33, 2.35), (0.44, 2.02), (0.30, 1.78), (0.47, 1.52),
            (0.31, 1.28), (0.20, 1.05), (0.13, 0.72), (0.115, 0.40),
            (0.14, 0.14), (0.05, 0.04), (0.0, 0.035)]
    right = [(0.22, 2.35), (0.13, 1.95), (0.17, 1.60), (0.30, 1.30),
             (0.37, 1.12), (0.285, 1.00), (0.42, 0.90), (0.58, 0.68),
             (0.62, 0.58), (0.55, 0.42), (0.38, 0.22), (0.20, 0.07),
             (0.05, -0.06), (0.0, -0.13)]
    L = _smooth(left)
    R = _smooth(right)
    # fills
    Lf = L[L[:, 1] <= zeta]
    _hatch_poly(axa, [(0, Lf[-1, 1])] + [tuple(p) for p in Lf] + [(0, zeta)],
                '---', fc='white')
    Rf = R[R[:, 1] <= zeta]
    _hatch_poly(axa, [(0, zeta)] + [tuple(p) for p in Rf], '---', fc='white')
    # outlines
    axa.plot(-L[:, 0], L[:, 1], 'k-', lw=1.4)
    axa.plot(R[:, 0], R[:, 1], 'k-', lw=1.4)
    # zeta line
    axa.plot([-Lf[0, 0], 0], [zeta, zeta], 'k-', lw=1.2)
    axa.plot([0.30, 0.72], [zeta, zeta], 'k--', lw=1.0)
    axa.text(0.77, zeta, r'$\zeta$', va='center')
    # axes
    _arrow(axa, (0, -0.45), (0, 2.30), lw=1.1, ms=10)
    axa.text(-0.07, 2.28, r'$\mathcal{E}$', ha='right', va='top')
    axa.plot([-1.18, 1.18], [0, 0], 'k-', lw=1.1)
    _arrow(axa, (-0.62, -0.16), (-1.02, -0.16), lw=1.1, ms=10)
    axa.text(-0.55, -0.16, r'$-\frac{1}{2}\,\mathcal{N}(\mathcal{E})$',
             ha='left', va='center')
    axa.text(0.55, -0.16, r'$\frac{1}{2}\,\mathcal{N}(\mathcal{E})$',
             ha='right', va='center')
    _arrow(axa, (0.98, -0.16), (1.20, -0.16), lw=1.1, ms=10)
    # n-, n+ markers
    _arrow(axa, (-0.115, 0.84), (-0.115, 0.60), lw=1.5, ms=11)
    axa.text(-0.115, 0.47, r'$n_-$', ha='center')
    _arrow(axa, (0.135, 0.58), (0.135, 0.82), lw=1.5, ms=11)
    axa.text(0.205, 0.66, r'$n_+$', ha='left')
    axa.text(0, -0.62, r'$(a)$', ha='center')
    axa.set_xlim(-1.4, 1.42)
    axa.set_ylim(-0.72, 2.45)
    axa.axis('off')

    # ---- (b) electronic specific heat
    axb.plot([0, 0], [0, 1.9], 'k-', lw=1.2)
    axb.plot([0, 1.5], [0, 0], 'k-', lw=1.2)
    curve = _smooth([(0.0, 0.0), (0.30, 0.38), (0.55, 0.75), (0.70, 1.12),
                     (0.78, 1.48), (0.80, 1.52), (0.82, 0.98), (0.95, 0.93),
                     (1.12, 0.90), (1.30, 0.92), (1.42, 0.94)])
    axb.plot(curve[:, 0], curve[:, 1], 'k-', lw=1.4)
    axb.plot([0.78, 0.78], [0, 0.05], 'k-', lw=1.1)
    axb.text(0.78, -0.10, r'$T_{\rm c}$', ha='center', va='top')
    axb.plot([0, 0.05], [1, 1], 'k-', lw=1.1)
    axb.text(-0.08, 1.0, r'$1$', ha='right', va='center')
    axb.text(-0.10, 1.52, r'$C/nk$', ha='right')
    axb.text(0.72, -0.88, r'$(b)$', ha='center')
    axb.set_xlim(-0.52, 1.6)
    axb.set_ylim(-1.02, 2.0)
    axb.set_aspect('equal')
    axb.axis('off')
    _save(fig, key)


# ------------------------------------------------------------------ Fig 178
def fig_178():
    key = 178
    fig, ax = plt.subplots(figsize=(4.7, 2.0))
    # ---- (a) atomic d levels, polarized
    ax.plot([0.25, 2.75], [2.2, 2.2], 'k-', lw=0.8)
    ax.plot([0.95, 2.15], [2.32, 2.32], 'k-', lw=1.3)
    ax.plot([0.95, 2.15], [2.10, 2.10], 'k-', lw=1.3)
    for x in (1.10, 1.55, 2.00):
        _arrow(ax, (x, 2.34), (x, 2.62), lw=1.4, ms=9)
        ax.plot([x], [2.32], marker='o', ms=2.5, color='k')
    for x in (1.32, 1.77):
        _arrow(ax, (x, 2.08), (x, 1.80), lw=1.4, ms=9)
        ax.plot([x], [2.10], marker='o', ms=2.5, color='k')
    ax.text(1.55, 2.80, r'$\mathcal{H}_{dd}$', ha='center')
    ax.plot([1.95, 3.05], [2.45, 3.28], 'k-', lw=1.0)
    ax.plot([1.95, 3.05], [1.97, 1.12], 'k-', lw=1.0)
    # ---- (b) split by d-d interaction
    ax.plot([3.1, 4.55], [3.3, 3.3], 'k-', lw=1.3)
    ax.text(4.62, 3.30, r'$\mathcal{E}_{d-}$', va='center')
    ax.plot([3.1, 4.55], [1.1, 1.1], 'k-', lw=1.3)
    for i in range(5):
        x = 3.18 + 0.30 * i
        _arrow(ax, (x, 1.12), (x, 1.42), lw=1.4, ms=9)
    ax.text(4.66, 0.74, r'$\mathcal{E}_{d+}$', va='center')
    _arrow(ax, (3.82, 2.88), (3.82, 3.22), lw=1.3, ms=10)
    ax.text(3.82, 2.20, r'$U$', ha='center')
    _arrow(ax, (3.82, 1.52), (3.82, 1.18), lw=1.3, ms=10)
    # ---- (c) broadened into resonances
    # upper (empty) resonance
    ax.plot([4.62, 5.95], [3.60, 3.44], 'k-', lw=1.0)
    ax.plot([4.62, 5.95], [3.30, 3.42], 'k-', lw=1.0)
    ax.text(5.05, 3.72, r'$V$', ha='center')
    ax.add_patch(mpatches.Ellipse((6.75, 3.44), 1.55, 0.60, fill=False,
                                  lw=1.6, zorder=4))
    ax.text(6.75, 3.92, r'$\rho_{d-}(\mathcal{E})$', ha='center')
    _brace(ax, 7.62, 3.14, 3.74, -0.14)
    ax.text(7.88, 3.44, r'$W$', va='center')
    # s-band
    ax.plot([5.35, 9.6], [2.55, 2.55], 'k-', lw=1.2)
    ax.text(9.66, 2.55, r'$\mathcal{E}_F$', va='center')
    th = np.linspace(np.pi, 2 * np.pi, 120)
    dome_x = 7.45 + 2.13 * np.cos(th)
    dome_y = 2.55 + 1.35 * np.sin(th)
    _hatch_poly(ax, [(5.32, 2.55)] + list(zip(dome_x, dome_y)) + [(9.58, 2.55)],
                '\\\\', fc='white')
    ax.plot([5.32, 9.6], [2.55, 2.55], 'k-', lw=1.2)
    ax.text(7.45, 0.72, r'$s$-electrons', ha='center')
    # lower (occupied) resonance inside the band
    ax.add_patch(mpatches.Ellipse((7.30, 1.62), 1.75, 0.80, facecolor='white',
                                  edgecolor='k', lw=1.4, hatch='...', zorder=4))
    for ang in (30, 75, 130, 210, 260, 320):
        x = 7.30 + 0.42 * np.cos(np.radians(ang))
        y = 1.62 + 0.20 * np.sin(np.radians(ang))
        _arrow(ax, (x, y - 0.10), (x, y + 0.13), lw=1.2, ms=8, z=6)
    ax.text(8.32, 1.60, r'$\rho_{d+}(\mathcal{E})$', va='center', zorder=6)
    # funnels to the lower resonance
    ax.plot([4.62, 6.45], [1.30, 1.62], 'k-', lw=1.0, zorder=3)
    ax.plot([4.62, 6.45], [0.92, 1.56], 'k-', lw=1.0, zorder=3)
    ax.text(5.35, 1.52, r'$V$', ha='center', zorder=6)
    # panel labels
    ax.text(1.5, 0.15, r'$(a)$', ha='center')
    ax.text(3.82, 0.15, r'$(b)$', ha='center')
    ax.text(7.3, 0.15, r'$(c)$', ha='center')
    ax.set_xlim(0, 10.1)
    ax.set_ylim(0, 4.15)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, key)


# ------------------------------------------------------------------ Fig 179
def fig_179():
    key = 179
    fig, ax = plt.subplots(figsize=(3.8, 3.65))
    rng = np.random.default_rng(11)

    def zone(r):  # up / down rings (Friedel oscillation)
        if r < 0.46 or 0.66 <= r < 0.85 or r >= 0.95:
            return 1
        return -1

    imps = ((0.0, 0.03), (0.30, -0.19), (-0.42, -0.38))
    X, Y, S = [], [], []
    r = 0.10
    while r < 1.0:
        dr = 0.065 + 0.055 * r          # isotropic ring spacing
        n = max(8, int(round(2 * np.pi * r / dr)))
        for k in range(n):
            th = 2 * np.pi * k / n
            th += rng.normal(0, 0.10 * 2 * np.pi / n)
            rr = r + rng.normal(0, 0.008)
            x, y = rr * np.cos(th), rr * np.sin(th)
            if min(np.hypot(x - px, y - py) for px, py in imps) < 0.10:
                continue
            X.append(x)
            Y.append(y)
            S.append(zone(r))
        r += dr
    X, Y, S = map(np.array, (X, Y, S))
    lengths = 0.055 + 0.032 * np.sqrt(X ** 2 + Y ** 2)
    ax.quiver(X, Y, np.zeros_like(X), S * lengths,
              angles='xy', scale_units='xy', scale=1, pivot='mid',
              width=0.0028, color='k', headwidth=3.2, headlength=4,
              headaxislength=4)
    # impurities
    for (px, py), lab, up in ((imps[0], 'A', True), (imps[1], 'B', True),
                              (imps[2], 'C', False)):
        ax.add_patch(mpatches.Circle((px, py), 0.062, fill=False, lw=1.2, zorder=5))
        if up:
            _arrow(ax, (px, py - 0.045), (px, py + 0.062), lw=1.8, ms=12, z=6)
        else:
            _arrow(ax, (px, py + 0.045), (px, py - 0.062), lw=1.8, ms=12, z=6)
        ax.text(px + 0.075, py - 0.01, f'${lab}$', fontsize=11, zorder=6)
    ax.set_xlim(-1.12, 1.12)
    ax.set_ylim(-1.12, 1.12)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, key)


# ------------------------------------------------------------------ Fig 180
def fig_180():
    key = 180
    fig, axs = plt.subplots(1, 2, figsize=(4.7, 3.5))
    for ax in axs:
        ax.set_xlim(0, 4.0)
        ax.set_ylim(0, 4.6)
        ax.set_aspect('equal')
        ax.axis('off')

    ax = axs[0]  # ---------------------------- (a) direct
    v1 = (2.05, 3.30)
    v2 = (2.25, 1.85)
    # dashed |k''> line through both vertices
    u = np.array([0.137, -0.990])
    p_top = np.array(v1) - 0.50 * u
    p_bot = np.array(v2) + 1.05 * u
    ax.plot([p_top[0], p_bot[0]], [p_top[1], p_bot[1]], 'k--', lw=1.1)
    _arrow(ax, (2.34, 1.10), (2.37, 1.34), lw=0.9, ms=8)
    ax.text(2.52, 0.92, r"$(1-f_{\mathbf{k}''})$", ha='left')
    # electron path
    ax.plot([0.35, v2[0], v1[0], 0.85], [0.45, v2[1], v1[1], 4.15],
            'k-', lw=1.2, zorder=3)
    _arrow(ax, (1.00, 0.82), (1.24, 0.97), lw=1.2, ms=11)
    _arrow(ax, (2.20, 2.40), (2.16, 2.72), lw=1.2, ms=11)
    _arrow(ax, (1.76, 3.62), (1.52, 3.78), lw=1.2, ms=11)
    # small spin ticks
    _arrow(ax, (0.72, 0.60), (0.72, 0.76), lw=0.8, ms=6)
    _arrow(ax, (1.50, 1.22), (1.50, 1.38), lw=0.8, ms=6)
    _arrow(ax, (2.24, 2.12), (2.24, 1.96), lw=0.8, ms=6)
    _arrow(ax, (1.30, 3.90), (1.30, 4.06), lw=0.8, ms=6)
    # labels along electron line
    ax.text(0.42, 0.24, r'$|\mathbf{k},+\rangle$', rotation=37,
            ha='center', va='center')
    ax.text(0.58, 4.28, r"$|\mathbf{k}',+\rangle$", rotation=37,
            ha='center', va='center')
    ax.text(1.98, 2.56, r"$|\mathbf{k}'',-\rangle$", ha='right', va='center')
    # d-spin arc and ends
    _thick(ax, [v1, (3.05, 2.55), v2], lw=2.5)
    _arrow(ax, (2.98, 2.52), (2.98, 2.88), lw=1.6, ms=13)
    _thick(ax, [v2, (2.90, 1.54)], lw=2.5)
    _arrow(ax, (3.08, 1.48), (3.08, 1.14), lw=1.6, ms=13)
    ax.text(3.28, 1.18, r'$S_i$', ha='left')
    _thick(ax, [v1, (2.62, 3.70)], lw=2.5)
    _arrow(ax, (2.80, 3.80), (2.80, 3.46), lw=1.6, ms=13)
    ax.text(2.0, 0.25, r'$(a)$', ha='center')

    ax = axs[1]  # ---------------------------- (b) exchange
    v1 = (2.30, 3.30)
    v2 = (2.55, 1.75)
    # incoming electron, crosses the outgoing line
    ax.plot([0.30, v1[0]], [0.85, v1[1]], 'k-', lw=1.2, zorder=3)
    _arrow(ax, (1.00, 1.66), (1.22, 1.86), lw=1.2, ms=11)
    _arrow(ax, (1.62, 2.32), (1.62, 2.50), lw=0.8, ms=6)
    _arrow(ax, (1.98, 2.70), (1.98, 2.88), lw=0.8, ms=6)
    ax.text(0.30, 0.62, r'$|\mathbf{k},+\rangle$', rotation=43,
            ha='center', va='center')
    # outgoing |k',+> line: v2 -> upper-left, gap at the crossing
    q0 = np.array(v2, float)
    end = np.array([0.35, 3.11])
    d = (end - q0) / np.linalg.norm(end - q0)
    g1 = q0 + 0.62 * (end - q0)
    g0 = q0 + 0.50 * (end - q0)
    ax.plot([v2[0], g1[0]], [v2[1], g1[1]], 'k-', lw=1.2, zorder=3)
    ax.plot([g0[0], end[0]], [g0[1], end[1]], 'k-', lw=1.2, zorder=3)
    _arrow(ax, (0.80, 2.92), (0.62, 3.05), lw=1.2, ms=11)
    ax.text(0.32, 3.42, r"$|\mathbf{k}',+\rangle$", rotation=-31,
            ha='center', va='center')
    # occupied |k''> line below v2
    ax.plot([v2[0], 2.92], [v2[1], 1.12], 'k-', lw=1.2, zorder=3)
    ax.plot([2.92, 3.28], [1.12, 0.35], 'k--', lw=1.1)
    _arrow(ax, (2.86, 1.14), (2.81, 1.38), lw=0.9, ms=8)
    _arrow(ax, (3.05, 0.78), (3.01, 0.96), lw=0.8, ms=6)
    ax.text(2.72, 0.88, r"$|\mathbf{k}'',-\rangle$", ha='right')
    ax.text(3.30, 0.68, r"$f_{\mathbf{k}''}$", ha='left')
    # d-spin arc and ends
    _thick(ax, [v1, (3.55, 2.55), v2], lw=2.5)
    _arrow(ax, (3.48, 2.72), (3.48, 2.36), lw=1.6, ms=13)
    _thick(ax, [v1, (3.12, 3.88)], lw=2.5)
    _arrow(ax, (3.36, 3.94), (3.36, 4.28), lw=1.6, ms=13)
    _thick(ax, [v2, (3.22, 1.38)], lw=2.5)
    _arrow(ax, (3.44, 1.28), (3.44, 1.64), lw=1.6, ms=13)
    ax.text(3.62, 1.40, r'$S_i$', ha='left')
    ax.text(2.1, 0.15, r'$(b)$', ha='center')
    _save(fig, key)


# ------------------------------------------------------------------ Fig 181
def fig_181():
    key = 181
    fig, axs = plt.subplots(1, 2, figsize=(4.1, 2.1))
    pat_b = [[1, -1, 1, -1], [-1, 1, -1, 1], [1, -1, 1, -1], [-1, 1, -1, 1]]
    for ax, spins, lab in ((axs[0], [[1] * 4] * 4, 'a'), (axs[1], pat_b, 'b')):
        for i in range(4):        # rows (top to bottom)
            for j in range(4):    # columns
                x, y = j * 0.78, (3 - i) * 0.78
                _spin_dot_circle(ax, (x, y), 0.29, up=(spins[i][j] > 0),
                                 alen=0.30, arrow_lw=1.4, ms=10)
        ax.text(1.17, -1.15, f'$({lab})$', ha='center')
        ax.set_xlim(-0.75, 3.1)
        ax.set_ylim(-1.45, 2.85)
        ax.set_aspect('equal')
        ax.axis('off')
    fig.subplots_adjust(wspace=0.25)
    _save(fig, key)


# ------------------------------------------------------------------ Fig 182
def fig_182():
    key = 182
    fig, axs = plt.subplots(1, 3, figsize=(4.8, 1.8),
                            gridspec_kw=dict(width_ratios=[1, 1, 1.9]))

    ax = axs[0]  # (a) H || mu
    _arrow(ax, (0.62, 1.95), (0.62, 1.18), lw=2.4, ms=16)
    ax.text(0.50, 1.90, r'$\mu_-$', ha='right')
    _arrow(ax, (1.02, 1.14), (1.02, 1.80), lw=2.4, ms=16, ls='--')
    ax.text(1.10, 1.44, r'$H$', ha='left')
    _arrow(ax, (0.62, 0.28), (0.62, 1.04), lw=2.4, ms=16)
    ax.text(0.50, 0.34, r'$\mu_+$', ha='right')
    ax.text(0.78, 0.02, r'$(a)$', ha='center')
    ax.set_xlim(0, 1.9)
    ax.set_ylim(0, 2.3)

    ax = axs[1]  # (b) H perp mu
    _arrow(ax, (0.50, 1.02), (1.32, 1.02), lw=2.4, ms=16, ls='--')
    ax.text(1.14, 1.15, r'$H$', ha='center')
    _arrow(ax, (0.38, 1.62), (0.80, 1.12), lw=2.4, ms=16)
    ax.text(0.32, 1.70, r'$\mu_-$', ha='right')
    _arrow(ax, (0.38, 0.42), (0.80, 0.92), lw=2.4, ms=16)
    ax.text(0.88, 0.40, r'$\mu_+$', ha='left')
    ax.text(0.78, 0.02, r'$(b)$', ha='center')
    ax.set_xlim(0, 1.9)
    ax.set_ylim(0, 2.3)

    ax = axs[2]  # (c) susceptibilities
    TN = 0.78
    _arrow(ax, (0, 0), (0, 1.42), lw=1.1, ms=10)
    _arrow(ax, (0, 0), (1.68, 0), lw=1.1, ms=10)
    ax.text(-0.06, 1.40, r'$\chi$', ha='right')
    ax.text(1.66, -0.14, r'$T$', ha='center')
    u = np.linspace(0, 1, 100)
    chi_perp = 1 - 0.10 * (1 - u) ** 2
    chi_par = u ** 2.5
    chi_av = chi_par / 3 + 2 * chi_perp / 3
    ax.plot([0, TN], [1, 1], 'k--', lw=0.9)
    ax.plot(u * TN, chi_perp, 'k-', lw=1.4)
    ax.plot(u * TN, chi_par, 'k--', lw=1.2)
    ax.plot(u * TN, chi_av, 'k-', lw=1.4)
    Th = np.linspace(TN, 1.60, 60)
    ax.plot(Th, (TN + 0.27) / (Th + 0.27), 'k-', lw=1.4)
    ax.plot([TN, TN], [0, 1], 'k--', lw=0.9)
    ax.text(0.40, 1.08, r'$\chi_\perp$', ha='center')
    ax.text(0.42, 0.87, r'$\chi$', ha='center')
    ax.text(0.30, 0.28, r'$\chi_\parallel$', ha='center')
    ax.text(1.40, 0.94, r'$\frac{1}{T+\theta}$', ha='center')
    ax.text(TN, -0.16, r'$T_N$', ha='center')
    ax.text(0.95, -0.42, r'$(c)$', ha='center')
    ax.set_xlim(-0.16, 1.8)
    ax.set_ylim(-0.52, 1.62)
    for ax in axs:
        ax.axis('off')
    fig.subplots_adjust(wspace=0.05)
    _save(fig, key)


# ------------------------------------------------------------------ Fig 183
def fig_183():
    key = 183
    fig, ax = plt.subplots(figsize=(2.6, 2.5))
    for i in range(3):        # row (top->bottom)
        for j in range(3):    # col
            x, y = (j - 1) * 1.05, (1 - i) * 1.05
            corner = (i in (0, 2)) and (j in (0, 2))
            edge = (i + j) % 2 == 1
            if corner:
                _spin_dot_circle(ax, (x, y), 0.42, up=False, alen=0.50,
                                 arrow_lw=2.0, ms=15)
            elif edge:
                _spin_dot_circle(ax, (x, y), 0.24, up=True, alen=0.28,
                                 arrow_lw=1.6, ms=11)
            else:  # centre
                _spin_dot_circle(ax, (x, y), 0.30, up=False, alen=0.36,
                                 arrow_lw=1.8, ms=13)
    ax.set_xlim(-1.85, 1.85)
    ax.set_ylim(-1.85, 1.85)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, key)


# ------------------------------------------------------------------ Fig 184
def fig_184():
    key = 184
    fig, ax = plt.subplots(figsize=(4.1, 1.7))
    # ion A (up spins)
    ax.add_patch(mpatches.Circle((0, 0), 0.62, facecolor='white',
                                 edgecolor='k', lw=1.2, hatch='...', zorder=3))
    ax.add_patch(mpatches.Circle((0, 0), 0.40, fill=False, lw=1.0, zorder=4))
    ax.add_patch(mpatches.Circle((0, 0), 0.045, color='k', zorder=5))
    for ang in (35, 90, 145, 215, 270, 325):
        x = 0.23 * np.cos(np.radians(ang))
        y = 0.21 * np.sin(np.radians(ang))
        _arrow(ax, (x, y - 0.09), (x, y + 0.13), lw=1.1, ms=8, z=6)
    # ion O
    ax.add_patch(mpatches.Circle((1.55, 0), 0.28, facecolor='white',
                                 edgecolor='k', lw=1.1, hatch='...', zorder=3))
    ax.add_patch(mpatches.Circle((1.55, 0), 0.10, fill=False, lw=0.9, zorder=4))
    ax.add_patch(mpatches.Circle((1.55, 0), 0.04, color='k', zorder=5))
    # ion B (down spins)
    ax.add_patch(mpatches.Circle((3.1, 0), 0.62, facecolor='white',
                                 edgecolor='k', lw=1.2, hatch='...', zorder=3))
    ax.add_patch(mpatches.Circle((3.1, 0), 0.40, fill=False, lw=1.0, zorder=4))
    ax.add_patch(mpatches.Circle((3.1, 0), 0.045, color='k', zorder=5))
    for ang in (35, 90, 145, 215, 270, 325):
        x = 3.1 + 0.23 * np.cos(np.radians(ang))
        y = 0.21 * np.sin(np.radians(ang))
        _arrow(ax, (x, y + 0.09), (x, y - 0.13), lw=1.1, ms=8, z=6)
    # p-electron paths A-O-B
    for s in (1, -1):
        xy = _bezier((0.376, s * 0.137), (0.95, s * 0.36), (1.45, s * 0.07))
        ax.plot(xy[:, 0], xy[:, 1], 'k-', lw=1.1, zorder=2)
        xy = _bezier((1.65, s * 0.07), (2.18, s * 0.36), (2.724, s * 0.137))
        ax.plot(xy[:, 0], xy[:, 1], 'k-', lw=1.1, zorder=2)
    _arrow(ax, (2.40, 0.24), (2.40, 0.42), lw=1.1, ms=9)
    ax.text(2.28, 0.33, r'$p$', ha='right', va='center')
    _arrow(ax, (0.92, -0.26), (0.92, -0.44), lw=1.1, ms=9)
    ax.text(1.02, -0.38, r'$p$', ha='left', va='center')
    # d-electron label
    ax.plot([3.50, 3.74], [-0.04, -0.12], 'k-', lw=0.9)
    ax.text(3.80, -0.14, r'$d$', ha='left', va='center')
    ax.text(0, -0.82, r'$A$', ha='center')
    ax.text(1.55, -0.46, r'$O$', ha='center')
    ax.text(3.1, -0.82, r'$B$', ha='center')
    ax.set_xlim(-0.85, 4.15)
    ax.set_ylim(-0.95, 0.62)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, key)


# ------------------------------------------------------------------ Fig 185
def fig_185():
    key = 185
    conf = ['++-+', '+-++', '+-+-', '-++-']
    fig, axs = plt.subplots(2, 2, figsize=(4.6, 4.5))

    # (a) +/- symbols
    ax = axs[0, 0]
    for i in range(4):
        for j in range(4):
            x, y = j * 0.62, (3 - i) * 0.62
            if conf[i][j] == '+':
                ax.plot([x - 0.11, x + 0.11], [y, y], 'k-', lw=1.2)
                ax.plot([x, x], [y - 0.11, y + 0.11], 'k-', lw=1.2)
            else:
                ax.plot([x - 0.11, x + 0.11], [y, y], 'k-', lw=1.2)
    ax.text(0.93, -0.75, r'$(a)$', ha='center')
    ax.set_xlim(-0.55, 2.45)
    ax.set_ylim(-1.05, 2.35)
    ax.set_aspect('equal')
    ax.axis('off')

    # (b) spins
    ax = axs[0, 1]
    for i in range(4):
        for j in range(4):
            _spin_dot_circle(ax, (j * 0.66, (3 - i) * 0.62), 0.20,
                             up=(conf[i][j] == '+'), alen=0.24,
                             arrow_lw=1.2, ms=9)
    ax.text(0.99, -0.72, r'$(b)$', ha='center')
    ax.set_xlim(-0.55, 2.55)
    ax.set_ylim(-1.02, 2.35)
    ax.set_aspect('equal')
    ax.axis('off')

    # (c) binary alloy
    ax = axs[1, 0]
    for i in range(4):
        for j in range(4):
            x, y = j * 0.62, (3 - i) * 0.62
            if conf[i][j] == '+':
                ax.add_patch(mpatches.Circle((x, y), 0.21, facecolor='white',
                                             edgecolor='k', lw=1.0,
                                             hatch='\\\\', zorder=3))
            else:
                ax.add_patch(mpatches.Circle((x, y), 0.21, fill=False,
                                             lw=1.0, zorder=3))
            ax.text(x, y, 'A' if conf[i][j] == '+' else 'B', style='italic',
                    ha='center', va='center', fontsize=10, zorder=4)
    ax.text(0.93, -0.75, r'$(c)$', ha='center')
    ax.set_xlim(-0.55, 2.45)
    ax.set_ylim(-1.05, 2.35)
    ax.set_aspect('equal')
    ax.axis('off')

    # (d) lattice gas
    ax = axs[1, 1]
    c = 0.56
    for i in range(5):
        ax.plot([0, 4 * c], [i * c, i * c], 'k-', lw=1.0)
        ax.plot([i * c, i * c], [0, 4 * c], 'k-', lw=1.0)
    for i in range(4):
        for j in range(4):
            if conf[i][j] == '+':
                ax.add_patch(mpatches.Circle(((j + 0.5) * c, (3.5 - i) * c),
                                             0.17, facecolor='white',
                                             edgecolor='k', lw=0.9,
                                             hatch='\\\\', zorder=3))
    ax.text(1.12, -0.52, r'$(d)$', ha='center')
    ax.set_xlim(-0.35, 2.6)
    ax.set_ylim(-0.85, 2.6)
    ax.set_aspect('equal')
    ax.axis('off')

    fig.subplots_adjust(wspace=0.12, hspace=0.10)
    _save(fig, key)


# ------------------------------------------------------------------ Fig 186
def fig_186():
    key = 186
    fig, ax = plt.subplots(figsize=(3.6, 3.5))

    def syms(row, x0, y):
        for k, ch in enumerate(row):
            x = x0 + 0.42 * k
            if ch == '+':
                ax.plot([x - 0.10, x + 0.10], [y, y], 'k-', lw=1.2)
                ax.plot([x, x], [y - 0.10, y + 0.10], 'k-', lw=1.2)
            else:
                ax.plot([x - 0.10, x + 0.10], [y, y], 'k-', lw=1.2)

    def box(x0, x1, y0, y1):
        ax.add_patch(mpatches.Rectangle((x0, y0), x1 - x0, y1 - y0,
                                        fill=False, edgecolor='k', lw=1.1,
                                        ls=(0, (4, 3))))

    # N_AB = 1 (2 chains)
    box(0.30, 2.62, 4.95, 6.20)
    syms('+++--', 0.72, 5.90)
    syms('--+++', 0.72, 5.30)
    ax.text(1.46, 4.60, r'$N_{AB}=1$', ha='center')
    # N_AB = 3 (4 chains)
    box(3.55, 5.87, 3.30, 6.20)
    syms('++-+-', 3.97, 5.90)
    syms('-+--+', 3.97, 5.18)
    syms('+-++-', 3.97, 4.46)
    syms('-+-++', 3.97, 3.74)
    ax.text(4.71, 2.95, r'$N_{AB}=3$', ha='center')
    # N_AB = 2 (3 chains)
    box(0.30, 2.62, 1.10, 3.45)
    syms('++--+', 0.72, 3.15)
    syms('+--++', 0.72, 2.43)
    syms('-+++-', 0.72, 1.71)
    ax.text(1.46, 0.75, r'$N_{AB}=2$', ha='center')
    # N_AB = 4 (1 chain)
    box(3.55, 5.87, 0.85, 1.60)
    syms('+-+-+', 3.97, 1.22)
    ax.text(4.71, 0.45, r'$N_{AB}=4$', ha='center')

    ax.set_xlim(0, 6.2)
    ax.set_ylim(0, 6.6)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, key)


# --------------------------------------------------------------------- main
if __name__ == '__main__':
    for f in (fig_175, fig_176, fig_177, fig_178, fig_179, fig_180,
              fig_181, fig_182, fig_183, fig_184, fig_185, fig_186):
        f()
