# -*- coding: utf-8 -*-
"""朗道《力学》卷1 插图重绘 批次 B4：图43-图56（刚体运动几何图 + 第七章图）。
风格合同见 插图规范.md：黑白、Times/mathtext-cm、主体实线/辅助虚线、'-|>'自绘箭头。"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse, Circle, Polygon
from matplotlib.lines import Line2D
import numpy as np

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

OUT = r"E:/AI整理书籍/朗道理论物理教程/卷1力学/重排本/figures"
PRE = OUT + "/preview"
DASH = (0, (6, 3))
DASHDOT = (0, (7, 2.6, 1.4, 2.6))


def new_ax(w, h, xlim, ylim):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect('equal'); ax.axis('off')
    return fig, ax


def save(fig, n):
    fig.savefig(f"{OUT}/fig{n}.pdf", bbox_inches='tight', pad_inches=0.03)
    fig.savefig(f"{PRE}/fig{n}.png", dpi=200, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


def arrow(ax, p0, p1, lw=1.1, ms=9, z=3):
    ax.annotate('', xy=tuple(p1), xytext=tuple(p0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0), zorder=z)


def darrow(ax, p0, p1, lw=1.0, ls=DASH, ms=9):
    """虚/点划线杆 + 实心箭头头部"""
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float)
    d = p1 - p0
    ax.add_line(Line2D([p0[0], p1[0] - .04 * d[0]], [p0[1], p1[1] - .04 * d[1]],
                       color='k', lw=lw, ls=ls, zorder=2.4))
    arrow(ax, p1 - .10 * d, p1, lw=lw, ms=ms)


def hatch_along(ax, p0, p1, side, n=14, L=0.09, lw=0.7):
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float)
    for t in np.linspace(0.02, 0.98, n):
        q = p0 + t * (p1 - p0)
        ax.add_line(Line2D([q[0], q[0] + side[0] * L], [q[1], q[1] + side[1] * L],
                           color='k', lw=lw))


def clip_patch(ax, patch):
    patch.set_facecolor('none'); patch.set_edgecolor('none')
    ax.add_patch(patch)
    return patch


def hatch_region(ax, patch, spacing=0.085, slant=(0.42, 1.0), ext=1.2, lw=0.55):
    s = np.asarray(slant, float); s = s / np.linalg.norm(s)
    nv = np.array([-s[1], s[0]])
    for q in np.arange(-2.4, 2.4, spacing):
        ln = Line2D([q * nv[0] - ext * s[0], q * nv[0] + ext * s[0]],
                    [q * nv[1] - ext * s[1], q * nv[1] + ext * s[1]],
                    color='k', lw=lw, zorder=2.05)
        ln.set_clip_path(patch)
        ax.add_line(ln)


def ell_pt(c, a, b, ang, t):
    ca, sa = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    ct, st = np.cos(np.radians(t)), np.sin(np.radians(t))
    return np.array([c[0] + a * ct * ca - b * st * sa,
                     c[1] + a * ct * sa + b * st * ca])


def tangents(P, c, a, b, ang):
    """外点 P 到椭圆(c,a,b,ang)的上、下切点参数"""
    ts = np.linspace(0, 360, 4001)
    pts = np.array([ell_pt(c, a, b, ang, t) for t in ts])
    d = pts - np.asarray(P, float)
    angp = np.arctan2(d[:, 1], d[:, 0])
    return ts[np.argmax(angp)], ts[np.argmin(angp)]


def arc_pts(c, r, t0, t1, k=1.0, n=60):
    ts = np.radians(np.linspace(t0, t1, n))
    return np.array([c[0] + r * np.cos(ts), c[1] + r * k * np.sin(ts)]).T


def ang_norm(a):
    """归一到 (-180,180]"""
    return (a + 180) % 360 - 180


def bezier(p0, p1, p2, p3, n=40):
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 +
            3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)


def draw_poly(ax, pts, lw=1.0, ls='-', z=2.0):
    ax.add_line(Line2D(pts[:, 0], pts[:, 1], color='k', lw=lw, ls=ls, zorder=z,
                       solid_capstyle='round'))


# ---------------------------------------------------------------- 图43
def fig_43():
    fig, ax = new_ax(3.4, 2.0, (-1.65, 3.55), (-1.35, 1.38))
    P = np.array([0., 0.]); O = np.array([0., 0.55])
    A = np.array([2.67, -1.03])
    C = np.array([2.82, -0.61])
    ea, eb, eang = 0.30, 0.38, -23.0

    ax.add_line(Line2D([P[0], A[0]], [P[1], A[1]], color='k', lw=0.9, ls=DASH, zorder=1.5))
    th = arc_pts(P, 0.70, -142.0, -21.0, n=60)
    draw_poly(ax, th, lw=0.9, z=1.6)
    ax.text(0.02, -0.98, r'$\theta$', fontsize=11)

    ax.add_line(Line2D([0, 2.62], [0, 0], color='k', lw=1.0, ls=DASHDOT, zorder=1.4))
    arrow(ax, (2.60, 0), (3.25, 0), lw=1.0)
    ax.text(3.28, -0.15, r'$Y$', fontsize=11)
    arrow(ax, P, (-1.28, -0.97), lw=1.0)
    ax.text(-1.46, -1.02, r'$X$', fontsize=11)
    ax.add_line(Line2D([0, 0], [0, 0.55], color='k', lw=1.0, zorder=1.4))
    arrow(ax, O, (0, 1.24), lw=1.0)
    ax.text(0.07, 1.12, r'$Z$', fontsize=11)
    ax.text(-0.18, 0.50, r'$O$', fontsize=11)

    t_up, t_lo = tangents(O, C, ea, eb, eang)
    Tup, Alo = ell_pt(C, ea, eb, eang, t_up), ell_pt(C, ea, eb, eang, t_lo)
    ts = np.linspace(0, 360, 721)
    tops = np.array([ell_pt(C, ea, eb, eang, t) for t in ts])
    Ttop = tops[np.argmax(tops[:, 1])]
    u = (C - O) / np.linalg.norm(C - O)
    ax.add_line(Line2D([O[0], Ttop[0]], [O[1], Ttop[1]], color='k', lw=0.9, ls=DASH, zorder=1.6))
    ax.add_line(Line2D([O[0], C[0] + 0.40 * u[0]], [O[1], C[1] + 0.40 * u[1]],
                       color='k', lw=0.9, ls=DASHDOT, zorder=1.6))
    for T in (Tup, Alo):
        ax.add_line(Line2D([O[0], T[0]], [O[1], T[1]], color='k', lw=1.6, zorder=2.5))
    ax.add_patch(Ellipse(C, 2 * ea, 2 * eb, angle=eang, fill=False, lw=1.6, zorder=2.6))
    ax.text(A[0] - 0.10, A[1] - 0.20, r'$A$', fontsize=11)

    a_axis = np.degrees(np.arctan2(u[1], u[0]))
    a_sil = np.degrees(np.arctan2(Tup[1] - O[1], Tup[0] - O[0]))
    al = arc_pts(O, 0.53, a_axis, a_sil, n=30)
    draw_poly(ax, al, lw=0.9, z=2.7)
    ax.text(0.68, 0.52, r'$\alpha$', fontsize=11)
    save(fig, 43)


# ---------------------------------------------------------------- 图44
def fig_44():
    fig, ax = new_ax(2.6, 2.15, (-1.95, 1.95), (-1.85, 1.10))
    ax.add_patch(Ellipse((0, 0), 2.10, 1.10, fill=False, lw=1.5, zorder=2.5))
    ax.add_patch(Ellipse((0, 0), 2.10, 0.72, fill=False, lw=0.8, ls=DASH, zorder=1.8))
    ax.add_patch(Ellipse((0, 0), 0.76, 1.10, fill=False, lw=0.8, ls=DASH, zorder=1.8))
    ax.add_line(Line2D([-1.55, -1.05], [0, 0], color='k', lw=1.2, zorder=2.2))
    ax.add_line(Line2D([-1.05, 1.05], [0, 0], color='k', lw=0.9, ls=DASH, zorder=2.1))
    ax.add_line(Line2D([1.05, 1.55], [0, 0], color='k', lw=1.2, zorder=2.2))
    ax.text(-1.76, -0.02, r'$A$', fontsize=11)
    ax.text(1.63, -0.02, r'$B$', fontsize=11)
    ax.add_line(Line2D([-1.55, -1.55, 1.55, 1.55], [0, -0.76, -0.76, 0],
                       color='k', lw=1.2, zorder=2.0))
    ax.add_line(Line2D([0, 0], [1.00, -0.55], color='k', lw=0.9, ls=DASHDOT, zorder=1.9))
    ax.add_line(Line2D([0, 0], [-0.55, -1.64], color='k', lw=1.2, zorder=2.2))
    ax.text(0.05, 0.88, r'$D$', fontsize=11)
    ax.text(-0.26, -1.12, r'$C$', fontsize=11)
    # theta_dot 环绕箭头（绕竖轴下端）
    t = np.radians(np.linspace(125, 350, 80))
    ax.add_line(Line2D(0.20 * np.cos(t), -1.42 + 0.20 * np.sin(t), color='k', lw=1.0, zorder=2.2))
    arrow(ax, (0.20 * np.cos(np.radians(341)), -1.42 + 0.20 * np.sin(np.radians(341))),
          (0.20 * np.cos(np.radians(356)), -1.42 + 0.20 * np.sin(np.radians(356))), lw=1.0, ms=8)
    ax.text(0.14, -1.20, r'$\dot\theta$', fontsize=11)
    # phi_dot 环绕箭头（绕 AB，靠近 B）
    t = np.radians(np.linspace(-75, 195, 80))
    ax.add_line(Line2D(1.28 + 0.10 * np.cos(t), 0.26 * np.sin(t), color='k', lw=1.0, zorder=2.4))
    arrow(ax, (1.28 + 0.10 * np.cos(np.radians(186)), 0.26 * np.sin(np.radians(186))),
          (1.28 + 0.10 * np.cos(np.radians(197)), 0.26 * np.sin(np.radians(197))), lw=1.0, ms=8)
    ax.text(1.13, 0.44, r'$\dot\varphi$', fontsize=11)
    save(fig, 44)


# ---------------------------------------------------------------- 图45
def fig_45():
    fig, ax = new_ax(2.9, 2.2, (-1.80, 1.85), (-1.55, 1.20))
    ang = 22.0
    ca, sa = np.cos(np.radians(ang)), np.sin(np.radians(ang))
    d = np.array([ca, sa])
    A = np.array([-1.30, -0.48]); B = np.array([1.54, 0.58])
    ctr = (A + B) / 2 + 0.08 * d + np.array([0.0, 0.10])
    ax.add_patch(Ellipse(ctr, 1.90, 1.00, angle=ang, fill=False, lw=1.5, zorder=2.5))
    ax.add_patch(Ellipse(ctr, 1.90, 0.65, angle=ang, fill=False, lw=0.8, ls=DASH, zorder=1.8))
    ax.add_patch(Ellipse(ctr, 0.70, 1.00, angle=ang, fill=False, lw=0.8, ls=DASH, zorder=1.8))
    eL, eR = ctr - 0.95 * d, ctr + 0.95 * d
    ax.add_line(Line2D([A[0], eL[0]], [A[1], eL[1]], color='k', lw=1.2, zorder=2.2))
    ax.add_line(Line2D([eL[0], eR[0]], [eL[1], eR[1]], color='k', lw=0.9, ls=DASH, zorder=2.1))
    ax.add_line(Line2D([eR[0], B[0]], [eR[1], B[1]], color='k', lw=1.2, zorder=2.2))
    ax.text(A[0] - 0.17, A[1] - 0.10, r'$A$', fontsize=11)
    ax.text(B[0] + 0.08, B[1] + 0.02, r'$B$', fontsize=11)
    ax.add_line(Line2D([A[0], A[0] + 0.62], [A[1], A[1]], color='k', lw=0.8, ls=DASH, zorder=1.8))
    al = arc_pts(A, 0.50, 0.0, ang, n=30)
    draw_poly(ax, al, lw=0.9, z=2.3)
    ax.text(A[0] + 0.60, A[1] + 0.09, r'$\alpha$', fontsize=11)
    ax.add_line(Line2D([A[0], A[0], B[0], B[0]], [A[1], -0.88, -0.88, B[1]],
                       color='k', lw=1.2, zorder=2.0))
    ax.add_line(Line2D([0, 0], [1.06, -0.88], color='k', lw=0.9, ls=DASHDOT, zorder=1.9))
    ax.add_line(Line2D([0, 0], [-0.88, -1.20], color='k', lw=1.2, zorder=2.2))
    ax.text(0.05, 0.97, r'$D$', fontsize=11)
    ax.text(0.06, -0.76, r'$C$', fontsize=11)
    t = np.radians(np.linspace(125, 350, 80))
    ax.add_line(Line2D(0.18 * np.cos(t), -1.38 + 0.18 * np.sin(t), color='k', lw=1.0, zorder=2.2))
    arrow(ax, (0.18 * np.cos(np.radians(341)), -1.38 + 0.18 * np.sin(np.radians(341))),
          (0.18 * np.cos(np.radians(356)), -1.38 + 0.18 * np.sin(np.radians(356))), lw=1.0, ms=8)
    ax.text(0.13, -1.16, r'$\dot\theta$', fontsize=11)
    cc = B - 0.16 * d
    t = np.radians(np.linspace(-75, 195, 80))
    xs = cc[0] + 0.10 * np.cos(t) * ca - 0.26 * np.sin(t) * sa
    ys = cc[1] + 0.10 * np.cos(t) * sa + 0.26 * np.sin(t) * ca
    ax.add_line(Line2D(xs, ys, color='k', lw=1.0, zorder=2.4))
    arrow(ax, (cc[0] + 0.10 * np.cos(np.radians(186)) * ca - 0.26 * np.sin(np.radians(186)) * sa,
               cc[1] + 0.10 * np.cos(np.radians(186)) * sa + 0.26 * np.sin(np.radians(186)) * ca),
          (cc[0] + 0.10 * np.cos(np.radians(197)) * ca - 0.26 * np.sin(np.radians(197)) * sa,
           cc[1] + 0.10 * np.cos(np.radians(197)) * sa + 0.26 * np.sin(np.radians(197)) * ca),
          lw=1.0, ms=8)
    ax.text(B[0] - 0.34, B[1] + 0.28, r'$\dot\varphi$', fontsize=11)
    save(fig, 45)


# ---------------------------------------------------------------- 图46
def fig_46():
    fig, ax = new_ax(2.7, 2.9, (-1.75, 1.85), (-0.85, 2.95))
    O = np.array([0., 0.])
    d3 = np.array([np.cos(np.radians(50)), np.sin(np.radians(50))])
    n3 = np.array([-d3[1], d3[0]])
    # 陀螺体：沿 x3 的双弧透镜体（尖端 ±0.95d3，半宽 0.45）
    Lb, Wb = 0.95, 0.45
    Rarc = (Lb ** 2 + Wb ** 2) / (2 * Wb)
    t = np.linspace(-np.arcsin(Lb / Rarc), np.arcsin(Lb / Rarc), 80)
    arc1 = np.array([Rarc * np.sin(t), Wb - Rarc + Rarc * np.cos(t)]).T   # 上弧（凸 +n3）
    arc2 = np.array([Rarc * np.sin(t), -(Wb - Rarc + Rarc * np.cos(t))]).T  # 下弧
    lens = np.vstack([arc1 @ np.vstack([d3, n3]).T, arc2[::-1] @ np.vstack([d3, n3]).T])
    body = Polygon(lens, closed=True, facecolor='white', edgecolor='k', lw=1.3, zorder=2.0)
    ax.add_patch(body)
    hatch_region(ax, clip_patch(ax, Polygon(lens, closed=True)),
                 spacing=0.10, slant=(0.35, 1.0), ext=1.2)
    # 体内 x3 点划轴线段
    ax.add_line(Line2D([-Lb * d3[0], 1.31 * d3[0]], [-Lb * d3[1], 1.31 * d3[1]],
                       color='k', lw=0.9, ls=DASHDOT, zorder=2.3))
    # M 竖直线（两个箭头）
    ax.add_line(Line2D([0, 0], [0, 2.62], color='k', lw=1.3, zorder=2.6))
    arrow(ax, (0, 2.48), (0, 2.74), lw=1.3, ms=11)
    arrow(ax, (0, 1.16), (0, 1.44), lw=1.3, ms=11)
    ax.text(-0.16, 2.78, r'$\boldsymbol{M}$', fontsize=11)
    ax.text(-0.76, 1.06, r'$\boldsymbol{\Omega}_{\rm pr}$', fontsize=11)
    # 进动锥底椭圆：后半点划，前半实线
    t = np.linspace(0, 180, 90)
    ax.add_line(Line2D(1.45 * np.cos(np.radians(t)), 1.36 + 0.44 * np.sin(np.radians(t)),
                       color='k', lw=0.9, ls=DASHDOT, zorder=1.7))
    t = np.linspace(180, 360, 90)
    ax.add_line(Line2D(1.45 * np.cos(np.radians(t)), 1.36 + 0.44 * np.sin(np.radians(t)),
                       color='k', lw=1.1, zorder=1.8))
    ax.text(1.52, 1.42, r'$x_3$', fontsize=11)
    # x3 轴箭头（至锥底右端）
    ax.add_line(Line2D([0, 1.98 * d3[0] - 0.14 * d3[0]], [0, 1.98 * d3[1] - 0.14 * d3[1]],
                       color='k', lw=1.1, zorder=2.4))
    arrow(ax, 1.90 * d3, 1.98 * d3, lw=1.1, ms=10)
    # Omega 粗箭头与分解（竖直虚线落到 x3 线上）
    Om = np.array([0.84, 2.74])
    ax.add_line(Line2D([0, Om[0] * .94], [0, Om[1] * .94], color='k', lw=1.7, zorder=2.6))
    arrow(ax, Om * .94, Om, lw=1.7, ms=12)
    ax.text(Om[0] + 0.10, Om[1] + 0.02, r'$\boldsymbol{\Omega}$', fontsize=11)
    Q = Om[0] / d3[0] * d3
    arrow(ax, Q - 0.10 * d3, Q + 0.03 * d3, lw=1.1, ms=9)
    ax.add_line(Line2D([Q[0], Om[0]], [Q[1], Om[1]], color='k', lw=0.8, ls=DASH, zorder=1.9))
    # theta 弧 + 引线
    th = arc_pts(O, 0.34, 50, 115, n=40)
    draw_poly(ax, th, lw=0.9, z=2.7)
    arrow(ax, (0.34 * np.cos(np.radians(110)), 0.34 * np.sin(np.radians(110))),
          (0.34 * np.cos(np.radians(117)), 0.34 * np.sin(np.radians(117))), lw=0.9, ms=8)
    ax.plot([-0.46, -0.24], [0.60, 0.30], color='k', lw=0.7, zorder=2.7)
    ax.text(-0.60, 0.64, r'$\theta$', fontsize=11)
    # x1 点划轴
    u1 = np.array([np.cos(np.radians(140)), np.sin(np.radians(140))])
    ax.add_line(Line2D([0, 1.15 * u1[0]], [0, 1.15 * u1[1]], color='k', lw=0.9, ls=DASHDOT, zorder=2.3))
    ax.text(1.20 * u1[0] - 0.16, 1.20 * u1[1] + 0.05, r'$x_1$', fontsize=11)
    save(fig, 46)


# ---------------------------------------------------------------- 图47
def fig_47():
    fig, ax = new_ax(3.6, 3.1, (-3.85, 4.45), (-2.50, 4.10))
    O = np.array([0., 0.])
    # 赤道面椭圆：左半点划、右半实线
    t = np.linspace(90, 270, 120)
    ax.add_line(Line2D(2.77 * np.cos(np.radians(t)), 1.45 * np.sin(np.radians(t)),
                       color='k', lw=1.0, ls=DASHDOT, zorder=1.6))
    t = np.linspace(-90, 90, 120)
    ax.add_line(Line2D(2.77 * np.cos(np.radians(t)), 1.45 * np.sin(np.radians(t)),
                       color='k', lw=1.2, zorder=1.7))
    # 动平面 (x1,x2)：以 x1、x2 投影方向为共轭直径的椭圆
    e1 = 1.95 * np.array([np.cos(np.radians(-10.4)), np.sin(np.radians(-10.4))])
    e2 = 2.55 * np.array([np.cos(np.radians(68)), np.sin(np.radians(68))])
    ph = np.linspace(0, 2 * np.pi, 241)
    body = np.array([c * e1 + s * e2 for c, s in zip(np.cos(ph), np.sin(ph))])
    draw_poly(ax, body, lw=1.2, z=1.8)
    # 节线方向 = 两椭圆交点（取右下者）
    f = (body[:, 0] / 2.77) ** 2 + (body[:, 1] / 1.45) ** 2 - 1
    cand = []
    for i in range(len(ph) - 1):
        if f[i] == 0 or f[i] * f[i + 1] < 0:
            g = np.linspace(ph[i], ph[i + 1], 20)
            ff = ((np.cos(g) * e1[0] + np.sin(g) * e2[0]) / 2.77) ** 2 + \
                 ((np.cos(g) * e1[1] + np.sin(g) * e2[1]) / 1.45) ** 2 - 1
            j = np.argmin(np.abs(ff))
            cand.append(np.array([np.cos(g[j]) * e1[0] + np.sin(g[j]) * e2[0],
                                  np.cos(g[j]) * e1[1] + np.sin(g[j]) * e2[1]]))
    Ndir = min(cand, key=lambda p: np.degrees(np.arctan2(p[1], p[0])) + 90)
    uN = Ndir / np.linalg.norm(Ndir)
    # 固定轴
    arrow(ax, O, (0, 3.90), lw=1.1, ms=10)
    ax.text(0.10, 3.78, r'$Z$', fontsize=11)
    arrow(ax, O, (4.05, 0), lw=1.1, ms=10)
    ax.text(3.88, -0.42, r'$Y$', fontsize=11)
    ax.add_line(Line2D([0, -1.25], [0, -1.75], color='k', lw=1.2, zorder=2.0))
    ax.text(-1.44, -1.70, r'$X$', fontsize=11)
    # 动轴
    x3d = np.array([np.cos(np.radians(152)), np.sin(np.radians(152))])
    ax.add_line(Line2D([0, 3.35 * x3d[0]], [0, 3.35 * x3d[1]], color='k', lw=1.2, zorder=2.2))
    arrow(ax, 3.30 * x3d, 3.52 * x3d, lw=1.2, ms=10)
    ax.text(3.60 * x3d[0] - 0.12, 3.60 * x3d[1] + 0.06, r'$x_3$', fontsize=11)
    x1d = np.array([np.cos(np.radians(-10.4)), np.sin(np.radians(-10.4))])
    ax.add_line(Line2D([0, 1.90 * x1d[0]], [0, 1.90 * x1d[1]], color='k', lw=1.0, ls=DASHDOT, zorder=2.0))
    ax.text(2.00 * x1d[0], 2.00 * x1d[1] - 0.14, r'$x_1$', fontsize=11)
    x2d = np.array([np.cos(np.radians(68)), np.sin(np.radians(68))])
    ax.add_line(Line2D([0, 2.48 * x2d[0]], [0, 2.48 * x2d[1]], color='k', lw=0.9, ls=DASH, zorder=2.0))
    ax.text(2.56 * x2d[0], 2.56 * x2d[1], r'$x_2$', fontsize=11)
    # 节线 ON（点划直线穿过 O，N 端箭头）
    ax.add_line(Line2D([-1.55 * uN[0], 1.88 * uN[0]], [-1.55 * uN[1], 1.88 * uN[1]],
                       color='k', lw=1.0, ls=DASHDOT, zorder=2.1))
    arrow(ax, 1.72 * uN, 1.95 * uN, lw=1.0, ms=10)
    ax.text(2.04 * uN[0] + 0.06, 2.04 * uN[1] - 0.04, r'$N$', fontsize=11)
    # theta 弧（Z 与 x3 间）
    th = arc_pts(O, 0.95, 90, 152, n=40)
    draw_poly(ax, th, lw=1.0, z=2.4)
    arrow(ax, 0.95 * np.array([np.cos(np.radians(147)), np.sin(np.radians(147))]),
          0.95 * np.array([np.cos(np.radians(153)), np.sin(np.radians(153))]), lw=1.0, ms=9)
    ax.text(-0.72, 1.10, r'$\theta$', fontsize=11)
    # phi 弧（X 到 ON，赤道面内压扁弧）
    aON = np.degrees(np.arctan2(uN[1], uN[0]))
    ph2 = arc_pts(O, 1.50, -125, aON, k=0.52, n=50)
    draw_poly(ax, ph2, lw=1.0, z=2.4)
    arrow(ax, np.array([1.50 * np.cos(np.radians(aON - 6)), 0.52 * 1.50 * np.sin(np.radians(aON - 6))]),
          np.array([1.50 * np.cos(np.radians(aON)), 0.52 * 1.50 * np.sin(np.radians(aON))]), lw=1.0, ms=9)
    ax.text(-0.16, -1.12, r'$\varphi$', fontsize=11)
    # psi 弧（ON 到 x1）
    aX1 = -10.4
    ps = arc_pts(O, 0.95, aON, aX1, k=0.52, n=40)
    draw_poly(ax, ps, lw=1.0, z=2.4)
    arrow(ax, np.array([0.95 * np.cos(np.radians(aX1 + 6)), 0.52 * 0.95 * np.sin(np.radians(aX1 + 6))]),
          np.array([0.95 * np.cos(np.radians(aX1)), 0.52 * 0.95 * np.sin(np.radians(aX1))]), lw=1.0, ms=9)
    am = np.radians(ang_norm(aON + aX1) / 2)
    ax.text(1.18 * np.cos(am) + 0.04, 0.52 * 1.18 * np.sin(am), r'$\psi$', fontsize=11)
    # phi_dot 绕 Z
    t = np.linspace(-40, 215, 60)
    ax.add_line(Line2D(0.30 * np.cos(np.radians(t)), 3.30 + 0.10 * np.sin(np.radians(t)),
                       color='k', lw=0.9, zorder=2.4))
    arrow(ax, (0.30 * np.cos(np.radians(206)), 3.30 + 0.10 * np.sin(np.radians(206))),
          (0.30 * np.cos(np.radians(217)), 3.30 + 0.10 * np.sin(np.radians(217))), lw=0.9, ms=8)
    ax.text(0.38, 3.40, r'$\dot\varphi$', fontsize=11)
    # psi_dot 绕 x3（小环：长轴垂直 x3）
    c3 = 2.0 * x3d
    t = np.linspace(-60, 205, 60)
    xs = c3[0] + 0.27 * np.cos(np.radians(t)) * x3d[1] - 0.09 * np.sin(np.radians(t)) * x3d[0]
    ys = c3[1] - 0.27 * np.cos(np.radians(t)) * x3d[0] - 0.09 * np.sin(np.radians(t)) * x3d[1]
    ax.add_line(Line2D(xs, ys, color='k', lw=0.9, zorder=2.4))
    arrow(ax, (xs[-3], ys[-3]), (xs[-1], ys[-1]), lw=0.9, ms=8)
    ax.text(c3[0] - 0.85, c3[1] + 0.42, r'$\dot\psi$', fontsize=11)
    # theta_dot 绕 ON（近 N 处）
    cN = 1.42 * uN
    t = np.linspace(-60, 205, 60)
    xs = cN[0] + 0.22 * np.cos(np.radians(t)) * uN[1] - 0.08 * np.sin(np.radians(t)) * uN[0]
    ys = cN[1] - 0.22 * np.cos(np.radians(t)) * uN[0] - 0.08 * np.sin(np.radians(t)) * uN[1]
    ax.add_line(Line2D(xs, ys, color='k', lw=0.9, zorder=2.4))
    arrow(ax, (xs[-3], ys[-3]), (xs[-1], ys[-1]), lw=0.9, ms=8)
    ax.text(cN[0] - 0.10, cN[1] - 0.42, r'$\dot\theta$', fontsize=11)
    ax.text(-0.16, -0.32, r'$O$', fontsize=11)
    save(fig, 47)


# ---------------------------------------------------------------- 图48
def fig_48():
    fig, ax = new_ax(2.7, 2.4, (-1.45, 1.55), (-0.85, 1.80))
    O = np.array([0., 0.])
    x3 = np.radians(125.4)
    d3 = np.array([np.cos(x3), np.sin(x3)])
    n3 = np.array([-d3[1], d3[0]])
    Lb, Wb = 1.14, 0.19
    # 泪滴形：两段三次贝塞尔（尖端的 O，圆头的远端）
    s1 = bezier(O, O + 0.42 * d3 + 0.24 * n3, O + 0.95 * d3 + 0.185 * n3, O + Lb * d3, 50)
    s2 = bezier(O, O + 0.42 * d3 - 0.24 * n3, O + 0.95 * d3 - 0.185 * n3, O + Lb * d3, 50)
    body_pts = np.vstack([s1, s2[::-1]])
    ax.add_patch(Polygon(body_pts, closed=True, facecolor='white', edgecolor='k',
                         lw=1.3, zorder=2.0))
    hatch_region(ax, clip_patch(ax, Polygon(body_pts, closed=True)),
                 spacing=0.075, slant=(0.35, 1.0), ext=0.8)
    # 轴
    arrow(ax, O, (0, 1.58), lw=1.1, ms=10)
    ax.text(0.06, 1.52, r'$Z$', fontsize=11)
    arrow(ax, O, (1.58, 0), lw=1.1, ms=10)
    ax.text(1.50, 0.10, r'$Y$', fontsize=11)
    arrow(ax, O, (-0.98, -0.63), lw=1.1, ms=10)
    ax.text(-1.16, -0.66, r'$X$', fontsize=11)
    arrow(ax, O, 1.52 * d3, lw=1.1, ms=10)
    ax.text(1.62 * d3[0] - 0.02, 1.62 * d3[1] + 0.05, r'$x_3$', fontsize=11)
    x2 = np.array([np.cos(np.radians(48)), np.sin(np.radians(48))])
    arrow(ax, O, 1.52 * x2, lw=1.1, ms=10)
    ax.text(1.62 * x2[0], 1.62 * x2[1] - 0.04, r'$x_2$', fontsize=11)
    x1 = np.array([np.cos(np.radians(-23)), np.sin(np.radians(-23))])
    arrow(ax, O, 1.38 * x1, lw=1.1, ms=10)
    ax.text(1.46 * x1[0], 1.46 * x1[1] + 0.04, r'$x_1$', fontsize=11)
    uN = np.array([np.cos(np.radians(-73)), np.sin(np.radians(-73))])
    arrow(ax, O, 1.02 * uN, lw=1.1, ms=10)
    ax.text(1.10 * uN[0] + 0.03, 1.10 * uN[1], r'$N$', fontsize=11)
    # 重力：l 处竖直虚箭头
    pl = 0.60 * d3
    darrow(ax, pl + (0, -0.10), pl + (0, -0.58), lw=0.9)
    ax.text(pl[0] - 0.22, pl[1] - 0.64, r'$\mu g$', fontsize=11)
    ax.text(pl[0] + 0.05, pl[1] + 0.03, r'$l$', fontsize=11)
    # theta 弧
    th = arc_pts(O, 0.34, 90, 125.4, n=30)
    draw_poly(ax, th, lw=0.9, z=2.5)
    arrow(ax, 0.34 * np.array([np.cos(np.radians(120)), np.sin(np.radians(120))]),
          0.34 * np.array([np.cos(np.radians(127)), np.sin(np.radians(127))]), lw=0.9, ms=8)
    ax.text(-0.14, 0.58, r'$\theta$', fontsize=11)
    # phi 弧（X 到 N，压扁）
    ph2 = arc_pts(O, 0.55, -147, -73, k=0.52, n=40)
    draw_poly(ax, ph2, lw=0.9, z=2.5)
    arrow(ax, np.array([0.55 * np.cos(np.radians(-79)), 0.52 * 0.55 * np.sin(np.radians(-79))]),
          np.array([0.55 * np.cos(np.radians(-72)), 0.52 * 0.55 * np.sin(np.radians(-72))]), lw=0.9, ms=8)
    ax.text(-0.28, -0.42, r'$\varphi$', fontsize=11)
    # psi 弧（N 到 x1）
    ps = arc_pts(O, 0.55, -73, -23, k=0.52, n=40)
    draw_poly(ax, ps, lw=0.9, z=2.5)
    arrow(ax, np.array([0.55 * np.cos(np.radians(-29)), 0.52 * 0.55 * np.sin(np.radians(-29))]),
          np.array([0.55 * np.cos(np.radians(-22)), 0.52 * 0.55 * np.sin(np.radians(-22))]), lw=0.9, ms=8)
    ax.text(0.60, -0.38, r'$\psi$', fontsize=11)
    ax.text(0.15, 0.50, r'$O$', fontsize=11)
    save(fig, 48)



# ---------------------------------------------------------------- 图49
def _sphere_panel(ax, cx, kind):
    R, beta = 1.0, np.radians(20)
    ax.add_line(Line2D([cx, cx], [-1.38, 1.38], color='k', lw=0.9, zorder=1.5))
    ax.add_patch(Circle((cx, 0), R, facecolor='white', edgecolor='k', lw=1.0, zorder=1.8))
    th1, th2 = np.radians(74), np.radians(39)

    def lat(th):
        cy = np.cos(th) * np.cos(beta)
        rx, ry = np.sin(th), np.sin(th) * np.sin(beta)
        t = np.linspace(np.pi, 2 * np.pi, 80)
        return cx + rx * np.cos(t), cy + ry * np.sin(t)

    for th, lab, lx, ly in ((th2, r'$\theta_2$', 0.88, 1.10), (th1, r'$\theta_1$', 1.04, 0.22)):
        xs, ys = lat(th)
        ax.add_line(Line2D(xs, ys, color='k', lw=0.9, zorder=2.0))
        ax.text(cx + lx, ly, lab, fontsize=10)

    thm, Amp = (th1 + th2) / 2, (th2 - th1) / 2
    if kind == 'a':      # theta1 处尖点
        th_f = lambda w: thm - Amp * np.cos(w)
        s_f = lambda w: w - np.sin(w)
    elif kind == 'b':    # theta1 处小环
        th_f = lambda w: thm - Amp * np.cos(w)
        s_f = lambda w: w - 2.4 * np.sin(w)
    else:                # theta2 处尖点
        th_f = lambda w: thm - Amp * np.cos(w)
        s_f = lambda w: w + np.sin(w)
    nper = {'a': 3.2, 'b': 4.6, 'c': 3.6}[kind]
    W = np.linspace(0, nper * 2 * np.pi, 2000)
    th = th_f(W)
    s_tot = s_f(W[-1])
    lam = 0.12 * np.pi + 0.76 * np.pi * s_f(W) / s_tot   # 始终位于正面
    u = np.sin(th) * np.cos(lam)
    v = np.cos(th) * np.cos(beta) - np.sin(th) * np.sin(beta) * np.sin(lam)
    ax.add_line(Line2D(cx + u, v, color='k', lw=1.6, zorder=2.4, solid_capstyle='round'))
    ax.text(cx, -1.74, kind, fontsize=11)


def fig_49():
    fig, ax = new_ax(3.55, 2.0, (-1.55, 7.25), (-2.0, 1.55))
    for i, k in enumerate('abc'):
        _sphere_panel(ax, i * 2.93, k)
    save(fig, 49)


# ---------------------------------------------------------------- 图50
def fig_50():
    fig, ax = new_ax(2.3, 2.6, (-1.10, 1.40), (-0.08, 2.55))
    A = np.array([0., 0.])
    ec = np.array([0., 1.55]); ea, eb = 0.92, 0.25
    ax.add_line(Line2D([0, 0], [0, ec[1]], color='k', lw=0.9, ls=DASH, zorder=1.6))
    ax.add_line(Line2D([0, 0], [ec[1], 2.28], color='k', lw=1.1, zorder=2.0))
    arrow(ax, (0, 2.24), (0, 2.42), lw=1.1, ms=10)
    ax.text(0.09, 2.30, r'$\Omega_{\rm pr}$', fontsize=11)
    t = np.linspace(0, 180, 80)
    ax.add_line(Line2D(ec[0] + ea * np.cos(np.radians(t)), ec[1] + eb * np.sin(np.radians(t)),
                       color='k', lw=0.9, ls=DASHDOT, zorder=1.8))
    t = np.linspace(180, 360, 80)
    ax.add_line(Line2D(ec[0] + ea * np.cos(np.radians(t)), ec[1] + eb * np.sin(np.radians(t)),
                       color='k', lw=1.1, zorder=1.9))
    ax.add_line(Line2D([0, -ea], [0, ec[1]], color='k', lw=1.1, zorder=1.9))
    # Omega_nut：沿右母线的粗箭头
    tip = np.array([ea, ec[1]])
    ax.add_line(Line2D([0, tip[0] * .94], [0, tip[1] * .94], color='k', lw=1.4, zorder=2.4))
    arrow(ax, tip * .94, tip, lw=1.4, ms=11)
    ax.text(tip[0] + 0.06, tip[1] - 0.14, r'$\Omega_{\rm nut}$', fontsize=11)
    # 小锥（本体锥）
    axd = np.radians(51)
    ua = np.array([np.cos(axd), np.sin(axd)])
    Cs = 1.18 * ua
    sa_, sb_ = 0.235, 0.160
    ell_ang = axd - 90
    tu, tl = tangents(A, Cs, sa_, sb_, ell_ang)
    Tup, Tlo = ell_pt(Cs, sa_, sb_, ell_ang, tu), ell_pt(Cs, sa_, sb_, ell_ang, tl)
    Tside = Tup if Tup[0] > Tlo[0] else Tlo
    ax.add_line(Line2D([0, Cs[0] * 1.18], [0, Cs[1] * 1.18], color='k', lw=0.9, ls=DASHDOT, zorder=2.1))
    tt = np.linspace(0, 360, 241)
    pts = np.array([ell_pt(Cs, sa_, sb_, ell_ang, t_) for t_ in tt])
    along = (pts - Cs) @ ua
    for i in range(240):
        v = along[i] <= 0
        ax.add_line(Line2D(pts[i:i + 2, 0], pts[i:i + 2, 1], color='k',
                           lw=0.9 if v else 1.1, ls=DASH if v else '-', zorder=2.2))
    for T in (Tup, Tlo):
        ax.add_line(Line2D([0, T[0]], [0, T[1]], color='k', lw=1.1, zorder=2.3))
    # 阴影泪滴（轴与右母线之间）
    bnd = [A + 0.03 * ua]
    for s in np.linspace(0.12, 0.88, 24):
        bnd.append(A + s * (Tside - A))
    q0 = A + 0.88 * (Tside - A)
    q1 = A + 0.76 * ua
    mid = (q0 + q1) / 2 + 0.13 * np.array([Tside[1], -Tside[0]]) / np.linalg.norm(Tside)
    arc = bezier(q0, mid, mid, q1, 24)
    bnd.extend(arc)
    for s in np.linspace(0.74, 0.05, 18):
        bnd.append(A + s * ua)
    bnd = np.array(bnd)
    ax.add_patch(Polygon(bnd, closed=True, facecolor='none', edgecolor='none', zorder=2.4))
    hatch_region(ax, clip_patch(ax, Polygon(bnd, closed=True)),
                 spacing=0.042, slant=(0.35, 1.0), ext=0.7)
    # alpha 弧
    al = arc_pts(A, 0.34, np.degrees(axd), 90, n=30)
    draw_poly(ax, al, lw=0.9, z=2.6)
    ax.text(0.09, 0.42, r'$\alpha$', fontsize=11)
    save(fig, 50)


# ---------------------------------------------------------------- 图51
def fig_51():
    """本体极迹：椭球 M_i^2/(2EI_i)=2E 与球面 |M|=c 的交线（世界系：
    体轴 x1->z（半轴最短 sa1），x2->y（sa2），x3->x（sa3））。"""
    fig, ax = new_ax(3.75, 2.05, (-3.90, 3.60), (-2.10, 2.10))
    sa1, sa2, sa3 = 1.35, 2.99, 3.45          # z, y, x 方向半轴
    al, be = np.radians(47.9), np.radians(23.7)
    cam = np.array([np.sin(be) * np.cos(al), np.sin(be) * np.sin(al), np.cos(be)])
    rgt = np.array([-np.sin(al), np.cos(al), 0])
    up = np.array([-np.sin(be) * np.cos(al), -np.sin(be) * np.sin(al), np.cos(be)])

    def proj(p):
        return np.array([np.dot(p, rgt), np.dot(p, up)])

    Qd = np.array([1 / sa3 ** 2, 1 / sa2 ** 2, 1 / sa1 ** 2])   # (x,y,z)

    def draw_surf_curve(pts, lw_s=1.1, lw_h=0.75):
        vis = np.array([np.dot(Qd * p, cam) > 0 for p in pts])
        i = 0
        while i < len(pts) - 1:
            j = i
            while j < len(pts) - 2 and vis[j + 1] == vis[j]:
                j += 1
            seg = pts[i:j + 2]
            p2 = np.array([proj(p) for p in seg])
            ax.add_line(Line2D(p2[:, 0], p2[:, 1], color='k',
                               lw=lw_s if vis[i] else lw_h,
                               ls='-' if vis[i] else DASH, zorder=2.4 if vis[i] else 2.0))
            i = j + 1

    def principal(pair):
        t = np.linspace(0, 2 * np.pi, 361)
        c, s = np.cos(t), np.sin(t)
        if pair == 'x1x2':      # (z,y)
            pts = np.vstack([np.zeros_like(t), sa2 * s, sa1 * c]).T
        elif pair == 'x1x3':    # (z,x)
            pts = np.vstack([sa3 * s, np.zeros_like(t), sa1 * c]).T
        else:                   # (x,y)
            pts = np.vstack([sa3 * c, sa2 * s, np.zeros_like(t)]).T
        draw_surf_curve(pts, lw_s=0.75, lw_h=0.65)

    principal('x1x2'); principal('x1x3'); principal('x2x3')

    def polhode(s, pole, sgn=(1,)):
        """pole: 'x1'/'x3'（世界 z / x 轴极），sgn 为该极的符号"""
        semi = np.array([sa3, sa2, sa1])          # (x,y,z)
        ipole = 2 if pole == 'x1' else 0          # 世界分量序号
        j, k = [q for q in range(3) if q != ipole]
        out = []

        def two(w):
            mj = ((s - w) / semi[k] ** 2 - (1 - w / semi[ipole] ** 2)) / \
                 (1 / semi[k] ** 2 - 1 / semi[j] ** 2)
            return mj, s - w - mj

        lo, hi = None, None
        for w in np.linspace(1e-9, s, 6000):
            mj, mk = two(w)
            if mj >= -1e-9 and mk >= -1e-9:
                if lo is None:
                    lo = w
                hi = w
        if lo is None:
            return out
        ws = np.linspace(lo, hi, 240)
        for sg in sgn:
            pts = []
            for w in ws:
                mj, mk = two(w)
                p = [0, 0, sg * np.sqrt(w)]; p[j] = np.sqrt(max(mj, 0)); p[k] = np.sqrt(max(mk, 0))
                pts.append(tuple(p))
            for w in ws[::-1]:
                mj, mk = two(w)
                p = [0, 0, sg * np.sqrt(w)]; p[j] = -np.sqrt(max(mj, 0)); p[k] = np.sqrt(max(mk, 0))
                pts.append(tuple(p))
            for w in ws:
                mj, mk = two(w)
                p = [0, 0, sg * np.sqrt(w)]; p[j] = -np.sqrt(max(mj, 0)); p[k] = -np.sqrt(max(mk, 0))
                pts.append(tuple(p))
            for w in ws[::-1]:
                mj, mk = two(w)
                p = [0, 0, sg * np.sqrt(w)]; p[j] = np.sqrt(max(mj, 0)); p[k] = -np.sqrt(max(mk, 0))
                pts.append(tuple(p))
            out.append(np.array(pts))
        return out

    # 分离线：M^2 = 2EI2（= sa2^2），两平面曲线过 x2 极（世界 y）
    k2 = np.sqrt((1 / sa2 ** 2 - 1 / sa3 ** 2) / (1 / sa1 ** 2 - 1 / sa2 ** 2))
    for sg in (1, -1):
        e1 = np.array([1, 0, sg * k2]); e1 /= np.linalg.norm(e1)   # (x,z) 平面内
        e2 = np.array([0, 1.0, 0])
        t = np.linspace(0, 2 * np.pi, 361)
        pts = []
        for t_ in t:
            dd = np.cos(t_) * e1 + np.sin(t_) * e2
            pts.append(dd / np.sqrt(np.sum(Qd * dd ** 2)))
        draw_surf_curve(np.array(pts), lw_s=1.15, lw_h=0.8)

    for curve in polhode(2.2, 'x1', sgn=(1,)):
        draw_surf_curve(curve, lw_s=1.1)
    for curve in polhode(3.8, 'x1', sgn=(1,)):
        draw_surf_curve(curve, lw_s=1.1)
    for curve in polhode(10.8, 'x3', sgn=(1, -1)):
        draw_surf_curve(curve, lw_s=1.1)

    # 外形轮廓（投影椭圆）
    P = np.vstack([rgt, up])
    G = np.linalg.inv(P @ np.diag(1 / Qd) @ P.T)
    t = np.linspace(0, 2 * np.pi, 361)
    w_, V_ = np.linalg.eigh(G)
    pts2 = (np.vstack([np.cos(t), np.sin(t)]).T / np.sqrt(w_)) @ V_.T
    ax.add_line(Line2D(pts2[:, 0], pts2[:, 1], color='k', lw=1.4, zorder=2.6))
    # 轴线：x1 沿 z 向上，x2 沿 y 向右下，x3 沿 +x（投影向左下）
    for vec, ext, lab, off in ((np.array([0, 0, 1.0]), 1.62, r'$x_1$', (0.06, 0.00)),
                               (np.array([0, 1.0, 0]), 1.42, r'$x_2$', (0.05, -0.12)),
                               (np.array([1.0, 0, 0]), 1.34, r'$x_3$', (-0.10, -0.16))):
        alen = sa1 if abs(vec[2]) else (sa2 if vec[1] else sa3)
        pole = vec * alen
        pA = proj(pole); pB = proj(pole * ext)
        ax.add_line(Line2D([pA[0], pB[0]], [pA[1], pB[1]], color='k', lw=1.0, zorder=2.5))
        ax.text(pB[0] + off[0], pB[1] + off[1], lab, fontsize=11)
    save(fig, 51)


# ---------------------------------------------------------------- 图52
def fig_52():
    fig, ax = new_ax(2.35, 3.15, (-1.15, 1.85), (-2.55, 0.95))
    C = np.array([0., 0.])
    alpha = np.radians(30)
    d = np.array([np.sin(alpha), -np.cos(alpha)])
    n = np.array([np.cos(alpha), np.sin(alpha)])
    w = 0.085
    ax.add_line(Line2D([-0.40, -0.40], [0, -2.0], color='k', lw=1.2, zorder=2.0))
    ax.add_line(Line2D([0, 0], [0, -2.0], color='k', lw=1.2, zorder=2.0))
    ax.add_line(Line2D([-0.40, 0], [0, 0], color='k', lw=1.2, zorder=2.0))
    hatch_along(ax, (-0.38, -0.005), (-0.02, -0.005), (0.5, -0.5) / np.sqrt(.5), n=7, L=0.085)
    hatch_along(ax, (-0.005, -0.12), (-0.005, -1.95), (-0.5, -0.5) / np.sqrt(.5), n=22, L=0.085)
    ax.add_line(Line2D([-0.40, 1.45], [-2.0, -2.0], color='k', lw=1.2, zorder=2.0))
    hatch_along(ax, (-0.38, -2.005), (1.42, -2.005), (0.5, -0.5) / np.sqrt(.5), n=22, L=0.085)
    # h 尺寸箭头（柱内，箭头指向两端面）
    arrow(ax, (-0.20, -0.55), (-0.20, -0.14), lw=0.9, ms=8)
    arrow(ax, (-0.20, -1.45), (-0.20, -1.86), lw=0.9, ms=8)
    ax.add_line(Line2D([-0.20, -0.20], [-0.50, -1.50], color='k', lw=0.9, zorder=2.0))
    ax.text(-0.37, -1.06, r'$h$', fontsize=11)
    # 绳张力 T（沿地面向左）
    arrow(ax, (1.17, -1.83), (0.52, -1.83), lw=1.0, ms=9)
    ax.text(0.62, -1.70, r'$T$', fontsize=11)
    # 杆 DB（两平行线 + 圆头端帽）
    t0, t1 = -0.66, 2.30
    th0 = np.arctan2(d[1], d[0])
    for sg in (-1, 1):
        q0 = C + t0 * d + sg * (w / 2) * n
        q1 = C + t1 * d + sg * (w / 2) * n
        ax.add_line(Line2D([q0[0], q1[0]], [q0[1], q1[1]], color='k', lw=1.4, zorder=2.6))
    for tt in (t0, t1):
        cc = C + tt * d
        angs = np.linspace(th0 + np.pi / 2, th0 + 3 * np.pi / 2, 30)
        ax.add_line(Line2D(cc[0] + (w / 2) * np.cos(angs), cc[1] + (w / 2) * np.sin(angs),
                           color='k', lw=1.4, zorder=2.6))
    # R_C（虚箭线，垂直于杆向右上）
    darrow(ax, C + 0.10 * n, C + 0.60 * n, lw=0.9)
    ax.text(C[0] + 0.68 * n[0], C[1] + 0.68 * n[1], r'$R_C$', fontsize=11)
    ax.text(C[0] + 0.16 * n[0] - 0.12, C[1] + 0.16 * n[1] + 0.06, r'$C$', fontsize=11)
    # alpha 弧
    al = arc_pts(C, 0.46, -90, -30, n=30)
    draw_poly(ax, al, lw=0.9, z=2.4)
    ax.text(0.13, -0.60, r'$\alpha$', fontsize=11)
    # P（杆中点竖直虚箭头）
    pm = C + 1.0 * d
    darrow(ax, pm + (0.02, -0.06), pm + (0.02, -0.48), lw=0.9)
    ax.text(pm[0] - 0.08, pm[1] - 0.68, r'$P$', fontsize=11)
    # R_B（B 处竖直虚箭头）
    pB = C + 2.06 * d + 0.02 * n
    darrow(ax, pB, pB + (0, 0.44), lw=0.9)
    ax.text(pB[0] + 0.09, pB[1] + 0.46, r'$R_B$', fontsize=11)
    # D、A、B 标注
    ax.text(C[0] + t0 * d[0] + 0.20, C[1] + t0 * d[1] + 0.04, r'$D$', fontsize=11)
    ax.text(-0.52, -2.28, r'$A$', fontsize=11)
    ax.text(pB[0] + 0.04, -2.30, r'$B$', fontsize=11)
    save(fig, 52)


# ---------------------------------------------------------------- 图53
def fig_53():
    fig, ax = new_ax(3.3, 2.9, (-0.10, 3.25), (-2.45, 0.50))
    B0 = np.array([0.21, -1.78])
    U1 = np.array([1.4125, 0.76])
    D3 = np.array([1.17, -0.05])
    H = 0.95
    wall = [B0, B0 + U1, B0 + U1 + (0, H), B0 + (0, H)]
    ax.add_line(Line2D([p[0] for p in wall] + [wall[0][0]],
                       [p[1] for p in wall] + [wall[0][1]], color='k', lw=1.0, zorder=1.5))
    flo = [B0, B0 + U1, B0 + U1 + D3, B0 + D3]
    ax.add_line(Line2D([p[0] for p in flo] + [flo[0][0]],
                       [p[1] for p in flo] + [flo[0][1]], color='k', lw=1.0, zorder=1.5))
    A = B0 + 0.133 * U1 + np.array([0, 0.525])
    Dp = B0 + 0.625 * U1 + np.array([0, 0.525])
    Bp = B0 + 0.753 * U1 + 0.455 * D3
    Cp = B0 + 0.203 * U1
    # 杆 AB（双线 + 端帽）
    u = Bp - A; u = u / np.linalg.norm(u)
    nv = np.array([-u[1], u[0]]) * 0.024
    for sg in (-1, 1):
        ax.add_line(Line2D([A[0] + sg * nv[0], Bp[0] + sg * nv[0]],
                           [A[1] + sg * nv[1], Bp[1] + sg * nv[1]], color='k', lw=1.2, zorder=2.4))
    ax.add_line(Line2D([A[0] - nv[0], A[0] + nv[0]], [A[1] - nv[1], A[1] + nv[1]], color='k', lw=1.2, zorder=2.4))
    ax.add_line(Line2D([Bp[0] - nv[0], Bp[0] + nv[0]], [Bp[1] - nv[1], Bp[1] + nv[1]], color='k', lw=1.2, zorder=2.4))
    ax.add_patch(Circle(Dp, 0.045, facecolor='white', edgecolor='k', lw=1.1, zorder=2.6))
    ax.add_patch(Circle(Cp, 0.045, facecolor='white', edgecolor='k', lw=1.1, zorder=2.6))
    ax.add_line(Line2D([A[0], Dp[0]], [A[1], Dp[1]], color='k', lw=0.9, zorder=2.2))
    ax.add_line(Line2D([Cp[0], Bp[0]], [Cp[1], Bp[1]], color='k', lw=0.9, zorder=2.2))
    # T_A（沿 AD 向上）
    uAD = (Dp - A) / np.linalg.norm(Dp - A)
    arrow(ax, A + 0.28 * uAD, A + 0.72 * uAD, lw=1.0, ms=9)
    ax.text(A[0] + 0.44 * uAD[0] - 0.06, A[1] + 0.44 * uAD[1] + 0.12, r'$T_A$', fontsize=11)
    # T_B（沿 B->C）
    uBC = (Cp - Bp) / np.linalg.norm(Cp - Bp)
    arrow(ax, Bp + 0.16 * uBC, Bp + 0.62 * uBC, lw=1.0, ms=9)
    ax.text(Bp[0] + 0.30 * uBC[0] + 0.10, Bp[1] + 0.30 * uBC[1] - 0.04, r'$T_B$', fontsize=11)
    # R_A（A 处水平虚箭线）
    darrow(ax, A + (0.06, 0.0), A + (0.50, 0.0), lw=0.9)
    ax.text(A[0] + 0.44, A[1] + 0.10, r'$R_A$', fontsize=11)
    # R_B（B 处竖直虚箭线）
    darrow(ax, Bp + (0, 0.05), Bp + (0, 0.62), lw=0.9)
    ax.text(Bp[0] + 0.06, Bp[1] + 0.68, r'$R_B$', fontsize=11)
    # P（杆中点竖直箭头）
    pm = (A + Bp) / 2
    arrow(ax, pm + (0, -0.05), pm + (0, -0.34), lw=1.0, ms=9)
    ax.text(pm[0] - 0.04, pm[1] - 0.55, r'$P$', fontsize=11)
    # alpha 弧（B 处，BA 与 BC 之间；角度走短弧）
    aA = np.degrees(np.arctan2((A - Bp)[1], (A - Bp)[0]))
    aC = np.degrees(np.arctan2((Cp - Bp)[1], (Cp - Bp)[0]))
    aC2 = aA + ang_norm(aC - aA)
    al = arc_pts(Bp, 0.50, aA, aC2, n=30)
    draw_poly(ax, al, lw=0.9, zorder=2.3) if False else draw_poly(ax, al, lw=0.9, z=2.3)
    amid = np.radians((aA + aC2) / 2)
    ax.text(Bp[0] + 0.58 * np.cos(amid), Bp[1] + 0.58 * np.sin(amid) + 0.02, r'$\alpha$', fontsize=11)
    # beta 弧（C 处，墙底线与绳之间）
    aB2 = np.degrees(np.arctan2((Bp - Cp)[1], (Bp - Cp)[0]))
    aU = np.degrees(np.arctan2(U1[1], U1[0]))
    be = arc_pts(Cp, 0.38, aB2, aU, n=30)
    draw_poly(ax, be, lw=0.9, z=2.3)
    bm = np.radians((aU + aB2) / 2)
    ax.text(Cp[0] + 0.30 * np.cos(bm), Cp[1] + 0.30 * np.sin(bm) + 0.05, r'$\beta$', fontsize=11)
    ax.text(A[0] - 0.17, A[1] - 0.05, r'$A$', fontsize=11)
    ax.text(Bp[0] + 0.08, Bp[1] - 0.03, r'$B$', fontsize=11)
    ax.text(Dp[0] + 0.01, Dp[1] + 0.13, r'$D$', fontsize=11)
    ax.text(Cp[0] - 0.07, Cp[1] + 0.15, r'$C$', fontsize=11)
    save(fig, 53)


# ---------------------------------------------------------------- 图54
def fig_54():
    fig, ax = new_ax(2.45, 2.7, (-0.80, 2.40), (-0.50, 2.28))
    g = -0.30
    Ax, Bx = (0.10, 1.90)
    Cx, Cy = (1.0, 1.95)
    w = 0.075
    ax.add_line(Line2D([-0.72, 2.32], [g, g], color='k', lw=1.4, zorder=2.0))
    hatch_along(ax, (-0.70, g - 0.005), (2.30, g - 0.005), (0.55, -0.55) / np.sqrt(.605),
                n=26, L=0.11, lw=0.8)

    def rod(P0, P1):
        P0 = np.asarray(P0, float); P1 = np.asarray(P1, float)
        u = P1 - P0; u = u / np.linalg.norm(u)
        nv = np.array([-u[1], u[0]])
        pa0, pb0 = P0 + (w / 2) * nv, P1 + (w / 2) * nv
        pa1, pb1 = P0 - (w / 2) * nv, P1 - (w / 2) * nv
        th = np.arctan2(u[1], u[0])
        cap0 = np.linspace(th + np.pi / 2, th + 3 * np.pi / 2, 24)
        cap1 = np.linspace(th - np.pi / 2, th + np.pi / 2, 24)
        pts = ([(P0[0] + (w / 2) * np.cos(a), P0[1] + (w / 2) * np.sin(a)) for a in cap0] +
               [tuple(pb0)] +
               [(P1[0] + (w / 2) * np.cos(a), P1[1] + (w / 2) * np.sin(a)) for a in cap1] +
               [tuple(pa1)])
        ax.add_patch(Polygon(pts, closed=True, facecolor='white', edgecolor='k', lw=1.3, zorder=2.4))

    rod((Ax, g), (Cx, Cy))
    rod((Bx, g), (Cx, Cy))
    # 绳 AB + 两个张力箭头
    ry = g + 0.09
    ax.add_line(Line2D([Ax + 0.04, Bx - 0.04], [ry, ry], color='k', lw=0.9, zorder=2.2))
    arrow(ax, (Ax + 0.38, ry), (Ax + 0.85, ry), lw=1.0, ms=9)
    arrow(ax, (Bx - 0.38, ry), (Bx - 0.85, ry), lw=1.0, ms=9)
    ax.text(Ax + 0.50, ry + 0.14, r'$T$', fontsize=11)
    ax.text(Bx - 0.72, ry + 0.14, r'$T$', fontsize=11)
    # F（AC 杆中点竖直向下）
    F0 = np.array([(Ax + Cx) / 2 + 0.02, (g + Cy) / 2 + 0.10])
    arrow(ax, F0, F0 + (0, -0.50), lw=1.0, ms=9)
    ax.text(F0[0] + 0.07, F0[1] - 0.62, r'$F$', fontsize=11)
    # R_C（沿 CB 延线，虚箭线）
    uCB = np.array([Cx - Bx, Cy - g]); uCB = uCB / np.linalg.norm(uCB)
    darrow(ax, np.array([Cx, Cy]) + 0.06 * uCB, np.array([Cx, Cy]) + 0.52 * uCB, lw=0.9)
    ax.text(Cx + 0.60 * uCB[0] - 0.34, Cy + 0.60 * uCB[1] + 0.04, r'$R_C$', fontsize=11)
    # R_A、R_B
    darrow(ax, (Ax - 0.02, g + 0.06), (Ax - 0.02, g + 0.50), lw=0.9)
    ax.text(Ax - 0.32, g + 0.52, r'$R_A$', fontsize=11)
    darrow(ax, (Bx + 0.02, g + 0.06), (Bx + 0.02, g + 0.50), lw=0.9)
    ax.text(Bx + 0.10, g + 0.52, r'$R_B$', fontsize=11)
    ax.text(Ax - 0.22, g - 0.05, r'$A$', fontsize=11)
    ax.text(Bx + 0.09, g - 0.05, r'$B$', fontsize=11)
    ax.text(Cx + 0.09, Cy + 0.01, r'$C$', fontsize=11)
    save(fig, 54)


# ---------------------------------------------------------------- 图55
def fig_55():
    fig, ax = new_ax(2.9, 1.75, (-0.55, 4.75), (-0.85, 2.35))
    P2 = np.array([0.0, 0.0]); P1 = np.array([4.2, 0.0]); T = np.array([2.55, 1.95])
    for p0, p1 in ((P2, P1), (P2, T), (T, P1)):
        ax.add_line(Line2D([p0[0], p1[0]], [p0[1], p1[1]], color='k', lw=1.3, zorder=2))
    a2 = np.degrees(np.arctan2((T - P2)[1], (T - P2)[0]))
    a1 = np.degrees(np.arctan2((T - P1)[1], (T - P1)[0]))
    arc2 = arc_pts(P2, 0.95, 0, a2, n=30)
    draw_poly(ax, arc2, lw=0.9, z=2.2)
    arc1 = arc_pts(P1, 0.95, a1, 180, n=30)
    draw_poly(ax, arc1, lw=0.9, z=2.2)
    am2 = np.radians(a2 / 2)
    ax.text(P2[0] + 1.28 * np.cos(am2) + 0.07, P2[1] + 1.28 * np.sin(am2) - 0.03, r'$\theta_2$', fontsize=11)
    am1 = np.radians((a1 + 180) / 2)
    ax.text(P1[0] + 1.28 * np.cos(am1) - 0.16, P1[1] + 1.28 * np.sin(am1) - 0.03, r'$\theta_1$', fontsize=11)
    u21 = (T - P2) / np.linalg.norm(T - P2)
    n21 = np.array([-u21[1], u21[0]])
    mid = P2 + 0.55 * (T - P2)
    ax.text(mid[0] + 0.16 * n21[0], mid[1] + 0.16 * n21[1], r'$r_2$', fontsize=11)
    u11 = (T - P1) / np.linalg.norm(T - P1)
    n11 = np.array([u11[1], -u11[0]])
    mid = P1 + 0.55 * (T - P1)
    ax.text(mid[0] + 0.16 * n11[0] - 0.02, mid[1] + 0.16 * n11[1], r'$r_1$', fontsize=11)
    ax.text(1.83, -0.40, r'$2\sigma$', fontsize=11)
    ax.text(-0.12, -0.46, r'$\alpha_2$', fontsize=11)
    ax.text(4.10, -0.46, r'$\alpha_1$', fontsize=11)
    save(fig, 55)


# ---------------------------------------------------------------- 图56
def fig_56():
    fig, ax = new_ax(2.65, 1.55, (-1.55, 2.35), (-1.55, 0.42))
    y0 = 0.0
    r = 0.072
    dx = 0.028
    x1, d1 = 0.0, -1.02
    x2, d2 = 0.92, -0.52
    for x, dd in ((x1, d1), (x2, d2)):
        ax.add_line(Line2D([x - dx, x - dx], [y0, dd], color='k', lw=1.1, zorder=2))
        ax.add_line(Line2D([x + dx, x + dx], [y0, dd], color='k', lw=1.1, zorder=2))
        ax.add_patch(Circle((x, dd - r * 0.55), r, facecolor='white', edgecolor='k',
                            lw=1.1, zorder=2.2))
    for xa, xb in ((-1.50, x1 - dx), (x1 + dx, x2 - dx), (x2 + dx, 2.30)):
        ax.add_line(Line2D([xa, xb], [y0, y0], color='k', lw=1.3, zorder=2))
    ax.text(x1 + 0.10, d1 - 0.18, r'$w_0$', fontsize=11)
    # 复变量 w 标记（独立小圆）
    ax.add_patch(Circle((1.80, -0.52), 0.155, facecolor='white', edgecolor='k', lw=1.1, zorder=2.2))
    ax.text(1.80, -0.575, r'$w$', fontsize=11, ha='center', zorder=2.3)
    save(fig, 56)


if __name__ == '__main__':
    import sys
    which = sys.argv[1:] if len(sys.argv) > 1 else []
    fns = {43: fig_43, 44: fig_44, 45: fig_45, 46: fig_46, 47: fig_47, 48: fig_48,
           49: fig_49, 50: fig_50, 51: fig_51, 52: fig_52, 53: fig_53, 54: fig_54,
           55: fig_55, 56: fig_56}
    for n, fn in fns.items():
        if which and str(n) not in which:
            continue
        fn()
        print(f'fig{n} done')
