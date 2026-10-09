# -*- coding: utf-8 -*-
"""Ziman, Principles of the Theory of Solids (2nd ed.), Chapter 3, Figs. 51-66.
Black-and-white textbook-style vector redraws. One function per figure.

Fig. 51  p106 (book 92)   Wave-function in a solid
Fig. 52  p106 (book 92)   (a) Energy contours, (b) E(k) along cube axis
Fig. 53  p107 (book 93)   Atomic levels spreading into bands
Fig. 54  p109 (book 95)   Bound atomic orbitals of free atoms
Fig. 55  p109 (book 95)   Bloch states of crystal
Fig. 56  p111 (book 97)   The Wigner-Seitz method
Fig. 57  p114 (book 100)  Synthesis of an orthogonalized plane wave
Fig. 58  p117 (book 103)  Muffin-tin potentials
Fig. 59  p121 (book 107)  Ordinary vs structural Green function
Fig. 60  p124 (book 110)  Model potential w and pseudo-wavefunction phi
Fig. 61  p125 (book 111)  Model pseudo-potential for KKR matrix elements
Fig. 62  p126 (book 112)  Model pseudo-potentials: (a) Heine-Abarenkov, (b) Shaw
Fig. 63  p127 (book 113)  (a) d-bands crossing s-band; (b) s-d hybridization
Fig. 64  p128 (book 114)  Virtual state tunnelling through centrifugal barrier
Fig. 65  p130 (book 116)  (a) General point k; (b) symmetry points/lines
Fig. 66  p132 (book 118)  Spin-orbit effect on p-type levels near zone centre
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
    'hatch.linewidth': 0.55,
})

BASE = r'E:\AI整理书籍\齐曼\重排本'
FIGD = os.path.join(BASE, 'figures')
PREV = os.path.join(FIGD, 'preview')
os.makedirs(PREV, exist_ok=True)


def save(fig, key):
    fig.savefig(os.path.join(FIGD, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, 'fig_%s.png' % key),
                dpi=200, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)
    print('fig_%s done' % key)


def ax_on(fig, rect, xlim, ylim, aspect=None):
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis('off')
    if aspect == 'equal':
        ax.set_aspect('equal', adjustable='box')
    return ax


def arr(ax, p0, p1, ms=11, style='-|>', z=6, lw=1.05):
    ax.annotate('', xy=tuple(p1), xytext=tuple(p0),
                arrowprops=dict(arrowstyle=style, color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms),
                zorder=z)


def seg(ax, p0, p1, lw=1.2, ls='-', z=3):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color='k', lw=lw, ls=ls,
            solid_capstyle='butt', zorder=z)


def polyline(ax, pts, lw=1.2, ls='-', z=3):
    pts = np.asarray(pts, float)
    ax.plot(pts[:, 0], pts[:, 1], color='k', lw=lw, ls=ls, zorder=z)


def dot(ax, p, s=18, z=8):
    ax.scatter([p[0]], [p[1]], s=s, color='k', zorder=z)


def cr(pts, n=24):
    """Catmull-Rom smooth spline through control points."""
    pts = np.asarray(pts, float)
    P = np.vstack([pts[0], pts, pts[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        t = np.linspace(0, 1, n)[:, None]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                          + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    return np.vstack(out)


def arc(ax, c, r, th0, th1, lw=1.2, ls='-', z=3, n=80):
    th = np.radians(np.linspace(th0, th1, n))
    ax.plot(c[0] + r * np.cos(th), c[1] + r * np.sin(th), color='k',
            lw=lw, ls=ls, zorder=z)


def brace(ax, x, y0, y1, d, flip=False, lw=1.0, z=3):
    """Curly brace with hooks at x (y0..y1), spine offset d, cusp pointing
    away from the hooks ('{' when flip=False, '}' when flip=True)."""
    ym = 0.5 * (y0 + y1)
    t = (y1 - y0)
    s = -1.0 if flip else 1.0          # direction the cusp points
    xs = x + s * 0.62 * d              # spine x
    pts = [(x, y1),
           (xs - s * 0.10 * d, y1 - 0.13 * t),
           (xs, y1 - 0.34 * t),
           (xs - s * 0.10 * d, y1 - 0.55 * t),
           (xs + s * 0.30 * d, ym),
           (xs - s * 0.10 * d, y0 + 0.55 * t),
           (xs, y0 + 0.34 * t),
           (xs - s * 0.10 * d, y0 + 0.13 * t),
           (x, y0)]
    polyline(ax, cr(pts, 12), lw=lw, z=z)


# ---------------------------------------------------------------- fig 51
def fig_51():
    fig = plt.figure(figsize=(4.5, 2.15))
    ax = ax_on(fig, [0.01, 0.02, 0.98, 0.96], (-0.15, 10.15), (-1.62, 2.30))
    # horizontal reference line with atom dots
    seg(ax, (-0.1, 0), (10.1, 0), lw=1.0, z=2)
    for xa in (2.3, 5.6, 8.5):
        dot(ax, (xa, 0), s=24)
    # dashed smooth envelope (the pseudo-wave-function)
    env = cr([(0.0, 0.44), (1.2, 0.475), (3.0, 0.452), (5.0, 0.28),
              (7.0, 0.02), (8.6, -0.16), (10.0, -0.26)], 16)
    ax.plot(env[:, 0], env[:, 1], 'k--', lw=1.1, dashes=(4, 2.6), zorder=3)
    # solid psi: plateaus, deep wells, tall core spikes at atoms
    psi = cr([(0.00, 0.400), (0.50, 0.455), (1.00, 0.465), (1.35, 0.420),
              (1.62, -0.55), (1.80, -1.28), (1.98, -1.28), (2.10, -0.45),
              (2.22, 0.35), (2.262, 1.55), (2.30, 2.05), (2.338, 1.55),
              (2.38, 0.35),
              (2.52, -0.85), (2.68, -1.28), (2.90, -1.05), (3.12, -0.30),
              (3.40, 0.34), (3.80, 0.46), (4.40, 0.465), (4.85, 0.40),
              (5.12, -0.60), (5.28, -1.26), (5.44, -1.20), (5.52, -0.30),
              (5.555, 0.40), (5.582, 1.45), (5.60, 1.92), (5.618, 1.45),
              (5.645, 0.30),
              (5.80, -0.35), (5.95, -0.56), (6.15, -0.32),
              (6.55, 0.28), (7.00, 0.42), (7.35, 0.385), (7.60, 0.29),
              (7.90, -0.10), (8.05, -0.28), (8.25, -0.05),
              (8.42, 0.45), (8.462, 0.88), (8.50, 0.98), (8.538, 0.88),
              (8.58, 0.40),
              (8.80, -0.05), (9.00, -0.22), (9.35, -0.27), (9.80, -0.28)], 14)
    ax.plot(psi[:, 0], psi[:, 1], 'k-', lw=1.3, zorder=4)
    save(fig, 51)


# ---------------------------------------------------------------- fig 52
def fig_52():
    fig = plt.figure(figsize=(4.8, 2.45))
    # ---- (a) energy contours in the square zone
    ax = ax_on(fig, [0.005, 0.02, 0.46, 0.94], (-0.14, 1.30),
               (-0.17, 1.27), aspect='equal')
    n = 500
    kx = np.linspace(-np.pi, np.pi, n)
    ky = np.linspace(-np.pi, np.pi, n)
    KX, KY = np.meshgrid(kx, ky)
    F = np.cos(KX) + np.cos(KY)
    lev = [-1.80, -1.35, -0.85, -0.40, 0.0, 0.35, 0.80, 1.30, 1.75]
    ax.contour((KX + np.pi) / (2 * np.pi), (KY + np.pi) / (2 * np.pi), F,
               levels=lev, colors='k', linewidths=0.85)
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, lw=1.3, ec='k'))
    dot(ax, (0.5, 0.5), s=14)
    ax.text(0.5, 0.415, r'$0$', ha='center', va='top', fontsize=11)
    ax.text(0.5, 1.045, r'$010$', ha='center', va='bottom', fontsize=11)
    ax.text(1.05, 0.5, r'$100$', ha='left', va='center', fontsize=11)
    ax.text(1.05, -0.10, r'$(a)$', ha='left', va='center', fontsize=11)
    # ---- (b) E(k) along a cube axis
    ax = ax_on(fig, [0.47, 0.02, 0.52, 0.94], (-1.30, 1.62), (-0.20, 1.36))
    seg(ax, (-1, 0), (1, 0), lw=1.0)                      # base line
    seg(ax, (-1, 0), (-1, 1), lw=1.1)                     # zone edges
    seg(ax, (1, 0), (1, 1), lw=1.1)
    kk = np.linspace(-1, 1, 300)
    ax.plot(kk, (1 - np.cos(np.pi * kk)) / 2, 'k-', lw=1.5, zorder=4)
    arr(ax, (0, 0), (0, 1.20), ms=10)                     # E(k) axis
    ax.text(0.05, 1.22, r'$\mathcal{E}(k)$', ha='left', fontsize=11)
    seg(ax, (-0.022, 0.30), (0.022, 0.30), lw=1.0)        # E_a tick
    seg(ax, (0, 0.30), (1, 0.30), lw=0.8)                 # E_a level
    ax.text(0.045, 0.335, r'$\mathcal{E}_a$', ha='left', fontsize=11)
    arr(ax, (0.96, 0.30), (0.96, 1.0), ms=9, style='<|-|>')
    ax.text(1.01, 0.60, r'$2\mathcal{E}_{100}$', ha='left', fontsize=10)
    ax.text(-1, -0.125, r'$-\pi/a$', ha='center', fontsize=10)
    ax.text(0, -0.125, r'$O$', ha='center', fontsize=11)
    ax.text(1, -0.125, r'$\pi/a$', ha='center', fontsize=10)
    ax.text(1.06, 0.06, r'$100$', ha='left', fontsize=10)
    arr(ax, (0.12, -0.062), (0.50, -0.062), ms=9)
    ax.text(0.31, -0.145, r'$k$', ha='center', fontsize=11)
    ax.text(1.42, -0.12, r'$(b)$', ha='center', fontsize=11)
    save(fig, 52)


# ---------------------------------------------------------------- fig 53
def fig_53():
    fig = plt.figure(figsize=(4.4, 2.75))
    ax = ax_on(fig, [0.005, 0.01, 0.99, 0.98], (0, 1.72), (0, 1.0))
    # axes
    arr(ax, (0.10, 0.06), (0.10, 0.95), ms=11)
    ax.text(0.085, 0.955, r'$\mathcal{E}$', ha='right', fontsize=12)
    arr(ax, (0.10, 0.07), (0.97, 0.07), ms=11)
    ax.text(0.092, 0.035, r'$O$', ha='right', fontsize=11)
    ax.text(0.435, 0.022, r'$a$', ha='center', fontsize=11)
    arr(ax, (0.465, 0.033), (0.565, 0.033), ms=9)
    # three bands, each fanning out toward small a
    for yc, sp, lab in ((0.795, 0.085, r'$\mathcal{E}_c$'),
                        (0.580, 0.062, r'$\mathcal{E}_b$'),
                        (0.365, 0.075, r'$\mathcal{E}_a$')):
        for f in np.linspace(-1, 1, 13):
            y0 = yc + f * sp
            b = cr([(0.30, y0), (0.47, yc + f * sp * 0.30), (0.665, yc)], 10)
            ax.plot(b[:, 0], b[:, 1], 'k-', lw=0.6, zorder=3)
        seg(ax, (0.665, yc), (0.98, yc), lw=2.4)
        ax.text(0.80, yc + 0.026, lab, ha='center', fontsize=11)
        ax.text(1.01, yc, r'$N$-fold', ha='left', va='center', fontsize=10)
    brace(ax, 0.225, 0.28, 0.90, 0.045)
    ax.text(0.155, 0.59, 'Bands\nin\nsolid', ha='center', va='center',
            fontsize=10)
    brace(ax, 1.13, 0.28, 0.90, 0.045, flip=True)
    ax.text(1.20, 0.59, 'Levels of\nfree atoms', ha='left', va='center',
            fontsize=10)
    save(fig, 53)


# ------------------------------------------------------- fig 54 helper
def _well54(ax, cx):
    """Coulombic funnel v_a with bound-level comb."""
    A = 0.11
    xs = np.linspace(0.078, 0.495, 300)
    for s in (1, -1):
        ax.plot(cx + s * xs, -A / xs, 'k-', lw=1.5, zorder=4)
    seg(ax, (cx - 0.505, 0), (cx + 0.505, 0), lw=0.8)      # E = 0 level
    for d in np.arange(1, 12) * 0.088 + 0.038:              # level comb
        w = min(A / d, 0.475)
        seg(ax, (cx - w, -d), (cx + w, -d), lw=0.55, z=2)
    arr(ax, (cx, -1.5), (cx, 0.27), ms=10)
    ax.text(cx + 0.03, 0.26, r'$\mathcal{E}$', ha='left', fontsize=11)
    ax.text(cx + 0.17, 0.115, r'$r$', ha='right', fontsize=11)
    arr(ax, (cx + 0.20, 0.125), (cx + 0.40, 0.125), ms=9)
    ax.text(cx + 0.13, -1.02, r'$v_a$', ha='left', fontsize=11)


def fig_54():
    fig = plt.figure(figsize=(4.9, 1.95))
    ax = ax_on(fig, [0.005, 0.02, 0.99, 0.95], (0, 2.30), (-1.58, 0.42))
    ax.text(0.135, 0.0, r'$\mathcal{E}=0$', ha='right', va='center',
            fontsize=10)
    seg(ax, (0.145, 0), (0.20, 0), lw=0.8, ls=(0, (2.5, 2)))
    _well54(ax, 0.70)
    ax.text(1.135, -0.02, r'$+$', ha='center', va='center', fontsize=15)
    _well54(ax, 1.87)
    # one bound orbital phi_a^(j), weakly bound -> long tail under E = 0
    dx = np.linspace(-0.44, 0.44, 400)
    phi = -0.075 + 0.052 * np.exp(-(dx / 0.40) ** 2) * np.cos(2 * np.pi * dx / 0.20)
    ax.plot(1.87 + dx, phi, 'k-', lw=0.8, zorder=3)
    ax.text(2.24, -0.50, r'$\phi_a^{(j)}$', ha='left', fontsize=11)
    arr(ax, (2.23, -0.46), (2.06, -0.155), ms=9)
    save(fig, 54)


# ---------------------------------------------------------------- fig 55
def fig_55():
    fig = plt.figure(figsize=(4.7, 2.0))
    ax = ax_on(fig, [0.005, 0.02, 0.99, 0.95], (0, 1.02), (-0.80, 0.46))
    # free-electron level comb of the interstitial region
    for i in range(12):
        y = -0.035 - i * 0.024
        seg(ax, (0, y), (1, y), lw=0.55, z=2)
    seg(ax, (0, 0), (1, 0), lw=0.9, z=3)                    # v = 0 level
    x = np.linspace(0, 1, 700)
    v = np.zeros_like(x)
    for xc in (0.17, 0.50, 0.83):
        v = v - 0.62 / np.cosh((x - xc) / 0.075) ** 2
    ax.plot(x, v, 'k-', lw=1.5, zorder=4)
    arr(ax, (0.335, -0.36), (0.335, 0.30), ms=10)
    ax.text(0.348, 0.285, r'$\mathcal{E}$', ha='left', fontsize=11)
    ax.text(0.565, 0.165, r'$r$', ha='right', fontsize=11)
    arr(ax, (0.60, 0.175), (0.72, 0.175), ms=9)
    # Bloch wave psi_k drawn as +/- pair; nodes (X crossings) at the cores
    psi = 0.052 * np.cos(2 * np.pi * (x - 0.004) / 0.665)
    for sgn in (1, -1):
        ax.plot(x, sgn * psi, 'k--', lw=1.0, dashes=(4.5, 2.8), zorder=5)
    arr(ax, (0.965, -0.155), (0.925, -0.155), ms=9)
    ax.text(0.972, -0.185, r'$\psi_{\mathbf{k}}$', ha='left', fontsize=11)
    save(fig, 55)


# ---------------------------------------------------------------- fig 56
def fig_56():
    fig = plt.figure(figsize=(4.35, 4.5))
    T = 0.27
    peaks = np.array([0.25, 0.52, 0.79])     # cell boundaries (psi_0 maxima)
    atoms = np.array([0.115, 0.385, 0.655, 0.925])   # nuclei (psi_0 minima)
    # ---- top: psi_0 with flat maxima at cell boundaries, deep minima at nuclei
    ax = ax_on(fig, [0.015, 0.545, 0.955, 0.435], (-0.02, 1.0), (-1.55, 0.80))
    seg(ax, (-0.02, 0), (1, 0), lw=0.9, z=2)
    x = np.linspace(-0.02, 1, 1600)
    p = np.min(np.abs(x[:, None] - atoms[None, :]), axis=1)
    q = np.min(np.abs(x[:, None] - peaks[None, :]), axis=1)
    y = 0.42 * np.abs(np.cos(np.pi * q / T)) ** 1.6         - 1.32 * np.exp(-(p / 0.0145) ** 2)
    ax.plot(x, y, 'k-', lw=1.4, zorder=4)
    for pb in (0.25, 0.52, 0.79):
        seg(ax, (pb - 0.05, 0.42), (pb + 0.05, 0.42), lw=0.9,
            ls=(0, (4, 2.4)))
        seg(ax, (pb, 0.60), (pb, -0.52), lw=0.9, ls=(0, (4, 2.4)))
    ax.text(0.02, 0.56, r'$\psi_0$', ha='left', fontsize=12)
    # ---- bottom: crystal potential, conduction band, E(0), r_s
    ax = ax_on(fig, [0.015, 0.03, 0.955, 0.44], (-0.02, 1.0), (-0.66, 0.52))
    ax.add_patch(Rectangle((-0.02, 0), 1.02, 0.30, facecolor='white',
                           edgecolor='none', hatch='/////', zorder=1))
    seg(ax, (-0.02, 0.30), (1, 0.30), lw=0.9, z=3)
    hcs = peaks
    # E(0) level: solid between barriers, dashed across them
    xs = [-0.02]
    for hc in hcs:
        xs += [hc - 0.075, hc + 0.075]
    xs += [1.0]
    for a, b in zip(xs[0::2], xs[1::2]):
        seg(ax, (a, 0), (b, 0), lw=0.9)
    for a, b in zip(xs[1::2], xs[2::2]):
        seg(ax, (a, 0), (b, 0), lw=0.9, ls=(0, (3.5, 2.2)))
    ax.text(1.008, 0.0, r'$\mathcal{E}(0)$', ha='left', va='center',
            fontsize=10)
    # potential: narrow slots at atoms + rounded barriers between
    xb = np.linspace(-0.02, 1, 2400)
    V = np.zeros_like(xb)
    for xc in atoms:
        V -= 0.62 * np.exp(-((xb - xc) / 0.021) ** 2)
    for hc in hcs:
        V += 0.15 * np.exp(-((xb - hc) / 0.062) ** 2)
    ax.plot(xb, V, 'k-', lw=1.4, zorder=4)
    for xc in atoms:                         # left wall up to panel top
        seg(ax, (xc - 0.016, 0.437), (xc - 0.016, -0.345), lw=1.2, z=4)
    for hc in hcs:
        ax.plot([hc], [0], marker='+', color='k', ms=11, mew=1.2, zorder=6)
        seg(ax, (hc, 0.40), (hc, -0.44), lw=0.9, ls=(0, (4.5, 2.8)), z=2)
    # r_s arrow from an atom to the next cell boundary
    arr(ax, (0.385, 0.44), (0.52, 0.44), ms=9, style='<|-|>')
    ax.text(0.532, 0.428, r'$r_s$', ha='left', fontsize=11)
    ax.text(0.335, -0.22, r'$\mathcal{V}$', ha='right', fontsize=12)
    save(fig, 56)


# ---------------------------------------------------------------- fig 57
def _cores57(ax):
    R = 0.052
    for c in np.array([0.14, 0.33, 0.52, 0.71, 0.90]):
        ax.add_patch(Circle((c, 0), R, facecolor='0.94', edgecolor='k',
                            lw=0.8, hatch='...', zorder=2))
        dot(ax, (c, 0), s=10, z=5)
    seg(ax, (0.03, 0), (0.99, 0), lw=0.9, z=1)


def fig_57():
    fig = plt.figure(figsize=(4.5, 4.6))
    # ---- (a) plane wave
    ax = ax_on(fig, [0.01, 0.715, 0.98, 0.245], (0, 1), (-0.155, 0.155))
    _cores57(ax)
    x = np.linspace(0.03, 0.99, 400)
    ax.plot(x, 0.105 * np.cos(2 * np.pi * (x - 0.14) / 1.52), 'k-', lw=1.3,
            zorder=4)
    ax.text(0.5, -0.128, r'$(a)$  Plane  wave', ha='center', fontsize=10.5)
    # ---- (b) core function
    ax = ax_on(fig, [0.01, 0.375, 0.98, 0.245], (0, 1), (-0.155, 0.185))
    _cores57(ax)
    sc = 0.30
    for pts in (
        [(0.045, 0), (0.10, 0.15), (0.117, 0.58), (0.132, 0.60),
         (0.150, 0.10), (0.165, -0.42), (0.185, -0.30), (0.205, -0.02),
         (0.23, 0)],
        [(0.24, 0), (0.27, 0.02), (0.295, 0.30), (0.315, 0.33),
         (0.33, -0.05), (0.345, -0.35), (0.365, -0.12), (0.395, -0.02),
         (0.42, 0)],
        [(0.43, 0), (0.465, 0.05), (0.49, 0.16), (0.51, 0.02),
         (0.53, -0.14), (0.55, -0.04), (0.575, 0.03), (0.61, 0)],
        [(0.62, 0), (0.645, -0.05), (0.66, -0.22), (0.675, -0.30),
         (0.69, -0.12), (0.705, 0.28), (0.72, 0.33), (0.735, 0.10),
         (0.755, -0.28), (0.775, -0.33), (0.79, -0.15), (0.82, -0.02),
         (0.85, 0)],
        [(0.86, 0), (0.885, 0.12), (0.90, 0.42), (0.915, 0.40),
         (0.935, 0.05), (0.95, -0.20), (0.97, -0.05), (0.99, 0.02)]):
        q = cr([(px, py * sc) for px, py in pts], 12)
        ax.plot(q[:, 0], q[:, 1], 'k-', lw=1.1, zorder=4)
    ax.text(0.5, -0.128, r'$(b)$  Core function', ha='center', fontsize=10.5)
    # ---- (c) O.P.W. = plane wave - core function
    ax = ax_on(fig, [0.01, 0.025, 0.98, 0.245], (0, 1), (-0.155, 0.215))
    _cores57(ax)
    x = np.linspace(0.03, 0.99, 400)
    ax.plot(x, 0.105 * np.cos(2 * np.pi * (x - 0.14) / 1.52), 'k--', lw=1.2,
            dashes=(5, 3), zorder=3)
    sc = 0.30
    opw = cr([(0.03, 0.29), (0.09, 0.265), (0.115, 0.42), (0.135, 0.68),
              (0.155, 0.40), (0.185, -0.05), (0.21, -0.24), (0.245, -0.20),
              (0.27, -0.02), (0.295, 0.10), (0.315, 0.30), (0.335, 0.36),
              (0.355, 0.14), (0.375, -0.16), (0.395, -0.30), (0.42, -0.22),
              (0.45, 0.0), (0.49, 0.10), (0.52, 0.05), (0.55, -0.06),
              (0.575, -0.12), (0.61, -0.04), (0.64, 0.05), (0.66, -0.10),
              (0.685, -0.28), (0.71, -0.30), (0.735, -0.05), (0.755, 0.18),
              (0.775, 0.44), (0.80, 0.20), (0.83, -0.10), (0.855, -0.24),
              (0.885, -0.14), (0.915, 0.10), (0.935, 0.30), (0.955, 0.24),
              (0.98, 0.05)], 12)
    ax.plot(opw[:, 0], sc * opw[:, 1], 'k-', lw=1.2, zorder=4)
    ax.text(0.5, -0.128,
            r'$(c)$  O.P.W. $=$ plane wave $-$ core function',
            ha='center', fontsize=10.5)
    save(fig, 57)


# ---------------------------------------------------------------- fig 58
def fig_58():
    fig = plt.figure(figsize=(4.3, 2.65))
    ax = ax_on(fig, [0.01, 0.02, 0.98, 0.95], (-1.18, 1.18), (-0.80, 0.80),
               aspect='equal')
    clip = Circle((0, 0), 0.755, transform=ax.transData)
    R = 0.235                     # hexagon circumradius
    dxs = np.sqrt(3) * R / 2      # column spacing
    dys = 1.5 * R                 # row spacing
    rin = np.sqrt(3) / 2 * R      # inradius
    # dashed Wigner-Seitz hexagon grid (2D section), clipped to a disc
    for j in range(-2, 3):
        y = j * dys
        xoff = dxs if j % 2 else 0.0
        for i in range(-3, 4):
            x = i * 2 * dxs + xoff
            if abs(x) > 1.15 or abs(y) > 0.80:
                continue
            hexpts = [(x + R * np.cos(a), y + R * np.sin(a))
                      for a in np.arange(np.pi / 6, 2 * np.pi, np.pi / 3)]
            hx = cr(hexpts + [hexpts[0]], 8)
            ln, = ax.plot(hx[:, 0], hx[:, 1], 'k--', lw=0.95,
                          dashes=(4.5, 2.8), zorder=2)
            ln.set_clip_path(clip)
    # concentric equipotential circles of the muffin-tin wells
    rr = 0.021 + np.arange(10) * 0.019
    for j in range(-3, 4):
        y = j * dys
        xoff = dxs if j % 2 else 0.0
        for i in range(-4, 5):
            x = i * 2 * dxs + xoff
            if np.hypot(x, y) > 0.98:
                continue
            for r in rr:
                c = Circle((x, y), r, fill=False, lw=0.85, ec='k', zorder=3)
                ax.add_patch(c)
                c.set_clip_path(clip)
            if np.hypot(x, y) < 0.70:
                dot(ax, (x, y), s=8, z=5)
    save(fig, 58)


# ---------------------------------------------------------------- fig 59
def _cell59(ax, hatch):
    R = 0.155
    cs = {'TL': (-0.17, 0.17), 'TR': (0.17, 0.17),
          'BL': (-0.17, -0.17), 'BR': (0.17, -0.17)}
    for c in cs.values():
        ax.add_patch(Circle(c, R, facecolor='0.96', edgecolor='k', lw=0.9,
                            hatch=hatch, zorder=2))
    return cs


def fig_59():
    fig = plt.figure(figsize=(4.75, 2.5))
    # ---- (a)
    ax = ax_on(fig, [0.005, 0.09, 0.48, 0.86], (-0.52, 0.52), (-0.62, 0.44),
               aspect='equal')
    cs = _cell59(ax, '///')
    r = (cs['TL'][0] + 0.06, cs['TL'][1])          # point r in cell 0
    seg(ax, cs['TL'], (cs['TL'][0] + 0.135, cs['TL'][1]), lw=1.0)
    dot(ax, r, s=13)
    ax.text(r[0], r[1] + 0.035, r'$\mathbf{r}$', ha='center', fontsize=12)
    arr(ax, cs['TL'], cs['BR'], ms=12)             # lattice vector l
    arr(ax, (-0.055, 0.055), (0.0, 0.0), ms=9)
    ax.text(cs['BR'][0] + 0.05, cs['BR'][1] - 0.015, r'$\boldsymbol{l}$',
            ha='left', fontsize=12)
    rp = (cs['BR'][0] - 0.125, cs['BR'][1] + 0.125)  # source point r'
    dot(ax, rp, s=12)
    ax.text(rp[0] - 0.03, rp[1] - 0.045, r"$\mathbf{r}'$", ha='right',
            fontsize=12)
    # wave-front arcs emitted at r', travelling toward r
    c0 = rp
    th = np.degrees(np.arctan2(r[1] - rp[1], r[0] - rp[0]))
    for rad in np.linspace(0.06, 0.28, 6):
        arc(ax, c0, rad, th - 24, th + 24, lw=0.7)
    pm = (c0[0] + 0.16 * np.cos(np.radians(th + 8)),
          c0[1] + 0.16 * np.sin(np.radians(th + 8)))
    u = np.array([np.cos(np.radians(th + 8)), np.sin(np.radians(th + 8))])
    arr(ax, tuple(pm - 0.020 * u), tuple(pm + 0.012 * u), ms=8)
    ax.text(0.0, -0.545, r'$(a)$', ha='center', fontsize=11)
    # ---- (b)
    ax = ax_on(fig, [0.515, 0.09, 0.48, 0.86], (-0.52, 0.52), (-0.62, 0.44),
               aspect='equal')
    cs = _cell59(ax, '///')
    r = (cs['TL'][0] + 0.06, cs['TL'][1])
    seg(ax, cs['TL'], (cs['TL'][0] + 0.135, cs['TL'][1]), lw=1.0)
    dot(ax, r, s=13)
    ax.text(r[0] + 0.01, r[1] - 0.05, r'$\mathbf{r}$', ha='center',
            fontsize=12)
    arr(ax, cs['TL'], cs['BR'], ms=12)
    arr(ax, (-0.055, 0.055), (0.0, 0.0), ms=9)
    ax.text(cs['BR'][0] + 0.05, cs['BR'][1] - 0.015, r'$\boldsymbol{l}$',
            ha='left', fontsize=12)
    # equivalent points r'' in every cell, waves converge on r
    for key, lab in (('TL', True), ('TR', True), ('BL', True), ('BR', False)):
        rq = (cs[key][0] - 0.125, cs[key][1] + 0.125)
        dot(ax, rq, s=11)
        if lab:
            ax.text(rq[0] - 0.015, rq[1] + 0.032, r'$\mathbf{r}''$',
                    ha='center', fontsize=12)
        if key != 'TL':
            arr(ax, (rq[0] - 0.03 * np.sign(rq[0] - r[0]),
                     rq[1] - 0.03 * np.sign(rq[1] - r[1])),
                (r[0] + 0.02 * np.sign(rq[0] - r[0]),
                 r[1] + 0.02 * np.sign(rq[1] - r[1])), ms=9)
            thq = np.degrees(np.arctan2(r[1] - rq[1], r[0] - rq[0]))
            mid = (0.5 * (rq[0] + r[0]), 0.5 * (rq[1] + r[1]))
            for rad in (0.055, 0.085, 0.115):
                arc(ax, rq, rad, thq - 22, thq + 22, lw=0.6)
    ax.text(0.0, -0.545, r'$(b)$', ha='center', fontsize=11)
    save(fig, 59)


# ---------------------------------------------------------------- fig 60
def fig_60():
    fig = plt.figure(figsize=(4.25, 3.6))
    # ---- top: |psi| for true psi and pseudo phi
    ax = ax_on(fig, [0.03, 0.545, 0.95, 0.42], (0, 1.0), (-1.08, 1.10))
    arr(ax, (0.06, -0.98), (0.06, 0.98), ms=10)
    ax.text(0.05, 0.60, r'$|\psi|$', ha='right', fontsize=12)
    arr(ax, (0.06, 0), (0.97, 0), ms=10)
    ax.text(0.925, -0.125, r'$r$', ha='center', fontsize=11)
    phi = cr([(0.06, 0.0), (0.16, 0.42), (0.30, 0.72), (0.44, 0.86),
              (0.55, 0.80), (0.66, 0.55), (0.78, 0.24), (0.90, 0.085),
              (0.97, 0.05)], 14)
    ax.plot(phi[:, 0], phi[:, 1], 'k--', lw=1.3, dashes=(5.5, 3), zorder=3)
    ax.text(0.475, 0.905, r'$\phi$', ha='left', fontsize=12)
    psi = cr([(0.06, 0.0), (0.11, 0.14), (0.15, 0.15), (0.19, 0.02),
              (0.23, -0.18), (0.27, -0.22), (0.31, -0.08), (0.36, 0.14),
              (0.42, 0.36), (0.48, 0.53), (0.54, 0.56), (0.60, 0.47),
              (0.66, 0.28), (0.73, 0.02), (0.80, -0.22), (0.87, -0.34),
              (0.93, -0.33), (0.97, -0.28)], 14)
    ax.plot(psi[:, 0], psi[:, 1], 'k-', lw=1.4, zorder=4)
    ax.text(0.155, 0.19, r'$\psi$', ha='left', fontsize=12)
    # ---- bottom: true potential v and weak model potential w
    ax = ax_on(fig, [0.03, 0.035, 0.95, 0.40], (0, 1.0), (-1.12, 0.40))
    arr(ax, (0.06, -1.08), (0.06, 0.30), ms=10)
    ax.text(0.048, 0.30, r'$\mathcal{E}$', ha='right', fontsize=11)
    arr(ax, (0.06, 0), (0.97, 0), ms=10)
    ax.text(0.925, -0.105, r'$r$', ha='center', fontsize=11)
    v = cr([(0.115, -1.04), (0.16, -0.80), (0.22, -0.55), (0.30, -0.33),
            (0.40, -0.155), (0.52, -0.06), (0.66, -0.015), (0.80, -0.002),
            (0.95, 0.0)], 14)
    ax.plot(v[:, 0], v[:, 1], 'k-', lw=1.5, zorder=4)
    ax.text(0.262, -0.44, r'$v$', ha='center', fontsize=12)
    seg(ax, (0.06, 0.145), (0.44, 0.145), lw=1.2, ls=(0, (5, 3)))
    seg(ax, (0.44, 0.145), (0.44, 0), lw=1.2, ls=(0, (5, 3)))
    ax.text(0.30, 0.175, r'$w$', ha='center', fontsize=12)
    save(fig, 60)


# ---------------------------------------------------------------- fig 61
def fig_61():
    fig = plt.figure(figsize=(4.85, 2.9))
    ax = ax_on(fig, [0.005, 0.02, 0.99, 0.95], (0, 2.62), (-1.28, 0.62))
    # left: v_MT well with muffin-tin zero level
    A = 0.029
    cx = 0.42
    for s in (1, -1):
        xs = np.linspace(0.035, 0.335, 200)
        ax.plot(cx + s * xs, -A / xs, 'k-', lw=1.5, zorder=4)
    seg(ax, (cx, -0.92), (cx, 0.0), lw=1.0)
    seg(ax, (0.10, -0.12), (0.84, -0.12), lw=0.9)
    ax.text(0.66, -0.20, r'$\mathcal{E}_{MTZ}$', ha='center', fontsize=10)
    ax.text(0.70, -0.085, r'$R_s$', ha='left', fontsize=11)
    arr(ax, (0.86, -0.12), (1.03, -0.12), ms=11)
    brace(ax, 1.09, 0.30, -0.62, 0.05)
    # three l-rows: radial wave functions and surface delta functions
    x0 = 1.98
    seg(ax, (x0, 0.42), (x0, -0.64), lw=1.0, z=1)
    for yr, lab, Alab in ((0.16, r'$l=0$', r'$A_0$'),
                          (-0.13, r'$l=1$', r'$A_1$'),
                          (-0.42, r'$l=2$', r'$A_2$')):
        seg(ax, (1.16, yr), (2.44, yr), lw=1.0)
        seg(ax, (1.42, yr), (1.42, yr + 0.07), lw=1.2)      # left marker
        ax.text(1.46, yr - 0.072, lab, ha='left', fontsize=10.5)
        seg(ax, (2.42, yr), (2.42, yr + 0.155), lw=1.4)     # delta at R_s
        ax.text(2.445, yr + 0.175, Alab, ha='left', fontsize=11)
        ax.text(2.42, yr - 0.055, r'$R_s$', ha='center', fontsize=10)
    kap = 5.23
    dx = np.linspace(-0.56, 0.47, 400)
    ax.plot(x0 + dx, 0.16 + 0.26 * np.sin(kap * dx) / (kap * dx), 'k-',
            lw=1.3, zorder=4)
    ax.text(2.06, 0.48, r'$j_0(\kappa R_s)$', ha='left', fontsize=10.5)
    dx = np.linspace(-0.50, 0.44, 400)
    ax.plot(x0 + dx, 0.16 + 0.100 * np.cos(2 * np.pi * dx / 0.215), 'k--',
            lw=1.1, dashes=(4, 2.4), zorder=3)
    ax.text(2.16, 0.028, r'$R_0(r)$', ha='left', fontsize=10.5)
    save(fig, 61)


# ---------------------------------------------------------------- fig 62
def fig_62():
    fig = plt.figure(figsize=(4.85, 2.3))
    ax = ax_on(fig, [0.005, 0.02, 0.99, 0.95], (0, 2.42), (-1.30, 0.36))
    A = 0.10
    # ---------------- (a) Heine-Abarenkov
    cx = 0.60
    RM = 0.30
    arr(ax, (cx, -1.14), (cx, 0.24), ms=10)
    ax.text(cx - 0.045, 0.225, r'$\mathcal{E}$', ha='right', fontsize=11)
    arr(ax, (cx - 0.52, 0), (cx + 0.52, 0), ms=10)
    ax.text(cx + 0.475, 0.035, r'$r$', ha='center', fontsize=11)
    for s in (1, -1):
        xs = np.linspace(0.098, 0.50, 240)
        ax.plot(cx + s * xs, -A / xs, 'k--', lw=1.2, dashes=(5, 2.8),
                zorder=3)
        xs2 = np.linspace(RM, 0.50, 120)
        ax.plot(cx + s * xs2, -A / xs2, 'k-', lw=1.5, zorder=5)
    for s in (1, -1):                                   # walls at +-R_M
        seg(ax, (cx + s * RM, -A / RM), (cx + s * RM, -0.085), lw=1.5, z=4)
    for lev in (-0.085, -0.165, -0.26):                 # l-dependent floors
        seg(ax, (cx - RM, lev), (cx + RM, lev), lw=1.3, z=4)
    seg(ax, (cx - RM, 0), (cx - RM, -0.26), lw=0.9, ls=(0, (3.5, 2.2)))
    seg(ax, (cx + RM, 0), (cx + RM, -0.26), lw=0.9, ls=(0, (3.5, 2.2)))
    ax.text(cx + RM + 0.02, 0.04, r'$R_M$', ha='center', fontsize=11)
    ax.text(cx + 0.115, -0.30, r'$-A_2$', ha='left', fontsize=11)
    ax.text(cx + 0.345, -0.29, r'$w^{\rm HA}$', ha='left', fontsize=11)
    seg(ax, (cx + 0.335, -0.297), (cx + RM + 0.006, -0.262), lw=0.8)
    seg(ax, (cx + RM, -0.095), (cx + 0.44, -0.375), lw=0.8)
    seg(ax, (cx + RM, -0.175), (cx + 0.44, -0.455), lw=0.8)
    ax.text(cx + 0.445, -0.405, r'$-(A_0-A_2)$', ha='left', fontsize=10)
    ax.text(cx + 0.445, -0.487, r'$-(A_1-A_2)$', ha='left', fontsize=10)
    ax.text(cx, -1.24, r'$(a)$', ha='center', fontsize=11)
    # ---------------- (b) Shaw
    cx = 1.82
    RI, RII = 0.36, 0.21
    AI, AII = 0.058 / RI, 0.058 / RII      # floors match v_a at RI, RII
    arr(ax, (cx, -1.14), (cx, 0.24), ms=10)
    ax.text(cx - 0.045, 0.225, r'$\mathcal{E}$', ha='right', fontsize=11)
    arr(ax, (cx - 0.52, 0), (cx + 0.52, 0), ms=10)
    ax.text(cx + 0.475, 0.035, r'$r$', ha='center', fontsize=11)
    for s in (1, -1):
        xs = np.linspace(0.053, 0.50, 260)
        ax.plot(cx + s * xs, -0.058 / xs, 'k--', lw=1.2, dashes=(5, 2.8),
                zorder=3)
        xs2 = np.linspace(RI, 0.50, 120)
        ax.plot(cx + s * xs2, -0.058 / xs2, 'k-', lw=1.5, zorder=5)
    for s in (1, -1):
        seg(ax, (cx + s * RII, -AII), (cx + s * RII, -AI), lw=1.5, z=4)
        seg(ax, (cx + s * RI, -AI), (cx + s * RI, -0.058 / RI), lw=1.5, z=4)
    for lev, e, r in ((AI, r'$-A_{\rm I}$', RI, ), (AII, r'$-A_{\rm II}$', RII, )):
        seg(ax, (cx - r, -lev), (cx + r, -lev), lw=1.3, z=4)
        seg(ax, (cx + r, 0), (cx + r, -lev), lw=0.9, ls=(0, (3.5, 2.2)))
        seg(ax, (cx - r, 0), (cx - r, -lev), lw=0.9, ls=(0, (3.5, 2.2)))
    ax.text(cx + 0.045, -AI + 0.035, r'$-A_{\rm I}$', ha='left', fontsize=11)
    ax.text(cx + 0.045, -AII - 0.055, r'$-A_{\rm II}$', ha='left',
            fontsize=11)
    ax.text(cx + RI + 0.015, -AI - 0.045, r'$R_{\rm I}$', ha='left',
            fontsize=11)
    ax.text(cx + RII + 0.025, -(AII + AI) / 2, r'$R_{\rm II}$', ha='left',
            fontsize=11)
    ax.text(cx + 0.455, -0.098, r'$w^{\rm S}$', ha='left', fontsize=11)
    ax.text(cx + 0.16, -0.66, r'$v_a(r)$', ha='left', fontsize=11)
    ax.text(cx, -1.24, r'$(b)$', ha='center', fontsize=11)
    save(fig, 62)


# ---------------------------------------------------------------- fig 63
def fig_63():
    fig = plt.figure(figsize=(4.75, 2.35))
    # ---- (a) crossing without hybridization
    ax = ax_on(fig, [0.02, 0.06, 0.44, 0.90], (0, 0.74), (-0.10, 1.14))
    ox = 0.06
    arr(ax, (ox, 0), (ox, 1.06), ms=10)
    ax.text(ox - 0.025, 1.075, r'$\mathcal{E}$', ha='right', fontsize=11)
    seg(ax, (ox, 0), (ox + 0.46, 0), lw=1.0)
    arr(ax, (ox + 0.22, 0), (ox + 0.31, 0), ms=10)
    ax.text(ox + 0.265, 0.04, r'$k$', ha='center', fontsize=11)
    ax.text(ox - 0.015, -0.045, r'$O$', ha='right', fontsize=11)
    seg(ax, (ox + 0.46, 0), (ox + 0.46, 1.06), lw=1.2)
    ax.text(ox + 0.46, -0.045, r'Z.B.', ha='center', fontsize=10)
    s = cr([(ox, 0), (0.16, 0.02), (0.26, 0.05), (0.33, 0.09),
            (0.385, 0.16), (0.42, 0.25), (0.455, 0.42), (0.49, 0.67),
            (0.515, 0.90), (ox + 0.46, 0.97)], 14)
    ax.plot(s[:, 0], s[:, 1], 'k-', lw=1.4, zorder=4)
    ax.text(0.435, 0.50, r'$s$-band', ha='left', fontsize=10.5,
            rotation=64)
    d1 = cr([(ox, 0.50), (0.20, 0.485), (0.34, 0.49), (0.44, 0.52),
             (ox + 0.46, 0.555)], 12)
    d2 = cr([(ox, 0.435), (0.20, 0.425), (0.34, 0.435), (0.44, 0.455),
             (ox + 0.46, 0.465)], 12)
    ax.plot(d1[:, 0], d1[:, 1], 'k-', lw=1.3, zorder=3)
    ax.plot(d2[:, 0], d2[:, 1], 'k-', lw=1.3, zorder=3)
    ax.text(0.115, 0.545, r'$d$-bands', ha='left', fontsize=10.5)
    ax.text(ox + 0.23, -0.085, r'$(a)$', ha='center', fontsize=11)
    # ---- (b) with s-d hybridization
    ax = ax_on(fig, [0.53, 0.06, 0.44, 0.90], (0.56, 1.30), (-0.10, 1.14))
    ox = 0.62
    arr(ax, (ox, 0), (ox, 1.06), ms=10)
    ax.text(ox - 0.025, 1.075, r'$\mathcal{E}$', ha='right', fontsize=11)
    seg(ax, (ox, 0), (ox + 0.46, 0), lw=1.0)
    arr(ax, (ox + 0.22, 0), (ox + 0.31, 0), ms=10)
    ax.text(ox + 0.265, 0.04, r'$k$', ha='center', fontsize=11)
    ax.text(ox - 0.015, -0.045, r'$O$', ha='right', fontsize=11)
    seg(ax, (ox + 0.46, 0), (ox + 0.46, 1.06), lw=1.2)
    ax.text(ox + 0.46, -0.045, r'Z.B.', ha='center', fontsize=10)
    s = cr([(ox, 0), (0.72, 0.02), (0.81, 0.05), (0.88, 0.10),
            (0.925, 0.18), (0.955, 0.30), (0.98, 0.43), (0.998, 0.50),
            (1.018, 0.516), (1.038, 0.506), (1.056, 0.63), (1.072, 0.83),
            (ox + 0.46, 0.97)], 14)
    ax.plot(s[:, 0], s[:, 1], 'k-', lw=1.4, zorder=4)
    d1 = cr([(ox, 0.50), (0.74, 0.487), (0.85, 0.492), (0.93, 0.51),
             (0.99, 0.535), (1.04, 0.555), (ox + 0.46, 0.562)], 12)
    d2 = cr([(ox, 0.435), (0.71, 0.428), (0.79, 0.438), (0.855, 0.47),
             (0.90, 0.50), (0.935, 0.508), (0.965, 0.49), (0.99, 0.478),
             (1.02, 0.478), (1.05, 0.49), (ox + 0.46, 0.487)], 12)
    ax.plot(d1[:, 0], d1[:, 1], 'k-', lw=1.3, zorder=3)
    ax.plot(d2[:, 0], d2[:, 1], 'k-', lw=1.3, zorder=3)
    ax.text(ox + 0.23, -0.085, r'$(b)$', ha='center', fontsize=11)
    save(fig, 63)


# ---------------------------------------------------------------- fig 64
def fig_64():
    fig = plt.figure(figsize=(4.05, 3.45))
    ax = ax_on(fig, [0.01, 0.02, 0.98, 0.95], (0, 1.12), (-0.75, 1.34))
    arr(ax, (0.055, -0.72), (0.055, 1.26), ms=10)
    ax.text(0.037, 1.27, r'$\mathcal{E}$', ha='right', fontsize=12)
    seg(ax, (0.055, 0), (1.06, 0), lw=1.0)                    # r axis / V=0
    arr(ax, (1.0, 0), (1.06, 0), ms=10)
    ax.text(0.045, -0.055, r'$O$', ha='right', fontsize=11)
    ax.text(0.76, -0.105, r'$r$', ha='center', fontsize=11)
    arr(ax, (0.80, -0.085), (0.92, -0.085), ms=9)
    seg(ax, (0.055, 0.145), (1.06, 0.145), lw=0.9)            # E_l level
    ax.text(0.048, 0.135, r'$\mathcal{E}_l$', ha='right', fontsize=11)
    # muffin-tin well (thin)
    vmt = cr([(0.085, 1.18), (0.10, 0.55), (0.115, -0.10), (0.14, -0.45),
              (0.175, -0.55), (0.22, -0.48), (0.27, -0.30), (0.33, -0.10),
              (0.40, 0.06), (0.48, 0.125), (0.58, 0.135), (0.70, 0.10),
              (0.82, 0.055), (0.95, 0.02), (1.05, 0.008)], 14)
    ax.plot(vmt[:, 0], vmt[:, 1], 'k-', lw=1.1, zorder=3)
    ax.text(0.40, -0.44, r'$v_{MT}(r)$', ha='left', fontsize=10.5)
    # centrifugal barrier (dashed)
    xb = np.linspace(0.096, 1.05, 300)
    ax.plot(xb, 0.011 / xb ** 2, 'k--', lw=1.1, dashes=(5, 3), zorder=3)
    ax.text(0.30, 0.60, r'$\dfrac{l(l+1)}{r^2}$', ha='center', fontsize=12)
    # total effective potential (heavy)
    heav = cr([(0.098, 1.22), (0.105, 0.85), (0.12, 0.48), (0.145, 0.18),
               (0.175, -0.12), (0.21, -0.30), (0.25, -0.33), (0.30, -0.28),
               (0.36, -0.12), (0.43, 0.08), (0.50, 0.22), (0.56, 0.28),
               (0.63, 0.26), (0.72, 0.19), (0.82, 0.150), (0.93, 0.156),
               (1.05, 0.158)], 14)
    ax.plot(heav[:, 0], heav[:, 1], 'k-', lw=2.2, zorder=5)
    ax.text(0.50, 0.74, r'$v_{MT}+\dfrac{l(l+1)}{r^2}$', ha='left',
            fontsize=11)
    arr(ax, (0.495, 0.70), (0.185, 0.295), ms=10)
    # wave function of the virtual state
    psi = cr([(0.115, 0.0), (0.15, 0.20), (0.185, 0.30), (0.21, 0.24),
              (0.235, 0.06), (0.26, -0.14), (0.285, -0.24), (0.31, -0.20),
              (0.335, -0.06), (0.36, 0.10), (0.385, 0.22), (0.41, 0.27),
              (0.435, 0.22), (0.46, 0.10), (0.485, -0.02), (0.51, -0.08),
              (0.535, -0.06), (0.56, 0.02), (0.585, 0.085), (0.61, 0.105),
              (0.635, 0.09), (0.66, 0.045), (0.685, 0.175), (0.72, 0.165),
              (0.755, 0.152), (0.79, 0.165), (0.825, 0.178), (0.86, 0.170),
              (0.90, 0.158), (0.95, 0.160), (1.0, 0.160), (1.05, 0.160)], 12)
    ax.plot(psi[:, 0], psi[:, 1], 'k-', lw=1.0, zorder=4)
    ax.text(0.265, 0.295, r'$\psi$', ha='left', fontsize=12)
    ax.text(0.78, 0.215, 'Resonance', ha='left', fontsize=10)
    save(fig, 64)


# ---------------------------------------------------------------- fig 65
def fig_65():
    fig = plt.figure(figsize=(4.8, 2.45))
    # ---- (a) general point k in reciprocal space
    ax = ax_on(fig, [0.005, 0.06, 0.475, 0.90], (-0.66, 0.66), (-0.76, 0.66),
               aspect='equal')
    a = 0.30
    polyline(ax, [(-a, -a), (a, -a), (a, a), (-a, a), (-a, -a)], lw=1.3)
    for e in (a, -a):                       # dashed grid extensions
        seg(ax, (-0.52, e), (-a, e), lw=0.9, ls=(0, (4, 2.6)))
        seg(ax, (a, e), (0.52, e), lw=0.9, ls=(0, (4, 2.6)))
        seg(ax, (e, -0.52), (e, -a), lw=0.9, ls=(0, (4, 2.6)))
        seg(ax, (e, a), (e, 0.52), lw=0.9, ls=(0, (4, 2.6)))
    gs = {'1': (0.60, 0), '2': (0, 0.60), '3': (-0.60, 0), '4': (0, -0.60),
          '5': (0.424, 0.424), '6': (-0.424, 0.424),
          '7': (-0.424, -0.424), '8': (0.424, -0.424)}
    for key, p in gs.items():
        seg(ax, (0, 0), p, lw=1.1)
        u = np.array(p) / np.hypot(*p)
        m = 0.62 * np.array(p)
        arr(ax, tuple(m - 0.045 * u), tuple(m + 0.045 * u), ms=10)
        dot(ax, p, s=16)
    dot(ax, (0, 0), s=10)
    kpt = (0.175, 0.11)
    arr(ax, (0, 0), (kpt[0] - 0.008, kpt[1] - 0.005), ms=10)
    dot(ax, kpt, s=10)
    ax.text(0.155, 0.155, r'$\mathbf{k}$', ha='center', fontsize=12)
    arr(ax, (0.595, -0.003), (kpt[0] + 0.01, kpt[1] + 0.006), ms=10)
    ax.text(0.47, 0.155, r'$\mathbf{k}-\mathbf{g}_1$', ha='center',
            fontsize=11)
    ax.text(0.50, -0.06, r'$\mathbf{g}_1$', ha='center', fontsize=11)
    ax.text(0.035, 0.44, r'$\mathbf{g}_2$', ha='left', fontsize=11)
    ax.text(-0.50, 0.035, r'$\mathbf{g}_3$', ha='center', fontsize=11)
    ax.text(0.035, -0.50, r'$\mathbf{g}_4$', ha='left', fontsize=11)
    ax.text(0.33, 0.315, r'$\mathbf{g}_5$', ha='left', fontsize=11)
    ax.text(-0.33, 0.315, r'$\mathbf{g}_6$', ha='right', fontsize=11)
    ax.text(-0.36, -0.475, r'$\mathbf{g}_7$', ha='right', fontsize=11)
    ax.text(0.36, -0.475, r'$\mathbf{g}_8$', ha='left', fontsize=11)
    ax.text(0, -0.70, r'$(a)$', ha='center', fontsize=11)
    # ---- (b) symmetry points and lines in the square zone
    ax = ax_on(fig, [0.505, 0.06, 0.475, 0.90], (0.86, 2.06), (-0.76, 0.66),
               aspect='equal')
    x0, w = 1.15, 0.60
    polyline(ax, [(x0, 0), (x0 + w, 0), (x0 + w, w), (x0, w), (x0, 0)],
             lw=1.3)
    G = (x0 + w / 2, w / 2)
    X = (x0 + w, w / 2)
    M = (x0 + w, w)
    dot(ax, G, s=13)
    ax.text(G[0] - 0.035, G[1] - 0.085, r'$\Gamma$', ha='center', fontsize=13)
    dot(ax, X, s=13)
    ax.text(X[0] + 0.025, X[1], r'$X$', ha='left', va='center', fontsize=12)
    ax.text(M[0] + 0.025, M[1] + 0.015, r'$M$', ha='left', fontsize=12)
    arr(ax, (G[0] + 0.08, G[1]), (G[0] + 0.17, G[1]), ms=10)
    ax.text(G[0] + 0.165, G[1] - 0.078, r'$\Delta$', ha='center',
            fontsize=12)
    arr(ax, (G[0] + 0.075, G[1] + 0.075), (G[0] + 0.155, G[1] + 0.155), ms=10)
    ax.text(G[0] + 0.055, G[1] + 0.125, r'$\Sigma$', ha='right', fontsize=12)
    ax.text(G[0], -0.115, r'$(b)$', ha='center', fontsize=11)
    save(fig, 65)


# ---------------------------------------------------------------- fig 66
def fig_66():
    fig = plt.figure(figsize=(4.8, 2.0))
    cxs = (0.55, 1.65, 2.75)
    for cx, lab in zip(cxs, ('(a)', '(b)', '(c)')):
        ax = ax_on(fig, [(cx - 0.545) / 3.30, 0.03, 1.09 / 3.30, 0.94],
                   (cx - 0.55, cx + 0.55), (0, 1.55))
        seg(ax, (cx - 0.42, 0.18), (cx + 0.42, 0.18), lw=1.0)
        arr(ax, (cx + 0.36, 0.18), (cx + 0.42, 0.18), ms=9)
        ax.text(cx + 0.30, 0.225, r'$k$', ha='center', fontsize=11)
        ax.text(cx - 0.03, 0.125, r'$O$', ha='right', fontsize=11)
        arr(ax, (cx, 0.18), (cx, 1.40), ms=10)
        ax.text(cx - 0.035, 1.415, r'$\mathcal{E}$', ha='right',
                fontsize=11)
        P = (cx, 0.95)
        if lab == '(a)':        # six-fold degenerate: 3 curves through P
            curves = (
                [(cx - 0.40, 0.860), (cx - 0.22, 0.925), (cx - 0.07, 0.952),
                 (cx, 0.955), (cx + 0.07, 0.952), (cx + 0.22, 0.925),
                 (cx + 0.40, 0.860)],
                [(cx - 0.40, 0.620), (cx - 0.24, 0.760), (cx - 0.10, 0.900),
                 (cx, 0.952), (cx + 0.10, 0.900), (cx + 0.24, 0.760),
                 (cx + 0.40, 0.620)],
                [(cx - 0.40, 1.060), (cx - 0.22, 1.000), (cx - 0.08, 0.958),
                 (cx, 0.955), (cx + 0.08, 0.958), (cx + 0.22, 1.000),
                 (cx + 0.40, 1.060)])
        elif lab == '(b)':      # 4-fold at P (2 curves) + split-off 2-fold
            curves = (
                [(cx - 0.40, 0.660), (cx - 0.22, 0.800), (cx - 0.10, 0.900),
                 (cx - 0.02, 0.952), (cx + 0.06, 0.930), (cx + 0.16, 0.860),
                 (cx + 0.40, 0.720)],
                [(cx - 0.40, 0.720), (cx - 0.16, 0.860), (cx - 0.06, 0.930),
                 (cx + 0.02, 0.952), (cx + 0.10, 0.900), (cx + 0.22, 0.800),
                 (cx + 0.40, 0.660)],
                [(cx - 0.26, 0.635), (cx - 0.12, 0.588), (cx, 0.575),
                 (cx + 0.12, 0.588), (cx + 0.26, 0.635)])
        else:                   # completely resolved
            curves = (
                [(cx - 0.40, 0.885), (cx - 0.20, 0.925), (cx - 0.05, 0.948),
                 (cx, 0.952), (cx + 0.14, 0.955), (cx + 0.40, 0.945)],
                [(cx - 0.40, 0.780), (cx - 0.20, 0.875), (cx - 0.05, 0.938),
                 (cx, 0.955), (cx + 0.10, 0.965), (cx + 0.28, 0.975),
                 (cx + 0.40, 0.978)],
                [(cx - 0.40, 1.060), (cx - 0.24, 1.020), (cx - 0.10, 0.985),
                 (cx, 0.958), (cx + 0.10, 0.925), (cx + 0.24, 0.865),
                 (cx + 0.40, 0.800)],
                [(cx - 0.26, 0.655), (cx - 0.10, 0.622), (cx, 0.618),
                 (cx + 0.10, 0.628), (cx + 0.26, 0.660)],
                [(cx - 0.26, 0.600), (cx - 0.12, 0.608), (cx, 0.622),
                 (cx + 0.10, 0.645), (cx + 0.26, 0.675)])
        for pts in curves:
            q = cr(pts, 14)
            ax.plot(q[:, 0], q[:, 1], 'k-', lw=1.2, zorder=4)
        ax.text(cx, 0.045, lab, ha='center', fontsize=11)
    save(fig, 66)


if __name__ == '__main__':
    for f in (fig_51, fig_52, fig_53, fig_54, fig_55, fig_56, fig_57,
              fig_58, fig_59, fig_60, fig_61, fig_62, fig_63, fig_64,
              fig_65, fig_66):
        f()
