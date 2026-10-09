# -*- coding: utf-8 -*-
"""
B5 批次（上）：文小刚《多体量子场论》第6章 6.1–6.8 共 8 幅插图重绘（黑白矢量）。
输出: figures/fig_6.x.pdf + figures/preview/fig_6.x.png
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
    'hatch.linewidth': 0.55,
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

LW = 1.1
DASH = (4, 2.4)
GRAY = '0.82'


def save(fig, key):
    fig.savefig(os.path.join(FIGDIR, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREVDIR, 'fig_%s.png' % key),
                bbox_inches='tight', pad_inches=0.03, dpi=170)
    plt.close(fig)
    print('fig_%s done' % key)


def arrow(ax, p0, p1, lw=1.0, ms=12, style='-|>'):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, lw=lw, color='k',
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def catmull_rom(pts, n=28):
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = (np.array(P[j], float) for j in (i - 1, i, i + 1, i + 2))
        for j in range(n):
            s = j / n
            s2, s3 = s * s, s * s * s
            pt = 0.5 * ((2 * p1) + (-p0 + p2) * s
                        + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s2
                        + (-p0 + 3 * p1 - 3 * p2 + p3) * s3)
            out.append(pt)
    out.append(np.array(P[-2], float))
    return np.array(out)


def newax(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    return fig, ax


# ------------------------------------------------------- 6.1 Z2 规范理论（正方形）
def fig_6_1():
    fig, ax = newax(2.6, 2.7)
    p = {1: (0, 1), 2: (1, 1), 3: (1, 0), 4: (0, 0)}
    for i, j in [(1, 2), (2, 3), (3, 4), (4, 1)]:
        a, b = np.array(p[i], float), np.array(p[j], float)
        ax.plot(*zip(a, b), color='k', lw=LW, zorder=1)
        m, e = 0.60, 0.985
        arrow(ax, a + (b - a) * m, a + (b - a) * e, lw=LW, ms=15)
        c = a + (b - a) * 0.5
        ax.add_patch(Circle(c, 0.055, fc='k', ec='k', zorder=3))
    lab = {'1': (-0.075, 1.075, 'right', 'bottom'),
           '2': (1.075, 1.075, 'left', 'bottom'),
           '3': (1.075, -0.075, 'left', 'top'),
           '4': (-0.075, -0.075, 'right', 'top')}
    for t, (x, y, ha, va) in lab.items():
        ax.text(x, y, t, ha=ha, va=va, fontsize=11)
    ax.text(0.5, 1.09, r'$s_{12}$', ha='center', va='bottom', fontsize=10.5)
    ax.text(1.09, 0.5, r'$s_{23}$', ha='left', va='center', fontsize=10.5)
    ax.text(0.5, -0.09, r'$s_{34}$', ha='center', va='top', fontsize=10.5)
    ax.text(-0.09, 0.5, r'$s_{41}$', ha='right', va='center', fontsize=10.5)
    ax.set_xlim(-0.32, 1.32)
    ax.set_ylim(-0.30, 1.30)
    ax.set_aspect('equal')
    save(fig, '6.1')


# --------------------------------------- 6.2 跨 x 线 / y 线的链附加负号
def fig_6_2():
    fig, ax = newax(4.3, 3.3)
    x0, x1, y0, y1 = 0, 4, 0, 3
    # 细网格：5 竖线 x 4 横线
    for x in range(5):
        ax.plot([x, x], [y0 - 0.28, y1 + 0.28], color='k', lw=0.75)
    for y in range(4):
        ax.plot([x0 - 0.55, x1 + 0.85], [y, y], color='k', lw=0.75)
    # 粗链：跨 x 线（底行竖链）+ 跨 y 线（第二列横链）
    for x in range(5):
        ax.plot([x, x], [0, 1], color='k', lw=2.6, solid_capstyle='butt')
    for y in range(4):
        ax.plot([1, 2], [y, y], color='k', lw=2.6, solid_capstyle='butt')
    # x line / y line（虚线，过中央粗方格中心）
    ax.plot([1.5, 1.5], [-0.85, 4.15], color='k', lw=0.85, ls='--', dashes=DASH)
    ax.plot([-1.15, 5.75], [0.5, 0.5], color='k', lw=0.85, ls='--', dashes=DASH)
    ax.text(1.5, 4.22, r'$y$ line', ha='center', va='bottom', fontsize=10)
    ax.text(5.8, 0.5, r'$x$ line', ha='left', va='center', fontsize=10)
    # 坐标轴箭头
    arrow(ax, (4, 0), (5.1, 0), lw=1.1, ms=13)
    ax.text(5.18, 0.0, r'$x$ axis', ha='left', va='center', fontsize=10)
    arrow(ax, (1, 3.05), (1, 3.85), lw=1.1, ms=13)
    ax.text(0.88, 3.80, r'$y$ axis', ha='right', va='center', fontsize=10)
    ax.set_xlim(-1.3, 6.9)
    ax.set_ylim(-0.95, 4.6)
    ax.set_aspect('equal')
    save(fig, '6.2')


# ------------------------------------- 6.3 改变 F_i 产生 Z2 涡旋（两块 -1）
def fig_6_3():
    fig, ax = newax(3.3, 2.7)
    nc, nr = 5, 4
    for x in range(nc + 1):
        ax.plot([x, x], [0, nr], color='k', lw=0.85)
    for y in range(nr + 1):
        ax.plot([0, nc], [y, y], color='k', lw=0.85)
    for (cx, cy) in [(3, 2), (1, 1)]:
        ax.add_patch(plt.Rectangle((cx, cy), 1, 1, fc=GRAY, ec='k', lw=0.85, zorder=2))
        ax.text(cx + 0.5, cy + 0.5, r'$-1$', ha='center', va='center',
                fontsize=10.5, zorder=3)
    ax.set_xlim(-0.12, nc + 0.12)
    ax.set_ylim(-0.12, nr + 0.12)
    ax.set_aspect('equal')
    save(fig, '6.3')


# --------------------------------------------- 6.4 开放的二维正方格子
def fig_6_4():
    fig, ax = newax(3.1, 2.4)
    nc, nr = 4, 3
    for x in range(nc + 1):
        ax.plot([x, x], [0, nr], color='k', lw=1.0)
    for y in range(nr + 1):
        ax.plot([0, nc], [y, y], color='k', lw=1.0)
    ax.set_xlim(-0.1, nc + 0.1)
    ax.set_ylim(-0.1, nr + 0.1)
    ax.set_aspect('equal')
    save(fig, '6.4')


# --------------------------- 6.5 单位球面上的圈 = 两个圆盘 D 与 D' 的边界
def _blob(cx, cy, s):
    pts = [(0.02, 0.48), (-0.07, 0.72), (0.08, 0.95), (0.33, 0.90),
           (0.48, 0.70), (0.72, 0.75), (0.98, 0.93), (1.15, 0.64),
           (1.00, 0.33), (0.85, 0.23), (0.52, 0.44), (0.18, 0.22)]
    P = catmull_rom(pts + [pts[0]])
    return cx + P[:, 0] * s - 0.55 * s, cy + P[:, 1] * s - 0.55 * s


def fig_6_5():
    fig, ax = newax(4.9, 2.35)
    R = 1.0
    # 左球：圈内阴影盘 D
    ax.add_patch(Circle((0, 0), R, fc='none', ec='k', lw=1.1, zorder=3))
    bx, by = _blob(0.12, 0.12, 0.78)
    ax.fill(bx, by, facecolor='white', edgecolor='k', lw=1.0,
            hatch='///', zorder=2)
    ax.text(0.12, 0.10, r'$D$', ha='center', va='center', fontsize=11,
            zorder=4, bbox=dict(fc='white', ec='none', pad=0.6))
    # 右球：阴影球面扣除白洞 D'
    ax.add_patch(Circle((2.75, 0), R, fc='white', ec='k', lw=1.1,
                        hatch='///', zorder=1))
    bx2, by2 = _blob(2.87, 0.12, 0.78)
    ax.fill(bx2, by2, facecolor='white', edgecolor='k', lw=1.0, zorder=2)
    ax.text(2.05, -0.55, r"$D'$", ha='center', va='center', fontsize=11,
            zorder=4, bbox=dict(fc='white', ec='none', pad=1.2))
    ax.set_xlim(-1.25, 4.05)
    ax.set_ylim(-1.22, 1.22)
    ax.set_aspect('equal')
    save(fig, '6.5')


# ------------------- 6.6 XY 模型涡旋–反涡旋对：θ 限制在阴影区（线性禁闭）
def fig_6_6():
    fig, ax = newax(4.9, 1.75)
    xa, xb = 0.0, 4.0
    H = 0.66
    x = np.linspace(xa, xb, 800)
    h = H * np.clip(1 - (np.abs(x - 2) / 2.0) ** 1.7, 0, 1) ** 0.6
    ax.fill_between(x, -h, h, color=GRAY, zorder=1)
    for f in (1.0, 0.66, 0.37):
        for sg in (1, -1):
            ax.plot(x, sg * f * h, color='k', lw=1.0, ls='--', dashes=DASH,
                    zorder=2)
    ax.plot([xa, xb], [0, 0], color='k', lw=1.2, zorder=3)
    for px in (xa, xb):
        ax.add_patch(Circle((px, 0), 0.105, fc='k', ec='k', zorder=4))
    bb = dict(fc='white', ec='none', pad=1.5)
    ax.text(2.0, H + 0.07, r'$\theta=0$', ha='center', va='bottom', fontsize=10.5)
    ax.text(2.0, -H - 0.07, r'$\theta=0$', ha='center', va='top', fontsize=10.5)
    ax.text(2.16, 0.37 * H, r'$\theta=\pi$', ha='center', va='center',
            fontsize=10.5, zorder=5, bbox=bb)
    ax.text(2.16, -0.37 * H, r'$\theta=-\pi$', ha='center', va='center',
            fontsize=10.5, zorder=5, bbox=bb)
    ax.set_xlim(-0.28, 4.28)
    ax.set_ylim(-1.06, 1.06)
    ax.set_aspect('equal')
    save(fig, '6.6')


# ----------------------------------------- 6.7/6.8 正方形上的 U(1) 规范理论
def _u1_square(diagonal):
    fig, ax = newax(2.7, 2.75)
    p = {1: (0, 1), 2: (1, 1), 3: (1, 0), 4: (0, 0)}
    edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
    if diagonal:
        edges.append((4, 2))
    for i, j in edges:
        ax.plot(*zip(p[i], p[j]), color='k', lw=LW, zorder=1)
    for i, (x, y) in p.items():
        ax.add_patch(Circle((x, y), 0.062, fc=GRAY, ec='k', lw=0.9, zorder=3))
    ax.text(-0.09, 1.09, '1', ha='right', va='bottom', fontsize=11)
    ax.text(1.09, 1.09, '2', ha='left', va='bottom', fontsize=11)
    ax.text(1.09, -0.09, '3', ha='left', va='top', fontsize=11)
    ax.text(-0.09, -0.09, '4', ha='right', va='top', fontsize=11)
    ax.text(0.5, 1.08, r'$a_{12}$', ha='center', va='bottom', fontsize=10.5)
    ax.text(1.08, 0.5, r'$a_{23}$', ha='left', va='center', fontsize=10.5)
    ax.text(0.5, -0.08, r'$a_{34}$', ha='center', va='top', fontsize=10.5)
    ax.text(-0.08, 0.5, r'$a_{41}$', ha='right', va='center', fontsize=10.5)
    if diagonal:
        ax.text(0.36, 0.60, r'$a_{24}$', ha='center', va='center', fontsize=10.5)
    ax.set_xlim(-0.42, 1.42)
    ax.set_ylim(-0.38, 1.38)
    ax.set_aspect('equal')
    return fig, ax


def fig_6_7():
    fig, ax = _u1_square(False)
    save(fig, '6.7')


def fig_6_8():
    fig, ax = _u1_square(True)
    save(fig, '6.8')


if __name__ == '__main__':
    for f in (fig_6_1, fig_6_2, fig_6_3, fig_6_4,
              fig_6_5, fig_6_6, fig_6_7, fig_6_8):
        f()
