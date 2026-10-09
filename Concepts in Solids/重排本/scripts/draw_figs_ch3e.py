# -*- coding: utf-8 -*-
"""
Concepts in Solids 第 3 章磁性部分插图重绘（批次 ch3e）
  fig_53 : p173 电子带 U+E(k) 与空穴带 E(k) 双曲线，水平基准线，两极小间双向箭头 U
  fig_54 : p177 交替自旋子晶格阵列（3x6 圆圈+自旋箭头），j/k 间自旋波弯曲箭头
  fig_55 : p179 自洽方程 (dE)^3-U(dE)^2 = -2UZ|b/U|^2 的图解曲线
  fig_56 : p182 球坐标示意：x,y,z 轴 + z' 轴，theta / phi 双向弧箭头，z' 投影虚线
  fig_57 : p191 简单立方交错子格 A/B 阵列（3x3），S_j（中心 A）与 S_l（上中 B）
输出 figures/fig_{key}.pdf 与 figures/preview/fig_{key}.png
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
})

BASE = r'E:\AI整理书籍\安德森\重排本'
FIGS = os.path.join(BASE, 'figures')
PREV = os.path.join(FIGS, 'preview')
os.makedirs(PREV, exist_ok=True)


def _canvas(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    return fig, ax


def _save(fig, key):
    fig.savefig(os.path.join(FIGS, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, 'fig_%s.png' % key), dpi=150,
                bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


def _arrow(ax, p0, p1, ms=10, lw=1.1, style='-|>', rad=0.0):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, mutation_scale=ms,
                                lw=lw, color='k',
                                connectionstyle='arc3,rad=%g' % rad))


# ----------------------------------------------------------------------
def fig_53():
    """p173: 电子带与空穴带（同一形状曲线，竖移 U），水平基准线相切。"""
    fig, ax = _canvas(4.6, 2.14)
    cx = 4.8                       # 公共极小/极点竖直线
    # 水平基准线
    ax.plot([0.28, 9.32], [0, 0], 'k-', lw=1.0)
    s = np.linspace(0, 1, 240)
    # 电子带：两端平台 +1.6，中部极小切于基线
    ye = 1.6 * (0.5 + 0.5 * np.cos(2 * np.pi * s))
    ax.plot(2.17 + 5.26 * s, ye, 'k-', lw=1.7)
    # 空穴带：两端在基线上，中部极小 -1.55
    yh = -1.55 * (0.5 - 0.5 * np.cos(2 * np.pi * s))
    ax.plot(1.865 + 5.87 * s, yh, 'k-', lw=1.7)
    # U 双向箭头（中间留字豁口）
    up = dict(arrowstyle='-|>', mutation_scale=10, lw=1.2, color='k')
    ax.annotate('', xy=(cx, 0.0), xytext=(cx, -0.60), arrowprops=up)
    ax.annotate('', xy=(cx, -1.55), xytext=(cx, -0.95), arrowprops=up)
    ax.text(cx, -0.775, r'$U$', ha='center', va='center')
    # 标注
    ax.text(2.00, 1.60, 'Electron band', ha='right', va='center')
    ax.text(7.60, 1.60, r'$U+E(k)$', ha='left', va='center')
    ax.text(1.72, -0.13, 'Hole band', ha='right', va='top')
    ax.text(7.87, -0.13, r'$E(k)$', ha='left', va='top')
    ax.set_xlim(-0.10, 10.00)
    ax.set_ylim(-2.65, 2.05)
    _save(fig, '53')


# ----------------------------------------------------------------------
def fig_54():
    """p177: 3x6 交替自旋阵列；底行 j 格自旋微倾，j<->k 两条弯曲交换箭头。"""
    fig, ax = _canvas(3.8, 2.12)
    rows = [2.0, 1.0, 0.0]
    pat = [[1, -1, 1, -1, 1, -1],
           [-1, 1, -1, 1, -1, 1],
           [1, -1, 1, -1, 1, -1]]
    dx, da, hl, r = 0.30, 0.27, 0.27, 0.075   # 箭头偏移、半长、圈半径
    for iy, y in enumerate(rows):
        for ix in range(6):
            ax.add_patch(plt.Circle((ix, y), r, fill=False, lw=1.2))
            x = ix + dx
            if pat[iy][ix] > 0:
                _arrow(ax, (x, y - hl), (x, y + hl), ms=9, lw=1.3)
            else:
                _arrow(ax, (x, y + hl), (x, y - hl), ms=9, lw=1.3)
    # j 格（底行第 3 列）：自旋微倾（顶端向左偏 ~4 度）
    jx, kx, y0 = 2.0, 3.0, 0.0
    _arrow(ax, (jx + dx + 0.02, y0 - hl), (jx + dx - 0.02, y0 + hl),
           ms=9, lw=1.3)
    # 顶部弯曲箭头：从 k 圈上方弧向左，指向 j 自旋顶端
    _arrow(ax, (kx, y0 + 0.32), (jx + dx - 0.14, y0 + 0.27),
           ms=9, lw=1.2, rad=-0.30)
    # 底部弯曲箭头：从 j 圈下方弧向右指向 k
    _arrow(ax, (jx - 0.04, y0 - 0.25), (kx - 0.10, y0 - 0.25),
           ms=9, lw=1.2, rad=-0.30)
    ax.text(jx - 0.08, y0 - 0.33, r'$j$', ha='center', va='center')
    ax.text(kx - 0.02, y0 - 0.33, r'$k$', ha='center', va='center')
    ax.set_xlim(-0.55, 5.60)
    ax.set_ylim(-1.20, 2.62)
    _save(fig, '54')


# ----------------------------------------------------------------------
def fig_55():
    """p179: dE/U 对 2Z|b/U|^2 的自洽曲线 x = y^2(1-y)（x 以 4/27 为单位）。"""
    fig, ax = _canvas(4.4, 2.00)
    # 轴线（原书为无箭头直线）
    ax.plot([0, 0], [0, 1.0], 'k-', lw=1.3)
    ax.plot([0, 2.90], [0, 0], 'k-', lw=1.3)
    # 曲线 x = y^2 (1-y)，x 以 4/27 为单位
    ys = np.linspace(0, 1, 300)
    ax.plot(ys ** 2 * (1 - ys) * 27.0 / 4.0, ys, 'k-', lw=1.7)
    # 2/3 虚线 与 4/27 竖直线
    ax.plot([0, 1], [2.0 / 3.0, 2.0 / 3.0], 'k--', lw=1.1, dashes=(5, 3))
    ax.plot([1, 1], [0, 2.0 / 3.0], 'k-', lw=1.3)
    # 标注（2/3、dE/U 按原书叠式分数）
    ax.text(-0.05, 1.13, r'$\frac{\Delta E}{U}$', ha='right', va='center',
            fontsize=12)
    ax.text(-0.05, 2.0 / 3.0, r'$\frac{2}{3}$', ha='right', va='center',
            fontsize=12)
    ax.text(1.0, -0.07, '4/27', ha='center', va='top', fontsize=10.5)
    ax.text(3.05, 0.0, r'$2Z\,|\frac{b}{U}|^2$', ha='left', va='center',
            fontsize=12)
    ax.set_xlim(-0.45, 4.05)
    ax.set_ylim(-0.85, 1.38)
    _save(fig, '55')


# ----------------------------------------------------------------------
def fig_56():
    """p182: 球坐标示意 —— x,y,z 轴、z' 轴、z' 端点投影虚线、theta/phi 弧。"""
    fig, ax = _canvas(3.2, 3.15)
    # 主轴
    ax.plot([0, 0], [0, 4.5], 'k-', lw=1.5)                 # z
    ax.plot([0, 4.7], [0, 0], 'k-', lw=1.5)                 # y
    ax.plot([0, -3.05], [0, -2.95], 'k-', lw=1.5)           # x
    ax.plot([0, 3.0], [0, 3.0], 'k-', lw=1.5)               # z'
    # z' 端点向下的竖直虚线 与 原点到垂足的投影线
    ax.plot([3.0, 3.0], [3.0, -1.75], 'k--', lw=1.2, dashes=(5, 3))
    ax.plot([0, 3.0], [0, -1.75], 'k-', lw=1.5)
    # theta 双向弧（z 与 z' 之间）
    t = np.deg2rad(45)
    _arrow(ax, (0, 1.10), (1.10 * np.cos(t), 1.10 * np.sin(t)),
           ms=7, lw=1.1, style='<|-|>', rad=0.22)
    ax.text(0.62, 1.42, r'$\theta$', ha='center', va='center')
    # phi 双向弧（x 轴与投影线之间，经过下方）
    a0, a1 = np.deg2rad(224), np.deg2rad(330)
    _arrow(ax, (1.20 * np.cos(a0), 1.20 * np.sin(a0)),
           (1.20 * np.cos(a1), 1.20 * np.sin(a1)),
           ms=7, lw=1.1, style='<|-|>', rad=-0.28)
    ax.text(-0.05, -1.48, r'$\phi$', ha='center', va='center')
    # 轴标签
    ax.text(0, 4.75, r'$z$', ha='center', va='center')
    ax.text(3.05, 3.28, r"$z'$", ha='left', va='center')
    ax.text(5.05, 0, r'$y$', ha='left', va='center')
    ax.text(-3.20, -3.12, r'$x$', ha='center', va='center')
    ax.set_xlim(-3.60, 5.40)
    ax.set_ylim(-3.90, 5.05)
    _save(fig, '56')


# ----------------------------------------------------------------------
def fig_57():
    """p191: A/B 交错子格 3x3 阵列；中心 A 格标 S_j，上中 B 格标 S_l。"""
    fig, ax = _canvas(3.3, 2.05)
    cols = [0.0, 1.5, 3.0]
    rows = [1.56, 0.78, 0.0]
    letter = [['A', 'B', 'A'],
              ['B', 'A', 'B'],
              ['A', 'B', 'A']]
    special = {(0, 1): r'$S_\ell$', (1, 1): r'$S_j$'}   # (row, col)
    for iy, y in enumerate(rows):
        for ix, x in enumerate(cols):
            ax.text(x - 0.20, y, letter[iy][ix], ha='center', va='center')
            ax.add_patch(plt.Circle((x, y), 0.06, fill=False, lw=1.1))
            if (iy, ix) in special:
                ax.text(x + 0.20, y, special[(iy, ix)],
                        ha='left', va='center')
    ax.set_xlim(-0.75, 4.05)
    ax.set_ylim(-0.95, 2.20)
    _save(fig, '57')


if __name__ == '__main__':
    for f in (fig_53, fig_54, fig_55, fig_56, fig_57):
        f()
        print('done:', f.__name__)
