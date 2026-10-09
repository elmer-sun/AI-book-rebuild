# -*- coding: utf-8 -*-
"""
《时空与几何》(Carroll, Spacetime and Geometry) 第 3 章插图重绘
黑白教材风矢量图, matplotlib Agg 后端。
产物: figures/fig_{key}.pdf + figures/preview/fig_{key}.png
图 3.1-3.9 (原书页码见各函数 docstring) + 习题 7 无编号回路图 (fig_3.11-ex7)。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Arc, Rectangle, PathPatch
from matplotlib.path import Path

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

BASE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(os.path.dirname(BASE), 'figures')
PRE_DIR = os.path.join(FIG_DIR, 'preview')
os.makedirs(PRE_DIR, exist_ok=True)

GRAY = '0.62'   # 辅助(灰色)箭头/线条
GRAYL = '0.72'  # 更浅的灰色块箭头


# ---------------------------------------------------------------- 公共小工具
def arrow(ax, p0, p1, lw=1.4, ms=14, color='k', ls='-', style='-|>', zorder=3,
          rad=None):
    """带箭头线段 (annotate 封装). rad: arc3 弯曲率."""
    props = dict(arrowstyle=style, color=color, lw=lw,
                 linestyle=ls, mutation_scale=ms, shrinkA=0, shrinkB=0)
    if rad is not None:
        props['connectionstyle'] = 'arc3,rad=%g' % rad
    ax.annotate('', xy=p1, xytext=p0, zorder=zorder, arrowprops=props)


def bez(p0, p1, p2, t):
    """二次贝塞尔: 点与切向."""
    x = (1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * p1[1] + t ** 2 * p2[1]
    dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
    dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
    return (x, y), (dx, dy)


def bezier_path(p0, p1, p2, n=100):
    t = np.linspace(0, 1, n)
    pts = [bez(p0, p1, p2, ti)[0] for ti in t]
    return np.array(pts)


def catmull_rom(pts, closed=False, n=24):
    """Catmull-Rom 样条插值, 返回密集采样点."""
    P = [np.array(p, float) for p in pts]
    if closed:
        P = P + [P[0], P[1], P[2]]
    else:
        P = [P[0]] + P + [P[-1]]
    out = []
    for i in range(len(P) - 3):
        p0, p1, p2, p3 = P[i], P[i + 1], P[i + 2], P[i + 3]
        t = np.linspace(0, 1, n, endpoint=False)
        for ti in t:
            ti2, ti3 = ti * ti, ti * ti * ti
            pt = 0.5 * ((2 * p1) + (-p0 + p2) * ti +
                        (2 * p0 - 5 * p1 + 4 * p2 - p3) * ti2 +
                        (-p0 + 3 * p1 - 3 * p2 + p3) * ti3)
            out.append(pt)
    out.append(np.array(P[-2], float))
    return np.array(out)


def new_ax(w, h, xlim, ylim, equal=True):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def save(fig, key):
    fig.savefig(os.path.join(FIG_DIR, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRE_DIR, 'fig_%s.png' % key),
                bbox_inches='tight', pad_inches=0.03, dpi=150)
    plt.close(fig)
    print('saved fig_%s' % key)


# ---------------------------------------------------------------- 图 3.1
def fig_3_1():
    """书页 103 (p118): 平直空间平行移动, 保持矢量分量不变."""
    fig, ax = new_ax(4.0, 2.55, (0, 4.0), (0, 2.6))

    # 两条细轴线 (无箭头)
    ax.plot([0.55, 0.55], [0, 2.6], color='k', lw=0.9)
    ax.plot([0, 4.0], [0.28, 0.28], color='k', lw=0.9)

    # 路径 p -> q (浅弧, 向左下微垂)
    p0, p1, p2 = (3.05, 0.55), (1.45, 0.78), (0.75, 1.55)
    pts = bezier_path(p0, p1, p2)
    ax.plot(pts[:, 0], pts[:, 1], color='k', lw=1.1, zorder=2)

    # 沿路径的 7 个平行矢量 (方向恒定)
    d = np.array([np.cos(np.radians(55)), np.sin(np.radians(55))])
    for t in np.linspace(0, 1, 7):
        (x, y), _ = bez(p0, p1, p2, t)
        arrow(ax, (x, y), (x + 0.75 * d[0], y + 0.75 * d[1]),
              lw=2.0, ms=17, zorder=4)

    # 端点与标注
    for (x, y) in [p0, p2]:
        ax.plot(x, y, 'k.', ms=6)
    ax.text(2.98, 0.40, r'$p$', fontsize=13)
    ax.text(0.52, 1.47, r'$q$', fontsize=13)

    # 灰色大弧形箭头 + 文字 (弧向右上方弯, 离开路径)
    arrow(ax, (3.55, 0.95), (1.35, 2.35), lw=4.5, ms=40, color=GRAY,
          style='-|>', zorder=1, rad=0.30)
    ax.text(2.92, 2.18, 'keep vector constant', fontsize=11.5,
            style='italic', rotation=-26, ha='center', va='center',
            rotation_mode='anchor')
    save(fig, '3.1')


# ---------------------------------------------------------------- 图 3.2
def fig_3_2():
    """书页 104 (p119): 球面上的平行移动, 结果依赖于路径."""
    fig, ax = new_ax(3.5, 3.6, (-1.25, 1.25), (-1.22, 1.62))
    R, b = 1.0, 0.27

    # 球体: 主圆 + 赤道以下略深
    ax.add_patch(plt.Circle((0, 0), R, facecolor='0.88', edgecolor='none'))
    th = np.linspace(np.pi, 2 * np.pi, 100)
    circ_lo = np.stack([np.cos(th), np.sin(th)], 1)
    ph = np.linspace(0, np.pi, 100)
    ell_lo = np.stack([np.cos(ph), -b * np.sin(ph)], 1)
    verts = np.vstack([circ_lo, ell_lo])
    codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 1)
    ax.add_patch(PathPatch(Path(verts, codes), facecolor='0.79',
                           edgecolor='none'))
    ax.add_patch(plt.Circle((0, 0), R, facecolor='none', edgecolor='k', lw=1.1))

    # 赤道 (完整椭圆)
    tq = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(tq), b * np.sin(tq), color='k', lw=0.9)

    # 赤道上的 5 个竖直矢量
    xs = [-0.62, -0.31, 0.0, 0.31, 0.62]
    for x in xs:
        y0 = -b * np.sqrt(1 - x * x)
        arrow(ax, (x, y0), (x, y0 + 0.52), lw=2.3, ms=20)

    # 两条经线 (二次贝塞尔, 向外轻鼓)
    pole = (0.02, 0.985)
    L = [(-0.62, -0.2116), (-0.82, 0.30), pole]
    Rt = [(0.62, -0.2116), (0.82, 0.30), pole]
    for P in (L, Rt):
        pts = bezier_path(*P)
        ax.plot(pts[:, 0], pts[:, 1], color='k', lw=1.0)

    # 沿路径的矢量 (角度为相对 +x 方向; 随上升渐向左倾, 汇于极点分开)
    for P in (L, Rt):
        for t, ang in zip([0.30, 0.55, 0.78], [90, 104, 120]):
            (x, y), _ = bez(*P, t)
            a = np.radians(ang)
            arrow(ax, (x, y), (x + 0.45 * np.cos(a), y + 0.45 * np.sin(a)),
                  lw=2.0, ms=17)

    # 极点处两支长矢量 (相差 theta)
    for ang in (137, 45):
        a = np.radians(ang)
        arrow(ax, pole, (pole[0] + 0.55 * np.cos(a), pole[1] + 0.55 * np.sin(a)),
              lw=2.3, ms=20)
    save(fig, '3.2')


# ---------------------------------------------------------------- 图 3.3
def fig_3_3():
    """书页 110 (p125): 类时路径可用总长度为零的类光折线逼近."""
    fig, ax = new_ax(2.4, 4.7, (0, 1), (0, 1), equal=False)

    # 灰色底板
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor='0.80',
                           edgecolor='none', zorder=0))

    # 类时光滑曲线 (S 形, 两端点)
    anchors = [(0.60, 0.955), (0.42, 0.78), (0.33, 0.60), (0.38, 0.44),
               (0.50, 0.32), (0.68, 0.18), (0.86, 0.045)]
    cur = catmull_rom(anchors, n=30)
    ax.plot(cur[:, 0], cur[:, 1], color='k', lw=2.3, zorder=3)
    ax.plot([anchors[0][0]], [anchors[0][1]], 'k.', ms=6, zorder=4)
    ax.plot([anchors[-1][0]], [anchors[-1][1]], 'k.', ms=6, zorder=4)

    # 类光锯齿线 (白色, 沿曲线凸侧锯齿状逼近)
    n = len(cur)
    cvx = np.zeros_like(cur)
    for i in range(n):
        a = cur[max(i - 1, 0)]
        b = cur[min(i + 1, n - 1)]
        sec = b - 2 * cur[i] + a          # 指向曲率中心
        nrm = np.hypot(*sec)
        if nrm > 1e-9:
            cvx[i] = -sec / nrm           # 凸侧法向
        else:
            cvx[i] = cvx[i - 1] if i else np.array([1.0, 0.0])
    zz = [cur[0]]
    step = (n - 1) // 16
    for i in range(1, 16):
        j = min(i * step, n - 1)
        amp = 0.075 if i % 2 else 0.022
        zz.append(cur[j] + amp * cvx[j])
    zz.append(cur[-1])
    zz = np.array(zz)
    ax.plot(zz[:, 0], zz[:, 1], color='white', lw=1.6, zorder=4)

    # 标注
    ax.annotate('timelike', xy=(0.40, 0.455), xytext=(0.60, 0.545),
                fontsize=12, ha='left', va='center',
                arrowprops=dict(arrowstyle='-', color='k', lw=0.7,
                                shrinkA=2, shrinkB=1))
    ax.annotate('null', xy=(0.50, 0.30), xytext=(0.20, 0.315),
                fontsize=12, ha='left', va='center',
                arrowprops=dict(arrowstyle='-', color='k', lw=0.7,
                                shrinkA=2, shrinkB=1))
    save(fig, '3.3')


# ---------------------------------------------------------------- 图 3.4
def fig_3_4():
    """书页 111 (p126): 指数映射 exp_p : T_p -> M."""
    fig, ax = new_ax(4.3, 2.25, (0, 10.6), (0, 4.9))

    # 切平面 T_p (先画, 流形盖住其下部)
    plane = [(2.45, 2.10), (6.05, 4.25), (6.55, 2.35), (2.90, 0.42)]
    ax.add_patch(plt.Polygon(plane, closed=True, facecolor='0.92',
                             edgecolor='0.55', lw=0.7))
    ax.text(2.80, 4.05, r'$T_p$', fontsize=13)

    # 流形 M (土豆形)
    blob = [(3.68, 2.88), (5.30, 3.16), (6.95, 3.02), (8.61, 2.45),
            (9.80, 1.90), (9.30, 1.15), (7.62, 0.81), (5.30, 0.75),
            (3.71, 1.15), (3.25, 1.75)]
    sm = catmull_rom(blob, closed=True, n=26)
    ax.add_patch(plt.Polygon(sm, closed=True, facecolor='0.86',
                             edgecolor='k', lw=1.0))

    # 测地线 x^nu(lambda), 从 p 到右端
    gd = [(3.81, 2.50), (4.34, 2.72), (5.63, 2.60), (6.95, 2.47),
          (8.28, 2.21), (9.27, 1.99), (9.54, 2.04)]
    g = catmull_rom(gd, n=18)
    ax.plot(g[:, 0], g[:, 1], color='k', lw=1.1, zorder=3)

    # 点 p 与矢量 k^mu
    p = (4.34, 2.72)
    ax.plot(*p, 'k.', ms=5.5, zorder=5)
    arrow(ax, p, (5.35, 3.02), lw=1.9, ms=16, zorder=5)
    ax.text(4.15, 2.30, r'$p$', fontsize=13)
    ax.text(5.02, 3.28, r'$k^\mu$', fontsize=13)

    # lambda = 1 点
    lam = (6.95, 2.47)
    ax.plot(*lam, 'k.', ms=5.5, zorder=5)
    ax.text(6.30, 1.98, r'$\lambda = 1$', fontsize=12.5)
    ax.text(8.85, 1.48, r'$x^\nu(\lambda)$', fontsize=12.5)
    ax.text(3.66, 0.52, r'$M$', fontsize=13)
    save(fig, '3.4')


# ------------------------------------------------------- 图 3.5 / 3.6 公共
def _parallelogram(ax, lab):
    """灰色平行四边形框架. lab='A' 画 A^mu/B^nu + 回路箭头; lab='nabla' 画 nabla."""
    O = np.array([0.07, 0.10])
    A = np.array([0.696, 0.129])
    B = np.array([0.157, 0.545])
    P0, PA, PB, PAB = O, O + A, O + B, O + A + B
    # 黑色: 底边与左边; 灰色: 顶边与右边
    arrow(ax, P0, PA, lw=2.2, ms=20)
    arrow(ax, P0, PB, lw=2.2, ms=20)
    arrow(ax, PB, PAB, lw=2.2, ms=20, color=GRAY)
    arrow(ax, PA, PAB, lw=2.2, ms=20, color=GRAY)

    if lab == 'A':
        ax.text(*(O + 0.5 * A + (0.02, -0.10)), r'$A^\mu$', fontsize=13,
                ha='center')
        ax.text(*(O + B + 0.5 * A + (-0.02, 0.09)), r'$A^\mu$', fontsize=13,
                ha='center')
        ax.text(*(O + 0.5 * B + (-0.09, -0.02)), r'$B^\nu$', fontsize=13,
                ha='right', va='center')
        ax.text(*(O + A + 0.5 * B + (0.10, 0.02)), r'$B^\nu$', fontsize=13,
                ha='left', va='center')
        # 内部回路椭圆 (逆时针方向箭头)
        cx, cy, aa, bb, phi = 0.50, 0.44, 0.205, 0.135, np.radians(32)
        th = np.linspace(0, 2 * np.pi, 200)
        ex = cx + aa * np.cos(th) * np.cos(phi) - bb * np.sin(th) * np.sin(phi)
        ey = cy + aa * np.cos(th) * np.sin(phi) + bb * np.sin(th) * np.cos(phi)
        ax.plot(ex, ey, color='k', lw=0.9, zorder=2)
        the = np.radians(210)
        pe = np.array([cx + aa * np.cos(the) * np.cos(phi)
                       - bb * np.sin(the) * np.sin(phi),
                       cy + aa * np.cos(the) * np.sin(phi)
                       + bb * np.sin(the) * np.cos(phi)])
        te = np.array([-aa * np.sin(the) * np.cos(phi)
                       - bb * np.cos(the) * np.sin(phi),
                       -aa * np.sin(the) * np.sin(phi)
                       + bb * np.cos(the) * np.cos(phi)])
        te = te / np.hypot(*te)
        arrow(ax, pe - 0.11 * te, pe, lw=1.2, ms=16, zorder=3)
    else:
        ax.text(*(O + 0.5 * A + (0.02, -0.10)), r'$\nabla_\mu$', fontsize=13,
                ha='center')
        ax.text(*(O + B + 0.5 * A + (-0.02, 0.09)), r'$\nabla_\mu$', fontsize=13,
                ha='center')
        ax.text(*(O + 0.5 * B + (-0.10, -0.02)), r'$\nabla_\nu$', fontsize=13,
                ha='right', va='center')
        ax.text(*(O + A + 0.5 * B + (0.11, 0.02)), r'$\nabla_\nu$', fontsize=13,
                ha='left', va='center')


def fig_3_5():
    """书页 121 (p136): 两矢量 A^mu, B^nu 张成的无穷小回路."""
    fig, ax = new_ax(3.0, 2.9, (-0.05, 1.05), (-0.05, 0.92))
    _parallelogram(ax, 'A')
    save(fig, '3.5')


def fig_3_6():
    """书页 122 (p137): 两个协变导数的对易子."""
    fig, ax = new_ax(3.0, 2.9, (-0.05, 1.05), (-0.05, 0.92))
    _parallelogram(ax, 'nabla')
    save(fig, '3.6')


# ---------------------------------------------------------------- 图 3.7
def fig_3_7():
    """书页 132 (p147): 环面 = 平面上对边认同的正方形."""
    fig = plt.figure(figsize=(4.8, 2.3))

    # 左: 3D 环面线框
    ax3 = fig.add_axes([0.00, 0.02, 0.50, 0.96], projection='3d')
    u = np.linspace(0, 2 * np.pi, 25)
    v = np.linspace(0, 2 * np.pi, 13)
    U, V = np.meshgrid(u, v)
    Rt, rt = 2.0, 0.85
    X = (Rt + rt * np.cos(V)) * np.cos(U)
    Y = (Rt + rt * np.cos(V)) * np.sin(U)
    Z = rt * np.sin(V)
    ax3.plot_surface(X, Y, Z, color='0.84', edgecolor='k', linewidth=0.35,
                     shade=False, rstride=1, cstride=1)
    ax3.set_axis_off()
    ax3.view_init(elev=26, azim=-90)
    ax3.set_box_aspect((2.6, 2.6, 1.15))
    ax3.set_xlim(-2.9, 2.9)
    ax3.set_ylim(-2.9, 2.9)
    ax3.set_zlim(-1.15, 1.15)

    # 右: 正方形 + 认同弧线
    ax = fig.add_axes([0.47, 0.02, 0.53, 0.96])
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 5.45)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.add_patch(Rectangle((4.8, 0.5), 4.4, 3.8, facecolor='white',
                           edgecolor='k', lw=1.6))
    # 上下边认同: 细实线弧绕左侧外围, 两端箭头指向边
    solid = catmull_rom([(6.15, 4.42), (5.25, 4.78), (4.25, 4.40),
                         (3.80, 3.35), (3.90, 2.15), (4.50, 1.00),
                         (5.45, 0.26), (5.95, 0.44)], n=14)
    ax.plot(solid[:, 0], solid[:, 1], color='k', lw=0.9)
    arrow(ax, (6.34, 4.70), (6.16, 4.44), lw=1.0, ms=12)   # 入上边
    arrow(ax, (5.70, 0.18), (5.92, 0.47), lw=1.0, ms=12)   # 入下边
    # 左右边认同: 虚线弧绕上方, 两端箭头指向边
    dashed = catmull_rom([(4.76, 3.92), (5.30, 4.60), (7.00, 4.97),
                          (8.70, 4.60), (9.24, 3.92)], n=14)
    ax.plot(dashed[:, 0], dashed[:, 1], color='k', lw=0.9,
            linestyle=(0, (4, 2.5)))
    arrow(ax, (4.97, 4.28), (4.78, 3.94), lw=1.0, ms=12)   # 入左边
    arrow(ax, (9.47, 4.26), (9.27, 3.94), lw=1.0, ms=12)   # 入右边
    ax.text(7.0, 5.24, 'identify', fontsize=12, style='italic',
            ha='center')

    # 中部两支灰色块箭头 (对应关系)
    for p0, p1 in [((2.55, 3.35), (4.45, 3.35)), ((4.45, 1.45), (2.55, 1.45))]:
        ax.add_patch(FancyArrowPatch(p0, p1,
                                     arrowstyle='simple,tail_width=0.65,'
                                                'head_width=1.15,head_length=1.05',
                                     mutation_scale=15, color=GRAYL,
                                     shrinkA=0, shrinkB=0))
    save(fig, '3.7')


# ---------------------------------------------------------------- 图 3.8
def fig_3_8():
    """书页 142 (p157): 负曲率上半平面, 测地线为竖直线与半圆."""
    fig, ax = new_ax(4.4, 3.15, (-3.0, 3.3), (-0.18, 2.92))

    # 竖直测地线
    for x in (-2.0, -1.0, 1.0, 2.0):
        ax.plot([x, x], [0, 2.70], color='k', lw=1.3)
    # 半圆测地线
    for c, r in [(0.22, 2.69), (0.48, 2.05), (0.48, 1.51),
                 (-1.78, 1.02), (0.0, 0.49)]:
        t = np.linspace(0, np.pi, 200)
        ax.plot(c + r * np.cos(t), r * np.sin(t), color='k', lw=1.3)

    # 坐标轴: x 轴 (虚线, y=0 边界), y 轴 (实线)
    arrow(ax, (-2.85, 0), (3.18, 0), lw=1.2, ms=13, ls='--')
    arrow(ax, (0, -0.02), (0, 2.85), lw=1.2, ms=13)
    ax.text(3.16, -0.28, r'$x$', fontsize=13, ha='center')
    ax.text(0.14, 2.72, r'$y$', fontsize=13)
    save(fig, '3.8')


# ---------------------------------------------------------------- 图 3.9
def fig_3_9():
    """书页 145 (p160): 测地线族 gamma_s(t), 切矢量 T^mu 与偏离矢量 S^mu."""
    fig, ax = new_ax(4.3, 3.62, (0, 8.3), (0, 7.0))

    # 5 条近族测地线 (同形曲线沿 s 方向平移)
    for k in range(5):
        dx, dy = 0.93 * k, -0.48 * k
        pts = bezier_path((0.67 + dx, 2.33 + dy), (2.97 + dx, 5.00 + dy),
                          (4.57 + dx, 6.60 + dy))
        ax.plot(pts[:, 0], pts[:, 1], color='k', lw=1.1)

    # 灰色参数方向箭头 t (沿测地线) 与 s (横跨族)
    arrow(ax, (1.0, 4.4), (3.0, 6.5), lw=5.0, ms=34, color=GRAYL)
    ax.text(1.55, 5.62, r'$t$', fontsize=14, ha='right')
    arrow(ax, (0.63, 1.87), (3.40, 0.43), lw=5.0, ms=34, color=GRAYL)
    ax.text(1.62, 1.02, r'$s$', fontsize=14, ha='center')

    # T^mu (切向) 与 S^mu (偏离) 于第二条测地线上
    base = (3.13, 3.59)
    arrow(ax, base, (3.90, 4.44), lw=2.4, ms=21)
    arrow(ax, base, (3.88, 3.10), lw=2.4, ms=21)
    ax.text(3.42, 4.55, r'$T^\mu$', fontsize=14, ha='center')
    ax.text(3.48, 2.80, r'$S^\mu$', fontsize=14, ha='center')

    ax.text(6.55, 5.62, r'$\gamma_s(t)$', fontsize=13)
    save(fig, '3.9')


# ------------------------------------------------------- 习题 7 附图 (无编号)
def fig_3_11_ex7():
    """书页 148 (p163) 习题 7: 无穷小回路 A->B->C->D->A,
    由曲线 x^1=0, x^1=da, x^2=0, x^2=db 围成."""
    fig, ax = new_ax(4.3, 3.05, (0, 10.6), (0, 6.9))

    # 四条坐标曲线
    c_x2_0 = bezier_path((3.10, 1.86), (5.60, 2.75), (9.14, 3.10))
    c_x2_db = bezier_path((4.40, 4.37), (6.90, 5.26), (10.44, 5.61))
    c_x1_0 = bezier_path((3.75, 1.31), (4.35, 3.50), (6.08, 6.06))
    c_x1_da = bezier_path((7.51, 2.13), (8.11, 4.32), (9.84, 6.88))
    for c in (c_x1_0, c_x1_da, c_x2_0, c_x2_db):
        ax.plot(c[:, 0], c[:, 1], color='k', lw=1.1)

    # 回路方向 (灰色箭头): A->B->C->D->A
    arrow(ax, (4.75, 2.42), (6.55, 2.62), lw=4.0, ms=28, color=GRAYL)
    arrow(ax, (8.80, 2.90), (9.42, 4.65), lw=4.0, ms=28, color=GRAYL)
    arrow(ax, (8.42, 5.88), (6.50, 5.55), lw=4.0, ms=28, color=GRAYL)
    arrow(ax, (4.72, 4.50), (4.10, 3.20), lw=4.0, ms=28, color=GRAYL)

    # 顶点与标注
    pts = {'A': (4.06, 2.26), 'B': (7.82, 3.08), 'C': (9.10, 5.43),
           'D': (5.36, 4.77)}
    offs = {'A': (0.18, -0.42), 'B': (0.22, -0.42), 'C': (0.28, -0.46),
            'D': (0.22, -0.46)}
    for k, (x, y) in pts.items():
        ax.plot(x, y, 'k.', ms=5.5, zorder=4)
        ax.text(x + offs[k][0], y + offs[k][1], '$%s$' % k, fontsize=13)

    # 曲线名称标注
    ax.text(3.45, 0.88, r'$x^1 = 0$', fontsize=12.5, ha='center')
    ax.text(7.60, 1.62, r'$x^1 = \delta a$', fontsize=12.5, ha='center')
    ax.text(2.10, 1.78, r'$x^2 = 0$', fontsize=12.5, ha='right')
    ax.text(3.60, 4.30, r'$x^2 = \delta b$', fontsize=12.5, ha='right')
    save(fig, '3.11-ex7')


# ---------------------------------------------------------------- 生成
if __name__ == '__main__':
    for fn in (fig_3_1, fig_3_2, fig_3_3, fig_3_4, fig_3_5, fig_3_6,
               fig_3_7, fig_3_8, fig_3_9, fig_3_11_ex7):
        fn()
    print('all done')
