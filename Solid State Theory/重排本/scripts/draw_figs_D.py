# -*- coding: utf-8 -*-
"""
李正中《固体理论》(第2版) 中文重排本 插图重绘 第五批：
第八章 图8.1-8.10（10幅）+ 第九章 图9.1（1幅）+ 第十章 图10.1-10.6（6幅）
+ 第十二章 图12.1-12.9（9幅）+ 附录 图D.1、图E.1 + 习题图1，共 29 幅。
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p-309/313/318/323/324/327/328/329/373/
391/392/394/404/406/408/507/518/527/531/533/537/540/546/551/570/572/581）。
注：图8.6 在 p-324 右上；图10.4 实际在 p-404 顶部（p-403 为正文提及页）；
    图D.1 在 p-570；图E.1 在 p-572；习题图1 在 p-581 右下；
    各图 (a)(b)(c) 面板小题注与图注均由 chNN/appX.tex 排印，图内不含。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Rectangle, Circle, Ellipse, Polygon, FancyArrowPatch
from scipy.interpolate import PchipInterpolator

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = r"E:\AI整理书籍\李正中\重排本"
FIGD = os.path.join(BASE, 'figures')
PRED = os.path.join(FIGD, 'preview')
os.makedirs(PRED, exist_ok=True)

LW_MAIN, LW_AUX = 1.2, 0.8
DASH = (5, 2.2)


def save(fig, n):
    fig.savefig(os.path.join(FIGD, f'fig{n}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRED, f'fig{n}.png'), bbox_inches='tight',
                pad_inches=0.03, dpi=220)
    plt.close(fig)


def arrow_axis(ax, x0, y0, x1, y1, lw=LW_MAIN):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=12))


def plain_axes(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def tick(ax, x, y, dx, dy, lw=0.9):
    ax.plot([x, x + dx], [y, y + dy], 'k-', lw=lw)


def dbarr(ax, x0, x1, y, ms=11, lw=1.0):
    ax.annotate('', xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def curvey(ax, pts, **kw):
    """Pchip 平滑曲线，pts = [(x, y), ...]"""
    f = PchipInterpolator([p[0] for p in pts], [p[1] for p in pts])
    xx = np.linspace(pts[0][0], pts[-1][0], max(120, len(pts) * 12))
    kw.setdefault('lw', 1.4)
    ax.plot(xx, f(xx), color='k', **kw)
    return f


def leader(ax, xy_from, xy_to, lw=0.9, ms=9):
    ax.annotate('', xy=xy_to, xytext=xy_from,
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


# ================================================================ 图8.1
def fig_8_1():
    """布洛赫函数在离子实区的振荡特征：ψ_k 尖峰 + V(r) 深阱"""
    fig, ax = plt.subplots(figsize=(5.6, 2.1))
    plain_axes(ax)
    ax.set_xlim(-0.5, 8.45)
    ax.set_ylim(-1.85, 1.45)

    arrow_axis(ax, -0.28, 0, 8.15, 0, lw=1.1)
    ax.text(8.2, -0.02, r'$r$', fontsize=11, ha='left', va='center')
    for xc in (1.93, 5.89):
        ax.plot([xc, xc], [1.18, -1.62], 'k-', lw=0.9)
    # ψ_k 曲线
    pts = [(0.05, 0.40), (0.5, 0.52), (0.95, 0.55), (1.35, 0.42), (1.65, 0.22),
           (1.80, 0.10), (1.88, 0.55), (1.93, 1.00), (1.99, 0.52), (2.07, -0.08),
           (2.25, -0.30), (2.5, -0.37), (2.75, -0.30), (3.0, -0.05), (3.25, 0.28),
           (3.5, 0.46), (3.75, 0.50), (4.0, 0.42), (4.25, 0.20), (4.5, -0.10),
           (4.75, -0.30), (5.0, -0.36), (5.25, -0.28), (5.5, -0.06), (5.65, 0.06),
           (5.78, -0.10), (5.89, -0.42), (6.0, -0.10), (6.12, 0.30), (6.27, 0.45),
           (6.42, 0.38), (6.57, 0.14), (6.72, 0.30), (6.92, 0.42), (7.15, 0.22),
           (7.4, -0.14), (7.55, -0.24)]
    curvey(ax, pts, lw=1.4)
    # V(r) 曲线（三段，在离子实竖线处断开）
    curvey(ax, [(0.05, -0.40), (0.55, -0.68), (1.1, -1.02), (1.62, -1.42)], lw=1.5)
    curvey(ax, [(2.24, -1.42), (2.9, -0.78), (3.55, -0.47), (4.2, -0.53),
                (4.7, -0.85), (5.1, -1.25), (5.55, -1.42)], lw=1.5)
    curvey(ax, [(6.22, -1.42), (6.6, -0.95), (7.05, -0.58), (7.5, -0.45),
                (7.8, -0.42)], lw=1.5)
    # 标注
    ax.text(3.42, 0.78, r'$\psi_k$', fontsize=10.5, ha='center', va='center')
    leader(ax, (3.32, 0.68), (2.95, 0.38))
    ax.text(3.05, -1.2, r'$V(\boldsymbol{r})$', fontsize=10.5,
            ha='center', va='center')
    leader(ax, (2.88, -1.16), (2.6, -0.82))
    save(fig, '8-1')


# ================================================================ 图8.2
def fig_8_2():
    """平面波 / 离子实波 / 正交化平面波（三行，圆圈为离子实）"""
    fig, ax = plt.subplots(figsize=(5.1, 6.0))
    plain_axes(ax)
    ax.set_xlim(-0.75, 5.75)
    ax.set_ylim(-9.6, 1.35)
    ax.set_aspect('equal')

    def ions(y0):
        ax.plot([-0.55, 5.55], [y0, y0], 'k-', lw=1.1)
        for i in range(5):
            ax.add_patch(Circle((0.5 + i, y0), 0.33, fill=False, lw=1.4, ec='k'))
            ax.plot([0.5 + i], [y0], 'ko', ms=2.6)

    def spikes(pts, y0, a=1.0):
        f = PchipInterpolator([p[0] for p in pts], [p[1] for p in pts])
        xx = np.linspace(pts[0][0], pts[-1][0], 200)
        ax.plot(xx, y0 + a * f(xx), 'k-', lw=1.4)

    def wiggles(y0):
        """各离子实处的急剧振荡（自设各点形态，照原书分布）"""
        spikes([(0.14, 0), (0.24, 0.10), (0.32, 1.35), (0.38, 0.55), (0.44, 1.15),
                (0.52, -0.45), (0.60, -0.92), (0.68, -0.25), (0.76, 0)], y0)
        spikes([(1.28, 0), (1.36, 0.35), (1.43, 1.0), (1.50, 0.1), (1.57, -0.78),
                (1.64, 0.28), (1.71, 0.12), (1.78, 0)], y0)
        spikes([(2.34, 0), (2.42, 0.30), (2.5, -0.42), (2.58, 0.22),
                (2.66, 0)], y0)
        spikes([(3.30, 0), (3.38, 0.55), (3.46, -0.60), (3.54, 0.48),
                (3.62, -0.18), (3.70, 0)], y0)
        spikes([(4.20, 0), (4.28, 0.55), (4.35, 1.05), (4.42, 0.30),
                (4.50, 0.95), (4.58, -0.35), (4.66, -1.55), (4.74, -1.72),
                (4.82, -1.15), (4.92, -0.30), (5.02, 0)], y0)

    # (a) 平面波
    ions(0)
    xx = np.linspace(-0.1, 5.15, 400)
    ax.plot(xx, 0.62 * np.cos(2 * np.pi * (xx - 0.55) / 7.0), 'k-', lw=1.5)
    # (b) 离子实波
    yb = -3.55
    ions(yb)
    wiggles(yb)
    # (c) 正交化平面波（虚线长波 + 实线 = 长波 + 芯区振荡）
    yc = -7.35
    ions(yc)

    def longwave(x):
        return 0.52 * np.cos(2 * np.pi * (x - 0.75) / 6.8) - 0.05

    xx = np.linspace(-0.1, 5.35, 400)
    ax.plot(xx, yc + longwave(xx), 'k--', lw=1.2, dashes=(5, 2.5))
    base = longwave(xx)
    solid = base.copy()
    for cx, amp in [(0.5, 1.35), (1.5, 0.95), (2.5, 0.42), (3.5, 0.72),
                    (4.5, 1.5)]:
        solid = solid + amp * np.sin(2 * np.pi * (xx - cx) / 0.46) * \
            np.exp(-((xx - cx) / 0.30) ** 2)
    ax.plot(xx, yc + solid, 'k-', lw=1.4)
    save(fig, '8-2')


# ================================================================ 图8.3
def fig_8_3():
    """用于离子的模型赝势：χ_k 光滑、ψ 芯区振荡、V(r) 库仑阱与 U_M 平台"""
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    plain_axes(ax)
    ax.set_xlim(-2.65, 2.65)
    ax.set_ylim(-1.85, 1.55)
    aM = 0.85
    ax.plot([-2.55, 2.55], [0, 0], 'k-', lw=1.0)
    ax.plot([0, 0], [1.38, -1.72], 'k-', lw=1.0)
    # χ_k 圆顶
    curvey(ax, [(-2.45, 0.05), (-1.8, 0.20), (-1.2, 0.48), (-0.6, 0.78),
                (0, 0.93), (0.6, 0.78), (1.2, 0.48), (1.8, 0.20), (2.45, 0.05)],
           lw=1.5)
    # ψ 芯区振荡
    curvey(ax, [(-0.83, 0.84), (-0.70, 0.52), (-0.55, -0.32), (-0.50, -0.40),
                (-0.42, -0.28), (-0.30, 0.10), (-0.16, 0.50), (-0.06, 0.95),
                (0, 1.13), (0.06, 0.95), (0.16, 0.50), (0.30, 0.10),
                (0.42, -0.28), (0.50, -0.40), (0.55, -0.32), (0.70, 0.52),
                (0.83, 0.84)], lw=1.5)
    # 轴上刻度 -a_M, a_M
    for sgn in (-1, 1):
        tick(ax, sgn * aM, 0, 0, -0.055)
    ax.text(-aM, -0.12, r'$-a_M$', fontsize=10.5, ha='center', va='top')
    ax.text(aM, -0.12, r'$a_M$', fontsize=10.5, ha='center', va='top')
    # V(r) 两支
    vpts = [(-2.45, -0.12), (-1.8, -0.28), (-1.2, -0.56), (-0.85, -0.86),
            (-0.5, -1.26), (-0.22, -1.66)]
    curvey(ax, vpts, lw=1.6)
    curvey(ax, [(-x, y) for x, y in vpts][::-1], lw=1.6)
    # U_M 虚线平台 + 外侧平滑虚线
    ax.plot([-0.76, 0.76], [-0.70, -0.70], 'k--', lw=1.1, dashes=(5, 2.5))
    dpts = [(-2.45, -0.09), (-2.2, -0.18), (-1.8, -0.35), (-1.4, -0.63),
            (-1.0, -0.90), (-0.76, -0.84)]
    for sgn in (-1, 1):
        ax.plot([sgn * 0.76, sgn * 0.76], [-0.70, -0.84], 'k--', lw=1.1,
                dashes=(5, 2.5))
        xs = [sgn * x for x, _ in dpts]
        ys = [y for _, y in dpts]
        if sgn < 0:
            ax.plot(xs, ys, 'k--', lw=1.0, dashes=(5, 2.5))
        else:
            ax.plot(xs[::-1], ys[::-1], 'k--', lw=1.0, dashes=(5, 2.5))
    # 标注
    ax.text(0.62, 1.30, r'$\chi_k$', fontsize=10.5, ha='left', va='center')
    leader(ax, (0.58, 1.20), (0.38, 0.99))
    ax.text(0.44, 0.58, r'$\psi$', fontsize=10.5, ha='left', va='center')
    leader(ax, (0.55, 0.56), (0.72, 0.48))
    ax.text(1.72, 1.10, r'$\psi$', fontsize=10.5, ha='center', va='center')
    leader(ax, (1.62, 1.02), (1.35, 0.72))
    ax.text(0.30, -0.56, r'$U_M$', fontsize=10.5, ha='left', va='center')
    ax.text(1.02, -1.36, r'$V(r)$', fontsize=10.5, ha='left', va='center')
    save(fig, '8-3')


# ================================================================ 图8.4
def fig_8_4():
    """晶体势 / 赝势 / 布洛赫函数 / 赝波函数（四条带，无坐标轴）"""
    fig, ax = plt.subplots(figsize=(6.0, 4.5))
    plain_axes(ax)
    ax.set_xlim(-0.25, 10.65)
    ax.set_ylim(-4.65, 0.35)

    def wells(y0, depth, hw=0.60, x0=0.9, n=6, period=1.5):
        xx = np.linspace(0.12, 10.28, 1200)
        y = np.zeros_like(xx)
        for k in range(n):
            xi = x0 + period * k
            d = np.abs(xx - xi)
            m = d < hw
            y[m] = np.minimum(y[m], -depth * (1 - d[m] / hw) ** 2)
        # 两端半阱（部分在图外）
        for xi in (x0 - period, x0 + period * n):
            d = np.abs(xx - xi)
            m = d < hw
            y[m] = np.minimum(y[m], -depth * (1 - d[m] / hw) ** 2)
        ax.plot(xx, y0 + y, 'k-', lw=1.5)

    # (a) 晶体势 V(r)
    wells(0.0, 0.42)
    for k in range(6):
        ax.plot([0.9 + 1.5 * k], [0.10], 'ko', ms=3.4)
    ax.text(6.85, -0.60, r'$V(\boldsymbol{r})$', fontsize=10.5,
            ha='left', va='center')
    # (b) 赝势 U_M
    yb = -1.42
    wells(yb, 0.12, hw=0.42)
    for k in range(6):
        ax.plot([0.9 + 1.5 * k], [yb + 0.10], 'ko', ms=3.4)
    ax.text(6.85, yb - 0.30, r'$U_M$', fontsize=10.5, ha='left', va='center')
    # (c) 布洛赫函数 ψ_k（折线，带尖角的不规则振荡）
    yc = -2.72
    pts = [(0.12, -0.06), (0.35, 0.06), (0.52, -0.14), (0.66, 0.30), (0.78, -0.26),
           (0.9, 0.10), (1.05, 0.36), (1.3, 0.30), (1.55, 0.12), (1.75, 0.18),
           (2.0, 0.04), (2.2, -0.08), (2.42, -0.20), (2.6, -0.24), (2.8, 0.02),
           (2.95, -0.16), (3.1, -0.34), (3.3, -0.42), (3.5, -0.16), (3.66, 0.10),
           (3.8, -0.10), (4.0, 0.14), (4.15, -0.02), (4.3, 0.22), (4.5, 0.10),
           (4.72, -0.06), (4.9, -0.22), (5.1, 0.06), (5.3, 0.26), (5.55, 0.32),
           (5.8, 0.16), (6.0, -0.06), (6.2, -0.18), (6.42, 0.06), (6.6, 0.22),
           (6.8, 0.04), (7.0, -0.16), (7.15, -0.08), (7.3, -0.32), (7.5, -0.16),
           (7.68, 0.10), (7.85, 0.16), (8.05, -0.04), (8.25, -0.28),
           (8.45, -0.38), (8.62, -0.16), (8.8, -0.26), (9.05, -0.10),
           (9.3, -0.20), (9.55, -0.08), (9.8, -0.16), (10.05, -0.10),
           (10.28, -0.13)]
    ax.plot([p[0] for p in pts], [yc + p[1] for p in pts], 'k-', lw=1.3)
    doty = {2.6: -0.24, 4.3: 0.22, 6.6: 0.22, 8.45: -0.38}
    for xd, yv in doty.items():
        ax.plot([xd], [yc + yv], 'ko', ms=3.6)
    ax.text(7.6, yc - 0.56, r'$\psi_k$', fontsize=10.5, ha='left', va='center')
    # (d) 赝波函数 χ_k
    yd = -4.12
    f = PchipInterpolator([0.12, 0.8, 1.6, 2.4, 3.2, 4.0, 4.8, 5.4, 6.2, 7.0,
                           7.8, 8.6, 9.4, 10.15],
                          [-0.04, 0.12, 0.22, 0.10, -0.12, -0.24, -0.15, 0.05,
                           0.22, 0.12, -0.10, -0.22, -0.18, -0.02])
    xx = np.linspace(0.12, 10.15, 300)
    ax.plot(xx, yd + f(xx), 'k-', lw=1.5)
    for xd in (1.4, 4.05, 5.9, 8.7):
        ax.plot([xd], [yd], 'ko', ms=3.6)
    ax.text(7.45, yd - 0.34, r'$\chi_k$', fontsize=10.5, ha='left', va='center')
    save(fig, '8-4')


# ================================================================ 图8.5
def fig_8_5():
    """金属 Na 导带底的维格纳-赛茨波函数 ψ_0(r)"""
    fig, ax = plt.subplots(figsize=(3.3, 3.0))
    plain_axes(ax)
    ax.set_xlim(-0.52, 4.85)
    ax.set_ylim(-0.165, 0.175)

    arrow_axis(ax, 0, -0.155, 0, 0.165)
    arrow_axis(ax, 0, 0, 4.7, 0, lw=1.0)
    ax.text(-0.07, 0.155, r'$\psi_0$', fontsize=10.5, ha='right', va='center')
    for v in (0.04, 0.08, 0.12):
        tick(ax, 0, v, -0.055, 0)
        tick(ax, 0, -v, -0.055, 0)
        ax.text(-0.075, v, f'{v:.2f}', fontsize=8, ha='right', va='center')
        ax.text(-0.075, -v, f'{v:.2f}', fontsize=8, ha='right', va='center')
    ax.text(-0.075, 0, '0', fontsize=8, ha='right', va='center')
    for v in (1, 2, 3, 4):
        tick(ax, v, 0, 0, -0.008)
        ax.text(v, -0.012, str(v), fontsize=8.5, ha='center', va='top')
    ax.text(4.62, -0.028, r'$r/a_{\rm H}$', fontsize=10, ha='center', va='top')

    curvey(ax, [(0.02, 0.125), (0.2, 0.105), (0.4, 0.070), (0.6, 0.020),
                (0.8, -0.040), (0.95, -0.085), (1.15, -0.122), (1.35, -0.105),
                (1.6, -0.030), (1.8, 0.030), (2.1, 0.065), (2.5, 0.081),
                (2.9, 0.083), (3.3, 0.079), (3.96, 0.070)], lw=1.5)
    save(fig, '8-5')


# ================================================================ 图8.6
def fig_8_6():
    """维格纳-赛茨波函数（晶体，虚线）和自由原子 3s 波函数（实线）"""
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    plain_axes(ax)
    ax.set_xlim(-0.55, 5.35)
    ax.set_ylim(-0.95, 1.18)

    arrow_axis(ax, 0.15, -0.88, 0.15, 1.06)
    arrow_axis(ax, 0.0, 0, 5.15, 0, lw=1.0)
    ax.text(5.08, -0.05, r'$r$', fontsize=10.5, ha='center', va='top')
    ax.text(-0.06, -0.05, r'$O$', fontsize=9.5, ha='right', va='top')
    # 自由原子 3s（实线）
    curvey(ax, [(0.15, 0.82), (0.3, 0.55), (0.45, 0.10), (0.6, -0.30),
                (0.75, -0.55), (0.9, -0.62), (1.05, -0.50), (1.25, -0.20),
                (1.45, 0.08), (1.7, 0.30), (2.0, 0.48), (2.3, 0.58),
                (2.6, 0.62), (2.9, 0.60), (3.3, 0.52), (3.7, 0.40),
                (4.1, 0.27), (4.5, 0.16), (4.78, 0.10)], lw=1.5)
    # 晶体（虚线）：hump 后趋平
    curvey(ax, [(0.15, 0.82), (0.3, 0.55), (0.45, 0.10), (0.6, -0.30),
                (0.75, -0.55), (0.9, -0.62), (1.05, -0.50), (1.25, -0.20),
                (1.45, 0.08), (1.7, 0.30), (2.0, 0.48), (2.2, 0.575),
                (2.4, 0.64), (2.65, 0.665), (2.95, 0.665), (3.3, 0.658),
                (3.7, 0.650), (4.1, 0.642), (4.35, 0.638)], ls='--', lw=1.1,
           dashes=(5, 2.5))
    # r_s 竖线
    ax.plot([3.3, 3.3], [0, 0.80], 'k-', lw=1.0)
    tick(ax, 3.3, 0, 0, -0.04)
    ax.text(3.3, -0.075, r'$r_{\rm s}$', fontsize=10, ha='center', va='top')
    # 标注
    ax.text(2.42, 0.92, u'晶体', fontsize=9.5, ha='center', va='center')
    leader(ax, (2.5, 0.84), (2.62, 0.70))
    ax.text(1.28, 0.35, r'$\psi_{3s}$', fontsize=10, ha='center', va='center')
    ax.text(4.05, 0.40, u'自由原子', fontsize=9.5, ha='left', va='center')
    save(fig, '8-6')


# ================================================================ 图8.7
def fig_8_7():
    """元胞法势：边界处实线导数不连续（尖峰），虚线为平滑势"""
    fig, ax = plt.subplots(figsize=(4.6, 2.3))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-1.78, 1.78)
    ax.set_ylim(-1.18, 0.66)

    ax.plot([-1.62, 1.62], [0, 0], 'k-', lw=1.0)
    for b in (-1, 0, 1):
        ax.plot([b, b], [0.38, -1.02], 'k-', lw=0.9)
    # ⊘（离子实位置）
    for x in (-0.5, 0.5):
        ax.add_patch(Circle((x, 0), 0.055, fc='white', ec='k', lw=1.0,
                            hatch='/////'))
    # 实线：元胞法势（边界尖峰）
    for b, xa, xb in [(-1, -1.46, -0.56), (0, -0.44, 0.44), (1, 0.56, 1.46)]:
        xx = np.linspace(xa, xb, 200)
        ax.plot(xx, -0.03 - 3.0 * (xx - b) ** 2, 'k-', lw=1.7)
        ax.plot([b], [-0.02], 'ko', ms=4.5)
    # 虚线：平滑势
    for b in (-1, 0, 1):
        xx = np.linspace(b - 0.36, b + 0.36, 100)
        ax.plot(xx, -0.17 - 1.38 * (xx - b) ** 2, 'k--', lw=1.0, dashes=(4, 2.2))
    ax.text(0.02, 0.50, u'W-S 界', fontsize=9.5, ha='center', va='bottom')
    save(fig, '8-7')


# ================================================================ 图8.8
def fig_8_8():
    """M-T 球：六角排列的丸盒（hexagon 元胞 + 内切圆）"""
    fig, ax = plt.subplots(figsize=(3.2, 2.35))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(0, 4.55)
    ax.set_ylim(0, 3.35)
    R = 0.52
    r = 0.28
    hexv = np.array([(R, 0), (R / 2, np.sqrt(3) * R / 2), (-R / 2, np.sqrt(3) * R / 2),
                     (-R, 0), (-R / 2, -np.sqrt(3) * R / 2), (R / 2, -np.sqrt(3) * R / 2)])
    for j in range(-1, 9):
        y = 0.45 + 0.45 * j
        xoff = 0.78 if j % 2 else 0.0
        for i in range(-1, 4):
            x = 0.52 + 1.56 * i + xoff
            if x < -R or x > 4.55 + R:
                continue
            ax.add_patch(Polygon(hexv + [x, y], closed=True, fill=False,
                                 ec='k', lw=1.0))
            ax.add_patch(Circle((x, y), r, fill=False, ec='k', lw=1.0))
    save(fig, '8-8')


# ================================================================ 图8.9
def fig_8_9():
    """M-T 势：常数势零线上悬挂窄深阱，离子位置以黑点标记"""
    fig, ax = plt.subplots(figsize=(4.1, 0.9))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(0.1, 6.35)
    ax.set_ylim(-1.15, 0.14)
    ax.plot([0.25, 6.1], [0, 0], 'k-', lw=1.3)
    for xd in (0.65, 1.95, 3.25, 4.55, 5.85):
        ax.plot([xd], [0], 'ko', ms=4.5)
    for c in (1.3, 2.6, 3.9, 5.2):
        w, H, s = 0.20, 1.02, 0.05
        t = np.linspace(0, 1, 60)
        ax.plot(c - w + s * t ** 2, -H * t, 'k-', lw=1.5)
        ax.plot(c + w - s * t ** 2, -H * t, 'k-', lw=1.5)
    save(fig, '8-9')


# ================================================================ 图8.10
def fig_8_10():
    """APW 示意图：r<r_1 球函数展开 ΣaYR，r>r_1 平面波 e^{ikr}"""
    fig, ax = plt.subplots(figsize=(3.6, 2.5))
    plain_axes(ax)
    ax.set_xlim(-0.42, 4.55)
    ax.set_ylim(-0.9, 1.12)

    arrow_axis(ax, 0.18, -0.82, 0.18, 1.0)
    arrow_axis(ax, 0.0, 0, 4.4, 0, lw=1.0)
    ax.text(0.06, 0.92, r'$\phi_k$', fontsize=10.5, ha='right', va='center')
    ax.text(0.10, -0.03, r'$O$', fontsize=9.5, ha='right', va='top')
    ax.text(4.33, -0.05, r'$r$', fontsize=10.5, ha='left', va='center')
    # 实线 φ_k
    curvey(ax, [(0.18, 0.92), (0.3, 0.60), (0.45, 0.10), (0.6, -0.33),
                (0.78, -0.52), (0.95, -0.45), (1.12, -0.20), (1.28, 0.10),
                (1.42, 0.28), (1.55, 0.32), (1.68, 0.27), (1.82, 0.24),
                (1.95, 0.25), (2.1, 0.31), (2.3, 0.40), (2.5, 0.43),
                (2.7, 0.39), (2.9, 0.26), (3.1, 0.0), (3.3, -0.33),
                (3.5, -0.50), (3.7, -0.52), (3.9, -0.40), (4.1, -0.15),
                (4.25, 0.06), (4.35, 0.22)], lw=1.5)
    # 虚线 e^{ikr}
    curvey(ax, [(0.18, -0.02), (0.35, -0.14), (0.55, -0.30), (0.75, -0.38),
                (0.95, -0.32), (1.15, -0.15), (1.35, 0.08), (1.55, 0.28),
                (1.75, 0.40), (1.95, 0.42), (2.15, 0.33), (2.35, 0.15),
                (2.55, -0.08), (2.75, -0.28), (2.95, -0.40), (3.15, -0.40),
                (3.35, -0.30), (3.5, -0.22)], ls='--', lw=1.0, dashes=(5, 2.5))
    # r_1 竖线
    ax.plot([1.55, 1.55], [0, 0.72], 'k-', lw=0.9)
    ax.text(1.55, -0.075, r'$r_1$', fontsize=10, ha='center', va='top')
    # 标注
    ax.text(0.78, 0.70, r'$\Sigma aYR$', fontsize=10, ha='center', va='center')
    leader(ax, (0.62, 0.60), (0.42, 0.42))
    ax.text(2.68, 0.56, r'$\mathrm{e}^{\mathrm{i}k\boldsymbol{r}}$',
            fontsize=10, ha='left', va='center')
    save(fig, '8-10')


# ================================================================ 图9.1
def fig_9_1():
    """f(α) 曲线（LLP 中间耦合理论的缓变函数）"""
    fig, ax = plt.subplots(figsize=(3.2, 2.9))
    plain_axes(ax)
    ax.set_xlim(-0.6, 8.85)
    ax.set_ylim(0.92, 1.62)

    arrow_axis(ax, 0, 0.95, 0, 1.585)
    arrow_axis(ax, 0, 0.95, 8.7, 0.95, lw=1.0)
    ax.text(-0.09, 1.555, r'$f(\alpha)$', fontsize=10.5, ha='right',
            va='center')
    ax.text(8.62, 0.925, r'$\alpha$', fontsize=10.5, ha='center', va='top')
    for k in range(11):
        v = 1.0 + 0.05 * k
        tick(ax, 0, v, -0.07, 0)
        ax.text(-0.095, v, f'{v:.1f}', fontsize=8, ha='right', va='center')
    for k in range(9):
        tick(ax, k, 0.95, 0, -0.017)
        ax.text(k, 0.928, str(k), fontsize=8, ha='center', va='top')
    curvey(ax, [(0, 1.0), (0.5, 1.018), (1, 1.045), (1.5, 1.07), (2, 1.10),
                (2.5, 1.13), (3, 1.165), (3.5, 1.20), (4, 1.235), (4.5, 1.27),
                (5, 1.30), (5.5, 1.33), (6, 1.36), (6.5, 1.39), (7, 1.42),
                (7.5, 1.44), (8, 1.46)], lw=1.5)
    save(fig, '9-1')


# ================================================================ 图10.1
def fig_10_1():
    """激子能级：导带/价带（斜线影区）+ n=1,2,3 激子能级 + 跃迁箭头"""
    fig, ax = plt.subplots(figsize=(3.4, 3.7))
    plain_axes(ax)
    ax.set_xlim(0, 7.65)
    ax.set_ylim(-0.1, 8.85)

    # 导带
    ax.add_patch(Rectangle((0.75, 8.12), 6.55, 0.68, fc='white', ec='none',
                           hatch='/////'))
    ax.plot([0.75, 7.3], [8.12, 8.12], 'k-', lw=2.0)
    ax.text(4.0, 8.46, u'导带', fontsize=9.5, ha='center', va='center',
            bbox=dict(fc='white', ec='none', pad=0.4))
    # 价带
    ax.add_patch(Rectangle((0.75, 0.06), 6.55, 0.68, fc='white', ec='none',
                           hatch='/////'))
    ax.plot([0.75, 7.3], [0.75, 0.75], 'k-', lw=2.0)
    ax.text(4.0, 0.40, u'价带', fontsize=9.5, ha='center', va='center',
            bbox=dict(fc='white', ec='none', pad=0.4))
    ax.text(0.58, 0.75, r'$0$', fontsize=10, ha='right', va='center')
    # 激子能级（n=3 逼近导带底，间距照原书比例）
    yn = {1: 5.2, 2: 6.6, 3: 7.56}
    for n, y in yn.items():
        ax.plot([0.95, 3.7], [y, y], 'k-', lw=2.2)
        ax.text(3.95, y, f'$n={n}$', fontsize=10, ha='left', va='center')
    ax.text(0.55, yn[2], r'$E_1$', fontsize=10.5, ha='right', va='center')
    # 花括号 + 激子能级
    ax.annotate('', xy=(4.78, yn[3]), xytext=(4.78, yn[1]),
                arrowprops=dict(arrowstyle='-', color='k', lw=0.9,
                                connectionstyle='bar,fraction=0.12'))
    ax.text(5.05, (yn[1] + yn[3]) / 2, u'激子能级', fontsize=9.5,
            ha='left', va='center')
    # 跃迁箭头（0 → n=1, n=2, n=2, n=3，照原书）
    for x, ytop in [(1.5, yn[1]), (2.1, yn[2]), (2.62, yn[2]), (3.25, yn[3])]:
        ax.annotate('', xy=(x, ytop), xytext=(x, 0.78),
                    arrowprops=dict(arrowstyle='-|>', color='k', lw=1.3,
                                    shrinkA=0, shrinkB=0, mutation_scale=11))
    save(fig, '10-1')


# ================================================================ 图10.2
def fig_10_2():
    """局域激发态：n 格点电子自 s 态激发至 p 态"""
    fig, ax = plt.subplots(figsize=(4.6, 1.5))
    plain_axes(ax)
    ax.set_xlim(-1.25, 5.85)
    ax.set_ylim(-0.62, 2.05)

    hl = 0.27
    yp, ys = 1.55, 0.75
    for i in range(6):
        ax.plot([i - hl, i + hl], [yp, yp], 'k-', lw=2.0)
        ax.plot([i - hl, i + hl], [ys, ys], 'k-', lw=2.0)
    ax.plot([3], [yp], 'ko', ms=4.6)                    # p 态：n 格点占据
    for i in (0, 1, 2, 4, 5):                           # s 态：n 格点空
        ax.plot([i], [ys], 'ko', ms=4.6)
    ax.text(-0.55, yp, u'p态', fontsize=9.5, ha='right', va='center')
    ax.text(-0.55, ys, u's态', fontsize=9.5, ha='right', va='center')
    ax.text(-0.55, 0.0, u'格点', fontsize=9.5, ha='right', va='center')
    labs = ['1', '2', r'$\cdots$', r'$n$', r'$n{+}1$', r'$\cdots$']
    for i, s in enumerate(labs):
        ax.text(i, -0.06, s, fontsize=9.5, ha='center', va='top')
    save(fig, '10-2')


# ================================================================ 图10.3
def fig_10_3():
    """积分 I 的计算图：K 沿 z 轴，μ 与 R 夹角 θ_0、θ、θ' 及方位角 φ"""
    fig, ax = plt.subplots(figsize=(4.0, 3.9))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-2.85, 3.25)
    ax.set_ylim(-2.75, 2.85)
    O = np.array([0.0, 0.0])
    Rs = 1.5           # 球面三角弧所在半径
    Rsil = 1.9         # 球轮廓虚线半径

    uz = np.array([0.0, 1.0])
    um = np.array([-0.76, 0.65]) / np.hypot(0.76, 0.65)
    ur = np.array([0.74, 0.68]) / np.hypot(0.74, 0.68)

    def slerp(a, b, t):
        w = np.arccos(np.clip(a @ b, -1, 1))
        if w < 1e-9:
            return a
        return (np.sin((1 - t) * w) * a + np.sin(t * w) * b) / np.sin(w)

    def arc(a, b, n=60, **kw):
        ts = np.linspace(0, 1, n)
        pts = Rs * np.array([slerp(a, b, t) for t in ts])
        ax.plot(pts[:, 0], pts[:, 1], color='k', **kw)

    def P(v, r=1.0):
        return (v[0] * r, v[1] * r)

    # 球轮廓（虚线圆）
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(Rsil * np.cos(th), Rsil * np.sin(th), 'k--', lw=0.8,
            dashes=(4, 2.5))
    # 球面三角（实线弧）：μ-z、z-R、μ-R
    arc(um, uz, lw=1.6)
    arc(uz, ur, lw=1.6)
    arc(um, ur, lw=1.6)
    # 虚线经线：μ、R 向下绕到前下方
    dmb = np.array([-0.35, -0.94])
    drb = np.array([0.50, -0.87])
    arc(um, dmb, ls='--', lw=0.9, dashes=(4, 2.2))
    arc(ur, drb, ls='--', lw=0.9, dashes=(4, 2.2))
    # φ 弧（实线粗）：x 轴方向到 R 经线足
    dxs = np.array([-0.86, -0.51])
    arc(dxs, drb, lw=1.8)
    ax.text(0.02, -1.98, r'$\phi$', fontsize=11, ha='center', va='center')
    # 坐标轴
    ax.annotate('', xy=(0, 2.35), xytext=(0, -1.6),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                mutation_scale=12))
    ax.annotate('', xy=(-2.15, -1.3), xytext=O,
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                mutation_scale=12))
    ax.annotate('', xy=(2.7, -0.8), xytext=O,
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                mutation_scale=12))
    ax.text(0.12, 2.32, r'$z$', fontsize=11, ha='left', va='center')
    ax.text(-0.30, 2.15, r'$\boldsymbol{K}$', fontsize=11, ha='right',
            va='center')
    ax.text(-2.25, -1.5, r'$x$', fontsize=11, ha='center', va='center')
    ax.text(2.8, -1.0, r'$y$', fontsize=11, ha='center', va='center')
    # μ 与 R 矢量（略伸出球面弧之外）
    ax.annotate('', xy=P(um, 2.1), xytext=O,
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.6,
                                mutation_scale=13))
    ax.annotate('', xy=P(ur, 2.35), xytext=O,
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.6,
                                mutation_scale=13))
    ax.text(-1.72, 1.55, r'$\boldsymbol{\mu}$', fontsize=11, ha='right',
            va='center')
    ax.text(2.42, 1.95, r'$\boldsymbol{R}$', fontsize=11, ha='left', va='center')
    # 角标注
    ax.text(-0.66, 1.20, r'$\theta_0$', fontsize=10.5, ha='center',
            va='center')
    ax.text(-0.22, 1.16, r"$\theta'$", fontsize=10.5, ha='center', va='center')
    ax.text(0.46, 1.22, r'$\theta$', fontsize=10.5, ha='center', va='center')
    save(fig, '10-3')


# ================================================================ 图10.4
def fig_10_4():
    """m_h* >> m_e* 极限的双激子互作用：三重态（排斥）/单重态（吸引）"""
    fig, ax = plt.subplots(figsize=(4.4, 3.1))
    plain_axes(ax)
    ax.set_xlim(-0.3, 5.6)
    ax.set_ylim(-0.56, 0.95)

    arrow_axis(ax, 0.55, -0.52, 0.55, 0.88)
    arrow_axis(ax, 0.35, 0, 5.45, 0, lw=1.0)
    ax.text(0.48, 0.86, r'$W(R)/|E_{\rm B}|$', fontsize=10, ha='right',
            va='center')
    ax.text(5.38, -0.055, r'$R/a_{\rm ex}$', fontsize=10, ha='right',
            va='top')
    for v in (0.6, 0.4, 0.2, -0.2, -0.4):
        tick(ax, 0.55, v, -0.06, 0)
        ax.text(0.47, v, f'{v:.1f}', fontsize=8.5, ha='right', va='center')
    tick(ax, 0.55, 0, -0.06, 0)
    ax.text(0.47, 0, '0', fontsize=8.5, ha='right', va='center')
    for v in (2, 4):
        tick(ax, v, 0, 0, -0.045)
        ax.text(v, -0.06, str(v), fontsize=8.5, ha='center', va='top')
    # 三重态（排斥）
    curvey(ax, [(0.95, 0.90), (1.02, 0.62), (1.15, 0.50), (1.3, 0.43),
                (1.5, 0.36), (1.8, 0.285), (2.2, 0.22), (2.6, 0.17),
                (3.0, 0.135), (3.5, 0.10), (4.0, 0.078), (4.5, 0.062),
                (5.0, 0.05), (5.25, 0.046)], lw=1.5)
    # 单重态（吸引）
    curvey(ax, [(0.95, 0.90), (1.0, 0.62), (1.08, 0.30), (1.18, 0.0),
                (1.3, -0.16), (1.45, -0.215), (1.65, -0.245), (1.9, -0.245),
                (2.2, -0.228), (2.6, -0.196), (3.0, -0.165), (3.5, -0.13),
                (4.0, -0.104), (4.5, -0.085), (5.0, -0.072), (5.25, -0.068)],
           lw=1.5)
    ax.text(2.45, 0.36, u'三重态', fontsize=9.5, ha='left', va='center')
    ax.text(3.35, -0.30, u'单重态', fontsize=9.5, ha='left', va='center')
    save(fig, '10-4')


# ================================================================ 图10.5
def fig_10_5():
    """激子分子结合能与 σ 的关系（框式坐标）"""
    fig, ax = plt.subplots(figsize=(3.3, 3.0))
    for s in ax.spines.values():
        s.set_linewidth(1.1)
    ax.set_xlim(0, 1.065)
    ax.set_ylim(0, 0.335)
    ax.set_xticks([0.5, 1.0])
    ax.set_yticks([0.1, 0.2, 0.3])
    ax.set_xticklabels(['0.5', '1.0'])
    ax.set_yticklabels(['0.1', '0.2', '0.3'])
    ax.tick_params(direction='in', length=3.5, labelsize=8.5)
    ax.text(-0.015, -0.017, '0', fontsize=8.5, ha='right', va='top',
            transform=ax.transAxes)
    ax.set_ylabel(r'$|E_{\rm M}|/|E_{\rm B}|$', fontsize=10)
    ax.set_xlabel(r'$\sigma=m_{\rm e}^{*}/m_{\rm h}^{*}$', fontsize=10)
    curvey(ax, [(0, 0.272), (0.03, 0.21), (0.06, 0.158), (0.10, 0.113),
                (0.15, 0.081), (0.20, 0.061), (0.30, 0.041), (0.40, 0.032),
                (0.50, 0.0295), (0.60, 0.0283), (0.70, 0.0278),
                (0.80, 0.0275), (0.90, 0.0274), (1.0, 0.0273)], lw=1.5)
    ax.text(1.008, 0.0273, '0.0273', fontsize=8, ha='left', va='center',
            transform=ax.transData)
    save(fig, '10-5')


# ================================================================ 图10.6
def fig_10_6():
    """E-H 液体基态能计算曲线：实线 Ge，虚线各向同性模型"""
    fig, ax = plt.subplots(figsize=(3.9, 3.4))
    for s in ax.spines.values():
        s.set_linewidth(1.1)
    ax.set_xlim(0.30, 3.02)
    ax.set_ylim(-2.18, 0.32)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['1', '2', '3'])
    ax.set_yticks([-0.5, -1.0, -1.5, -2.0])
    ax.tick_params(direction='in', length=3.5, labelsize=8.5)
    # r_s' 刻度（Ge 极小点位置）
    ax.plot([0.82, 0.82], [-2.18, -2.13], 'k-', lw=1.0, clip_on=False)
    ax.text(0.82, -2.26, r"$r_{\rm s}^{\prime}$", fontsize=9, ha='center',
            va='top', clip_on=False)
    ax.set_ylabel(r'$E_{\rm G}(r_{\rm s})$', fontsize=10)
    # Ge（实线）
    curvey(ax, [(0.52, 0.30), (0.58, -0.52), (0.63, -1.10), (0.68, -1.60),
                (0.72, -1.88), (0.78, -1.99), (0.85, -1.98), (0.95, -1.87),
                (1.1, -1.71), (1.3, -1.54), (1.5, -1.41), (1.8, -1.26),
                (2.1, -1.15), (2.4, -1.06), (2.7, -0.99), (3.0, -0.94)],
           lw=1.6)
    ax.text(2.5, -1.20, 'Ge', fontsize=9.5, ha='center', va='center')
    # 各向同性模型（虚线）
    curvey(ax, [(0.88, 0.30), (0.95, -0.15), (1.05, -0.42), (1.2, -0.62),
                (1.4, -0.76), (1.6, -0.83), (1.8, -0.855), (1.95, -0.862),
                (2.1, -0.85), (2.3, -0.81), (2.5, -0.76), (2.7, -0.70),
                (3.0, -0.63)], ls='--', lw=1.3, dashes=(5, 2.5))
    ax.text(2.35, -0.56, u'各向同性模型', fontsize=9, ha='center',
            va='center')
    save(fig, '10-6')


# ================================================================ 图12.1
def fig_12_1():
    """无序分类：(a)有序晶格 (b)成分无序 (c)拓扑无序（题注由 tex 排）"""
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-0.35, 13.95)
    ax.set_ylim(-7.3, 0.6)
    r = 0.098

    def grid(x0, y0, fillset, stub=0.24):
        sp = 0.78
        xs = [x0 + sp * i for i in range(5)]
        ys = [y0 - sp * j for j in range(4)]
        for x in xs:
            ax.plot([x, x], [ys[0] + stub, ys[-1] - stub], 'k-', lw=1.1)
        for y in ys:
            ax.plot([xs[0] - stub, xs[-1] + stub], [y, y], 'k-', lw=1.1)
        for j in range(4):
            for i in range(5):
                fc = 'k' if (j, i) in fillset else 'white'
                ax.add_patch(Circle((xs[i], ys[j]), r, fc=fc, ec='k', lw=1.0,
                                    zorder=3))

    # (a) 有序晶格
    grid(0.4, -0.35, set())
    # (b) 成分无序系统
    fillb = {(0, 2), (0, 3), (1, 0), (1, 2), (1, 4), (2, 0), (2, 4),
             (3, 0), (3, 3), (3, 4)}
    grid(6.6, -0.35, fillb)
    # (c) 拓扑无序系统（不规则四边形网格：中带断开成两片 + 左上三角元胞 + 短线头）
    x0, y0 = 4.45, -3.02
    rows = [
        [0.00, 0.86, 1.80, 2.68, 3.58],
        [-0.14, 0.78, 1.90, 2.78, 3.66],
        [0.08, 0.96, 2.02, 2.90, 3.78],
        [-0.04, 0.84, 1.94, 2.82, 3.70],
        [0.04, 0.94, 1.86, 2.76],
    ]
    P = [[(x0 + x, y0 - 0.76 * j) for x in row] for j, row in enumerate(rows)]

    def bond(p, q):
        ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=1.1)

    # 横向键：第 1—3 行在 col1—col2 间断开（两片仅在顶行与底行相连）
    gaps = {1, 2, 3}
    for j in range(5):
        for i in range(len(rows[j]) - 1):
            if j in gaps and i == 1:
                continue
            bond(P[j][i], P[j][i + 1])
    # 纵向键
    for j in range(4):
        n = min(len(rows[j]), len(rows[j + 1]))
        for i in range(n):
            bond(P[j][i], P[j + 1][i])
    # 左上三角元胞：对角键
    bond(P[0][1], P[1][2])
    # 断口处的短线头（指向断口）
    for p, d in [(P[1][1], (0.26, 0.05)), (P[1][2], (-0.26, 0.05)),
                 (P[2][1], (0.26, 0.0)), (P[2][2], (-0.26, 0.0)),
                 (P[3][1], (0.26, -0.05)), (P[3][2], (-0.26, -0.05))]:
        ax.plot([p[0], p[0] + d[0]], [p[1], p[1] + d[1]], 'k-', lw=1.1)
    # 边界短线头（朝外）
    stubs = [(P[0][0], (-0.30, 0.12)), (P[0][4], (0.24, -0.18)),
             (P[1][0], (-0.30, 0)), (P[1][4], (0.30, 0)),
             (P[2][0], (-0.28, -0.14)), (P[2][4], (0.30, 0.05)),
             (P[3][0], (-0.30, 0)), (P[3][4], (0.30, 0)),
             (P[4][0], (-0.28, -0.12)), (P[4][3], (0.22, -0.22)),
             (P[0][2], (0.06, 0.3)), (P[0][3], (0.05, 0.3)),
             (P[4][1], (0.0, -0.3)), (P[4][2], (0.05, -0.28))]
    for p, d in stubs:
        ax.plot([p[0], p[0] + d[0]], [p[1], p[1] + d[1]], 'k-', lw=1.1)
    for j in range(5):
        for i in range(len(rows[j])):
            ax.add_patch(Circle(P[j][i], r, fc='white', ec='k', lw=1.0,
                                zorder=3))
    save(fig, '12-1')


# ================================================================ 图12.2
def fig_12_2():
    """CPA 单格点近似自洽方程图示：两块 3×3 格点，中心为 V_A / V_B"""
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-0.55, 11.65)
    ax.set_ylim(-1.35, 3.75)

    def patch(x0, vlab, tlab):
        sp = 1.18
        xs = [x0 + sp * i for i in range(3)]
        ys = [0.45 + sp * j for j in range(3)]
        for x in xs:
            ax.plot([x, x], [ys[0] - 0.3, ys[-1] + 0.3], 'k-', lw=1.3)
        for y in ys:
            ax.plot([xs[0] - 0.3, xs[-1] + 0.3], [y, y], 'k-', lw=1.3)
        for j in range(3):
            for i in range(3):
                if (i, j) == (1, 1):
                    ax.add_patch(Circle((xs[i], ys[j]), 0.155, fc='white',
                                        ec='k', lw=1.3, zorder=5))
                    ax.text(xs[i] + 0.26, ys[j] - 0.24, vlab, fontsize=11,
                            ha='left', va='center', zorder=5)
                else:
                    ax.add_patch(Circle((xs[i], ys[j]), 0.12, fc='k',
                                        ec='k', zorder=5))
        ax.text(xs[1], ys[0] - 0.62, tlab, fontsize=11, ha='center', va='top')

    patch(0.7, r'$V_{\rm A}$', r'$x\,t_{\rm A}$')
    ax.text(5.62, -0.18, '+', fontsize=12, ha='center', va='center')
    patch(6.75, r'$V_{\rm B}$', r'$(1-x)\,t_{\rm B}=0$')
    save(fig, '12-2')


# ================================================================ 图12.3
def fig_12_3():
    """安德逊模型 P(ε) 矩形分布"""
    fig, ax = plt.subplots(figsize=(3.4, 1.75))
    plain_axes(ax)
    ax.set_xlim(-1.95, 2.25)
    ax.set_ylim(-0.42, 1.3)

    arrow_axis(ax, 0, -0.05, 0, 1.18)
    arrow_axis(ax, -1.78, 0, 2.1, 0, lw=1.0)
    ax.text(0.07, 1.10, r'$P(\varepsilon)$', fontsize=10, ha='left',
            va='center')
    ax.text(2.03, -0.035, r'$\varepsilon$', fontsize=10.5, ha='center',
            va='top')
    H = 0.72
    ax.plot([-1, -1], [0, H], 'k-', lw=1.6)
    ax.plot([-1, 1], [H, H], 'k-', lw=1.6)
    ax.plot([1, 1], [H, 0], 'k-', lw=1.6)
    tick(ax, -1, 0, 0, -0.05)
    tick(ax, 1, 0, 0, -0.05)
    ax.text(-1, -0.085, r'$-\dfrac{W}{2}$', fontsize=10, ha='center', va='top')
    ax.text(1, -0.085, r'$\dfrac{W}{2}$', fontsize=10, ha='center', va='top')
    ax.text(0.22, 0.80, r'$\dfrac{1}{W}$', fontsize=10, ha='left', va='center')
    save(fig, '12-3')


# ================================================================ 图12.4
def fig_12_4():
    """莫特模型：δ<δc 时态密度，带尾定域态（斜线影区）+ 带心扩展态"""
    fig, ax = plt.subplots(figsize=(4.4, 2.6))
    plain_axes(ax)
    ax.set_xlim(-3.75, 3.95)
    ax.set_ylim(-0.16, 1.06)

    arrow_axis(ax, 0, -0.02, 0, 1.0)
    arrow_axis(ax, -3.35, 0, 3.8, 0, lw=1.0)
    ax.text(0.10, 0.965, r'$\rho(E)$', fontsize=10, ha='left', va='center')
    ax.text(3.72, -0.035, r'$E$', fontsize=10.5, ha='center', va='top')

    def bell(x):
        return 0.88 * np.exp(-x ** 2 / (2 * 1.05 ** 2))

    xx = np.linspace(-3.3, 3.3, 500)
    ax.plot(xx, bell(xx), 'k-', lw=1.6)
    Ec = 1.6
    for x0, x1 in [(-3.3, -Ec), (Ec, 3.3)]:
        xa = np.linspace(x0, x1, 120)
        poly = np.column_stack([xa, bell(xa)])
        poly = np.vstack([poly, [x1, 0], [x0, 0]])
        ax.add_patch(Polygon(poly, closed=True, fc='white', ec='k', lw=0.9,
                             hatch='/////'))
    tick(ax, -Ec, 0, 0, -0.035)
    tick(ax, Ec, 0, 0, -0.035)
    ax.text(-Ec, -0.055, r'$-E_{\rm c}$', fontsize=9.5, ha='center', va='top')
    ax.text(Ec, -0.055, r'$E_{\rm c}$', fontsize=9.5, ha='center', va='top')
    ax.text(0, -0.055, r'$O$', fontsize=9.5, ha='center', va='top')
    ax.text(-2.62, 0.42, u'局域态', fontsize=9.5, ha='center', va='center')
    ax.plot([-2.35, -2.0], [0.34, 0.14], 'k-', lw=0.8)
    ax.text(2.52, 0.42, u'局域态', fontsize=9.5, ha='center', va='center')
    ax.plot([2.26, 2.0], [0.34, 0.14], 'k-', lw=0.8)
    ax.text(-0.52, 0.44, u'扩展态', fontsize=9.5, ha='center', va='center')
    save(fig, '12-4')


# ================================================================ 图12.5
def fig_12_5():
    """定域态间的跳跃传导示意：随机短能级线，占据态以圆点标记，A→B 跳迁"""
    fig, ax = plt.subplots(figsize=(4.6, 2.6))
    plain_axes(ax)
    ax.set_xlim(-0.95, 6.95)
    ax.set_ylim(-0.85, 3.45)

    # 边框
    ax.plot([0, 6.2, 6.2, 0, 0], [0, 0, 2.9, 2.9, 0], 'k-', lw=1.4)
    ax.text(-0.42, 1.45, u'能量 E', fontsize=9.5, rotation=90,
            ha='center', va='center')
    ax.text(3.1, -0.45, u'距离 R', fontsize=9.5, ha='center', va='center')

    def dash(x0, x1, y):
        ax.plot([x0, x1], [y, y], 'k-', lw=1.5)

    def state(xc, y, half=0.22):
        dash(xc - half, xc + half, y)
        ax.plot([xc], [y], 'ko', ms=4.2)

    # 未占据定域态（短横线，上半部为主）
    for x0, x1, y in [(0.40, 0.89, 2.61), (1.94, 2.43, 2.51), (3.23, 3.70, 2.36),
                      (5.41, 5.96, 2.72), (1.49, 1.88, 1.87), (3.87, 4.42, 1.97),
                      (4.91, 5.33, 2.16), (4.30, 4.80, 1.30), (5.45, 5.95, 1.60),
                      (2.93, 3.72, 1.48)]:
        dash(x0, x1, y)
    # 占据定域态（线 + 圆点，下半部为主）
    for xc, y in [(0.45, 1.28), (1.19, 1.08), (2.05, 0.79), (3.10, 0.94),
                  (3.79, 0.59), (4.46, 0.37), (4.86, 0.86), (5.26, 0.27),
                  (5.90, 0.62)]:
        state(xc, y)
    # A：已占据态（电子自 A 吸收声子激发后跳向 B）
    axc, yc_ = 2.18, 1.47
    dash(axc - 0.33, axc + 0.33, yc_)
    ax.plot([axc], [yc_], 'ko', ms=4.6)
    ax.text(axc - 0.13, yc_ + 0.17, '$A$', fontsize=11, ha='right', va='center')
    # 声子激发箭头（指向右上方能级）
    leader(ax, (axc + 0.10, yc_ + 0.08), (axc + 0.48, 2.02), lw=1.4, ms=12)
    # A → B 跳迁折线箭头
    ax.annotate('', xy=(3.52, 1.63), xytext=(axc + 0.06, yc_),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.4,
                                shrinkA=0, shrinkB=0, mutation_scale=13,
                                connectionstyle='angle3,angleA=0,angleB=-70'))
    ax.text(3.16, 1.24, '$B$', fontsize=11, ha='center', va='center')
    save(fig, '12-5')


# ================================================================ 图12.6
def fig_12_6():
    """(a) 无序样品透射/反射电流 (b) 一维模拟势垒（题注由 tex 排）"""
    fig, ax = plt.subplots(figsize=(6.6, 1.9))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-0.75, 12.0)
    ax.set_ylim(-1.05, 2.85)

    # (a)
    ax.add_patch(Rectangle((0.45, 0.3), 2.65, 1.4, fc='white', ec='k',
                           lw=1.6, hatch='/////'))
    ax.annotate('', xy=(0.45, 1.35), xytext=(-0.05, 1.35),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.3,
                                shrinkA=0, shrinkB=0, mutation_scale=12))
    ax.text(-0.12, 1.35, r'$I_0$', fontsize=11, ha='right', va='center')
    ax.annotate('', xy=(-0.05, 0.62), xytext=(0.45, 0.62),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.3,
                                shrinkA=0, shrinkB=0, mutation_scale=12))
    ax.text(-0.12, 0.62, r'$I_{\rm r}$', fontsize=11, ha='right', va='center')
    ax.annotate('', xy=(3.65, 1.0), xytext=(3.1, 1.0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.3,
                                shrinkA=0, shrinkB=0, mutation_scale=12))
    ax.text(3.72, 1.0, r'$I_{\rm t}$', fontsize=11, ha='left', va='center')
    # ΔV 尺寸线
    for xv in (0.45, 3.1):
        ax.plot([xv, xv], [-0.12, -0.5], 'k-', lw=0.9)
    dbarr(ax, 0.45, 3.1, -0.31, ms=10)
    ax.text(1.775, -0.31, r'$\Delta V$', fontsize=11, ha='center',
            va='center', bbox=dict(fc='white', ec='none', pad=1))
    # (b)
    bx = 6.55
    ax.plot([bx, bx + 1.7], [0.3, 0.3], 'k-', lw=1.8)
    ax.plot([bx + 3.2, bx + 4.9], [0.3, 0.3], 'k-', lw=1.8)
    ax.plot([bx + 1.7, bx + 1.7, bx + 3.2, bx + 3.2],
            [0.3, 2.3, 2.3, 0.3], 'k-', lw=1.8)
    ax.annotate('', xy=(bx + 1.7, 1.7), xytext=(bx + 0.85, 1.7),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.3,
                                shrinkA=0, shrinkB=0, mutation_scale=12))
    ax.text(bx + 0.76, 1.7, r'$I$', fontsize=11, ha='right', va='center')
    ax.annotate('', xy=(bx + 0.85, 0.72), xytext=(bx + 1.7, 0.72),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.3,
                                shrinkA=0, shrinkB=0, mutation_scale=12))
    ax.text(bx + 0.76, 0.72, r'$R$', fontsize=11, ha='right', va='center')
    ax.annotate('', xy=(bx + 4.05, 1.7), xytext=(bx + 3.2, 1.7),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.3,
                                shrinkA=0, shrinkB=0, mutation_scale=12))
    ax.text(bx + 4.12, 1.7, r'$T$', fontsize=11, ha='left', va='center')
    save(fig, '12-6')


# ================================================================ 图12.7
def fig_12_7():
    """一维双势垒：入射 1、反射 A，垒间 B e^{iφ} / C e^{-iφ}，透射 D"""
    fig, ax = plt.subplots(figsize=(5.8, 1.75))
    plain_axes(ax)
    ax.set_xlim(-0.55, 6.35)
    ax.set_ylim(-0.16, 1.62)

    ax.plot([-0.35, 6.15], [0, 0], 'k-', lw=1.4)
    # 势垒 1、2
    ax.add_patch(Rectangle((0.95, 0), 0.8, 0.62, fc='white', ec='k', lw=1.6))
    ax.text(1.35, 0.31, '1', fontsize=11, ha='center', va='center')
    ax.add_patch(Rectangle((3.15, 0), 0.9, 1.35, fc='white', ec='k', lw=1.6))
    ax.text(3.6, 0.68, '2', fontsize=11, ha='center', va='center')

    def harrow(x0, x1, y):
        ax.annotate('', xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle='-|>', color='k', lw=1.3,
                                    shrinkA=0, shrinkB=0, mutation_scale=12))

    harrow(-0.35, 0.95, 0.72)                       # 入射 1
    harrow(0.95, -0.35, 0.40)                       # 反射 A
    harrow(1.75, 3.15, 0.72)                        # B
    harrow(3.15, 1.75, 0.40)                        # C
    harrow(4.05, 5.5, 0.72)                         # D
    ax.text(0.25, 0.81, '1', fontsize=11, ha='center', va='center')
    ax.text(0.55, 0.50, '$A$', fontsize=11, ha='center', va='center')
    ax.text(1.95, 0.81, '$B$', fontsize=11, ha='left', va='center')
    ax.text(3.02, 0.83, r'$B\mathrm{e}^{\mathrm{i}\phi}$', fontsize=10.5,
            ha='right', va='center')
    ax.text(1.95, 0.50, '$C$', fontsize=11, ha='left', va='center')
    ax.text(3.02, 0.50, r'$C\mathrm{e}^{-\mathrm{i}\phi}$', fontsize=10.5,
            ha='right', va='center')
    ax.text(4.45, 0.81, '$D$', fontsize=11, ha='left', va='center')
    save(fig, '12-7')


# ================================================================ 图12.8
def fig_12_8():
    """d=1,2,3 维体系的 β–ln g 标度曲线（含流向箭头、sln(g/gc) 虚线、C/g）"""
    fig, ax = plt.subplots(figsize=(5.4, 3.7))
    plain_axes(ax)
    ax.set_xlim(-2.75, 3.85)
    ax.set_ylim(-3.1, 1.62)

    arrow_axis(ax, 0, -3.0, 0, 1.52)
    arrow_axis(ax, -2.6, 0, 3.75, 0, lw=1.0)
    ax.text(0.12, 1.44, r'$\beta(g)$', fontsize=10.5, ha='left', va='center')
    ax.text(3.68, -0.14, r'$\ln g$', fontsize=10.5, ha='right', va='top')
    for v, lab in [(1, '1'), (-1, '$-1$')]:
        tick(ax, 0, v, -0.055, 0)
        ax.text(-0.09, v, lab, fontsize=9, ha='right', va='center')
    tick(ax, -0.07, 0, 0, -0.05)
    ax.text(-0.02, -0.14, r'$g_{\rm c}$', fontsize=9.5, ha='left', va='top')

    d3 = [(-2.2, -1.52), (-1.9, -1.28), (-1.6, -1.06), (-1.3, -0.85),
          (-1.0, -0.65), (-0.7, -0.46), (-0.4, -0.28), (-0.2, -0.15),
          (0.0, 0.03), (0.3, 0.25), (0.6, 0.48), (0.9, 0.68), (1.2, 0.83),
          (1.5, 0.93), (1.9, 0.98), (2.4, 1.0), (3.3, 1.0)]
    d2 = [(-2.2, -1.78), (-1.9, -1.55), (-1.6, -1.32), (-1.3, -1.10),
          (-1.0, -0.89), (-0.7, -0.70), (-0.4, -0.52), (-0.1, -0.37),
          (0.2, -0.26), (0.5, -0.18), (0.8, -0.12), (1.1, -0.08),
          (1.5, -0.05), (2.0, -0.03), (2.6, -0.02), (3.3, -0.015)]
    d1 = [(-2.2, -2.62), (-1.9, -2.35), (-1.6, -2.08), (-1.3, -1.83),
          (-1.0, -1.60), (-0.7, -1.40), (-0.4, -1.24), (-0.1, -1.13),
          (0.2, -1.06), (0.5, -1.02), (0.8, -1.00), (1.2, -0.99),
          (1.8, -0.985), (3.3, -0.98)]
    f3 = curvey(ax, d3, lw=1.6)
    f2 = curvey(ax, d2, lw=1.6)
    f1 = curvey(ax, d1, lw=1.6)

    # 曲线上的流向箭头（右侧向右，左侧向左下）
    def flow(f, x, dsign):
        y = float(f(x))
        dy = float(f(x + 0.02)) - y
        d = np.array([dsign * 0.055, dsign * dy * 2.2])
        n = d / np.hypot(*d)
        p0 = np.array([x, y]) - n * 0.05
        p1 = np.array([x, y]) + n * 0.05
        ax.annotate('', xy=p1, xytext=p0,
                    arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2,
                                    shrinkA=0, shrinkB=0, mutation_scale=12))

    for f in (f3, f2, f1):
        flow(f, 2.4, +1)
        flow(f, -1.15, -1)
    # 渐近虚线
    ax.plot([0.10, 0.74], [0.17, 1.02], 'k--', lw=1.0, dashes=(5, 2.5))
    ax.text(0.78, 1.10, r'$s\ln(g/g_{\rm c})$', fontsize=10, ha='left',
            va='center')
    ax.plot([-2.08, -1.05], [-1.42, -0.73], 'k--', lw=1.0, dashes=(5, 2.5))
    # C/g 标注（d=2 曲线与横轴的间距）
    dbarr(ax, 0.55, 0.55, float(f2(0.55)), ms=8)
    ax.annotate('', xy=(0.40, -0.055), xytext=(0.14, -0.055),
                arrowprops=dict(arrowstyle='->', color='k', lw=0.9))
    ax.text(0.10, -0.055, r'$C/g$', fontsize=10, ha='right', va='center')
    # 维度标签
    ax.text(2.25, 0.86, '$d$=3', fontsize=10, ha='center', va='center')
    ax.text(2.5, -0.12, '$d$=2', fontsize=10, ha='center', va='center')
    ax.text(2.4, -1.13, '$d$=1', fontsize=10, ha='center', va='center')
    save(fig, '12-8')


# ================================================================ 图12.9
def fig_12_9():
    """二维系统 β–ln g 曲线的非单调行为（新标度理论）"""
    fig, ax = plt.subplots(figsize=(4.3, 2.5))
    plain_axes(ax)
    ax.set_xlim(-2.3, 3.05)
    ax.set_ylim(-1.25, 0.72)

    arrow_axis(ax, 0, -1.15, 0, 0.64)
    arrow_axis(ax, -2.2, 0, 2.95, 0, lw=1.0)
    ax.text(0.12, 0.58, r'$\beta$', fontsize=11, ha='left', va='center')
    ax.text(2.88, -0.13, r'$\ln g$', fontsize=10.5, ha='right', va='top')
    f = curvey(ax, [(-1.05, -0.80), (-0.8, -0.53), (-0.55, -0.29),
                    (-0.3, -0.10), (-0.1, 0.04), (0.08, 0.13), (0.25, 0.22),
                    (0.45, 0.30), (0.65, 0.335), (0.8, 0.34), (1.0, 0.32),
                    (1.2, 0.28), (1.4, 0.235), (1.6, 0.19), (1.8, 0.155),
                    (2.0, 0.12), (2.25, 0.09)], lw=1.6)
    tick(ax, 0.08, 0, 0, -0.05)
    ax.text(0.15, -0.10, r'$g_{\rm c}$', fontsize=9.5, ha='left', va='top')

    def flow(f, x, dsign):
        y = float(f(x))
        dy = float(f(x + 0.02)) - y
        d = np.array([dsign * 0.05, dsign * dy * 2.0])
        n = d / np.hypot(*d)
        p0 = np.array([x, y]) - n * 0.05
        p1 = np.array([x, y]) + n * 0.05
        ax.annotate('', xy=p1, xytext=p0,
                    arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2,
                                    shrinkA=0, shrinkB=0, mutation_scale=12))

    flow(f, 0.45, +1)
    flow(f, 1.5, -1)
    save(fig, '12-9')


# ================================================================ 图D.1
def fig_D_1():
    """电子的谱函数：峰宽 2Γ_k 的共振峰（洛伦兹型）"""
    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    plain_axes(ax)
    ax.set_xlim(-2.5, 2.75)
    ax.set_ylim(-0.14, 1.2)

    axx = -1.62
    arrow_axis(ax, axx, -0.02, axx, 1.1)
    arrow_axis(ax, axx, 0, 2.6, 0, lw=1.0)
    ax.text(axx - 0.07, 1.06, r'$A(k,\omega)$', fontsize=10, ha='right',
            va='center')
    x0, G, H = 0.25, 0.42, 0.95
    xx = np.linspace(axx + 0.02, 2.35, 600)
    ax.plot(xx, H / (1 + ((xx - x0) / G) ** 2), 'k-', lw=1.6)
    # 半高与峰高虚线
    ax.plot([axx, 1.10], [H, H], 'k--', lw=0.9, dashes=(4, 2.2))
    ax.plot([axx, 1.55], [H / 2, H / 2], 'k--', lw=0.9, dashes=(4, 2.2))
    ax.text(axx - 0.07, H, r'$\dfrac{1}{\pi\Gamma_k}$', fontsize=10,
            ha='right', va='center')
    ax.text(axx - 0.07, H / 2, r'$\dfrac{1}{2\pi\Gamma_k}$', fontsize=10,
            ha='right', va='center')
    # 峰心与半高点的竖直虚线
    for xv, ytop in [(x0, H), (x0 - G, H / 2), (x0 + G, H / 2)]:
        ax.plot([xv, xv], [0, ytop], 'k--', lw=0.9, dashes=(4, 2.2))
    ax.text(x0, -0.06, r'$\widetilde{E}_{k}$', fontsize=10, ha='center',
            va='top')
    # 2Γ_k 双向箭头与引线
    dbarr(ax, x0 - G, x0 + G, H / 2, ms=9)
    ax.annotate('', xy=(x0 + G + 0.03, H / 2 + 0.01), xytext=(1.35, 0.66),
                arrowprops=dict(arrowstyle='->', color='k', lw=0.9))
    ax.text(1.38, 0.68, r'$2\Gamma_k$', fontsize=10, ha='left', va='center')
    save(fig, 'D-1')


# ================================================================ 图E.1
def fig_E_1():
    """泊松求和公式的回路：Γ 大圆弧、C 虚轴旁路（× 为 f(z) 极点）、
    C‘ 实轴旁路（· 为 (z-x)^{-1} 极点）。图例与图注由 tex 排印。"""
    fig, ax = plt.subplots(figsize=(4.5, 3.7))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-1.85, 2.25)
    ax.set_ylim(-1.7, 1.95)
    R = 1.0

    def arc(a0, a1, r=R, lw=1.8, **kw):
        th = np.linspace(np.deg2rad(a0), np.deg2rad(a1), 120)
        ax.plot(r * np.cos(th), r * np.sin(th), color='k', lw=lw, **kw)

    # 虚 / 实轴（细线）
    ax.annotate('', xy=(0, 1.62), xytext=(0, -1.35),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=0.9,
                                mutation_scale=11))
    ax.annotate('', xy=(1.85, 0), xytext=(-1.32, 0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=0.9,
                                mutation_scale=11))
    ax.text(0.0, 1.66, r'Im $z$', fontsize=10.5, ha='center', va='bottom')
    ax.text(1.9, 0.0, r'Re $z$', fontsize=10.5, ha='left', va='center')

    # Γ 四段大弧（箭头照原书：上两段指向上方、下左指向下方、下右指向右）
    arc(97.5, 172)
    arc(188, 262.5)
    arc(7.5, 82.5)
    arc(277.5, 352)
    for adeg, tgt in [(140, (0.72, -0.70)), (225, (0.70, 0.70)),
                      (45, (-0.70, -0.70)), (315, (0.70, -0.70))]:
        a = np.deg2rad(adeg)
        p = np.array([R * np.cos(a), R * np.sin(a)])
        t = np.array(tgt)
        ax.annotate('', xy=p + 0.09 * t, xytext=p - 0.09 * t,
                    arrowprops=dict(arrowstyle='-|>', color='k', lw=1.6,
                                    shrinkA=0, shrinkB=0, mutation_scale=12))
    # C：虚轴两侧竖线（左向下、右向上）
    d = 0.13
    for sgn, dirs in [(-1, (0.55, -0.52)), (1, (0.55, -0.52))]:
        ax.plot([sgn * d, sgn * d], [-0.99, 0.99], 'k-', lw=1.8)
    for sgn in (-1, 1):
        for yv, dsign in [(0.55, -1 if sgn < 0 else 1),
                          (-0.5, -1 if sgn < 0 else 1)]:
            ax.annotate('', xy=(sgn * d, yv + 0.09 * dsign),
                        xytext=(sgn * d, yv - 0.09 * dsign),
                        arrowprops=dict(arrowstyle='-|>', color='k', lw=1.6,
                                        shrinkA=0, shrinkB=0,
                                        mutation_scale=12))
    # C'：实轴上下旁路（发卡状，左发卡在左 C 线外折回、右发卡在右 C 线外折回）
    h = 0.045
    ax.plot([-0.95, -0.185], [h, h], 'k-', lw=1.8)
    ax.plot([-0.95, -0.185], [-h, -h], 'k-', lw=1.8)
    th = np.linspace(np.pi / 2, -np.pi / 2, 60)
    ax.plot(-0.185 + h * np.cos(th), h * np.sin(th), 'k-', lw=1.8)
    ax.plot([0.185, 0.95], [h, h], 'k-', lw=1.8)
    ax.plot([0.185, 0.95], [-h, -h], 'k-', lw=1.8)
    th = np.linspace(np.pi / 2, 3 * np.pi / 2, 60)
    ax.plot(0.185 + h * np.cos(th), h * np.sin(th), 'k-', lw=1.8)
    for x0_, dsign in [(-0.55, 1), (-0.55, -1), (0.55, -1), (0.55, -1)]:
        y0_ = h if dsign == 1 else -h
        ax.annotate('', xy=(x0_ + 0.1 * dsign, y0_), xytext=(x0_, y0_),
                    arrowprops=dict(arrowstyle='-|>', color='k', lw=1.5,
                                    shrinkA=0, shrinkB=0, mutation_scale=11))
    # f(z) 的极点 ×（虚轴上，位于两 C 线之间）
    for yv in (0.18, 0.34, 0.50, 0.66, 0.82, -0.18, -0.34, -0.50, -0.66, -0.82):
        s = 0.038
        ax.plot([-s, s], [yv - s, yv + s], 'k-', lw=1.4)
        ax.plot([-s, s], [yv + s, yv - s], 'k-', lw=1.4)
    # (z-x)^{-1} 的极点 ·（实轴上 x 处）
    ax.plot([0.36], [0], 'ko', ms=4.2)
    ax.text(0.36, -0.13, '$x$', fontsize=11, ha='center', va='center')
    # 回路标注
    for adeg, lab in [(140, r'$\Gamma$'), (220, r'$\Gamma$'),
                      (42, r'$\Gamma$'), (318, r'$\Gamma$')]:
        a = np.deg2rad(adeg)
        ax.text(1.24 * R * np.cos(a), 1.24 * R * np.sin(a), lab, fontsize=12,
                ha='center', va='center')
    for x0_, y0_, ha in [(-0.26, 0.52, 'right'), (-0.26, -0.48, 'right'),
                         (0.26, 0.52, 'left'), (0.26, -0.48, 'left')]:
        ax.text(x0_, y0_, '$C$', fontsize=12, ha=ha, va='center')
    for x0_, y0_ in [(-0.62, 0.115), (-0.62, -0.115), (0.62, 0.115),
                     (0.62, -0.115)]:
        ax.text(x0_, y0_, "$C'$", fontsize=12, ha='center',
                va='bottom' if y0_ > 0 else 'top')
    save(fig, 'E-1')


# ================================================================ 习题图1
def fig_x_1():
    """题7：二维密排六角晶格简约区 BZ（Γ、K、M、Σ、T 及直角标记）"""
    fig, ax = plt.subplots(figsize=(3.9, 3.8))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-1.72, 2.05)
    ax.set_ylim(-1.9, 1.85)
    R = 1.0
    verts = [(R * np.cos(np.deg2rad(a)), R * np.sin(np.deg2rad(a)))
             for a in range(0, 360, 60)]
    ax.add_patch(Polygon(verts, closed=True, fill=False, ec='k', lw=2.2))
    # 坐标轴
    arrow_axis(ax, -1.42, 0, 1.78, 0, lw=1.1)
    arrow_axis(ax, 0, -1.62, 0, 1.68, lw=1.1)
    ax.text(1.7, -0.16, r'$k_x$', fontsize=11, ha='center', va='top')
    ax.text(-0.12, 1.56, r'$k_y$', fontsize=11, ha='right', va='center')
    # Γ
    ax.plot([0], [0], 'ko', ms=4.6)
    ax.text(-0.10, -0.16, r'$\Gamma$', fontsize=12, ha='right', va='center')
    # K（右顶点）
    tick(ax, 1.06, 0, 0, 0.05)
    tick(ax, 1.06, 0, 0, -0.05)
    ax.text(1.10, -0.17, '$K$', fontsize=12, ha='left', va='center')
    # M（右上边中点）与 Σ 线、直角标记
    M = np.array([0.75, np.sqrt(3) / 4])
    ax.plot([0, M[0]], [0, M[1]], 'k-', lw=1.4)
    ax.plot([M[0]], [M[1]], 'ko', ms=4.2)
    ax.text(M[0] + 0.12, M[1] + 0.10, '$M$', fontsize=12, ha='left',
            va='center')
    ax.plot([M[0] / 2], [M[1] / 2], 'ko', ms=4.2)
    ax.text(M[0] / 2 - 0.06, M[1] / 2 + 0.10, r'$\Sigma$', fontsize=12,
            ha='center', va='center')
    s = 0.10
    u = np.array([np.cos(np.pi / 6), np.sin(np.pi / 6)])
    n = np.array([np.sin(np.pi / 6), -np.cos(np.pi / 6)])
    sq = [M, M - s * u, M - s * u + s * n, M + s * n]
    ax.add_patch(Polygon(sq, closed=True, fill=False, ec='k', lw=1.0))
    # T（Γ–K 中点）
    ax.plot([0.5], [0], 'ko', ms=4.6)
    ax.text(0.5, -0.17, '$T$', fontsize=12, ha='center', va='center')
    save(fig, 'x-1')


if __name__ == '__main__':
    import sys
    names = ['8-1', '8-2', '8-3', '8-4', '8-5', '8-6', '8-7', '8-8', '8-9',
             '8-10', '9-1', '10-1', '10-2', '10-3', '10-4', '10-5', '10-6',
             '12-1', '12-2', '12-3', '12-4', '12-5', '12-6', '12-7', '12-8',
             '12-9', 'D-1', 'E-1', 'x-1']
    only = sys.argv[1:] or names
    for n in only:
        globals()['fig_' + n.replace('-', '_')]()
        print(f'fig{n} done')
