# -*- coding: utf-8 -*-
"""Batch B2: redraw figs 14-27 of Landau Mechanics (vol.1), Chinese 5th ed.
Black-and-white textbook-style vector figures. See 插图规范.md.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

OUT = r'E:\AI整理书籍\朗道理论物理教程\卷1力学\重排本\figures'
PRE = OUT + r'\preview'

LW = 1.2      # main lines
LW0 = 0.8     # auxiliary lines
FS = 9        # default font size
DD = (0, (5, 2, 1, 2))   # dash-dot pattern for tangent constructions


def new_ax(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_axis_off()
    return fig, ax


def vec(ax, p0, p1, lw=LW, ms=9, style='-|>', ls='-'):
    """straight arrow from p0 to p1 (filled head, book style)"""
    ax.annotate('', xy=p1, xytext=p0, zorder=5,
                arrowprops=dict(arrowstyle=style, color='k', lw=lw,
                                linestyle=ls, mutation_scale=ms,
                                shrinkA=0, shrinkB=0))


def arc(ax, c, r, a1, a2, lw=LW0):
    """plain thin arc from angle a1 to a2 (degrees), counterclockwise"""
    ax.add_patch(Arc(c, 2 * r, 2 * r, angle=0, theta1=a1, theta2=a2,
                     lw=lw, color='k', capstyle='round'))


def save(fig, name):
    fig.savefig(f'{OUT}\\{name}.pdf', bbox_inches='tight', pad_inches=0.03)
    fig.savefig(f'{PRE}\\{name}.png', dpi=200, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)
    print(name, 'done')


def _spring(ax, p0, p1, n=13, amp=0.055):
    """zigzag spring from p0 to p1"""
    p0 = np.array(p0, float)
    p1 = np.array(p1, float)
    d = p1 - p0
    L = np.linalg.norm(d)
    u = d / L
    w = np.array([-u[1], u[0]])
    s = np.zeros(n + 2)
    s[1:-1] = [(-1.0) ** (i + 1) for i in range(n)]
    ks = np.linspace(0, 1, n + 2)
    pts = p0[None, :] + ks[:, None] * d[None, :] + (amp * s)[:, None] * w[None, :]
    ax.plot(pts[:, 0], pts[:, 1], 'k-', lw=0.9)


# ---------------------------------------------------------------- fig 14
def fig_14():
    """Velocity circle for decay of a particle, panels (a) V<v0, (b) V>v0."""
    fig, axs = plt.subplots(1, 2, figsize=(3.2, 1.75))

    # ---- panel (a): V < v0
    ax = axs[0]
    ax.set_aspect('equal')
    ax.set_axis_off()
    R = 1.0                     # circle radius = v0
    V = 0.63                    # |V|
    O = (0.0, 0.0)
    A = (-V, 0.0)
    t = np.radians(48.0)
    C = (R * np.cos(t), R * np.sin(t))
    ax.add_patch(Circle(O, R, fill=False, lw=LW, ec='k'))
    ax.plot([O[0], R], [O[1], O[1]], 'k--', lw=LW0)          # dashed horiz. radius
    vec(ax, A, O)                                             # V
    vec(ax, A, C)                                             # v
    vec(ax, O, C)                                             # v0
    th = np.degrees(np.arctan2(C[1] - A[1], C[0] - A[0]))
    arc(ax, A, 0.30, 0, th)
    arc(ax, O, 0.30, 0, 48.0)
    ax.text(-0.17, 0.13, r'$\theta$', fontsize=FS)
    ax.text(0.36, 0.10, r'$\theta_0$', fontsize=FS)
    ax.text(A[0] - 0.20, -0.24, r'$A$', fontsize=FS)
    ax.text(-0.38, -0.20, r'$\boldsymbol{V}$', fontsize=FS)
    ax.text(-0.14, 0.48, r'$\boldsymbol{v}$', fontsize=FS)
    ax.text(0.55, 0.55, r'$\boldsymbol{v}_0$', fontsize=FS)
    ax.set_xlim(-1.25, 1.15)
    ax.set_ylim(-1.15, 1.15)

    # ---- panel (b): V > v0
    ax = axs[1]
    ax.set_aspect('equal')
    ax.set_axis_off()
    R = 0.55                    # circle radius = v0
    V = 1.06                    # |V|
    O = (0.0, 0.0)
    A = (-V, 0.0)
    tt = np.radians(50.0)
    C = (R * np.cos(tt), R * np.sin(tt))                      # endpoint of v
    alpha = np.arcsin(R / V)                                  # theta_max
    lt = np.sqrt(V * V - R * R)
    T = (A[0] + lt * np.cos(alpha), lt * np.sin(alpha))       # tangent point
    ax.add_patch(Circle(O, R, fill=False, lw=LW, ec='k'))
    ax.plot([O[0], R], [O[1], O[1]], 'k--', lw=LW0)
    vec(ax, A, O)                                             # V
    vec(ax, A, C)                                             # v
    vec(ax, O, C)                                             # v0
    vec(ax, A, T, lw=LW0, ms=7, ls=DD)                        # tangent A->T
    vec(ax, O, T, lw=LW0, ms=7, ls=DD)                        # radius O->T
    thv = np.degrees(np.arctan2(C[1] - A[1], C[0] - A[0]))
    thmax = np.degrees(alpha)
    arc(ax, A, 0.20, 0, thv)                                  # theta
    arc(ax, A, 0.34, 0, thmax)                                # theta_max
    ax.text(-0.78, -0.22, r'$\theta$', fontsize=FS)
    ax.text(-1.05, 0.40, r'$\theta_\mathrm{max}$', fontsize=FS)
    ax.text(0.26, 0.10, r'$\theta_0$', fontsize=FS)
    ax.text(A[0] - 0.10, -0.24, r'$A$', fontsize=FS)
    ax.text(-0.56, -0.22, r'$\boldsymbol{V}$', fontsize=FS)
    ax.text(-0.10, 0.42, r'$\boldsymbol{v}$', fontsize=FS)
    ax.text(0.33, 0.28, r'$\boldsymbol{v}_0$', fontsize=FS)
    ax.text(C[0] + 0.02, C[1] + 0.08, r'$C$', fontsize=FS)
    # B: where line AC enters the circle (near intersection)
    d = np.array(C) - np.array(A)
    d = d / np.linalg.norm(d)
    fc = np.array(A)
    tb = -np.dot(fc, d) - np.sqrt(np.dot(fc, d) ** 2 - np.dot(fc, fc) + R ** 2)
    Bpt = fc + tb * d
    ax.text(Bpt[0] + 0.10, Bpt[1] - 0.12, r'$B$', fontsize=FS)
    ax.set_xlim(-1.30, 0.85)
    ax.set_ylim(-1.15, 1.15)

    fig.subplots_adjust(wspace=0.04, left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 'fig14')


# ---------------------------------------------------------------- fig 15
def fig_15():
    """Momentum circle for collision of two particles + vector formulas."""
    fig, ax = new_ax(2.0, 2.45)
    ax.set_aspect('equal')
    R = 1.0
    O = (0.0, 0.0)
    A = (-0.45, 0.0)
    B = (1.0, 0.0)
    tc = np.radians(80.0)
    C = (R * np.cos(tc), R * np.sin(tc))
    ax.add_patch(Circle(O, R, fill=False, lw=LW, ec='k'))
    vec(ax, A, (-0.05, 0.0))                        # AO (head before O)
    vec(ax, O, B)                                   # OB
    vec(ax, A, C)                                   # p1'
    vec(ax, C, (0.955, 0.0))                        # p2' (head before B)
    vec(ax, O, (0.555 * C[0], 0.555 * C[1]))        # n0, head partway
    ax.text(C[0] - 0.02, C[1] + 0.10, r'$C$', fontsize=FS)
    ax.text(A[0] - 0.20, -0.22, r'$A$', fontsize=FS)
    ax.text(O[0] - 0.05, -0.24, r'$O$', fontsize=FS)
    ax.text(B[0] - 0.02, -0.24, r'$B$', fontsize=FS)
    ax.text(-0.70, 0.68, r"$\boldsymbol{p}_1'$", fontsize=FS)
    ax.text(0.63, 0.62, r"$\boldsymbol{p}_2'$", fontsize=FS)
    ax.text(0.24, 0.40, r'$\boldsymbol{n}_0$', fontsize=FS)

    # three small vector-formula lines below the circle (drawn in-figure)
    xe = 0.30                # x of the '=' sign, shared by all three lines
    ys = (-1.38, -1.98, -2.58)
    rights = (r'$= m\,\boldsymbol{v}\,,$',
              r'$= \dfrac{m_1(\boldsymbol{p}_1+\boldsymbol{p}_2)}{m_1+m_2}\,,$',
              r'$= \dfrac{m_2(\boldsymbol{p}_1+\boldsymbol{p}_2)}{m_1+m_2}\,.$')
    lefts = ('OC', 'AO', 'OB')
    for y, rt, lf in zip(ys, rights, lefts):
        ax.text(xe, y, rt, fontsize=7.5, ha='left', va='center')
        ax.text(xe - 0.045, y, lf, fontsize=7.5, ha='right', va='center')
        # small vector arrow above the two-letter symbol
        ax.annotate('', xy=(xe - 0.05, y + 0.14), xytext=(xe - 0.25, y + 0.14),
                    arrowprops=dict(arrowstyle='->', color='k', lw=0.6,
                                    shrinkA=0, shrinkB=0))
    ax.set_xlim(-1.50, 1.50)
    ax.set_ylim(-2.85, 1.15)
    save(fig, 'fig15')


# ---------------------------------------------------------------- fig 16
def _mom_circle(ax, A, C, R, tang=False):
    """common drawing of the momentum circle for fig16"""
    O = (0.0, 0.0)
    B = (R, 0.0)
    ax.add_patch(Circle(O, R, fill=False, lw=LW, ec='k'))
    if A[0] > -R:      # A inside: dashed extension to the left rim
        ax.plot([-R, A[0]], [0, 0], 'k--', lw=LW0)
    vec(ax, A, B)                                   # p1 (horizontal)
    vec(ax, A, C)                                   # p1'
    vec(ax, C, (R - 0.045, 0.0))                    # p2' (head before B)
    ax.plot([O[0], C[0]], [O[1], C[1]], 'k--', lw=LW0)      # OC dashed
    thc = np.degrees(np.arctan2(C[1], C[0]))
    tha = np.degrees(np.arctan2(C[1] - A[1], C[0] - A[0]))
    arc(ax, O, 0.30, 0, thc)                        # chi
    arc(ax, A, 0.26, 0, tha)                        # theta1
    thb = np.degrees(np.arctan2(C[1], C[0] - R))    # direction B->C
    arc(ax, B, 0.30, thb, 180.0)                    # theta2
    if tang:                                        # dash-dot tangent, theta_max
        V = abs(A[0])
        alpha = np.arcsin(R / V)
        lt = np.sqrt(V * V - R * R)
        T = (A[0] + lt * np.cos(alpha), lt * np.sin(alpha))
        vec(ax, A, T, lw=LW0, ms=7, ls=DD)
        arc(ax, A, 0.44, tha, np.degrees(alpha))
    return O, B, thc, tha, thb


def fig_16():
    """Momentum circles, (a) m1<m2  (b) m1>m2."""
    fig, axs = plt.subplots(1, 2, figsize=(3.4, 1.85),
                            gridspec_kw={'width_ratios': [2.45, 3.55]})

    # ---- (a) m1 < m2 : A inside
    ax = axs[0]
    ax.set_aspect('equal')
    ax.set_axis_off()
    R = 1.0
    A = (-0.55, 0.0)
    tc = np.radians(62.0)
    C = (R * np.cos(tc), R * np.sin(tc))
    O, B, thc, tha, thb = _mom_circle(ax, A, C, R)
    ax.text(C[0] - 0.04, C[1] + 0.09, r'$C$', fontsize=FS)
    ax.text(A[0] - 0.19, -0.22, r'$A$', fontsize=FS)
    ax.text(O[0] - 0.05, -0.24, r'$O$', fontsize=FS)
    ax.text(B[0] + 0.02, -0.24, r'$B$', fontsize=FS)
    ax.text(-0.12, 0.52, r"$\boldsymbol{p}_1'$", fontsize=FS)
    ax.text(0.42, 0.64, r"$\boldsymbol{p}_2'$", fontsize=FS)
    ax.text(0.36, 0.10, r'$\chi$', fontsize=FS)
    ax.text(-0.13, 0.13, r'$\theta_1$', fontsize=FS)
    ax.text(0.56, 0.12, r'$\theta_2$', fontsize=FS)
    ax.set_xlim(-1.25, 1.2)
    ax.set_ylim(-1.15, 1.15)

    # ---- (b) m1 > m2 : A outside, theta_max tangent shown
    ax = axs[1]
    ax.set_aspect('equal')
    ax.set_axis_off()
    R = 1.0
    V = 1.80
    A = (-V, 0.0)
    tc = np.radians(50.0)
    C = (R * np.cos(tc), R * np.sin(tc))
    O, B, thc, tha, thb = _mom_circle(ax, A, C, R, tang=True)
    ax.text(C[0] - 0.04, C[1] + 0.09, r'$C$', fontsize=FS)
    ax.text(A[0] - 0.10, -0.22, r'$A$', fontsize=FS)
    ax.text(O[0] - 0.04, -0.24, r'$O$', fontsize=FS)
    ax.text(B[0] + 0.03, -0.24, r'$B$', fontsize=FS)
    ax.text(-0.66, 0.46, r"$\boldsymbol{p}_1'$", fontsize=FS)
    ax.text(0.53, 0.68, r"$\boldsymbol{p}_2'$", fontsize=FS)
    ax.text(0.36, 0.10, r'$\chi$', fontsize=FS)
    ax.text(-1.42, -0.20, r'$\theta_1$', fontsize=FS)
    ax.text(0.52, 0.12, r'$\theta_2$', fontsize=FS)
    ax.text(-1.52, 0.50, r'$\theta_\mathrm{max}$', fontsize=FS)
    ax.set_xlim(-2.35, 1.2)
    ax.set_ylim(-1.15, 1.15)

    fig.subplots_adjust(wspace=0.02, left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 'fig16')


# ---------------------------------------------------------------- fig 17
def fig_17():
    """Equal masses: A and B both on the circle, exit rays perpendicular."""
    fig, ax = new_ax(2.1, 2.1)
    ax.set_aspect('equal')
    R = 1.0
    O = (0.0, 0.0)
    A = (-R, 0.0)
    B = (R, 0.0)
    tc = np.radians(62.0)
    C = (R * np.cos(tc), R * np.sin(tc))
    ax.add_patch(Circle(O, R, fill=False, lw=LW, ec='k'))
    vec(ax, A, B)                                   # p1 horizontal
    vec(ax, A, C)                                   # p1'
    vec(ax, C, (R - 0.045, 0.0))                    # p2'
    ax.plot([O[0], C[0]], [O[1], C[1]], 'k--', lw=LW0)
    thc = np.degrees(np.arctan2(C[1], C[0]))
    tha = np.degrees(np.arctan2(C[1], C[0] + R))
    arc(ax, O, 0.34, 0, thc)
    arc(ax, A, 0.34, 0, tha)
    thb = np.degrees(np.arctan2(C[1], C[0] - R))
    arc(ax, B, 0.34, thb, 180.0)
    ax.text(C[0] - 0.02, C[1] + 0.09, r'$C$', fontsize=FS)
    ax.text(A[0] - 0.22, -0.10, r'$A$', fontsize=FS)
    ax.text(O[0] - 0.05, -0.24, r'$O$', fontsize=FS)
    ax.text(B[0] + 0.04, -0.10, r'$B$', fontsize=FS)
    ax.text(-0.40, 0.60, r"$\boldsymbol{p}_1'$", fontsize=FS)
    ax.text(0.46, 0.70, r"$\boldsymbol{p}_2'$", fontsize=FS)
    ax.text(0.40, 0.13, r'$\chi$', fontsize=FS)
    ax.text(-0.50, 0.15, r'$\theta_1$', fontsize=FS)
    ax.text(0.58, 0.16, r'$\theta_2$', fontsize=FS)
    ax.set_xlim(-1.45, 1.3)
    ax.set_ylim(-1.15, 1.15)
    save(fig, 'fig17')


# ---------------------------------------------------------------- fig 18
def fig_18():
    """Scattering in a central field: periapsis A, impact parameter rho."""
    fig, ax = new_ax(2.4, 2.05)
    ax.set_aspect('equal')
    rho = 1.0
    O = (0.0, 0.0)
    f0 = np.radians(53.0)                    # OA azimuth
    rmin = 3.2
    A = (rmin * np.cos(f0), rmin * np.sin(f0))
    P = (0.55, rho)                          # intersection of the asymptotes
    dst = np.radians(104.0)                  # outgoing asymptote direction
    dirv = np.array([np.cos(dst), np.sin(dst)])

    ax.plot([-0.75, 2.15], [0, 0], 'k--', lw=LW0)             # line through O
    ax.plot([-0.35, 2.45], [rho, rho], 'k--', lw=LW0)         # incoming asymp.
    ax.plot([P[0], P[0] + 3.1 * dirv[0]], [P[1], P[1] + 3.1 * dirv[1]],
            'k--', lw=LW0)                                    # outgoing asymp.
    ax.plot([O[0], A[0]], [O[1], A[1]], 'k--', lw=LW0)        # OA
    vec(ax, (1.7, 0.0), (1.7, rho), lw=LW0, ms=7, style='<|-|>')
    ax.text(1.82, 0.38, r'$\rho$', fontsize=FS)
    arc(ax, O, 0.42, 0, 53.0)
    ax.text(0.62, 0.30, r'$\varphi_0$', fontsize=FS)
    arc(ax, P, 0.50, 104.0, 180.0)
    ax.text(0.02, 1.52, r'$\chi$', fontsize=FS)

    # schematic trajectory: S -> A -> E (cubics with prescribed tangents)
    S = np.array([3.55, rho])
    dirA = np.array([np.cos(f0 + np.pi / 2), np.sin(f0 + np.pi / 2)])
    E = P + 2.75 * dirv

    def hermite(P0, P1, m0, m1, n=80):
        t = np.linspace(0, 1, n)[:, None]
        h00 = 2 * t ** 3 - 3 * t ** 2 + 1
        h10 = t ** 3 - 2 * t ** 2 + t
        h01 = -2 * t ** 3 + 3 * t ** 2
        h11 = t ** 3 - t ** 2
        return h00 * P0 + h10 * m0 + h01 * P1 + h11 * m1

    Aa = np.array(A)
    seg1 = hermite(S, Aa, -1.6 * np.array([1.0, 0.0]), 1.7 * dirA)
    seg2 = hermite(Aa, E, 1.7 * dirA, 2.6 * dirv)
    ax.plot(seg1[:, 0], seg1[:, 1], 'k-', lw=LW)
    ax.plot(seg2[:, 0], seg2[:, 1], 'k-', lw=LW)
    vec(ax, (3.0, 1.01), (2.6, 1.01), lw=LW, ms=8)            # incoming arrow
    p1 = Aa + 1.5 * dirA                                       # outgoing arrow
    vec(ax, tuple(p1 - 0.22 * dirA), tuple(p1 + 0.22 * dirA), lw=LW, ms=8)
    ax.text(A[0] + 0.12, A[1] + 0.02, r'$A$', fontsize=FS)
    ax.text(O[0] - 0.28, -0.30, r'$O$', fontsize=FS)
    ax.set_xlim(-0.95, 3.75)
    ax.set_ylim(-0.65, 4.1)
    save(fig, 'fig18')


# ---------------------------------------------------------------- fig 19
def fig_19():
    """Scattering off a rigid sphere: rho = a sin(phi0)."""
    fig, ax = new_ax(1.9, 1.8)
    ax.set_aspect('equal')
    a = 1.0
    O = (0.0, 0.0)
    f0d = 40.0
    f0 = np.radians(f0d)
    P1 = (a * np.cos(f0), a * np.sin(f0))
    rho = np.sin(f0)
    ax.add_patch(Circle(O, a, fill=False, lw=LW, ec='k'))
    ax.plot([0, 2.35], [0, 0], 'k--', lw=LW0)                 # line through centre
    ax.plot([O[0], 1.5 * P1[0]], [O[1], 1.5 * P1[1]], 'k--', lw=LW0)
    ax.plot([2.35, P1[0]], [rho, rho], 'k-', lw=LW)           # incoming ray
    vec(ax, (1.75, rho), (1.45, rho), lw=LW, ms=8)            # motion arrow
    vr = np.array([np.cos(2 * f0), np.sin(2 * f0)])           # reflected ray
    vec(ax, P1, tuple(P1 + 1.35 * vr))
    pm = P1 + 0.75 * vr
    vp = np.array([-vr[1], vr[0]])
    vec(ax, tuple(pm + 0.13 * vp), tuple(pm - 0.13 * vp), lw=LW, ms=8)
    vec(ax, (1.85, 0.0), (1.85, rho), lw=LW0, ms=7, style='<|-|>')
    ax.text(1.97, 0.26, r'$\rho$', fontsize=FS)
    arc(ax, O, 0.40, 0, f0d)
    ax.text(0.58, 0.24, r'$\varphi_0$', fontsize=FS)
    ax.text(0.30, 0.52, r'$a$', fontsize=FS)
    ax.set_xlim(-1.15, 2.55)
    ax.set_ylim(-1.15, 2.15)
    save(fig, 'fig19')


# ---------------------------------------------------------------- fig 20
def fig_20():
    """U_eff(r) for U = -alpha/r^n: barrier of height U0."""
    fig, ax = new_ax(1.75, 1.7)
    x0 = 7.0
    ax.plot([x0, x0], [-1.35, 1.75], 'k-', lw=LW0)            # vertical axis
    ax.plot([x0, 26.6], [0, 0], 'k-', lw=LW0)                 # r axis
    ax.text(x0 + 0.5, 1.52, r'$U_\mathrm{eff}$', fontsize=FS)
    ax.text(26.2, -0.42, r'$r$', fontsize=FS)
    r = np.linspace(7.15, 26.0, 400)
    U = 1.0 / r ** 4 - 8.0 / r ** 5
    U = U / U.max()                                            # max = 1 at r=10
    ax.plot(r, U, 'k-', lw=LW)
    vec(ax, (10.0, 0.0), (10.0, 1.0), lw=LW0, ms=7, style='<|-|>')
    ax.text(10.8, 0.52, r'$U_0$', fontsize=FS)
    ax.set_xlim(6.9, 26.5)
    ax.set_ylim(-1.4, 1.85)
    save(fig, 'fig20')


# ---------------------------------------------------------------- fig 21
def fig_21():
    """Small-angle scattering: refraction-like ray through a sphere."""
    fig, ax = new_ax(2.5, 2.35)
    ax.set_aspect('equal')
    a = 1.0
    O = (0.0, 0.0)
    f0d = 33.0
    f0 = np.radians(f0d)
    P1 = np.array([a * np.cos(f0), a * np.sin(f0)])
    rho = np.sin(f0)
    betad = 24.0
    beta = np.radians(betad)
    dch = np.radians(180.0 + f0d - betad)                     # chord direction
    dc = np.array([np.cos(dch), np.sin(dch)])
    t2 = -2 * np.dot(P1, dc)
    P2 = P1 + t2 * dc
    ax.add_patch(Circle(O, a, fill=False, lw=LW, ec='k'))
    ax.plot([O[0], 2.25], [O[1], O[1]], 'k--', lw=LW0)        # horizontal dashed
    ax.plot([O[0], 1.42 * P1[0]], [O[1], 1.42 * P1[1]], 'k--', lw=LW0)
    # radius arrow "a" toward lower left
    dira = np.radians(222.0)
    vec(ax, O, (a * np.cos(dira), a * np.sin(dira)), lw=LW0, ms=8)
    ax.text(0.44 * np.cos(dira) - 0.22, 0.44 * np.sin(dira) + 0.10,
            r'$a$', fontsize=FS)
    # incoming ray (no head at P1) + motion arrow
    ax.plot([2.25, P1[0]], [rho, rho], 'k-', lw=LW)
    vec(ax, (1.72, rho), (1.50, rho), lw=LW, ms=8)
    # chord + motion arrow along it
    ax.plot([P1[0], P2[0]], [P1[1], P2[1]], 'k-', lw=LW)
    pm = P1 + 0.42 * dc
    vec(ax, tuple(pm - 0.16 * dc), tuple(pm + 0.16 * dc), lw=LW, ms=8)
    # exit ray: azimuth of outward normal at P2 plus alpha
    n2 = P2 / np.linalg.norm(P2)
    azn = np.degrees(np.arctan2(n2[1], n2[0]))
    de = np.array([np.cos(np.radians(azn + f0d)), np.sin(np.radians(azn + f0d))])
    ax.plot([P2[0], P2[0] + 0.75 * de[0]], [P2[1], P2[1] + 0.75 * de[1]],
            'k-', lw=LW)
    pe = P2 + 0.40 * de
    vec(ax, tuple(pe - 0.14 * de), tuple(pe + 0.14 * de), lw=LW, ms=8)
    # rho
    vec(ax, (1.95, 0.0), (1.95, rho), lw=LW0, ms=7, style='<|-|>')
    ax.text(2.06, 0.14, r'$\rho$', fontsize=FS)
    # angles at P1
    arc(ax, P1, 0.30, 0, f0d)
    ax.text(P1[0] + 0.29, P1[1] + 0.08, r'$\alpha$', fontsize=FS)
    arc(ax, P1, 0.36, np.degrees(dch), 180.0 + f0d)
    ax.text(P1[0] - 0.52, P1[1] + 0.16, r'$\beta$', fontsize=FS)
    # phi0 at centre
    arc(ax, O, 0.52, 0, f0d)
    ax.text(0.62, 0.16, r'$\varphi_0$', fontsize=FS)
    # angles at P2: short thin radius line beyond the circle
    ax.plot([P2[0], P2[0] + 0.50 * n2[0]], [P2[1], P2[1] + 0.50 * n2[1]],
            'k-', lw=0.6)
    aze = np.degrees(np.arctan2(de[1], de[0]))
    azc = np.degrees(np.arctan2(dc[1], dc[0]))
    arc(ax, P2, 0.30, azn, aze)
    ax.text(P2[0] - 0.34, P2[1] + 0.16, r'$\alpha$', fontsize=FS)
    arc(ax, P2, 0.40, azn, azc)
    ax.text(P2[0] + 0.16, P2[1] + 0.14, r'$\beta$', fontsize=FS)
    ax.set_xlim(-2.0, 2.5)
    ax.set_ylim(-1.25, 1.35)
    save(fig, 'fig21')


# ---------------------------------------------------------------- fig 22
def fig_22():
    """Spring connecting point A to mass m moving along a line."""
    fig, ax = new_ax(1.95, 1.75)
    ax.set_aspect('equal')
    A = (1.72, 1.52)
    m = (0.55, 0.0)
    ax.plot([0.0, 2.55], [0, 0], 'k-', lw=LW0)                # the line
    ax.add_patch(Circle(m, 0.055, fc='k', ec='k'))
    _spring(ax, m, A, n=13, amp=0.055)
    ax.plot([A[0], A[0]], [0, A[1]], 'k--', lw=LW0)           # dashed vertical
    ax.text(A[0] + 0.10, A[1] - 0.02, r'$A$', fontsize=FS)
    ax.text(A[0] + 0.08, 0.70, r'$l$', fontsize=FS)
    ax.text(m[0] - 0.05, -0.28, r'$m$', fontsize=FS)
    ax.text(1.08, -0.28, r'$x$', fontsize=FS)
    ax.set_xlim(-0.12, 2.6)
    ax.set_ylim(-0.42, 1.68)
    save(fig, 'fig22')


# ---------------------------------------------------------------- fig 23
def fig_23():
    """Pendulum, suspension A joined to m by a spring; r, l, phi marked."""
    fig, ax = new_ax(1.8, 2.15)
    ax.set_aspect('equal')
    A = (0.0, 3.05)
    T = (0.0, 1.75)                 # top of the dashed circle
    P = (0.0, 0.0)                  # ground point (centre of dashed circle)
    azm = np.radians(66.0)
    M = (1.75 * np.cos(azm), 1.75 * np.sin(azm))
    # ground with hatching
    ax.plot([-0.30, 0.30], [0, 0], 'k-', lw=LW)
    for x in np.linspace(-0.27, 0.27, 8):
        ax.plot([x, x - 0.11], [0, -0.14], 'k-', lw=0.7)
    # rod from ground point to mass (plain line, no arrowhead)
    ax.plot([0.0, M[0]], [0.0, M[1]], 'k-', lw=LW)
    # vertical line A -> T with head at T (l), double arrow T -> P (r)
    vec(ax, A, T, lw=LW0, ms=8)
    vec(ax, T, (0.0, 0.012), lw=LW0, ms=7, style='<|-|>')
    # dashed circle arc around P through T and M
    th1 = np.degrees(np.arctan2(M[1], M[0]))
    arc(ax, P, 1.75, th1, 128.0)
    # spring A -> M with suspension mark at A
    _spring(ax, A, M, n=14, amp=0.075)
    ax.plot([A[0]], [A[1]], marker='<', ms=4, mfc='k', mec='k')
    ax.add_patch(Circle(M, 0.055, fc='k', ec='k'))
    # phi arc at the ground point
    arc(ax, P, 0.52, th1, 90.0)
    ax.text(0.10, 0.62, r'$\varphi$', fontsize=FS)
    ax.text(A[0] - 0.26, A[1] - 0.06, r'$A$', fontsize=FS)
    ax.text(-0.12, 2.35, r'$l$', fontsize=FS)
    ax.text(-0.14, 0.85, r'$r$', fontsize=FS)
    ax.text(M[0] + 0.11, M[1] + 0.02, r'$m$', fontsize=FS)
    ax.set_xlim(-0.55, 1.9)
    ax.set_ylim(-0.42, 3.25)
    save(fig, 'fig23')


# ---------------------------------------------------------------- figs 24-27
def _axes_Ft(ax, xmax=2.15, ymax=1.5, xmin=-0.28):
    ax.plot([xmin, xmax], [0, 0], 'k-', lw=LW0)
    ax.plot([0, 0], [0, ymax], 'k-', lw=LW0)
    ax.text(xmax - 0.02, -0.26, r'$t$', fontsize=FS, ha='right')
    ax.text(0.07, ymax - 0.06, r'$F$', fontsize=FS)
    ax.text(-0.04, -0.26, r'$O$', fontsize=FS, ha='right')


def fig_24():
    """F = F0 t / T ramp, then constant F0 (fig 24)."""
    fig, ax = new_ax(1.7, 1.35)
    _axes_Ft(ax)
    T, F0 = 1.0, 1.0
    ax.plot([0, T, 2.0], [0, F0, F0], 'k-', lw=LW)
    ax.plot([T, T], [0, F0], 'k--', lw=LW0)
    ax.text(T, -0.26, r'$T$', fontsize=FS, ha='center')
    ax.text(T + 0.07, 0.52, r'$F_0$', fontsize=FS)
    ax.set_xlim(-0.3, 2.2)
    ax.set_ylim(-0.42, 1.55)
    save(fig, 'fig24')


def fig_25():
    """Rectangular pulse F0 during 0<t<T (fig 25)."""
    fig, ax = new_ax(1.7, 1.35)
    _axes_Ft(ax)
    T, F0 = 1.0, 1.0
    ax.plot([0, T, T], [F0, F0, 0], 'k-', lw=LW)
    ax.text(T, -0.26, r'$T$', fontsize=FS, ha='center')
    ax.text(-0.07, 0.80, r'$F_0$', fontsize=FS, ha='right')
    ax.set_xlim(-0.3, 2.2)
    ax.set_ylim(-0.42, 1.55)
    save(fig, 'fig25')


def fig_26():
    """Triangular pulse F = F0 t/T, drop at T (fig 26)."""
    fig, ax = new_ax(1.7, 1.35)
    _axes_Ft(ax)
    T, F0 = 1.0, 1.0
    ax.plot([0, T, T], [0, F0, 0], 'k-', lw=LW)
    ax.text(T, -0.26, r'$T$', fontsize=FS, ha='center')
    ax.text(T + 0.07, 0.52, r'$F_0$', fontsize=FS)
    ax.set_xlim(-0.3, 2.2)
    ax.set_ylim(-0.42, 1.55)
    save(fig, 'fig26')


def fig_27():
    """F = F0 sin(wt) pulse over one period (fig 27)."""
    fig, ax = new_ax(1.7, 1.3)
    _axes_Ft(ax, xmax=1.55, ymax=1.42, xmin=-0.25)
    T = 1.0
    t = np.linspace(0, T, 200)
    ax.plot(t, np.sin(2 * np.pi * t / T), 'k-', lw=LW)
    ax.text(T + 0.04, 0.08, r'$T$', fontsize=FS)
    ax.set_xlim(-0.28, 1.6)
    ax.set_ylim(-1.35, 1.5)
    save(fig, 'fig27')


if __name__ == '__main__':
    import sys
    wanted = sys.argv[1:] if len(sys.argv) > 1 else []
    funcs = {k: v for k, v in list(globals().items())
             if callable(v) and k.startswith('fig_')}
    for name, fn in sorted(funcs.items(), key=lambda kv: int(kv[0].split('_')[1])):
        if wanted and name.split('_')[1] not in wanted:
            continue
        fn()
