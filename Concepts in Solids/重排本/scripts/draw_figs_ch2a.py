# -*- coding: utf-8 -*-
"""
Redraw Figures 1-14 of P. W. Anderson, "Concepts in Solids" (chapters 1-2 batch a).
Black-and-white textbook style, vector PDF output + PNG previews for self-check.
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import numpy as np

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
    'hatch.linewidth': 0.7,
})

BASE = r'E:\AI整理书籍\安德森\重排本'
OUT = os.path.join(BASE, 'figures')
PREV = os.path.join(OUT, 'preview')
os.makedirs(PREV, exist_ok=True)


def spline(xs, ys, n=260):
    """Natural cubic spline through the given points, densely sampled."""
    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    m = len(xs)
    if m == 2:
        t = np.linspace(0, 1, n)
        return xs[0] + t * (xs[1] - xs[0]), ys[0] + t * (ys[1] - ys[0])
    h = np.diff(xs)
    A = np.zeros((m, m))
    b = np.zeros(m)
    A[0, 0] = A[-1, -1] = 1
    for i in range(1, m - 1):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        b[i] = 3 * ((ys[i + 1] - ys[i]) / h[i] - (ys[i] - ys[i - 1]) / h[i - 1])
    c = np.linalg.solve(A, b)
    xq = np.linspace(xs[0], xs[-1], n)
    yq = np.empty(n)
    idx = np.clip(np.searchsorted(xs, xq) - 1, 0, m - 2)
    for k, i in enumerate(idx):
        dx = xq[k] - xs[i]
        bi = (ys[i + 1] - ys[i]) / h[i] - h[i] * (2 * c[i] + c[i + 1]) / 3
        di = (c[i + 1] - c[i]) / (3 * h[i])
        yq[k] = ys[i] + bi * dx + c[i] * dx ** 2 + di * dx ** 3
    return xq, yq


def curve(ax, pts, lw=1.4, **kw):
    x, y = spline([p[0] for p in pts], [p[1] for p in pts])
    ax.plot(x, y, lw=lw, color='k', solid_capstyle='round', **kw)
    return x, y


def arrow(ax, x0, y0, x1, y1, lw=1.2, both=False, ms=12):
    style = '<|-|>' if both else '-|>'
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


# ---------------------------------------------------------------- Figure 1
def fig_1():
    fig, ax = plt.subplots(figsize=(4.6, 1.55))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    # V = 0 line
    ax.plot([0.01, 0.855], [0.80, 0.80], color='k', lw=1.2)
    ax.text(0.868, 0.80, '$V(r)$', va='center', ha='left', fontsize=12)
    # proton positions a, b
    for x, lab in ((0.258, '$a$'), (0.631, '$b$')):
        ax.plot([x, x], [0.845, 0.02], color='k', lw=1.0)
        ax.text(x, 0.885, lab, ha='center', va='bottom', fontsize=12)
    # potential: two outer walls + central barrier arch (well bottoms run off
    # the bottom of the frame, as in the original)
    x = np.linspace(0.0, 0.242, 80)
    ax.plot(x, 0.735 * (1 - (x / 0.242) ** 1.7), color='k', lw=1.4)
    xa = np.linspace(0.283, 0.605, 120)
    ax.plot(xa, 0.725 * (1 - ((xa - 0.444) / 0.161) ** 2), color='k', lw=1.4)
    xr = np.linspace(0.662, 1.0, 80)
    ax.plot(xr, 0.735 * (1 - ((1 - xr) / 0.338) ** 1.7), color='k', lw=1.4)
    return fig, 'fig_1'


# ---------------------------------------------------------------- Figure 2
def fig_2():
    fig, ax = plt.subplots(figsize=(3.6, 2.5))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    # k axis with arrowheads on both ends
    arrow(ax, 0.02, 0.44, 0.98, 0.44, both=True)
    # bisecting planes at -K/2 and +K/2
    for x in (0.27, 0.80):
        ax.plot([x, x], [0.06, 0.88], color='k', lw=1.1, ls=(0, (5, 4)))
    # origin (reciprocal lattice point O)
    ax.plot([0.535], [0.44], marker='o', ms=5, mfc='white', mec='k', mew=1.1, ls='')
    # vector k ending on the left bisecting plane
    arrow(ax, 0.535, 0.44, 0.272, 0.665)
    ax.text(0.44, 0.60, r'$\vec{k}$', fontsize=13, ha='center')
    ax.text(0.105, 0.365, r'$-\vec{K}$', fontsize=13, ha='center')
    ax.text(0.878, 0.365, r'$\vec{K}$', fontsize=13, ha='center')
    return fig, 'fig_2'


# ---------------------------------------------------------------- Figure 3
def fig_3():
    fig, ax = plt.subplots(figsize=(3.8, 2.3))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    # axes
    ax.plot([0.02, 0.02], [0.03, 0.97], color='k', lw=1.2)
    ax.plot([0.02, 0.97], [0.03, 0.03], color='k', lw=1.2)
    ax.text(0.98, 0.075, r'$k_{\parallel}$', fontsize=13, ha='left')
    # Bragg plane
    ax.plot([0.46, 0.46], [0.03, 0.95], color='k', lw=0.9)
    # unperturbed free-electron line (thin, through the crossing point)
    ax.plot([0.128, 0.75], [0.168, 0.911], color='k', lw=0.9)
    # upper band: dashed free-line piece upper-left, solid flattened piece,
    # then merges with the free line to upper right
    up = [(0.20, 0.855), (0.26, 0.785), (0.33, 0.718), (0.40, 0.660),
          (0.46, 0.635), (0.53, 0.648), (0.60, 0.700), (0.66, 0.768),
          (0.72, 0.868), (0.735, 0.898)]
    x, y = curve(ax, up)
    n = int(np.searchsorted(x, 0.345))
    ax.lines[-1].remove()
    ax.plot(x[:n], y[:n], color='k', lw=1.6, ls=(0, (4, 3)))
    ax.plot(x[n - 1:], y[n - 1:], color='k', lw=1.6)
    # lower band: solid hugging the free line from lower left, flattening just
    # below the crossing, then dashed descending to lower right
    lo = [(0.155, 0.175), (0.24, 0.268), (0.33, 0.392), (0.40, 0.498),
          (0.46, 0.565), (0.53, 0.522), (0.60, 0.442), (0.66, 0.368),
          (0.73, 0.285)]
    x, y = curve(ax, lo)
    n = int(np.searchsorted(x, 0.50))
    ax.lines[-1].remove()
    ax.plot(x[:n], y[:n], color='k', lw=1.6)
    ax.plot(x[n - 1:], y[n - 1:], color='k', lw=1.6, ls=(0, (4, 3)))
    # crossing (E0) level: thin horizontal segments left and right
    ax.plot([0.345, 0.565], [0.60, 0.60], color='k', lw=0.8)
    # V_K gap arrows: thin shaft with small solid triangle heads
    for x, yb, yt in ((0.395, 0.600, 0.633), (0.53, 0.567, 0.600)):
        ax.plot([x, x], [yb + 0.003, yt - 0.003], color='k', lw=0.7)
        ax.plot([x], [yt + 0.004], marker='^', ms=3.5, color='k', ls='')
        ax.plot([x], [yb - 0.004], marker='v', ms=3.5, color='k', ls='')
    ax.text(0.368, 0.617, r'$V_K$', fontsize=12, ha='right', va='center')
    ax.text(0.556, 0.583, r'$V_K$', fontsize=12, ha='left', va='center')
    return fig, 'fig_3'


# ---------------------------------------------------------------- Figure 4
def fig_4():
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    # axes
    ax.plot([0.375, 0.375], [0.03, 0.95], color='k', lw=1.2)
    ax.plot([0.07, 0.95], [0.03, 0.03], color='k', lw=1.2)
    ax.text(0.35, 0.945, '$E$', fontsize=13, ha='right')
    ax.text(0.925, 0.062, '$k$', fontsize=13, ha='left')
    # zone-boundary verticals
    for xb, yt in ((0.205, 0.28), (0.545, 0.72), (0.715, 0.97)):
        ax.plot([xb, xb], [0.03, yt], color='k', lw=0.9)
    # the curve as a whole: one rising branch, its continuity broken at each
    # boundary; dashed pieces show the formal continuations past the boundary.
    # solid tips are pulled slightly apart (= the gap 2 V_K).
    ax.plot(*spline([0.205, 0.240, 0.290, 0.335, 0.375, 0.425, 0.475,
                     0.518, 0.533],
                    [0.280, 0.212, 0.140, 0.082, 0.032, 0.095, 0.190,
                     0.278, 0.300]), color='k', lw=1.5)
    ax.plot(*spline([0.528, 0.545, 0.562], [0.292, 0.318, 0.344]),
            color='k', lw=1.2, ls=(0, (4, 3)))
    ax.plot(*spline([0.558, 0.600, 0.650, 0.690, 0.703],
                    [0.362, 0.445, 0.532, 0.586, 0.600]), color='k', lw=1.5)
    ax.plot(*spline([0.698, 0.715, 0.732], [0.585, 0.622, 0.658]),
            color='k', lw=1.2, ls=(0, (4, 3)))
    ax.plot(*spline([0.728, 0.742, 0.755], [0.688, 0.800, 0.930]),
            color='k', lw=1.5)
    # label as printed in the original (with the minus sign)
    ax.text(0.775, 0.875, r'$-\frac{\hbar^2k^2}{2m}$',
            fontsize=14, ha='left', va='center')
    return fig, 'fig_4'


# ---------------------------------------------------------------- Figure 5
def fig_5():
    fig, ax = plt.subplots(figsize=(3.0, 4.8))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    G, L, y0 = 0.10, 0.97, 0.045
    # box: Gamma axis, L axis, bottom axis
    ax.plot([G, G], [y0, 0.975], color='k', lw=1.2)
    ax.plot([L, L], [y0, 0.955], color='k', lw=1.2)
    ax.plot([G, L], [y0, y0], color='k', lw=1.2)
    ax.text(G, 0.012, r'$\Gamma$', ha='center', va='top', fontsize=13)
    ax.text(L, 0.012, r'$L$', ha='center', va='top', fontsize=13)
    ax.text(0.535, 0.012, r'$|k|$', ha='center', va='top', fontsize=12)
    ax.text(0.055, 0.72, '$E$', ha='right', va='center', fontsize=13)
    ax.text(0.055, 0.50, '$A$', ha='right', va='center', fontsize=13)
    # bottom branch: free parabola Gamma -> L (lower meeting point)
    x = np.linspace(G, L, 200)
    ax.plot(x, y0 + 0.222 * ((x - G) / (L - G)) ** 1.6, color='k', lw=1.5)
    # upper V-joint on the Gamma axis
    ax.plot([G, 0.50], [0.875, 0.985], color='k', lw=1.4)
    curve(ax, [(G, 0.875), (0.35, 0.720), (0.60, 0.575), (0.80, 0.500),
               (L, 0.435)], lw=1.5)
    # from A: steep rise (ends mid-air), shallow rise (ends mid-air)
    curve(ax, [(G, 0.50), (0.20, 0.585), (0.32, 0.700), (0.45, 0.855),
               (0.51, 0.955)], lw=1.5)
    curve(ax, [(G, 0.50), (0.25, 0.565), (0.40, 0.635), (0.55, 0.710),
               (0.68, 0.790)], lw=1.5)
    # from A: gentle branch with a shallow dip -> L (upper meeting point)
    curve(ax, [(G, 0.50), (0.35, 0.442), (0.55, 0.428), (0.75, 0.424),
               (L, 0.415)], lw=1.5)
    # from A: steep flattening branch -> lower meeting point on L
    curve(ax, [(G, 0.50), (0.30, 0.415), (0.50, 0.345), (0.70, 0.295),
               (0.85, 0.262), (L, 0.238)], lw=1.5)
    # dashed degeneracy arcs hugging the axis just above/below A
    x1, y1 = spline([G, 0.16, 0.235], [0.548, 0.570, 0.608])
    ax.plot(x1, y1, color='k', lw=1.2, ls=(0, (4, 3)))
    x2, y2 = spline([G, 0.15, 0.215], [0.452, 0.428, 0.398])
    ax.plot(x2, y2, color='k', lw=1.2, ls=(0, (4, 3)))
    # dashed marks at the near-degenerate meeting points on the L axis
    for yy in (0.452, 0.398, 0.252):
        ax.plot([0.895, L], [yy, yy], color='k', lw=1.1, ls=(0, (4, 3)))
    return fig, 'fig_5'


# ---------------------------------------------------------------- Figure 6
def fig_6():
    fig = plt.figure(figsize=(4.8, 2.3))
    axg = fig.add_axes([0.005, 0.03, 0.42, 0.94])
    axg.set_xlim(-0.45, 2.45); axg.set_ylim(-0.45, 2.45)
    axg.set_aspect('equal'); axg.axis('off')
    # 2x2 grid
    axg.plot([0, 2, 2, 0, 0], [0, 0, 2, 2, 0], color='k', lw=1.1)
    axg.plot([1, 1], [0, 2], color='k', lw=1.1)
    axg.plot([0, 2], [1, 1], color='k', lw=1.1)
    r = 0.24
    for (cx, cy) in ((0, 0), (2, 0), (0, 2), (2, 2), (1, 1)):
        axg.add_patch(Circle((cx, cy), r, fc='white', ec='k', lw=1.3))
    for (cx, cy) in ((1, 0), (1, 2), (0, 1), (2, 1)):
        axg.add_patch(Rectangle((cx - 0.20, cy - 0.20), 0.40, 0.40,
                                fc='white', ec='k', lw=1.3))
    for (cx, cy) in ((0.5, 0.5), (1.5, 1.5)):
        axg.add_patch(Circle((cx, cy), r, fc='white', ec='k', lw=1.4,
                             hatch='////'))
    # legend: texts plus small aspect-equal marker insets
    axl = fig.add_axes([0.44, 0.03, 0.55, 0.94])
    axl.set_xlim(0, 10); axl.set_ylim(0, 1); axl.axis('off')
    rows = (0.80, 0.52, 0.24)
    for ry in rows:
        axl.text(0.9, ry, ('= 1st plane of f.c.c. lattice' if ry == rows[0]
                           else '= 2nd plane of f.c.c. lattice' if ry == rows[1]
                           else '= intermediate plane of\ndiamond lattice'),
                 va='center', fontsize=11)
    for ry, kind in zip(rows, ('o', 's', 'h')):
        axm = fig.add_axes([0.445, 0.03 + 0.94 * ry - 0.035, 0.05, 0.07])
        axm.set_xlim(-1, 1); axm.set_ylim(-1, 1)
        axm.set_aspect('equal'); axm.axis('off')
        if kind == 'o':
            axm.add_patch(Circle((0, 0), 0.60, fc='white', ec='k', lw=1.3))
        elif kind == 's':
            axm.add_patch(Rectangle((-0.52, -0.52), 1.04, 1.04, fc='white',
                                    ec='k', lw=1.3))
        else:
            axm.add_patch(Circle((0, 0), 0.60, fc='white', ec='k', lw=1.3,
                                 hatch='////'))
    return fig, 'fig_6'


# ---------------------------------------------------------------- Figure 7
def fig_7():
    fig, ax = plt.subplots(figsize=(3.6, 3.1))
    ax.set_xlim(-0.20, 1.62); ax.set_ylim(-0.14, 1.38)
    ax.set_aspect('equal'); ax.axis('off')
    dx, dy = 0.43, 0.21
    F = [(0, 0), (1, 0), (1, 1), (0, 1)]
    B = [(x + dx, y + dy) for (x, y) in F]
    # front and back faces
    ax.plot([p[0] for p in F] + [F[0][0]], [p[1] for p in F] + [F[0][1]],
            color='k', lw=1.2)
    ax.plot([p[0] for p in B] + [B[0][0]], [p[1] for p in B] + [B[0][1]],
            color='k', lw=1.2)
    for (x, y), (xb, yb) in zip(F, B):
        ax.plot([x, xb], [y, yb], color='k', lw=1.2)
    rr = 0.075
    open_pts = [(0, 0), (1, 1), (0 + dx, 1 + dy), (1 + dx, 0 + dy)]
    hatch_pts = [(0, 1), (1, 0), (0 + dx, 0 + dy), (1 + dx, 1 + dy),
                 (0.5 + dx / 2, 0.5 + dy / 2)]
    for (x, y) in open_pts:
        ax.add_patch(Circle((x, y), rr, fc='white', ec='k', lw=1.3, zorder=5))
    for (x, y) in hatch_pts:
        ax.add_patch(Circle((x, y), rr, fc='white', ec='k', lw=1.3,
                            hatch='////', zorder=5))
    return fig, 'fig_7'


# ---------------------------------------------------------------- Figure 8
def fig_8():
    fig, ax = plt.subplots(figsize=(4.2, 1.7))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    def X(px): return (px - 245) / 690 * 0.89 + 0.06
    def Y(py): return (965 - py) / 220 * 0.68 + 0.10
    ax.plot([0.06, 0.06], [0.10, Y(735)], color='k', lw=1.2)
    ax.plot([0.06, 0.95], [0.10, 0.10], color='k', lw=1.2)
    ax.text(0.048, Y(738), '$Z(r)$', ha='right', va='center', fontsize=12)
    ax.text(0.958, 0.10, '$r$', ha='left', va='center', fontsize=12)
    # level Z = 1 (dashed) with axis tick and label
    y1 = Y(860)
    ax.plot([0.06, 0.922], [y1, y1], color='k', lw=0.9, ls=(0, (5, 4)))
    ax.plot([0.052, 0.068], [y1, y1], color='k', lw=1.2)
    ax.text(0.044, y1, '1', ha='right', va='center', fontsize=11)
    # screened Z(r) curve approaching 1 from above
    curve(ax, [(X(245), Y(745)), (X(300), Y(792)), (X(360), Y(826)),
               (X(420), Y(848)), (X(480), Y(856)), (X(545), Y(858)),
               (X(700), Y(858)), (X(880), Y(856))], lw=1.4)
    # R_core, R_cell verticals
    for px in (545, 775):
        ax.plot([X(px), X(px)], [Y(858), 0.10], color='k', lw=0.9)
    ax.text(X(600), Y(938), r'$R_{\rm core}$', ha='left', va='center',
            fontsize=12)
    ax.text(X(822), Y(948), r'$R_{\rm cell}$', ha='left', va='center',
            fontsize=12)
    return fig, 'fig_8'


# ---------------------------------------------------------------- Figure 9
def fig_9():
    fig, ax = plt.subplots(figsize=(3.6, 4.7))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    def X(px): return (px - 245) / 715 * 0.96 + 0.03
    def Y(py): return (1180 - py) / 970 * 0.98
    # vertical axis spans both panels; horizontal r-axis between them
    ax.plot([X(245), X(245)], [Y(1155), Y(210)], color='k', lw=1.2)
    ax.plot([X(245), X(935)], [Y(695), Y(695)], color='k', lw=1.2)
    ax.text(X(932), Y(718), '$r$', ha='center', va='top', fontsize=12)
    ax.text(X(230), Y(465), r'$\mu_0(r)$', rotation=90, ha='center',
            va='center', fontsize=12)
    ax.text(X(230), Y(1000), '$V(r)$', rotation=90, ha='center',
            va='center', fontsize=12)
    # energy levels of V(r) (thin horizontal lines ending on the V curve)
    for py, px_end in ((1070, 295), (875, 412), (787, 559), (765, 641)):
        ax.plot([X(245), X(px_end)], [Y(py), Y(py)], color='k', lw=0.8)
    # turning-point verticals: from the V curve up to the mu0 curves
    for px, ptop in ((293, 472), (412, 505), (559, 560), (641, 645)):
        pyb = {293: 1070, 412: 875, 559: 787, 641: 765}[px]
        ax.plot([X(px), X(px)], [Y(ptop), Y(pyb)], color='k', lw=0.8)
    # R_core / R_cell: small ticks on the r axis with labels above
    for px, tx, ty, lab in ((520, 520, 662, r'$R_{\rm core}$'),
                            (721, 700, 674, r'$R_{\rm cell}$')):
        ax.plot([X(px), X(px)], [Y(700), Y(688)], color='k', lw=1.1)
        ax.text(X(tx), Y(ty), lab, ha='center', va='bottom', fontsize=12)
    # energy labels on the left
    ax.text(X(252), Y(748), '$E_f$', ha='left', va='bottom', fontsize=12)
    ax.text(X(300), Y(792), '$E_3=E_0$', ha='left', va='top', fontsize=12)
    ax.text(X(256), Y(868), '$E_2$', ha='left', va='bottom', fontsize=12)
    ax.text(X(310), Y(1070), '$E_1$', ha='left', va='center', fontsize=12)
    # turning-point labels below the r axis
    for px, plab in ((293, 330), (412, 450), (559, 592), (641, 700)):
        ax.text(X(plab), Y(724), r'$R_{\rm t}(E_%s)$' %
                {330: '1', 450: '2', 592: '3', 700: 'f'}[plab],
                ha='left', va='center', fontsize=9.5)
    # mu0(r) solutions for increasing energies
    curve(ax, [(X(248), Y(680)), (X(268), Y(560)), (X(292), Y(472)),
               (X(315), Y(350)), (X(332), Y(225))], lw=1.4)
    curve(ax, [(X(248), Y(688)), (X(320), Y(612)), (X(415), Y(500)),
               (X(500), Y(360)), (X(575), Y(225))], lw=1.4)
    curve(ax, [(X(248), Y(690)), (X(300), Y(640)), (X(360), Y(560)),
               (X(415), Y(505)), (X(500), Y(558)), (X(600), Y(595)),
               (X(680), Y(608)), (X(780), Y(588)), (X(870), Y(548)),
               (X(935), Y(515))], lw=1.4)
    curve(ax, [(X(248), Y(692)), (X(320), Y(650)), (X(380), Y(618)),
               (X(420), Y(602)), (X(500), Y(630)), (X(580), Y(660)),
               (X(660), Y(676)), (X(750), Y(682)), (X(850), Y(684)),
               (X(935), Y(683))], lw=1.4)
    # V(r): deep at the origin, rising toward zero like -2/r
    curve(ax, [(X(250), Y(1140)), (X(295), Y(1070)), (X(412), Y(875)),
               (X(559), Y(787)), (X(641), Y(765)), (X(750), Y(748)),
               (X(935), Y(733))], lw=1.4)
    return fig, 'fig_9'


# --------------------------------------------------------------- Figure 10
def fig_10():
    fig, ax = plt.subplots(figsize=(4.6, 2.5))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    def X(px): return (px - 90) / 1000 * 0.97 + 0.02
    def Y(py): return (1240 - py) / 550 * 0.95 + 0.02
    ax.plot([X(290), X(290)], [Y(700), Y(1230)], color='k', lw=1.2)
    ax.plot([X(95), X(1060)], [Y(945), Y(945)], color='k', lw=1.2)
    ax.text(X(1072), Y(945), '$E$', ha='left', va='center', fontsize=13)
    ax.text(0.004, Y(720), r'$\frac{1}{U}\,\frac{\mathrm{d}U}{\mathrm{d}r}'
            r'\vert_{r\,=\,R_{\rm core}}$',
            ha='left', va='top', fontsize=13)
    # three cot-like branches of the logarithmic derivative
    curve(ax, [(X(95), Y(790)), (X(180), Y(810)), (X(260), Y(845)),
               (X(340), Y(890)), (X(420), Y(960)), (X(470), Y(1040)),
               (X(510), Y(1130)), (X(530), Y(1195))], lw=1.4)
    curve(ax, [(X(550), Y(700)), (X(600), Y(790)), (X(650), Y(850)),
               (X(700), Y(880)), (X(745), Y(920)), (X(790), Y(1010)),
               (X(820), Y(1110)), (X(838), Y(1195))], lw=1.4)
    curve(ax, [(X(890), Y(700)), (X(930), Y(780)), (X(970), Y(880)),
               (X(990), Y(930)), (X(1010), Y(990)), (X(1030), Y(1045))],
          lw=1.4)
    # hypothetical spectral term values marked by x
    for px, py in ((462, 995), (512, 1105), (605, 838), (712, 895),
                   (940, 885), (1022, 1000)):
        ax.plot([X(px)], [Y(py)], marker='x', ms=7, mew=1.6, color='k',
                ls='')
    return fig, 'fig_10'


# --------------------------------------------------------------- Figure 11
def fig_11():
    fig, ax = plt.subplots(figsize=(4.3, 2.4))
    ax.set_xlim(0, 1); ax.set_ylim(0.36, 0.97); ax.axis('off')

    def X(px): return (px - 220) / 660 * 0.96 + 0.03
    def Y(py): return 0.55 - (py - 972) * 0.0012
    ax.plot([0.03, 0.03], [0.55, 0.935], color='k', lw=1.2)
    ax.plot([0.03, 0.97], [0.55, 0.55], color='k', lw=1.2)
    ax.text(0.014, 0.925, r'$\Psi$', ha='right', va='center', fontsize=13)
    ax.text(0.978, 0.528, '$r$', ha='left', va='center', fontsize=12)
    # E0: dips slightly then rises steeply
    curve(ax, [(X(430), Y(745)), (X(500), Y(763)), (X(560), Y(774)),
               (X(600), Y(775)), (X(660), Y(760)), (X(710), Y(733)),
               (X(760), Y(713)), (X(798), Y(696))], lw=1.4)
    ax.text(X(640), Y(790), r'$E_{\rm O}$', ha='left', va='top',
            fontsize=12)
    # EI: free-atom level, gently falling and flattening
    curve(ax, [(X(430), Y(850)), (X(520), Y(868)), (X(620), Y(892)),
               (X(720), Y(915)), (X(820), Y(930)), (X(860), Y(937))],
          lw=1.4)
    ax.text(X(735), Y(876), r'$E_{\rm I}$', ha='left', va='bottom',
            fontsize=12)
    # E top: nearly straight, plunging through the r axis
    curve(ax, [(X(415), Y(900)), (X(500), Y(950)), (X(585), Y(972)),
               (X(650), Y(1012)), (X(700), Y(1050))], lw=1.4)
    ax.text(X(755), Y(1022), 'E top', ha='left', va='center', fontsize=12)
    ax.text(X(440), Y(1005), r'$R_{\rm c}$', ha='center', va='center',
            fontsize=12)
    return fig, 'fig_11'


# --------------------------------------------------------------- Figure 12
def fig_12():
    fig, ax = plt.subplots(figsize=(4.6, 2.0))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    def X(px): return (px - 155) / 905 * 0.98 + 0.01
    def Y(py): return (925 - py) / 395 * 0.95 + 0.02
    ax.plot([X(185), X(185)], [Y(915), Y(545)], color='k', lw=1.2)
    ax.plot([X(185), X(1040)], [Y(915), Y(915)], color='k', lw=1.2)
    ax.text(X(1052), Y(900), '$k_F R$', ha='left', va='center', fontsize=13)
    ax.text(0.030, Y(575), r'$\frac{n}{2}-\rho$', ha='right', va='center',
            fontsize=13)
    yl = Y(712)
    ax.plot([X(185), 0.99], [yl, yl], color='k', lw=0.9)
    ax.text(0.055, Y(758), r'$\frac{n}{2}=ek_F^3/6\pi^2$', ha='left',
            va='top', fontsize=12)
    # exchange hole: sigmoid rise, overshoot, damped oscillation onto n/2
    curve(ax, [(X(185), Y(913)), (X(240), Y(900)), (X(300), Y(872)),
               (X(360), Y(840)), (X(420), Y(808)), (X(480), Y(780)),
               (X(540), Y(755)), (X(600), Y(728)), (X(650), Y(700)),
               (X(690), Y(672)), (X(730), Y(655)), (X(770), Y(650)),
               (X(810), Y(660)), (X(850), Y(685)), (X(890), Y(712)),
               (X(915), Y(722)), (X(935), Y(718))], lw=1.4)
    return fig, 'fig_12'


# --------------------------------------------------------------- Figure 13
def fig_13():
    fig, ax = plt.subplots(figsize=(4.4, 2.15))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    def X(s): return 0.037 + 0.46 * s
    def Y(v): return 0.046 + 0.2185 * v
    ax.plot([0.037, 0.037], [0.11, 0.965], color='k', lw=1.2)
    ax.plot([0.02, 0.99], [0.11, 0.11], color='k', lw=1.2)
    # value-4 and value-2 ticks
    for v, lab in ((4, '4'), (2, '2')):
        ax.plot([0.029, 0.045], [Y(v), Y(v)], color='k', lw=1.2)
        ax.text(0.021, Y(v), lab, ha='right', va='center', fontsize=12)
    # A(k) bracket function: 2 + (1-s^2)/s * ln|(1+s)/(1-s)|
    s = np.linspace(0.006, 2.07, 600)
    v = 2 + (1 - s ** 2) / s * np.log(np.abs((1 + s) / (1 - s)))
    ax.plot(X(s), Y(v), color='k', lw=1.5)
    # position marks
    for sv in (1.0, 2.0):
        ax.plot([X(sv), X(sv)], [0.11, 0.090], color='k', lw=1.1)
    ax.text(X(1.0), 0.045, '$k_F$', ha='center', va='top', fontsize=13)
    ax.text(X(2.0), 0.045, '$2k_F$', ha='center', va='top', fontsize=13)
    ax.text(X(0.75), 0.155, '$k$', ha='center', va='bottom', fontsize=13)
    return fig, 'fig_13'


# --------------------------------------------------------------- Figure 14
def fig_14():
    fig, ax = plt.subplots(figsize=(4.5, 1.7))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')

    def X(px): return (px - 155) / 750 * 0.96 + 0.03
    def Y(py): return (1330 - py) / 285 * 0.95 + 0.02
    ax.plot([X(165), X(165)], [Y(1315), Y(1055)], color='k', lw=1.2)
    ax.plot([X(165), X(890)], [Y(1315), Y(1315)], color='k', lw=1.2)
    ax.text(X(900), Y(1300), '$k$', ha='left', va='center', fontsize=13)
    ax.text(X(150), Y(1065), '$A(k)$', ha='right', va='center', fontsize=13)
    # k_F tick
    ax.plot([X(455), X(455)], [Y(1315), Y(1345)], color='k', lw=1.1)
    ax.text(X(455), Y(1355), '$k_F$', ha='center', va='top', fontsize=13)
    # Slater approximation level (thin horizontal line)
    ys = Y(1135)
    ax.plot([X(165), X(880)], [ys, ys], color='k', lw=0.9)
    ax.text(X(525), Y(1103), 'Slater approx.', ha='left', va='bottom',
            fontsize=12)
    ax.annotate('', xy=(X(532), Y(1150)), xytext=(X(532), Y(1118)),
                arrowprops=dict(arrowstyle='->', color='k', lw=0.9))
    # screened effective exchange A_eff(k): kink at k_F smoothed away
    curve(ax, [(X(165), Y(1075)), (X(250), Y(1085)), (X(340), Y(1110)),
               (X(420), Y(1150)), (X(500), Y(1200)), (X(580), Y(1245)),
               (X(660), Y(1275)), (X(740), Y(1292)), (X(795), Y(1300))],
          lw=1.5)
    ax.text(X(655), Y(1250), r'$A_{\rm eff}$', ha='left', va='bottom',
            fontsize=13)
    return fig, 'fig_14'


if __name__ == '__main__':
    for fn in (fig_1, fig_2, fig_3, fig_4, fig_5, fig_6, fig_7, fig_8,
               fig_9, fig_10, fig_11, fig_12, fig_13, fig_14):
        fig, name = fn()
        fig.savefig(os.path.join(OUT, name + '.pdf'),
                    bbox_inches='tight', pad_inches=0.03)
        fig.savefig(os.path.join(PREV, name + '.png'), dpi=150,
                    bbox_inches='tight', pad_inches=0.03)
        plt.close(fig)
        print('saved', name)
