# -*- coding: utf-8 -*-
"""
Concepts in Solids 第 3 章激子部分插图重绘（批次 ch3c）
  fig_42         : p149 能级图（E_k(p) 带、E_p(atomic)、E_s，U / E_o / E_k(p)-E_k(s) 箭头）
  fig_43         : p153 sigma_j / b_j 能级阶梯与锯齿 "Barrier"
  fig_44         : p155 纵偶极波：偶极子箭头 + 电荷行（node / antinode）
  fig_45         : p158 光子-激子色散劈裂
  exciton-jkj    : p149 无编号 Frenkel 激子组态示意（p/s 能级，j、k、j'）
  dipole-t       : p156 无编号 T_t 等效图像（椭球 + 电容 + 细棒）
  dipole-l       : p156 无编号 T_l 等效图像（圆柱内平行朝上偶极子，上 + 下 -）
输出 figures/fig_{key}.pdf 与 figures/preview/fig_{key}.png
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Rectangle, FancyBboxPatch

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


def _smooth(pts, n=60):
    """Catmull-Rom 样条平滑过点曲线，返回 (x, y)。"""
    pts = np.asarray(pts, float)
    P = np.vstack([pts[0], pts, pts[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (p2 - p0) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-2])
    return np.array(out).T


def _halfsig(t, L, R):
    """0->R 的 S 形过渡：两端水平、中段陡（用于图 42 粗曲线臂）。"""
    t = np.asarray(t, float)
    t0, b = L / 2.0, 2.7 / L
    return R * (np.tanh(b * (t - t0)) - np.tanh(-b * t0)) / \
           (np.tanh(b * (L - t0)) - np.tanh(-b * t0))


# ----------------------------------------------------------------------
def fig_42():
    fig, ax = _canvas(3.55, 3.6)
    # 能级线：E_p(atomic) 三重线 与 E_s
    for y in (4.73, 4.50, 4.27):
        ax.plot([0.55, 7.30], [y, y], 'k-', lw=1.1)
    ax.plot([0.55, 7.30], [0.80, 0.80], 'k-', lw=1.1)
    # 细带曲线 E_k(p)（过腰点的缓拱）
    c = np.polyfit([1.25, 3.39, 6.78], [7.28, 7.49, 7.16], 2)
    xt = np.linspace(1.25, 6.78, 120)
    ax.plot(xt, np.polyval(c, xt), 'k-', lw=1.0)
    # 领结：两条粗 S 曲线在腰点相切交叉
    wx, wy = 3.39, 7.48
    t = np.linspace(0, 1.72, 80)
    ax.plot(wx - t, wy + _halfsig(t, 1.72, 0.68), 'k-', lw=2.0)   # 左上臂
    t = np.linspace(0, 1.50, 80)
    ax.plot(wx + t, wy + _halfsig(t, 1.50, 0.68), 'k-', lw=2.0)   # 右上臂
    t = np.linspace(0, 1.15, 80)
    ax.plot(wx + t, wy - _halfsig(t, 1.15, 0.89), 'k-', lw=2.0)   # 右下臂
    t = np.linspace(0, 1.41, 80)
    ax.plot(wx - t, wy - _halfsig(t, 1.41, 0.89), 'k-', lw=2.0)   # 左下臂
    # 双向箭头
    dbl = dict(arrowstyle='<|-|>', mutation_scale=11, lw=1.1, color='k')
    ax.annotate('', xy=(wx, 4.74), xytext=(wx, 7.34), arrowprops=dbl)      # U
    ax.annotate('', xy=(4.83, 0.82), xytext=(4.83, 7.36), arrowprops=dbl)  # E_k(p)-E_k(s)
    ax.annotate('', xy=(2.30, 4.23), xytext=(2.30, 0.82), arrowprops=dbl)  # E_o
    # 标注
    ax.text(3.55, 6.00, r'$U$', ha='left', va='center')
    ax.text(6.95, 7.27, r'$E_k(p)$', ha='left', va='center')
    ax.text(7.45, 4.35, r'$E_p$ (atomic)', ha='left', va='center')
    ax.text(7.45, 0.80, r'$E_s$', ha='left', va='center')
    ax.text(2.12, 2.60, r'$E_o$', ha='right', va='center')
    ax.text(4.98, 2.60, r'$E_k(p)-E_k(s)$', ha='left', va='center')
    ax.set_xlim(0, 9.3)
    ax.set_ylim(-0.9, 8.7)
    _save(fig, '42')


# ----------------------------------------------------------------------
def fig_43():
    fig, ax = _canvas(4.05, 2.6)
    y0, y1, y2, y3, y4 = 1.20, 2.27, 3.34, 4.38, 5.45   # n_j = 0..4
    # 左列 sigma_j（只有 0、1 两级）与右列 b_j（完整阶梯）
    ax.plot([0.00, 2.60], [y1, y1], 'k-', lw=1.2)
    ax.plot([0.00, 2.60], [y0, y0], 'k-', lw=1.2)
    for y in (y0, y1, y2, y3, y4):
        ax.plot([5.09, 7.50], [y, y], 'k-', lw=1.2)
    # 锯齿 "Barrier"（介于 1、2 之间，横跨两列）
    xs = np.linspace(0.36, 7.86, 16)
    ys = np.empty(16)
    ys[0], ys[-1] = 2.81, 2.57
    ys[1::2] = 2.99    # 峰
    ys[2:-1:2] = 2.57  # 谷
    ax.plot(xs, ys, 'k-', lw=1.2)
    # 右侧级别标注
    ax.text(7.68, y4, '4', ha='left', va='center')
    ax.text(7.68, y3, '3', ha='left', va='center')
    ax.text(7.68, y2, '2', ha='left', va='center')
    ax.text(8.15, 2.92, '"Barrier"', ha='left', va='center', fontsize=10)
    ax.text(7.68, y1, '1', ha='left', va='center')
    ax.text(7.68, y0, r'$n_j=0$', ha='left', va='center')
    # 列标签与图注
    ax.text(1.30, 0.72, r'$\sigma_j$', ha='center', va='center')
    ax.text(6.30, 0.72, r'$b_j$', ha='center', va='center')
    ax.set_xlim(-0.3, 9.9)
    ax.set_ylim(-0.65, 5.8)
    _save(fig, '43')


# ----------------------------------------------------------------------
def fig_44():
    fig, ax = _canvas(4.8, 2.2)
    cols = [1.8, 11.0, 20.2, 29.4, 38.6]
    for x in cols:
        _arrow(ax, (x, 28.6), (x, 26.8))            # 下
        ax.text(x, 25.0, r'$+$', ha='center', va='center')
        _arrow(ax, (x, 21.1), (x, 23.0))            # 上
        ax.text(x, 19.4, r'$-$', ha='center', va='center')
        _arrow(ax, (x, 17.5), (x, 15.7))            # 下
        ax.text(x, 14.1, r'$+$', ha='center', va='center')
    ax.text(40.4, 25.0, 'node', ha='left', va='center', fontsize=9.5)
    ax.text(40.4, 19.4, 'antinode', ha='left', va='center', fontsize=9.5)
    ax.set_xlim(0, 48)
    ax.set_ylim(7.9, 29.7)
    _save(fig, '44')


# ----------------------------------------------------------------------
def fig_45():
    fig, ax = _canvas(3.6, 2.95)
    # 坐标轴（原书为无箭头直线）
    ax.plot([0.52, 0.52], [0.27, 6.94], 'k-', lw=1.3)
    ax.plot([0.52, 9.71], [0.27, 0.27], 'k-', lw=1.3)
    ax.text(0.15, 6.85, r'$\omega$', ha='left', va='center')
    ax.text(9.85, 0.27, r'$k$', ha='left', va='center')
    ax.text(0.38, 3.42, r'$\omega_r$', ha='right', va='center')
    # 光子直线（斜率 c）
    ax.plot([0.52, 4.34], [0.27, 6.94], 'k-', lw=1.5)
    # 激子缓升曲线
    ex = _smooth([(0.52, 3.74), (1.5, 3.80), (2.5, 3.92),
                  (3.5, 4.10), (4.5, 4.35), (5.55, 4.61)])
    ax.plot(ex[0], ex[1], 'k-', lw=1.5)
    # 劈裂虚线：上支（自 omega_L 附近出发并入光子线）、下支（自原点出发并入激子线）
    up = _smooth([(0.52, 4.02), (1.0, 4.08), (1.6, 4.22), (2.3, 4.52),
                  (3.0, 5.00), (3.6, 5.60), (3.9, 6.00), (4.1, 6.20)])
    ax.plot(up[0], up[1], 'k--', lw=1.4, dashes=(4.5, 2.5))
    lo = _smooth([(0.52, 0.28), (0.9, 0.62), (1.3, 0.80), (1.9, 1.05),
                  (2.6, 1.50), (3.4, 2.30), (4.2, 3.20), (4.9, 3.90),
                  (5.45, 4.35)])
    ax.plot(lo[0], lo[1], 'k--', lw=1.4, dashes=(4.5, 2.5))
    # 标注
    ax.text(4.55, 6.30, 'Photon\n(slope = $c$)', ha='left', va='top', fontsize=10)
    ax.text(5.75, 4.61, 'Exciton', ha='left', va='center')
    ax.set_xlim(0, 10.3)
    ax.set_ylim(-0.8, 7.4)
    _save(fig, '45')


# ----------------------------------------------------------------------
def fig_exciton_jkj():
    fig, ax = _canvas(2.9, 1.05)
    xt = [2.6, 5.6, 8.3]           # 格点 j, k, j'
    hl = 0.62                      # 能级半长
    # p 行
    for x in xt:
        ax.plot([x - hl, x + hl], [2.30, 2.30], 'k-', lw=1.3)
    ax.text(0.55, 2.30, r'$p$', ha='center', va='center')
    ax.text(2.6, 2.74, r'$\ominus$', ha='center', va='center', fontsize=10)
    _arrow(ax, (3.10, 2.76), (5.52, 2.50), ms=11, lw=1.2, rad=-0.35)
    ax.text(4.00, 2.30, r'$+\,U$', ha='center', va='center', fontsize=10.5)
    # s 行
    for x in xt:
        ax.plot([x - hl, x + hl], [0.75, 0.75], 'k-', lw=1.3)
    ax.text(0.55, 0.75, r'$s$', ha='center', va='center')
    ax.text(5.6, 1.19, r'$\ominus$', ha='center', va='center', fontsize=10)
    ax.text(8.3, 1.19, r'$\ominus$', ha='center', va='center', fontsize=10)
    ax.text(2.6, 0.18, r'$j$', ha='center', va='center')
    ax.text(5.6, 0.18, r'$k$', ha='center', va='center')
    ax.text(8.3, 0.18, r"$j'$", ha='center', va='center')
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.15, 3.35)
    _save(fig, 'exciton-jkj')


# ----------------------------------------------------------------------
def fig_dipole_t():
    fig, ax = _canvas(4.6, 2.11)
    # ---- 椭球：内嵌交替反向的横向偶极子阵列 ----
    cx, cy, ea, eb = 10.85, 15.30, 8.6, 6.7
    ax.add_patch(Ellipse((cx, cy), 2 * ea, 2 * eb, fill=False, lw=1.5))
    rows = [3, 2, 1, 0, -1, -2, -3]
    for k in rows:
        dy = 5.6 * k / 3.0
        y = cy + dy
        halfw = ea * np.sqrt(max(1.0 - (dy / eb) ** 2, 0.0))
        n = 3 if abs(dy) / eb > 0.70 else 5
        m = 1.6 if n == 3 else 0.7          # 顶/底行更向内收
        usable = 2 * (halfw - m)
        L = (usable - 0.85 * (n - 1)) / n
        left = cx - usable / 2.0 - m
        d = -1 if k % 2 == 1 else 1         # 顶行(k=3)向左，交替
        for i in range(n):
            x0 = left + m + 0.425 + i * (L + 0.85)
            if d > 0:
                _arrow(ax, (x0, y), (x0 + L, y), ms=8, lw=1.1)
            else:
                _arrow(ax, (x0 + L, y), (x0, y), ms=8, lw=1.1)
    # 椭球边缘交替电荷
    angles = [105, 79.3, 53.6, 27.9, 2.1, -23.6, -49.3, -75,
              -100.7, -126.4, -152.1, 182.1, 156.4, 130.7]
    for i, th in enumerate(angles):
        sgn = r'$+$' if i % 2 == 0 else r'$-$'
        t = np.deg2rad(th)
        phi = np.arctan2(ea * np.sin(t), eb * np.cos(t))
        px, py = ea * np.cos(phi), eb * np.sin(phi)
        nx, ny = eb * np.cos(phi), ea * np.sin(phi)
        nn = np.hypot(nx, ny)
        ax.text(cx + px + 1.5 * nx / nn, cy + py + 1.5 * ny / nn, sgn,
                ha='center', va='center', fontsize=9)
    ax.text(25.8, 15.2, 'which is equivalent to', ha='left', va='center',
            fontsize=8.5)
    # ---- 细棒（两端 -、+，内部箭头同向）----
    ax.add_patch(Rectangle((3.0, 4.2), 14.5, 1.9, fill=False, lw=1.2))
    ax.text(1.9, 5.15, r'$-$', ha='center', va='center', fontsize=10)
    ax.text(18.6, 5.15, r'$+$', ha='center', va='center', fontsize=10)
    for i in range(3):
        x0 = 4.5 + i * 4.0
        _arrow(ax, (x0, 5.15), (x0 + 2.9, 5.15), ms=8, lw=1.1)
    ax.text(21.2, 5.15, 'or', ha='center', va='center', fontsize=9)
    # ---- 充电平行板电容器 ----
    ax.add_patch(Rectangle((29.0, 0.98), 12.25, 7.6, fill=False, lw=1.4))
    ax.plot([28.2, 28.2], [0.30, 9.30], 'k-', lw=2.2)
    ax.plot([42.1, 42.1], [0.30, 9.30], 'k-', lw=2.2)
    ax.plot([23.2, 28.2], [4.80, 4.80], 'k-', lw=1.3)
    ax.plot([42.1, 46.6], [4.80, 4.80], 'k-', lw=1.3)
    for v in (2.2, 3.85, 5.5, 7.15):
        ax.text(30.0, v, r'$+$', ha='center', va='center', fontsize=9)
        ax.text(40.3, v, r'$-$', ha='center', va='center', fontsize=9)
        for i in range(3):
            x0 = 31.6 + i * 2.7
            _arrow(ax, (x0 + 1.9, v), (x0, v), ms=8, lw=1.1)
        ax.text(26.9, v, r'$-$', ha='center', va='center', fontsize=9)
        ax.text(43.4, v, r'$+$', ha='center', va='center', fontsize=9)
    ax.set_xlim(0, 48)
    ax.set_ylim(0, 22)
    _save(fig, 'dipole-t')


# ----------------------------------------------------------------------
def fig_dipole_l():
    fig, ax = _canvas(3.2, 1.17)
    ax.add_patch(FancyBboxPatch((1.2, 3.4), 27.6, 5.6,
                                boxstyle='round,pad=0,rounding_size=2.2',
                                fill=False, lw=1.4))
    for i in range(11):
        x = 1.2 + 27.6 * (i + 0.5) / 11.0
        _arrow(ax, (x, 3.9), (x, 8.5), ms=9, lw=1.1)
        ax.text(x, 10.4, r'$+$', ha='center', va='center', fontsize=10)
        ax.text(x, 2.2, r'$-$', ha='center', va='center', fontsize=10)
    ax.set_xlim(0, 30)
    ax.set_ylim(0.8, 11.8)
    _save(fig, 'dipole-l')


if __name__ == '__main__':
    for f in (fig_42, fig_43, fig_44, fig_45,
              fig_exciton_jkj, fig_dipole_t, fig_dipole_l):
        f()
        print('done:', f.__name__)
