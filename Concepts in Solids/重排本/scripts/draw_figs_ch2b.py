# -*- coding: utf-8 -*-
"""
Redraw Figures 15-22 + rapid/adiabatic (unnumbered) of Anderson,
"Concepts in Solids", ch. II, as black-and-white vector PDFs.
Style contract: 插图规范.md  (mono, Times/cm mathtext, hand-drawn axes).
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle
import numpy as np

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

HERE = os.path.dirname(os.path.abspath(__file__))
FIGD = os.path.normpath(os.path.join(HERE, '..', 'figures'))
PREV = os.path.join(FIGD, 'preview')
os.makedirs(PREV, exist_ok=True)


# ---------------------------------------------------------------- helpers
def spline(pts, n=28, closed=False):
    """Catmull-Rom cubic through 2D points; smooth hand-sketch curves."""
    P = np.asarray(pts, float)
    m = P.shape[0]
    if closed:
        Q = np.vstack([P[-1], P, P[0], P[1]])
    else:
        Q = np.vstack([P[0], P, P[-1]])
    T = np.zeros_like(Q)
    for i in range(1, len(Q) - 1):
        T[i] = (Q[i + 1] - Q[i - 1]) / 2.0
    if not closed:
        T[0] = Q[1] - Q[0]
        T[-1] = Q[-1] - Q[-2]
    segs = P if closed else P[:-1]
    xs, ys = [], []
    for i in range(len(segs)):
        P0, P1, M0, M1 = Q[i + 1], Q[i + 2], T[i + 1], T[i + 2]
        t = np.linspace(0, 1, n, endpoint=(i == len(segs) - 1))
        t2, t3 = t * t, t * t * t
        xs.append((2 * t3 - 3 * t2 + 1) * P0[0] + (t3 - 2 * t2 + t) * M0[0]
                  + (-2 * t3 + 3 * t2) * P1[0] + (t3 - t2) * M1[0])
        ys.append((2 * t3 - 3 * t2 + 1) * P0[1] + (t3 - 2 * t2 + t) * M0[1]
                  + (-2 * t3 + 3 * t2) * P1[1] + (t3 - t2) * M1[1])
    return np.concatenate(xs), np.concatenate(ys)


def arrow(ax, xy0, xy1, lw=1.0, ms=9, style='-|>', **kw):
    ax.add_patch(FancyArrowPatch(xy0, xy1, arrowstyle=style,
                                 mutation_scale=ms, lw=lw,
                                 color='k', shrinkA=0, shrinkB=0, **kw))


def new_ax(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    return fig, ax


def save(fig, key):
    fig.savefig(os.path.join(FIGD, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, 'fig_%s.png' % key), dpi=170,
                bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)
    print('fig_%s done' % key)


# ---------------------------------------------------------------- Figure 15
def fig_15():
    """Z_eff(r) for Si: cancellation of V by V_R  (Cohen-Heine)."""
    fig, ax = new_ax(3.6, 1.93)
    ax.set_xlim(-0.75, 3.75)
    ax.set_ylim(14.9, -1.9)                      # inverted: 14 at bottom

    # axes (plain, no arrowheads)
    ax.plot([0, 0], [0, 14.4], 'k-', lw=1.1)
    ax.plot([0, 3.62], [0, 0], 'k-', lw=1.1)
    for x in (1, 2, 3):
        ax.plot([x, x], [0, 0.13], 'k-', lw=0.9)
        ax.text(x, -0.42, '%d' % x, ha='center', va='bottom', fontsize=10)
    ax.text(3.68, -0.15, '$r$', ha='left', va='center')
    for z in (4, 8, 12, 14):
        ax.plot([-0.06, 0], [z, z], 'k-', lw=0.9)
        ax.text(-0.11, z, '%d' % z, ha='right', va='center', fontsize=10)
    ax.text(-0.62, 10.9, r'$Z_{\rm eff}$', ha='center', va='center', fontsize=11)

    # asymptote: dashed from axis to r~2.15, then solid merged line
    ax.plot([0.03, 2.15], [4, 4], 'k--', dashes=(5, 3), lw=0.9)
    ax.plot([2.15, 3.55], [4, 4], 'k-', lw=1.2)

    # bare ionic potential V
    V = [(0.048, 14.0), (0.06, 12.5), (0.09, 11.3), (0.15, 10.6), (0.25, 9.8),
         (0.40, 8.9), (0.55, 8.2), (0.75, 7.3), (1.0, 6.4), (1.25, 5.7),
         (1.5, 5.15), (1.75, 4.75), (2.0, 4.35), (2.15, 4.1)]
    xv, yv = spline(V)
    ax.plot(xv, yv, 'k-', lw=1.3)
    ax.text(0.80, 9.6, '$V$', ha='center', va='center', fontsize=11)

    # cancelled potential V + V_R (overshoot with double bump)
    VR = [(0.048, 14.0), (0.058, 9.0), (0.07, 3.0), (0.095, -0.85),
          (0.14, -1.10), (0.24, -1.14), (0.34, -0.85), (0.43, -0.47),
          (0.50, -0.65), (0.56, -1.0), (0.63, -0.7), (0.70, -0.05),
          (0.78, 0.5), (0.88, 0.98), (1.0, 1.45), (1.15, 2.05),
          (1.35, 2.75), (1.55, 3.25), (1.8, 3.65), (2.0, 3.92), (2.15, 4.0)]
    xr, yr = spline(VR)
    ax.plot(xr, yr, 'k-', lw=1.3)
    ax.text(1.2, 3.15, r'$V+V_{\rm R}$', ha='center', va='center', fontsize=10)
    save(fig, '15')


# ---------------------------------------------------------------- Figure 16
def fig_16():
    """Radial equation: centrifugal term keeps l>0 states out of the core."""
    fig, ax = new_ax(3.6, 1.38)
    ax.set_xlim(0.3, 10.2)
    ax.set_ylim(0, 3.78)

    ax.plot([1.2, 1.2], [2.6, 0.05], 'k-', lw=1.1)
    ax.plot([1.2, 9.5], [2.6, 2.6], 'k-', lw=1.1)
    ax.text(9.72, 2.62, '$r$', ha='left', va='center')

    # effective potential  V + L(L+1)/r^2  (dashed)
    eff = [(1.75, 3.5), (2.05, 2.65), (2.4, 2.05), (2.85, 1.55), (3.35, 1.2),
           (3.9, 1.05), (4.4, 1.03), (5.0, 1.15), (5.7, 1.40), (6.5, 1.78),
           (7.3, 2.3)]
    xe, ye = spline(eff)
    ax.plot(xe, ye, 'k--', dashes=(6, 4), lw=1.3)

    # bare V(r)
    Vr = [(4.5, 0.04), (4.9, 0.4), (5.35, 0.8), (5.8, 1.2), (6.25, 1.5),
          (6.7, 1.73), (7.2, 1.9), (7.7, 2.0), (8.15, 2.04)]
    xv, yv = spline(Vr)
    ax.plot(xv, yv, 'k-', lw=1.3)
    ax.text(5.68, 0.33, '$V(r)$', ha='center', va='center', fontsize=11)

    # bound-state level in the centrifugal pocket
    ax.plot([2.68, 5.3], [1.13, 1.13], 'k-', lw=0.8)
    ax.text(3.75, 1.4, 'Bound state?', ha='center', va='bottom', fontsize=10)
    arrow(ax, (2.55, 0.82), (2.55, 1.32), lw=0.8, ms=7)

    ax.text(1.35, 0.5, r'$V+\dfrac{L(L+1)}{r^2}$',
            ha='left', va='center', fontsize=10)
    save(fig, '16')


# ---------------------------------------------------------------- Figure 17
def fig_17():
    """Momentum-space atomic wave functions 1s, 2p, 3d."""
    fig, ax = new_ax(3.6, 1.9)
    ax.set_xlim(-0.42, 3.62)
    ax.set_ylim(-0.14, 1.1)

    ax.plot([0, 0], [0, 1.03], 'k-', lw=1.1)
    ax.plot([0, 3.30], [0, 0], 'k-', lw=1.1)
    ax.text(3.42, 0.0, '$k$', ha='left', va='center')
    ax.text(-0.09, 0.96, r'$\phi_k$', ha='right', va='center')
    ax.plot([1.71, 1.71], [0, -0.045], 'k-', lw=0.9)
    ax.text(1.71, -0.1, r'$\kappa$', ha='center', va='top', fontsize=10)

    f1s = [(0.02, 0.94), (0.27, 0.93), (0.50, 0.90), (0.75, 0.84),
           (0.94, 0.77), (1.13, 0.67), (1.30, 0.56), (1.47, 0.44),
           (1.66, 0.30), (1.88, 0.19), (2.17, 0.145), (2.48, 0.128),
           (2.77, 0.11)]
    f3d = [(0.01, 0.005), (0.12, 0.032), (0.27, 0.121), (0.43, 0.238),
           (0.59, 0.359), (0.75, 0.448), (0.91, 0.594), (1.00, 0.687),
           (1.09, 0.754), (1.19, 0.79), (1.28, 0.802), (1.38, 0.799),
           (1.47, 0.790), (1.57, 0.770), (1.66, 0.754), (1.70, 0.745),
           (1.79, 0.688), (1.88, 0.592), (2.01, 0.475), (2.17, 0.351),
           (2.32, 0.240), (2.45, 0.160)]
    f2p = [(0.01, 0.005), (0.27, 0.140), (0.59, 0.317), (0.91, 0.485),
           (1.13, 0.594), (1.28, 0.668), (1.36, 0.70), (1.50, 0.668),
           (1.63, 0.596), (1.70, 0.526), (1.76, 0.452), (1.82, 0.34),
           (1.88, 0.24), (1.97, 0.199), (2.07, 0.146), (2.17, 0.104)]
    for f in (f1s, f3d, f2p):
        x, y = spline(f)
        ax.plot(x, y, 'k-', lw=1.3)
    ax.text(0.61, 0.87, '$1s$', ha='center', va='center')
    ax.text(1.80, 0.733, '$3d$', ha='left', va='center')
    ax.text(1.73, 0.44, '$2p$', ha='left', va='center')
    save(fig, '17')


# ---------------------------------------------------------------- Figure 18
def fig_18():
    """Bloch sum in momentum space: spikes of b(p) at k+K under phi_1s."""
    fig, ax = new_ax(3.6, 1.7)
    ax.set_xlim(-0.03, 1.05)
    ax.set_ylim(-0.14, 1.1)

    ax.plot([-0.02, 1.0], [0, 0], 'k-', lw=1.1)

    bell = [(0.02, 0.17), (0.05, 0.26), (0.08, 0.36), (0.105, 0.473),
            (0.14, 0.585), (0.18, 0.69), (0.21, 0.77), (0.27, 0.89),
            (0.33, 0.965), (0.366, 1.0), (0.40, 0.975), (0.44, 0.855),
            (0.494, 0.635), (0.558, 0.50), (0.616, 0.392), (0.674, 0.305),
            (0.733, 0.243), (0.791, 0.208), (0.866, 0.181)]
    xb, yb = spline(bell)
    ax.plot(xb, yb, 'k-', lw=1.4)

    # spikes at k-K, k, k+K (solid) and dashed line at 0
    ax.plot([0.105, 0.105], [0, 0.66], 'k-', lw=0.9)
    ax.plot([0.494, 0.494], [0, 0.655], 'k-', lw=0.9)
    ax.plot([0.866, 0.866], [0, 0.20], 'k-', lw=0.9)
    ax.plot([0.384, 0.384], [0, 0.99], 'k--', dashes=(4, 3), lw=0.9)

    ax.text(-0.005, -0.07, r'$k-K$', ha='center', va='top', fontsize=10)
    ax.text(0.384, -0.07, r'$0$', ha='center', va='top', fontsize=10)
    ax.text(0.494, -0.07, r'$k$', ha='center', va='top', fontsize=10)
    ax.text(0.866, -0.07, r'$k+K$', ha='center', va='top', fontsize=10)
    ax.text(0.61, 0.89, r'$\phi_{1s}$', ha='left', va='center')

    ax.text(0.19, 0.35, r'$b(p)$', ha='center', va='center')
    arrow(ax, (0.235, 0.31), (0.112, 0.21), lw=0.6, ms=7)
    arrow(ax, (0.235, 0.32), (0.491, 0.05), lw=0.6, ms=7)
    arrow(ax, (0.235, 0.36), (0.862, 0.05), lw=0.6, ms=7)
    save(fig, '18')


# ---------------------------------------------------------------- Figure 19
def fig_19():
    """Band electron under constant force: E_n(k) (also x) and velocity."""
    fig, ax = new_ax(3.6, 3.25)
    ax.set_xlim(-0.55, 11.1)
    ax.set_ylim(-0.55, 9.9)
    ax.set_aspect('equal')

    xk = [1.57, 3.44, 5.31, 7.18, 9.05]          # -K/2 .. 3K/2
    lbl = [r'$-K/2$', r'$0$', r'$K/2$', r'$K$', r'$3K/2$']
    xx = np.linspace(xk[0], xk[4], 300)
    ph = np.pi * (xx - xk[0]) / 1.87

    # ---- upper panel: E_n (also x); max at -K/2, min at 0 and K
    ax.plot([0.5, 0.5], [6.9, 9.8], 'k-', lw=1.1)
    ax.plot([0.5, 9.65], [6.9, 6.9], 'k-', lw=1.1)
    ax.text(0.72, 9.57, r'$E_{\rm n}$', ha='left', va='center')
    ax.text(0.72, 9.17, r'also $x$', ha='left', va='center')
    ax.plot(xx, 8.25 + 0.75 * np.cos(ph), 'k-', lw=1.4)
    for x, top, lb in zip(xk, (9.05, 8.31, 9.21, 8.29, 9.21), lbl):
        ax.plot([x, x], [6.9, top], 'k-', lw=0.7)
        ax.text(x, 6.55, lb, ha='center', va='top', fontsize=10)
    ax.text(9.72, 7.15, r'$k=eEt/\hbar$', ha='left', va='center', fontsize=10)

    # ---- lower panel: velocity
    ax.plot([0.5, 0.5], [0.67, 2.89], 'k-', lw=1.1)
    ax.plot([0.5, 9.65], [0.67, 0.67], 'k-', lw=1.1)
    ax.plot(xx, 0.67 - 0.75 * np.sin(ph), 'k-', lw=1.4)
    for x in xk:
        ax.plot([x, x], [-0.25, 2.1], 'k-', lw=0.7)
    ax.text(1.05, 1.25, 'and of velocity:', ha='left', va='center',
            fontsize=10)
    ax.text(0.38, 0.67, r'$v_x=\dfrac{\partial E_n}{\partial k_x}$',
            ha='right', va='center', fontsize=10)
    save(fig, '19')


# ---------------------------------------------------------------- Figure 20
def fig_20():
    """Semiclassical band structure in an external potential (slope eE)."""
    fig, ax = new_ax(3.9, 1.67)
    ax.set_xlim(-0.15, 5.8)
    ax.set_ylim(-0.18, 2.4)
    ax.set_aspect('equal')

    x0 = [0.4, 1.5, 2.1, 3.2]                    # lines L1..L4 (x at y=0)
    top = 2.1
    for x in x0:
        ax.plot([x, x + top], [0, top], 'k-', lw=1.5)

    # hatching of the forbidden gap between L2 and L3
    for xc in np.arange(x0[1], x0[2] + top, 0.065):
        yb = max(0.0, xc - x0[2])
        yt = min(top, xc - x0[1])
        if yt > yb:
            ax.plot([xc, xc], [yb, yt], 'k-', lw=0.8)

    # fixed-energy line: solid, then dashed with arrowhead past L4
    y1 = 0.62
    xs1 = x0[3] + y1
    ax.plot([0.05, xs1 + 0.03], [y1, y1], 'k-', lw=1.1)
    ax.plot([xs1 + 0.03, xs1 + 0.62], [y1, y1], 'k--', dashes=(5, 3), lw=1.1)
    ax.add_patch(plt.Polygon([(xs1 + 0.67, y1), (xs1 + 0.49, y1 + 0.048),
                              (xs1 + 0.49, y1 - 0.048)],
                             closed=True, fc='k', ec='k'))

    # displaced level: dashed from L3 to L4
    y2 = 0.44
    ax.plot([x0[2] + y2, x0[3] + y2], [y2, y2], 'k--', dashes=(5, 3), lw=0.9)

    # W/eE horizontal and W vertical double arrows
    ye = 0.82
    arrow(ax, (x0[2] + ye, ye), (x0[3] + ye, ye), lw=1.0, ms=9,
          style='<|-|>')
    ax.text((x0[2] + x0[3]) / 2 + ye, ye + 0.13, r'$W/eE$',
            ha='center', va='bottom', fontsize=10)
    xw = 4.35
    arrow(ax, (xw, xw - x0[3]), (xw, xw - x0[2]), lw=1.0, ms=9,
          style='<|-|>')
    ax.text(xw + 0.1, xw - x0[2] + 0.05, r'$W$', ha='left', va='center',
            fontsize=10)

    # labels
    ax.text(1.32, 1.52, 'Slope $eE$', ha='center', va='center', fontsize=10)
    arrow(ax, (1.62, 1.38), (1.78, 1.20), lw=0.7, ms=7)
    ax.text(2.25, 1.32, 'Allowed', ha='center', va='center', rotation=45,
            fontsize=10)
    ax.text(x0[1] + 0.72 + 0.55, 1.05, 'Forbidden', ha='center', va='center',
            rotation=45, fontsize=10,
            bbox=dict(fc='white', ec='none', pad=1.0))
    ax.text(4.02, 1.6, 'Allowed', ha='center', va='center', rotation=45,
            fontsize=10)
    ax.text(4.88, 1.08, 'Forbidden', ha='center', va='center', rotation=45,
            fontsize=10)
    arrow(ax, (3.88, 0.1), (4.14, 0.1), lw=0.8, ms=7)
    ax.text(4.24, 0.1, '$x$', ha='left', va='center')
    save(fig, '20')


# ---------------------------------------------------------------- Figure 21
def fig_21():
    """p-n junction (degenerate): bands bent, constant E_F dashed."""
    fig, ax = new_ax(3.9, 1.49)
    ax.set_xlim(0, 8.75)
    ax.set_ylim(-0.2, 3.15)
    ax.set_aspect('equal')

    xa, xb = 0.32, 8.0                           # line span
    t = np.clip((np.linspace(xa, xb, 300) - 2.5) / 1.8, 0, 1)
    s = 0.5 - 0.5 * np.cos(np.pi * t)            # smooth S-bend

    def band(yl, yr):
        return yl + (yr - yl) * s

    for yl, yr in ((1.725, 2.925), (0.875, 2.075), (0.0, 1.2)):
        ax.plot(np.linspace(xa, xb, 300), band(yl, yr), 'k-', lw=1.4)
    ax.plot([xa, xb], [1.05, 1.05], 'k--', dashes=(5, 3), lw=1.0)
    ax.text(8.12, 1.02, r'$E_{\rm F}$', ha='left', va='center')

    ax.text(1.35, 2.55, 'p-n junction', ha='left', va='center', fontsize=10)
    ax.text(5.65, 2.48, 'Conduction\nband', ha='center', va='center',
            fontsize=10)
    ax.text(5.72, 1.62, 'Gap', ha='center', va='center', fontsize=10)
    ax.text(5.9, 0.28, 'Valence band', ha='center', va='center', fontsize=10)
    save(fig, '21')


# ---------------------------------------------------------------- Figure 22
def fig_22():
    """Constant-energy contours in k space; k follows contour about H."""
    fig, ax = new_ax(3.7, 1.85)
    ax.set_xlim(0.1, 7.3)
    ax.set_ylim(0.1, 3.75)
    ax.set_aspect('equal')

    outer = [(3.55, 3.475), (4.30, 3.43), (4.85, 3.13), (5.20, 2.60),
             (5.32, 2.00), (5.25, 1.45), (4.95, 1.00), (4.50, 0.83),
             (3.85, 0.85), (3.45, 0.85), (2.90, 0.70), (2.35, 0.60),
             (1.90, 0.50), (1.25, 0.375), (0.85, 0.55), (0.55, 1.05),
             (0.45, 1.60), (0.48, 2.10), (0.62, 2.50), (0.90, 2.83),
             (1.30, 2.95), (1.80, 2.85), (2.20, 2.93), (2.70, 3.23),
             (3.10, 3.40)]
    xo, yo = spline(outer, closed=True)
    ax.plot(xo, yo, 'k-', lw=1.4)

    inner = [(1.30, 1.88), (1.48, 2.03), (1.85, 2.15), (2.30, 2.21),
             (2.80, 2.25), (3.30, 2.29), (3.75, 2.33), (4.10, 2.34),
             (4.38, 2.23), (4.58, 2.05), (4.63, 1.88), (4.50, 1.68),
             (4.25, 1.55), (3.90, 1.50), (3.50, 1.53), (3.15, 1.58),
             (2.85, 1.63), (2.50, 1.58), (2.10, 1.58), (1.75, 1.65),
             (1.45, 1.75)]
    xi, yi = spline(inner, closed=True)
    ax.plot(xi, yi, 'k-', lw=1.4)

    # k vector: from inner contour down to outer contour
    arrow(ax, (2.80, 2.05), (2.47, 0.58), lw=0.9, ms=8)
    ax.text(2.80, 1.30, '$k$', ha='left', va='center')

    ax.text(4.28, 1.92, r'$E_2$', ha='center', va='center')
    ax.text(5.42, 1.30, r'$E_1$', ha='left', va='center')
    ax.text(6.85, 2.5, r'$H$', ha='center', va='center', fontsize=12)
    ax.add_patch(Circle((6.9, 2.05), 0.105, fill=False, lw=0.9))
    ax.plot([6.795, 7.005], [2.05, 2.05], 'k-', lw=0.8)
    ax.plot([6.9, 6.9], [1.945, 2.155], 'k-', lw=0.8)
    save(fig, '22')


# ---------------------------------------------------------------- rapid
def fig_rapid():
    """Rapid limit: electron stays on its diabatic branch through k-K."""
    fig, ax = new_ax(2.6, 2.5)
    ax.set_xlim(0, 5.0)
    ax.set_ylim(0, 4.8)
    ax.set_aspect('equal')

    bra = [(0.70, 4.10), (1.10, 3.40), (1.50, 2.80), (2.00, 2.10),
           (2.55, 1.45), (3.10, 0.90), (3.60, 0.50)]
    aro = [(0.45, 0.30), (1.30, 1.10), (1.70, 1.66), (2.00, 2.10),
           (2.30, 2.50), (2.70, 3.00), (3.30, 3.94)]
    for pts in (bra, aro):
        x, y = spline(pts)
        ax.plot(x, y, 'k-', lw=1.6)

    # arrowhead on the a branch (path arrow so it follows the curve)
    i0 = 40
    xa, ya = spline(aro)
    ax.add_patch(FancyArrowPatch(
        path=matplotlib.path.Path(np.column_stack([xa[i0:], ya[i0:]])),
        arrowstyle='-|>', mutation_scale=13,
        lw=1.6, color='k', shrinkA=0, shrinkB=0))

    # weak-coupling (avoided crossing) gaps: dashed cup above, cap below
    tu = np.linspace(0, 1, 60)
    xu = 1.45 + 1.25 * tu
    yu = 2.91 - 0.18 * np.sin(np.pi * tu)
    ax.plot(xu, yu, 'k--', dashes=(4, 3), lw=0.9)
    xd = 1.30 + 1.60 * tu
    yd = 1.11 + 0.25 * np.sin(np.pi * tu)
    ax.plot(xd, yd, 'k--', dashes=(4, 3), lw=0.9)

    ax.text(0.40, 4.42, '$b$', ha='center', va='center')
    ax.text(0.30, 1.12, '$a$', ha='center', va='center')
    ax.text(3.62, 2.15, 'Rapid', ha='left', va='center')
    save(fig, 'rapid')


# ---------------------------------------------------------------- adiabatic
def fig_adiabatic():
    """Adiabatic limit: electron follows the lower avoided-crossing branch."""
    fig, ax = new_ax(2.6, 2.5)
    ax.set_xlim(0, 6.4)
    ax.set_ylim(0.2, 6.2)
    ax.set_aspect('equal')

    # unperturbed crossing branches (thin)
    ax.plot([0.25, 4.40], [5.70, 0.65], 'k-', lw=0.9)
    ax.plot([0.30, 4.45], [0.65, 5.75], 'k-', lw=0.9)

    up = [(0.40, 5.70), (0.70, 5.42), (1.00, 5.10), (1.40, 4.60),
          (1.80, 4.20), (2.10, 4.02), (2.35, 3.97), (2.60, 4.02),
          (2.95, 4.22), (3.40, 4.62), (3.85, 5.10), (4.30, 5.58)]
    lo = [(0.40, 0.62), (0.75, 1.02), (1.10, 1.42), (1.50, 1.82),
          (1.85, 2.10), (2.10, 2.28), (2.35, 2.34), (2.60, 2.28),
          (2.95, 2.08), (3.35, 1.70), (3.80, 1.22), (4.30, 0.68)]
    for pts in (up, lo):
        x, y = spline(pts)
        ax.plot(x, y, 'k-', lw=1.6)

    # arrow on the lower branch (a -> b), following the curve
    xl, yl = spline(lo)
    i0 = int(np.argmax(xl > 1.50))
    i1 = int(np.argmax(xl > 2.05))
    ax.add_patch(FancyArrowPatch(
        path=matplotlib.path.Path(np.column_stack([xl[i0:i1 + 1],
                                                   yl[i0:i1 + 1]])),
        arrowstyle='-|>', mutation_scale=13,
        lw=1.6, color='k', shrinkA=0, shrinkB=0))

    ax.text(1.00, 0.92, '$a$', ha='center', va='center')
    ax.text(3.35, 0.92, '$b$', ha='center', va='center')
    ax.text(4.72, 3.85, 'Adiabatic', ha='left', va='center')
    save(fig, 'adiabatic')


# ---------------------------------------------------------------- main
if __name__ == '__main__':
    for f in (fig_15, fig_16, fig_17, fig_18, fig_19,
              fig_20, fig_21, fig_22, fig_rapid, fig_adiabatic):
        f()
