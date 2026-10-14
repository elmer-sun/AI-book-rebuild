# -*- coding: utf-8 -*-
"""
李正中《固体理论》(第2版) 中文重排本 插图重绘 第四批：
第十一章 图11.1-11.25（25幅）。
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p-416/420/421/422/428/430/431/437/439/441/
442/443/447/461/464/477/478/479/487/490/494/495/500/502）。
注：图11.3 实际位于 p-421（印刷401，清单写 p420 偏一页）；
    图11.12/11.13 同在 p-443，为并排两幅不同插图（manifest 同 hash 系误标）。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Rectangle, Circle, Ellipse, Polygon, PathPatch
from matplotlib.path import Path

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


def vtext(ax, x, y, s, **kw):
    ax.text(x, y, '\n'.join(s), ha='center', va='center',
            linespacing=1.02, **kw)


# ================================================================ 图11.1
def fig_11_1():
    """Δ=0 半满赫伯德模型的能态：(a)基态 (b)第一激发态（能级线+×占据符）"""
    fig, ax = plt.subplots(figsize=(3.55, 1.72))
    plain_axes(ax)
    ax.set_xlim(-0.25, 6.05)
    ax.set_ylim(0.72, 3.85)
    xs = np.arange(0.35, 6.0, 1.06)          # 6 个格点位置
    LW = 1.6                                  # 能级线宽
    HL = 0.30                                 # 能级线半长

    def level(y, occ):
        for x in xs:
            ax.plot([x - HL, x + HL], [y, y], 'k-', lw=LW)
            if occ:
                s = 0.105
                ax.plot([x - s, x + s], [y - s, y + s], 'k-', lw=1.1)
                ax.plot([x - s, x + s], [y + s, y - s], 'k-', lw=1.1)

    level(3.45, False)                        # (a) 上排 T0+U
    level(2.92, True)                         # (a) 下排 T0
    level(1.72, False)                        # (b) 上排：仅格点4占据
    for x in xs:
        ax.plot([x - HL, x + HL], [1.72, 1.72], 'k-', lw=LW)
    x4 = xs[3]
    s = 0.105
    ax.plot([x4 - s, x4 + s], [1.72 - s, 1.72 + s], 'k-', lw=1.1)
    ax.plot([x4 - s, x4 + s], [1.72 + s, 1.72 - s], 'k-', lw=1.1)
    for i, x in enumerate(xs):                # (b) 下排：格点2空
        y = 1.19
        ax.plot([x - HL, x + HL], [y, y], 'k-', lw=LW)
        if i != 1:
            ax.plot([x - s, x + s], [y - s, y + s], 'k-', lw=1.1)
            ax.plot([x - s, x + s], [y + s, y - s], 'k-', lw=1.1)
    save(fig, '11-1')


# ================================================================ 图11.2
def fig_11_2():
    """不计关联时的单带示意图：(a)能带曲线 (b)态密度"""
    fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.25),
                            gridspec_kw=dict(width_ratios=[1.08, 1.0]))
    # -------- (a) 能带曲线
    ax = axs[0]
    plain_axes(ax)
    ax.set_xlim(-0.13, 1.32)
    ax.set_ylim(-0.17, 1.12)
    arrow_axis(ax, 0, 0, 0, 1.08)
    arrow_axis(ax, 0, 0, 1.28, 0, lw=1.0)
    ax.text(-0.04, 1.05, r'$E$', fontsize=10, ha='right', va='center')
    ax.plot([1.0, 1.0], [0, 1.045], 'k-', lw=1.2)          # BZ 界
    u = np.linspace(0, 1, 300)
    ax.plot(u, 0.16 + 0.79 * (0.5 - 0.5 * np.cos(np.pi * u)), 'k-', lw=1.5)
    ax.plot([0, 1.0], [0.555, 0.555], 'k--', lw=0.9, dashes=(4, 2))
    ax.text(-0.035, 0.555, r'$T_0$', fontsize=9.5, ha='right', va='center')
    # Δ 双向箭头
    ax.plot([1.06, 1.10], [0.16, 0.16], 'k-', lw=0.9)
    ax.plot([1.06, 1.10], [0.95, 0.95], 'k-', lw=0.9)
    ax.annotate('', xy=(1.08, 0.95), xytext=(1.08, 0.16),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=1.0,
                                shrinkA=0, shrinkB=0, mutation_scale=10))
    ax.text(1.13, 0.555, r'$\Delta$', fontsize=10, ha='left', va='center')
    ax.text(0, -0.06, r'$k$=0', fontsize=9, ha='center', va='top')
    ax.text(0.5, -0.06, r'$k\rightarrow$', fontsize=9, ha='center', va='top')
    ax.text(1.0, -0.06, u'BZ界', fontsize=9, ha='center', va='top',
            fontfamily='SimSun')

    # -------- (b) 态密度
    ax = axs[1]
    plain_axes(ax)
    ax.set_xlim(-0.13, 1.05)
    ax.set_ylim(-0.17, 1.12)
    arrow_axis(ax, 0, 0, 0, 1.08)
    arrow_axis(ax, 0, 0, 1.0, 0, lw=1.0)
    ax.text(-0.04, 1.05, r'$E$', fontsize=10, ha='right', va='center')
    th = np.linspace(0, np.pi, 200)
    ex, ey = 0.52 * np.sin(th), 0.075 + 0.44 * (1 - np.cos(th))
    ax.plot(ex, ey, 'k-', lw=1.5)
    # E_F 以下填充阴影
    m = ey <= 0.515
    poly = np.column_stack([ex[m], ey[m]])
    poly = np.vstack([poly, [0, 0.515]])
    ax.add_patch(Polygon(poly, closed=True, fc='white', ec='none', hatch='///'))
    ax.plot(ex, ey, 'k-', lw=1.5)
    ax.plot([0, 0.72], [0.515, 0.515], 'k--', lw=0.9, dashes=(4, 2))
    ax.text(0.745, 0.515, r'$E_{\rm F}$', fontsize=9.5, ha='left', va='center')
    ax.text(1.0, -0.075, r'$\rho_{\sigma}(E)|_{U=0}$', fontsize=9,
            ha='center', va='top')
    save(fig, '11-2')


# ================================================================ 图11.3
def fig_11_3():
    """计入关联后的能带分裂图：(a)子能带曲线 (b)子带态密度示意"""
    fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.3),
                            gridspec_kw=dict(width_ratios=[1.08, 1.0]))
    # -------- (a)
    ax = axs[0]
    plain_axes(ax)
    ax.set_xlim(-0.13, 1.30)
    ax.set_ylim(-0.15, 1.10)
    ax.plot([0, 0], [0, 1.03], 'k-', lw=1.2)
    ax.plot([1.0, 1.0], [0, 1.03], 'k-', lw=1.2)
    ax.plot([0, 1.0], [0, 0], 'k-', lw=1.2)
    u = np.linspace(0, 1, 300)
    ss = 0.5 - 0.5 * np.cos(np.pi * u)
    ax.plot(u, 0.68 + 0.29 * ss, 'k-', lw=1.5)              # E_k^(2)
    ax.plot(u, 0.14 + 0.24 * ss, 'k-', lw=1.5)              # E_k^(1)
    for y0, lab in [(0.825, r'$T_0$+$U$'), (0.26, r'$T_0$')]:
        tick(ax, 0, y0, -0.03, 0)
        ax.text(-0.045, y0, lab, fontsize=9.5, ha='right', va='center')
    ax.text(0.42, 0.90, r'$E_k^{(2)}$', fontsize=10, ha='left', va='center')
    ax.text(0.42, 0.355, r'$E_k^{(1)}$', fontsize=10, ha='left', va='center')
    ax.text(0, -0.055, r'$k$=0', fontsize=9, ha='center', va='top')
    ax.text(0.5, -0.055, r'$k$', fontsize=9, ha='center', va='top')
    ax.text(1.0, -0.055, u'BZ界', fontsize=9, ha='center', va='top',
            fontfamily='SimSun')

    # -------- (b)
    ax = axs[1]
    plain_axes(ax)
    ax.set_xlim(-0.13, 1.05)
    ax.set_ylim(-0.15, 1.10)
    arrow_axis(ax, 0, 0, 0, 1.06)
    arrow_axis(ax, 0, 0, 1.0, 0, lw=1.0)
    th = np.linspace(0, np.pi, 200)

    def blob(yc, hb, wb, hatch=False):
        ex, ey = wb * np.sin(th), yc + hb * np.cos(th)
        if hatch:
            ax.add_patch(Polygon(np.column_stack([ex, ey]), closed=True,
                                 fc='white', ec='none', hatch='///'))
        ax.plot(np.concatenate([[0], ex, [0]]),
                np.concatenate([[yc + hb], ey, [yc - hb]]), 'k-', lw=1.4)

    blob(0.835, 0.135, 0.34)                    # 上子带（空）
    blob(0.30, 0.170, 0.42, hatch=True)         # 下子带（满，影线）
    for y0, lab in [(0.835, r'$T_0$+$U$'), (0.30, r'$T_0$')]:
        tick(ax, 0, y0, -0.03, 0)
        ax.text(-0.045, y0, lab, fontsize=9.5, ha='right', va='center')
    ax.plot([0, 0.44], [0.55, 0.55], 'k--', lw=0.9, dashes=(4, 2))
    ax.text(0.455, 0.55, r'$E_{\rm F}$', fontsize=9.5, ha='left', va='center')
    ax.text(1.0, -0.075, r'$\rho_{\sigma}(E)$', fontsize=9.5, ha='center',
            va='top')
    save(fig, '11-3')


# ================================================================ 图11.4
def fig_11_4():
    """赫伯德模型中的 M-I 转变：两子带随 Δ/U 的演化，交叠区影线"""
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(3.35, 3.05))
    plain_axes(ax)
    ax.set_xlim(-0.09, 1.28)
    ax.set_ylim(-0.16, 1.09)
    arrow_axis(ax, 0, 0, 0, 1.05)
    arrow_axis(ax, 0, 0, 1.24, 0, lw=1.0)
    ax.text(-0.045, 1.02, r'$E$', fontsize=10, ha='right', va='center')
    ax.text(1.24, -0.055, r'$\Delta/U$', fontsize=10, ha='center', va='top')

    T0U, T0, EF, xc = 0.78, 0.32, 0.55, 0.42
    f_ut = PchipInterpolator([0, 0.2, 0.45, 0.7, 1.0],
                             [0.78, 0.845, 0.895, 0.935, 0.965])   # 上带顶
    f_ub = PchipInterpolator([0, 0.15, 0.3, xc],
                             [0.78, 0.72, 0.645, 0.55])            # 上带底
    f_lt = PchipInterpolator([0, 0.15, 0.3, xc],
                             [0.32, 0.40, 0.475, 0.55])            # 下带顶
    f_lb = PchipInterpolator([0, 0.15, 0.35, 0.6, 1.0],
                             [0.32, 0.20, 0.13, 0.095, 0.07])      # 下带底
    x1 = np.linspace(0, 1.0, 200)
    x2 = np.linspace(0, xc, 150)
    # 交叠区（金属相被填充态）影线
    poly = np.vstack([np.column_stack([x2, f_lt(x2)]),
                      [[1.0, EF]],
                      np.column_stack([x1[::-1], f_lb(x1[::-1])])])
    ax.add_patch(Polygon(poly, closed=True, fc='white', ec='none', hatch='///'))
    # 曲线
    ax.plot(x1, f_ut(x1), 'k-', lw=1.6)
    ax.plot(x2, f_ub(x2), 'k-', lw=1.6)
    ax.plot(x2, f_lt(x2), 'k-', lw=1.6)
    ax.plot(x1, f_lb(x1), 'k-', lw=1.6)
    # T0、T0+U、E_F
    for y0, lab in [(T0U, r'$T_0$+$U$'), (T0, r'$T_0$')]:
        tick(ax, 0, y0, -0.025, 0)
        ax.text(-0.035, y0, lab, fontsize=9.5, ha='right', va='center')
    ax.plot([0.18, 1.13], [EF, EF], 'k--', lw=0.9, dashes=(4, 2))
    ax.text(1.135, EF, r'$E_{\rm F}$', fontsize=9.5, ha='left', va='center')
    # (Δ/U)_c 虚线
    ax.plot([xc, xc], [EF, -0.005], 'k--', lw=0.9, dashes=(4, 2))
    ax.text(xc, -0.045, r'$(\frac{\Delta}{U})_{\rm c}$=$\frac{2}{\sqrt{3}}$',
            fontsize=9.5, ha='center', va='top')
    save(fig, '11-4')


# ================================================================ 图11.5
def fig_11_5():
    """局域电子态密度：洛伦兹共振峰"""
    fig, ax = plt.subplots(figsize=(2.75, 2.55))
    plain_axes(ax)
    ax.set_xlim(-0.09, 2.35)
    ax.set_ylim(-0.12, 1.22)
    arrow_axis(ax, 0, 0, 0, 1.16)
    arrow_axis(ax, 0, 0, 2.28, 0, lw=1.0)
    ax.text(-0.035, 1.12, r'$\rho_{d\sigma}$', fontsize=10, ha='right',
            va='center')
    ax.text(2.26, -0.045, r'$\omega$', fontsize=10, ha='center', va='top')
    x0, G = 0.72, 0.155
    x = np.linspace(0.0, 2.15, 600)
    y = G ** 2 / ((x - x0) ** 2 + G ** 2)
    ax.plot(x, y, 'k-', lw=1.6)
    # 峰高 1/πΓ
    ax.plot([0, x0], [1.0, 1.0], 'k--', lw=0.9, dashes=(4, 2))
    ax.text(-0.04, 1.0, r'$\dfrac{1}{\pi\Gamma}$', fontsize=10, ha='right',
            va='center')
    # 中心虚线 Ẽ_d
    ax.plot([x0, x0], [0, 1.0], 'k--', lw=0.9, dashes=(4, 2))
    ax.text(x0, -0.05, r'$\tilde{E}_d$', fontsize=10, ha='center', va='top')
    # 半高 Γ 记号
    yh = 0.5
    xh = x0 + G
    ax.plot([x0, xh], [yh, yh], 'k--', lw=0.9, dashes=(3, 1.8))
    tick(ax, xh, yh, 0.03, 0)
    ax.text(xh + 0.05, yh, r'$\Gamma$', fontsize=10, ha='left', va='center')
    save(fig, '11-5')


# ================================================================ 图11.6
def fig_11_6():
    """〈n_dσ〉的自洽解：(a) U=Γ 非磁解 (b) U=5Γ 磁性解"""
    fig, axs = plt.subplots(1, 2, figsize=(5.9, 3.25))

    def acot(x):
        return np.pi / 2 - np.arctan(x)

    def panel(ax, g, dots, labA, dashed):
        plain_axes(ax)
        ax.set_xlim(-0.30, 1.30)
        ax.set_ylim(-0.14, 1.10)
        ax.set_aspect('equal', adjustable='box')
        # 方框
        ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], 'k-', lw=1.2)
        ax.text(-0.05, 1.0, '1', fontsize=9, ha='right', va='center')
        ax.text(-0.05, 0.0, '0', fontsize=9, ha='right', va='center')
        ax.text(1.05, -0.01, '1', fontsize=9, ha='left', va='top')
        ax.text(0.5, -0.075, r'$\langle n_{d\uparrow}\rangle$', fontsize=10,
                ha='center', va='top')
        ax.text(-0.09, 0.62, r'$\langle n_{d\downarrow}\rangle$', fontsize=10,
                ha='right', va='center')
        # 陡曲线: n↑ = g·cot(πn↓)+0.5（在方框内：g·cot(πn)=1/2 处进入）
        na = np.arctan(2 * g) / np.pi
        nd = np.linspace(na, 1 - na, 300)
        ax.plot(nd, g / np.tan(np.pi * nd) + 0.5, 'k-', lw=1.5)
        # 浅曲线（11.2.44 的镜像）: n↓ = g·cot(πn↑)+0.5
        ny = np.linspace(na, 1 - na, 300)
        ax.plot(g / np.tan(np.pi * ny) + 0.5, ny, 'k-', lw=1.5)
        for (px, py) in dots:
            ax.plot(px, py, 'ko', ms=4.5)
        if dashed:
            ax.plot([0, dots[0][0]], [dots[0][1], dots[0][1]], 'k--', lw=0.9,
                    dashes=(4, 2))
            ax.plot([dots[0][0], dots[0][0]], [0, dots[0][1]], 'k--', lw=0.9,
                    dashes=(4, 2))
        if labA:
            ax.text(dots[0][0] + 0.045, dots[0][1] + 0.03, r'$A$', fontsize=11,
                    ha='left', va='center')

    # (a) U=Γ：唯一非磁解
    panel(axs[0], 1.0, [(0.5, 0.5)], True, True)
    # (b) U=5Γ：A + 两个对称磁解
    def acot_(x):
        return np.pi / 2 - np.arctan(x)
    g = 0.2
    f1 = lambda n: g / np.tan(np.pi * n) + 0.5
    f2 = lambda n: acot_(5 * (n - 0.5)) / np.pi
    ns = np.linspace(0.02, 0.98, 4001)
    gr = f1(ns) - f2(ns)
    roots = []
    for i in range(len(ns) - 1):
        if gr[i] == 0 or gr[i] * gr[i + 1] < 0:
            roots.append(0.5 * (ns[i] + ns[i + 1]))
    roots = sorted(roots)
    dots = [(r, f1(r)) for r in roots]
    panel(axs[1], g, dots, True, False)
    fig.subplots_adjust(wspace=0.42, bottom=0.10, top=0.97)
    save(fig, '11-6')


# ================================================================ 图11.7
def fig_11_7():
    """安德逊哈特利-福克解的磁性与非磁性区域（半椭圆相界）"""
    fig, ax = plt.subplots(figsize=(3.6, 2.45))
    plain_axes(ax)
    ax.set_xlim(-0.16, 1.15)
    ax.set_ylim(-0.20, 1.13)
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], 'k-', lw=1.3)
    th = np.linspace(0, np.pi, 300)
    ex, ey = 0.5 - 0.5 * np.cos(th), np.sin(th)
    ax.add_patch(Polygon(np.column_stack([ex, ey]), closed=True, fc='white',
                         ec='none', hatch='///'))
    ax.plot(ex, ey, 'k-', lw=1.8)
    ax.text(0.135, 0.80, u'非磁', fontsize=10, ha='center', va='center',
            fontfamily='SimSun')
    ax.text(0.5, 0.47, u'磁', fontsize=10, ha='center', va='center',
            fontfamily='SimSun',
            bbox=dict(fc='white', ec='none', pad=1.5))
    ax.text(-0.045, 1.0, '1', fontsize=9.5, ha='right', va='center')
    ax.text(-0.045, 0.0, '0', fontsize=9.5, ha='right', va='center')
    ax.text(0.0, -0.055, '0', fontsize=9.5, ha='center', va='top')
    ax.text(1.0, -0.055, '1', fontsize=9.5, ha='center', va='top')
    ax.text(-0.115, 0.5, r'$\dfrac{\pi\Gamma}{U}$', fontsize=10, ha='center',
            va='center', rotation=90)
    ax.text(0.5, -0.10, r'$(E_{\rm F}-E_{\rm d})/U$', fontsize=10, ha='center',
            va='top')
    save(fig, '11-7')


# ================================================================ 图11.8
def fig_11_8():
    """电阻极小示意图：R = R声子 + R杂质"""
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(3.7, 3.35))
    plain_axes(ax)
    ax.set_xlim(-0.14, 1.14)
    ax.set_ylim(-0.14, 1.10)
    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], 'k-', lw=1.3)
    x = np.linspace(0.02, 0.98, 300)
    ax.plot(x, 0.44 + 0.40 * ((x - 0.47) / 0.50) ** 2, 'k-', lw=1.7)   # R
    xr = np.linspace(0.20, 0.97, 200)
    fr = PchipInterpolator([0.20, 0.35, 0.47, 0.65, 0.97],
                           [0.13, 0.23, 0.345, 0.47, 0.66])
    ax.plot(xr, fr(xr), 'k--', lw=1.4, dashes=(6, 3))                  # R声
    xi = np.linspace(0.03, 0.86, 200)
    fi = PchipInterpolator([0.03, 0.2, 0.35, 0.47, 0.65, 0.86],
                           [0.72, 0.56, 0.44, 0.345, 0.25, 0.19])
    ax.plot(xi, fi(xi), 'k-.', lw=1.4, dashes=(7, 2.5, 1.5, 2.5))      # R杂
    ax.plot([0.47, 0.47], [0.345, 0.0], 'k--', lw=1.0, dashes=(4, 2))
    ax.text(0.47, -0.055, u'极小点', fontsize=9.5, ha='center', va='top',
            fontfamily='SimSun')
    ax.text(0.97, -0.055, r'$T$', fontsize=10, ha='center', va='top')
    ax.text(-0.035, 0.79, r'$R$', fontsize=10, ha='right', va='center')
    ax.text(0.875, 0.615, r'$R$', fontsize=10, ha='left', va='center')
    ax.text(0.915, 0.60, u'声', fontsize=8.5, ha='left', va='center',
            fontfamily='SimSun')
    ax.text(0.795, 0.235, r'$R$', fontsize=10, ha='left', va='center',
            bbox=dict(fc='white', ec='none', pad=0.5))
    ax.text(0.835, 0.22, u'杂', fontsize=8.5, ha='left', va='center',
            fontfamily='SimSun',
            bbox=dict(fc='white', ec='none', pad=0.5))
    save(fig, '11-8')


# ================================================================ 图11.9
def fig_11_9():
    """自旋倒逆散射的二极过程：(a)电子中间态 (b)空穴中间态"""
    fig, axs = plt.subplots(1, 2, figsize=(5.6, 3.9))
    Y0 = 0.0
    DY = -1.12

    def cu(ax, x, y):
        s = 0.14
        ax.plot([x - s, x + s], [y - s, y + s], 'k-', lw=1.2)
        ax.plot([x - s, x + s], [y + s, y - s], 'k-', lw=1.2)

    def oxy(ax, x, y):
        ax.add_patch(Circle((x, y), 0.115, fill=False, lw=1.3, ec='k'))

    def spin(ax, x, y, up):
        if up:
            arrow_axis(ax, x, y + 0.17, x, y + 0.52, lw=1.0)
        else:
            arrow_axis(ax, x, y + 0.52, x, y + 0.17, lw=1.0)

    def spin2(ax, x, y):
        spin(ax, x - 0.09, y, False)
        spin(ax, x + 0.09, y, True)

    def prog(ax, x, y):
        arrow_axis(ax, x, y - 0.30, x, y - 0.82, lw=1.2)

    def hop(ax, x1, x2, y):
        """虚线跃迁弧：自 x1 上方弧至 x2 上方，箭头指向 x2"""
        S = np.array([x1, y + 0.16])
        E = np.array([x2, y + 0.16])
        M = 0.5 * (S + E) + np.array([0.0, 0.55])
        t = np.linspace(0, 1, 60)
        B = ((1 - t) ** 2)[:, None] * S + (2 * t * (1 - t))[:, None] * M + \
            (t ** 2)[:, None] * E
        ax.plot(B[:, 0], B[:, 1], 'k--', lw=1.1, dashes=(4, 2.2))
        p0 = B[-6]
        ax.annotate('', xy=(E[0], E[1] + 0.02), xytext=(p0[0], p0[1]),
                    arrowprops=dict(arrowstyle='-|>', color='k', lw=1.1,
                                    mutation_scale=13))

    for ax in axs:
        plain_axes(ax)
        ax.set_xlim(-1.55, 1.55)
        ax.set_ylim(-5.05, 0.75)
        ax.set_aspect('equal')

    ax = axs[0]
    rows = [Y0 + i * DY for i in range(5)]
    cu(ax, -0.9, rows[0]); spin(ax, -0.9, rows[0], True)
    oxy(ax, 0, rows[0])
    cu(ax, 0.9, rows[0]); spin(ax, 0.9, rows[0], False)
    hop(ax, 0.72, 0.16, rows[0])
    prog(ax, 0, rows[0])
    cu(ax, -0.9, rows[1]); spin(ax, -0.9, rows[1], True)
    oxy(ax, 0, rows[1]); spin(ax, 0, rows[1], False)
    cu(ax, 0.9, rows[1])
    hop(ax, -0.72, -0.16, rows[1])
    prog(ax, 0, rows[1])
    cu(ax, -0.9, rows[2])
    oxy(ax, 0, rows[2]); spin2(ax, 0, rows[2])
    cu(ax, 0.9, rows[2])
    hop(ax, 0.16, 0.72, rows[2])
    prog(ax, 0, rows[2])
    cu(ax, -0.9, rows[3])
    oxy(ax, 0, rows[3])
    cu(ax, 0.9, rows[3]); spin(ax, 0.9, rows[3], True)
    hop(ax, -0.16, -0.72, rows[3])
    prog(ax, 0, rows[3])
    cu(ax, -0.9, rows[4]); spin(ax, -0.9, rows[4], False)
    oxy(ax, 0, rows[4])
    cu(ax, 0.9, rows[4]); spin(ax, 0.9, rows[4], True)
    save(fig, '11-9')

    ax = axs[1]
    cu(ax, -0.9, rows[0]); spin(ax, -0.9, rows[0], True)
    oxy(ax, 0, rows[0])
    cu(ax, 0.9, rows[0]); spin(ax, 0.9, rows[0], False)
    hop(ax, -0.72, -0.16, rows[0])
    prog(ax, 0, rows[0])
    cu(ax, -0.9, rows[1])
    oxy(ax, 0, rows[1]); spin(ax, 0, rows[1], True)
    cu(ax, 0.9, rows[1]); spin(ax, 0.9, rows[1], False)
    hop(ax, 0.16, 0.72, rows[1])
    prog(ax, 0, rows[1])
    cu(ax, -0.9, rows[2])
    oxy(ax, 0, rows[2])
    cu(ax, 0.9, rows[2]); spin2(ax, 0.9, rows[2])
    hop(ax, 0.72, 0.16, rows[2])
    prog(ax, 0, rows[2])
    cu(ax, -0.9, rows[3])
    oxy(ax, 0, rows[3])
    cu(ax, 0.9, rows[3]); spin(ax, 0.9, rows[3], True)
    hop(ax, -0.16, -0.72, rows[3])
    prog(ax, 0, rows[3])
    cu(ax, -0.9, rows[4]); spin(ax, -0.9, rows[4], False)
    oxy(ax, 0, rows[4])
    cu(ax, 0.9, rows[4]); spin(ax, 0.9, rows[4], True)
    save(fig, '11-9')


# ================================================================ 图11.10
def fig_11_10():
    """有效杂质磁矩的温度曲线（AuV）"""
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(3.7, 2.9))
    plain_axes(ax)
    ax.set_xlim(-22, 325)
    ax.set_ylim(-0.28, 3.20)
    ax.plot([0, 0], [0, 3.05], 'k-', lw=1.2)
    ax.plot([0, 315], [0, 0], 'k-', lw=1.2)
    for v in (1, 2, 3):
        tick(ax, 0, v, -5, 0)
        ax.text(-9, v, str(v), fontsize=9, ha='right', va='center')
    for v in (100, 200, 300):
        tick(ax, v, 0, 0, -0.07)
        ax.text(v, -0.14, str(v), fontsize=9, ha='center', va='top')
    ax.text(-30, 1.72, r'$\dfrac{\mu_{\rm eff}}{\mu_{\rm B}}$', fontsize=11,
            ha='center', va='center')
    ax.text(150, -0.62, r'$T$/K', fontsize=10, ha='center', va='top')
    f = PchipInterpolator([20, 40, 60, 80, 100, 130, 160, 200, 250, 300],
                          [0.50, 0.95, 1.25, 1.50, 1.70, 1.92, 2.07,
                           2.22, 2.33, 2.40])
    xx = np.linspace(20, 300, 300)
    ax.plot(xx, f(xx), 'k-', lw=1.7)
    save(fig, '11-10')


# ================================================================ 图11.11
def fig_11_11():
    """CuCr 合金杂质比热容的 lnT 曲线"""
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(4.35, 3.15))
    for s in ax.spines.values():
        s.set_linewidth(1.1)
    ax.set_xlim(np.log10(0.015), np.log10(32))
    ax.set_ylim(0, 3.1)
    ax.set_xticks([np.log10(0.1), 0, 1])
    ax.set_xticklabels(['0.1', '1.0', '10.0'])
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(['1.0', '2.0', '3.0'])
    ax.tick_params(direction='in', length=3.5, labelsize=9)
    ax.text(np.log10(0.015), -0.32, '0', fontsize=9, ha='center', va='top')
    ax.set_xlabel(r'$T$/K', fontsize=10)
    ax.text(-0.20, 0.55, r'$\dfrac{\Delta c}{x}$ (J/K$-$mol$\cdot$Cr)',
            fontsize=10, ha='center', va='center', rotation=90,
            transform=ax.transAxes)
    lt = np.linspace(np.log10(0.015), np.log10(30), 400)
    f = PchipInterpolator([-1.82, -1.5, -1.2, -1.0, -0.7, -0.4, -0.2, 0.0,
                           0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.47],
                          [0.42, 0.55, 0.75, 0.92, 1.28, 1.72, 2.05, 2.25,
                           2.28, 2.24, 2.02, 1.62, 1.15, 0.80, 0.55])
    ax.plot(lt, f(lt), 'k-', lw=1.8)
    save(fig, '11-11')


# ================================================================ 图11.12
def fig_11_12():
    """低温杂质电阻的温度曲线（CuFe 合金）"""
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    for s in ax.spines.values():
        s.set_linewidth(1.1)
    ax.set_xlim(np.log10(0.02), np.log10(30))
    ax.set_ylim(0, 1.0)
    ax.set_xticks([-1, 0, 1])
    ax.set_xticklabels(['0.1', '1.0', '10.0'])
    ax.set_yticks([0.3, 0.65])
    ax.set_yticklabels(['', ''])
    ax.tick_params(direction='in', length=3.5, labelsize=9)
    ax.set_xlabel(r'$T$/K', fontsize=10)
    ax.text(-0.13, 0.5, r'$R$', fontsize=11, ha='center', va='center',
            transform=ax.transAxes)
    ax.text(-0.085, 0.435, u'杂', fontsize=8.5, ha='center', va='center',
            transform=ax.transAxes, fontfamily='SimSun')
    lt = np.linspace(np.log10(0.03), np.log10(25), 400)
    f = PchipInterpolator([-1.5, -1.0, -0.5, 0.0, 0.3, 0.5, 0.7, 0.9, 1.0,
                           1.15, 1.3, 1.4],
                          [0.78, 0.785, 0.792, 0.80, 0.795, 0.775, 0.72,
                           0.58, 0.45, 0.35, 0.30, 0.28])
    ax.plot(lt, f(lt), 'k-', lw=1.8)
    save(fig, '11-12')


# ================================================================ 图11.13
def fig_11_13():
    """杂质磁化率的温度曲线"""
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(4.4, 2.85))
    for s in ax.spines.values():
        s.set_linewidth(1.1)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    ax.tick_params(direction='in', length=0)
    ax.set_xlabel(r'$T$', fontsize=11)
    ax.text(-0.09, 0.55, r'$\chi^{-1}$', fontsize=12, ha='center', va='center',
            transform=ax.transAxes)
    ax.text(-0.035, 0.415, u'杂', fontsize=8.5, ha='center', va='center',
            transform=ax.transAxes, fontfamily='SimSun')
    f = PchipInterpolator([0.0, 0.05, 0.12, 0.25, 0.40, 0.55, 0.70, 0.80,
                           0.87],
                          [0.28, 0.273, 0.28, 0.315, 0.385, 0.49, 0.63,
                           0.76, 0.88])
    xx = np.linspace(0.0, 0.87, 300)
    ax.plot(xx, f(xx), 'k-', lw=1.8)
    ax.text(0.60, 0.40, r'$\chi^{-1}\sim T$', fontsize=11, ha='left',
            va='center')
    ax.text(0.09, 0.12, r'$\chi\sim(1-BT^2)$', fontsize=11, ha='left',
            va='center')
    save(fig, '11-13')


# ================================================================ 图11.14
def fig_11_14():
    """杂质上的 d 电子组态：(a)零占据 (b)单占据 (c)双占据"""
    fig, axs = plt.subplots(1, 3, figsize=(5.9, 1.15))
    occ = [(False, False), (False, True), (True, True)]
    for k, ax in enumerate(axs):
        plain_axes(ax)
        ax.set_xlim(-0.72, 1.0)
        ax.set_ylim(0.05, 1.42)
        ax.plot([0, 0.82], [1.05, 1.05], 'k-', lw=1.4)
        ax.plot([0, 0.82], [0.42, 0.42], 'k-', lw=1.4)
        ax.text(-0.06, 1.05, r'$E_{\rm d}$+$U$', fontsize=10, ha='right',
                va='center')
        ax.text(-0.06, 0.42, r'$E_{\rm d}$', fontsize=10, ha='right',
                va='center')
        o1, o2 = occ[k]
        ax.plot(0.41, 1.05, 'o', ms=6.5, mfc='white' if not o1 else 'k',
                mec='k', mew=1.1)
        ax.plot(0.41, 0.42, 'o', ms=6.5, mfc='white' if not o2 else 'k',
                mec='k', mew=1.1)
    save(fig, '11-14')


# ================================================================ 图11.15
def fig_11_15():
    """重整杂化带的示意图：ε_k=Dcos(ka), E_f=-0.2D, Ṽ²=0.1D²"""
    fig, ax = plt.subplots(figsize=(4.35, 3.3))
    for s in ax.spines.values():
        s.set_linewidth(1.1)
    ax.set_xlim(0, 1)
    ax.set_ylim(-1.16, 1.16)
    ax.set_xticks([]); ax.set_yticks([])
    ax.tick_params(direction='in', length=0)
    for y0, lab in [(1.0, r'$D$'), (0.0, r'$0$'), (-0.2, r'$E_{f}$'),
                    (-1.0, r'$-D$')]:
        ax.text(-0.025, y0, lab, fontsize=10, ha='right', va='center')
        if lab != r'$E_{f}$':
            tick(ax, 0, y0, -0.015, 0)
    ax.text(-0.075, 0.42, r'$\omega$', fontsize=11, ha='center', va='center')
    ax.plot([0, 1], [-0.2, -0.2], 'k--', lw=0.9, dashes=(4, 2))
    ax.text(0.5, -1.24, r'$k$', fontsize=10, ha='center', va='top')
    ax.text(0.012, -1.21, r'$0$', fontsize=10, ha='center', va='top')
    ax.text(1.0, -1.21, r'$\pi/a$', fontsize=10, ha='center', va='top')

    u = np.linspace(0, 1, 400)
    eps = -np.cos(np.pi * u)                       # ε_k/D，取 -Dcos(ka)
    Ef, V2 = -0.2, 0.1
    half = np.sqrt(((eps - Ef) / 2) ** 2 + V2)
    wp = (eps + Ef) / 2 + half
    wm = (eps + Ef) / 2 - half
    ax.plot(u, eps, 'k--', lw=1.0, dashes=(4, 2))
    ax.plot(u, wp, 'k-', lw=1.7)
    ax.plot(u, wm, 'k-', lw=1.7)
    i1 = np.searchsorted(u, 0.33)
    ax.text(u[i1] - 0.02, wp[i1] + 0.13, r'$\omega_k^+$', fontsize=10,
            ha='center', va='bottom')
    ax.text(0.60, wm[np.searchsorted(u, 0.60)] - 0.13, r'$\omega_k^-$',
            fontsize=10, ha='center', va='top')
    i2 = np.searchsorted(u, 0.75)
    ax.text(u[i2] + 0.03, eps[i2] + 0.02, r'$\varepsilon_k$', fontsize=10,
            ha='left', va='center')
    save(fig, '11-15')


# ================================================================ 图11.16
def fig_11_16():
    """f-DOS 和 c-DOS 示意图"""
    fig, ax = plt.subplots(figsize=(4.35, 3.55))
    plain_axes(ax)
    ax.set_xlim(-0.34, 1.06)
    ax.set_ylim(-0.10, 1.06)
    ax.add_patch(Rectangle((0, 0), 1.0, 1.0, fc='none', ec='k', lw=1.3))
    yb, yclow = 0.32, 0.145
    wa, wb, Ef, wc, wd = 0.115, 0.475, 0.535, 0.60, 0.94
    Dn, Dp = 0.235, 0.83
    # 基线 ω 轴
    ax.plot([0, 1.0], [yb, yb], 'k-', lw=1.1)
    # c-DOS 常值 1/2D（矩形盒）
    for x0, x1 in [(wa, wb), (wc, wd)]:
        ax.plot([x0, x1], [yclow, yclow], 'k-', lw=1.1)
        ax.plot([x0, x0], [yclow, yb], 'k-', lw=1.1)
    ax.plot([wb, wb], [yclow, 1.0], 'k-', lw=1.4)       # ω_b 处竖直发散线
    ax.plot([wc, wc], [yclow, 1.0], 'k-', lw=1.4)       # ω_c 处
    # f-DOS 曲线
    C = (1.0 - yb) / ((wb - Ef) ** -2)                  # 顶点达到 1.0
    xL = np.linspace(wa, wb - 0.004, 300)
    yL = yb + C * (xL - Ef) ** -2
    xR = np.linspace(wc + 0.004, wd, 300)
    yR = yb + C * (xR - Ef) ** -2
    ax.plot(xL, np.minimum(yL, 1.0), 'k-', lw=1.6)
    ax.plot(xR, np.minimum(yR, 1.0), 'k-', lw=1.6)
    # 1/2D 双箭头
    ax.annotate('', xy=(0.31, yclow), xytext=(0.31, yb),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=1.0,
                                shrinkA=0, shrinkB=0, mutation_scale=10))
    ax.text(0.31, 0.115, r'$1/2D$', fontsize=8.5, ha='center', va='top',
            zorder=5)
    # 标注
    ax.text(-0.035, yb, r'$\rho_{\rm c}(\omega)$', fontsize=10, ha='right',
            va='center')
    arrow_axis(ax, -0.09, yb - 0.055, -0.09, yb - 0.16, lw=1.0)
    ax.text(0.315, 0.62, r'$\rho_{\rm f}(\omega)$', fontsize=10, ha='center',
            va='center')
    tick(ax, Ef, yb, 0, 0.022)
    ax.text(Ef, yb + 0.045, r'$E_{f}$', fontsize=10, ha='center', va='bottom')
    ax.annotate('', xy=(0.535, yb - 0.145), xytext=(0.46, yb - 0.145),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                mutation_scale=11))
    ax.text(0.443, yb - 0.145, r'$\omega$', fontsize=10, ha='right',
            va='center')
    for x0, lab, ha in [(wa, r'$\omega_{\rm a}$', 'center'), (Dn, r'$-D$', 'center'),
                    (wb, r'$\omega_{\rm b}$', 'right'), (wc, r'$\omega_{\rm c}$', 'left'),
                    (Dp, r'$D$', 'center'), (wd, r'$\omega_{\rm d}$', 'center')]:
        tick(ax, x0, yb, 0, -0.02)
        off = -0.012 if ha == 'right' else (0.012 if ha == 'left' else 0.0)
        ax.text(x0 + off, yb - 0.033, lab, fontsize=9.5, ha=ha, va='top')
    save(fig, '11-16')


# ================================================================ 图11.17
def fig_11_17():
    """铜空穴自旋间超交换的两个4阶通道：(a)不含U (b)含U"""
    fig, axs = plt.subplots(1, 2, figsize=(6.3, 4.5))

    def cu(ax, x, y):
        s = 0.15
        ax.plot([x - s, x + s], [y - s, y + s], 'k-', lw=1.2)
        ax.plot([x - s, x + s], [y + s, y - s], 'k-', lw=1.2)

    def oxy(ax, x, y):
        ax.add_patch(Circle((x, y), 0.125, fill=False, lw=1.3, ec='k'))

    def spin(ax, x, y, up):
        if up:
            arrow_axis(ax, x, y + 0.19, x, y + 0.56, lw=1.0)
        else:
            arrow_axis(ax, x, y + 0.56, x, y + 0.19, lw=1.0)

    def spin2(ax, x, y):
        spin(ax, x - 0.10, y, False)
        spin(ax, x + 0.10, y, True)

    def prog(ax, x, y):
        arrow_axis(ax, x, y - 0.28, x, y - 0.60, lw=1.3)

    def hop(ax, x1, x2, y):
        S = np.array([x1, y + 0.18])
        E = np.array([x2, y + 0.18])
        M = 0.5 * (S + E) + np.array([0.0, 0.60])
        t = np.linspace(0, 1, 60)
        B = ((1 - t) ** 2)[:, None] * S + (2 * t * (1 - t))[:, None] * M + \
            (t ** 2)[:, None] * E
        ax.plot(B[:, 0], B[:, 1], 'k--', lw=1.1, dashes=(4, 2.2))
        p0 = B[-6]
        ax.annotate('', xy=(E[0], E[1] + 0.02), xytext=(p0[0], p0[1]),
                    arrowprops=dict(arrowstyle='-|>', color='k', lw=1.1,
                                    mutation_scale=13))

    for ax in axs:
        plain_axes(ax)
        ax.set_xlim(-1.7, 1.7)
        ax.set_ylim(-5.55, 0.8)
        ax.set_aspect('equal')

    ax = axs[0]
    rows = [0.0, -1.25, -2.5, -3.75, -5.0]
    cu(ax, -1.0, rows[0]); spin(ax, -1.0, rows[0], True)
    oxy(ax, 0, rows[0])
    cu(ax, 1.0, rows[0]); spin(ax, 1.0, rows[0], False)
    hop(ax, 0.80, 0.18, rows[0]); prog(ax, 0, rows[0])
    cu(ax, -1.0, rows[1]); spin(ax, -1.0, rows[1], True)
    oxy(ax, 0, rows[1]); spin(ax, 0, rows[1], False)
    cu(ax, 1.0, rows[1])
    hop(ax, -0.80, -0.18, rows[1]); prog(ax, 0, rows[1])
    cu(ax, -1.0, rows[2])
    oxy(ax, 0, rows[2]); spin2(ax, 0, rows[2])
    cu(ax, 1.0, rows[2])
    hop(ax, 0.18, 0.80, rows[2]); prog(ax, 0, rows[2])
    cu(ax, -1.0, rows[3])
    oxy(ax, 0, rows[3])
    cu(ax, 1.0, rows[3]); spin(ax, 1.0, rows[3], True)
    hop(ax, -0.18, -0.80, rows[3]); prog(ax, 0, rows[3])
    cu(ax, -1.0, rows[4]); spin(ax, -1.0, rows[4], False)
    oxy(ax, 0, rows[4])
    cu(ax, 1.0, rows[4]); spin(ax, 1.0, rows[4], True)
    save(fig, '11-17')

    ax = axs[1]
    cu(ax, -1.0, rows[0]); spin(ax, -1.0, rows[0], True)
    oxy(ax, 0, rows[0])
    cu(ax, 1.0, rows[0]); spin(ax, 1.0, rows[0], False)
    hop(ax, -0.80, -0.18, rows[0]); prog(ax, 0, rows[0])
    cu(ax, -1.0, rows[1])
    oxy(ax, 0, rows[1]); spin(ax, 0, rows[1], True)
    cu(ax, 1.0, rows[1]); spin(ax, 1.0, rows[1], False)
    hop(ax, 0.18, 0.80, rows[1]); prog(ax, 0, rows[1])
    cu(ax, -1.0, rows[2])
    oxy(ax, 0, rows[2])
    cu(ax, 1.0, rows[2]); spin2(ax, 1.0, rows[2])
    hop(ax, 0.80, 0.18, rows[2]); prog(ax, 0, rows[2])
    cu(ax, -1.0, rows[3])
    oxy(ax, 0, rows[3])
    cu(ax, 1.0, rows[3]); spin(ax, 1.0, rows[3], True)
    hop(ax, -0.18, -0.80, rows[3]); prog(ax, 0, rows[3])
    cu(ax, -1.0, rows[4]); spin(ax, -1.0, rows[4], False)
    oxy(ax, 0, rows[4])
    cu(ax, 1.0, rows[4]); spin(ax, 1.0, rows[4], True)
    save(fig, '11-17')


# ================================================================ 图11.18
def fig_11_18():
    """氧空穴(2p5)与铜空穴(3d9)的杂化示意图（相位±）"""
    fig, ax = plt.subplots(figsize=(4.9, 4.35))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-3.15, 3.55)
    ax.set_ylim(-2.75, 2.45)

    def porb(px, py, horiz, lout, lin, wout, win, s_out, s_in):
        """p 轨道：两椭圆在腰(px,py)相切，lout/lin 为两瓣中心距腰的长度"""
        if horiz:
            ax.add_patch(Ellipse((px - lout, py), 2 * lout, wout, fill=False,
                                 lw=1.3, ec='k'))
            ax.add_patch(Ellipse((px + lin, py), 2 * lin, win, fill=False,
                                 lw=1.3, ec='k'))
            ax.text(px - lout, py, s_out, fontsize=12, ha='center',
                    va='center')
            ax.text(px + lin, py, s_in, fontsize=12, ha='center',
                    va='center')
        else:
            ax.add_patch(Ellipse((px, py + lout), wout, 2 * lout, fill=False,
                                 lw=1.3, ec='k'))
            ax.add_patch(Ellipse((px, py - lin), win, 2 * lin, fill=False,
                                 lw=1.3, ec='k'))
            ax.text(px, py + lout, s_out, fontsize=12, ha='center',
                    va='center')
            ax.text(px, py - lin, s_in, fontsize=12, ha='center',
                    va='center')

    V = 1.55          # 菱形顶点（氧腰点）距中心
    LL, WW = 0.44, 0.36   # 瓣心距腰/瓣宽
    # 4 个氧 p 轨道（腰在菱形顶点）：外瓣相位、内瓣相位
    porb(0, V, False, LL, LL, WW, WW, r'$-$', r'$+$')               # 上
    porb(0, -V, False, LL, LL, WW, WW, r'$+$', r'$-$')              # 下
    porb(-V, 0, True, LL, LL, WW, WW, r'$-$', r'$+$')               # 左
    porb(V, 0, True, LL, LL, WW, WW, r'$+$', r'$-$')                # 右
    # Cu d_{x2-y2}：横瓣+、纵瓣−
    for cx, cy, w, h, sg in [(-0.42, 0, 0.80, 0.34, r'$+$'),
                             (0.42, 0, 0.80, 0.34, r'$+$'),
                             (0, 0.42, 0.34, 0.80, r'$-$'),
                             (0, -0.42, 0.34, 0.80, r'$-$')]:
        ax.add_patch(Ellipse((cx, cy), w, h, fill=False, lw=1.3, ec='k'))
        ax.text(cx, cy, sg, fontsize=12, ha='center', va='center')
    # 虚线菱形（连接四个氧腰点）
    vx = [(0, V), (V, 0), (0, -V), (-V, 0)]
    for i in range(4):
        x0, y0 = vx[i]
        x1, y1 = vx[(i + 1) % 4]
        ax.plot([x0, x1], [y0, y1], 'k--', lw=1.1, dashes=(5, 2.5))
    # 轨道标记
    ax.text(0.30, V + 0.42, r'$\boldsymbol{p}_{i+\frac{1}{2}\hat{y}}$',
            fontsize=11, ha='left', va='center')
    ax.text(0.30, -V - 0.42, r'$\boldsymbol{p}_{i-\frac{1}{2}\hat{y}}$',
            fontsize=11, ha='left', va='center')
    ax.text(-V - 0.35, 0.42, r'$\boldsymbol{p}_{i-\frac{1}{2}\hat{x}}$',
            fontsize=11, ha='center', va='center')
    ax.text(V + 0.40, 0.42, r'$\boldsymbol{p}_{i+\frac{1}{2}\hat{x}}$',
            fontsize=11, ha='center', va='center')
    ax.text(0.28, -0.78, r'$\boldsymbol{d}_i$', fontsize=11, ha='left',
            va='center')
    save(fig, '11-18')


# ================================================================ 图11.19
def fig_11_19():
    """氧空穴的对称组合轨道 P_iσ（泪滴形瓣，实线方块）"""
    fig, ax = plt.subplots(figsize=(4.6, 4.35))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-3.3, 3.4)
    ax.set_ylim(-2.85, 2.6)

    def teardrop(tip, ang, L, W):
        d = np.array([np.cos(ang), np.sin(ang)])
        n = np.array([-d[1], d[0]])
        P = lambda a, b: tuple(np.asarray(tip) + a * L * d + b * W * n)
        verts = [tuple(tip),
                 P(0.15, 0.75), P(0.55, 1.0), P(0.95, 0.55),
                 P(1.10, 0.25), P(1.10, -0.25), P(0.95, -0.55),
                 P(0.55, -1.0), P(0.15, -0.75),
                 tuple(tip)]
        codes = [Path.MOVETO] + [Path.CURVE4] * 9
        ax.add_patch(PathPatch(Path(verts, codes), fc='white', ec='k',
                               lw=1.3, zorder=3))

    wt = {'n': (0, 1.18), 'e': (1.32, 0), 's': (0, -1.18), 'w': (-1.32, 0)}
    ANG = {'n': -np.pi / 2, 'e': np.pi, 's': np.pi / 2, 'w': 0.0}
    INN = {'n': np.pi / 2, 'e': 0.0, 's': -np.pi / 2, 'w': np.pi}
    # 外瓣（指向外）与内瓣（指向中心）
    outer_sign = {'n': r'$+$', 's': r'$+$', 'w': r'$-$', 'e': r'$-$'}
    inner_sign = {'n': r'$-$', 's': r'$-$', 'w': r'$+$', 'e': r'$+$'}
    for k in wt:
        teardrop(wt[k], ANG[k], 0.62, 0.40)
        teardrop(wt[k], INN[k], 0.80, 0.42)
    # 实线方块（菱形）
    order = ['n', 'e', 's', 'w']
    for i in range(4):
        x0, y0 = wt[order[i]]
        x1, y1 = wt[order[(i + 1) % 4]]
        ax.plot([x0, x1], [y0, y1], 'k-', lw=1.2, zorder=4)
    # 瓣内符号
    ax.text(0, 1.18 + 0.40, outer_sign['n'], fontsize=12, ha='center',
            va='center', zorder=5)
    ax.text(0, 1.18 - 0.42, inner_sign['n'], fontsize=12, ha='center',
            va='center', zorder=5)
    ax.text(0, -1.18 - 0.40, outer_sign['s'], fontsize=12, ha='center',
            va='center', zorder=5)
    ax.text(0, -1.18 + 0.42, inner_sign['s'], fontsize=12, ha='center',
            va='center', zorder=5)
    ax.text(-1.32 - 0.42, 0, outer_sign['w'], fontsize=12, ha='center',
            va='center', zorder=5)
    ax.text(-1.32 + 0.44, 0, inner_sign['w'], fontsize=12, ha='center',
            va='center', zorder=5)
    ax.text(1.32 + 0.42, 0, outer_sign['e'], fontsize=12, ha='center',
            va='center', zorder=5)
    ax.text(1.32 - 0.44, 0, inner_sign['e'], fontsize=12, ha='center',
            va='center', zorder=5)
    # 标记
    ax.text(0.55, 1.80, r'$-\boldsymbol{p}_{i+\frac{1}{2}\hat{y}}$',
            fontsize=11, ha='left', va='center')
    ax.text(0.30, -1.86, r'$\boldsymbol{p}_{i-\frac{1}{2}\hat{y}}$',
            fontsize=11, ha='left', va='center')
    ax.text(-1.95, 0.40, r'$\boldsymbol{p}_{i-\frac{1}{2}\hat{x}}$',
            fontsize=11, ha='center', va='center')
    ax.text(2.18, 0.40, r'$-\boldsymbol{p}_{i+\frac{1}{2}\hat{x}}$',
            fontsize=11, ha='center', va='center')
    save(fig, '11-19')


# ================================================================ 图11.20
def fig_11_20():
    """推广 t-J 模型的示意相图"""
    fig, ax = plt.subplots(figsize=(4.4, 3.35))
    plain_axes(ax)
    ax.set_xlim(-0.07, 1.13)
    ax.set_ylim(-0.17, 1.13)
    arrow_axis(ax, 0, 0, 0, 1.09)
    arrow_axis(ax, 0, 0, 1.09, 0, lw=1.0)
    ax.text(-0.035, 1.05, r'$T$', fontsize=11, ha='right', va='center')
    ax.text(1.07, -0.045, r'$\delta$', fontsize=11, ha='center', va='top')
    # 反铁磁条带
    ax.add_patch(Rectangle((0, 0), 0.17, 0.97, fc='white', ec='none',
                           hatch='///'))
    ax.plot([0.17, 0.17], [0, 0.97], 'k-', lw=1.2)
    vtext(ax, 0.085, 0.44, u'反铁磁', fontsize=9.5, fontfamily='SimSun',
          bbox=dict(fc='white', ec='none', pad=1.2))
    # T_B 直线
    ax.plot([0, 0.90], [0, 0.97], 'k-', lw=1.4)
    ax.text(0.90, 0.99, r'$T_{\rm B}$', fontsize=10.5, ha='left', va='bottom')
    # T_RVB 曲线（四分之一椭圆）
    xx = np.linspace(0, 0.72, 300)
    yr = 0.72 * np.sqrt(1 - (xx / 0.72) ** 2)
    ax.plot(xx, yr, 'k-', lw=1.7)
    ax.text(0.30, 0.775, r'$T_{\rm RVB}$', fontsize=10.5, ha='center',
            va='bottom')
    # 交点虚线
    xc = 0.484
    ax.plot([xc, xc], [0.533, -0.05], 'k--', lw=1.0, dashes=(4, 2))
    # T_c 标注
    ax.text(0.28, 0.235, r'$T_{\rm c}$', fontsize=10.5, ha='center',
            va='center')
    ax.text(0.615, 0.265, r'$T_{\rm c}$', fontsize=10.5, ha='center',
            va='center')
    ax.text(0.64, 0.615, u'费密液体', fontsize=9.5, ha='left', va='center',
            fontfamily='SimSun')
    # 轴标注
    ax.text(0.0, -0.055, r'$O$', fontsize=10, ha='right', va='top')
    ax.text(0.17, -0.055, r'$\delta_{\rm c}$', fontsize=10, ha='center',
            va='top')
    ax.text(0.30, -0.055, r'$L$', fontsize=10.5, ha='center', va='top')
    ax.text(0.56, -0.055, r'$H$', fontsize=10.5, ha='center', va='top')
    save(fig, '11-20')


# ================================================================ 图11.21
def fig_11_21():
    """过渡金属的 FM 相示意图：自旋上/下能带态密度（镜像）"""
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(4.7, 3.3))
    plain_axes(ax)
    ax.set_xlim(-0.09, 1.24)
    ax.set_ylim(-1.42, 1.42)
    # 纵轴：双向箭头
    ax.annotate('', xy=(0, 1.36), xytext=(0, -1.36),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=1.2,
                                shrinkA=0, shrinkB=0, mutation_scale=13))
    arrow_axis(ax, 0, 0, 1.20, 0, lw=1.2)
    ax.text(0.045, 1.28, r'$\rho_{\downarrow}(E)$', fontsize=10, ha='left',
            va='center')
    ax.text(0.045, -1.30, r'$\rho_{\uparrow}(E)$', fontsize=10, ha='left',
            va='center')
    ax.text(1.20, -0.13, r'$E$', fontsize=11, ha='center', va='center')

    # 双峰 d 带态密度形状
    g = lambda t, c, w: np.exp(-((t - c) / w) ** 2)
    tt = np.linspace(0, 1, 500)
    f0 = (0.66 * g(tt, 0.27, 0.155) + 1.0 * g(tt, 0.66, 0.185)) * \
        np.sin(np.pi * tt) ** 0.30
    f0 = f0 / f0.max()
    fint = PchipInterpolator(tt, f0)
    a0, W, d2, EF = 0.14, 0.80, 0.145, 0.815       # 上带起点、带宽、2Δ、E_F
    x1 = a0 + W * tt
    y1 = fint(tt)
    ax.plot(x1, y1, 'k-', lw=1.6)
    x2 = a0 + d2 + W * tt
    ax.plot(x2, -y1, 'k-', lw=1.6)
    # 阴影（填充至 E_F）
    m1 = x1 <= EF
    ax.add_patch(Polygon(np.vstack([np.column_stack([x1[m1], y1[m1]]),
                                    [[EF, 0]]]), closed=True, fc='white',
                         ec='none', hatch='///'))
    m2 = x2 <= EF
    ax.add_patch(Polygon(np.vstack([np.column_stack([x2[m2], -y1[m2]]),
                                    [[EF, 0]]]), closed=True, fc='white',
                         ec='none', hatch='///'))
    ax.plot(x1, y1, 'k-', lw=1.6)
    ax.plot(x2, -y1, 'k-', lw=1.6)
    ax.plot([EF, EF], [fint((EF - a0) / W), -fint((EF - a0 - d2) / W)],
            'k-', lw=1.3)
    ax.text(EF + 0.015, -0.52, r'$E_{\rm F}$', fontsize=10.5, ha='left',
            va='center')
    # 2Δ 标注
    for xd in (a0, a0 + d2):
        ax.plot([xd, xd], [0, -0.60], 'k--', lw=0.9, dashes=(4, 2))
    y2d = -0.47
    ax.annotate('', xy=(a0 - 0.005, y2d), xytext=(a0 - 0.10, y2d),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                mutation_scale=10))
    ax.annotate('', xy=(a0 + d2 + 0.005, y2d), xytext=(a0 + d2 + 0.10, y2d),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                mutation_scale=10))
    ax.text(a0 + d2 / 2, y2d, r'$2\Delta$', fontsize=10.5, ha='center',
            va='center', bbox=dict(fc='white', ec='none', pad=0.5))
    save(fig, '11-21')


# ================================================================ 图11.22
def fig_11_22():
    """铁磁相中↑、↓电子的费密球"""
    fig, ax = plt.subplots(figsize=(3.5, 3.35))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.42, 1.42)
    R, r = 1.0, 0.62
    ax.add_patch(Circle((0, 0), R, fc='white', ec='k', lw=1.5, hatch='.'))
    ax.add_patch(Circle((0, 0), r, fc='white', ec='k', lw=1.3,
                        hatch='...'))
    # 半径线
    ax.plot([0, R], [0, 0], 'k-', lw=1.0)
    ax.text(0.80, -0.125, r'$k_{\downarrow}$', fontsize=10.5, ha='center',
            va='center')
    a1 = np.deg2rad(112)
    ax.plot([0, r * np.cos(a1)], [0, r * np.sin(a1)], 'k-', lw=1.0)
    ax.text(0.14, 0.33, r'$k_{\uparrow}$', fontsize=10.5, ha='left',
            va='center')
    # k 与 k+q
    a2 = np.deg2rad(127)
    pk = (1.10 * np.cos(a2), 1.10 * np.sin(a2))
    pq = (0.575 * np.cos(np.deg2rad(122)), 0.575 * np.sin(np.deg2rad(122)))
    ax.plot([pk[0], pq[0]], [pk[1], pq[1]], 'k-', lw=0.9)
    ax.plot(*pk, marker='o', ms=6, mfc='k', mec='k')
    ax.add_patch(Circle(pq, 0.048, fc='white', ec='k', lw=1.1))
    ax.text(pk[0] - 0.10, pk[1] + 0.10, r'$\boldsymbol{k}$', fontsize=11,
            ha='center', va='bottom')
    ax.text(pq[0] + 0.10, pq[1] + 0.075, r'$\boldsymbol{k}+\boldsymbol{q}$',
            fontsize=11, ha='left', va='center')
    save(fig, '11-22')


# ================================================================ 图11.23
def fig_11_23():
    """确定磁序参量 ζ 的图示：R(ζ) 曲线与 (nU/2E_F)ζ 直线（照原书形态）"""
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(3.3, 3.15))
    plain_axes(ax)
    ax.set_xlim(-0.10, 1.40)
    ax.set_ylim(-0.115, 1.12)
    ax.plot([0, 0], [0, 1.06], 'k-', lw=1.1)
    ax.plot([1, 1], [0, 1.06], 'k-', lw=1.1)
    ax.plot([0, 1.0], [0, 0], 'k-', lw=1.1)
    ax.text(-0.05, 1.02, r'$R$', fontsize=11, ha='right', va='center')
    ax.text(0.5, -0.055, r'$\zeta$', fontsize=11, ha='center', va='top')
    ax.text(0.0, -0.055, r'$0$', fontsize=10, ha='center', va='top')
    ax.text(1.0, -0.055, r'$1$', fontsize=10, ha='center', va='top')
    # R(ζ) 曲线（原书形态：起始斜率略缓于直线，ζ≈0.57 处穿越直线后上翘）
    zc = 0.57
    alpha = 0.50
    f = PchipInterpolator([0.0, 0.25, 0.40, zc, 0.75, 0.90, 0.965, 1.0],
                          [0.0, 0.105, 0.185, alpha * zc, 0.45, 0.62,
                           0.73, 2 ** (-1.0 / 3.0)])
    z = np.linspace(0, 1, 400)
    ax.plot(z, f(z), 'k-', lw=1.7)
    ax.plot([0, 1], [0, alpha], 'k-', lw=1.4)
    ax.plot(0, 0, 'ko', ms=5.5)
    ax.plot(zc, alpha * zc, 'ko', ms=5.5)
    ax.plot(1, alpha, 'ko', ms=5.5)
    ax.text(1.02, 2 ** (-1.0 / 3.0), r'$2^{-1/3}$', fontsize=11, ha='left',
            va='center')
    ax.text(1.03, alpha, r'$(nU/2E_{\rm F})$', fontsize=10.5, ha='left',
            va='center')
    save(fig, '11-23')


# ================================================================ 图11.24
def fig_11_24():
    """方程式(11.11.72)的根：F(ω)=1 与各支的交点"""
    fig, ax = plt.subplots(figsize=(4.9, 3.1))
    plain_axes(ax)
    ax.set_xlim(-0.66, 1.50)
    ax.set_ylim(-0.62, 1.98)
    arrow_axis(ax, 0, -0.50, 0, 1.90)
    arrow_axis(ax, -0.10, 0, 1.44, 0, lw=1.0)
    ax.text(-0.06, 1.86, r'$F(\omega)$', fontsize=10.5, ha='right',
            va='center')
    ax.text(1.44, 0.055, r'$\omega$', fontsize=10.5, ha='center', va='center')
    ax.plot([-0.60, 1.38], [1, 1], 'k-', lw=1.0)
    poles = [0.32, 0.40, 0.465, 0.53, 0.715, 0.75]
    for p in poles:
        ax.plot([p, p], [-0.42, 1.78], 'k--', lw=0.9, dashes=(4, 2.4))
    # A 支（低频端，过 1 的圆圈点后发散于 ω_min）
    xa = np.array([-0.60, -0.38, -0.15, 0.05, 0.18, 0.25, 0.29, 0.307])
    ya = np.array([0.30, 0.375, 0.475, 0.60, 0.78, 1.0, 1.35, 1.78])
    from scipy.interpolate import PchipInterpolator
    fa = PchipInterpolator(xa, ya)
    xx = np.linspace(-0.60, 0.307, 300)
    ax.plot(xx, fa(xx), 'k-', lw=1.7)
    ax.plot(0.25, 1, 'o', ms=5.5, mfc='white', mec='k', mew=1.2)
    # 中间陡支（横穿 1）
    def steep(p0, p1, xc_cross):
        yy = np.linspace(-0.40, 1.78, 300)
        m = 0.5 * (p0 + p1)
        d = 0.5 * (p1 - p0) * 0.93
        xx = m + d * np.tanh((yy - 1.0) / 0.85)
        ax.plot(xx, yy, 'k-', lw=1.7)
        ax.plot(xc_cross, 1, 'o', ms=5.5, mfc='white', mec='k', mew=1.2)
    steep(poles[0], poles[1], 0.363)
    steep(poles[1], poles[2], 0.433)
    steep(poles[2], poles[3], 0.498)
    steep(poles[4], poles[5], 0.735)
    # ω>ω_max 末支：自下而上趋近 1
    xf = np.linspace(poles[5] + 0.035, 1.36, 300)
    yf = 1 - 1.45 * np.exp(-(xf - poles[5] - 0.035) / 0.115)
    ax.plot(xf, yf, 'k-', lw=1.7)
    ax.text(poles[0] - 0.03, -0.135, r'$\omega_{\min}$', fontsize=10.5,
            ha='right', va='center')
    ax.text(poles[5] + 0.075, -0.175, r'$\omega_{\max}$', fontsize=10.5,
            ha='left', va='center', bbox=dict(fc='white', ec='none', pad=0.8))
    save(fig, '11-24')


# ================================================================ 图11.25
def fig_11_25():
    """铁磁金属的元激发谱：自旋波与个别激发区"""
    fig, ax = plt.subplots(figsize=(4.4, 3.3))
    plain_axes(ax)
    ax.set_xlim(-0.10, 1.16)
    ax.set_ylim(-0.12, 1.98)
    arrow_axis(ax, 0, 0, 0, 1.92)
    arrow_axis(ax, 0, 0, 1.12, 0, lw=1.0)
    ax.text(-0.045, 1.87, r'$\omega$', fontsize=11, ha='right', va='center')
    ax.text(1.12, 0.05, r'$q$', fontsize=11, ha='center', va='center')
    # 个别激发区（Stoner 连续区）
    w0 = 0.72
    xu = np.linspace(0, 1.04, 200)
    yu = w0 + 1.02 * xu + 0.13 * xu ** 2
    xl = np.linspace(0, 0.78, 200)
    yl = w0 * np.sqrt(1 - (xl / 0.79) ** 2)
    poly = np.vstack([np.column_stack([xu, yu]),
                      [[1.04, 0.0]],
                      np.column_stack([xl[::-1], yl[::-1]])])
    ax.add_patch(Polygon(poly, closed=True, fc='white', ec='none',
                         hatch='///'))
    ax.plot(xu, yu, 'k-', lw=1.5)
    ax.plot(xl, yl, 'k-', lw=1.5)
    ax.text(0.60, 0.95, u'个别激发区', fontsize=9.5, ha='left', va='center',
            fontfamily='SimSun',
            bbox=dict(fc='white', ec='none', pad=1.0))
    # 自旋波支：实线转虚线，与个别激发区下界相接
    xsw = np.linspace(0, 0.45, 200)
    ax.plot(xsw, 1.30 * xsw ** 2, 'k-', lw=1.6)
    xsd = np.linspace(0.45, 0.60, 100)
    ax.plot(xsd, 1.30 * xsd ** 2, 'k--', lw=1.4, dashes=(5, 2.5))
    ax.text(0.20, 0.30, u'自旋波', fontsize=9.5, ha='center', va='center',
            fontfamily='SimSun')
    # 纵轴截距标注
    ax.text(-0.02, w0, r'$U\langle n_{\downarrow}-n_{\uparrow}\rangle$',
            fontsize=10, ha='right', va='center')
    save(fig, '11-25')


if __name__ == '__main__':
    import sys
    names = ['11-%d' % i for i in range(1, 26)]
    only = sys.argv[1:] or names
    for n in only:
        globals()['fig_' + n.replace('-', '_')]()
        print(f'fig{n} done')
