# -*- coding: utf-8 -*-
"""
Redraw all 17 figures of Chapter 3 of XG Wen "Quantum Field Theory of Many-Body
Systems" (Oxford 2004) as black-and-white vector figures.

fig_3_1  p091 (b76)  phonon-roton spectrum surface  E(k)
fig_3_2  p093 (b78)  thermal potential Omega(mu), second-order transition
fig_3_3  p094 (b79)  order parameter phi0 and superfluid transition
fig_3_4  p095 (b80)  switching minima -> kink in Omega0 (first order)
fig_3_5  p095 (b80)  phi0 -> -phi0 symmetry, continuous switching (2nd order)
fig_3_6  p102 (b87)  boson flow around (a) vortex ring (roton), (b) dipole
fig_3_7  p104 (b89)  gapless Nambu-Goldstone mode on the degenerate valley
fig_3_8  p118 (b103) S_eff vs l/l_n, four panels
fig_3_9  p119 (b104) phase diagram of 2D XY model (eta axis)
fig_3_10 p128 (b113) RG flow (a) eqn (3.5.9), (b) eqn (3.5.10)
fig_3_11 p133 (b118) RG fixed points: (a) A,B,C + separatrix DCD'; (b) fixed lines
fig_3_12 p136 (b121) energy levels of (1+1)-d interacting bosons
fig_3_13 p137 (b122) phase diagram: Mott insulator vs conductor
fig_3_14 p137 (b122) Mott insulator: bosons in periodic potential wells
fig_3_15 p149 (b134) condensate phase with twist n; vortex changes n -> n-1
fig_3_16 p156 (b141) two phi^4 vertices
fig_3_17 p157 (b142) three Feynman diagrams (connected/connected/disconnected)
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, Arc, FancyArrow

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

ROOT = r'E:\AI整理书籍\文小刚\重排本'
FIGD = os.path.join(ROOT, 'figures')
PREV = os.path.join(FIGD, 'preview')
os.makedirs(PREV, exist_ok=True)

BLACK = '0.0'


# ----------------------------------------------------------------- helpers --
def blank_ax(fig, rect=(0.02, 0.02, 0.96, 0.96)):
    ax = fig.add_axes(rect)
    ax.set_axis_off()
    return ax


def seg(ax, x0, y0, x1, y1, lw=1.0, ls='-', z=3, color=BLACK):
    ax.plot([x0, x1], [y0, y1], ls=ls, lw=lw, color=color, zorder=z,
            solid_capstyle='butt')


def polyline(ax, xs, ys, lw=1.2, ls='-', z=3, color=BLACK):
    ax.plot(xs, ys, lw=lw, ls=ls, color=color, zorder=z)


def head(ax, x, y, dx, dy, scale=9.0, lw=0.0, z=6, color=BLACK):
    """bare arrowhead at (x,y) pointing along (dx,dy)"""
    n = np.hypot(dx, dy)
    if n == 0:
        return
    dx, dy = dx / n, dy / n
    ax.annotate('', xy=(x + 0.05 * dx, y + 0.05 * dy), xytext=(x, y),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw,
                                mutation_scale=scale, shrinkA=0, shrinkB=0),
                zorder=z)


def curve_arrow(ax, pts, t, scale=9.0, back=0.035, z=6):
    """arrowhead on a polyline `pts` at fraction t, pointing along it"""
    n = len(pts)
    i = int(t * (n - 1))
    i = max(1, min(n - 2, i))
    p0 = np.array(pts[i - 1]); p1 = np.array(pts[i + 1])
    head(ax, pts[i][0] - back * (p1[0] - p0[0]),
         pts[i][1] - back * (p1[1] - p0[1]),
         p1[0] - p0[0], p1[1] - p0[1], scale=scale, z=z)


def bez2(p0, p1, p2, n=80):
    t = np.linspace(0, 1, n)
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    return np.column_stack([x, y])


def bez3(p0, p1, p2, p3, n=90):
    t = np.linspace(0, 1, n)
    x = ((1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] +
         3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0])
    y = ((1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] +
         3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1])
    return np.column_stack([x, y])


def chain(ax, curves, lw=1.0, ls='-', z=3, color=BLACK):
    for c in curves:
        polyline(ax, c[:, 0], c[:, 1], lw=lw, ls=ls, z=z, color=color)


def dot(ax, x, y, r=0.022, face=BLACK, edge=BLACK, lw=1.0, z=8):
    ax.add_patch(Circle((x, y), r, facecolor=face, edgecolor=edge,
                        lw=lw, zorder=z))


def block_arrow(ax, x, y, ln=0.55, ht=0.52, wd=0.24):
    """hollow block arrow '=>' like the book"""
    ax.add_patch(FancyArrow(x, y, ln, 0, width=wd, head_width=ht,
                            head_length=0.42 * ln, length_includes_head=True,
                            facecolor='white', edgecolor=BLACK, lw=1.1,
                            zorder=4))


# ------------------------------------------------------------------- 3.1 ---
def fig_3_1():
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    def Efun(r):
        E = 0.5 * r
        E = E + 0.38 * np.exp(-((r - 1.7) / 0.50) ** 2)
        E = E - 0.50 * np.exp(-((r - 2.3) / 0.45) ** 2)
        E = E + 0.48 * np.maximum(r - 2.5, 0.0) ** 1.7
        return E

    fig = plt.figure(figsize=(4.4, 3.6))
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0), projection='3d')
    ax.set_axis_off()
    ax.view_init(elev=19, azim=-60)
    ax.set_box_aspect((1.15, 1.0, 0.70))

    th = np.linspace(0, 2 * np.pi, 61)
    # inner phonon cone: radial fan only (no rings), like the book
    ri = np.linspace(0.001, 1.7, 25)
    R, T = np.meshgrid(ri, th)
    ax.plot_wireframe(R * np.cos(T), R * np.sin(T), Efun(R),
                      rstride=2, cstride=60, color=BLACK, lw=0.45)
    # outer bowl (roton dip + outer wall): rings + spokes
    ro = np.linspace(1.7, 3.0, 13)
    R, T = np.meshgrid(ro, th)
    ax.plot_wireframe(R * np.cos(T), R * np.sin(T), Efun(R),
                      rstride=2, cstride=2, color=BLACK, lw=0.45)

    # thick radial profile on the left front (phonon rise + roton dip)
    tp = np.deg2rad(199)
    xs = ri * np.cos(tp); ys = ri * np.sin(tp)
    ax.plot(xs, ys, Efun(ri), color=BLACK, lw=2.4)
    rr = np.linspace(1.7, 3.0, 30)
    ax.plot(rr * np.cos(tp), rr * np.sin(tp), Efun(rr), color=BLACK, lw=2.4)
    tp2 = np.deg2rad(166)
    ax.plot(rr * np.cos(tp2), rr * np.sin(tp2), Efun(rr), color=BLACK, lw=1.2)

    # vertical Energy axis
    ax.plot([0, 0], [0, 0], [0, 2.0], color=BLACK, lw=0.8)
    # critical-velocity tangent line (slope of the phonon part)
    tv = np.deg2rad(-33)
    rv = np.linspace(0, 2.75, 2)
    ax.plot(rv * np.cos(tv), rv * np.sin(tv), 0.5 * rv, color=BLACK, lw=0.9)
    # kx, ky axes
    for ang in (199, -19):
        a = np.deg2rad(ang)
        ax.plot([-1.75 * np.cos(a), 1.75 * np.cos(a)],
                [-1.75 * np.sin(a), 1.75 * np.sin(a)], [0, 0],
                color=BLACK, lw=0.7)

    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(0, 2.05)

    # NOTE: Axes3D.text2D is misplaced in mpl 3.11 -> use fig.text
    fig.text(0.525, 0.845, 'Energy', ha='center', va='center', fontsize=12)
    fig.text(0.255, 0.435, 'Roton', ha='center', va='center', fontsize=12)
    fig.text(0.425, 0.245, 'Phonon', ha='center', va='center', fontsize=12)
    fig.text(0.175, 0.155, r'$k_x$', ha='center', va='center', fontsize=12)
    fig.text(0.675, 0.235, r'$k_y$', ha='center', va='center', fontsize=12)
    fig.text(0.79, 0.435, 'Critical\nvelocity', ha='center', va='center',
             fontsize=11)
    # small arrow from the label to the tangent line (figure coords)
    from matplotlib.text import Annotation
    fig.add_artist(Annotation('', xy=(0.715, 0.46), xytext=(0.775, 0.435),
                              xycoords='figure fraction',
                              textcoords='figure fraction',
                              arrowprops=dict(arrowstyle='->', color=BLACK,
                                              lw=0.8, mutation_scale=10)))
    return fig


# ------------------------------------------------------------------- 3.2 ---
def fig_3_2():
    fig = plt.figure(figsize=(2.9, 2.0))
    ax = blank_ax(fig)
    ax.set_xlim(-1.75, 1.75); ax.set_ylim(-0.42, 1.5)
    ax.set_aspect('auto')
    # axes
    ax.annotate('', xy=(1.6, 0), xytext=(-1.55, 0),
                arrowprops=dict(arrowstyle='->', color=BLACK, lw=0.9,
                                mutation_scale=11))
    ax.annotate('', xy=(0, 1.32), xytext=(0, -0.12),
                arrowprops=dict(arrowstyle='->', color=BLACK, lw=0.9,
                                mutation_scale=11))
    # curve: 0 for mu<0, mu^2/2 for mu>0
    xm = np.linspace(-1.45, 0, 20)
    polyline(ax, xm, 0 * xm, lw=2.2)
    xp = np.linspace(0, 1.15, 60)
    polyline(ax, xp, 0.62 * xp ** 2, lw=2.2)
    ax.text(0.09, 1.24, r'$\Omega(\mu)$', fontsize=12, ha='left', va='center')
    ax.text(-0.08, -0.20, '0', fontsize=12, ha='center', va='center')
    ax.text(1.52, -0.20, r'$\mu$', fontsize=12, ha='center', va='center')
    ax.text(-1.42, 0.92, 'Transition point', fontsize=11, ha='left',
            va='center')
    ax.annotate('', xy=(-0.04, 0.035), xytext=(-0.42, 0.78),
                arrowprops=dict(arrowstyle='->', color=BLACK, lw=0.9,
                                mutation_scale=11))
    return fig


# ------------------------------------------------------------------- 3.3 ---
def fig_3_3():
    fig = plt.figure(figsize=(3.2, 2.2))
    ax = blank_ax(fig)
    ax.set_xlim(-2.1, 2.1); ax.set_ylim(-0.5, 1.55)
    # thin axes
    seg(ax, -1.85, 0, 1.95, 0, lw=0.9)
    seg(ax, 0, -0.18, 0, 1.42, lw=0.9)
    # order parameter: drawn as in the book (nonzero for mu<0)
    xm = np.linspace(-1.55, 0, 100)
    polyline(ax, xm, 0.88 * np.sqrt(-xm), lw=2.3)
    # zero branch: thick line on the axis for mu>0
    seg(ax, 0.0, 0, 1.7, 0, lw=2.6)
    ax.text(0.10, 1.32, 'Order', fontsize=12, ha='left', va='center')
    ax.text(0.10, 1.12, 'parameter', fontsize=12, ha='left', va='center')
    ax.text(0.10, 0.42, 'Phase', fontsize=12, ha='left', va='center')
    ax.text(0.10, 0.24, 'transition', fontsize=12, ha='left', va='center')
    ax.text(0.0, -0.24, '0', fontsize=12, ha='center', va='center')
    ax.text(1.82, -0.24, r'$\mu$', fontsize=12, ha='center', va='center')
    return fig


# ------------------------------------------------------------------- 3.4 ---
def fig_3_4():
    fig = plt.figure(figsize=(6.6, 2.0))
    ax = blank_ax(fig)
    ax.set_xlim(0, 10.4); ax.set_ylim(0, 2.3)

    def well(phi, tilt):
        return 0.42 * (phi ** 2 - 0.85 ** 2) ** 2 + tilt * phi

    # ---- panel (a): global minimum A (right) ----
    xc = 1.55
    seg(ax, xc, 0.12, xc, 2.12, lw=0.9)
    ax.text(xc + 0.07, 2.05, r'$\Omega_0$', fontsize=11, ha='left')
    phi = np.linspace(-1.45, 1.9, 200)
    y = 0.95 + 1.35 * well(phi, -0.24)
    polyline(ax, xc + 0.78 * phi, y, lw=1.7)
    iA = np.argmin(y)
    dot(ax, xc + 0.78 * phi[iA], y[iA], r=0.05)
    ax.text(xc + 0.78 * (-0.87), 0.30, '$B$', fontsize=12, ha='center')
    ax.text(xc + 0.78 * phi[iA], y[iA] - 0.18, '$A$', fontsize=12,
            ha='center', va='top')
    ax.text(xc - 1.35, 2.16, '(a)', fontsize=12, ha='center')
    block_arrow(ax, 3.15, 1.02)

    # ---- panel (b): global minimum B (left) ----
    xc = 5.35
    seg(ax, xc, 0.12, xc, 2.12, lw=0.9)
    ax.text(xc + 0.07, 2.05, r'$\Omega_0$', fontsize=11, ha='left')
    y = 0.95 + 1.35 * well(phi, 0.24)
    polyline(ax, xc + 0.78 * phi, y, lw=1.7)
    iB = np.argmin(y)
    dot(ax, xc + 0.78 * phi[iB], y[iB], r=0.05)
    ax.text(xc + 0.78 * phi[iB], y[iB] - 0.18, '$B$', fontsize=12,
            ha='center', va='top')
    ax.text(xc + 0.78 * 0.87, 0.30, '$A$', fontsize=12, ha='center')
    ax.text(xc - 1.35, 2.16, '(b)', fontsize=12, ha='center')
    block_arrow(ax, 6.95, 1.02)

    # ---- panel (c): two branches crossing -> kink ----
    xc, yc = 9.25, 1.15
    seg(ax, 7.85, 0.12, 7.85, 2.12, lw=0.9)
    ax.text(7.92, 2.05, r'$\Omega_0$', fontsize=11, ha='left')
    seg(ax, 8.0, 0.25, 10.3, 0.25, lw=0.9)
    ax.text(10.28, 0.08, r'$\mu$', fontsize=11, ha='center')
    d = np.linspace(-1.30, 1.18, 100)
    yA = yc + 0.50 * d + 0.154 * d ** 2          # rising branch
    yB = yc - 0.50 * d + 0.154 * d ** 2          # falling branch
    mA = d < 0; mB = d > 0
    # thin above crossing, thick below (the followed branch)
    polyline(ax, xc + d[mA], yA[mA], lw=2.3)
    polyline(ax, xc + d[~mA], yA[~mA], lw=0.9)
    polyline(ax, xc + d[mB], yB[mB], lw=2.3)
    polyline(ax, xc + d[~mB], yB[~mB], lw=0.9)
    ax.text(xc - 0.62, 0.52, '$A$', fontsize=12, ha='center')
    ax.text(xc + 0.62, 0.52, '$B$', fontsize=12, ha='center')
    ax.text(7.85 - 0.55, 2.16, '(c)', fontsize=12, ha='center')
    return fig


# ------------------------------------------------------------------- 3.5 ---
def fig_3_5():
    fig = plt.figure(figsize=(6.6, 2.0))
    ax = blank_ax(fig)
    ax.set_xlim(0, 9.6); ax.set_ylim(0, 2.3)
    phi = np.linspace(-1.25, 1.25, 200)

    # ---- (a) symmetric well, minimum on the axis ----
    xc = 1.45
    seg(ax, xc, 0.10, xc, 2.12, lw=0.9)
    ax.text(xc + 0.07, 2.05, r'$\Omega_0$', fontsize=11, ha='left')
    seg(ax, 0.15, 0.72, 2.75, 0.72, lw=0.9)
    ax.text(2.72, 0.55, r'$\phi_0$', fontsize=11, ha='center')
    y = 0.72 + 0.72 * phi ** 2
    polyline(ax, xc + 0.85 * phi, y, lw=1.7)
    dot(ax, xc, 0.72, r=0.05)
    ax.text(xc - 0.20, 0.87, '$A$', fontsize=12, ha='center')
    ax.text(xc - 1.05, 2.16, '(a)', fontsize=12, ha='center')
    block_arrow(ax, 3.0, 1.02)

    # ---- (b) flatter well, still symmetric ----
    xc = 4.75
    seg(ax, xc, 0.10, xc, 2.12, lw=0.9)
    ax.text(xc + 0.07, 2.05, r'$\Omega_0$', fontsize=11, ha='left')
    seg(ax, 3.45, 0.72, 6.05, 0.72, lw=0.9)
    ax.text(6.02, 0.55, r'$\phi_0$', fontsize=11, ha='center')
    y = 0.72 + 0.42 * phi ** 4
    polyline(ax, xc + 0.85 * phi, y, lw=1.7)
    dot(ax, xc, 0.72, r=0.05)
    ax.text(xc - 0.20, 0.87, '$A$', fontsize=12, ha='center')
    ax.text(xc - 1.05, 2.16, '(b)', fontsize=12, ha='center')
    block_arrow(ax, 6.3, 1.02)

    # ---- (c) double well below the axis; dot at B (right) only ----
    xc = 8.0
    seg(ax, xc, 0.10, xc, 2.12, lw=0.9)
    ax.text(xc + 0.07, 2.05, r'$\Omega_0$', fontsize=11, ha='left')
    seg(ax, 6.6, 0.72, 9.35, 0.72, lw=0.9)
    ax.text(9.32, 0.55, r'$\phi_0$', fontsize=11, ha='center')
    y = 0.72 + 1.15 * (0.9 * (phi ** 2 - 0.3844) ** 2 - 0.25)
    polyline(ax, xc + 0.85 * phi, y, lw=1.7)
    iB = np.where(phi > 0)[0][np.argmin(y[phi > 0])]
    iBp = np.where(phi < 0)[0][np.argmin(y[phi < 0])]
    dot(ax, xc + 0.85 * phi[iB], y[iB], r=0.05)
    ax.text(xc + 0.85 * phi[iB], y[iB] - 0.16, '$B$', fontsize=12,
            ha='center', va='top')
    ax.text(xc + 0.85 * phi[iBp], y[iBp] - 0.16, "$B'$",
            fontsize=12, ha='center', va='top')
    ax.text(xc - 0.13, 0.88, '$A$', fontsize=12, ha='center')
    ax.text(xc - 1.05, 2.16, '(c)', fontsize=12, ha='center')
    return fig


# ------------------------------------------------------------------- 3.6 ---
def fig_3_6():
    fig = plt.figure(figsize=(5.8, 2.7))
    ax = blank_ax(fig)
    ax.set_xlim(0, 6.0); ax.set_ylim(0, 2.6)
    ax.set_aspect('equal')

    def ellipse(cx, cy, w, h, lw=1.0):
        t = np.linspace(0, 2 * np.pi, 200)
        polyline(ax, cx + 0.5 * w * np.cos(t), cy + 0.5 * h * np.sin(t),
                 lw=lw)

    # ---------------- (a) roton = vortex ring seen edge-on --------------
    ax.text(0.18, 2.42, '(a)', fontsize=12, ha='center')
    cx, cy = 1.75, 1.3
    seg(ax, 0.35, cy, 3.15, cy, lw=0.8)
    # the ring core (stadium shape)
    for sy in (-1, 1):
        dot(ax, cx, cy + sy * 0.29, r=0.085, face='white', lw=1.1)
    seg(ax, cx - 0.085, cy - 0.29, cx - 0.085, cy + 0.29, lw=1.1)
    seg(ax, cx + 0.085, cy - 0.29, cx + 0.085, cy + 0.29, lw=1.1)
    # flow loops (small + big) around each core cross-section
    ellipse(cx, cy + 0.34, 0.50, 0.30)          # small top loop
    ellipse(cx, cy + 0.27, 1.85, 1.16)          # big top loop
    ellipse(cx, cy - 0.34, 0.50, 0.30)          # small bottom loop
    ellipse(cx, cy - 0.27, 1.85, 1.16)          # big bottom loop
    head(ax, cx, cy + 0.27 + 0.58, -1, 0)       # big top: left
    head(ax, cx, cy + 0.34 + 0.15, -1, 0)       # small top: left
    head(ax, cx, cy - 0.34 - 0.15, 1, 0)        # small bottom: right
    head(ax, cx, cy - 0.27 - 0.58, 1, 0)        # big bottom: right

    # ---------------- (b) dipole of phonon charge -----------------------
    ax.text(3.35, 2.42, '(b)', fontsize=12, ha='center')
    cx2, cy2 = 4.55, 1.3
    seg(ax, 3.15, cy2, 5.95, cy2, lw=0.8)
    r0 = 0.21
    dot(ax, cx2 - 0.21, cy2, r=r0, face='white', lw=1.2)   # drain (open)
    dot(ax, cx2 + 0.21, cy2, r=r0, face=BLACK, lw=1.2)     # source (filled)
    # inner arches (over / under the touching point)
    p = bez2((cx2 - 0.21, cy2 + r0), (cx2, cy2 + 0.72), (cx2 + 0.21, cy2 + r0))
    polyline(ax, p[:, 0], p[:, 1], lw=1.0)
    head(ax, cx2, cy2 + 0.475, -1, -0.12)
    p = bez2((cx2 - 0.21, cy2 - r0), (cx2, cy2 - 0.72), (cx2 + 0.21, cy2 - r0))
    polyline(ax, p[:, 0], p[:, 1], lw=1.0)
    head(ax, cx2, cy2 - 0.475, -1, 0.12)
    # outer loops
    p = bez3((cx2 - 0.21 - r0, cy2), (cx2 - 0.55, cy2 + 1.05),
             (cx2 + 0.55, cy2 + 1.05), (cx2 + 0.21 + r0, cy2))
    polyline(ax, p[:, 0], p[:, 1], lw=1.0)
    head(ax, cx2, cy2 + 0.79, -1, 0)
    p = bez3((cx2 - 0.21 - r0, cy2), (cx2 - 0.55, cy2 - 1.05),
             (cx2 + 0.55, cy2 - 1.05), (cx2 + 0.21 + r0, cy2))
    polyline(ax, p[:, 0], p[:, 1], lw=1.0)
    head(ax, cx2, cy2 - 0.79, -1, 0)
    return fig


# ------------------------------------------------------------------- 3.7 ---
def fig_3_7():
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    r0 = 0.95

    def V(r):
        return 0.55 * (r ** 2 - r0 ** 2) ** 2

    fig = plt.figure(figsize=(4.9, 3.9))
    ax = fig.add_axes((0.0, 0.0, 1.0, 1.0), projection='3d')
    ax.set_axis_off()
    ax.view_init(elev=20, azim=-55)
    ax.set_box_aspect((1.25, 1.0, 0.85))

    th = np.linspace(0, 2 * np.pi, 61)
    ri = np.linspace(0.001, r0, 21)          # inner region: fine mesh
    ro = np.linspace(r0, 1.55, 11)           # outer bowl: coarse mesh
    for rr, rstr, cstr in ((ri, 3, 1), (ro, 3, 2)):
        R, T = np.meshgrid(rr, th)
        X, Y = R * np.cos(T), R * np.sin(T)
        ax.plot_wireframe(X, Y, V(R), rstride=rstr, cstride=cstr,
                          color=BLACK, lw=0.4)

    # heavy circle of degenerate ground states
    tt = np.linspace(0, 2 * np.pi, 200)
    ax.plot(r0 * np.cos(tt), r0 * np.sin(tt), V(np.full_like(tt, r0)),
            color=BLACK, lw=2.2)

    # vertical V(phi) axis and two phi axes through the centre
    ax.plot([0, 0], [0, 0], [0, 1.42], color=BLACK, lw=0.8)
    ax.plot([-1.62, 1.62], [0, 0], [0, 0], color=BLACK, lw=0.6)
    ax.plot([0, 0], [-1.62, 1.62], [0, 0], color=BLACK, lw=0.6)

    # gapless-mode arrow along the valley circle (front right):
    # bold arc + V-shaped 3D arrowhead (robust; no 2D annotate needed)
    ta = np.deg2rad(np.linspace(-48, -10, 40))
    zv = V(np.full_like(ta, r0))
    ax.plot(r0 * np.cos(ta), r0 * np.sin(ta), zv, color=BLACK, lw=2.0)
    p_tip = np.array([r0 * np.cos(ta[0]), r0 * np.sin(ta[0]), zv[0]])
    p_prev = np.array([r0 * np.cos(ta[3]), r0 * np.sin(ta[3]), zv[3]])
    tangent = p_tip - p_prev
    tangent = tangent / np.linalg.norm(tangent)
    normal = np.array([p_tip[0], p_tip[1], 0.0])
    normal = normal / np.linalg.norm(normal)
    h, w = 0.16, 0.075
    q1 = p_tip - h * tangent + w * normal
    q2 = p_tip - h * tangent - w * normal
    for q in (q1, q2):
        ax.plot([p_tip[0], q[0]], [p_tip[1], q[1]], [p_tip[2], q[2]],
                color=BLACK, lw=2.0)

    ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.7, 1.7); ax.set_zlim(0, 1.45)
    fig.text(0.535, 0.875, r'$V(\phi)$', ha='center', va='center',
             fontsize=12)
    fig.text(0.775, 0.235, 'Gapless\nmode', ha='center', va='center',
             fontsize=11)
    return fig


# ------------------------------------------------------------------- 3.8 ---
def fig_3_8():
    fig = plt.figure(figsize=(5.3, 3.7))
    x = np.linspace(0, 1, 200)
    panels = [
        # rect, curve, ylim, sub-label
        ((0.09, 0.60, 0.37, 0.34), 2.2 * x ** 3 - 1.1 * x, (-0.55, 1.2),
         r'$S_c \gg 1, \quad h < 2$'),
        ((0.56, 0.60, 0.37, 0.34), -1.05 * (1 - np.exp(-1.8 * x)),
         (-1.2, 0.35), r'$S_c \ll -1, \quad h < 2$'),
        ((0.09, 0.13, 0.37, 0.34), 0.95 * (1 - np.exp(-2.6 * x)),
         (-0.2, 1.2), r'$S_c \gg 1, \quad h > 2$'),
        ((0.56, 0.13, 0.37, 0.34), 2.6 * x * np.exp(-5 * x) - 1.35 * x ** 2.6,
         (-1.55, 0.5), r'$S_c \ll -1, \quad h > 2$'),
    ]
    for rect, y, ylim, lab in panels:
        ax = fig.add_axes(rect)
        ax.set_axis_off()
        ax.set_xlim(0, 1.32); ax.set_ylim(*ylim)
        y0 = 0
        seg(ax, 0, ylim[0] * 0.96, 0, ylim[1] * 0.96, lw=0.9)   # vertical
        seg(ax, 0, y0, 1.3, y0, lw=0.9)                          # horizontal
        polyline(ax, x, y, lw=1.8)
        ax.text(0.015, ylim[1] * 0.97, r'$S_{\mathrm{eff}}$', fontsize=11,
                ha='left', va='bottom')
        ax.text(1.28, 0.05, r'$l/l_n$', fontsize=11, ha='center',
                va='bottom')
        ax.text(0.62, ylim[0] - 0.13 * (ylim[1] - ylim[0]), lab, fontsize=11,
                ha='center', va='top')
    return fig


# ------------------------------------------------------------------- 3.9 ---
def _phase_line(labels_left, labels_right):
    """shared by 3.9 and 3.13: horizontal arrow axis with a tick eta_c"""
    fig = plt.figure(figsize=(4.9, 1.0))
    ax = blank_ax(fig)
    ax.set_xlim(0, 4.9); ax.set_ylim(-0.62, 0.55)
    ax.annotate('', xy=(4.72, 0), xytext=(0.18, 0),
                arrowprops=dict(arrowstyle='-|>', color=BLACK, lw=1.2,
                                mutation_scale=16))
    xtick = 2.45
    seg(ax, xtick, -0.05, xtick, 0.13, lw=1.6)
    ax.text(xtick, 0.24, r'$\eta_c$', fontsize=12, ha='center', va='bottom')
    if labels_left:
        ax.text(1.25, -0.26, labels_left, fontsize=11, ha='center',
                va='center')
    if labels_right == 'algebraic':   # phrase wraps around the axis
        ax.text(3.42, 0.14, 'Algebraic', fontsize=11, ha='center',
                va='center')
        ax.text(3.42, -0.26, 'long-range order', fontsize=11, ha='center',
                va='center')
    else:
        ax.text(3.45, -0.26, labels_right, fontsize=11, ha='center',
                va='center')
    ax.text(4.68, -0.26, r'$\eta$', fontsize=12, ha='center', va='center')
    return fig


def fig_3_9():
    return _phase_line('Short-range order', 'algebraic')


# ------------------------------------------------------------------ 3.10 --
def fig_3_10():
    fig = plt.figure(figsize=(6.4, 3.0))

    # ============================ (a) ===================================
    ax = fig.add_axes((0.035, 0.10, 0.44, 0.86))
    ax.set_axis_off()
    ax.set_xlim(-0.12, 4.55); ax.set_ylim(-0.30, 1.30)
    seg(ax, 0.05, 0, 0.05, 1.18, lw=0.9)
    seg(ax, 0.05, 0, 4.35, 0, lw=0.9)
    ax.text(0.0, 1.20, r'$\bar g_\lambda$', fontsize=12, ha='right',
            va='bottom')
    ax.text(4.33, -0.14, r'$\bar\kappa_\lambda$', fontsize=12, ha='right',
            va='top')
    xc = 2.1
    # U trajectories (flow to the right at the bottom)
    for c in (0.55, 0.25):
        xx = np.linspace(0.05, 4.3, 150)
        yy = c + 0.098 * (xx - xc) ** 2
        yy = np.minimum(yy, 1.20)
        polyline(ax, xx, yy, lw=1.1)
        head(ax, xc, c + 0.02, 1, 0, scale=10)
    # dashed separatrix V converging at the cusp (n^2/8pi, 0)
    xl = np.linspace(0.05, xc, 80)
    polyline(ax, xl, 0.62 * ((xc - xl) / (xc - 0.05)) ** 1.7, lw=1.1,
             ls=(0, (5, 3)))
    xl2 = np.linspace(0.30, xc, 80)
    polyline(ax, xl2, 0.40 * ((xc - xl2) / (xc - 0.30)) ** 1.7, lw=1.1,
             ls=(0, (5, 3)))
    xr = np.linspace(xc, 4.3, 80)
    polyline(ax, xr, 0.56 * ((xr - xc) / (4.3 - xc)) ** 1.7, lw=1.1,
             ls=(0, (5, 3)))
    # solid branch of the separatrix hugging the right dashed from above
    polyline(ax, xr, 0.66 * ((xr - xc) / (4.3 - xc)) ** 1.7, lw=1.1)
    # small arrows on the dashed branches near the cusp
    head(ax, 1.72, 0.075, 0.9, -0.42, scale=8)
    head(ax, 2.48, 0.070, -0.9, -0.42, scale=8)
    # facing arrows marking the width ~ kappa - kappa_c
    head(ax, 0.60, 0.28, 1, 0, scale=8)
    head(ax, 0.95, 0.28, -1, 0, scale=8)
    seg(ax, 0.635, 0.25, 0.635, 0.31, lw=0.9)
    seg(ax, 0.915, 0.25, 0.915, 0.31, lw=0.9)
    ax.text(1.06, 0.50, r'$\sim\, \bar\kappa - \bar\kappa_c$', fontsize=11,
            ha='left', va='center')
    ax.annotate('', xy=(0.82, 0.335), xytext=(1.06, 0.46),
                arrowprops=dict(arrowstyle='->', color=BLACK, lw=0.8,
                                mutation_scale=9))
    # solid curves of region I (upper-left -> axis) with down-right arrows
    p = bez2((0.05, 0.33), (0.95, 0.24), (1.62, 0.0))
    polyline(ax, p[:, 0], p[:, 1], lw=1.1)
    curve_arrow(ax, p, 0.52, scale=10)
    p = bez2((0.05, 0.16), (1.05, 0.11), (1.92, 0.0))
    polyline(ax, p[:, 0], p[:, 1], lw=1.1)
    curve_arrow(ax, p, 0.5, scale=10)
    # mirror curves of region II with up-left arrows
    p = bez2((2.58, 0.0), (3.40, 0.18), (4.3, 0.38))
    polyline(ax, p[:, 0], p[:, 1], lw=1.1)
    curve_arrow(ax, p, 0.42, scale=10)
    p = bez2((2.28, 0.0), (3.25, 0.11), (4.3, 0.20))
    polyline(ax, p[:, 0], p[:, 1], lw=1.1)
    curve_arrow(ax, p, 0.38, scale=10)
    # region labels
    ax.text(0.42, 0.10, 'I', fontsize=14, ha='center', va='center')
    ax.text(3.95, 0.10, 'II', fontsize=14, ha='center', va='center')
    ax.text(2.80, 0.46, 'III', fontsize=14, ha='center', va='center')
    ax.text(xc, -0.14, r'$n^2/8\pi$', fontsize=12, ha='center', va='top')
    ax.text(0.12, 1.24, '(a)', fontsize=12, ha='left')

    # ============================ (b) ===================================
    ax = fig.add_axes((0.53, 0.10, 0.44, 0.86))
    ax.set_axis_off()
    ax.set_xlim(-0.12, 4.55); ax.set_ylim(-0.30, 1.30)
    seg(ax, 0.05, 0, 0.05, 1.18, lw=0.9)
    seg(ax, 0.05, 0, 4.35, 0, lw=0.9)
    ax.text(0.0, 1.20, r'$\bar g_\lambda$', fontsize=12, ha='right',
            va='bottom')
    ax.text(4.33, -0.14, r'$\bar\kappa_\lambda$', fontsize=12, ha='right',
            va='top')
    xc = 2.1
    seg(ax, xc, 0, xc, 1.05, lw=1.1, ls=(0, (5, 3)))   # critical line
    for xv in (0.55, 1.25, 1.75):
        seg(ax, xv, 0, xv, 1.02, lw=1.0)
        head(ax, xv, 0.50, 0, -1, scale=10)
    for xv in (2.48, 3.05, 3.70):
        seg(ax, xv, 0, xv, 1.02, lw=1.0)
        head(ax, xv, 0.50, 0, 1, scale=10)
    ax.text(xc, -0.14, r'$n^2/8\pi$', fontsize=12, ha='center', va='top')
    ax.text(0.12, 1.24, '(b)', fontsize=12, ha='left')
    return fig


# ------------------------------------------------------------------ 3.11 --
def _rg_panel(ax):
    ax.set_xlim(-0.10, 1.12); ax.set_ylim(-0.16, 1.10)
    ax.set_aspect('equal')
    seg(ax, 0.02, 0.0, 0.02, 1.0, lw=0.9)
    seg(ax, 0.02, 0.0, 1.05, 0.0, lw=0.9)
    ax.text(0.0, 1.02, r'$\tilde g_2$', fontsize=12, ha='right',
            va='bottom')
    ax.text(1.05, -0.05, r'$\tilde g_1$', fontsize=12, ha='right',
            va='top')


def fig_3_11():
    fig = plt.figure(figsize=(6.6, 3.0))

    # ============================ (a) ===================================
    ax = fig.add_axes((0.03, 0.04, 0.44, 0.92))
    ax.set_axis_off()
    _rg_panel(ax)
    B = (0.78, 0.60); A = (0.42, 0.05); C = (0.34, 0.42)

    # dashed separatrix D -> C -> D'  (flow converges to C along it)
    p1 = bez2((0.02, 0.74), (0.17, 0.62), C)
    p2 = bez3(C, (0.38, 0.50), (0.44, 0.53), (0.52, 0.50))
    p3 = bez3((0.52, 0.50), (0.70, 0.44), (0.88, 0.20), (0.97, 0.035))
    chain(ax, [p1, p2, p3], lw=1.4, ls=(0, (5, 3)))
    curve_arrow(ax, p1, 0.55, scale=10)
    curve_arrow(ax, p3, 0.45, scale=10)
    ax.text(0.005, 0.755, '$D$', fontsize=12, ha='right', va='bottom')
    ax.text(0.965, 0.02, "$D'$", fontsize=12, ha='left', va='top')

    # trajectories converging into B
    b_curves = [
        bez2((0.42, 1.0), (0.55, 0.85), (0.755, 0.615)),
        bez2((0.60, 1.0), (0.69, 0.84), (0.775, 0.625)),
        bez3((0.02, 0.95), (0.30, 0.88), (0.55, 0.79), (0.75, 0.635)),
        bez3((0.02, 0.86), (0.32, 0.80), (0.55, 0.72), (0.745, 0.625)),
        bez3((0.02, 0.79), (0.30, 0.72), (0.52, 0.66), (0.738, 0.615)),
    ]
    chain(ax, b_curves, lw=0.9)
    for i, c in enumerate(b_curves):
        curve_arrow(ax, c, 0.45 if i < 2 else 0.5, scale=9)
        curve_arrow(ax, c, 0.93, scale=8)
    # the horseshoe trajectory passing just above C and into B
    h1 = bez3((0.02, 0.70), (0.20, 0.65), (0.32, 0.57), (0.45, 0.53))
    h2 = bez3((0.45, 0.53), (0.58, 0.50), (0.68, 0.53), (0.755, 0.585))
    chain(ax, [h1, h2], lw=0.9)
    curve_arrow(ax, h1, 0.55, scale=9)
    curve_arrow(ax, h2, 0.85, scale=8)
    # from the right edge into B
    r1 = bez2((1.02, 0.74), (0.90, 0.70), (0.80, 0.625))
    r2 = bez3((1.02, 0.50), (0.88, 0.47), (0.80, 0.51), (0.792, 0.565))
    chain(ax, [r1, r2], lw=0.9)
    curve_arrow(ax, r1, 0.6, scale=9)
    curve_arrow(ax, r2, 0.75, scale=9)

    # trajectories converging into A
    a_curves = [
        bez3((0.02, 0.62), (0.16, 0.46), (0.24, 0.24), (0.355, 0.075)),
        bez3((0.02, 0.52), (0.19, 0.38), (0.30, 0.17), (0.40, 0.065)),
        bez3((0.02, 0.40), (0.21, 0.30), (0.34, 0.13), (0.41, 0.06)),
        bez3((0.02, 0.28), (0.23, 0.22), (0.36, 0.10), (0.415, 0.055)),
        bez3((0.02, 0.15), (0.21, 0.12), (0.34, 0.07), (0.41, 0.048)),
    ]
    chain(ax, a_curves, lw=0.9)
    for c in a_curves:
        curve_arrow(ax, c, 0.62, scale=9)
        curve_arrow(ax, c, 0.95, scale=8)
    a6 = bez2((0.30, 0.0), (0.36, 0.02), (0.415, 0.045))
    chain(ax, [a6], lw=0.9)
    curve_arrow(ax, a6, 0.5, scale=8)
    r3 = bez3((1.02, 0.12), (0.75, 0.14), (0.58, 0.12), (0.47, 0.065))
    r4 = bez3((1.02, 0.22), (0.78, 0.24), (0.62, 0.20), (0.49, 0.10))
    chain(ax, [r3, r4], lw=0.9)
    curve_arrow(ax, r3, 0.45, scale=9)
    curve_arrow(ax, r4, 0.45, scale=9)
    curve_arrow(ax, r3, 0.93, scale=8)
    curve_arrow(ax, r4, 0.93, scale=8)

    dot(ax, *B, r=0.024)
    dot(ax, *A, r=0.024)
    dot(ax, *C, r=0.028, face='white', lw=1.5)
    seg(ax, 0.325, 0.445, 0.355, 0.395, lw=1.2)   # tick through C
    ax.text(0.375, 0.425, '$C$', fontsize=13, ha='left', va='center')
    ax.text(0.755, 0.525, '$B$', fontsize=13, ha='right', va='top')
    ax.text(0.43, 0.022, '$A$', fontsize=13, ha='left', va='center')
    ax.text(0.02, 1.045, '(a)', fontsize=12, ha='left', va='bottom')

    # ============================ (b) ===================================
    ax = fig.add_axes((0.52, 0.04, 0.44, 0.92))
    ax.set_axis_off()
    _rg_panel(ax)
    B = (0.75, 0.55); Bp = (0.72, 0.17); C = (0.33, 0.42); A = (0.10, 0.03)

    # stable fixed line CA (thick) and unstable fixed line CA' (dash-dot)
    pCA = bez2(A, (0.155, 0.19), C)
    polyline(ax, pCA[:, 0], pCA[:, 1], lw=2.4)
    pCAp = bez3((0.35, 0.415), (0.55, 0.40), (0.75, 0.375), (0.93, 0.35))
    polyline(ax, pCAp[:, 0], pCAp[:, 1], lw=1.2, ls=(0, (6, 2, 1.5, 2)))
    ax.text(0.95, 0.345, "$A'$", fontsize=13, ha='left', va='center')

    # dashed separatrix D -> C, and C -> hump -> B, C -> lower -> D'
    d1 = bez2((0.02, 0.68), (0.17, 0.57), C)
    d2 = bez3(C, (0.38, 0.52), (0.48, 0.55), (0.58, 0.535))
    d3 = bez3((0.58, 0.535), (0.67, 0.525), (0.72, 0.545), (0.742, 0.552))
    chain(ax, [d1, d2, d3], lw=1.3, ls=(0, (5, 3)))
    curve_arrow(ax, d1, 0.55, scale=10)
    curve_arrow(ax, d2, 0.6, scale=9)
    e1 = bez3(C, (0.36, 0.30), (0.42, 0.18), (0.52, 0.12))
    e2 = bez3((0.52, 0.12), (0.65, 0.05), (0.80, 0.02), (0.96, 0.015))
    chain(ax, [e1, e2], lw=1.3, ls=(0, (5, 3)))
    curve_arrow(ax, e1, 0.55, scale=9)
    curve_arrow(ax, e2, 0.45, scale=9)
    ax.text(0.005, 0.695, '$D$', fontsize=12, ha='right', va='bottom')
    ax.text(0.975, 0.0, "$D'$", fontsize=12, ha='left', va='top')

    # trajectories into B
    bc = [
        bez2((0.40, 1.0), (0.55, 0.83), (0.742, 0.57)),
        bez2((0.58, 1.0), (0.68, 0.84), (0.755, 0.575)),
        bez3((0.02, 0.92), (0.32, 0.86), (0.55, 0.76), (0.735, 0.575)),
        bez3((0.02, 0.84), (0.33, 0.78), (0.55, 0.70), (0.728, 0.568)),
        bez3((0.02, 0.76), (0.32, 0.70), (0.52, 0.64), (0.718, 0.56)),
    ]
    chain(ax, bc, lw=0.9)
    for c in bc:
        curve_arrow(ax, c, 0.5, scale=9)
        curve_arrow(ax, c, 0.93, scale=8)
    # trajectories between the dashed arcs: up into B, down into B'
    m1 = bez3((0.56, 0.375), (0.62, 0.44), (0.66, 0.50), (0.715, 0.545))
    m2 = bez3((0.58, 0.36), (0.64, 0.28), (0.68, 0.22), (0.712, 0.185))
    chain(ax, [m1, m2], lw=0.9)
    curve_arrow(ax, m1, 0.75, scale=9)
    curve_arrow(ax, m2, 0.75, scale=9)
    # trajectories into B'
    bp = [
        bez2((0.50, 0.0), (0.60, 0.05), (0.705, 0.15)),
        bez2((0.78, 0.0), (0.75, 0.05), (0.725, 0.15)),
        bez2((1.02, 0.10), (0.88, 0.11), (0.75, 0.165)),
        bez2((1.02, 0.26), (0.88, 0.25), (0.742, 0.19)),
    ]
    chain(ax, bp, lw=0.9)
    for i, c in enumerate(bp):
        curve_arrow(ax, c, 0.75, scale=9)
    # trajectories flowing to the CA line / A
    ac = [
        [bez3((0.02, 0.62), (0.16, 0.52), (0.21, 0.38), (0.24, 0.28)),
         bez2((0.24, 0.28), (0.19, 0.15), (0.12, 0.055))],
        [bez3((0.02, 0.50), (0.17, 0.42), (0.20, 0.30), (0.215, 0.22)),
         bez2((0.215, 0.22), (0.17, 0.12), (0.115, 0.05))],
        [bez3((0.02, 0.38), (0.14, 0.30), (0.17, 0.20), (0.18, 0.16)),
         bez2((0.18, 0.16), (0.15, 0.09), (0.11, 0.045))],
        [bez2((0.02, 0.26), (0.10, 0.18), (0.145, 0.10)),
         bez2((0.145, 0.10), (0.12, 0.06), (0.105, 0.04))],
    ]
    for cchain in ac:
        chain(ax, cchain, lw=0.9)
        curve_arrow(ax, cchain[0], 0.55, scale=9)
        curve_arrow(ax, cchain[-1], 0.85, scale=8)

    dot(ax, *B, r=0.024)
    dot(ax, *Bp, r=0.024)
    dot(ax, *A, r=0.02)
    dot(ax, *C, r=0.028, face='white', lw=1.5)
    seg(ax, 0.315, 0.445, 0.345, 0.395, lw=1.2)
    ax.text(0.368, 0.415, '$C$', fontsize=13, ha='left', va='center')
    ax.text(0.775, 0.575, '$B$', fontsize=13, ha='left', va='center')
    ax.text(0.755, 0.125, "$B'$", fontsize=13, ha='left', va='center')
    ax.text(0.085, 0.02, '$A$', fontsize=13, ha='right', va='center')
    ax.text(0.02, 1.045, '(b)', fontsize=12, ha='left', va='bottom')
    return fig


# ------------------------------------------------------------------ 3.12 --
def fig_3_12():
    fig = plt.figure(figsize=(5.9, 1.9))

    # (a)
    ax = fig.add_axes((0.02, 0.02, 0.30, 0.96))
    ax.set_axis_off()
    ax.set_xlim(-1.85, 1.85); ax.set_ylim(-0.42, 1.5)
    ax.annotate('', xy=(1.75, 0), xytext=(-1.7, 0),
                arrowprops=dict(arrowstyle='-|>', color=BLACK, lw=0.9,
                                mutation_scale=12))
    ax.annotate('', xy=(0, 1.32), xytext=(0, -0.2),
                arrowprops=dict(arrowstyle='-|>', color=BLACK, lw=0.9,
                                mutation_scale=12))
    tri = np.array([(-1.15, 1.0), (1.15, 1.0), (0, 0)])
    ax.add_patch(plt.Polygon(tri, facecolor='0.75', edgecolor='0.2', lw=0.5))
    ax.text(0.10, 1.2, '$E$', fontsize=12, ha='left', va='center')
    ax.text(1.68, -0.24, '$k$', fontsize=12, ha='center', va='center')
    ax.text(-1.6, 1.32, '(a)', fontsize=12, ha='left')

    # (b)
    ax = fig.add_axes((0.34, 0.02, 0.64, 0.96))
    ax.set_axis_off()
    ax.set_xlim(-4.9, 4.9); ax.set_ylim(-0.42, 1.5)
    ax.annotate('', xy=(4.75, 0), xytext=(-4.6, 0),
                arrowprops=dict(arrowstyle='-|>', color=BLACK, lw=0.9,
                                mutation_scale=12))
    ax.annotate('', xy=(0, 1.32), xytext=(0, -0.2),
                arrowprops=dict(arrowstyle='-|>', color=BLACK, lw=0.9,
                                mutation_scale=12))
    for xi in (-2.3, 0.0, 2.3):
        tri = np.array([(xi - 1.05, 1.0), (xi + 1.05, 1.0), (xi, 0)])
        ax.add_patch(plt.Polygon(tri, facecolor='0.75', edgecolor='0.2',
                                 lw=0.5))
    ax.text(0.10, 1.2, '$E$', fontsize=12, ha='left', va='center')
    ax.text(-2.3, -0.26, r'$K_{-1}$', fontsize=12, ha='center', va='center')
    ax.text(2.3, -0.26, r'$K_{1}$', fontsize=12, ha='center', va='center')
    ax.text(4.66, -0.24, '$k$', fontsize=12, ha='center', va='center')
    ax.text(-4.7, 1.32, '(b)', fontsize=12, ha='left')
    return fig


# ------------------------------------------------------------------ 3.13 --
def fig_3_13():
    return _phase_line('Mott insulator', 'Conductor')


# ------------------------------------------------------------------ 3.14 --
def fig_3_14():
    fig = plt.figure(figsize=(5.3, 1.35))
    ax = blank_ax(fig)
    ax.set_xlim(-0.05, 6.45); ax.set_ylim(-1.02, 0.32)
    ax.set_aspect('equal')
    P = 1.05
    x = np.linspace(-0.02, 6.35, 500)
    y = -0.42 * (1 + np.cos(2 * np.pi * x / P))
    polyline(ax, x, y, lw=1.5)
    yb = -0.84
    wells = np.array([0.525 + k * P for k in range(6)])
    for k, xw in enumerate(wells):
        if k == 2:      # empty well (grey dot)
            dot(ax, xw, yb + 0.10, r=0.093, face='0.55', edge='0.3', lw=0.6)
        elif k == 3:    # doubly occupied well
            dot(ax, xw, yb + 0.17, r=0.098)
            dot(ax, xw, yb + 0.41, r=0.098)
        else:
            dot(ax, xw, yb + 0.10, r=0.093)
    # hopping arrow: boson moves from the empty well to the doubly occupied one
    ax.annotate('', xy=(wells[3] - 0.03, yb + 0.55),
                xytext=(wells[2] + 0.10, yb + 0.50),
                arrowprops=dict(arrowstyle='->', color=BLACK, lw=1.0,
                                mutation_scale=11,
                                connectionstyle='arc3,rad=-0.35'))
    return fig


# ------------------------------------------------------------------ 3.15 --
def fig_3_15():
    fig = plt.figure(figsize=(6.2, 3.3))
    ax = blank_ax(fig)
    ax.set_xlim(0, 6.2); ax.set_ylim(0, 3.3)
    ax.set_aspect('equal')

    def annulus(cx, cy, vortex):
        Ro, Ri = 1.22, 0.55
        th = np.deg2rad(52)
        ax.add_patch(Circle((cx, cy), Ro, facecolor='0.85', edgecolor=BLACK,
                            lw=0.9, zorder=1))
        ax.add_patch(Circle((cx, cy), Ri, facecolor='white', edgecolor=BLACK,
                            lw=0.9, zorder=2))
        # dashed reference lines
        polyline(ax, [cx, cx + 1.45], [cy, cy], lw=1.0, ls=(0, (5, 3)), z=3)
        polyline(ax, [cx, cx + 1.42 * np.cos(th)],
                 [cy, cy + 1.42 * np.sin(th)], lw=1.0, ls=(0, (5, 3)), z=3)
        # arrowheads on the radial cut, at both circle crossings
        for rad in (Ri, Ro):
            x0, y0 = cx + (rad - 0.055) * np.cos(th), cy + (rad - 0.055) * np.sin(th)
            x1, y1 = cx + (rad + 0.055) * np.cos(th), cy + (rad + 0.055) * np.sin(th)
            ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                        arrowprops=dict(arrowstyle='-|>', color=BLACK,
                                        lw=0.001, mutation_scale=13,
                                        shrinkA=0, shrinkB=0), zorder=6)
        # theta arc
        ax.add_patch(Arc((cx, cy), 0.62, 0.62, theta1=0, theta2=52,
                         lw=0.9, zorder=4))
        th2 = np.deg2rad(26)
        ax.text(cx + 0.42 * np.cos(th2), cy + 0.42 * np.sin(th2),
                r'$\theta$', fontsize=13, ha='center', va='center', zorder=5)
        # phase labels with curved arrows
        ax.text(cx - 0.75, cy + 1.02,
                (r'$\phi = \mathrm{e}^{\mathrm{i}\theta n}$' if not vortex
                 else r'$\phi = \mathrm{e}^{\mathrm{i}\theta(n-1)}$'),
                fontsize=12, ha='center', va='center', zorder=5)
        ax.annotate('', xy=(cx + 0.52 * np.cos(np.deg2rad(148)),
                            cy + 0.52 * np.sin(np.deg2rad(148))),
                    xytext=(cx - 0.70, cy + 0.84),
                    arrowprops=dict(arrowstyle='-|>', color=BLACK, lw=1.0,
                                    mutation_scale=12,
                                    connectionstyle='arc3,rad=0.40'),
                    zorder=6)
        ax.text(cx + 0.98, cy + 1.00,
                r'$\phi = \mathrm{e}^{\mathrm{i}\theta n}$',
                fontsize=12, ha='left', va='center', zorder=5)
        ax.annotate('', xy=(cx + 1.06 * np.cos(th), cy + 1.06 * np.sin(th)),
                    xytext=(cx + 1.05, cy + 0.82),
                    arrowprops=dict(arrowstyle='-|>', color=BLACK, lw=1.0,
                                    mutation_scale=12,
                                    connectionstyle='arc3,rad=0.35'),
                    zorder=6)
        if vortex:
            rv = 0.88
            vx, vy = cx + rv * np.cos(th), cy + rv * np.sin(th)
            dot(ax, vx, vy, r=0.052)
            dot(ax, vx, vy, r=0.135, face='white', lw=1.1, z=7)
            ax.annotate('', xy=(vx + 0.135 * np.cos(np.deg2rad(128)),
                                vy + 0.135 * np.sin(np.deg2rad(128))),
                        xytext=(vx + 0.135 * np.cos(np.deg2rad(62)),
                                vy + 0.135 * np.sin(np.deg2rad(62))),
                        arrowprops=dict(arrowstyle='-|>', color=BLACK, lw=1.0,
                                        mutation_scale=11,
                                        connectionstyle='arc3,rad=0.25'),
                        zorder=8)
            ax.text(vx + 0.10, vy - 0.22, 'Vortex', fontsize=12, ha='left',
                    va='top', zorder=8)

    ax.text(0.30, 3.02, '(a)', fontsize=12, ha='center')
    ax.text(3.30, 3.02, '(b)', fontsize=12, ha='center')
    annulus(1.62, 1.60, vortex=False)
    annulus(4.62, 1.60, vortex=True)
    return fig


# ------------------------------------------------------------------ 3.16 --
def fig_3_16():
    fig = plt.figure(figsize=(2.7, 1.15))
    ax = blank_ax(fig)
    ax.set_xlim(0, 2.7); ax.set_ylim(0, 1.15)
    ax.set_aspect('equal')
    for cx, lab in ((0.75, '1'), (2.0, '2')):
        L = 0.34
        for ang in (45, 135, 225, 315):
            a = np.deg2rad(ang)
            seg(ax, cx, 0.58, cx + L * np.cos(a), 0.58 + L * np.sin(a),
                lw=1.4)
        dot(ax, cx, 0.58, r=0.075)
        ax.text(cx + 0.11, 0.55, lab, fontsize=12, ha='left', va='center')
    return fig


# ------------------------------------------------------------------ 3.17 --
def fig_3_17():
    fig = plt.figure(figsize=(6.6, 1.9))
    ax = blank_ax(fig)
    ax.set_xlim(0, 13.2); ax.set_ylim(0, 2.0)
    ax.set_aspect('equal')
    y0 = 0.72

    def vertex(x, lab_l=None, lab_r=None):
        dot(ax, x, y0, r=0.085)
        if lab_l:
            ax.text(x - 0.14, y0 - 0.02, lab_l, fontsize=12, ha='right',
                    va='center')
        if lab_r:
            ax.text(x + 0.14, y0 - 0.02, lab_r, fontsize=12, ha='left',
                    va='center')

    # ---- (a) four lines between two vertices ----
    ax.text(0.15, 1.80, '(a)', fontsize=12, ha='left')
    v1, v2 = (0.95, y0), (2.65, y0)
    for h in (0.30, 0.72, -0.30, -0.72):
        p = bez2(v1, ((v1[0] + v2[0]) / 2, y0 + h), v2)
        polyline(ax, p[:, 0], p[:, 1], lw=1.1)
    vertex(v1[0], lab_r='1')
    vertex(v2[0], lab_l='2')
    ax.text(3.35, 1.42, 'Vertex', fontsize=11, ha='left', va='center')
    ax.annotate('', xy=(2.78, 0.86), xytext=(3.30, 1.34),
                arrowprops=dict(arrowstyle='->', color=BLACK, lw=1.0,
                                mutation_scale=11))

    # ---- (b) tadpole + big circle + tadpole ----
    ax.text(4.15, 1.80, '(b)', fontsize=12, ha='left')
    v1, v2 = (4.95, y0), (7.15, y0)
    for cx in (4.40, 7.70):
        t = np.linspace(0, 2 * np.pi, 200)
        polyline(ax, cx + 0.55 * np.cos(t), y0 + 0.62 * np.sin(t), lw=1.1)
    t = np.linspace(0, 2 * np.pi, 200)
    polyline(ax, 6.05 + 1.10 * np.cos(t), y0 + 1.00 * np.sin(t), lw=1.1)
    vertex(v1[0], lab_r='1')
    vertex(v2[0], lab_l='2')
    ax.text(8.30, 1.30, 'Propagator', fontsize=11, ha='left', va='center')
    ax.annotate('', xy=(7.12, 1.04), xytext=(8.25, 1.22),
                arrowprops=dict(arrowstyle='->', color=BLACK, lw=1.0,
                                mutation_scale=11))

    # ---- (c) two disconnected blobs, each a figure-eight ----
    ax.text(8.30, 1.80, '(c)', fontsize=12, ha='left')
    for vxx in (9.35, 11.55):
        for cx in (vxx - 0.55, vxx + 0.55):
            t = np.linspace(0, 2 * np.pi, 200)
            polyline(ax, cx + 0.55 * np.cos(t), y0 + 0.62 * np.sin(t),
                     lw=1.1)
        vertex(vxx, lab_r='1' if vxx < 10.5 else '2')
    return fig


# ------------------------------------------------------------------- run --
ALL = {
    '3.1': fig_3_1, '3.2': fig_3_2, '3.3': fig_3_3, '3.4': fig_3_4,
    '3.5': fig_3_5, '3.6': fig_3_6, '3.7': fig_3_7, '3.8': fig_3_8,
    '3.9': fig_3_9, '3.10': fig_3_10, '3.11': fig_3_11, '3.12': fig_3_12,
    '3.13': fig_3_13, '3.14': fig_3_14, '3.15': fig_3_15, '3.16': fig_3_16,
    '3.17': fig_3_17,
}

if __name__ == '__main__':
    import sys
    only = sys.argv[1:] or list(ALL)
    for key in only:
        fig = ALL[key]()
        name = f'fig_{key}'            # key keeps the dot (fig_3.2.pdf/png)
        if key in ('3.1', '3.7'):      # 3D: tight bbox is unreliable here
            fig.savefig(os.path.join(FIGD, f'{name}.pdf'))
            fig.savefig(os.path.join(PREV, f'{name}.png'), dpi=150)
        else:
            fig.savefig(os.path.join(FIGD, f'{name}.pdf'),
                        bbox_inches='tight', pad_inches=0.03)
            fig.savefig(os.path.join(PREV, f'{name}.png'), dpi=150,
                        bbox_inches='tight', pad_inches=0.03)
        plt.close(fig)
        print('done', key)
