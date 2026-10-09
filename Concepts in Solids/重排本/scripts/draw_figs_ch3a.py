# -*- coding: utf-8 -*-
"""
Redraw Figures 23-31 of P. W. Anderson, "Concepts in Solids" (chapter 3, part a).
Black-and-white textbook style, vector PDF output + PNG previews for self-check.

Original pages (PDF page numbers of the scanned book):
  fig 23: p102  open orbits across zone boundaries (magnetic case)
  fig 24: p104  E vs k repeated-zone parabolas, Zener breakdown
  fig 25: p106  tight-binding orbit with "Hops" in repeated zone
  fig 26: p107  Bloch wave = envelope x Wannier bells
  fig 27: p108  a_n bells / linear potential r / stair-step R
  fig 28: p108  X = r - R sawtooth
  fig 29: p113  scattering out of the Fermi sphere
  fig 30: p122  quasi-particle delta spike + continuum
  fig 31: p124  polarization spheres of radius R and dR
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
    'hatch.linewidth': 0.55,
})

OUT = r'E:\AI整理书籍\安德森\重排本\figures'
PREV = os.path.join(OUT, 'preview')
os.makedirs(PREV, exist_ok=True)

DASH = (0, (5, 3))
KD = dict(color='k', linestyle=DASH)


def savefig(fig, key):
    fig.savefig(os.path.join(OUT, f'fig_{key}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, f'fig_{key}.png'), dpi=160, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


def sstep(t):
    """smoothstep 0->1, vectorized, clipped."""
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def S(x, a, w):
    """smooth 0->1 transition centred at a with half-width w."""
    return sstep((x - (a - w)) / (2 * w))


def arrow(ax, p0, p1, ms=9, lw=1.1, rad=0.0, style='-|>', ls='-'):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, color='k', lw=lw,
                                mutation_scale=ms, linestyle=ls,
                                connectionstyle=f'arc3,rad={rad}'))


# ---------------------------------------------------------------- fig 23 ----
def fig_23():
    """Open orbits in a magnetic field: box = 4 zones; two possible orbits."""
    fig, ax = plt.subplots(figsize=(3.9, 1.7))
    # zone box with 4 cells
    ax.plot([0, 4, 4, 0, 0], [0, 0, 1, 1, 0], 'k-', lw=1.2)
    for xv in (1, 2, 3):
        ax.plot([xv, xv], [0, 1], 'k-', lw=1.2)
    # upper orbit: periodic bumps, one per cell, lower level between bumps
    x = np.linspace(0, 4, 2000)
    y = np.full_like(x, 0.68)
    for i in range(4):
        y = y + 0.16 * (S(x, i + 0.19, 0.05) - S(x, i + 0.80, 0.05))
    ax.plot(x, y, 'k-', lw=1.3)
    # lower orbit: staircase drifting out through the bottom of the box
    x2 = np.linspace(0, 2.37, 1500)
    y2 = (0.40
          - 0.115 * S(x2, 0.50, 0.06)
          - 0.705 * S(x2, 1.13, 0.10)
          - 0.330 * S(x2, 1.84, 0.08)
          + 0.050 * S(x2, 2.30, 0.045))
    ax.plot(x2, y2, 'k-', lw=1.3)
    ax.text(-0.10, 0.36, 'or', ha='right', va='center')
    ax.set_xlim(-0.55, 4.08)
    ax.set_ylim(-0.92, 1.07)
    ax.axis('off')
    savefig(fig, 23)


# ---------------------------------------------------------------- fig 24 ----
def fig_24():
    """E-k repeated-zone parabolas, zone boundary BZ, states k and k-K."""
    fig, ax = plt.subplots(figsize=(4.3, 2.9))
    s, K, Emax = 5.5, 0.2, 0.426
    dxm = np.sqrt(Emax / s)
    x0 = np.linspace(-dxm, dxm, 500)
    ax.plot(x0, s * x0**2, 'k-', lw=1.4)                      # parabola at k=0
    xk = np.linspace(K - dxm, K + dxm, 500)
    ax.plot(xk, s * (xk - K)**2, 'k-', lw=1.4)                # parabola at k=K
    # horizontal k axis
    ax.plot([-0.24, 0.505], [0, 0], 'k-', lw=1.2)
    ax.text(0.517, 0.004, '$k$', ha='left', va='center')
    ax.text(-0.205, 0.400, '$E$', ha='center', va='bottom')
    # thin dimension lines at k=0 and k=K (extend a bit below axis)
    for xv in (0.0, K):
        ax.plot([xv, xv], [0.0, 0.34], 'k-', lw=0.8)
        ax.plot([xv, xv], [-0.060, 0.0], 'k-', lw=0.8)
    # K dimension arrow
    arrow(ax, (0.0, -0.046), (K, -0.046), ms=7, lw=1.0, style='<|-|>')
    ax.text(0.1, -0.085, '$K$', ha='center', va='center')
    # BZ boundary line through the crossing k=K/2 (runs down to just above the axis)
    ax.plot([K / 2, K / 2], [0.012, 0.415], 'k-', lw=0.9)
    ax.text(K / 2, 0.435, 'BZ', ha='center', va='bottom')
    # states k(t) and k(t)-K (same energy: dashed horizontal; same abscissa: dashed vertical)
    dk = 0.171                       # |k| offset of the k-K state on the k=0 parabola
    Ekk = s * dk**2
    xkdot = 0.029                    # abscissa of k(t) (and of k-K on the shifted parabola)
    ax.plot([-dk], [Ekk], 'ko', ms=4.5)
    ax.plot([xkdot], [s * xkdot**2], 'ko', ms=4.5)
    ax.plot([-dk, xkdot], [Ekk, Ekk], lw=1.0, **KD)
    ax.plot([xkdot, xkdot], [s * xkdot**2, Ekk], lw=1.0, **KD)
    ax.text(-dk - 0.03, Ekk, '$k-K$', ha='right', va='center')
    ax.text(xkdot + 0.022, Ekk + 0.024, '$k-K$', ha='left', va='center')
    ax.text(xkdot + 0.017, 0.024, '$k$', ha='left', va='center')
    arrow(ax, (xkdot + 0.030, 0.030), (xkdot + 0.058, 0.050), ms=6, lw=1.0)
    # motion arrows (k increasing: down the left branches, up the right ones)
    def par(p):  # point on P0
        return (p, s * p * p)

    def parK(p):
        return (p, s * (p - K)**2)

    arrow(ax, par(-0.196), par(-0.179), ms=8)          # on k=0 left branch
    arrow(ax, parK(0.040), parK(0.053), ms=8)          # on k=K left branch
    arrow(ax, par(0.134), par(0.156), ms=8)            # on k=0 right branch
    arrow(ax, parK(0.308), parK(0.327), ms=8)          # on k=K right branch
    ax.set_xlim(-0.263, 0.528)
    ax.set_ylim(-0.085, 0.445)
    ax.axis('off')
    savefig(fig, 24)


# ---------------------------------------------------------------- fig 25 ----
def fig_25():
    """Repeated-zone orbit of a tight-binding band; orbit 'hops' at zone boundaries."""
    fig, ax = plt.subplots(figsize=(3.8, 2.8))
    ax.set_aspect('equal')
    cx, cy, R = 0.5, 0.5, 0.95
    # grid: 2 vertical + 2 horizontal zone boundaries
    for xv in (0.0, 1.0):
        ax.plot([xv, xv], [cy - 0.83, cy + 0.83], 'k-', lw=1.0)
    for yv in (0.0, 1.0):
        ax.plot([cx - 1.96, cx + 2.10], [yv, yv], 'k-', lw=1.0)

    def pt(th, r):
        return (cx + r * np.cos(np.radians(th)), cy + r * np.sin(np.radians(th)))

    def hook(ax, th, side):
        """Fishhook: sweeps from th (just short of the crossing) past it, curling in."""
        t = np.linspace(0, 1, 40)
        ths = th + side * (7.0 * t - 2.0)
        rs = R * (1 - 0.20 * t**1.6)
        pts = [pt(v, rr) for v, rr in zip(ths, rs)]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], 'k-', lw=1.3,
                solid_capstyle='round')

    def arc(th0, th1, hook0=True, hook1=True):
        ths = np.linspace(th0 + 2.0, th1 - 2.0, 120)
        pts = [pt(v, R) for v in ths]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], 'k-', lw=1.3)
        if hook0:
            hook(ax, th0, -1)
        if hook1:
            hook(ax, th1, +1)

    arcs = [(31.7, 58.3), (58.3, 121.7), (121.7, 148.3), (148.3, 211.7),
            (211.7, 238.3), (238.3, 301.7), (301.7, 328.3), (328.3, 391.7)]
    for th0, th1 in arcs:
        arc(th0, th1)
    # dashed 'hops' bridging the two lower-left junctions
    tip = lambda th, side: pt(th + side * 5.0, R * (1 - 0.20))
    p_w = tip(211.7, +1)     # end of W arc hook
    p_sw0 = tip(211.7, -1)   # start of SW arc hook
    p_sw1 = tip(238.3, +1)   # end of SW arc hook
    p_s0 = tip(238.3, -1)    # start of S arc hook
    ax.plot([p_w[0], p_sw0[0]], [p_w[1], p_sw0[1]], lw=1.0, linestyle=(0, (4, 3)), color='k')
    ax.plot([p_sw1[0], p_s0[0]], [p_sw1[1], p_s0[1]], lw=1.0, linestyle=(0, (4, 3)), color='k')
    # label
    ax.text(0.33, -0.74, 'Hops', ha='center', va='center')
    arrow(ax, (0.27, -0.695), (0.075, -0.475), ms=8, rad=0.35)
    ax.set_xlim(-1.55, 1.68)
    ax.set_ylim(-0.95, 1.43)
    ax.axis('off')
    savefig(fig, 25)


# ---------------------------------------------------------------- fig 26 ----
def bellf(x, c, h, w=0.10, p=1.8):
    return h / (1 + np.abs((x - c) / w)**2)**p


def fig_26():
    """Bloch wave b_n(k) = envelope x Wannier bells a_n(r-R_j)."""
    fig, ax = plt.subplots(figsize=(4.45, 1.5))
    sites = np.arange(1, 7)
    env = lambda x: 1.12 * np.cos(np.pi * (x - 0.9) / 5.4)
    xs = np.linspace(-0.35, 7.15, 2400)
    ax.plot([-0.35, 7.15], [0, 0], 'k-', lw=1.1, zorder=1)       # r axis
    ax.plot(xs, env(xs), 'k-', lw=1.2, zorder=2)                 # envelope
    for xi in sites:
        ax.plot([xi, xi], [-0.035, 0.035], 'k-', lw=0.9, zorder=3)
        ax.plot(xs, bellf(xs, xi, 1.04 * env(xi)), 'k-', lw=1.3, zorder=4)
    ax.text(7.29, 0.0, '$r$', ha='left', va='center')
    ax.text(-0.46, 1.05, '$b_{n}(k)$', ha='center', va='center')
    ax.text(0.68, -0.27, '$a_{n}(r-R_{j})$', ha='left', va='center')
    ax.set_xlim(-0.62, 7.50)
    ax.set_ylim(-1.38, 1.36)
    ax.axis('off')
    savefig(fig, 26)


# ---------------------------------------------------------------- fig 27 ----
def fig_27():
    """Wannier bells a_n, linear potential r, and stair-step R vs r."""
    fig, ax = plt.subplots(figsize=(4.0, 2.4))
    sites = np.arange(1, 6)
    xs = np.linspace(0.0, 6.0, 2200)
    # vertical lattice-site lines through everything (poking a bit above the bells)
    for xi in sites:
        ax.plot([xi, xi], [-2.84, 0.95], 'k-', lw=0.8, zorder=1)
    # a_n bells on their baseline
    ax.plot([0.21, 5.80], [0.0, 0.0], 'k-', lw=1.1, zorder=2)
    for xi in sites:
        ax.plot(xs, bellf(xs, xi, 0.81, w=0.10), 'k-', lw=1.3, zorder=3)
    ax.text(0.12, 0.0, '$a_{n}$', ha='right', va='center')
    # linear potential r
    ax.plot([0.21, 5.80], [0.39, -1.22], 'k-', lw=1.2, zorder=2)
    ax.text(0.12, 0.38, '$r$', ha='right', va='center')
    # stair-step R (solid treads, dashed risers)
    levels = [-1.45, -1.71, -1.97, -2.23, -2.49]
    for j, xi in enumerate(sites):
        ax.plot([xi - 0.37, xi + 0.37], [levels[j], levels[j]], 'k-', lw=1.3, zorder=3)
        if j < 4:
            ax.plot([xi + 0.37, sites[j + 1] - 0.37], [levels[j], levels[j + 1]],
                    lw=1.1, linestyle=(0, (4, 3)), color='k', zorder=2)
    ax.text(0.12, -1.45, '$R$', ha='right', va='center')
    ax.set_xlim(-0.50, 6.40)
    ax.set_ylim(-3.05, 1.05)
    ax.axis('off')
    savefig(fig, 27)


# ---------------------------------------------------------------- fig 28 ----
def fig_28():
    """X = r - R : sawtooth wave."""
    fig, ax = plt.subplots(figsize=(4.3, 0.68))
    x = np.linspace(-0.12, 5.42, 3000)
    u = (x - 0.55) % 1.0
    y = 0.38 * np.where(u < 0.88,
                        1 - 2 * sstep(u / 0.88),
                        -1 + 2 * sstep((u - 0.88) / 0.12))
    ax.plot([-0.30, 5.60], [0, 0], 'k-', lw=1.1)
    ax.plot(x, y, 'k-', lw=1.3)
    for xt in (1, 2, 3, 4, 5):
        ax.plot([xt, xt], [-0.05, 0.05], 'k-', lw=0.9)
    ax.text(5.73, 0.0, '$r$', ha='left', va='center')
    ax.text(-0.52, 0.06, '$X$', ha='right', va='center')
    ax.set_xlim(-0.85, 5.95)
    ax.set_ylim(-0.55, 0.55)
    ax.axis('off')
    savefig(fig, 28)


# ---------------------------------------------------------------- fig 29 ----
def fig_29():
    """Two electrons scattering out of the Fermi sphere: n,n' -> m,m'."""
    fig, ax = plt.subplots(figsize=(3.8, 2.4))
    ax.set_aspect('equal')
    circ = plt.Circle((0, 0), 1.0, fill=False, lw=1.3)
    ax.add_patch(circ)
    ax.text(0.04, -0.54, 'Fermi sphere', ha='center', va='center')
    # states inside (filled dots)
    ax.plot([-0.66], [0.40], 'ko', ms=5)
    ax.text(-0.60, 0.325, '$n$', ha='left', va='center')
    ax.plot([0.70], [0.0], 'ko', ms=5)
    ax.text(0.615, -0.045, "$n'$", ha='right', va='center')
    # final states outside (open circles)
    for (xc, yc) in ((-1.38, 0.75), (1.60, -0.09)):
        ax.add_patch(plt.Circle((xc, yc), 0.055, fc='white', ec='k', lw=1.2))
    ax.text(-1.475, 0.75, '$m$', ha='right', va='center')
    ax.text(1.70, -0.09, "$m'$", ha='left', va='center')
    # scattering arrows
    arrow(ax, (-0.615, 0.425), (-1.305, 0.715), ms=10)
    arrow(ax, (0.755, -0.015), (1.520, -0.083), ms=10)
    ax.set_xlim(-1.95, 2.05)
    ax.set_ylim(-1.42, 1.12)
    ax.axis('off')
    savefig(fig, 29)


# ---------------------------------------------------------------- fig 30 ----
def fig_30():
    """Spectral weight: delta-function spike at E_k plus hatched continuum."""
    fig, ax = plt.subplots(figsize=(4.2, 1.4))
    ax.plot([0, 0], [0, 0.59], 'k-', lw=1.1)
    ax.plot([0, 1.55], [0, 0], 'k-', lw=1.1)
    # delta spike
    xsp = 0.323
    ax.plot([xsp, xsp], [0, 0.545], 'k-', lw=1.3)
    ax.text(xsp, -0.052, '$E_{k}$', ha='center', va='top')
    ax.text(0.389, 0.592, r'$\delta$-function', ha='center', va='bottom')
    ax.text(0.389, 0.545, 'spike', ha='center', va='bottom')
    # axis labels
    ax.text(-0.03, 0.585, 'Coefficient', ha='right', va='center')
    ax.text(-0.03, 0.505, r'$|\langle n\,|\,c_{k}^{\dagger}\,|\,g\rangle|^{2}$',
            ha='right', va='center')
    ax.text(1.575, 0.0, '$E_{n}$', ha='left', va='center')
    # continuum onset + hatched area
    xc = 0.605
    x = np.linspace(xc, 1.44, 400)
    y = 0.40 * (1 - np.exp(-(x - xc) / 0.14))
    ax.fill_between(x, 0, y, facecolor='white', edgecolor='black', hatch='////', lw=0.0)
    ax.plot(x, y, 'k-', lw=1.3)
    ax.text(0.805, 0.362, 'Continuum', ha='center', va='bottom')
    ax.set_xlim(-0.75, 1.70)
    ax.set_ylim(-0.115, 0.70)
    ax.axis('off')
    savefig(fig, 30)


# ---------------------------------------------------------------- fig 31 ----
def fig_31():
    """Polarization spheres: outer radius R, inner (quasi-particle) radius dR."""
    fig, ax = plt.subplots(figsize=(3.0, 2.85))
    ax.set_aspect('equal')
    ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, lw=1.3))
    ax.add_patch(plt.Circle((0, 0), 0.34, fill=False, lw=1.3))
    # dR arrow to inner sphere
    a = np.radians(-30)
    arrow(ax, (0, 0), (0.34 * np.cos(a), 0.34 * np.sin(a)), ms=8)
    ax.text(0.0, 0.14, r'$\Delta R$', ha='center', va='bottom')
    # R arrow to outer sphere
    b = np.radians(-102)
    arrow(ax, (0, 0), (np.cos(b), np.sin(b)), ms=8)
    ax.text(0.03, -0.57, '$R$', ha='left', va='center')
    ax.set_xlim(-1.32, 1.38)
    ax.set_ylim(-1.35, 1.30)
    ax.axis('off')
    savefig(fig, 31)


if __name__ == '__main__':
    for f in (fig_23, fig_24, fig_25, fig_26, fig_27,
              fig_28, fig_29, fig_30, fig_31):
        f()
        print(f.__name__, 'done')
