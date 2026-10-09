# -*- coding: utf-8 -*-
"""Ziman, Principles of the Theory of Solids, 2nd ed. Chapter 11 (Superconductivity).
Redraw Figs. 199-213 as black-and-white textbook-style vector figures."""
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
    'hatch.linewidth': 0.55,
})

ROOT = Path(r'E:\AI整理书籍\齐曼\重排本')
OUT = ROOT / 'figures'
PREV = OUT / 'preview'
PREV.mkdir(parents=True, exist_ok=True)


def save(fig, key):
    fig.savefig(str(OUT / f'fig_{key}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(str(PREV / f'fig_{key}.png'), dpi=150, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)
    print('saved fig', key)


# ---------------- helpers ----------------

def arrow_head(ax, p0, p1, ms=9, lw=0, style='-|>', cs=None):
    """Draw only an arrowhead pointing from p0 to p1."""
    kw = dict(arrowstyle=style, color='k', lw=lw, mutation_scale=ms,
              shrinkA=0, shrinkB=0)
    if cs:
        kw['connectionstyle'] = cs
    ax.annotate('', xy=p1, xytext=p0, arrowprops=kw)


def mid_arrow(ax, p0, p1, frac=0.5, ms=9, frac_len=0.14):
    """Arrowhead placed along segment p0->p1 at frac, pointing toward p1."""
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    a = p0 + (p1 - p0) * frac
    b = p0 + (p1 - p0) * max(frac - frac_len, 0.0)
    arrow_head(ax, b, a, ms=ms)


def seg(ax, p0, p1, ls='-', lw=1.2):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color='k', lw=lw, linestyle=ls,
            solid_capstyle='butt')


def chord_arrow(ax, p0, p1, frac=0.5, ls='-', lw=1.2, ms=9):
    seg(ax, p0, p1, ls=ls, lw=lw)
    mid_arrow(ax, p0, p1, frac=frac, ms=ms)


def dot(ax, p, ms=5):
    ax.plot([p[0]], [p[1]], 'ko', ms=ms, mfc='k', mec='k')


def open_dot(ax, p, ms=7.5):
    ax.plot([p[0]], [p[1]], 'o', ms=ms, mfc='white', mec='k', mew=1.2)


def stipple_circle(ax, c, r, n=380, s=1.4, seed=0, extra_ring=True):
    """Stippled filled circle (Fermi sea)."""
    rng = np.random.default_rng(seed)
    rr = r * np.sqrt(rng.random(n))
    th = 2 * np.pi * rng.random(n)
    ax.scatter(c[0] + rr * np.cos(th), c[1] + rr * np.sin(th), s=s, c='k', linewidths=0)
    if extra_ring:
        rr2 = r * (0.80 + 0.19 * rng.random(int(n * 0.5)))
        th2 = 2 * np.pi * rng.random(int(n * 0.5))
        ax.scatter(c[0] + rr2 * np.cos(th2), c[1] + rr2 * np.sin(th2),
                   s=s * 0.8, c='k', linewidths=0)
    ax.add_patch(mpatches.Circle(c, r, facecolor='none', edgecolor='k', lw=1.4))


def curly_brace(ax, p0, p1, d=0.08, lw=1.1, side=1):
    """Curly brace from p0 to p1; tip on the side given (side=+1 -> right of p0->p1)."""
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    u = p1 - p0
    L = np.hypot(*u)
    u = u / L
    n = np.array([u[1], -u[0]]) * side
    m = (p0 + p1) / 2 + d * n
    a1 = p0 + 0.30 * L * u - 0.75 * d * n
    a2 = p0 + 0.52 * L * u + 0.50 * d * n
    b1 = p1 - 0.52 * L * u + 0.50 * d * n
    b2 = p1 - 0.30 * L * u - 0.75 * d * n
    Path = mpath.Path
    path = Path([p0, a1, a2, m, b1, b2, p1],
                [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.CURVE4, Path.CURVE4, Path.CURVE4])
    ax.add_patch(mpatches.PathPatch(path, facecolor='none', edgecolor='k', lw=lw))


def panel_label(ax, x, y, s):
    ax.text(x, y, f'${s}$', ha='center', va='center', fontsize=11.5)


# ---------------- Fig. 199 ----------------

def fig_199():
    fig, ax = plt.subplots(figsize=(3.3, 3.3))
    a = 1.0
    r_ion = 0.38
    # grid lines
    for i in range(4):
        ax.plot([-0.55, 3.55], [i, i], '-', color='k', lw=1.0)
        ax.plot([i, i], [-0.55, 3.55], '-', color='k', lw=1.0)
    # dashed circles at undisplaced inner ion positions
    for (i, j) in [(1, 1), (2, 1), (1, 2), (2, 2)]:
        ax.add_patch(mpatches.Circle((i, j), r_ion, facecolor='none',
                                     edgecolor='k', lw=1.1, ls=(0, (4, 3))))
    # displaced hatched ions (toward center (1.5,1.5))
    d = 0.17
    for (i, j) in [(1, 1), (2, 1), (1, 2), (2, 2)]:
        v = np.array([1.5 - i, 1.5 - j])
        v = v / np.hypot(*v) * d
        p = (i + v[0], j + v[1])
        ax.add_patch(mpatches.Circle(p, r_ion, facecolor='none', edgecolor='k',
                                     lw=1.2, hatch='///'))
        dot(ax, p, ms=4)
    # outer ions
    for i in range(4):
        for j in range(4):
            if (i, j) in [(1, 1), (2, 1), (1, 2), (2, 2)]:
                continue
            ax.add_patch(mpatches.Circle((i, j), r_ion, facecolor='none',
                                         edgecolor='k', lw=1.2, hatch='///'))
            dot(ax, (i, j), ms=4)
    # electron
    dot(ax, (1.5, 1.5), ms=4.5)
    ax.text(1.53, 1.40, '$e^-$', fontsize=11, ha='left', va='top')
    ax.set_xlim(-0.75, 3.75)
    ax.set_ylim(-0.75, 3.75)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 199)


# ---------------- Fig. 200 ----------------

def _phonon_diagram(ax, qlabel, arrow_right):
    L = np.array([-1.0, 0.0]); R = np.array([1.0, 0.0])
    bl = (-1.78, -1.38); tl = (-1.78, 1.38)
    br = (1.78, -1.38); tr = (1.78, 1.38)
    seg(ax, bl, L); seg(ax, L, tl); seg(ax, br, R); seg(ax, R, tr)
    mid_arrow(ax, bl, L, frac=0.55)
    mid_arrow(ax, L, tl, frac=0.45)
    mid_arrow(ax, br, R, frac=0.55)
    mid_arrow(ax, R, tr, frac=0.45)
    # wavy phonon line
    t = np.linspace(0, 1, 240)
    xw = -1.0 + 2.0 * t
    yw = 0.065 * np.sin(2 * np.pi * 5.5 * t)
    ax.plot(xw, yw, '-', color='k', lw=1.1)
    # phonon arrowhead
    t0 = 0.60
    xa = -1.0 + 2.0 * t0
    if arrow_right:
        arrow_head(ax, (xa - 0.18, 0.0), (xa, 0.0), ms=15)
    else:
        arrow_head(ax, (xa + 0.18, 0.0), (xa, 0.0), ms=15)
    ax.text(0.10, -0.42, qlabel, ha='center', fontsize=12)
    ax.text(-1.70, -1.62, r'$\mathbf{k}$', ha='center', fontsize=12)
    ax.text(-1.55, 1.60, r'$\mathbf{k}-\mathbf{K}$', ha='center', fontsize=12)
    ax.text(1.72, -1.62, r"$\mathbf{k}^{\prime}$", ha='center', fontsize=12)
    ax.text(1.62, 1.60, r"$\mathbf{k}^{\prime}+\mathbf{K}$", ha='center', fontsize=12)
    ax.set_xlim(-2.55, 2.55)
    ax.set_ylim(-2.35, 2.05)
    ax.set_aspect('equal')
    ax.axis('off')


def fig_200():
    fig, axs = plt.subplots(1, 2, figsize=(4.8, 2.35))
    _phonon_diagram(axs[0], r'$\mathbf{q}$', True)
    panel_label(axs[0], 0, -2.15, '(a)')
    _phonon_diagram(axs[1], r'$-\mathbf{q}$', False)
    panel_label(axs[1], 0, -2.15, '(b)')
    fig.subplots_adjust(wspace=0.05)
    save(fig, 200)


# ---------------- Fig. 201 ----------------

def fig_201():
    fig, axs = plt.subplots(1, 2, figsize=(4.8, 2.75))
    for ax in axs:
        ax.set_xlim(-2.45, 2.45)
        ax.set_ylim(-2.55, 2.25)
        ax.set_aspect('equal')
        ax.axis('off')
        stipple_circle(ax, (0, 0), 1.0, n=330, seed=3)
    # (a) direct scattering
    ax = axs[0]
    k2 = (0.62, 1.30); k2p = (-1.48, 0.66)
    k1 = (-0.55, -1.35); k1p = (1.48, -0.66)
    chord_arrow(ax, k1, k1p, frac=0.52, ls='-', ms=10)
    chord_arrow(ax, k2, k2p, frac=0.45, ls=(0, (5, 4)), ms=10)
    dot(ax, k2); dot(ax, k2p); dot(ax, k1); dot(ax, k1p)
    ax.text(0.86, 1.44, r'$\mathbf{k}_2$', fontsize=12)
    ax.text(-2.02, 0.56, r"$\mathbf{k}^{\prime}_2$", fontsize=12, ha='right')
    ax.text(-0.88, -1.56, r'$\mathbf{k}_1$', fontsize=12, ha='right')
    ax.text(1.76, -0.56, r"$\mathbf{k}^{\prime}_1$", fontsize=12)
    panel_label(ax, 0, -2.35, '(a)')
    # (b) second-order term
    ax = axs[1]
    k2 = (0.62, 1.30); k2p = (-1.48, 0.66)
    k1 = (-0.55, -1.35); k1p = (1.48, -0.66)
    k2m = (-0.18, 1.66); k1pK = (0.14, -1.70)
    chord_arrow(ax, k2, k2p, frac=0.42, ls=(0, (5, 4)), ms=10)
    chord_arrow(ax, k1, k1p, frac=0.50, ls=(0, (5, 4)), ms=10)
    seg(ax, k2, k2m); mid_arrow(ax, k2, k2m, frac=0.5, ms=10)
    seg(ax, k2m, k2p); mid_arrow(ax, k2m, k2p, frac=0.35, ms=10)
    seg(ax, k1, k1pK); mid_arrow(ax, k1, k1pK, frac=0.5, ms=10)
    seg(ax, k1pK, k1p); mid_arrow(ax, k1pK, k1p, frac=0.35, ms=10)
    for p in (k2, k2p, k1, k1p, k2m, k1pK):
        dot(ax, p)
    ax.text(0.95, 1.40, r'$\mathbf{k}_2$', fontsize=12)
    ax.text(-2.02, 0.52, r"$\mathbf{k}^{\prime}_2$", fontsize=12, ha='right')
    ax.text(-0.88, -1.56, r'$\mathbf{k}_1$', fontsize=12, ha='right')
    ax.text(1.76, -0.52, r"$\mathbf{k}^{\prime}_1$", fontsize=12)
    ax.text(-0.30, 1.92, r'$\mathbf{k}_2-\mathbf{K}$', fontsize=11, ha='center')
    ax.text(0.36, 1.56, r'$-\mathbf{K}$', fontsize=11, ha='left')
    ax.text(0.14, -1.98, r'$\mathbf{k}_1+\mathbf{K}$', fontsize=11, ha='center')
    ax.text(-0.24, -1.66, r'$\mathbf{K}$', fontsize=11, ha='right')
    panel_label(ax, 0, -2.35, '(b)')
    fig.subplots_adjust(wspace=0.02)
    save(fig, 201)


# ---------------- Fig. 202 ----------------

def fig_202():
    fig, axs = plt.subplots(1, 3, figsize=(5.1, 2.55))
    for ax in axs:
        ax.set_xlim(-2.35, 2.35)
        ax.set_ylim(-2.45, 2.05)
        ax.set_aspect('equal')
        ax.axis('off')
        stipple_circle(ax, (0, 0), 1.0, n=300, seed=5)
    DASH = (0, (5, 4))

    # (a) hole created at k3, filled by k2
    ax = axs[0]
    k2 = (0.60, 1.28); k2p = (-1.46, 0.64)
    k1 = (-0.55, -1.30); k1p = (1.46, -0.64)
    m = (-0.02, -1.60)
    k3 = (-0.55, 0.48)
    chord_arrow(ax, k2, k2p, frac=0.42, ls=DASH, ms=10)
    chord_arrow(ax, k1, k1p, frac=0.50, ls=DASH, ms=10)
    seg(ax, k2, k3); mid_arrow(ax, k2, k3, frac=0.45, ms=10)
    seg(ax, k3, k2p); mid_arrow(ax, k3, k2p, frac=0.30, ms=10)
    seg(ax, k1, m); mid_arrow(ax, k1, m, frac=0.5, ms=10)
    seg(ax, m, k1p); mid_arrow(ax, m, k1p, frac=0.5, ms=10)
    for p in (k2, k2p, k1, k1p, m):
        dot(ax, p)
    open_dot(ax, k3)
    ax.text(0.84, 1.42, r'$\mathbf{k}_2$', fontsize=12)
    ax.text(-2.00, 0.54, r"$\mathbf{k}^{\prime}_2$", fontsize=12, ha='right')
    ax.text(-0.88, -1.52, r'$\mathbf{k}_1$', fontsize=12, ha='right')
    ax.text(1.74, -0.54, r"$\mathbf{k}^{\prime}_1$", fontsize=12)
    ax.text(-0.32, 0.26, r'$\mathbf{k}_3$', fontsize=12, ha='left')
    panel_label(ax, 0, -2.28, '(a)')

    # (b) successive pair scattering
    ax = axs[1]
    k2 = (0.60, 1.28); k2p = (-1.46, 0.58)
    k1 = (-0.55, -1.30); k1p = (1.46, -0.58)
    A = (0.00, 1.58); B = (-1.02, 1.24)
    C = (0.00, -1.60); D = (1.02, -1.24)
    chord_arrow(ax, k2, k2p, frac=0.40, ls=DASH, ms=10)
    chord_arrow(ax, k1, k1p, frac=0.45, ls=DASH, ms=10)
    seg(ax, k2, A); mid_arrow(ax, k2, A, frac=0.5, ms=10)
    seg(ax, A, B); mid_arrow(ax, A, B, frac=0.5, ms=10)
    seg(ax, B, k2p); mid_arrow(ax, B, k2p, frac=0.45, ms=10)
    seg(ax, k1, C); mid_arrow(ax, k1, C, frac=0.5, ms=10)
    seg(ax, C, D); mid_arrow(ax, C, D, frac=0.5, ms=10)
    seg(ax, D, k1p); mid_arrow(ax, D, k1p, frac=0.45, ms=10)
    for p in (k2, k2p, k1, k1p, A, B, C, D):
        dot(ax, p)
    ax.text(0.84, 1.42, r'$\mathbf{k}_2$', fontsize=12)
    ax.text(-2.00, 0.50, r"$\mathbf{k}^{\prime}_2$", fontsize=12, ha='right')
    ax.text(-0.88, -1.52, r'$\mathbf{k}_1$', fontsize=12, ha='right')
    ax.text(1.74, -0.50, r"$\mathbf{k}^{\prime}_1$", fontsize=12)
    panel_label(ax, 0, -2.28, '(b)')

    # (c) pair scattering with holes
    ax = axs[2]
    k2 = (0.60, 1.28); k2p = (-1.46, 0.64)
    k1 = (-0.55, -1.30); k1p = (1.46, -0.64)
    h2 = (-0.70, 0.44); h1 = (0.70, -0.44)
    chord_arrow(ax, k2, k2p, frac=0.42, ls=DASH, ms=10)
    chord_arrow(ax, k1, k1p, frac=0.45, ls=DASH, ms=10)
    seg(ax, k2, h2); mid_arrow(ax, k2, h2, frac=0.45, ms=10)
    seg(ax, h2, k2p); mid_arrow(ax, h2, k2p, frac=0.45, ms=10)
    seg(ax, k1, h1); mid_arrow(ax, k1, h1, frac=0.45, ms=10)
    seg(ax, h1, k1p); mid_arrow(ax, h1, k1p, frac=0.45, ms=10)
    for p in (k2, k2p, k1, k1p):
        dot(ax, p)
    open_dot(ax, h2); open_dot(ax, h1)
    ax.text(0.84, 1.42, r'$\mathbf{k}_2$', fontsize=12)
    ax.text(-2.00, 0.54, r"$\mathbf{k}^{\prime}_2$", fontsize=12, ha='right')
    ax.text(-0.88, -1.52, r'$\mathbf{k}_1$', fontsize=12, ha='right')
    ax.text(1.74, -0.54, r"$\mathbf{k}^{\prime}_1$", fontsize=12)
    ax.text(0.30, -0.06, r"$\mathbf{k}^{\prime}_1-\mathbf{K}$", fontsize=11.5, ha='center')
    panel_label(ax, 0, -2.28, '(c)')
    fig.subplots_adjust(wspace=0.02)
    save(fig, 202)


# ---------------- Fig. 203 ----------------

def fig_203():
    fig, ax = plt.subplots(figsize=(3.8, 3.8))
    ax.set_xlim(-1.95, 1.95)
    ax.set_ylim(-1.85, 1.95)
    ax.set_aspect('equal')
    ax.axis('off')
    # stipple of occupied region
    rng = np.random.default_rng(7)
    n = 950
    rr = np.sqrt(rng.random(n))
    th = 2 * np.pi * rng.random(n)
    ax.scatter(rr * np.cos(th), rr * np.sin(th), s=0.8, c='k', linewidths=0)
    rr2 = 0.72 + 0.27 * rng.random(450)
    th2 = 2 * np.pi * rng.random(450)
    ax.scatter(rr2 * np.cos(th2), rr2 * np.sin(th2), s=0.7, c='k', linewidths=0)
    # inner dashed circle (gap annulus) and outer Fermi surface
    ax.add_patch(mpatches.Circle((0, 0), 0.86, facecolor='none', edgecolor='k',
                                 lw=1.0, ls=(0, (4, 3))))
    ax.add_patch(mpatches.Circle((0, 0), 1.0, facecolor='none', edgecolor='k', lw=1.4))
    # radial dashed rays
    angles = [100, 84, 68, 52, 22, -15, -52, -78, -100, -130, -158, 168, 118]
    for ang in angles:
        a = np.radians(ang)
        ax.plot([0.05 * np.cos(a), 1.12 * np.cos(a)],
                [0.05 * np.sin(a), 1.12 * np.sin(a)],
                ls=(0, (4, 3)), color='k', lw=0.9)
    # k electron: solid arrow + big dot
    a = np.radians(135)
    ax.plot([0.35 * np.cos(a), 0.95 * np.cos(a)], [0.35 * np.sin(a), 0.95 * np.sin(a)],
            '-', color='k', lw=1.2)
    arrow_head(ax, (0.80 * np.cos(a), 0.80 * np.sin(a)),
               (0.97 * np.cos(a), 0.97 * np.sin(a)), ms=10)
    dot(ax, (1.10 * np.cos(a), 1.10 * np.sin(a)), ms=10)
    ax.text(-0.70, 0.34, r'$\mathbf{k}$', fontsize=12)
    # more electrons (filled dots just outside Fermi surface)
    for ang, ms in [(101, 7.5), (88, 6.5), (75, 5)]:
        aa = np.radians(ang)
        dot(ax, (1.08 * np.cos(aa), 1.08 * np.sin(aa)), ms=ms)
    # holes (open circles just inside)
    for ang, ms in [(233, 9), (250, 6.5), (263, 5), (274, 4)]:
        aa = np.radians(ang)
        open_dot(ax, (0.91 * np.cos(aa), 0.91 * np.sin(aa)), ms=ms)
    # -k ray arrow + label
    a = np.radians(-42)
    arrow_head(ax, (0.66 * np.cos(a), 0.66 * np.sin(a)),
               (0.82 * np.cos(a), 0.82 * np.sin(a)), ms=10)
    ax.text(0.58, -0.40, r'$-\mathbf{k}$', fontsize=12)
    # xi(k) axis
    seg(ax, (0, 0), (1.55, 0))
    arrow_head(ax, (1.40, 0), (1.56, 0), ms=11)
    ax.text(1.28, 0.13, r'$\xi(k)$', fontsize=12)
    ax.text(1.10, -0.16, 'O', fontsize=11, ha='center')
    # 2Delta0 pointer
    ax.text(-1.72, 0.22, r'$2\Delta_0$', fontsize=12, ha='center')
    arrow_head(ax, (-1.50, 0.17), (-1.05, 0.11), ms=10)
    # Fermi surface label along arc
    a = np.radians(55)
    ax.text(1.30 * np.cos(a), 1.30 * np.sin(a), 'Fermi surface', fontsize=10.5,
            rotation=-37, ha='center', va='center')
    save(fig, 203)


# ---------------- Fig. 204 ----------------

def fig_204():
    fig, ax = plt.subplots(figsize=(4.0, 2.9))
    ax.set_xlim(-2.35, 2.45)
    ax.set_ylim(-2.25, 2.45)
    ax.axis('off')
    ax.set_aspect('auto')
    s = 0.9
    x = np.linspace(-2.15, 2.15, 400)
    eps = np.sqrt(0.55 ** 2 + (s * x) ** 2)
    # axes
    seg(ax, (0, -0.80), (0, 2.28))
    arrow_head(ax, (0, 2.12), (0, 2.30), ms=11)
    ax.text(0.02, 2.44, 'Energy', ha='center', fontsize=12)
    seg(ax, (-2.25, 0), (2.38, 0))
    arrow_head(ax, (2.24, 0), (2.40, 0), ms=11)
    ax.text(2.30, -0.28, r'$k$', ha='center', fontsize=12)
    # dashed xi and |xi|
    ax.plot(x, s * x, ls=(0, (6, 4)), color='k', lw=1.3)
    ax.plot(x, s * np.abs(x), ls=(0, (6, 4)), color='k', lw=1.3)
    ax.text(-2.10, 1.42, r'$|\xi(k)|$', fontsize=12, ha='center')
    ax.text(2.12, 1.42, r'$|\xi(k)|$', fontsize=12, ha='center')
    # solid epsilon(k)
    ax.plot(x, eps, '-', color='k', lw=2.0)
    ax.text(0.80, 1.28, r'$\epsilon(k)$', fontsize=12, ha='center')
    # Delta0 brace
    curly_brace(ax, (0.12, 0.0), (0.12, 0.55), d=0.07)
    ax.text(0.32, 0.14, r'$\Delta_0$', fontsize=12, ha='left')
    ax.text(0.10, -0.28, r'$k_F$', fontsize=12, ha='left')
    save(fig, 204)


# ---------------- Fig. 205 ----------------

def fig_205():
    fig, ax = plt.subplots(figsize=(3.2, 3.1))
    ax.set_xlim(-0.42, 1.42)
    ax.set_ylim(-0.30, 2.32)
    ax.axis('off')
    # axes
    seg(ax, (0, 0), (1.36, 0))
    arrow_head(ax, (1.24, 0), (1.38, 0), ms=11)
    seg(ax, (0, 0), (0, 2.10))
    for y, lab in [(1, '1'), (2, '2')]:
        seg(ax, (-0.045, y), (0, y))
        ax.text(-0.085, y, lab, ha='right', va='center', fontsize=11.5)
    ax.text(-0.07, -0.10, '0', ha='right', va='center', fontsize=11.5)
    ax.text(1.00, -0.10, r'$T_c$', ha='center', va='top', fontsize=12)
    ax.text(1.36, -0.10, r'$T$', ha='center', va='top', fontsize=12)
    ax.text(-0.26, 1.55, r'$\Delta/kT_c$', rotation=90,
            ha='center', va='center', fontsize=12)
    # curve
    t = np.linspace(1e-4, 1.0, 500)
    y = 1.764 * np.tanh(1.74 * np.sqrt(1.0 / t - 1.0))
    ax.plot(t, y, '-', color='k', lw=2.0)
    # brace for Delta0
    curly_brace(ax, (0.075, 0.0), (0.075, 1.764), d=0.055)
    ax.text(0.17, 0.88, r'$\Delta_0$', fontsize=12, ha='left')
    save(fig, 205)


# ---------------- Fig. 206 ----------------

def fig_206():
    fig, ax = plt.subplots(figsize=(3.9, 3.3))
    ax.set_xlim(-0.30, 1.85)
    ax.set_ylim(-0.30, 2.95)
    ax.axis('off')
    # axes
    seg(ax, (0, 0), (1.78, 0))
    arrow_head(ax, (1.66, 0), (1.80, 0), ms=11)
    seg(ax, (0, 0), (0, 2.88))
    for y, lab in [(1, '1'), (2, '2')]:
        seg(ax, (-0.045, y), (0, y))
        ax.text(-0.085, y, lab, ha='right', va='center', fontsize=11.5)
    ax.text(-0.13, 2.72, r'$C_s$', ha='center', fontsize=12)
    ax.text(1.00, -0.10, r'$T_c$', ha='center', va='top', fontsize=12)
    ax.text(1.76, -0.10, r'$T$', ha='center', va='top', fontsize=12)
    # normal line
    ax.plot([0, 1.0], [0, 1.0], ls=(0, (5, 4)), color='k', lw=1.4)
    ax.plot([1.0, 1.58], [1.0, 1.58], '-', color='k', lw=1.4)
    ax.text(1.36, 1.44, 'Normal', rotation=27, ha='center', va='bottom', fontsize=11)
    # superconducting curve
    t = np.linspace(0.24, 0.995, 400)
    y = 13.97 * np.exp(-1.76 / t)
    ax.plot(t, np.minimum(y, 2.42), '-', color='k', lw=1.9)
    seg(ax, (1.0, 2.43), (1.0, 1.0), lw=1.9)
    ax.plot([1.0, 1.0], [1.0, 0.0], ls=(0, (5, 4)), color='k', lw=1.3)
    ax.text(0.86, 1.80, 'Superconducting', rotation=52, ha='center', va='bottom',
            fontsize=11)
    save(fig, 206)


# ---------------- Fig. 207 ----------------

def fig_207():
    fig, axs = plt.subplots(1, 2, figsize=(4.9, 2.6))
    # (a) semiconductor: gap tied to zone boundary (square)
    ax = axs[0]
    ax.set_xlim(-0.75, 2.85)
    ax.set_ylim(-1.15, 2.75)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.add_patch(mpatches.Rectangle((0, 0), 2.0, 2.0, facecolor='white',
                                    edgecolor='k', lw=1.5, hatch='...'))
    dot(ax, (1.0, 1.0), ms=3)
    ax.text(1.0, 2.14, 'Energy gap', ha='center', va='bottom', fontsize=10.5)
    ax.text(1.0, -0.14, 'Energy gap', ha='center', va='top', fontsize=10.5)
    ax.text(-0.14, 1.0, 'Energy gap', ha='right', va='center', rotation=90, fontsize=10.5)
    ax.text(2.14, 1.0, 'Energy gap', ha='left', va='center', rotation=270, fontsize=10.5)
    panel_label(ax, 1.0, -0.85, '(a)')
    # (b) superconductor: gap carried by displaced Fermi surface
    ax = axs[1]
    ax.set_xlim(-1.85, 3.05)
    ax.set_ylim(-1.85, 2.15)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.add_patch(mpatches.Circle((0, 0), 1.0, facecolor='none', edgecolor='k',
                                 lw=1.3, ls=(0, (5, 4))))
    ax.add_patch(mpatches.Circle((0.45, 0), 1.0, facecolor='white', edgecolor='k',
                                 lw=1.4, hatch='...'))
    seg(ax, (0, 0), (0.45, 0))
    arrow_head(ax, (0.33, 0), (0.46, 0), ms=10)
    dot(ax, (0, 0), ms=5); dot(ax, (0.45, 0), ms=5)
    ax.text(0.22, 0.16, r'$\delta\mathbf{k}$', ha='center', fontsize=11.5)
    a = np.radians(72)
    ax.text(0.45 + 1.18 * np.cos(a), 1.18 * np.sin(a), 'Energy gap', fontsize=10.5,
            rotation=-24, ha='center', va='bottom')
    panel_label(ax, 0.45, -1.55, '(b)')
    fig.subplots_adjust(wspace=0.02)
    save(fig, 207)


# ---------------- Fig. 208 ----------------

def fig_208():
    fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.6))
    # (a) wave-number space
    ax = axs[0]
    ax.set_xlim(-0.90, 1.70)
    ax.set_ylim(-0.42, 1.42)
    ax.axis('off')
    seg(ax, (-0.05, 0), (1.55, 0))
    arrow_head(ax, (1.44, 0), (1.57, 0), ms=11)
    seg(ax, (0, 0), (0, 1.30))
    arrow_head(ax, (0, 1.20), (0, 1.32), ms=11)
    ax.text(-0.06, -0.10, 'O', ha='right', va='center', fontsize=11.5)
    ax.text(1.52, -0.10, r'$q$', ha='center', va='center', fontsize=12)
    ax.text(-0.06, 1.36, r'$\Gamma(q)$', ha='right', fontsize=12)
    x = np.linspace(0, 1.45, 300)
    y = 1.0 / (1.0 + (x / 0.66) ** 2.53)
    ax.plot(x, y, '-', color='k', lw=1.6)
    ax.plot([0, 1.15], [1, 1], ls=(0, (6, 4)), color='k', lw=1.3)
    ax.text(0.56, 1.05, 'London', ha='center', fontsize=11)
    yq = 1.0 / (1.0 + (0.75 / 0.66) ** 2.53)
    ax.plot([0.75, 0.75], [0, yq], ls=(0, (4, 3)), color='k', lw=1.1)
    ax.text(0.75, -0.10, r'$q_c$', ha='center', va='center', fontsize=12)
    # bracket 4 pi n e^2 / m c^2
    seg(ax, (-0.16, 0), (-0.16, 1.0))
    seg(ax, (-0.16, 0), (-0.24, 0))
    seg(ax, (-0.16, 1.0), (-0.24, 1.0))
    ax.text(-0.28, 0.50, r'$\dfrac{4\pi ne^2}{mc^2}$', ha='right', va='center', fontsize=11)
    ax.text(0.63, 0.50, 'Pippard', rotation=-44, ha='center', fontsize=11)
    panel_label(ax, 0.70, -0.34, '(a)')
    # (b) real space
    ax = axs[1]
    ax.set_xlim(-0.70, 1.50)
    ax.set_ylim(-0.42, 1.55)
    ax.axis('off')
    seg(ax, (-0.60, 0), (1.42, 0))
    arrow_head(ax, (1.31, 0), (1.44, 0), ms=11)
    seg(ax, (0, 0), (0, 1.42))
    arrow_head(ax, (0, 1.32), (0, 1.44), ms=11)
    ax.text(0.05, -0.10, 'O', ha='left', va='center', fontsize=11.5)
    ax.text(1.40, -0.10, r'$r$', ha='center', va='center', fontsize=12)
    ax.text(-0.06, 1.50, r'$\Gamma(r)$', ha='right', fontsize=12)
    # London delta spike (dashed)
    xs = np.linspace(-0.17, 0.17, 200)
    ax.plot(xs, 1.08 * np.exp(-(xs / 0.045) ** 2), ls=(0, (4, 2.5)), color='k', lw=1.3)
    ax.text(0.28, 1.00, 'London', ha='left', fontsize=11)
    # Pippard solid curve
    xx = np.linspace(-0.42, 1.28, 400)
    yy = np.where(xx < 0, 0.52 * np.exp(1.55 * xx),
                  (0.50 + 0.10 * np.exp(-((xx - 0.18) / 0.22) ** 2)) * np.exp(-1.45 * xx))
    ax.plot(xx, yy, '-', color='k', lw=1.6)
    yr = (0.50 + 0.10 * np.exp(-((0.55 - 0.18) / 0.22) ** 2)) * np.exp(-1.45 * 0.55)
    ax.plot([0.55, 0.55], [0, yr], ls=(0, (4, 3)), color='k', lw=1.1)
    ax.text(0.55, -0.10, r'$1/q_c$', ha='center', va='center', fontsize=11.5)
    ax.text(0.68, 0.30, 'Pippard', ha='left', fontsize=11)
    panel_label(ax, 0.45, -0.34, '(b)')
    fig.subplots_adjust(wspace=0.10)
    save(fig, 208)


# ---------------- Fig. 209 ----------------

def fig_209():
    fig, ax = plt.subplots(figsize=(3.6, 3.6))
    ax.set_xlim(-2.45, 2.45)
    ax.set_ylim(-2.45, 2.45)
    ax.set_aspect('equal')
    ax.axis('off')
    # hatched exterior
    ax.add_patch(mpatches.Rectangle((-2.4, -2.4), 4.8, 4.8, facecolor='white',
                                    edgecolor='none', hatch='///', zorder=1))
    # erase inside big circle
    ax.add_patch(mpatches.Circle((0, 0), 1.52, facecolor='white', edgecolor='none',
                                 zorder=2))
    # cross-hatched penetration annulus
    ax.add_patch(mpatches.Circle((0, 0), 1.34, facecolor='white', edgecolor='none',
                                 hatch='xxxx', zorder=2))
    # clear core
    ax.add_patch(mpatches.Circle((0, 0), 1.02, facecolor='white', edgecolor='none',
                                 zorder=2))
    # edges
    ax.add_patch(mpatches.Circle((0, 0), 1.52, facecolor='none', edgecolor='k',
                                 lw=1.3, zorder=3))
    ax.add_patch(mpatches.Circle((0, 0), 1.02, facecolor='none', edgecolor='k',
                                 lw=2.4, zorder=3))
    # H at centre
    dot(ax, (0, 0), ms=5.5)
    ax.text(0.14, 0.0, r'$\mathbf{H}$', fontsize=13, ha='left', va='center')
    # dl arrow on path (clockwise at top): short arc + tangent head
    th = np.linspace(np.radians(103), np.radians(77), 30)
    ax.plot(1.52 * np.cos(th), 1.52 * np.sin(th), '-', color='k', lw=1.3, zorder=3)
    arrow_head(ax, (1.52 * np.cos(np.radians(83)), 1.52 * np.sin(np.radians(83))),
               (1.52 * np.cos(np.radians(77)), 1.52 * np.sin(np.radians(77))), ms=12)
    ax.text(-0.18, 1.80, r'$\mathbf{dl}$', ha='center', fontsize=12)
    save(fig, 209)


# ---------------- Fig. 210 ----------------

def _half_ellipse(cx, cy, rx, ry, n=80):
    th = np.linspace(np.pi, 2 * np.pi, n)
    xs = cx + rx * np.cos(th)
    ys = cy + ry * np.sin(th)
    return np.column_stack([np.concatenate([[cx - rx], xs, [cx + rx]]),
                            np.concatenate([[cy], ys, [cy]])])


def _junction_panel(ax, bias=False):
    ax.set_xlim(0, 2.15)
    ax.set_ylim(-0.10, 2.85)
    ax.set_aspect('equal')
    ax.axis('off')
    # barrier
    seg(ax, (0.98, 0.28), (0.98, 2.42), lw=1.5)
    seg(ax, (1.14, 0.28), (1.14, 2.42), lw=1.5)
    ax.text(1.06, 2.62, 'Barrier', ha='center', fontsize=11)
    arrow_head(ax, (1.06, 2.52), (1.06, 2.44), ms=9)
    # normal metal (left)
    yl = 1.60 if bias else 1.25
    P = _half_ellipse(0.63, yl, 0.35, 0.95)
    ax.add_patch(mpatches.Polygon(P, closed=True, facecolor='white', edgecolor='k',
                                  lw=1.1, hatch='///'))
    seg(ax, (0.28, yl), (0.98, yl), lw=1.4)
    ax.text(0.28, yl + 0.07, r'$\epsilon_F$', ha='right', fontsize=11.5)
    # superconducting metal (right)
    for yy, st in [(1.50, '-'), (1.25, (0, (5, 4))), (1.00, '-')]:
        seg(ax, (1.14, yy), (1.92, yy), ls=st, lw=1.3)
    P = _half_ellipse(1.53, 1.00, 0.39, 0.78)
    ax.add_patch(mpatches.Polygon(P, closed=True, facecolor='white', edgecolor='k',
                                  lw=1.1, hatch='xx'))
    seg(ax, (1.14, 1.00), (1.92, 1.00), lw=1.4)
    # 2 Delta arrow
    ax.annotate('', xy=(1.74, 1.48), xytext=(1.74, 1.02),
                arrowprops=dict(arrowstyle='<->', color='k', lw=1.1,
                                mutation_scale=10))
    ax.text(1.82, 1.25, r'$2\Delta$', ha='left', fontsize=12)
    if bias:
        # dashed eps_F continues across
        ax.plot([0.28, 1.92], [1.25, 1.25], ls=(0, (5, 4)), color='k', lw=1.2)
        # phi arrow
        ax.annotate('', xy=(0.80, 1.58), xytext=(0.80, 1.27),
                    arrowprops=dict(arrowstyle='<->', color='k', lw=1.1,
                                    mutation_scale=10))
        ax.text(0.72, 1.42, r'$\phi$', ha='right', fontsize=12)
        # tunnelling electron
        dot(ax, (0.95, 1.53), ms=5)
        dot(ax, (1.21, 1.55), ms=5)
        ax.annotate('', xy=(1.19, 1.55), xytext=(0.97, 1.53),
                    arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                    ls=(0, (3, 2)), mutation_scale=10))
    ax.text(1.06, -0.02, ' ', fontsize=1)


def fig_210():
    fig = plt.figure(figsize=(4.9, 4.35))
    axa = fig.add_axes([0.02, 0.52, 0.47, 0.44])
    axb = fig.add_axes([0.52, 0.52, 0.47, 0.44])
    axc = fig.add_axes([0.30, 0.04, 0.42, 0.36])
    _junction_panel(axa, bias=False)
    panel_label(axa, 1.06, -0.05, '(a)')
    _junction_panel(axb, bias=True)
    panel_label(axb, 1.06, -0.05, '(b)')
    # (c) I-V characteristic
    ax = axc
    ax.set_xlim(0, 1.62)
    ax.set_ylim(-0.14, 1.85)
    ax.axis('off')
    seg(ax, (0.22, 0.22), (0.22, 1.70))
    arrow_head(ax, (0.22, 1.58), (0.22, 1.72), ms=11)
    seg(ax, (0.22, 0.22), (1.55, 0.22))
    arrow_head(ax, (1.43, 0.22), (1.57, 0.22), ms=11)
    ax.text(0.13, 1.76, r'$J$', ha='right', fontsize=12)
    ax.text(1.52, 0.06, r'$\phi$', ha='center', fontsize=12)
    # curve: zero, then sharp rise at Delta, then slower rise
    xs1 = np.linspace(0.62, 0.90, 200)
    s0, s1 = 1 / (1 + np.exp(-(0.62 - 0.76) / 0.05)), 1 / (1 + np.exp(-(0.90 - 0.76) / 0.05))
    ys1 = 0.22 + 0.95 * (1 / (1 + np.exp(-(xs1 - 0.76) / 0.05)) - s0) / (s1 - s0)
    xs2 = np.linspace(0.90, 1.48, 200)
    ys2 = ys1[-1] + 0.42 * (1 - np.exp(-(xs2 - 0.90) / 0.42))
    ax.plot(np.concatenate([[0.22], xs1, xs2]),
            np.concatenate([[0.22], ys1, ys2]), '-', color='k', lw=1.7)
    # ideal T=0 jump (dashed)
    ax.plot([0.735, 0.735], [0.72, 1.16], ls=(0, (4, 3)), color='k', lw=1.2)
    ax.text(0.76, 0.06, r'$\Delta$', ha='center', va='top', fontsize=12)
    panel_label(ax, 1.10, -0.14, '(c)')
    save(fig, 210)


# ---------------- Fig. 211 ----------------

def fig_211():
    fig, ax = plt.subplots(figsize=(3.4, 4.4))
    ax.set_xlim(-0.25, 5.45)
    ax.set_ylim(-1.75, 7.75)
    ax.set_aspect('equal')
    ax.axis('off')
    y0, y1 = 0.3, 6.9
    # slabs
    ax.add_patch(mpatches.Rectangle((0, y0), 2.35, y1 - y0, facecolor='white',
                                    edgecolor='k', lw=1.4, hatch='///'))
    ax.add_patch(mpatches.Rectangle((2.85, y0), 2.35, y1 - y0, facecolor='white',
                                    edgecolor='k', lw=1.4, hatch='///'))
    # penetration strips
    ax.add_patch(mpatches.Rectangle((2.35, y0), 0.15, y1 - y0, facecolor='white',
                                    edgecolor='k', lw=1.0, hatch='xx'))
    ax.add_patch(mpatches.Rectangle((2.70, y0), 0.15, y1 - y0, facecolor='white',
                                    edgecolor='k', lw=1.0, hatch='xx'))
    # magnetic field line (dots)
    for yy in np.arange(0.55, 6.85, 0.27):
        dot(ax, (2.60, yy), ms=3.5)
    # labels
    ax.text(2.60, 7.18, 'Barrier', ha='center', fontsize=11)
    arrow_head(ax, (2.60, 7.06), (2.60, 6.94), ms=9)
    ax.text(3.42, 6.42, 'Magnetic\nfield line', ha='left', fontsize=10.5)
    arrow_head(ax, (3.38, 6.22), (2.70, 5.98), ms=9)
    # path points
    L2 = (1.95, 5.35); R2 = (3.25, 5.35)
    L1 = (1.95, 1.85); R1 = (3.25, 1.85)
    seg(ax, L2, R2, lw=1.0)
    seg(ax, L1, R1, lw=1.0)
    seg(ax, L1, L2, lw=1.3)
    mid_arrow(ax, L1, L2, frac=0.47, ms=12)
    seg(ax, R2, R1, lw=1.3)
    mid_arrow(ax, R2, R1, frac=0.47, ms=12)
    for p in (L1, L2, R1, R2):
        dot(ax, p, ms=5)
    ax.text(1.80, 3.75, r'$\mathbf{dl}$', ha='right', fontsize=12)
    ax.text(3.40, 3.75, r'$\mathbf{dl}$', ha='left', fontsize=12)
    ax.text(1.30, 3.05, r'$\Psi(L)$', ha='center', fontsize=12)
    ax.text(3.92, 3.05, r'$\Psi(R)$', ha='center', fontsize=12)
    # penetration region brace
    ax.text(2.60, -0.32, '{', rotation=90, ha='center', va='center',
            fontsize=26, rotation_mode='anchor')
    ax.text(2.60, -0.78, 'Penetration\nregion', ha='center', va='top', fontsize=10.5)
    save(fig, 211)


# ---------------- Fig. 212 ----------------

def _boundary_panel(ax, typ):
    ax.set_xlim(-1.70, 4.45)
    ax.set_ylim(-0.80, 3.30)
    ax.set_aspect('equal')
    ax.axis('off')
    if typ == 'I':
        xlam, xxi, hh, ps = 1.30, 2.60, (0.62, 0.26), (1.15, 0.45)
    else:
        xlam, xxi, hh, ps = 1.60, 0.75, (0.75, 0.30), (0.32, 0.16)
    xHc = 1.9
    # hatched superconducting region
    ax.add_patch(mpatches.Rectangle((0, 0), xlam, 2.55, facecolor='white',
                                    edgecolor='none', hatch='///'))
    # baseline and boundaries
    seg(ax, (-1.55, 0), (4.30, 0), lw=1.2)
    seg(ax, (0, 0), (0, 2.55), lw=1.2)
    seg(ax, (xlam, 0), (xlam, 2.55), lw=1.2)
    # Hc level and H curve
    seg(ax, (-1.45, xHc), (0, xHc), lw=1.4)
    ax.text(-1.12, xHc + 0.10, r'$H_c$', ha='center', fontsize=12)
    xh = np.linspace(0, xlam, 300)
    yh = 0.5 * xHc * (1 + np.tanh((hh[0] - xh) / hh[1]))
    ax.plot(xh, yh, '-', color='k', lw=1.7)
    if typ == 'I':
        ax.text(0.66, 1.22, r'$H$', ha='left', fontsize=12)
    else:
        ax.text(0.94, 0.60, r'$H$', ha='left', fontsize=12)
    # |Psi| curve and |Psi0| asymptote
    xp = np.linspace(0, min(xlam + 0.15, 2.45), 300)
    yp = 0.875 * (1 + np.tanh((xp - ps[0]) / ps[1]))
    ax.plot(xp, yp, ls=(0, (6, 4)), color='k', lw=1.5)
    pstart = 2.40 if typ == 'I' else ps[0] + 0.12
    ax.plot([pstart, 4.15], [1.75, 1.75], ls=(0, (6, 4)), color='k', lw=1.5)
    ax.text(4.20, 1.75, r'$|\Psi_0|$', ha='left', va='center', fontsize=12)
    if typ == 'I':
        ax.text(1.72, 1.28, r'$|\Psi|$', ha='left', fontsize=12)
    else:
        ax.text(0.50, 1.32, r'$|\Psi|$', ha='right', fontsize=12)
    # xi and lambda arrows
    ytop = 2.72
    xl = 0.5 * xxi
    seg(ax, (0.03, ytop), (xl - 0.18, ytop))
    arrow_head(ax, (xl - 0.45, ytop), (0.03, ytop), ms=10)
    seg(ax, (xl + 0.18, ytop), (xxi - 0.03, ytop))
    arrow_head(ax, (xl + 0.45, ytop), (xxi - 0.03, ytop), ms=10)
    ax.text(xl, ytop + 0.02, r'$\xi$', ha='center', va='center',
            fontsize=12, bbox=dict(fc='white', ec='none', pad=0.5))
    ybot = -0.30
    ym = 0.5 * xlam
    seg(ax, (0.03, ybot), (ym - 0.18, ybot))
    arrow_head(ax, (ym - 0.45, ybot), (0.03, ybot), ms=10)
    seg(ax, (ym + 0.18, ybot), (xlam - 0.03, ybot))
    arrow_head(ax, (ym + 0.45, ybot), (xlam - 0.03, ybot), ms=10)
    ax.text(ym, ybot, r'$\lambda$', ha='center', va='center',
            fontsize=12, bbox=dict(fc='white', ec='none', pad=0.5))
    ax.text(-0.85, 1.02, 'Normal', ha='center', fontsize=11)
    if typ == 'I':
        ax.text(1.92, 0.82, 'Superconducting', ha='left', fontsize=10.5)
        ax.text(3.95, 1.12, 'Type I', ha='center', fontsize=11.5)
    else:
        ax.text(1.78, 1.12, 'Superconducting', ha='left', fontsize=10)
        ax.text(4.05, 1.12, 'Type II', ha='center', fontsize=11.5)


def fig_212():
    fig, axs = plt.subplots(2, 1, figsize=(5.0, 6.4))
    _boundary_panel(axs[0], 'I')
    panel_label(axs[0], 1.9, -0.68, '(a)')
    _boundary_panel(axs[1], 'II')
    panel_label(axs[1], 1.9, -0.68, '(b)')
    fig.subplots_adjust(hspace=0.10)
    save(fig, 212)


# ---------------- Fig. 213 ----------------

def fig_213():
    fig, ax = plt.subplots(figsize=(4.6, 3.8))
    W, H = 4.6, 3.8
    ax.set_xlim(-0.08, W + 0.08)
    ax.set_ylim(-0.08, H + 0.08)
    ax.set_aspect('equal')
    ax.axis('off')
    # cross-hatch over square
    sq = mpatches.Rectangle((0, 0), W, H, facecolor='none', edgecolor='none')
    ax.add_patch(sq)
    lines = []
    for x0 in np.arange(-H, W + H, 0.22):
        lines.append([(x0, 0), (x0 + H, H)])
        lines.append([(x0, H), (x0 + H, 0)])
    lc = plt.matplotlib.collections.LineCollection(lines, color='k', linewidths=0.9,
                                                   zorder=1)
    lc.set_clip_path(sq)
    ax.add_collection(lc)
    # flux cores
    r = 0.62
    cores = [(0.10, 2.72), (2.20, 2.76), (W - 0.02, 2.66), (1.08, 0.72), (3.38, 0.66)]
    rng = np.random.default_rng(21)
    for (cx, cy) in cores:
        ax.add_patch(mpatches.Circle((cx, cy), 1.02 * r, facecolor='white',
                                     edgecolor='none', zorder=2))
        n = 360
        rr = r * np.sqrt(rng.random(n))
        th = 2 * np.pi * rng.random(n)
        ax.scatter(cx + rr * np.cos(th), cy + rr * np.sin(th), s=2.0, c='k',
                   linewidths=0, zorder=3)
    # vortex arc arrows (clockwise)
    for k, (cx, cy) in enumerate(cores):
        offs = [(150, 122), (60, 32), (-40, -68)]
        for a1, a2 in offs:
            a1r, a2r = np.radians(a1 + 7 * k), np.radians(a2 + 7 * k)
            th = np.linspace(a1r, a2r, 30)
            ax.plot(cx + 1.06 * r * np.cos(th), cy + 1.06 * r * np.sin(th),
                    '-', color='k', lw=1.1)
            arrow_head(ax, (cx + 1.06 * r * np.cos(a2r + 0.10),
                            cy + 1.06 * r * np.sin(a2r + 0.10)),
                       (cx + 1.06 * r * np.cos(a2r), cy + 1.06 * r * np.sin(a2r)), ms=9)
    # annotations on the top-middle core
    cx, cy = cores[1]
    y_xi = cy
    seg(ax, (cx - 2.05 * r, y_xi), (cx - 1.05 * r, y_xi))
    arrow_head(ax, (cx - 1.45 * r, y_xi), (cx - 2.05 * r, y_xi), ms=9)
    arrow_head(ax, (cx - 1.60 * r, y_xi), (cx - 1.05 * r, y_xi), ms=9)
    ax.text(cx - 1.55 * r, y_xi + 0.18, r'$\xi$', ha='center', fontsize=12)
    a = np.radians(-32)
    p0 = (cx + 0.15 * r * np.cos(a), cy + 0.15 * r * np.sin(a))
    p1 = (cx + 2.05 * r * np.cos(a), cy + 2.05 * r * np.sin(a))
    seg(ax, p0, p1)
    arrow_head(ax, (cx + 1.80 * r * np.cos(a), cy + 1.80 * r * np.sin(a)), p1, ms=10)
    ax.text(p1[0] + 0.05, p1[1] - 0.02, r'$\lambda$', ha='left', va='center', fontsize=12)
    ax.text(cx + 0.10, cy + r + 0.16, r'$v_s$', ha='center', fontsize=11.5)
    ax.text(0.55, 1.76, 'Superconducting', ha='left', fontsize=10.5)
    save(fig, 213)


# ---------------- generate all ----------------

if __name__ == '__main__':
    for f in [fig_199, fig_200, fig_201, fig_202, fig_203, fig_204, fig_205,
              fig_206, fig_207, fig_208, fig_209, fig_210, fig_211, fig_212,
              fig_213]:
        f()
    print('all done')
