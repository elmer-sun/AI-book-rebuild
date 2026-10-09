# -*- coding: utf-8 -*-
"""Ziman, Principles of the Theory of Solids (2nd ed.), Chapter 3, Figs. 36-50.
Black-and-white textbook-style vector redraws. One function per figure."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle, Polygon, Arc

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


def ax_on(fig, rect, xlim, ylim, aspect='equal'):
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis('off')
    if aspect == 'equal':
        ax.set_aspect('equal', adjustable='box')
    return ax


def arr(ax, p0, p1, ms=11, lw=0.0, style='-|>', z=6):
    ax.annotate('', xy=tuple(p1), xytext=tuple(p0),
                arrowprops=dict(arrowstyle=style, color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms),
                zorder=z)


def seg(ax, p0, p1, lw=1.2, ls='-', z=3):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color='k', lw=lw, ls=ls,
            solid_capstyle='butt', zorder=z)


def polyline(ax, pts, lw=1.2, ls='-', z=3):
    pts = np.asarray(pts)
    ax.plot(pts[:, 0], pts[:, 1], color='k', lw=lw, ls=ls, zorder=z)


def cr(pts, n=30):
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


def arc(ax, c, r, th0, th1, lw=1.2, z=3, n=100):
    th = np.radians(np.linspace(th0, th1, n))
    ax.plot(c[0] + r * np.cos(th), c[1] + r * np.sin(th), color='k',
            lw=lw, zorder=z)


def dot(ax, p, s=14, z=8):
    ax.plot([p[0]], [p[1]], 'k.', markersize=s, zorder=z)


def hatch_rect(ax, x0, y0, x1, y1, hatch='////', lw=0.0, z=1):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor='none',
                           edgecolor='k', lw=lw, hatch=hatch, zorder=z))


def wavycirc(ax, c, r0, eps, th0=0, th1=360, n=361, lw=1.2, z=3):
    """circle modulated r = r0 (1 - eps cos 4th): bumps on diagonals, dips on axes."""
    th = np.radians(np.linspace(th0, th1, n))
    r = r0 * (1 - eps * np.cos(4 * th))
    ax.plot(c[0] + r * np.cos(th), c[1] + r * np.sin(th), color='k', lw=lw,
            zorder=z)


def nfe2(k, G, V):
    """exact two-term NFE roots with G (k, G scalars or arrays)."""
    e1 = k ** 2
    e2 = (k - G) ** 2
    avg = 0.5 * (e1 + e2)
    dif = 0.5 * (e1 - e2)
    rad = np.sqrt(dif ** 2 + V ** 2)
    return avg - rad, avg + rad


# ---------------------------------------------------------------- fig 36
def fig_36():
    fig = plt.figure(figsize=(3.2, 3.1))
    ax = ax_on(fig, [0.02, 0.02, 0.96, 0.96], [-1.55, 1.6], [-1.5, 1.55])
    # axes
    seg(ax, (0, -1.45), (0, 1.42))
    seg(ax, (-1.42, 0), (1.50, 0))
    arr(ax, (0, 1.42), (0, 1.5), ms=12)
    arr(ax, (1.50, 0), (1.58, 0), ms=12)
    ax.text(0.07, 1.40, r'$k_y$', fontsize=11)
    ax.text(1.40, -0.17, r'$k_x$', fontsize=11)
    # constant-energy circles + Fermi disc
    Rout, Rin = 1.28, 0.92
    ax.add_patch(Circle((0, 0), Rin, facecolor='none', edgecolor='k',
                        lw=0.0, hatch='////', zorder=1))
    ax.add_patch(Circle((0, 0), Rin, facecolor='none', edgecolor='k',
                        lw=1.0, zorder=3))
    ax.add_patch(Circle((0, 0), Rout, facecolor='none', edgecolor='k',
                        lw=1.0, zorder=3))
    for r in (0.15, 0.22, 0.30, 0.40, 0.49):
        ax.add_patch(Circle((0, 0), r, facecolor='none', edgecolor='k',
                            lw=0.8, zorder=3))
    # k_F arrow
    t = np.radians(40)
    arr(ax, (0.03, 0.03), (Rin * np.cos(t), Rin * np.sin(t)), ms=12)
    ax.text(0.46, 0.545, r'$k_F$', fontsize=11)
    ax.text(1.00, 0.075, r'$\mathcal{E}_F$', fontsize=11)
    save(fig, 36)


# ---------------------------------------------------------------- fig 37
def fig_37():
    fig = plt.figure(figsize=(3.6, 2.9))
    ax = ax_on(fig, [0.02, 0.02, 0.96, 0.96], [-0.15, 2.18], [-0.42, 1.2])
    P, Q, O = (0, 0), (2, 0), (1, 0.72)
    seg(ax, (1.0, 1.05), (1.0, -0.30), ls='--', lw=1.1)   # zone boundary
    ax.text(1.06, 0.97, 'Zone', fontsize=11)
    ax.text(1.06, 0.86, 'boundary', fontsize=11)
    seg(ax, P, Q)
    arr(ax, (0.62, 0), (0.90, 0), ms=13)
    ax.text(0.80, -0.115, r'$\mathbf{g}$', fontsize=11)
    seg(ax, P, O)
    seg(ax, Q, O)
    d1 = np.array(O) - np.array(P)
    d2 = np.array(O) - np.array(Q)
    m1 = P + 0.60 * d1
    m2 = Q + 0.56 * d2
    arr(ax, m1 - 0.001 * d1, m1 + 0.001 * d1, ms=13)   # arrowheads on lines
    arr(ax, m2 - 0.001 * d2, m2 + 0.001 * d2, ms=13)
    ax.text(0.36, 0.46, r'$\mathbf{k}$', fontsize=11)
    ax.text(1.63, 0.415, r'$\mathbf{k}-\mathbf{g}$', fontsize=11)
    dot(ax, P)
    dot(ax, Q)
    ax.text(0.885, 0.735, r'$O$', fontsize=12)
    ax.text(-0.035, -0.115, r'$P$', fontsize=12)
    ax.text(1.96, -0.115, r'$Q$', fontsize=12)
    save(fig, 37)


def band_lo_1d(k, V, dep_c=0.40, dep_w=0.09):
    """1-D lower band: free parabola with a flattened, depressed shelf at the
    zone boundaries (|k| = 0.5), sitting about V below the free value."""
    k = np.asarray(k, float)
    dep = 0.5 * V * (1 + np.tanh((np.abs(k) - dep_c) / dep_w))
    return k ** 2 + 0.0032 - dep


def band_up_1d(k, Etop=1.003, EB=0.33):
    """1-D second band, reduced zone: dome peaking at k = 0."""
    k = np.asarray(k, float)
    return EB + (Etop - EB) * np.sin(np.pi * (0.5 - np.abs(k))) ** 2


# ---------------------------------------------------------------- fig 38
def fig_38():
    fig = plt.figure(figsize=(3.5, 3.9))
    ax = ax_on(fig, [0.10, 0.09, 0.86, 0.87], [-0.78, 0.78], [-0.34, 1.38])
    V = 0.08
    # frame: bottom axis + boundary verticals + centre line
    seg(ax, (-0.5, 0), (0.5, 0))
    seg(ax, (-0.5, 0), (-0.5, 0.345))
    seg(ax, (0.5, 0), (0.5, 0.345))
    seg(ax, (0, 0), (0, 1.20))
    k = np.linspace(-0.5, 0.5, 600)
    ax.plot(k, band_lo_1d(k, V), 'k-', lw=1.5, zorder=4)
    ax.plot(k, band_up_1d(k), 'k-', lw=1.5, zorder=4)
    # dashed free parabola through the gaps
    for s in (1, -1):
        kd = np.linspace(0.42, 0.58, 60) * s
        ax.plot(kd, kd ** 2, 'k--', lw=1.1, zorder=3)
    ax.text(0.28, 0.70, r'$\psi^+$', fontsize=12)
    ax.text(0.315, 0.045, r'$\psi^-$', fontsize=12)
    ax.text(0.035, 0.55, r'$\mathcal{E}(k)$', fontsize=11)
    ax.text(-0.545, 0.325, r"$B'$", fontsize=12)
    ax.text(-0.545, 0.135, r"$A'$", fontsize=12)
    ax.text(0.53, 0.325, r'$B$', fontsize=12)
    ax.text(0.53, 0.135, r'$A$', fontsize=12)
    ax.text(-0.09, -0.115, r'$O$', fontsize=12)
    ax.text(-0.72, -0.115, r'$-\frac{1}{2}G$', fontsize=11)
    ax.text(0.40, -0.115, r'$+\frac{1}{2}G$', fontsize=11)
    seg(ax, (0.10, -0.225), (0.24, -0.225))
    arr(ax, (0.24, -0.225), (0.27, -0.225), ms=11)
    ax.text(0.165, -0.325, r'$k$', fontsize=11)
    save(fig, 38)


# ---------------------------------------------------------------- fig 39
def fig_39():
    fig = plt.figure(figsize=(4.6, 3.3))
    ax = ax_on(fig, [0.06, 0.10, 0.90, 0.86], [-1.12, 1.30], [-0.17, 1.10])
    V = 0.08
    seg(ax, (-1, 0), (1, 0))                    # bottom axis
    seg(ax, (-1, 0), (-1, 1.02))
    seg(ax, (1, 0), (1, 1.02))
    seg(ax, (0, 0), (0, 0.98))
    seg(ax, (-0.5, 0), (-0.5, 0.375))
    seg(ax, (0.5, 0), (0.5, 0.375))
    # lower band with depressed shelves at the boundaries
    k = np.linspace(-0.5, 0.5, 600)
    ax.plot(k, band_lo_1d(k, V), 'k-', lw=1.5, zorder=4)
    # upper branches (extended zone): flattened start, then free parabola
    for s in (1, -1):
        kk = np.linspace(0.5, 1.0, 200) * s
        E = nfe2(kk, 1.0 * np.sign(s), V)[1]
        ax.plot(kk, E, 'k-', lw=1.5, zorder=4)
    # dashed free parabola near the gaps
    for s in (1, -1):
        kd = np.linspace(0.42, 1.0, 120) * s
        ax.plot(kd, kd ** 2, 'k--', lw=1.1, zorder=3)
    ax.text(0.035, 0.60, r'$\mathcal{E}(k)$', fontsize=11)
    ax.text(-0.545, 0.335, r"$B'$", fontsize=12)
    ax.text(-0.545, 0.125, r"$A'$", fontsize=12)
    ax.text(0.53, 0.335, r'$B$', fontsize=12)
    ax.text(0.53, 0.125, r'$A$', fontsize=12)
    # gap marker 2|V_G|
    seg(ax, (0.73, 0.33), (0.88, 0.33))
    seg(ax, (0.73, 0.17), (0.88, 0.17))
    arr(ax, (0.805, 0.245), (0.805, 0.325), ms=9, lw=0.9)
    arr(ax, (0.805, 0.255), (0.805, 0.175), ms=9, lw=0.9)
    ax.text(0.79, 0.23, r'$2|\mathcal{V}_G|$', fontsize=10, ha='right')
    # G span and k arrow
    arr(ax, (-0.5, -0.10), (-0.06, -0.10), ms=10, lw=1.0)
    arr(ax, (0.06, -0.10), (0.5, -0.10), ms=10, lw=1.0)
    ax.text(0, -0.135, r'$G$', fontsize=12, ha='center')
    arr(ax, (0.62, -0.10), (0.76, -0.10), ms=10, lw=1.0)
    ax.text(0.665, -0.055, r'$k$', fontsize=11)
    save(fig, 39)


# ---------------------------------------------------------------- fig 40
def _panel40(ax, phase, label, vlabel=False):
    """phase 's': density peaks on atoms;  'p': peaks between atoms."""
    x0, x1 = -0.7, 3.7
    seg(ax, (x0, 0), (x1, 0), z=4)
    # hatched potential background
    edges = [x0] + sum(([n + 0.25, n + 0.75] for n in range(3)), []) + [x1]
    for i in range(0, len(edges), 2):
        hatch_rect(ax, edges[i], -0.62, edges[i + 1], 0.0)
    # wells + atoms
    for n in range(3):
        xc = n + 0.5
        ax.add_patch(Rectangle((xc - 0.25, -0.55), 0.5, 0.55,
                               facecolor='white', edgecolor='k', lw=1.1,
                               zorder=3))
        dot(ax, (xc, -0.28), s=13)
    # electron density |psi|^2
    xd = np.linspace(x0, x1, 700)
    if phase == 's':
        d = 0.85 * np.cos(np.pi * (xd - 0.5)) ** 2
    else:
        d = 0.85 * np.cos(np.pi * xd) ** 2
    ax.fill_between(xd, 0, d, facecolor='none', edgecolor='k', lw=0.0,
                    hatch='////', zorder=2)
    ax.plot(xd, d, 'k-', lw=1.4, zorder=4)
    ax.text(3.02, 0.93, label, fontsize=12)
    if vlabel:
        ax.text(3.42, -0.80, r'$\mathcal{V}(r)$', fontsize=11)


def fig_40():
    fig = plt.figure(figsize=(4.6, 2.75))
    ax1 = ax_on(fig, [0.03, 0.56, 0.94, 0.40], [-0.78, 3.85], [-1.35, 1.15])
    _panel40(ax1, 's', r'$|\psi^-|^2$', vlabel=True)
    arr(ax1, (0.25, -1.02), (0.66, -1.02), ms=10, lw=1.0)
    arr(ax1, (0.84, -1.02), (1.25, -1.02), ms=10, lw=1.0)
    ax1.text(0.75, -1.02, r'$a$', fontsize=12, ha='center', va='center',
             bbox=dict(fc='white', ec='none', pad=0.5))
    ax2 = ax_on(fig, [0.03, 0.04, 0.94, 0.40], [-0.78, 3.85], [-1.35, 1.15])
    _panel40(ax2, 'p', r'$|\psi^+|^2$')
    save(fig, 40)


# ---------------------------------------------------------------- fig 41
def fig_41():
    fig = plt.figure(figsize=(4.8, 1.95))
    # (a)
    ax = ax_on(fig, [0.01, 0.10, 0.47, 0.83], [-0.42, 1.45], [-0.42, 1.15])
    seg(ax, (0.25, -0.30), (0.25, 1.06))
    seg(ax, (1.0, -0.30), (1.0, 1.06))
    seg(ax, (-0.32, 0), (1.36, 0))
    seg(ax, (-0.32, 0.78), (1.36, 0.78))
    O = (0.45, 0.30)
    d = np.array([1.23 - O[0], 0.805 - O[1]])
    seg(ax, O, (O[0] + d[0], O[1] + d[1]))
    arr(ax, (O[0] + 0.94 * d[0], O[1] + 0.94 * d[1]),
        (O[0] + d[0], O[1] + d[1]), ms=9)
    dot(ax, O, s=10)
    ax.text(0.385, 0.185, r'$O$', fontsize=12)
    ax.text(1.035, 0.585, r'$A$', fontsize=12)
    ax.text(1.205, 0.71, r'$B$', fontsize=12)
    ax.text(0.42, -0.40, r'$(a)$', fontsize=12)
    # (b)
    ax = ax_on(fig, [0.53, 0.10, 0.46, 0.83], [-0.13, 1.70], [-0.42, 2.25])
    V = 0.06

    def shelf(kk, kb, w, side):
        """smoothstep shelf: EB (flat) at kb -> free parabola at kb+side*w."""
        if side < 0:
            E0, E1 = kb ** 2 - V, (kb - w) ** 2
            t = (kb - kk) / w
        else:
            E0, E1 = kb ** 2 + V, (kb + w) ** 2
            t = (kk - kb) / w
        s = 3 * t ** 2 - 2 * t ** 3
        return E0 + (E1 - E0) * s

    seg(ax, (0, 0), (0, 2.02))
    seg(ax, (0, 0), (1.55, 0))
    seg(ax, (0.85, 0), (0.85, 2.02))
    seg(ax, (1.25, 0), (1.25, 2.02))
    k = np.linspace(0.0, 1.52, 700)
    E = k ** 2 + 0.0
    for kb in (0.85, 1.25):
        mlo = (k > kb - 0.16) & (k <= kb)
        E[mlo] = shelf(k[mlo], kb, 0.16, -1)
        mhi = (k >= kb) & (k < kb + 0.20)
        E[mhi] = shelf(k[mhi], kb, 0.20, +1)
        # jump drawn as a vertical bar
        ax.plot([kb, kb], [kb ** 2 - V, kb ** 2 + V], 'k-', lw=1.5, zorder=5)
        idx = int(np.argmin(np.abs(k - kb)))
        E[idx] = np.nan
    ax.plot(k, E, 'k-', lw=1.5, zorder=4)
    kd = np.linspace(0.0, 1.52, 100)
    ax.plot(kd, kd ** 2, 'k--', lw=1.0, zorder=3)
    ax.text(0.06, 1.82, r'$\mathcal{E}(k)$', fontsize=11)
    ax.text(-0.055, -0.14, r'$O$', fontsize=12)
    ax.text(0.815, -0.15, r'$A$', fontsize=12)
    ax.text(1.215, -0.15, r'$B$', fontsize=12)
    ax.text(1.36, -0.335, r'$k$', fontsize=11)
    arr(ax, (1.43, -0.30), (1.54, -0.30), ms=9, lw=1.0)
    ax.text(0.45, -0.33, r'$(b)$', fontsize=12)
    save(fig, 41)


# ---------------------------------------------------------------- fig 42
def fig_42():
    fig = plt.figure(figsize=(4.2, 3.1))
    ax = ax_on(fig, [0.03, 0.03, 0.94, 0.94], [-0.18, 1.16], [-0.52, 0.86])
    P, Q = (0, 0), (1, 0)
    seg(ax, (0.5, 0.80), (0.5, -0.42))
    seg(ax, P, Q)
    arr(ax, (0.60, 0), (0.72, 0), ms=12)
    ax.text(0.655, -0.075, r'$\mathbf{G}$', fontsize=11)
    dot(ax, P, s=16)
    dot(ax, Q, s=16)
    ax.text(-0.03, -0.065, r'$P$', fontsize=12)
    ax.text(0.965, -0.065, r'$Q$', fontsize=12)
    # heavy branch inside the zone (through S, vertex on the boundary)
    h1 = cr([(-0.10, 0.615), (0.02, 0.565), (0.14, 0.517), (0.26, 0.472),
             (0.34, 0.444), (0.377, 0.429), (0.44, 0.399), (0.483, 0.377),
             (0.498, 0.363)], 12)
    ax.plot(h1[:, 0], h1[:, 1], 'k-', lw=2.3, zorder=5)
    # thin free circle through S and O
    arc(ax, P, 0.578, 48, 21, lw=1.0, z=4)
    # dashed: the other free circle beyond the boundary (upper and lower)
    ax.plot([0.578 * np.cos(np.radians(t)) + 1 for t in range(150, 126, -1)],
            [0.578 * np.sin(np.radians(t)) for t in range(150, 126, -1)],
            'k--', lw=1.3, zorder=4)
    th = np.radians(np.linspace(180, 212, 40))
    ax.plot(1 + 0.578 * np.cos(th), 0.578 * np.sin(th), 'k--', lw=1.3, zorder=4)
    # heavy branch S' beyond the boundary
    h2 = cr([(0.505, 0.250), (0.525, 0.185), (0.545, 0.09), (0.553, 0.0),
             (0.545, -0.12), (0.528, -0.24), (0.512, -0.315)], 12)
    ax.plot(h2[:, 0], h2[:, 1], 'k-', lw=2.3, zorder=5)
    # k arrow from P to S
    S = (0.377, 0.429)
    d = np.array(S) - np.array(P)
    m = np.array(P) + 0.66 * d
    seg(ax, P, S, lw=1.0)
    arr(ax, m - 0.012 * d / np.linalg.norm(d), m + 0.012 * d / np.linalg.norm(d),
        ms=13)
    ax.text(0.215, 0.335, r'$\mathbf{k}$', fontsize=11)
    ax.text(0.405, 0.462, r'$S$', fontsize=12)
    ax.text(0.425, 0.322, r'$O$', fontsize=12)
    ax.text(0.565, 0.243, r"$S'$", fontsize=12)
    ax.text(0.405, 0.018, r'$Z$', fontsize=11)
    ax.text(0.522, 0.018, r'$B$', fontsize=11)
    save(fig, 42)


# ---------------------------------------------------------------- fig 43
def fig_43():
    fig = plt.figure(figsize=(4.8, 3.7))
    ax = ax_on(fig, [0.02, 0.05, 0.96, 0.92], [-2.15, 2.45], [-1.5, 1.62])
    hw, hh = 1.0, 0.617
    # hatched first zone
    ax.add_patch(Rectangle((-hw, -hh), 2 * hw, 2 * hh, facecolor='none',
                           edgecolor='k', lw=0.0, hatch='////', zorder=1))
    # rectangle (solid edges)
    ax.add_patch(Rectangle((-hw, -hh), 2 * hw, 2 * hh, facecolor='none',
                           edgecolor='k', lw=1.3, zorder=3))
    # dashed extensions of the zone edges
    for s in (1, -1):
        seg(ax, (s * hw, s * hh), (s * 1.6, s * hh), ls='--', lw=1.1)
        seg(ax, (-s * hw, s * hh), (-s * 1.6, s * hh), ls='--', lw=1.1)
        seg(ax, (s * hw, s * hh), (s * hw, s * 1.24), ls='--', lw=1.1)
        seg(ax, (s * hw, -s * hh), (s * hw, -s * 1.24), ls='--', lw=1.1)
    # hexagon (bisector planes of 2g1, 2g4, +-g3 ...)
    top, rv = 1.23, 1.36
    seg(ax, (-0.70, top), (0.67, top))
    seg(ax, (-0.70, -top), (0.67, -top))
    for sx in (1, -1):
        for sy in (1, -1):
            # slanted edge through the zone corner (sx*hw, sy*hh)
            ex, ey = sx * rv, 0.0
            cx, cy = sx * 0.60, sy * top
            dx, dy = ex - cx, ey - cy
            L = np.hypot(dx, dy)
            u = np.array([dx / L, dy / L])
            p0 = (cx - 0.09 * u[0], cy - 0.09 * u[1])
            p1 = (ex + 0.09 * u[0], ey + 0.09 * u[1])
            seg(ax, p0, p1)
    dot(ax, (0, 0), s=15)
    ax.text(0.045, -0.115, r'$O$', fontsize=12)
    # reciprocal lattice vectors
    seg(ax, (0, 0), (0, 0.76))
    arr(ax, (0, 0.76), (0, 0.84), ms=12)
    dot(ax, (0, hh), s=15)
    ax.text(0.055, 0.685, r'$\mathbf{g}_1$', fontsize=11)
    seg(ax, (0, 0), (0, -0.78))
    arr(ax, (0, -0.78), (0, -0.86), ms=12)
    dot(ax, (0, -hh), s=15)
    ax.text(0.06, -0.735, r'$\mathbf{g}_4$', fontsize=11)
    seg(ax, (-1.0, 0), (1.88, 0), lw=1.0)
    arr(ax, (1.52, 0), (1.62, 0), ms=11)
    dot(ax, (1.88, 0), s=15)
    ax.text(1.66, -0.135, r'$\mathbf{g}_2$', fontsize=11)
    seg(ax, (0, 0), (1.92, 1.18), lw=1.0)
    d3 = np.array([1.92, 1.18])
    u3 = d3 / np.linalg.norm(d3)
    m3 = 0.80 * d3
    arr(ax, m3 - 0.02 * u3, m3 + 0.02 * u3, ms=11)
    dot(ax, tuple(d3), s=15)
    ax.text(1.70, 0.845, r'$\mathbf{g}_3$', fontsize=11)
    # P, P'
    dot(ax, (0.54, hh), s=15)
    ax.text(0.505, 0.695, r'$P$', fontsize=12)
    dot(ax, (0.54, -hh), s=15)
    ax.text(0.455, -0.525, r"$P'$", fontsize=12)
    # the oblique line carrying X1..X4
    seg(ax, (-1.95, -0.80), (1.03, 0.62), lw=1.0)
    for xl, yl, lab in ((-0.87, -0.22, r'$X_1$'), (-1.17, -0.335, r'$X_2$'),
                        (-1.55, -0.475, r'$X_3$'), (-1.93, -0.685, r'$X_4$')):
        ax.text(xl, yl, lab, fontsize=10)
    save(fig, 43)


# ---------------------------------------------------------------- fig 44
def fig_44():
    fig = plt.figure(figsize=(4.0, 3.5))
    ax = ax_on(fig, [0.03, 0.03, 0.94, 0.94], [-1.95, 1.95], [-1.6, 1.6])
    top, rv = 1.16, 1.47
    # hexagon
    hexv = [(-0.60, top), (0.60, top), (rv, 0), (0.60, -top), (-0.60, -top),
            (-rv, 0)]
    ax.add_patch(Polygon(hexv, closed=True, facecolor='none', edgecolor='k',
                         lw=1.3, zorder=3))
    # rectangle
    ax.add_patch(Rectangle((-1, -0.63), 2, 1.26, facecolor='none',
                           edgecolor='k', lw=1.3, zorder=3))
    # centre contours
    dot(ax, (0, 0), s=14)
    ax.text(0.03, -0.165, r'$O$', fontsize=12, ha='left')
    ax.add_patch(Circle((0, 0), 0.115, facecolor='none', edgecolor='k',
                        lw=1.3, zorder=4))
    ax.add_patch(Circle((0, 0), 0.26, facecolor='none', edgecolor='k',
                        lw=1.3, zorder=4))
    wavycirc(ax, (0, 0), 0.42, 0.08, lw=1.3)
    wavycirc(ax, (0, 0), 0.58, 0.15, lw=1.3)
    # outer wavy loop clipped to the rectangle
    th = np.radians(np.linspace(0, 360, 721))
    r = 0.74 * (1 - 0.18 * np.cos(4 * th))
    xs, ys = r * np.cos(th), r * np.sin(th)
    inside = (np.abs(xs) < 1.0) & (np.abs(ys) < 0.63)
    xs2, ys2 = xs.copy(), ys.copy()
    xs2[~inside] = np.nan
    ax.plot(xs2, ys2, 'k-', lw=1.3, zorder=4)
    # arcs bulging out of the top/bottom zone edges
    for cx, r in ((-0.45, 0.24), (0.22, 0.16)):
        arc(ax, (cx, 0.63), r, 15, 165, lw=1.3)
        arc(ax, (-cx, -0.63), r, 195, 345, lw=1.3)
    # corner wraps of the rectangle
    for sx in (1, -1):
        for sy in (1, -1):
            c = (sx, sy * 0.63)
            a0, a1 = (90, 180) if (sx < 0 and sy > 0) else \
                     ((0, 90) if sx > 0 and sy > 0 else
                      ((180, 270) if sx < 0 else (270, 360)))
            arc(ax, c, 0.19, a0, a1, lw=1.3)
    # hexagon corner arcs (top/bottom)
    for sx in (1, -1):
        for r in (1.30, 1.46):
            a0, a1 = (246, 286) if sx > 0 else (254, 294)
            arc(ax, (0, 2.32), r, a0, a1, lw=1.3)
            b0, b1 = (74, 114) if sx > 0 else (66, 106)
            arc(ax, (0, -2.32), r, b0, b1, lw=1.3)
    # hexagon side vertex arcs (left/right)
    for sx in (1, -1):
        for r in (1.55, 1.75, 1.95):
            a0, a1 = (147, 213) if sx < 0 else (-33, 33)
            arc(ax, (sx * 2.94, 0), r, a0, a1, lw=1.3)
    # arcs parallel to the slants (centres at the diagonal lattice points)
    for sx in (1, -1):
        for sy in (1, -1):
            c = (sx * 2.0, sy * 1.26)
            if sx > 0 and sy > 0:
                a0, a1 = 199, 229
            elif sx < 0 and sy > 0:
                a0, a1 = 311, 341
            elif sx > 0 and sy < 0:
                a0, a1 = 131, 161
            else:
                a0, a1 = 19, 49
            for r in (1.26, 1.40):
                arc(ax, c, r, a0, a1, lw=1.3)
    # arcs crossing the vertical zone edges
    for sy in (1, -1):
        for r in (0.28, 0.44):
            arc(ax, (-1, sy * 0.30), r, 100, 260, lw=1.3)
            arc(ax, (1, -sy * 0.30), r, 280, 80, lw=1.3)
    # labels
    ax.text(0.27, 1.235, r'$A$', fontsize=12)
    ax.text(0.665, 1.20, r'$Q$', fontsize=12)
    ax.text(0.845, 0.985, r"$C'$", fontsize=12)
    ax.text(0.665, 0.685, r'$P$', fontsize=12)
    ax.text(-1.365, 0.315, r"$B'$", fontsize=12)
    ax.text(-1.80, -0.045, r'$Q$"', fontsize=12)
    ax.text(-1.425, -0.35, r'$C$', fontsize=12)
    ax.text(0.60, -0.545, r"$P'$", fontsize=12)
    ax.text(0.815, -1.045, r'$B$', fontsize=12)
    ax.text(0.27, -1.285, r"$A'$", fontsize=12)
    ax.text(0.665, -1.315, r"$Q'$", fontsize=12)
    save(fig, 44)


# ---------------------------------------------------------------- fig 45
def fig_45():
    fig = plt.figure(figsize=(4.0, 2.4))
    ax = ax_on(fig, [0.02, 0.06, 0.96, 0.90], [-0.06, 2.06], [-0.10, 1.30])
    ax.add_patch(Rectangle((0, 0), 2, 1.2, facecolor='none', edgecolor='k',
                           lw=1.4, zorder=3))
    apex1, apex2 = (0.80, 0.60), (1.447, 0.60)
    seg(ax, (0, 1.2), apex1)
    seg(ax, (0, 0), apex1)
    seg(ax, (2, 1.2), apex2)
    seg(ax, (2, 0), apex2)
    seg(ax, apex1, (1.107, 0.60))
    cx, cy, r = 1.331, 0.60, 0.224
    arc(ax, (cx, cy), r, 47, 169, lw=2.2, z=5)
    arc(ax, (cx, cy), r, 194, 294, lw=2.2, z=5)
    ax.text(1.045, 0.655, r"$A'$", fontsize=12)
    ax.text(1.045, 0.505, r'$A$', fontsize=12)
    ax.text(1.295, 0.685, r"$Q'$", fontsize=12)
    ax.text(1.30, 0.475, r'$Q$', fontsize=12)
    ax.text(1.495, 0.625, r'$Q$"', fontsize=12)
    ax.text(1.395, 0.795, r'$B$', fontsize=12)
    ax.text(1.555, 0.745, r"$B'$", fontsize=12)
    ax.text(1.575, 0.445, r'$C$', fontsize=12)
    ax.text(1.405, 0.315, r"$C'$", fontsize=12)
    save(fig, 45)


# ---------------------------------------------------------------- fig 46
def _rect46(ax):
    ax.add_patch(Rectangle((-1, -0.622), 2, 1.244, facecolor='none',
                           edgecolor='k', lw=1.4, zorder=3))


def fig_46():
    fig = plt.figure(figsize=(4.8, 1.85))
    # first zone
    ax = ax_on(fig, [0.015, 0.16, 0.44, 0.75], [-1.06, 1.06], [-0.70, 0.70])
    _rect46(ax)
    dot(ax, (0, 0), s=13)
    ax.add_patch(Circle((0, 0), 0.13, facecolor='none', edgecolor='k',
                        lw=1.3, zorder=4))
    ax.add_patch(Circle((0, 0), 0.235, facecolor='none', edgecolor='k',
                        lw=1.3, zorder=4))
    wavycirc(ax, (0, 0), 0.33, 0.13, lw=1.3)
    wavycirc(ax, (0, 0), 0.47, 0.16, lw=1.3)
    for sx in (1, -1):
        for sy in (1, -1):
            c = (sx, sy * 0.622)
            a0, a1 = ((90, 180) if sx < 0 and sy > 0 else
                      (0, 90) if sx > 0 and sy > 0 else
                      (180, 270) if sx < 0 else (270, 360))
            for r in (0.42, 0.26):
                arc(ax, c, r, a0, a1, lw=1.3)
    arc(ax, (0, 0.622), 0.25, 195, 345, lw=1.3)
    arc(ax, (0, -0.622), 0.25, 15, 165, lw=1.3)
    arc(ax, (-1, 0), 0.30, -78, 78, lw=1.3)
    arc(ax, (1, 0), 0.30, 102, 258, lw=1.3)
    ax.text(0, -0.88, 'First zone', fontsize=12, ha='center')
    # second zone
    ax = ax_on(fig, [0.545, 0.16, 0.44, 0.75], [-1.06, 1.06], [-0.70, 0.70])
    _rect46(ax)
    for sx in (1, -1):
        for r in (0.27, 0.165):
            ax.add_patch(Circle((sx * 0.46, 0), r, facecolor='none',
                                edgecolor='k', lw=1.3, zorder=4))
    for r in (0.32, 0.20):
        arc(ax, (0, 0.622), r, 200, 340, lw=1.3)
        arc(ax, (0, -0.622), r, 20, 160, lw=1.3)
    for sx in (1, -1):
        for sy in (1, -1):
            c = (sx, sy * 0.622)
            a0, a1 = ((90, 180) if sx < 0 and sy > 0 else
                      (0, 90) if sx > 0 and sy > 0 else
                      (180, 270) if sx < 0 else (270, 360))
            for r in (0.34, 0.20):
                arc(ax, c, r, a0, a1, lw=1.3)
    ax.text(0, -0.88, 'Second zone', fontsize=12, ha='center')
    save(fig, 46)


# ---------------------------------------------------------------- fig 47
def fig_47():
    fig = plt.figure(figsize=(4.0, 3.1))
    ax = ax_on(fig, [0.02, 0.02, 0.96, 0.96], [-1.9, 1.9], [-1.62, 1.62])
    a2, b = 1.0, 0.63          # half spacings: lattice at (+-1, +-0.63)
    for sy in (1, -1):
        seg(ax, (-1.45, sy * b), (1.45, sy * b), lw=1.0)
    for sx in (1, -1):
        seg(ax, (sx, -1.18), (sx, 1.18), lw=1.0)
    # circles around lattice points (zone corners)
    for sx in (1, -1):
        for sy in (1, -1):
            for r in (0.265, 0.483):
                ax.add_patch(Circle((sx, sy * b), r, facecolor='none',
                                    edgecolor='k', lw=1.1, zorder=3))
    # circles around cell centres
    for c in ((0, 0), (2, 0), (-2, 0), (0, 1.26), (0, -1.26)):
        if c == (0, 0):
            dot(ax, c, s=13)
        for r in (0.20, 0.40):
            ax.add_patch(Circle(c, r, facecolor='none', edgecolor='k',
                                lw=1.2, zorder=3))
    # repeated first-zone wavy contours
    for c in ((0, 0), (2, 0), (-2, 0), (0, 1.26), (0, -1.26)):
        wavycirc(ax, c, 0.85, 0.15, lw=1.6)
    ax.text(0.09, 0.685, r'$P$', fontsize=12)
    ax.text(0.10, -0.545, r"$P'$", fontsize=12)
    save(fig, 47)


# ---------------------------------------------------------------- fig 48
def fig_48():
    fig = plt.figure(figsize=(3.8, 3.8))
    ax = ax_on(fig, [0.02, 0.02, 0.96, 0.96], [-1.55, 1.55], [-1.55, 1.55])
    R = 1.0
    a, b = 1.145, 0.88
    # lattice grid lines through the neighbouring lattice points
    for sx in (1, -1):
        seg(ax, (sx * a / 2, -1.38), (sx * a / 2, 1.38), lw=1.0)
    for sy in (1, -1):
        seg(ax, (-1.5, sy * b / 2), (1.5, sy * b / 2), lw=1.0)
    # free-electron spheres about the origin and the neighbouring
    # reciprocal lattice points
    centres = [(0, 0), (a / 2, b / 2), (-a / 2, b / 2), (a / 2, -b / 2),
               (-a / 2, -b / 2), (0, b), (0, -b)]
    for i, c in enumerate(centres):
        if i == 0:
            ax.add_patch(Circle(c, R, facecolor='none', edgecolor='k',
                                lw=0.0, hatch='////', zorder=1))
        lw = 1.4 if i == 0 else 1.0
        ax.add_patch(Circle(c, R, facecolor='none', edgecolor='k', lw=lw,
                            zorder=3))
    dot(ax, (0, 0), s=13)
    dot(ax, (0, b), s=13)
    dot(ax, (0, -b), s=13)
    save(fig, 48)


# ---------------------------------------------------------------- fig 49
def _astroid_diag(ax, c, s, lw=1.4):
    """4-point star, tips on the diagonals, concave flanks."""
    t = np.linspace(0, 2 * np.pi, 361)
    X = s * np.cos(t) ** 3
    Y = s * np.sin(t) ** 3
    xr = (X - Y) / np.sqrt(2)
    yr = (X + Y) / np.sqrt(2) * 1.08
    pts = np.stack([c[0] + xr, c[1] + yr], axis=1)
    ax.add_patch(Polygon(pts, closed=True, facecolor='none', edgecolor='k',
                         lw=0.0, hatch='////', zorder=2))
    ax.plot(np.append(pts[:, 0], pts[0, 0]), np.append(pts[:, 1], pts[0, 1]),
            'k-', lw=lw, zorder=4)


def _astroid_ax(ax, c, dx, dy, lw=1.4):
    t = np.linspace(0, 2 * np.pi, 361)
    pts = np.stack([c[0] + dx * np.cos(t) ** 3, c[1] + dy * np.sin(t) ** 3],
                   axis=1)
    ax.add_patch(Polygon(pts, closed=True, facecolor='none', edgecolor='k',
                         lw=0.0, hatch='////', zorder=2))
    ax.plot(np.append(pts[:, 0], pts[0, 0]), np.append(pts[:, 1], pts[0, 1]),
            'k-', lw=lw, zorder=4)


def fig_49():
    fig = plt.figure(figsize=(4.8, 3.7))
    # first zone (full)
    ax = ax_on(fig, [0.04, 0.63, 0.30, 0.30], [-0.8, 0.8], [-0.66, 0.66])
    ax.add_patch(Rectangle((-0.73, -0.60), 1.46, 1.20, facecolor='white',
                           edgecolor='k', lw=1.4, hatch='////', zorder=2))
    ax.text(0, -0.90, 'First zone (full)', fontsize=11, ha='center')
    # second zone
    ax = ax_on(fig, [0.50, 0.63, 0.46, 0.30], [-1.32, 1.32], [-0.56, 0.56])
    ax.add_patch(Rectangle((-1.28, -0.335), 2.56, 0.67, facecolor='none',
                           edgecolor='k', lw=0.0, hatch='////', zorder=1))
    # notch bites at the panel edges (dashed, periodic continuation)
    for sx in (1, -1):
        y0, y1 = (0.10, -0.165) if sx < 0 else (-0.10, 0.165)
        ax.add_patch(Rectangle((sx * 1.28 - (0.34 if sx > 0 else 0),
                                min(y0, y1) if sx > 0 else min(y0, y1)),
                               0.0, 0.0, facecolor='none'))
        xn = 0.98 * sx
        xs = [sx * 1.30, xn, xn, sx * 1.30]
        ys = [y0, y0, y1, y1]
        ax.add_patch(Rectangle((min(xs), min(ys)), max(xs) - min(xs),
                               max(ys) - min(ys), facecolor='white',
                               edgecolor='none', zorder=2))
        polyline(ax, list(zip(xs, ys)), ls='--', lw=1.1, z=4)
    # hole in the middle
    t = np.linspace(0, 1, 60)
    bez = []
    corners = [(-0.30, 0.115), (0.30, 0.115), (0.30, -0.115), (-0.30, -0.115)]
    ctrls = [(0.0, 0.093), (0.235, 0.0), (0.0, -0.093), (-0.235, 0.0)]
    for i in range(4):
        p0 = np.array(corners[i])
        p2 = np.array(corners[(i + 1) % 4])
        pc = np.array(ctrls[i])
        seg_t = (1 - t)[:, None] ** 2 * p0 + 2 * ((1 - t) * t)[:, None] * pc \
            + t[:, None] ** 2 * p2
        bez.append(seg_t)
    hole = np.vstack(bez)
    ax.add_patch(Polygon(hole, closed=True, facecolor='white',
                         edgecolor='k', lw=1.7, zorder=3))
    for sx in (1, -1):
        seg(ax, (sx * 0.62, -0.52), (sx * 0.62, 0.52), ls='-.',
             lw=1.0, z=4)
    # solid central edges, dashed beyond
    for sy in (1, -1):
        seg(ax, (-0.62, sy * 0.335), (0.62, sy * 0.335), lw=1.5, z=4)
        for sx in (1, -1):
            seg(ax, (sx * 0.62, sy * 0.335), (sx * 1.30, sy * 0.335),
                ls='--', lw=1.1, z=4)
    ax.text(0, -0.80, 'Second zone', fontsize=11, ha='center')
    # third zone
    ax = ax_on(fig, [0.06, 0.06, 0.38, 0.48], [-1.25, 1.25], [-1.0, 1.0])
    for sx in (1, -1):
        seg(ax, (sx * 0.75, -0.93), (sx * 0.75, 0.93), lw=1.0)
    for sy in (1, -1):
        seg(ax, (-1.13, sy * 0.55), (1.13, sy * 0.55), lw=1.0)
    for sx in (1, -1):
        for sy in (1, -1):
            _astroid_diag(ax, (sx * 0.75, sy * 0.55), 0.27)
    ax.text(0, -1.22, 'Third zone', fontsize=11, ha='center')
    # fourth zone
    ax = ax_on(fig, [0.545, 0.06, 0.38, 0.48], [-1.25, 1.25], [-1.0, 1.0])
    for sx in (1, -1):
        seg(ax, (sx * 0.70, -0.93), (sx * 0.70, 0.93), lw=1.0)
    for sy in (1, -1):
        seg(ax, (-1.10, sy * 0.57), (1.10, sy * 0.57), lw=1.0)
    for sx in (1, -1):
        for sy in (1, -1):
            _astroid_ax(ax, (sx * 0.70, sy * 0.57), 0.185, 0.215)
    ax.text(0, -1.22, 'Fourth zone', fontsize=11, ha='center')
    save(fig, 49)


# ---------------------------------------------------------------- fig 50
def fig_50():
    fig = plt.figure(figsize=(3.4, 4.2))
    ax = ax_on(fig, [0.06, 0.03, 0.88, 0.94], [-1.32, 1.32], [-0.14, 1.44])
    P, Q, O = (-1, 0), (1, 0), (0, 0.83)
    R = 1.30
    # zone boundary + base line
    seg(ax, (0, 1.38), (0, 0.06), ls='--', lw=1.2)
    seg(ax, P, Q)
    arr(ax, (0.36, 0), (0.52, 0), ms=12)
    ax.text(0.43, -0.085, r'$\mathbf{G}$', fontsize=11)
    dot(ax, P, s=16)
    dot(ax, Q, s=16)
    ax.text(-1.05, -0.085, r'$P$', fontsize=12)
    ax.text(0.95, -0.085, r'$Q$', fontsize=12)
    # free-electron circles through O
    arc(ax, P, R, 26, 79, lw=1.0, z=4)
    arc(ax, Q, R, 101, 154, lw=1.0, z=4)
    dot(ax, O, s=10)
    ax.text(0.045, 0.775, r'$O$', fontsize=12)
    S, Sp = (-0.22, 1.00), (0.24, 0.645)
    # upper pair of branch-1 sheets, touching at S
    A1 = cr([(-1.02, 1.175), (-0.60, 1.088), (-0.35, 1.022), S,
             (-0.05, 0.992), (0.30, 1.000), (0.60, 1.055), (0.95, 1.17)], 12)
    A2 = cr([(-1.02, 1.132), (-0.60, 1.052), (-0.38, 1.008), S,
             (-0.05, 0.955), (0.30, 0.962), (0.60, 1.015), (0.95, 1.125)], 12)
    ax.plot(A1[:, 0], A1[:, 1], 'k-', lw=2.0, zorder=5)
    ax.plot(A2[:, 0], A2[:, 1], 'k-', lw=2.0, zorder=5)
    # lower pair of branch-2 sheets
    C1 = cr([(-1.0, 0.50), (-0.60, 0.575), (-0.30, 0.635), (0, 0.655),
             Sp, (0.50, 0.63), (0.75, 0.575), (1.0, 0.49)], 12)
    C2 = cr([(-1.0, 0.455), (-0.60, 0.52), (-0.30, 0.575), (0, 0.595),
             (0.24, 0.592), (0.50, 0.575), (0.75, 0.52), (1.0, 0.445)], 12)
    ax.plot(C1[:, 0], C1[:, 1], 'k-', lw=2.0, zorder=5)
    ax.plot(C2[:, 0], C2[:, 1], 'k-', lw=2.0, zorder=5)
    # incident and diffracted wave vectors ending at S
    d1 = np.array(S) - np.array(P)
    seg(ax, P, S, lw=1.0)
    m1 = np.array(P) + 0.55 * d1
    u1 = d1 / np.linalg.norm(d1)
    arr(ax, m1 - 0.02 * u1, m1 + 0.02 * u1, ms=13)
    ax.text(-0.66, 0.40, r'$\mathbf{k}$', fontsize=11)
    d2 = np.array(S) - np.array(Q)
    seg(ax, Q, S, lw=1.0)
    m2 = np.array(Q) + 0.55 * d2
    u2 = d2 / np.linalg.norm(d2)
    arr(ax, m2 - 0.02 * u2, m2 + 0.02 * u2, ms=13)
    ax.text(0.50, 0.37, r'$\mathbf{k}-\mathbf{G}$', fontsize=11)
    dot(ax, S, s=16)
    dot(ax, Sp, s=16)
    ax.text(-0.26, 1.045, r'$S$', fontsize=13)
    ax.text(0.265, 0.575, r"$S'$", fontsize=13)
    save(fig, 50)


if __name__ == '__main__':
    for f in (fig_36, fig_37, fig_38, fig_39, fig_40, fig_41, fig_42,
              fig_43, fig_44, fig_45, fig_46, fig_47, fig_48, fig_49,
              fig_50):
        f()
