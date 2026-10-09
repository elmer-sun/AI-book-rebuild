# -*- coding: utf-8 -*-
"""
B8 批次：文小刚《多体量子场论》第10章 10.1–10.13 共 13 幅插图重绘（黑白矢量）。
输出: figures/fig_10.x.pdf + figures/preview/fig_10.x.png

图目
----
10.1  H_J 基态上的开弦激发（6x4 自旋格子、偶数方块棋盘阴影、翻转自旋、U/g 项）
10.2  Z2 电荷绕四个相邻偶数方块的跳跃（闭环菱形 + 开弦 + "+" 荷 + F_i 通量标注）
10.3  三类弦 (a)T1 电通量弦 (b)T2 磁通量弦（虚线） (c)T3 弦（沿键粗虚线 + 细虚线交叉）
10.4  H_U+H_g+H_J 相图（星形线分区、SP）        [原书 p460，MinerU 漏抓，本次补]
10.5  H_U+H_g+H_t 相图（同 10.4 + 对角线"额外平移对称"标注）
10.6  费米子绕方块 1234 与绕方块 5678 的跳跃（灰色 T3 弦 + 跳跃箭头网络）
10.7  立方格子中的开弦与键的指标对 (x/x̄, y/ȳ, z/z̄)，弦端翻转 4 个阴影面
10.8  闭合回路 C 分解为 C1 与 C2
10.9  费米子从键 1 可跳到 2-11（i、j 两个格点的十字键图）
10.10 (a) 四转子系统 (b) 相应格子规范理论
10.11 (a) 三转子系统 (b) 相应格子规范理论
10.12 转子格子、低能涨落回路与电荷激发对 A、B（菱形阴影，角为转子）
10.13 (a) 闭合弦网 (b) 开弦网（端点 A、B）
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import (Circle, Ellipse, Polygon, Rectangle)

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

GRAY = '0.84'


def save(fig, key):
    fig.savefig(os.path.join(FIGDIR, f'fig_{key}.pdf'),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREVDIR, f'fig_{key}.png'),
                dpi=170, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)
    print('saved', key)


def arrow(ax, p0, p1, lw=1.0, ms=8, style='-|>', color='k', zorder=6):
    ax.annotate('', xy=p1, xytext=p0, annotation_clip=False,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms * 1.6),
                zorder=zorder)


# ================================================================ 10.1 开弦
def _spin_site(ax, x, y, r, flipped=False):
    """自旋箭头：此图中 c+y 偶 -> y 向箭头，c+y 奇 -> x 向箭头；
    flipped: 大黑圆 + 白色反向箭头。"""
    if flipped:
        ax.add_patch(Circle((x, y), r * 1.15, fc='k', ec='k', lw=0.6,
                            zorder=6))
        col, lw = 'w', 1.5
    else:
        ax.add_patch(Circle((x, y), r, fc='white', ec='k', lw=0.8, zorder=4))
        col, lw = 'k', 1.0
    d = -1 if flipped else 1
    if (x + y) % 2 == 0:                     # y 向
        arrow(ax, (x, y - d * r), (x, y), lw=lw, ms=8, color=col, zorder=7)
    else:                                    # x 向
        arrow(ax, (x, y), (x + d * r, y), lw=lw, ms=8, color=col, zorder=7)


def _lattice_checker(ax, nc=6, nr=4, dots=False, dot_r=0.09):
    for c in range(nc - 1):
        for y in range(nr - 1):
            if (c + y) % 2 == 1:
                ax.add_patch(Rectangle((c, y), 1, 1, fc=GRAY, ec='none',
                                       zorder=0))
    for c in range(nc):
        ax.plot([c, c], [0, nr - 1], color='k', lw=0.8, zorder=1)
    for y in range(nr):
        ax.plot([0, nc - 1], [y, y], color='k', lw=0.8, zorder=1)
    if dots:
        for c in range(nc):
            for y in range(nr):
                ax.add_patch(Circle((c, y), dot_r, fc='k', ec='k', zorder=6))


def _g_term_square(ax, slabels=True, right_lab=None):
    """右上角白方块 (4,2) 上的三条虚线键与 sigma 标注。"""
    for (x0, y0, x1, y1) in [(4, 2, 5, 2), (5, 1, 5, 2), (4, 1, 5, 1)]:
        ax.plot([x0, x1], [y0, y1], color='k', lw=1.6, ls=(0, (4, 3)),
                zorder=3)
    if slabels:
        ax.text(4.14, 2.72, r'$\sigma^y$', fontsize=9, zorder=8)
        ax.text(4.66, 2.72, r'$\sigma^x$', fontsize=9, zorder=8)
        ax.text(4.14, 2.18, r'$\sigma^x$', fontsize=9, zorder=8)
        ax.text(4.66, 2.18, r'$\sigma^y$', fontsize=9, zorder=8)
    if right_lab:
        ax.text(5.12, 2.45, right_lab, fontsize=10.5, ha='left', zorder=8)


def fig_10_1():
    fig, ax = plt.subplots(figsize=(4.4, 3.1))
    ax.set_xlim(-0.72, 6.1)
    ax.set_ylim(-1.02, 3.52)
    ax.set_aspect('equal')
    ax.axis('off')

    _lattice_checker(ax, 6, 4)
    flipped = {(1, 2), (2, 2), (3, 1), (4, 1)}
    for c in range(6):
        for y in range(4):
            _spin_site(ax, c, y, 0.20, (c, y) in flipped)

    pts = [(0.5, 1.5), (1, 2), (1.5, 2.5), (2, 2), (2.5, 1.5),
           (3, 1), (3.5, 0.5), (4.5, 1.5)]
    P = np.array(pts)
    ax.plot(P[:, 0], P[:, 1], color='k', lw=2.3, zorder=5,
            solid_joinstyle='miter')

    lab = dict(fontsize=10, zorder=8)
    ax.text(0.60, 2.26, r'$\sigma^y$', **lab)
    ax.text(2.28, 2.26, r'$\sigma^x$', **lab)
    ax.text(3.28, 1.26, r'$\sigma^x$', **lab)
    ax.text(4.30, 0.58, r'$\sigma^y$', **lab)

    # U 项：虚线方块 (1,0)-(2,1)
    ax.plot([1, 2, 2, 1, 1], [0, 0, 1, 1, 0], color='k', lw=1.6,
            ls=(0, (4, 3)), zorder=3)
    ax.text(1.14, 0.76, r'$\sigma^y$', fontsize=9, zorder=8)
    ax.text(1.78, 0.76, r'$\sigma^x$', fontsize=9, zorder=8)
    ax.text(1.14, 0.08, r'$\sigma^x$', fontsize=9, zorder=8)
    ax.text(1.78, 0.08, r'$\sigma^y$', fontsize=9, zorder=8)
    ax.text(1.5, -0.52, 'U term', fontsize=10.5, ha='center')

    _g_term_square(ax, right_lab='g term')

    ax.annotate('', xy=(3.5, 0.42), xytext=(3.5, -0.40),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0))
    ax.text(3.5, -0.56, 'Even plaquette', fontsize=10.5, ha='center',
            va='top')
    save(fig, '10.1')


# ================================================== 10.2 Z2 电荷跳跃
def fig_10_2():
    fig, ax = plt.subplots(figsize=(4.4, 3.1))
    ax.set_xlim(-0.32, 6.32)
    ax.set_ylim(-0.52, 3.52)
    ax.set_aspect('equal')
    ax.axis('off')

    _lattice_checker(ax, 6, 4, dots=True, dot_r=0.09)

    dia = np.array([(1.5, 2.5), (2, 2), (2.5, 1.5), (2, 1), (1.5, 0.5),
                    (1, 1), (0.5, 1.5), (1, 2), (1.5, 2.5)])
    ax.plot(dia[:, 0], dia[:, 1], color='k', lw=2.3, zorder=5)
    op = np.array([(2.5, 1.5), (3, 1), (3.5, 0.5), (4, 1), (4.5, 1.5)])
    ax.plot(op[:, 0], op[:, 1], color='k', lw=2.3, zorder=5)

    ax.plot([2.38, 2.62], [1.5, 1.5], color='k', lw=3.2, zorder=7)
    ax.plot([2.5, 2.5], [1.38, 1.62], color='k', lw=3.2, zorder=7)

    lab = dict(fontsize=9.5, zorder=8)
    ax.text(1.28, 2.26, r'$\sigma^y$', **lab)
    ax.text(2.28, 2.26, r'$\sigma^x$', **lab)
    ax.text(0.60, 0.58, r'$\sigma^x$', **lab)
    ax.text(2.28, 0.58, r'$\sigma^y$', **lab)
    ax.text(3.28, 1.26, r'$\sigma^x$', **lab)
    ax.text(4.30, 0.58, r'$\sigma^y$', **lab)

    _g_term_square(ax, right_lab=r'$F_i$')
    ax.text(4.20, 1.60, r'$F_i=-1$', fontsize=8.5, ha='left', zorder=8)
    save(fig, '10.2')


# ============================================================ 10.3 三类弦
def fig_10_3():
    fig, axs = plt.subplots(3, 1, figsize=(4.2, 8.8))
    labs = ['(a)', '(b)', '(c)']
    for k, ax in enumerate(axs):
        ax.set_xlim(-0.78, 6.32)
        ax.set_ylim(-0.66, 3.70)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.text(-0.70, 3.40, labs[k], fontsize=11)
        _lattice_checker(ax, 6, 4, dots=True, dot_r=0.09)

    F = dict(fontsize=10, style='italic')

    # ---- (a) T1 电通量弦（实线）
    a = axs[0]
    P = np.array([(0.5, 1.5), (1, 2), (1.5, 2.5), (2, 2), (2.5, 1.5),
                  (3, 1), (3.5, 0.5), (4, 1), (4.5, 1.5)])
    a.plot(P[:, 0], P[:, 1], color='k', lw=2.2, zorder=5)
    a.text(0.60, 2.26, r'$\sigma^y$', fontsize=9.5, zorder=8)
    a.text(2.28, 2.26, r'$\sigma^x$', fontsize=9.5, zorder=8)
    a.text(3.28, 1.26, r'$\sigma^x$', fontsize=9.5, zorder=8)
    a.text(4.30, 0.58, r'$\sigma^y$', fontsize=9.5, zorder=8)
    a.text(-0.12, 1.24, r'$F_i=-1$', **F)
    a.text(4.46, 1.88, r'$F_i=-1$', **F)
    a.text(2.95, 0.58, 'Electric flux string', fontsize=10, zorder=8)

    # ---- (b) T2 磁通量弦（虚线，连接奇数方块）
    b = axs[1]
    Q = np.array([(0.5, 0.5), (1, 1), (1.5, 1.5), (2, 1), (2.5, 0.5),
                  (3, 1), (4, 2), (4.5, 2.5)])
    b.plot(Q[:, 0], Q[:, 1], color='k', lw=2.4, ls=(0, (5, 3.4)), zorder=5)
    b.text(1.28, 0.58, r'$\sigma^y$', fontsize=9.5, zorder=8)
    b.text(2.28, 1.26, r'$\sigma^x$', fontsize=9.5, zorder=8)
    b.text(3.28, 0.58, r'$\sigma^y$', fontsize=9.5, zorder=8)
    b.text(4.28, 1.60, r'$\sigma^y$', fontsize=9.5, zorder=8)
    b.text(-0.12, 0.16, r'$F_i=-1$', **F)
    b.text(4.40, 2.70, r'$F_i=-1$', **F)
    b.text(1.12, 0.34, 'Magnetic flux string', fontsize=10, zorder=8)

    # ---- (c) T3 弦：沿键粗虚线 + T1/T2 细虚线交叉
    c = axs[2]
    for (sx, sy), dirs in [((1, 2), [(-1, 1), (1, 1), (1, -1), (-1, -1)]),
                           ((2, 2), [(-1, 1), (1, 1), (1, -1), (-1, -1)]),
                           ((3, 2), [(-1, 1), (1, -1)]),
                           ((3, 1), [(-1, 1), (1, 1), (1, -1), (-1, -1)])]:
        for dx, dy in dirs:
            c.plot([sx, sx + dx * 0.5], [sy, sy + dy * 0.5], color='k',
                   lw=1.2, ls=(0, (3.6, 2.8)), zorder=4)
    c.plot([0.5, 3], [2, 2], color='k', lw=3.0, ls=(0, (4.5, 3.2)),
           zorder=6)
    c.plot([3, 3], [2, 0.5], color='k', lw=3.0, ls=(0, (4.5, 3.2)),
           zorder=6)
    c.text(1.28, 1.68, r'$\sigma^z$', fontsize=9.5, zorder=8)
    c.text(2.28, 1.68, r'$\sigma^z$', fontsize=9.5, zorder=8)
    c.text(3.26, 2.22, r'$\sigma^x$', fontsize=9.5, zorder=8)
    c.text(3.24, 0.94, r'$\sigma^z$', fontsize=9.5, zorder=8)
    c.text(-0.10, 2.70, r'$F_i=-1$', **F)
    c.text(-0.10, 1.76, r'$F_i=-1$', **F)
    c.text(1.95, 0.26, r'$F_i=-1$', **F)
    c.text(3.10, 0.26, r'$F_i=-1$', **F)
    save(fig, '10.3')


# ==================================================== 10.4 / 10.5 相图
def _phase_diagram(ax, ylab, xlab, diagonal=False):
    s = 1.0
    ax.add_patch(Rectangle((-s, -s), 2 * s, 2 * s, fc='none', ec='k',
                           lw=1.3))
    xs = np.linspace(0, 1, 90)
    arc = xs ** 1.25
    ax.plot(-xs[::-1], arc[::-1], color='k', lw=1.5)
    ax.plot(xs, arc, color='k', lw=1.5)
    ax.plot(xs[::-1], -arc[::-1], color='k', lw=1.5)
    ax.plot(-xs, -arc, color='k', lw=1.5)
    ax.plot([-s, s], [0, 0], color='k', lw=0.6)
    ax.plot([0, 0], [-s, s], color='k', lw=0.6)
    if diagonal:
        ax.plot([-s, s], [-s, s], color='k', lw=0.8, ls=(0, (5, 4)))

    lab = dict(fontsize=10.5)
    ax.text(-s - 0.10, s + 0.03, r'$+\infty$', ha='right', va='bottom',
            **lab)
    ax.text(-s - 0.14, -s - 0.00, r'$-\infty$', ha='right', va='top', **lab)
    ax.text(-s - 0.10, 0, '0', ha='right', va='center', **lab)
    ax.text(-s - 0.70, 0, ylab, ha='center', va='center', fontsize=11.5)
    ax.text(-s + 0.02, -s - 0.12, r'$-\infty$', ha='center', va='top', **lab)
    ax.text(0, -s - 0.12, '0', ha='center', va='top', **lab)
    ax.text(s - 0.02, -s - 0.12, r'$+\infty$', ha='center', va='top', **lab)
    ax.text(0, -s - 0.44, xlab, ha='center', va='center', fontsize=11.5)

    L = dict(fontsize=7.8, ha='left')
    R = dict(fontsize=7.8, ha='right')
    ax.text(-0.90, 0.76, 'String condense', **L)
    ax.text(-0.90, 0.55, r'$Z_2$ flux', **L)
    ax.text(-0.90, 0.35, r'$(Z_{2b},Z_{2a})$', **L)
    ax.text(0.90, 0.76, 'String condense', **R)
    ax.text(0.90, 0.55, r'$Z_2$', **R)
    ax.text(0.90, 0.35, r'$(Z_{2a},Z_{2a})$', **R)
    ax.text(-0.90, -0.38, r'$(Z_{2b},Z_{2b})$', **L)
    ax.text(-0.90, -0.58, r'$Z_2$ flux–charge', **L)
    ax.text(-0.90, -0.79, 'String condense', **L)
    dy = 0.10 if diagonal else 0.0
    ax.text(0.90, -0.38 - dy, r'$(Z_{2a},Z_{2b})$', **R)
    ax.text(0.90, -0.58 - dy, r'$Z_2$ charge', **R)
    ax.text(0.90, -0.79 - dy, 'String condense', **R)
    ax.text(-0.12, 0.09, 'SP', fontsize=10.5, ha='center')

    if diagonal:
        ax.annotate('', xy=(-0.16, -0.18), xytext=(0.10, -0.17),
                    arrowprops=dict(arrowstyle='-|>', color='k', lw=0.9))
        ax.text(0.11, -0.06, 'Extra\ntranslational\nsymmetry',
                fontsize=7.4, ha='left', va='top', linespacing=1.15)


def fig_10_4():
    fig, ax = plt.subplots(figsize=(3.5, 3.6))
    ax.set_xlim(-1.90, 1.35)
    ax.set_ylim(-1.62, 1.26)
    ax.set_aspect('equal')
    ax.axis('off')
    _phase_diagram(ax, '$U/J$', '$g/J$')
    save(fig, '10.4')


def fig_10_5():
    fig, ax = plt.subplots(figsize=(3.5, 3.6))
    ax.set_xlim(-1.90, 1.35)
    ax.set_ylim(-1.62, 1.26)
    ax.set_aspect('equal')
    ax.axis('off')
    _phase_diagram(ax, '$U/t$', '$g/t$', diagonal=True)
    save(fig, '10.5')


# ============================================ 10.6 费米子绕方块跳跃
def fig_10_6():
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    ax.set_xlim(-0.55, 5.95)
    ax.set_ylim(-0.60, 3.58)
    ax.set_aspect('equal')
    ax.axis('off')

    _lattice_checker(ax, 6, 4, dots=True, dot_r=0.085)

    # T3 弦（灰色粗线）：键 1-2 中点 (1.5,2) -> (0,2) -> (0,1) -> 键 5-6 中点 (3.5,1)
    gp = np.array([(1.5, 2), (0, 2), (0, 1), (3.5, 1)])
    ax.plot(gp[:, 0], gp[:, 1], color='0.45', lw=3.8, zorder=4,
            solid_capstyle='round')

    def hop(p0, p1, at=0.78):
        p0 = np.array(p0, float)
        p1 = np.array(p1, float)
        arrow(ax, p0, p0 + (p1 - p0) * at, lw=1.0, ms=6)

    # 绕方块 1234（cols1-2, y2-3；键中点菱形 + 中竖线）
    hop((1.5, 2), (2, 2.5))
    hop((2, 2.5), (1.5, 3))
    hop((1.5, 3), (1, 2.5))
    hop((1, 2.5), (1.5, 2))
    hop((1.5, 2), (1.5, 3))
    hop((1, 1.5), (1.5, 2))
    hop((1.5, 2), (1, 1.5))
    hop((1, 1.5), (0.5, 2))
    # 绕方块 5678（cols3-4, y1-2）
    hop((3.5, 1), (4, 1.5))
    hop((4, 1.5), (3.5, 2))
    hop((3.5, 2), (3, 1.5))
    hop((3, 1.5), (3.5, 1))
    hop((3.5, 1), (3.5, 2))
    hop((3, 0.5), (3.5, 1))
    hop((3.5, 1), (3, 0.5))
    hop((3, 0.5), (2.5, 1))

    # T3 弦方向小箭头
    arrow(ax, (1.15, 2), (1.32, 2), lw=1.6, ms=7)
    arrow(ax, (3.15, 1), (3.32, 1), lw=1.6, ms=7)

    num = dict(fontsize=11.5, style='italic', zorder=8)
    ax.text(1.14, 1.80, '1', **num)
    ax.text(2.14, 1.80, '2', **num)
    ax.text(2.14, 2.78, '3', **num)
    ax.text(1.14, 2.78, '4', **num)
    ax.text(3.14, 0.80, '5', **num)
    ax.text(4.14, 0.80, '6', **num)
    ax.text(4.14, 1.80, '7', **num)
    ax.text(3.14, 1.80, '8', **num)
    save(fig, '10.6')


# ================================================= 10.7 立方格子开弦
def fig_10_7():
    fig, ax = plt.subplots(figsize=(5.4, 4.5))
    wx, wy = 0.46, 0.46

    def P(p):
        ix, iy, iz = p
        return (ix + wx * iy, iz + wy * iy)

    ax.set_xlim(-0.60, 3.55)
    ax.set_ylim(-0.52, 3.30)
    ax.set_aspect('equal')
    ax.axis('off')

    faces = [
        [(0, 1, 1), (1, 1, 1), (1, 2, 1), (0, 2, 1)],
        [(0, 1, 0), (1, 1, 0), (1, 2, 0), (0, 2, 0)],
        [(0, 1, 1), (1, 1, 1), (1, 1, 2), (0, 1, 2)],
        [(0, 2, 1), (1, 2, 1), (1, 2, 2), (0, 2, 2)],
    ]
    for f in faces:
        ax.add_patch(Polygon([P(p) for p in f], closed=True, fc=GRAY,
                             ec='none', zorder=1))

    bonds = []
    for ix in range(3):
        for iy in range(3):
            for iz in range(3):
                if ix < 2:
                    bonds.append(((ix, iy, iz), (ix + 1, iy, iz), 'x'))
                if iy < 2:
                    bonds.append(((ix, iy, iz), (ix, iy + 1, iz), 'y'))
                if iz < 2:
                    bonds.append(((ix, iy, iz), (ix, iy, iz + 1), 'z'))
    for s1, s2, d in bonds:
        p1, p2 = P(s1), P(s2)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='k', lw=0.7,
                zorder=2)
    over = {'x': 'x̄', 'y': 'ȳ', 'z': 'z̄'}
    for s1, s2, d in bonds:
        m = 0.5 * (np.array(P(s1)) + np.array(P(s2)))
        t = d if sum(s1) % 2 == 1 else over[d]
        ax.text(m[0], m[1], t, fontsize=6.2, ha='center', va='center',
                zorder=5, bbox=dict(fc='white', ec='none', pad=0.3))

    st = [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0.5, 1, 1)]
    Sp = [P(p) for p in st]
    for k in range(3):
        ax.plot([Sp[k][0], Sp[k + 1][0]], [Sp[k][1], Sp[k + 1][1]],
                color='k', lw=3.4, zorder=6, solid_capstyle='round')

    pi = P((0, 0, 1))
    ax.text(pi[0] - 0.16, pi[1], '$i$', fontsize=12, ha='right',
            va='center', zorder=7)
    save(fig, '10.7')


# ==================================================== 10.8 回路分解
def fig_10_8():
    fig, ax = plt.subplots(figsize=(4.3, 3.6))
    ax.set_xlim(-0.45, 5.60)
    ax.set_ylim(-0.50, 4.45)
    ax.set_aspect('equal')
    ax.axis('off')
    nc, nr = 5, 4
    for c in range(nc + 1):
        ax.plot([c, c], [0, nr], color='k', lw=0.8, zorder=1)
    for r in range(nr + 1):
        ax.plot([0, nc], [r, r], color='k', lw=0.8, zorder=1)
    for c in range(nc + 1):
        for r in range(nr + 1):
            ax.add_patch(Circle((c, r), 0.10, fc='k', ec='k', zorder=6))

    thick = [
        ((1, 3), (2, 3)), ((2, 3), (3, 3)), ((3, 3), (4, 3)),
        ((4, 1), (4, 2)), ((4, 2), (4, 3)),
        ((2, 1), (3, 1)), ((3, 1), (4, 1)),
        ((2, 0), (2, 1)),
        ((1, 0), (2, 0)),
        ((1, 0), (1, 1)), ((1, 1), (1, 2)), ((1, 2), (1, 3)),
        ((2, 2), (2, 3)), ((2, 2), (3, 2)), ((3, 1), (3, 2)),
    ]
    for (a, b) in thick:
        ax.plot([a[0], b[0]], [a[1], b[1]], color='k', lw=3.0, zorder=4,
                solid_capstyle='round')

    ax.text(1.80, 3.60, '$C$', fontsize=12, style='italic')
    arrow(ax, (1.72, 3.50), (1.40, 3.14), lw=1.0, ms=7)
    arrow(ax, (1.98, 3.50), (2.34, 3.14), lw=1.0, ms=7)
    ax.text(1.40, 1.36, '$C_1$', fontsize=12, style='italic')
    ax.text(3.55, 2.10, '$C_2$', fontsize=12, style='italic')
    save(fig, '10.8')


# ============================================ 10.9 费米子的 ten 条键
def _hop_cross(ax, cx, cy, links, labs, center_lab):
    L = 1.55
    ax.plot([cx, cx], [cy - L, cy + L], color='k', lw=0.9, zorder=1)
    ax.plot([cx - L, cx + L], [cy, cy], color='k', lw=0.9, zorder=1)
    d = 1.10
    ax.plot([cx - d, cx + d], [cy - d, cy + d], color='k', lw=0.9,
            zorder=1)
    for (px, py), vert, diag in links:
        if diag:
            e = Ellipse((px, py), 0.30, 0.15, angle=45, fc='k', ec='k',
                        zorder=5)
        elif vert:
            e = Ellipse((px, py), 0.16, 0.34, fc='k', ec='k', zorder=5)
        else:
            e = Ellipse((px, py), 0.34, 0.16, fc='k', ec='k', zorder=5)
        ax.add_patch(e)
    for t, px, py, ha, va in labs:
        ax.text(px, py, t, fontsize=11, ha=ha, va=va, zorder=6)
    ax.text(cx + 0.16, cy - 0.32, center_lab, fontsize=12,
            style='italic', zorder=6)
    # 键方向标签
    bl = dict(fontsize=8.5, ha='center', va='center', zorder=6)
    ax.text(cx - 0.30, cy + 0.10, r'$\bar{x}$', **bl)
    ax.text(cx + 0.30, cy + 0.10, r'$x$', **bl)
    ax.text(cx + 0.10, cy + 0.30, r'$z$', **bl)
    ax.text(cx + 0.10, cy - 0.30, r'$\bar{z}$', **bl)
    ax.text(cx + 0.30, cy + 0.34, r'$y$', **bl)
    ax.text(cx - 0.30, cy - 0.34, r'$\bar{y}$', **bl)


def fig_10_9():
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    ax.set_xlim(-2.5, 5.3)
    ax.set_ylim(-2.15, 2.15)
    ax.set_aspect('equal')
    ax.axis('off')

    links_i = [((0.60, 0), False, False), ((0, -0.60), True, False),
               ((-0.60, 0), False, False), ((0, 0.60), True, False),
               ((0.47, 0.47), False, True), ((-0.47, -0.47), False, True)]
    labs_i = [('1', 0.60, 0.26, 'center', 'bottom'),
              ('2', 0.17, -0.62, 'left', 'center'),
              ('3', -0.62, -0.26, 'right', 'center'),
              ('4', -0.17, 0.62, 'right', 'center'),
              ('5', 0.55, 0.74, 'center', 'bottom'),
              ('6', -0.55, -0.74, 'center', 'top')]
    _hop_cross(ax, 0, 0, links_i, labs_i, '$i$')

    links_j = [((3.10, 0), False, False), ((2.50, 0.60), True, False),
               ((2.50, -0.60), True, False), ((2.97, 0.47), False, True),
               ((2.03, -0.47), False, True)]
    labs_j = [('10', 3.10, 0.26, 'center', 'bottom'),
              ('9', 2.33, 0.62, 'right', 'center'),
              ('11', 2.33, -0.62, 'right', 'center'),
              ('7', 3.05, 0.74, 'center', 'bottom'),
              ('8', 1.95, -0.74, 'center', 'top')]
    _hop_cross(ax, 2.50, 0, links_j, labs_j, '$j$')
    save(fig, '10.9')


# ============================================ 10.10 / 10.11 转子与规范论
def _rotor_square(ax, ox, oy, s, rotors=True):
    c0 = (ox, oy + s)
    c1 = (ox + s, oy + s)
    c2 = (ox + s, oy)
    c3 = (ox, oy)
    xs = [c0[0], c1[0], c2[0], c3[0], c0[0]]
    ys = [c0[1], c1[1], c2[1], c3[1], c0[1]]
    ax.plot(xs, ys, color='k', lw=1.0, zorder=2)
    num = dict(fontsize=12, style='italic')
    ax.text(ox - 0.10 * s, oy + s + 0.10 * s, '1', ha='right', **num)
    ax.text(ox + s + 0.10 * s, oy + s + 0.10 * s, '2', ha='left', **num)
    ax.text(ox + s + 0.10 * s, oy - 0.10 * s, '3', ha='left', **num)
    ax.text(ox - 0.10 * s, oy - 0.10 * s, '4', ha='right', **num)
    if rotors:
        m0 = (ox + s / 2, oy + s)
        m1 = (ox + s, oy + s / 2)
        m2 = (ox + s / 2, oy)
        m3 = (ox, oy + s / 2)
        for m in (m0, m1, m2, m3):
            ax.add_patch(Circle(m, 0.115 * s, fc='k', ec='k', zorder=5))
        e = 0.14 * s
        arrow(ax, (ox + 0.30 * s, oy + s), (ox + s - e, oy + s), lw=1.3,
              ms=7)
        arrow(ax, (ox + s, oy + s - 0.30 * s), (ox + s, oy + e), lw=1.3,
              ms=7)
        arrow(ax, (ox + s - 0.30 * s, oy), (ox + e, oy), lw=1.3, ms=7)
        arrow(ax, (ox, oy + 0.30 * s), (ox, oy + s - e), lw=1.3, ms=7)
        lab = dict(fontsize=11)
        ax.text(m0[0], m0[1] + 0.17 * s, r'$\theta_{12}$', ha='center',
                **lab)
        ax.text(m1[0] + 0.17 * s, m1[1], r'$\theta_{23}$', ha='left',
                **lab)
        ax.text(m2[0], m2[1] - 0.15 * s, r'$\theta_{34}$', ha='center',
                va='top', **lab)
        ax.text(m3[0] - 0.17 * s, m3[1], r'$\theta_{41}$', ha='right',
                **lab)
    else:
        for p in (c0, c1, c2, c3):
            ax.add_patch(Circle(p, 0.085 * s, fc='k', ec='k', zorder=5))
        lab = dict(fontsize=11)
        ax.text(ox + s / 2, oy + s + 0.14 * s, r'$a_{12}$', ha='center',
                **lab)
        ax.text(ox + s + 0.14 * s, oy + s / 2, r'$a_{23}$', ha='left',
                **lab)
        ax.text(ox + s / 2, oy - 0.14 * s, r'$a_{34}$', ha='center', **lab)
        ax.text(ox - 0.14 * s, oy + s / 2, r'$a_{41}$', ha='right', **lab)


def fig_10_10():
    fig, ax = plt.subplots(figsize=(6.0, 2.9))
    ax.set_xlim(0.1, 6.5)
    ax.set_ylim(-0.35, 2.65)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(0.30, 2.42, '(a)', fontsize=12)
    ax.text(3.85, 2.42, '(b)', fontsize=12)
    _rotor_square(ax, 0.95, 0.30, 1.70, rotors=True)
    _rotor_square(ax, 4.45, 0.30, 1.70, rotors=False)
    save(fig, '10.10')


def fig_10_11():
    fig, ax = plt.subplots(figsize=(6.8, 2.75))
    ax.set_xlim(0.55, 7.60)
    ax.set_ylim(-0.60, 2.60)
    ax.set_aspect('equal')
    ax.axis('off')

    def draw(tri, rotors):
        p1, p2, p3 = tri
        for a, b in [(p1, p2), (p2, p3), (p3, p1)]:
            ax.plot([a[0], b[0]], [a[1], b[1]], color='k', lw=1.0, zorder=2)
        if rotors:
            m12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
            m23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
            m31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
            for m in (m12, m23, m31):
                ax.add_patch(Circle(m, 0.185, fc='k', ec='k', zorder=5))
            # 1->2 (右边缘, 箭头靠 2), 2->3 (底边, 靠 3), 3->1 (左边缘, 靠 1)
            for (pa, pb, pt) in [(p1, p2, p2), (p2, p3, p3), (p3, p1, p1)]:
                A = (pt[0] + (pa[0] - pt[0]) * 0.38,
                     pt[1] + (pa[1] - pt[1]) * 0.38)
                B = (pt[0] + (pa[0] - pt[0]) * 0.12,
                     pt[1] + (pa[1] - pt[1]) * 0.12)
                arrow(ax, A, B, lw=1.3, ms=7)
            lab = dict(fontsize=11)
            ax.text(m12[0] + 0.22, m12[1] + 0.12, r'$\theta_{12}$',
                    ha='left', **lab)
            ax.text(m23[0], m23[1] - 0.24, r'$\theta_{23}$', ha='center',
                    **lab)
            ax.text(m31[0] - 0.24, m31[1] + 0.12, r'$\theta_{31}$',
                    ha='right', **lab)
        else:
            for p in tri:
                ax.add_patch(Circle(p, 0.145, fc='k', ec='k', zorder=5))
            lab = dict(fontsize=11)
            ax.text((p1[0] + p2[0]) / 2 + 0.22, (p1[1] + p2[1]) / 2 + 0.12,
                    r'$a_{12}$', ha='left', **lab)
            ax.text((p2[0] + p3[0]) / 2, p2[1] - 0.22, r'$a_{23}$',
                    ha='center', **lab)
            ax.text((p3[0] + p1[0]) / 2 - 0.24, (p3[1] + p1[1]) / 2 + 0.12,
                    r'$a_{31}$', ha='right', **lab)
        num = dict(fontsize=12, style='italic')
        ax.text(p1[0], p1[1] + 0.16, '1', ha='center', **num)
        ax.text(p2[0] + 0.14, p2[1] - 0.02, '2', ha='left', **num)
        ax.text(p3[0] - 0.14, p3[1] - 0.02, '3', ha='right', **num)

    ax.text(0.62, 2.36, '(a)', fontsize=12)
    ax.text(4.48, 2.36, '(b)', fontsize=12)
    draw([(2.85, 2.10), (4.10, 0.05), (1.60, 0.05)], True)
    draw([(6.10, 2.10), (7.35, 0.05), (4.85, 0.05)], False)
    save(fig, '10.11')


# ============================== 10.12 / 10.13 转子格子 + 弦网公共函数
def _clip_poly(poly, nc, nr, a):
    """Sutherland–Hodgman：多边形对格子框 [0,nc]x[0,nr] 裁剪。"""
    def clip_edge(pts, inside, intersect):
        out = []
        n = len(pts)
        for k in range(n):
            cur, nxt = pts[k], pts[(k + 1) % n]
            ci, ni = inside(cur), inside(nxt)
            if ci:
                out.append(cur)
            if ci != ni:
                out.append(intersect(cur, nxt))
        return out

    pts = list(poly)
    for (inside, inter) in [
        (lambda p: p[0] >= 0,
         lambda p, q: (0, p[1] + (q[1] - p[1]) * (0 - p[0]) / (q[0] - p[0]))),
        (lambda p: p[0] <= nc * a,
         lambda p, q: (nc * a, p[1] + (q[1] - p[1]) * (nc * a - p[0])
                       / (q[0] - p[0]))),
        (lambda p: p[1] >= 0,
         lambda p, q: (p[0] + (q[0] - p[0]) * (0 - p[1]) / (q[1] - p[1]), 0)),
        (lambda p: p[1] <= nr * a,
         lambda p, q: (p[0] + (q[0] - p[0]) * (nr * a - p[1])
                       / (q[1] - p[1]), nr * a)),
    ]:
        pts = clip_edge(pts, inside, inter)
        if not pts:
            break
    return pts


def rotor_net_lattice(ax, nc, nr, a=1.0, thick_H=(), thick_V=(),
                      head_sites=()):
    """薄格子 + 转子点(键中点) + 全体格点菱形阴影(裁剪于框内) + 粗弦网 +
    弦网站点处的指向箭头对。"""
    xs = [c * a for c in range(nc + 1)]
    ys = [r * a for r in range(nr + 1)]
    ax.add_patch(Rectangle((0, 0), nc * a, nr * a, fc='white', ec='none',
                           zorder=0))
    for c in range(nc + 1):
        for r in range(nr + 1):
            dm = [(xs[c] - a / 2, ys[r]), (xs[c], ys[r] + a / 2),
                  (xs[c] + a / 2, ys[r]), (xs[c], ys[r] - a / 2)]
            dm = _clip_poly(dm, nc, nr, a)
            if len(dm) >= 3:
                ax.add_patch(Polygon(dm, closed=True, fc=GRAY, ec='none',
                                     zorder=1))
    for x in xs:
        ax.plot([x, x], [0, nr * a], color='k', lw=0.7, zorder=2)
    for y in ys:
        ax.plot([0, nc * a], [y, y], color='k', lw=0.7, zorder=2)
    for c in range(nc):
        for r in range(nr + 1):
            ax.add_patch(Circle(((xs[c] + xs[c + 1]) / 2, ys[r]), 0.088 * a,
                                fc='k', ec='k', zorder=4))
    for c in range(nc + 1):
        for r in range(nr):
            ax.add_patch(Circle((xs[c], (ys[r] + ys[r + 1]) / 2), 0.088 * a,
                                fc='k', ec='k', zorder=4))
    for (c, r) in thick_H:
        ax.plot(xs[c:c + 2], [ys[r]] * 2, color='k', lw=3.0, zorder=5,
                solid_capstyle='round')
    for (c, r) in thick_V:
        ax.plot([xs[c]] * 2, ys[r:r + 2], color='k', lw=3.0, zorder=5,
                solid_capstyle='round')

    def head(px, py, tx, ty):
        """转子位置上的箭头，指向格点（叠加在转子上，原书样式）。"""
        d = np.array([tx - px, ty - py], dtype=float)
        n = np.linalg.norm(d)
        if n < 1e-9:
            return
        d /= n
        p = np.array([px, py], dtype=float)
        tip = p + d * 0.19
        base = p + d * 0.02
        side = np.array([-d[1], d[0]]) * 0.085
        ax.add_patch(Polygon([tip, base + side, base - side], closed=True,
                             fc='k', ec='none', zorder=7))

    for (c, r) in head_sites:
        x0, y0 = xs[c], ys[r]
        cand = []
        if c > 0:
            cand.append((x0 - a / 2, y0))
        if c < nc:
            cand.append((x0 + a / 2, y0))
        if r > 0:
            cand.append((x0, y0 - a / 2))
        if r < nr:
            cand.append((x0, y0 + a / 2))
        for (px, py) in cand:
            head(px, py, x0, y0)
    # 格子边框
    ax.add_patch(Rectangle((0, 0), nc * a, nr * a, fc='none', ec='k',
                           lw=0.8, zorder=3))


def fig_10_12():
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    nc, nr = 6, 4
    ax.set_xlim(-0.06, nc + 0.06)
    ax.set_ylim(-0.48, nr + 0.06)
    ax.set_aspect('equal')
    ax.axis('off')

    thick_H = [(1, 0), (2, 1), (4, 1), (1, 3), (2, 3), (4, 3)]
    thick_V = [(1, 0), (1, 1), (1, 2), (2, 0), (3, 1), (3, 2),
               (4, 1), (4, 2)]
    sites = [(1, 0), (2, 0), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
             (1, 2), (3, 2), (4, 2), (1, 3), (2, 3), (3, 3), (4, 3),
             (5, 3)]
    rotor_net_lattice(ax, nc, nr, thick_H=thick_H, thick_V=thick_V,
                      head_sites=sites)

    # 回路方向箭头
    arrow(ax, (1.30, 3), (1.66, 3), lw=1.4, ms=6)
    arrow(ax, (3, 2.64), (3, 2.30), lw=1.4, ms=6)
    arrow(ax, (1, 1.36), (1, 1.68), lw=1.4, ms=6)
    arrow(ax, (2, 0.40), (2, 0.68), lw=1.4, ms=6)
    arrow(ax, (4.30, 1), (4.64, 1), lw=1.4, ms=6)
    arrow(ax, (4.30, 3), (4.64, 3), lw=1.4, ms=6)

    pm = dict(fontsize=11, ha='center', va='center', zorder=8)
    ax.text(1.52, 3.30, '+', **pm)
    ax.text(2.52, 3.30, '$-$', **pm)
    ax.text(4.52, 3.30, '+', **pm)
    ax.text(1.30, 2.46, '$-$', **pm)
    ax.text(3.24, 2.46, '+', **pm)
    ax.text(4.20, 2.46, '$-$', **pm)
    ax.text(1.30, 1.40, '+', **pm)
    ax.text(2.58, 1.15, '+', **pm)
    ax.text(3.24, 0.72, '$-$', **pm)
    ax.text(3.70, 0.60, '$-$', **pm)
    ax.text(4.24, 1.12, '+', **pm)
    ax.text(1.58, -0.34, '+', **pm)
    ax.text(5.24, 3.04, 'B', fontsize=12, style='italic', zorder=8)
    ax.text(5.24, 0.92, 'A', fontsize=12, style='italic', zorder=8)
    save(fig, '10.12')


def fig_10_13():
    fig, axs = plt.subplots(2, 1, figsize=(4.6, 6.4))

    a = axs[0]
    a.set_xlim(-0.06, 6.06)
    a.set_ylim(-0.06, 4.06)
    a.set_aspect('equal')
    a.axis('off')
    a.text(-0.02, 4.10, '(a)', fontsize=12, clip_on=False)
    thick_H_a = [(2, 4), (3, 4), (4, 4),
                 (1, 3), (2, 3),
                 (2, 2), (3, 2),
                 (2, 1), (4, 1),
                 (1, 0)]
    thick_V_a = [(1, 0), (1, 1), (1, 2),
                 (2, 0), (2, 2), (2, 3),
                 (3, 1), (3, 2),
                 (4, 1),
                 (5, 1), (5, 2), (5, 3)]
    sites_a = [(1, 0), (2, 0), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
               (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
               (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
               (2, 4), (3, 4), (4, 4), (5, 4)]
    rotor_net_lattice(a, 6, 4, thick_H=thick_H_a, thick_V=thick_V_a,
                      head_sites=sites_a)

    b = axs[1]
    b.set_xlim(-0.06, 6.06)
    b.set_ylim(-0.06, 4.06)
    b.set_aspect('equal')
    b.axis('off')
    b.text(-0.02, 4.10, '(b)', fontsize=12, clip_on=False)
    thick_H_b = [(3, 4),
                 (1, 3), (2, 3), (4, 3),
                 (3, 2),
                 (2, 1), (4, 1),
                 (1, 0)]
    thick_V_b = [(1, 0), (1, 1), (1, 2),
                 (2, 0),
                 (3, 1), (3, 3),
                 (4, 1), (4, 2), (4, 3)]
    sites_b = [(1, 0), (2, 0), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
               (3, 2), (4, 2),
               (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
               (3, 4), (4, 4)]
    rotor_net_lattice(b, 6, 4, thick_H=thick_H_b, thick_V=thick_V_b,
                      head_sites=sites_b)
    b.text(5.24, 3.02, 'B', fontsize=12, style='italic', zorder=8)
    b.text(5.24, 0.58, 'A', fontsize=12, style='italic', zorder=8)
    save(fig, '10.13')


if __name__ == '__main__':
    for f in [fig_10_1, fig_10_2, fig_10_3, fig_10_4, fig_10_5, fig_10_6,
              fig_10_7, fig_10_8, fig_10_9, fig_10_10, fig_10_11,
              fig_10_12, fig_10_13]:
        f()
