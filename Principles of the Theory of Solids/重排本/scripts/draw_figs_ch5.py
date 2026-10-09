# -*- coding: utf-8 -*-
"""Ziman, Principles of the Theory of Solids, 2nd ed. Chapter 5.
Redraw Figs. 86-96 as black-and-white textbook-style vector figures."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.path as mpath
from matplotlib.patches import (Circle, Rectangle, Polygon, FancyBboxPatch,
                                Arc, PathPatch)
from matplotlib.backends.backend_pdf import PdfPages  # noqa: F401
import numpy as np
import os

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
    'hatch.linewidth': 0.6,
})

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
PRE = os.path.join(OUT, 'preview')
os.makedirs(PRE, exist_ok=True)

Path = mpath.Path


def _save(fig, key):
    fig.savefig(os.path.join(OUT, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRE, 'fig_%s.png' % key),
                bbox_inches='tight', pad_inches=0.03, dpi=220)
    plt.close(fig)
    print('saved fig_%s' % key)


def _arrow(ax, x0, y0, x1, y1, style='-|>', lw=1.2, rad=0.0, ms=7):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, lw=lw,
                                mutation_scale=ms,
                                connectionstyle='arc3,rad=%g' % rad),
                annotation_clip=False)


def _brace(ax, x0, x1, y, depth, up=True, lw=1.0):
    """Curly brace along x from x0 to x1 at level y, cusp pointing up/down."""
    xm = 0.5 * (x0 + x1)
    s = depth if up else -depth
    verts = [(x0, y),
             (xm - 0.12 * (x1 - x0), y + 1.45 * s), (xm, y + s),
             (xm + 0.12 * (x1 - x0), y + 1.45 * s), (x1, y)]
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3]
    ax.add_patch(PathPatch(Path(verts, codes), fill=False,
                                 lw=lw, edgecolor='black', capstyle='round'))


# ---------------------------------------------------------------- Fig. 86
def fig_86():
    fig, ax = plt.subplots(figsize=(4.6, 2.0))
    c, yF, dU = 0.72, 2.6, 0.55
    xL, xR = 2.6, 7.6

    # axes: vertical (E) through left well, baseline with O
    ax.plot([xL, xL], [0, 3.72], color='black', lw=1.0)
    _arrow(ax, xL, 3.72, xL, 4.05, lw=1.0)
    ax.text(xL - 0.18, 3.95, r'$\mathcal{E}$', fontsize=12, ha='right')
    ax.plot([0.4, 9.95], [0, 0], color='black', lw=1.0)
    ax.text(0.22, -0.34, r'$O$', fontsize=11, ha='center')

    # left well (filled up to E_F) and its surface line
    xs = np.linspace(xL - 1.9, xL + 1.9, 200)
    parL = c * (xs - xL) ** 2
    ax.fill_between(xs, 0, np.minimum(parL, yF), color='0.86', lw=0)
    xa = np.linspace(xL - 2.02, xL + 2.02, 200)
    ax.plot(xa, c * (xa - xL) ** 2, color='black', lw=1.3)
    ax.plot([xL - 1.9, xL + 1.9], [yF, yF], color='black', lw=1.3)
    ax.text(xL - 1.9 - 0.12, yF, r'$\mathcal{E}_F$', fontsize=11,
            ha='right', va='center')

    # dashed Fermi level (zeta) to the right
    ax.plot([xL + 1.9, 10.05], [yF, yF], color='black', lw=1.0,
            linestyle=(0, (5, 3)))
    ax.text(10.18, yF, r'$\zeta$', fontsize=12, ha='left', va='center')

    # right well, lifted by delta-U, filled up to zeta + delta-U
    top = yF + dU
    xs2 = np.linspace(xR - 1.9, xR + 1.9, 200)
    parR = dU + c * (xs2 - xR) ** 2
    ax.fill_between(xs2, parR, top, color='0.86', lw=0)
    xb = np.linspace(xR - 2.02, xR + 2.02, 200)
    ax.plot(xb, dU + c * (xb - xR) ** 2, color='black', lw=1.3)
    ax.plot([xR - 1.9, xR + 1.9], [top, top], color='black', lw=1.3)
    # centre line of right well
    ax.plot([xR, xR], [dU, 3.42], color='black', lw=0.8)

    # delta-U double arrow
    _arrow(ax, xR, -0.02, xR, dU, style='<|-|>', lw=1.0, ms=10)
    ax.text(xR + 0.22, dU / 2, r'$\delta\mathcal{U}$', fontsize=11,
            ha='left', va='center')

    # electrons and flow arrow (away from the raised region)
    ax.plot([xL + 1.9], [yF], marker='o', ms=5.5, color='black')
    ax.plot([6.6], [top], marker='o', ms=5.5, color='black')
    _arrow(ax, 6.60, top + 0.10, xL + 2.08, yF + 0.12, rad=0.45, lw=1.1)

    ax.set_xlim(-0.35, 10.85)
    ax.set_ylim(-0.62, 4.35)
    ax.set_aspect('auto')
    ax.axis('off')
    _save(fig, '86')


# ---------------------------------------------------------------- Fig. 87
def fig_87():
    fig, ax = plt.subplots(figsize=(4.8, 2.45))

    # ---- (a) divalent impurity in monovalent metal
    ax.add_patch(Rectangle((0, 0), 4.6, 3.5, fill=False, lw=1.3))
    cols, rows, r = [1.0, 2.3, 3.6], [0.70, 1.75, 2.80], 0.46
    for i, cx in enumerate(cols):
        for j, cy in enumerate(rows):
            if i == 1 and j == 1:
                ax.add_patch(Circle((cx, cy), r, facecolor='0.85',
                                    edgecolor='black', lw=1.7))
                ax.add_patch(Circle((cx, cy), r - 0.07, facecolor='none',
                                    edgecolor='black', lw=0.8))
                ax.text(cx, cy, r'Zn$^{++}$', ha='center', va='center',
                        fontsize=9)
            else:
                ax.add_patch(Circle((cx, cy), r, facecolor='0.85',
                                    edgecolor='black', lw=1.1))
                ax.text(cx, cy, r'Cu$^+$', ha='center', va='center',
                        fontsize=9)
    els = [(2.85, 3.28, (2.99, 3.36), 'left'),
           (1.75, 2.92, (1.80, 2.62), 'left'),
           (0.50, 2.22, (0.64, 2.16), 'left'),
           (1.88, 2.24, (2.03, 2.33), 'left'),
           (2.92, 2.34, (3.06, 2.42), 'left'),
           (3.80, 2.32, (3.94, 2.40), 'left'),
           (1.28, 1.12, (1.42, 1.08), 'left'),
           (2.45, 1.08, (2.59, 1.14), 'left'),
           (4.10, 1.32, (4.18, 1.12), 'left'),
           (2.68, 0.50, (2.84, 0.40), 'left')]
    for ex, ey, tx, ha in els:
        ax.plot([ex], [ey], marker='o', ms=4.5, color='black')
        ax.text(tx[0], tx[1], r'$e^-$', fontsize=9, ha=ha, va='center')
    ax.text(2.3, -0.32, r'$(a)$', ha='center', fontsize=11)

    # ---- (b) point charge in a continuum
    x0 = 5.5
    ax.add_patch(Rectangle((x0, 0), 4.6, 3.5, fill=False, lw=1.3))
    rng = np.random.default_rng(7)
    n = 2600
    px = rng.uniform(x0 + 0.03, x0 + 4.57, n)
    py = rng.uniform(0.03, 3.47, n)
    keep = rng.random(n) < 0.62
    ax.scatter(px[keep], py[keep], s=rng.uniform(0.5, 2.6, keep.sum()),
               c=rng.uniform(0.25, 0.62, keep.sum()), cmap='gray',
               vmin=0.1, vmax=0.7, lw=0, marker='o')
    ax.add_patch(Circle((x0 + 2.3, 1.75), 0.30, facecolor='white',
                        edgecolor='black', lw=1.1, zorder=5))
    ax.text(x0 + 2.3, 1.75, r'$+$', ha='center', va='center', fontsize=12,
            zorder=6)
    for ex, ey, tx, ha in els:
        ax.plot([ex + x0], [ey], marker='o', ms=4.5, color='black',
                zorder=6)
        ax.text(tx[0] + x0, tx[1], r'$e^-$', fontsize=9, ha=ha,
                va='center', zorder=6)
    ax.text(x0 + 2.3, -0.32, r'$(b)$', ha='center', fontsize=11)

    ax.set_xlim(-0.25, 10.35)
    ax.set_ylim(-0.55, 3.75)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '87')


# ---------------------------------------------------------------- Fig. 88
def _bez(*pts, n=40):
    """Sample a Bezier curve through the given control points (3=quadratic,
    4=cubic)."""
    t = np.linspace(0, 1, n)[:, None]
    if len(pts) == 3:
        p0, p1, p2 = (np.array(p) for p in pts)
        return ((1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2)
    p0, p1, p2, p3 = (np.array(p) for p in pts)
    return ((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)


def fig_88():
    fig = plt.figure(figsize=(4.9, 1.9))
    fr = [0.02, 0.30, 0.29, 0.68], [0.355, 0.30, 0.29, 0.68], \
         [0.69, 0.30, 0.29, 0.68]
    for k in range(3):
        ax = fig.add_axes(fr[k])
        ax.set_xlim(0, 10)
        ax.set_ylim(-6.4, 1.7)
        ax.axis('off')
        # vertical E axis and horizontal r axis (at the top, v = 0)
        ax.plot([0.7, 0.7], [-6.0, 1.05], color='black', lw=1.0)
        _arrow(ax, 0.7, 1.05, 0.7, 1.62, lw=1.0)
        ax.text(0.42, 1.38, r'$\mathcal{E}$', fontsize=11, ha='right')
        ax.plot([0.7, 9.45], [0, 0], color='black', lw=1.0)
        _arrow(ax, 9.45, 0, 9.95, 0, lw=1.0)
        ax.text(9.05, 0.30, r'$r$', fontsize=11, ha='left')
        if k == 0:
            x = np.linspace(0.95, 9.5, 200)
            ax.plot(x, -2.55 / (x - 0.42), color='black', lw=1.4)
            ax.text(1.55, -4.35, r'$v_b(r)$', fontsize=10)
            ax.text(5.5, -1.80, r'$-\dfrac{Ze^2}{r}$', fontsize=11)
            ax.text(5.0, -7.15, r'$(a)$', ha='center', fontsize=11)
            _arrow(ax, 10.7, -2.6, 12.3, -2.6, lw=1.1)
        elif k == 1:
            rc, A = 2.9, -1.5
            ax.plot([0.8, rc], [A, A], color='black', lw=1.4)
            ax.plot([rc, rc], [-1.85, 0.55], color='black', lw=0.9,
                    linestyle=(0, (4, 3)))
            ax.text(rc, 0.78, r'$r_c$', fontsize=11, ha='center')
            ax.text(1.75, -1.12, r'$A$', fontsize=11)
            m, K = 1.7, 2.34
            x = np.linspace(3.02, 9.5, 200)
            ax.plot(x, -K / (x - m), color='black', lw=1.4)
            ax.text(4.35, -2.75, r'$w_b(r)$', fontsize=10)
            ax.text(7.15, -1.65, r'$-\dfrac{Ze^2}{r}$', fontsize=11)
            ax.text(5.0, -7.15, r'$(b)$', ha='center', fontsize=11)
            _arrow(ax, 10.7, -2.6, 12.3, -2.6, lw=1.1)
        else:
            rc, A = 2.9, -1.5
            ax.plot([0.8, rc - 0.04], [A, A], color='black', lw=1.4)
            ax.plot([rc, rc], [-3.6, 0.55], color='black', lw=0.9,
                    linestyle=(0, (4, 3)))
            ax.text(rc, 0.78, r'$r_c$', fontsize=11, ha='center')
            p = _bez((rc - 0.04, A), (rc + 0.02, -2.6), (rc + 0.16, -3.3))
            q = _bez((rc + 0.16, -3.3), (rc + 0.34, -3.55), (3.5, -0.52))
            x = np.linspace(3.5, 9.5, 200)
            tail = -0.52 * (3.5 / x) ** 1.16
            ax.plot(np.r_[p[:, 0], q[:, 0], x],
                    np.r_[p[:, 1], q[:, 1], tail], color='black', lw=1.4)
            ax.text(4.15, -2.75, r'$w_s(r)$', fontsize=10)
            ax.text(6.75, -1.60, r'$-\dfrac{Ze^2}{r}\,e^{-\lambda r}$',
                    fontsize=11)
            ax.text(5.0, -7.15, r'$(c)$', ha='center', fontsize=11)
    _save(fig, '88')


# ---------------------------------------------------------------- Fig. 89
def fig_89():
    fig, ax = plt.subplots(figsize=(4.4, 2.85))
    rng = np.random.default_rng(5)
    cols = [0.95, 2.25, 3.55, 4.85]
    rows = [0.80, 1.90, 3.00]
    rc = 0.30
    R = 0.80
    centers = [(cx, cy) for cy in rows for cx in cols]
    # displaced ion in the middle row (2nd column -> shifted right by half)
    centers = [(x, y) for (x, y) in centers]
    disp = [(cols[1] + 0.66, rows[1]) if (x == cols[1] and y == rows[1])
            else (x, y) for (x, y) in centers]
    for (cx, cy) in disp:
        n = 430
        th = rng.uniform(0, 2 * np.pi, n)
        rr = R * rng.uniform(0, 1, n) ** 0.42
        px = cx + rr * np.cos(th)
        py = cy + rr * np.sin(th)
        w = rng.uniform(0.35, 1.0, n)
        ax.scatter(px, py, s=0.7 + 1.4 * w ** 2,
                   c=0.30 + 0.35 * (1 - w), cmap='gray', vmin=0.2,
                   vmax=0.75, lw=0, marker='o')
        ax.add_patch(Circle((cx, cy), rc, facecolor='black',
                            edgecolor='black', zorder=5))
    ax.set_xlim(0.0, 5.8)
    ax.set_ylim(0.0, 3.85)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '89')


# ---------------------------------------------------------------- Fig. 90
def fig_90():
    fig, ax = plt.subplots(figsize=(3.7, 2.15))
    ax.plot([0, 0], [0, 1.24], color='black', lw=1.0)
    _arrow(ax, 0, 1.24, 0, 1.38, lw=1.0)
    ax.text(-0.10, 1.32, r'$\lambda$', fontsize=12, ha='right')
    ax.plot([0, 3.02], [0, 0], color='black', lw=1.0)
    _arrow(ax, 3.02, 0, 3.22, 0, lw=1.0)
    ax.text(3.10, -0.10, r'$q$', fontsize=12, ha='left', va='top')
    ax.text(-0.06, -0.05, r'$O$', fontsize=11, ha='right', va='top')

    x1 = np.linspace(0.012, 1.0, 300)
    y1 = 0.18 + 0.82 * (1 - x1 ** 2) ** 0.75
    x2 = np.linspace(1.0, 3.0, 150)
    y2 = 0.18 / (1 + 1.3 * (x2 - 1)) ** 0.7
    ax.plot(np.r_[x1, x2], np.r_[y1, y2], color='black', lw=1.4)
    ax.plot([1, 1], [0, 0.18], color='black', lw=0.9, linestyle=(0, (4, 3)))
    ax.text(1.0, -0.10, r'$2k_{\mathcal{F}}$', fontsize=11, ha='center',
            va='top')
    ax.set_xlim(-0.32, 3.35)
    ax.set_ylim(-0.28, 1.5)
    ax.axis('off')
    _save(fig, '90')


# ---------------------------------------------------------------- Fig. 91
def _arc(cx, cy, r, a0, a1, n=100):
    a = np.radians(np.linspace(a0, a1, n))
    return cx + r * np.cos(a), cy + r * np.sin(a)


def fig_91():
    fig, ax = plt.subplots(figsize=(4.9, 1.55))

    # ---- (a) small q
    C = (0.0, 0.0)
    ax.add_patch(Circle((C[0] - 0.55, C[1]), 1.0, facecolor='none',
                        edgecolor='black', lw=1.0, linestyle=(0, (4, 3))))
    ax.add_patch(Circle(C, 1.0, facecolor='0.87', edgecolor='black',
                        lw=1.1))
    # crescent: shifted circle (0.55,0) minus solid circle
    xo, yo = _arc(0.55, 0, 1.0, 106, -106)
    xi_, yi = _arc(0, 0, 1.0, -74, 74)
    verts = list(zip(xo, yo)) + list(zip(xi_, yi)) + [(xo[0], yo[0])]
    codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 1)
    ax.add_patch(PathPatch(Path(verts, codes), facecolor='white',
                                 edgecolor='black', lw=0.9, hatch='///'))
    ax.plot([0], [0], marker='o', ms=3.5, color='black')
    _arrow(ax, 0.46, -0.02, 0.04, -0.02, lw=1.2)
    ax.text(0.16, -0.40, r'$\mathbf{q}$', fontsize=11, ha='center')
    _arrow(ax, 0, 0, 0.62, -0.75, lw=1.1)
    ax.text(0.70, -0.55, r'$k_{\mathcal{F}}$', fontsize=9.5, ha='left')
    _arrow(ax, 0.82, 0.60, 1.42, 0.74, lw=1.1)
    _arrow(ax, 1.0, 0.26, 1.60, 0.34, lw=1.1)
    ax.text(0.0, -1.72, r'$(a)$', ha='center', fontsize=11)

    # ---- (b) q < 2 kF
    X = 4.0
    ax.add_patch(Circle((X + 1.3, 0), 1.0, facecolor='white',
                        edgecolor='black', lw=1.1, hatch='///'))
    a = np.degrees(np.arccos(0.65))
    xl, yl = _arc(X, 0, 1.0, a, -a)
    xr, yr = _arc(X + 1.3, 0, 1.0, 180 - a, 180 + a)
    verts = list(zip(xl, yl)) + list(zip(xr, yr)) + [(xl[0], yl[0])]
    codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 1)
    ax.add_patch(PathPatch(Path(verts, codes), facecolor='0.87',
                                 edgecolor='none', zorder=4))
    ax.add_patch(Circle((X, 0), 1.0, facecolor='none', edgecolor='black',
                        lw=1.0, linestyle=(0, (4, 3)), zorder=5))
    ax.add_patch(Circle((X + 1.3, 0), 1.0, facecolor='none',
                        edgecolor='black', lw=1.1, zorder=6))
    _arrow(ax, X, 0, X + 1.26, 0, lw=1.2)
    ax.text(X + 0.50, -0.38, r'$\mathbf{q}$', fontsize=11)
    _arrow(ax, X + 0.78, 0.60, X + 2.92, 0.60, lw=1.1)
    _arrow(ax, X + 0.88, -0.55, X + 2.92, -0.55, lw=1.1)
    ax.text(X + 0.65, -1.72, r'$(b)$', ha='center', fontsize=11)

    # ---- (c) q > 2 kF
    X = 9.0
    ax.add_patch(Circle((X + 2.05, 0), 1.0, facecolor='white',
                        edgecolor='black', lw=1.1, hatch='///'))
    ax.add_patch(Circle((X, 0), 1.0, facecolor='none', edgecolor='black',
                        lw=1.0, linestyle=(0, (4, 3))))
    ax.add_patch(Circle((X + 2.05, 0), 1.0, facecolor='none',
                        edgecolor='black', lw=1.1))
    _arrow(ax, X, 0, X + 2.01, 0, lw=1.2)
    ax.text(X + 0.95, -0.38, r'$\mathbf{q}$', fontsize=11)
    _arrow(ax, X + 1.05, 0.60, X + 3.62, 0.60, lw=1.1)
    _arrow(ax, X + 1.20, -0.48, X + 3.72, -0.48, lw=1.1)
    ax.text(X + 1.0, -1.72, r'$(c)$', ha='center', fontsize=11)

    ax.set_xlim(-2.05, 13.1)
    ax.set_ylim(-1.95, 1.75)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '91')


# ---------------------------------------------------------------- Fig. 92
def fig_92():
    fig, ax = plt.subplots(figsize=(4.9, 2.5))

    # ---- (a) Kohn anomaly: parallel tangents
    ax.add_patch(FancyBboxPatch((-1.2, -1.2), 2.4, 2.4,
                                boxstyle='round,pad=0.0,rounding_size=0.38',
                                facecolor='none', edgecolor='black', lw=1.1,
                                linestyle=(0, (5, 3))))
    ax.add_patch(FancyBboxPatch((0.35, -0.45), 2.4, 2.4,
                                boxstyle='round,pad=0.0,rounding_size=0.38',
                                facecolor='white', edgecolor='black',
                                lw=1.2, hatch='///'))
    ax.plot([0], [0], marker='o', ms=5, color='black')
    ax.plot([0, 0.35], [0, 0.14], color='black', lw=1.2)
    ax.text(0.12, -0.28, r'$\mathbf{q}$', fontsize=11, ha='center')
    ax.plot([0.35], [0.62], marker='o', ms=4.5, color='black', zorder=5)
    ax.plot([0.35], [0.14], marker='o', ms=4.5, color='black', zorder=5)
    _arrow(ax, 0.35, 0.62, 3.05, 1.98, lw=1.2)
    _arrow(ax, 0.35, 0.14, 2.95, 1.05, lw=1.2)
    _arrow(ax, 1.15, 0.64, 1.65, 0.97, lw=1.1)
    for (px, py) in [(0.35, 0.62), (0.35, 0.14), (2.90, 2.10),
                     (-0.62, -1.28)]:
        ax.plot([px - 0.19, px + 0.19], [py + 0.38, py - 0.38],
                color='black', lw=0.9, linestyle=(0, (4, 3)))
    ax.text(0.85, -2.05, r'$(a)$', ha='center', fontsize=11)

    # ---- (b) several values of qc (peanut Fermi surface)
    X = 6.2
    rc, nb = 0.8, 0.30
    cl, cr = X - 0.95, X + 0.95
    a = 65.0
    ca, sa = np.cos(np.radians(a)), np.sin(np.radians(a))
    # right lobe arc (from -a to +a through 0)
    th = np.radians(np.linspace(-a, a, 40))
    px = [cr + rc * np.cos(t) for t in th]
    py = [rc * np.sin(t) for t in th]
    # cubic bezier: right lobe top -> neck -> left lobe top
    b = _bez((cr + rc * ca, rc * sa), (X + 0.70, nb), (X - 0.70, nb),
             (cl - rc * ca, rc * sa), n=60)
    px += list(b[:, 0]); py += list(b[:, 1])
    # left lobe arc (from 180-a to 180+a through 180)
    th = np.radians(np.linspace(180 - a, 180 + a, 40))
    px += [cl + rc * np.cos(t) for t in th]
    py += [rc * np.sin(t) for t in th]
    # cubic bezier: left lobe bottom -> neck -> right lobe bottom
    b = _bez((cl - rc * ca, -rc * sa), (X - 0.70, -nb), (X + 0.70, -nb),
             (cr + rc * ca, -rc * sa), n=60)
    px += list(b[:, 0]); py += list(b[:, 1])
    ax.add_patch(Polygon(list(zip(px, py)), closed=True, facecolor='white',
                         edgecolor='black', lw=1.2, hatch='///'))
    # q1 across left lobe, q2 across the whole peanut
    _arrow(ax, X - 1.55, -0.55, X - 0.38, 0.62, lw=1.2)
    ax.text(X - 0.60, 0.02, r'$q_1$', fontsize=10, ha='left')
    _arrow(ax, X - 1.30, 0.25, X + 1.90, 0.25, lw=1.2)
    ax.text(X + 1.15, 0.45, r'$q_2$', fontsize=10)
    # dashed tangents: neck (2), top-left, bottom-left
    for (px, py, sgn) in [(X, nb, 1), (X, -nb, -1)]:
        ax.plot([px - 0.18, px + 0.18], [py + 0.28 * sgn, py - 0.28 * sgn],
                color='black', lw=0.9, linestyle=(0, (4, 3)))
    for (px, py) in [(X - 1.41, 0.79), (X - 1.65, -0.59)]:
        ax.plot([px - 0.39, px + 0.39], [py + 0.23, py - 0.23],
                color='black', lw=0.9, linestyle=(0, (4, 3)))
    ax.text(X, -2.05, r'$(b)$', ha='center', fontsize=11)

    ax.set_xlim(-1.7, 8.45)
    ax.set_ylim(-2.3, 2.75)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '92')


# ---------------------------------------------------------------- Fig. 93
def fig_93():
    fig, ax = plt.subplots(figsize=(4.6, 1.15))
    # k axis
    ax.plot([0.2, 9.45], [0, 0], color='black', lw=1.1)
    _arrow(ax, 9.45, 0, 10.05, 0, lw=1.1)
    x0, dx = 0.60, 1.05
    ticks = [x0 + i * dx for i in range(9)]
    # dashed (shifted) ticks
    for i, xt in enumerate(ticks):
        t = i / 8.0
        shift = dx * (0.10 + 0.48 * np.sin(np.pi * t) ** 1.2)
        ax.plot([xt + shift, xt + shift], [0.03, 0.24], color='black',
                lw=1.1, linestyle=(0, (3, 2)))
        ax.plot([xt, xt], [-0.085, 0.085], color='black', lw=1.4)
    ax.text(ticks[0] - 0.05, -0.34, r'$k$', fontsize=11, ha='center')
    ax.text(ticks[-1] - 0.02, -0.34, r"$k'$", fontsize=11, ha='center')
    # braces
    _brace(ax, ticks[1], ticks[2], -0.17, 0.13, up=False)
    ax.text(0.5 * (ticks[1] + ticks[2]), -0.62, r'$\pi/R$', fontsize=11,
            ha='center')
    xt = ticks[4]
    shift = dx * (0.10 + 0.48 * np.sin(np.pi * 0.5) ** 1.2)
    _brace(ax, xt, xt + shift, 0.34, 0.12, up=True)
    ax.text(xt + 0.5 * shift, 0.60, r'$\eta(k)/R$', fontsize=11,
            ha='center')
    ax.set_xlim(0.0, 10.4)
    ax.set_ylim(-0.85, 0.85)
    ax.axis('off')
    _save(fig, '93')


# ---------------------------------------------------------------- Fig. 94
def fig_94():
    fig, ax = plt.subplots(figsize=(3.2, 2.9))
    rng = np.random.default_rng(3)
    n = 8000
    px = rng.uniform(-1, 1, n)
    py = rng.uniform(-1, 1, n)
    r = np.hypot(px, py)
    inside = r <= 1.0
    px, py, r = px[inside], py[inside], r[inside]
    s = r
    rings = 0.42 + 0.58 * np.cos(2 * np.pi * 3.0 * s + 0.4) ** 2
    base = 1.8 * np.exp(-2.4 * s)
    edge = np.clip((1.0 - s) / 0.09, 0, 1)
    p = np.clip(base * rings * edge, 0, 1)
    keep = rng.random(len(s)) < p
    ax.scatter(px[keep], py[keep], s=0.8 + 1.4 * rng.random(keep.sum()),
               c='black', lw=0, marker='o')
    ax.add_patch(Circle((0, 0), 0.048, facecolor='black',
                        edgecolor='black'))
    ax.set_xlim(-1.12, 1.12)
    ax.set_ylim(-1.12, 1.12)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '94')


# ---------------------------------------------------------------- Fig. 95
def fig_95():
    fig, ax = plt.subplots(figsize=(3.5, 3.3))
    y1, A1, w1 = 3.9, 0.95, 0.55      # 'down' spin resonance
    y2, A2, w2 = 2.0, 1.75, 0.85      # 'up' spin resonance
    yF = 3.3

    def xd(y):
        return A2 / (1 + ((y - y2) / w2) ** 2)

    def xu(y):
        return A1 / (1 + ((y - y1) / w1) ** 2)

    # occupied region (below Fermi level) hatched horizontally
    yh = np.linspace(0.12, yF, 300)
    ax.fill_betweenx(yh, 0, xu(yh) + xd(yh), facecolor='white',
                     edgecolor='black', hatch='---', linewidth=0.0)
    # resonance outlines
    yu = np.linspace(1.98, 4.95, 300)
    ax.plot(xu(yu), yu, color='black', lw=1.3)
    yd = np.linspace(0.02, 3.58, 300)
    ax.plot(xd(yd), yd, color='black', lw=1.3)
    # energy axis (zeta) and Fermi level
    ax.plot([0, 0], [0.05, 4.98], color='black', lw=1.1)
    _arrow(ax, 0, 4.98, 0, 5.22, lw=1.1)
    ax.text(-0.10, 5.05, r'$\zeta$', fontsize=12, ha='right')
    ax.plot([0, 1.30], [yF, yF], color='black', lw=0.9)
    ax.text(0.06, yF + 0.10, 'Fermi level', fontsize=8.5,
            bbox=dict(facecolor='white', edgecolor='none', pad=0.4))
    # d-d exchange splitting
    _arrow(ax, 2.55, y1, 2.55, y2, style='<|-|>', lw=1.1)
    ax.text(2.46, 2.98, 'd-d exchange splitting', fontsize=8,
            ha='right', va='center',
            bbox=dict(facecolor='white', edgecolor='none', pad=0.5))
    # spin labels
    ax.text(2.02, 4.28, "\u2018down\u2019 spin", fontsize=9)
    ax.text(2.12, 1.82, "\u2018up\u2019 spin", fontsize=9)
    # horizontal axis
    _arrow(ax, 0.02, 0.02, 1.15, 0.02, lw=1.2)
    ax.text(1.28, 0.02, 'Spin density', fontsize=9, va='center')
    ax.set_xlim(-0.38, 3.45)
    ax.set_ylim(-0.18, 5.42)
    ax.axis('off')
    _save(fig, '95')


# ---------------------------------------------------------------- Fig. 96
def _wavy(p0, p1, amp=0.13, waves=5.0, n=160):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    L = np.hypot(*d)
    u = d / L
    v = np.array([-u[1], u[0]])
    t = np.linspace(0, 1, n)
    return (p0[None, :] + t[:, None] * d[None, :]
            + (amp * np.sin(2 * np.pi * waves * t))[:, None] * v[None, :])


def _box(ax, cx, cy, side, ang):
    a = np.radians(ang)
    ux, uy = np.cos(a), np.sin(a)
    vx, vy = -uy, ux
    h = side / 2
    corners = [(cx + h * ux + h * vx, cy + h * uy + h * vy),
               (cx + h * ux - h * vx, cy + h * uy - h * vy),
               (cx - h * ux - h * vx, cy - h * uy - h * vy),
               (cx - h * ux + h * vx, cy - h * uy + h * vy)]
    ax.add_patch(Polygon(corners, closed=True, facecolor='white',
                         edgecolor='black', lw=1.1))


def fig_96():
    fig, ax = plt.subplots(figsize=(4.1, 3.15))
    # hatched sample rectangle
    ax.add_patch(Rectangle((0.8, 2.15), 5.5, 1.65, facecolor='white',
                           edgecolor='black', lw=1.2, hatch='////'))
    P = (6.05, 2.97)
    # electron momentum
    _arrow(ax, 2.15, 2.97, 5.78, 2.97, lw=1.3)
    ax.text(3.55, 3.22, r'$\hbar k$', fontsize=12)
    ax.add_patch(Circle(P, 0.085, facecolor='white', edgecolor='black',
                        lw=1.0, zorder=5))
    ax.text(5.68, 3.30, r'$-$', fontsize=13, ha='center')
    ax.text(6.42, 3.30, r'$+$', fontsize=12, ha='center')
    # dashed reference direction and theta
    ax.plot([P[0], 5.02], [P[1], 5.28], color='black', lw=0.9,
            linestyle=(0, (5, 3)))
    arc = Arc(P, 3.1, 3.1, angle=0, theta1=76, theta2=106,
              lw=0.9, color='black')
    ax.add_patch(arc)
    th = np.radians(93)
    ax.text(P[0] + 1.78 * np.cos(th), P[1] + 1.72 * np.sin(th),
            r'$\theta$', fontsize=12)
    # photons (wavy lines) + detectors
    w = _wavy(P, (6.92, 5.28), amp=0.13, waves=5.2)
    ax.plot(w[:, 0], w[:, 1], color='black', lw=1.1)
    _arrow(ax, 6.88, 5.18, 7.00, 5.42, lw=1.1)
    _box(ax, 7.22, 5.66, 0.62, 22)
    w2 = _wavy(P, (6.32, 0.98), amp=0.13, waves=5.0)
    ax.plot(w2[:, 0], w2[:, 1], color='black', lw=1.1)
    _arrow(ax, 6.30, 1.05, 6.20, 0.82, lw=1.1)
    _box(ax, 6.10, 0.48, 0.62, -25)
    # photon labels
    ax.text(7.30, 4.30, r'$\dfrac{\hbar\nu}{c}$', fontsize=12, ha='left')
    ax.text(6.55, 1.62, r'$\dfrac{\hbar\nu}{c}$', fontsize=12, ha='left')
    ax.set_xlim(0.3, 8.6)
    ax.set_ylim(0.0, 6.25)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '96')


if __name__ == '__main__':
    for f in (fig_86, fig_87, fig_88, fig_89, fig_90, fig_91,
              fig_92, fig_93, fig_94, fig_95, fig_96):
        f()
