# -*- coding: utf-8 -*-
"""Batch B1: redraw figs 1-13 of Landau Mechanics (vol 1), Chinese 5th ed.
Black-and-white textbook-style vector figures.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc
from scipy.interpolate import PchipInterpolator

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

OUT = r'E:\AI整理书籍\朗道理论物理教程\卷1力学\重排本\figures'
LW = 1.2      # main lines
LW0 = 0.8     # auxiliary lines
FS = 10       # base font size


def new_ax(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def save(fig, n):
    fig.savefig(rf'{OUT}\fig{n}.pdf', bbox_inches='tight', pad_inches=0.03)
    fig.savefig(rf'{OUT}\preview\fig{n}.png', dpi=200,
                bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


def arr(ax, x0, y0, x1, y1, lw=LW0, ms=9):
    """thin arrow with solid head"""
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k',
                                lw=lw, mutation_scale=ms,
                                shrinkA=0, shrinkB=0))


def dim(ax, x0, y0, x1, y1, ms=8, lw=LW0):
    """dimension line with heads at both ends"""
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='<|-|>', color='k',
                                lw=lw, mutation_scale=ms,
                                shrinkA=0, shrinkB=0))


def angle_arc(ax, c, r, t1, t2, lw=LW0):
    ax.add_patch(Arc(c, 2*r, 2*r, angle=0, theta1=t1, theta2=t2,
                     lw=lw, color='k'))


# ---------------------------------------------------------------- fig 1
def fig_1():
    """plane double pendulum"""
    fig, ax = new_ax(3.2, 3.3)
    f1, f2 = np.radians(23), np.radians(36)   # angles from vertical
    l1, l2 = 2.0, 1.8
    P = np.array([0.0, 0.0])
    M1 = P + l1 * np.array([np.sin(f1), -np.cos(f1)])
    M2 = M1 + l2 * np.array([np.sin(f2), -np.cos(f2)])

    # ceiling hatching
    ax.plot([-0.42, 0.42], [0.05, 0.05], 'k-', lw=LW)
    for x in np.arange(-0.40, 0.45, 0.12):
        ax.plot([x, x + 0.16], [0.05, 0.30], 'k-', lw=LW0)
    # x axis (horizontal) and vertical reference through pivot
    ax.plot([0, 3.15], [0, 0], 'k-', lw=LW0)
    ax.text(3.27, -0.02, r'$x$', fontsize=FS, va='center')
    ax.plot([0, 0], [0, -3.62], 'k-', lw=LW0)
    ax.text(-0.12, -3.62, r'$y$', fontsize=FS, va='center', ha='right')

    # strings
    ax.plot([P[0], M1[0]], [P[1], M1[1]], 'k-', lw=LW)
    ax.plot([M1[0], M2[0]], [M1[1], M2[1]], 'k-', lw=LW)
    # thin vertical through m1
    ax.plot([M1[0], M1[0]], [M1[1], M1[1] - 1.50], 'k-', lw=LW0)

    # masses
    ax.plot(*M1, 'ko', ms=6)
    ax.plot(*M2, 'ko', ms=6)

    # angle arcs (between vertical, i.e. 270 deg, and string)
    angle_arc(ax, P, 0.62, 270, 270 + 23)
    ax.text(0.08, -0.84, r'$\varphi_1$', fontsize=FS)
    angle_arc(ax, M1, 0.62, 270, 270 + 36)
    ax.text(M1[0] + 0.24, M1[1] - 0.82, r'$\varphi_2$', fontsize=FS)

    # labels
    ax.text(0.62, -1.08, r'$l_1$', fontsize=FS)
    ax.text(1.60, -2.40, r'$l_2$', fontsize=FS)
    ax.text(M1[0] + 0.15, M1[1] - 0.04, r'$m_1$', fontsize=FS)
    ax.text(M2[0] + 0.15, M2[1] - 0.04, r'$m_2$', fontsize=FS)

    ax.set_xlim(-0.9, 3.7)
    ax.set_ylim(-4.0, 0.65)
    save(fig, 1)


# ---------------------------------------------------------------- fig 2
def fig_2():
    """pendulum with horizontally sliding suspension point"""
    fig, ax = new_ax(3.5, 2.6)
    f = np.radians(33)
    l = 2.6
    M1 = np.array([1.2, 0.0])
    M2 = M1 + l * np.array([np.sin(f), -np.cos(f)])

    # rail: dashed horizontal line + origin cross at left
    ax.plot([-1.35, 2.6], [0, 0], 'k--', lw=LW0)
    ax.plot([-0.8, -0.8], [-0.42, 0.42], 'k--', lw=LW0)
    ax.text(-0.55, 0.13, r'$x$', fontsize=FS)

    # vertical dashed through m1
    ax.plot([M1[0], M1[0]], [0.0, -2.45], 'k--', lw=LW0)

    # string + masses
    ax.plot([M1[0], M2[0]], [M1[1], M2[1]], 'k-', lw=LW)
    ax.plot(*M1, 'ko', ms=6)
    ax.plot(*M2, 'ko', ms=6)

    # angle arc
    angle_arc(ax, M1, 0.62, 270, 270 + 33)
    ax.text(M1[0] + 0.20, -0.80, r'$\varphi$', fontsize=FS)

    ax.text(M1[0] + 0.06, 0.16, r'$m_1$', fontsize=FS, ha='center')
    ax.text(2.28, -1.50, r'$l$', fontsize=FS)
    ax.text(M2[0] + 0.15, M2[1] - 0.04, r'$m_2$', fontsize=FS)

    ax.set_xlim(-1.7, 3.55)
    ax.set_ylim(-2.85, 0.6)
    save(fig, 2)


# ---------------------------------------------------------------- fig 3
def fig_3():
    """pendulum whose suspension point moves along a vertical circle"""
    fig, ax = new_ax(3.2, 3.45)
    R = 1.35
    C = np.array([0.0, 0.0])
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(C[0] + R * np.cos(th), C[1] + R * np.sin(th), 'k-', lw=LW)

    # radius arrow a
    aa = np.radians(48)
    arr(ax, C[0], C[1], R * np.cos(aa), R * np.sin(aa), lw=LW0, ms=10)
    ax.text(0.36, 0.56, r'$a$', fontsize=FS)

    # axes through centre
    ax.plot([0, 2.35], [0, 0], 'k-', lw=LW0)
    ax.text(2.45, -0.02, r'$x$', fontsize=FS, va='center')
    ax.plot([0, 0], [0, -3.05], 'k-', lw=LW0)
    ax.text(-0.12, -2.98, r'$y$', fontsize=FS, va='center', ha='right')

    # pivot on circle (lower right), string down-right, vertical through pivot
    pa = np.radians(-52)
    Q = C + R * np.array([np.cos(pa), np.sin(pa)])
    f = np.radians(40)
    l = 2.15
    M = Q + l * np.array([np.sin(f), -np.cos(f)])
    ax.plot([Q[0], Q[0]], [Q[1], Q[1] - 1.90], 'k-', lw=LW0)
    ax.plot([Q[0], M[0]], [Q[1], M[1]], 'k-', lw=LW)
    ax.plot(*M, 'ko', ms=6)

    angle_arc(ax, Q, 0.55, 270, 270 + 40)
    ax.text(Q[0] + 0.12, Q[1] - 0.80, r'$\varphi$', fontsize=FS)
    ax.text(M[0] + 0.15, M[1] - 0.04, r'$m$', fontsize=FS)

    ax.set_xlim(-1.8, 2.9)
    ax.set_ylim(-3.35, 1.7)
    save(fig, 3)


# ---------------------------------------------------------------- fig 4
def fig_4():
    """system rotating about vertical axis"""
    fig, ax = new_ax(2.9, 3.9)
    A = np.array([0.0, 3.1])
    y1 = 0.0                       # height of m1
    x1 = 1.35
    y2 = -1.7                      # height of m2

    ax.plot([0, 0], [3.75, -2.5], 'k-', lw=LW0)          # vertical axis
    ax.plot([A[0], -x1], [A[1], y1], 'k-', lw=LW)
    ax.plot([A[0],  x1], [A[1], y1], 'k-', lw=LW)
    ax.plot([-x1, 0], [y1, y2], 'k-', lw=LW)
    ax.plot([ x1, 0], [y1, y2], 'k-', lw=LW)

    # masses m1 (open circles), m2 (filled bead on the axis)
    ax.plot(-x1, y1, 'o', mfc='white', mec='k', ms=7, mew=1.1)
    ax.plot(x1, y1, 'o', mfc='white', mec='k', ms=7, mew=1.1)
    ax.add_patch(plt.Rectangle((-0.105, y2 - 0.16), 0.09, 0.34, fc='k', ec='k'))
    ax.add_patch(plt.Rectangle((0.015, y2 - 0.16), 0.09, 0.34, fc='k', ec='k'))

    # angle theta at A (between downward axis and right string)
    th = np.degrees(np.arctan2(y1 - A[1], x1))
    angle_arc(ax, A, 0.72, -90, th)
    ax.text(0.20, 2.20, r'$\theta$', fontsize=FS)

    ax.text(0.09, 3.02, r'$A$', fontsize=FS)
    ax.text(-0.80, 1.62, r'$a$', fontsize=FS)
    ax.text(0.78, 1.62, r'$a$', fontsize=FS)
    ax.text(-0.80, -0.75, r'$a$', fontsize=FS)
    ax.text(0.76, -0.75, r'$a$', fontsize=FS)
    ax.text(-x1 - 0.16, y1 - 0.04, r'$m_1$', fontsize=FS, ha='right')
    ax.text(x1 + 0.16, y1 - 0.04, r'$m_1$', fontsize=FS)
    ax.text(0.20, y2 - 0.04, r'$m_2$', fontsize=FS)

    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-2.75, 3.95)
    save(fig, 4)


# ---------------------------------------------------------------- fig 5
def fig_5():
    """infinitesimal rotation: displacement of the radius vector"""
    fig, ax = new_ax(2.9, 3.9)
    O = np.array([0.0, 0.0])
    B = np.array([0.0, 3.15])          # point on axis, height of P
    T = np.array([1.75, 3.62])         # tip of r
    P = np.array([2.45, 3.15])         # tip of rotated vector

    # rotation axis with arrow
    ax.plot([0, 0], [-0.55, 4.35], 'k-', lw=LW0)
    arr(ax, 0, 4.35, 0, 4.62, lw=LW0, ms=11)
    ax.text(0.14, 4.44, r'$\boldsymbol{\delta\varphi}$', fontsize=FS)
    ax.text(-0.13, -0.10, r'$O$', fontsize=FS, ha='right')

    # thin triangle: B->P horizontal, B->T
    ax.plot([B[0], P[0]], [B[1], P[1]], 'k-', lw=LW0)
    ax.plot([B[0], T[0]], [B[1], T[1]], 'k-', lw=LW0)

    # main vectors
    arr(ax, O[0], O[1], T[0], T[1], lw=LW, ms=11)     # r
    arr(ax, O[0], O[1], P[0], P[1], lw=LW, ms=11)     # rotated r
    arr(ax, P[0], P[1], T[0], T[1], lw=LW, ms=11)     # delta r
    ax.text(1.05, 1.82, r'$r$', fontsize=FS)
    ax.text(2.30, 3.50, r'$\boldsymbol{\delta r}$', fontsize=FS)

    # theta at O
    thT = np.degrees(np.arctan2(T[1], T[0]))
    angle_arc(ax, O, 1.05, 0, thT)
    ax.text(0.28, 0.86, r'$\theta$', fontsize=FS)

    # delta phi angle at B (between horizontal BP and BT) with tick
    th1 = np.degrees(np.arctan2(P[1] - B[1], P[0] - B[0]))
    th2 = np.degrees(np.arctan2(T[1] - B[1], T[0] - B[0]))
    angle_arc(ax, B, 0.72, th1, th2)
    tmid = np.radians((th1 + th2) / 2)
    ax.plot([B[0] + 0.62 * np.cos(tmid), B[0] + 0.84 * np.cos(tmid)],
            [B[1] + 0.62 * np.sin(tmid), B[1] + 0.84 * np.sin(tmid)],
            'k-', lw=LW0)
    ax.text(0.52, 3.42, r'$\delta\varphi$', fontsize=FS)

    ax.set_xlim(-0.75, 2.95)
    ax.set_ylim(-0.75, 4.85)
    save(fig, 5)


# ---------------------------------------------------------------- fig 6
def fig_6():
    """potential energy curve U(x), energy E, turning points x1 x2"""
    fig, ax = new_ax(3.7, 2.0)
    E = 0.5
    xs = np.array([-0.62, -0.30, 0.0, 0.30, 0.55, 0.90, 1.25, 1.60,
                   1.95, 2.25, 2.55, 2.95, 3.30, 3.65])
    us = np.array([1.42, 1.06, 0.84, 0.63, 0.50, 0.30, 0.20, 0.28,
                   0.50, 0.62, 0.66, 0.50, 0.30, 0.06])
    f = PchipInterpolator(xs, us)
    x = np.linspace(-0.62, 3.65, 400)
    ax.plot(x, f(x), 'k-', lw=LW)

    x1, x2, xC = 0.55, 1.95, 2.95
    ytop, ybot = 1.62, -0.12

    # axes
    ax.plot([0, 0], [ybot, ytop], 'k-', lw=LW0)
    ax.text(0.09, 1.52, r'$U$', fontsize=FS)
    ax.plot([-0.62, 4.15], [0, 0], 'k-', lw=LW0)
    ax.text(4.15, -0.10, r'$x$', fontsize=FS, ha='center', va='top')

    # energy line
    ax.plot([-0.62, 4.15], [E, E], 'k--', lw=LW0)
    ax.text(4.12, E + 0.06, r'$U=E$', fontsize=FS, ha='right')

    # dashed drop lines and point labels
    ax.plot([x1, x1], [0, E], 'k--', lw=LW0)
    ax.plot([x2, x2], [0, E], 'k--', lw=LW0)
    ax.text(x1 + 0.06, E + 0.07, r'$A$', fontsize=FS)
    ax.text(x2 - 0.10, E + 0.07, r'$B$', fontsize=FS)
    ax.text(xC + 0.07, E + 0.07, r'$C$', fontsize=FS)
    ax.text(x1, -0.10, r'$x_1$', fontsize=FS, ha='center', va='top')
    ax.text(x2, -0.10, r'$x_2$', fontsize=FS, ha='center', va='top')

    # hatching of allowed regions under the x axis
    for x0 in np.arange(x1 + 0.05, x2 - 0.02, 0.105):
        ax.plot([x0, x0 - 0.075], [0, -0.085], 'k-', lw=LW0)
    for x0 in np.arange(xC + 0.05, 4.11, 0.105):
        ax.plot([x0, x0 - 0.075], [0, -0.085], 'k-', lw=LW0)

    ax.set_xlim(-0.68, 4.28)
    ax.set_ylim(-0.32, 1.72)
    save(fig, 6)


# ---------------------------------------------------------------- fig 7
def fig_7():
    """recovering U(x) from the period; single well, x1(U), x2(U)"""
    fig, ax = new_ax(3.5, 2.1)
    E = 1.35
    x1, x2 = -1.55, 1.55
    x = np.linspace(-1.85, 1.85, 400)
    u = 0.56 * x ** 2
    ax.plot(x, u, 'k-', lw=LW)

    # axes
    ax.plot([0, 0], [-0.06, 2.25], 'k-', lw=LW0)
    ax.text(0.10, 2.12, r'$U$', fontsize=FS)
    ax.plot([-2.15, 2.35], [0, 0], 'k-', lw=LW0)
    ax.text(2.35, -0.09, r'$x$', fontsize=FS, ha='center', va='top')

    # E line + drop lines
    ax.plot([-2.15, 2.35], [E, E], 'k--', lw=LW0)
    ax.text(2.42, E, r'$U=E$', fontsize=FS, va='center')
    ax.plot([x1, x1], [0, E], 'k--', lw=LW0)
    ax.plot([x2, x2], [0, E], 'k--', lw=LW0)
    ax.text(x1, -0.09, r'$x_1$', fontsize=FS, ha='center', va='top')
    ax.text(x2, -0.09, r'$x_2$', fontsize=FS, ha='center', va='top')
    ax.text(0.02, -0.09, r'$O$', fontsize=FS, ha='center', va='top')

    # curved labels along branches (inside the well)
    ax.text(-0.86, 0.66, r'$x_1(U)$', fontsize=FS, rotation=-52,
            rotation_mode='anchor', ha='center', va='center')
    ax.text(0.86, 0.66, r'$x_2(U)$', fontsize=FS, rotation=52,
            rotation_mode='anchor', ha='center', va='center')

    ax.set_xlim(-2.3, 3.05)
    ax.set_ylim(-0.35, 2.42)
    save(fig, 7)


# ---------------------------------------------------------------- fig 8
def fig_8():
    """areal velocity: sector swept by the radius vector"""
    fig, ax = new_ax(3.3, 2.9)
    O = np.array([0.0, 0.0])
    # trajectory: smooth branch r(theta), passing through P1 (31 deg), P2 (13 deg)
    thd = np.linspace(60, -9, 300)
    th = np.radians(thd)
    r = 2.0 + 0.05 * np.cos(np.radians(6 * (thd - 22))) + 0.0006 * (thd - 22) ** 2
    ax.plot(r * np.cos(th), r * np.sin(th), 'k-', lw=LW)

    P1 = np.array([1.76, 1.06])
    P2 = np.array([2.00, 0.46])
    arr(ax, O[0], O[1], P1[0], P1[1], lw=LW0, ms=10)
    arr(ax, O[0], O[1], P2[0], P2[1], lw=LW0, ms=10)
    ax.text(0.80, 0.64, r'$r$', fontsize=FS)

    # dashed segment rdphi: from P1 down to the lower radius vector
    u2 = P2 / np.linalg.norm(P2)
    P1p = np.dot(P1, u2) * u2
    ax.plot([P1[0], P1p[0]], [P1[1], P1p[1]], 'k--', lw=LW0)
    ax.text(1.80, 0.66, r'$r\,\mathrm{d}\varphi$', fontsize=FS, ha='right')

    # angle arc at O
    t1 = np.degrees(np.arctan2(P2[1], P2[0]))
    t2 = np.degrees(np.arctan2(P1[1], P1[0]))
    angle_arc(ax, O, 0.90, t1, t2)
    ax.text(1.10, 0.36, r'$\mathrm{d}\varphi$', fontsize=FS)

    ax.text(-0.20, -0.06, r'$O$', fontsize=FS, ha='right')

    ax.set_xlim(-0.55, 3.30)
    ax.set_ylim(-0.70, 2.75)
    save(fig, 8)


# ---------------------------------------------------------------- fig 9
def fig_9():
    """non-closing rosette orbit filling the annulus r_min..r_max"""
    fig, ax = new_ax(3.4, 3.5)
    rmax, rmin = 1.55, 0.28
    rm = 0.5 * (rmax + rmin)
    amp = 0.5 * (rmax - rmin)
    dphi = np.radians(312.0)          # angle swept between apocentres
    nu = 2 * np.pi / dphi
    phi = np.linspace(0, 5.5 * dphi, 4500)
    r = rm + amp * np.cos(nu * phi)
    X, Y = r * np.cos(phi), r * np.sin(phi)
    ax.plot(X, Y, 'k-', lw=LW)

    # dashed circles rmin, rmax
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(rmax * np.cos(th), rmax * np.sin(th), 'k--', lw=LW0)
    ax.plot(rmin * np.cos(th), rmin * np.sin(th), 'k--', lw=LW0)

    # centre: open circle + small arrow to the right
    ax.plot(0, 0, 'o', mfc='white', mec='k', ms=5, mew=1.0)
    arr(ax, 0.03, 0, 0.55, 0, lw=LW0, ms=8)

    # rmax radial pointer at ~123 deg
    aa = np.radians(123)
    arr(ax, 0, 0, rmax * np.cos(aa), rmax * np.sin(aa), lw=LW0, ms=9)
    ax.text(-1.08, 0.64, r'$r_\mathrm{max}$', fontsize=FS,
            ha='right', va='center')
    # rmin pointer at ~112 deg
    ab = np.radians(112)
    ax.plot([0.04, rmin * np.cos(ab)], [0.04, rmin * np.sin(ab)], 'k-', lw=LW0)
    ax.text(-0.20, 0.42, r'$r_\mathrm{min}$', fontsize=FS,
            ha='center', va='center')

    # arrows along the orbit (motion counterclockwise)
    for deg in range(8, 1685, 58):
        p0, p1 = np.radians(deg), np.radians(deg + 6)
        r0 = rm + amp * np.cos(nu * p0)
        r1 = rm + amp * np.cos(nu * p1)
        arr(ax, r0 * np.cos(p0), r0 * np.sin(p0),
            r1 * np.cos(p1), r1 * np.sin(p1), lw=LW0, ms=8)

    # ticks + brace between successive apocentres at 216 and 264 deg
    pa1, pa2 = 216.0, 264.0
    for pa in (pa1, pa2):
        rad = np.radians(pa)
        ax.plot([rmax * 0.93 * np.cos(rad), rmax * 1.07 * np.cos(rad)],
                [rmax * 0.93 * np.sin(rad), rmax * 1.07 * np.sin(rad)],
                'k-', lw=LW0)
    # curly brace along the arc: smooth ends, pointed cusp at middle
    t = np.linspace(0, 1, 120)
    tang = np.radians(pa1 + t * (pa2 - pa1))
    Rb = rmax * 1.06 + rmax * 0.15 * np.sqrt(np.sin(np.pi * t))
    ax.plot(Rb * np.cos(tang), Rb * np.sin(tang), 'k-', lw=LW0)
    ax.text(-1.92, -1.12, r'$\Delta\varphi$', fontsize=FS, ha='right')

    ax.set_xlim(-2.30, 2.05)
    ax.set_ylim(-2.15, 2.15)
    save(fig, 9)


# ---------------------------------------------------------------- fig 10
def fig_10():
    """effective potential U_eff for an attractive Coulomb field"""
    fig, ax = new_ax(3.0, 2.9)
    xs = np.array([0.20, 0.35, 0.55, 0.80, 1.00, 1.25, 1.50, 1.80,
                   2.10, 2.40, 2.70, 3.00, 3.25])
    us = np.array([2.95, 1.35, 0.60, 0.12, -0.14, -0.32, -0.43, -0.48,
                   -0.49, -0.465, -0.41, -0.34, -0.27])
    f = PchipInterpolator(xs, us)
    x = np.linspace(0.20, 3.25, 500)
    ax.plot(x, f(x), 'k-', lw=LW)

    ax.plot([0, 0], [-1.05, 2.85], 'k-', lw=LW0)
    ax.plot([-0.45, 3.35], [0, 0], 'k-', lw=LW0)
    ax.text(3.45, 0.0, r'$r$', fontsize=FS, va='center')
    ax.text(-0.10, 2.72, r'$U_\mathrm{eff}$', fontsize=FS, ha='right')
    ax.text(-0.10, -0.12, r'$O$', fontsize=FS, ha='right', va='top')

    ax.set_xlim(-0.62, 3.75)
    ax.set_ylim(-1.30, 3.10)
    save(fig, 10)


# ---------------------------------------------------------------- fig 11
def fig_11():
    """elliptic orbit geometry: 2a, 2b, p, ae (focus at origin)"""
    fig, ax = new_ax(3.6, 3.4)
    a, e = 1.5, 0.58
    b = a * np.sqrt(1 - e ** 2)
    ae = a * e
    p = a * (1 - e ** 2)
    cxe = -ae                                   # ellipse centre (focus at O)

    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(cxe + a * np.cos(th), b * np.sin(th), 'k-', lw=LW)

    # axes: x through centre, y through focus
    ax.plot([-2.62, 2.15], [0, 0], 'k-', lw=LW0)
    ax.text(2.26, 0.0, r'$x$', fontsize=FS, va='center')
    ax.plot([0, 0], [2.30, -1.55], 'k-', lw=LW0)
    ax.text(0.10, 2.22, r'$y$', fontsize=FS)

    # 2b dimension at left
    dim(ax, -2.42, b, -2.42, -b)
    ax.plot([-2.42, cxe - a], [b, b], 'k-', lw=LW0)
    ax.plot([-2.42, cxe - a], [-b, -b], 'k-', lw=LW0)
    ax.text(-2.56, 0.0, r'$2b$', fontsize=FS, ha='right', va='center')

    # 2a dimension at bottom
    dim(ax, cxe - a, -2.30, cxe + a, -2.30)
    ax.plot([cxe - a, cxe - a], [-b, -2.30], 'k-', lw=LW0)
    ax.plot([cxe + a, cxe + a], [-b, -2.30], 'k-', lw=LW0)
    ax.text(cxe, -2.20, r'$2a$', fontsize=FS, ha='center', va='bottom')

    # p dimension: from x-axis up to the ellipse at the focus
    dim(ax, -0.22, 0, -0.22, p)
    ax.plot([-0.22, 0], [p, p], 'k-', lw=LW0)
    ax.text(-0.34, p * 0.52, r'$p$', fontsize=FS, ha='right')

    # ae dimension: centre tick to focus line, below axis
    ax.plot([cxe, cxe], [0, -0.66], 'k-', lw=LW0)
    dim(ax, cxe, -0.55, 0, -0.55)
    ax.text(-ae / 2, -0.47, r'$ae$', fontsize=FS, ha='center', va='bottom')

    ax.set_xlim(-3.0, 2.55)
    ax.set_ylim(-2.75, 2.55)
    save(fig, 11)


# ---------------------------------------------------------------- fig 12
def fig_12():
    """hyperbolic orbit, attractive field (e>1): p and a(e-1)"""
    fig, ax = new_ax(2.7, 3.3)
    e, p = 2.0, 2.0
    ph = np.linspace(-np.radians(97), np.radians(97), 400)
    r = p / (1 + e * np.cos(ph))
    ax.plot(r * np.cos(ph), r * np.sin(ph), 'k-', lw=LW)

    # axes
    ax.plot([-1.0, 2.15], [0, 0], 'k-', lw=LW0)
    ax.text(2.25, 0.0, r'$x$', fontsize=FS, va='center')
    ax.plot([0, 0], [-2.60, 2.60], 'k-', lw=LW0)
    ax.text(0.10, 2.48, r'$y$', fontsize=FS)
    ax.text(-0.10, -0.12, r'$O$', fontsize=FS, ha='right', va='top')

    # p dimension (curve crosses y-axis at height p)
    dim(ax, -0.55, 0, -0.55, p)
    ax.plot([-0.55, 0], [p, p], 'k-', lw=LW0)
    ax.text(-0.67, p * 0.5, r'$p$', fontsize=FS, ha='right', va='center')

    # a(e-1) dimension: vertex distance; text above arrow (as in book)
    rmin = p / (1 + e)
    ax.plot([0, 0], [0, -0.84], 'k-', lw=LW0)
    ax.plot([rmin, rmin], [0, -0.84], 'k-', lw=LW0)
    dim(ax, 0, -0.68, rmin, -0.68)
    ax.text(0.03, -0.42, r'$a(e-1)$', fontsize=9, ha='left', va='center')

    ax.set_xlim(-1.15, 2.50)
    ax.set_ylim(-2.85, 2.80)
    save(fig, 12)


# ---------------------------------------------------------------- fig 13
def fig_13():
    """hyperbolic orbit, repulsive field: a(e+1)"""
    fig, ax = new_ax(2.8, 3.3)
    e, p = 1.5, 1.15
    a = p / (e ** 2 - 1)
    ph = np.linspace(-np.radians(46.5), np.radians(46.5), 400)
    r = p / (e * np.cos(ph) - 1)
    ax.plot(r * np.cos(ph), r * np.sin(ph), 'k-', lw=LW)

    # axes
    ax.plot([-0.85, 4.15], [0, 0], 'k-', lw=LW0)
    ax.text(4.28, 0.0, r'$x$', fontsize=FS, va='center')
    ax.plot([0, 0], [-2.75, 2.75], 'k-', lw=LW0)
    ax.text(0.10, 2.62, r'$y$', fontsize=FS)
    ax.text(-0.10, -0.12, r'$O$', fontsize=FS, ha='right', va='top')

    # a(e+1) dimension
    rmin = p / (e - 1)
    ax.plot([0, 0], [0, -0.90], 'k-', lw=LW0)
    ax.plot([rmin, rmin], [0, -0.90], 'k-', lw=LW0)
    dim(ax, 0, -0.76, rmin, -0.76)
    ax.text(rmin / 2, -0.58, r'$a(e+1)$', fontsize=FS,
            ha='center', va='bottom')

    ax.set_xlim(-1.15, 4.75)
    ax.set_ylim(-3.05, 2.95)
    save(fig, 13)


if __name__ == '__main__':
    import sys
    todo = sys.argv[1:] or [f'{i}' for i in range(1, 14)]
    for t in todo:
        globals()[f'fig_{t}']()
        print(f'fig {t} done')
