# -*- coding: utf-8 -*-
"""
李正中《固体理论》(第2版) 中文重排本 插图重绘 第三批：
第六章 图6.13-6.23（11幅）+ 第七章 图7.1-7.17（17幅），共28幅。
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p-212/216/224/235/238/242/244/245/246/247/
252/254/255/259/260/262/265/269/270/282/291/293/294/297/300/302/303）。
注：图6.16 实际在 p-224；图6.18 在 p-238；图7.4 在 p-259；图7.16 在 p-302。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Rectangle, Circle, Ellipse, Polygon

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
    """坐标轴上的短刻度"""
    ax.plot([x, x + dx], [y, y + dy], 'k-', lw=lw)


def dbarr(ax, x0, x1, y, ms=11, lw=1.0):
    """水平双向箭头"""
    ax.annotate('', xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def vtext(ax, x, y, s, **kw):
    """竖排中文：逐字换行"""
    ax.text(x, y, '\n'.join(s), ha='center', va='center',
            linespacing=1.02, **kw)


def dclover(ax, cx, cy, s, rot=0.0, plus='+-', fs=7):
    """d_{x^2-y^2} 四瓣符号：水平瓣 +、竖直瓣 -；rot 为旋转角(度)"""
    th = np.deg2rad(rot)
    ca, sa = np.cos(th), np.sin(th)

    def R(px, py):
        return (cx + px * ca - py * sa, cy + px * sa + py * ca)

    for ang, sg in [(0, plus[0]), (180, plus[0]), (90, plus[1]), (270, plus[1])]:
        a = np.deg2rad(ang)
        px, py = 0.60 * s * np.cos(a), 0.60 * s * np.sin(a)
        ex, ey = R(px, py)
        w, h = (1.05 * s, 0.42 * s) if ang in (0, 180) else (0.42 * s, 1.05 * s)
        e = Ellipse((ex, ey), w, h, angle=rot, fill=False, lw=0.9, ec='k')
        ax.add_patch(e)
        tx, ty = R(0.95 * s * np.cos(a), 0.95 * s * np.sin(a))
        ax.text(tx, ty, sg, fontsize=fs, ha='center', va='center')


# ================================================================ 图6.13
def fig_6_13():
    fig, ax = plt.subplots(figsize=(3.0, 2.6))
    plain_axes(ax)
    ax.set_xlim(-0.42, 3.72)
    ax.set_ylim(-0.72, 3.95)

    arrow_axis(ax, 0, 0, 0, 3.75)
    arrow_axis(ax, 0, 0, 3.6, 0)
    for v in (1, 2, 3):
        tick(ax, 0, v, -0.07, 0)
        tick(ax, v, 0, 0, -0.07)
        ax.text(-0.12, v, str(v), fontsize=8.5, ha='right', va='center')
        ax.text(v, -0.14, str(v), fontsize=8.5, ha='center', va='top')
    ax.text(0, -0.2, r'$O$', fontsize=10, ha='right', va='top')
    ax.text(-0.06, 3.55, r'$G_{\rm SN}/G_{\rm NN}$', fontsize=10,
            ha='right', va='bottom')
    ax.text(3.6, -0.16, r'$eV/\Delta$', fontsize=10, ha='center', va='top')

    ax.plot([0, 3.3], [1, 1], 'k-', lw=1.1)                      # G=1 参考线
    # T=0K：x=1 处竖直发散 + 衰减曲线
    ax.plot([1, 1], [1.0, 3.3], 'k-', lw=1.4)
    xx = np.linspace(1.01, 3.3, 300)
    ax.plot(xx, 1 + 0.245 / np.sqrt(xx - 1.0), 'k-', lw=1.4)
    ax.text(1.55, 2.55, r'$T$=0 K', fontsize=9.5, ha='left', va='center')
    # T>0K：虚线，峰值约2
    xa = np.linspace(0.50, 1.0, 150)
    ax.plot(xa, 2.0 * np.exp(-0.5 * ((xa - 1.0) / 0.145) ** 2), 'k--', lw=1.0,
            dashes=(4, 2))
    xb = np.linspace(1.0, 3.3, 150)
    ax.plot(xb, 1 + 1.0 * np.exp(-(xb - 1.0) / 0.30), 'k--', lw=1.0, dashes=(4, 2))
    ax.text(0.42, 0.62, r'$T>0$ K', fontsize=9.5, ha='left', va='center')
    save(fig, '6-13')


# ================================================================ 图6.14
def fig_6_14():
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(2.9, 2.75))
    plain_axes(ax)
    ax.set_xlim(-0.35, 3.3)
    ax.set_ylim(-0.35, 2.35)

    arrow_axis(ax, 0, 0, 0, 2.2)
    arrow_axis(ax, 0, 0, 3.15, 0)
    ax.text(0.1, 2.2, r'$I$', fontsize=10, ha='left', va='center')
    for v in (1, 2):
        tick(ax, v, 0, 0, -0.06)
        ax.text(v, -0.12, str(v), fontsize=8.5, ha='center', va='top')
    ax.text(0, -0.16, r'$O$', fontsize=10, ha='right', va='top')
    ax.text(3.1, -0.14, r'$eV/\Delta$', fontsize=10, ha='center', va='top')

    k = 0.69
    ax.plot([0, 2.65], [0, k * 2.65], 'k-', lw=1.4)              # I_NN
    ax.text(1.15, k * 1.35 + 0.16, r'$I_{\rm NN}$', fontsize=10,
            ha='left', va='bottom')
    xx = np.linspace(1.0, 2.62, 300)                             # I_SN (T=0)
    ax.plot(xx, k * np.sqrt(xx ** 2 - 1), 'k-', lw=1.4)
    ax.text(1.74, 1.0, r'$I_{\rm SN}$', fontsize=10, ha='left', va='center')
    # T>0K 虚线
    pts = [(0, 0), (0.5, 0.02), (0.75, 0.045), (0.9, 0.085), (0.97, 0.14),
           (1.0, 0.17), (1.05, 0.25), (1.09, 0.315)]
    f = PchipInterpolator([p[0] for p in pts], [p[1] for p in pts])
    xd = np.linspace(0, 1.09, 150)
    ax.plot(xd, f(xd), 'k--', lw=1.0, dashes=(4, 2))
    ax.text(0.36, 0.14, r'$T>0$K', fontsize=9.5, ha='left', va='center')
    ax.text(1.12, 0.115, r'$T$=0 K', fontsize=9.5, ha='left', va='center')
    save(fig, '6-14')


# ================================================================ 图6.15
def fig_6_15():
    fig, ax = plt.subplots(figsize=(2.35, 2.5))
    plain_axes(ax)
    ax.set_xlim(-0.5, 4.1)
    ax.set_ylim(-0.24, 1.42)

    arrow_axis(ax, 0, 0, 0, 1.3)
    arrow_axis(ax, 0, 0, 3.95, 0)
    tick(ax, 0, 0.5, -0.06, 0)
    tick(ax, 0, 1.0, -0.06, 0)
    ax.text(-0.1, 0.5, '0.5', fontsize=8.5, ha='right', va='center')
    ax.text(-0.1, 1.0, '1.0', fontsize=8.5, ha='right', va='center')
    for v in (1.0, 2.0, 3.0):
        tick(ax, v, 0, 0, -0.06)
        ax.text(v, -0.1, f'{v:.1f}', fontsize=8.5, ha='center', va='top')
    ax.text(0, -0.15, r'$O$', fontsize=10, ha='right', va='top')
    ax.text(-0.03, 1.28, r'$K(q)/K(0)$', fontsize=9.5, ha='left', va='bottom')
    ax.text(3.95, -0.12, r'$q\xi_0$', fontsize=10, ha='center', va='top')

    x = np.linspace(1e-6, 3.35, 400)
    y = 1.5 * ((x ** 2 + 1) * np.arctan(x) - x) / x ** 3
    ax.plot(x, y, 'k-', lw=1.5)
    save(fig, '6-15')


# ================================================================ 图6.16
def fig_6_16():
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(3.0, 2.75))
    plain_axes(ax)
    ax.set_xlim(-0.35, 4.85)
    ax.set_ylim(-0.62, 1.42)

    arrow_axis(ax, 0, 0, 0, 1.28)
    arrow_axis(ax, 0, 0, 4.7, 0)
    for v in np.arange(0.2, 1.01, 0.2):
        tick(ax, 0, v, -0.06, 0)
        ax.text(-0.1, v, f'{v:.1f}', fontsize=8, ha='right', va='center')
    ax.text(-0.1, 0, '0', fontsize=8, ha='right', va='center')
    for v in (1.0, 2.0, 3.0, 4.0):
        tick(ax, v, 0, 0, -0.06)
        ax.text(v, -0.1, f'{v:.1f}', fontsize=8, ha='center', va='top')
    ax.text(4.35, 0.14, r'$R/\xi_0$', fontsize=10, ha='left', va='center')

    pts = [(0, 1), (0.15, 0.72), (0.3, 0.53), (0.5, 0.43), (0.8, 0.365),
           (1.2, 0.295), (1.6, 0.235), (2.0, 0.17), (2.5, 0.115),
           (3.0, 0.082), (3.5, 0.065), (4.0, 0.055)]
    f = PchipInterpolator([p[0] for p in pts], [p[1] for p in pts])
    xx = np.linspace(0, 4.0, 300)
    ax.plot(xx, f(xx), 'k-', lw=1.5)
    ax.plot(xx, np.exp(-xx), 'k--', lw=1.0, dashes=(5, 2.5))
    # 图例
    y0 = -0.52
    ax.plot([0.25, 0.75], [y0, y0], 'k-', lw=1.3)
    ax.text(0.88, y0, r'BCS $J(R)$', fontsize=9.5, ha='left', va='center')
    ax.plot([2.5, 3.0], [y0, y0], 'k--', lw=1.0, dashes=(5, 2.5))
    ax.text(3.13, y0, u'皮帕 e$^{-R/\\xi_0}$', fontsize=9.5, ha='left',
            va='center', fontfamily='SimSun')
    save(fig, '6-16')


# ================================================================ 图6.17
def fig_6_17():
    fig, ax = plt.subplots(figsize=(4.9, 2.4))
    plain_axes(ax)
    ax.set_xlim(-0.98, 1.78)
    ax.set_ylim(-0.18, 1.22)
    ax.set_aspect('auto')

    arrow_axis(ax, -0.95, 0, 1.72, 0, lw=1.0)
    ax.text(1.66, -0.12, r'$z$', fontsize=10, ha='center', va='center')
    Hc = 0.88
    lam, xi = 0.42, 1.0
    # 竖直线
    ax.plot([0, 0], [0, 1.08], 'k-', lw=1.0)
    ax.plot([lam, lam], [0, 1.02], 'k-', lw=1.0)
    ax.plot([xi, xi], [0, 1.08], 'k-', lw=1.0)
    # Hc 虚线 + B 衰减曲线
    ax.plot([-0.95, 0], [Hc, Hc], 'k--', lw=1.1, dashes=(4, 2))
    zb = np.linspace(0, 0.62, 200)
    ax.plot(zb, Hc * np.exp(-zb / 0.19), 'k--', lw=1.1, dashes=(4, 2))
    ax.text(0.13, 0.75, r'$B$', fontsize=10, ha='left', va='center')
    # |psi| 曲线
    zp = np.linspace(0, 1.38, 300)
    ps = 0.5 * (1 + np.tanh((zp - 0.62) / 0.155))
    ax.plot(zp, Hc * ps, 'k-', lw=1.7)
    ax.text(1.13, Hc + 0.06, r'$\psi_0$', fontsize=10, ha='left', va='bottom')
    # 双向箭头与标注
    dbarr(ax, lam, xi, 1.0, ms=11)
    ax.text((lam + xi) / 2, 1.05, r'$(\xi-\lambda)$', fontsize=9.5,
            ha='center', va='bottom')
    dbarr(ax, 0, xi, 0.62, ms=11)
    ax.text(0.30, 0.67, r'$\xi$', fontsize=10, ha='center', va='bottom')
    ax.text(0.60, 0.67, r'$|\psi|$', fontsize=10, ha='center', va='bottom')
    dbarr(ax, 0, lam, 0.22, ms=10)
    ax.text(lam / 2, 0.255, r'$\lambda$', fontsize=10, ha='center', va='bottom')
    ax.text(lam, -0.055, r'$\lambda$', fontsize=9.5, ha='center', va='top')
    ax.text(xi, -0.055, r'$\xi$', fontsize=9.5, ha='center', va='top')
    ax.text(-0.52, 0.48, 'N', fontsize=10, ha='center', va='center')
    ax.text(1.22, 0.48, 'S', fontsize=10, ha='center', va='center')
    save(fig, '6-17')


# ================================================================ 图6.18
def fig_6_18():
    fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.75))
    for ax in axs:
        plain_axes(ax)
        ax.set_aspect('equal')
        ax.set_xlim(-1.75, 1.75)
        ax.set_ylim(-1.45, 1.45)

    def outer_ticks(ax, r=1.0, n=36, ln=0.09):
        for a in np.linspace(0, 2 * np.pi, n, endpoint=False):
            x0, y0 = r * np.cos(a), r * np.sin(a)
            ax.plot([x0, x0 * (r + ln) / r], [y0, y0 * (r + ln) / r],
                    'k-', lw=0.8)

    def circ_arrow(ax, r, ang, lw=1.0):
        """虚线圆 + 逆时针箭头"""
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(r * np.cos(th), r * np.sin(th), 'k--', lw=lw, dashes=(4, 2.2))
        a = np.deg2rad(ang)
        p = np.array([r * np.cos(a), r * np.sin(a)])
        t = np.array([-np.sin(a), np.cos(a)])          # 逆时针切向
        p2 = p - 0.13 * t
        ax.annotate('', xy=p, xytext=p2,
                    arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                    shrinkA=0, shrinkB=0, mutation_scale=12))

    # (a) 单连通
    ax = axs[0]
    ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.5, ec='k'))
    outer_ticks(ax)
    circ_arrow(ax, 0.72, 128)
    ax.text(0.62, 0.72, r'$C$', fontsize=10, ha='left', va='bottom')
    ax.add_patch(Circle((-1.32, 0.18), 0.045, fill=False, lw=0.9, ec='k'))
    ax.add_patch(Circle((-1.32, 0.18), 0.012, fc='k', ec='k'))
    ax.text(-1.48, 0.18, r'$H$', fontsize=10, ha='right', va='center')
    ax.text(0.5, -1.32, u'(a) 单连通超导体', fontsize=9.5, ha='center', va='top')

    # (b) 复连通
    ax = axs[1]
    ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.5, ec='k'))
    outer_ticks(ax)
    ax.add_patch(Circle((0, 0), 0.30, fill=False, lw=1.4, ec='k'))
    for a in np.linspace(0, 2 * np.pi, 18, endpoint=False):
        x0, y0 = 0.30 * np.cos(a), 0.30 * np.sin(a)
        ax.plot([x0, x0 * 1.22], [y0, y0 * 1.22], 'k-', lw=0.7)
    ax.add_patch(Circle((0, 0), 0.055, fill=False, lw=0.9, ec='k'))
    ax.add_patch(Circle((0, 0), 0.016, fc='k', ec='k'))
    ax.text(0.10, 0.0, r'$H$', fontsize=9, ha='left', va='center')
    circ_arrow(ax, 0.62, 108)
    ax.text(-0.60, -0.52, r'$C$', fontsize=10, ha='right', va='top')
    ax.text(0.5, -1.32, u'(b) 复连通超导体', fontsize=9.5, ha='center', va='top')

    # (c) II 类
    ax = axs[2]
    ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.5, ec='k'))
    for px, py in [(0, 0), (0.52, 0.52), (0.60, 0.0),
                   (0.52, -0.52), (-0.52, 0.52), (-0.60, 0.0),
                   (-0.52, -0.52)]:
        ax.add_patch(Circle((px, py), 0.155, fc='white', ec='k', lw=1.0))
        ax.text(px, py, 'N', fontsize=8, ha='center', va='center')
    circ_arrow(ax, 0.33, 95)
    ax.text(0.47, 0.40, r'$C$', fontsize=10, ha='left', va='center')
    ax.text(0.12, -0.80, 'S', fontsize=10, ha='center', va='center')
    ax.text(0.5, -1.32, u'(c) Ⅱ类超导体', fontsize=9.5, ha='center', va='top')
    save(fig, '6-18')


# ================================================================ 图6.19
def fig_6_19():
    fig, ax = plt.subplots(figsize=(3.4, 2.3))
    plain_axes(ax)
    ax.set_xlim(-3.95, 4.35)
    ax.set_ylim(-0.32, 1.42)

    arrow_axis(ax, 0, 0, 0, 1.3)
    arrow_axis(ax, -3.75, 0, 4.2, 0, lw=1.0)
    ax.text(0.12, 1.26, r'$I_{\max}$', fontsize=10, ha='left', va='center')
    for v in range(-3, 4):
        tick(ax, v, 0, 0, -0.06)
        ax.text(v, -0.1, f'{v}', fontsize=8, ha='center', va='top')
    ax.text(4.1, -0.2, r'$\Phi$', fontsize=9, ha='center', va='center')
    ax.text(4.1, -0.38, r'$\Phi_0$', fontsize=9, ha='center', va='center')

    x = np.linspace(-3.5, 3.5, 2000)
    y = np.abs(np.sin(np.pi * x) / (np.pi * x))
    ax.plot(x, y, 'k-', lw=1.4)
    save(fig, '6-19')


# ================================================================ 图6.20
def fig_6_20():
    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    plain_axes(ax)
    ax.set_xlim(-0.18, 3.15)
    ax.set_ylim(-0.22, 1.78)

    arrow_axis(ax, 0, 0, 0, 1.68)
    arrow_axis(ax, 0, 0, 3.05, 0, lw=1.0)
    ax.text(0.09, 1.64, r'$I$', fontsize=10, ha='left', va='center')
    ax.text(2.97, -0.1, r'$eV$', fontsize=10, ha='center', va='top')
    D = 0.95
    for lab, v in [(r'$\Delta$', D), (r'$2\Delta$', 2 * D)]:
        tick(ax, v, 0, 0, -0.06)
        ax.text(v, -0.11, lab, fontsize=9.5, ha='center', va='top')

    ax.plot([0, 2.38], [0, 1.52], 'k--', lw=1.1, dashes=(5, 2.5))   # 正常态直线
    # 准粒子隧穿电流（2Δ处陡升）
    ax.plot([2 * D, 2 * D], [0, 0.268], 'k-', lw=1.7)
    xq = np.linspace(2 * D + 0.001, 2.48, 200)
    yq = 1.53 * np.sqrt(1 - (2 * D / xq) ** 2)
    ax.plot(xq, yq, 'k-', lw=1.7)
    # 夏皮洛台阶（虚线阶梯）
    sx, sy = 0.03, 0.0
    steps = [(0.22, 0.075), (0.44, 0.145), (0.68, 0.215), (0.92, 0.275),
             (1.16, 0.33), (1.42, 0.375), (1.66, 0.415), (1.90, 0.45)]
    ax.plot([0.02, steps[0][0]], [sy, sy], 'k--', lw=1.1, dashes=(3.5, 2))
    for x1, y1 in steps:
        ax.plot([sx, x1], [sy, sy], 'k--', lw=1.1, dashes=(3.5, 2))
        ax.plot([x1, x1], [sy, y1], 'k--', lw=1.1, dashes=(3.5, 2))
        sx, sy = x1, y1
    # V=0 约瑟夫森电流（I 轴上的竖直双箭头段）
    ax.annotate('', xy=(0, 0.50), xytext=(0, 0.32),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=1.4,
                                shrinkA=0, shrinkB=0, mutation_scale=8))
    # 标注
    ax.text(0.44, 0.72, u'正常态隧穿\n约瑟夫森电流', fontsize=8.5,
            ha='left', va='center', linespacing=1.4)
    ax.annotate('', xy=(0.015, 0.42), xytext=(0.40, 0.645),
                arrowprops=dict(arrowstyle='->', color='k', lw=0.9,
                                connectionstyle='arc3,rad=-0.25'))
    ax.text(1.62, 0.86, u'准粒子隧穿电流', fontsize=8.5, ha='left', va='center')
    ax.annotate('', xy=(1.915, 0.52), xytext=(1.60, 0.845),
                arrowprops=dict(arrowstyle='->', color='k', lw=0.9))
    ax.text(1.30, 0.16, u'夏皮洛台阶', fontsize=8.5, ha='left', va='center')
    ax.annotate('', xy=(1.27, 0.35), xytext=(1.28, 0.21),
                arrowprops=dict(arrowstyle='->', color='k', lw=0.9))
    save(fig, '6-20')


# ================================================================ 图6.21
def fig_6_21():
    fig, ax = plt.subplots(figsize=(4.15, 4.3))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-1.5, 1.5)
    R, ri = 1.0, 0.70
    # 环体（灰色）
    th = np.linspace(0, 2 * np.pi, 400)
    ax.add_patch(Polygon(np.column_stack([R * np.cos(th), R * np.sin(th)]),
                         closed=True, fc='0.72', ec='none'))
    ax.add_patch(Circle((0, 0), ri, fc='white', ec='none'))
    ax.add_patch(Circle((0, 0), R, fill=False, ec='k', lw=1.4))
    ax.add_patch(Circle((0, 0), ri, fill=False, ec='k', lw=1.4))
    # 左右引线
    for x0 in (-1.95, 0.95):
        ax.add_patch(Rectangle((x0, -0.15), 1.0, 0.30, fc='0.72', ec='k', lw=1.1))
    # 上下结（白色缺口 + 斜线框）
    for yc in (1, -1):
        ax.add_patch(Rectangle((-0.10, min(0.64 * yc, 1.02 * yc)),
                               0.20, abs(1.02 * yc - 0.64 * yc),
                               fc='white', ec='none', zorder=3))
        ax.add_patch(Rectangle((-0.05, min(0.64 * yc, 1.0 * yc)),
                               0.10, abs(1.0 * yc - 0.64 * yc),
                               fc='white', ec='k', lw=1.0, hatch='///', zorder=4))
        if yc > 0:
            ax.plot([-0.10, -0.10], [0.64, 1.0], 'k-', lw=1.2, zorder=5)
            ax.plot([0.10, 0.10], [0.64, 1.0], 'k-', lw=1.2, zorder=5)
        else:
            ax.plot([-0.10, -0.10], [-0.64, -1.0], 'k-', lw=1.2, zorder=5)
            ax.plot([0.10, 0.10], [-0.64, -1.0], 'k-', lw=1.2, zorder=5)
    # 字母 a b c d
    ax.text(-0.24, 0.84, r'$b$', fontsize=9.5, ha='right', va='center', zorder=6)
    ax.text(0.24, 0.84, r'$a$', fontsize=9.5, ha='left', va='center', zorder=6)
    ax.text(-0.24, -0.84, r'$d$', fontsize=9.5, ha='right', va='center', zorder=6)
    ax.text(0.24, -0.84, r'$c$', fontsize=9.5, ha='left', va='center', zorder=6)
    # 中心磁通符号 Φ
    ax.add_patch(Circle((0, 0.02), 0.085, fill=False, lw=0.9, ec='k'))
    for a in (245, 270, 295):
        r0 = np.deg2rad(a)
        ax.plot([0.085 * np.cos(r0), 0.19 * np.cos(r0)],
                [0.02 + 0.085 * np.sin(r0), 0.02 + 0.19 * np.sin(r0)],
                'k-', lw=0.9)
    ax.text(0.27, 0.02, r'$\Phi$', fontsize=11, ha='left', va='center')
    # 结1 / 结2 箭头
    ax.annotate('', xy=(0, 0.56), xytext=(0, 0.26),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.1,
                                mutation_scale=11))
    ax.text(0.0, 0.40, u'结1', fontsize=9, ha='center', va='center',
            bbox=dict(fc='white', ec='none', pad=0.5))
    ax.annotate('', xy=(0, -0.56), xytext=(0, -0.26),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.1,
                                mutation_scale=11))
    ax.text(0.0, -0.40, u'结2', fontsize=9, ha='center', va='center',
            bbox=dict(fc='white', ec='none', pad=0.5))
    save(fig, '6-21')


# ================================================================ 图6.22
def fig_6_22():
    fig, ax = plt.subplots(figsize=(3.4, 2.0))
    plain_axes(ax)
    ax.set_xlim(-3.95, 4.35)
    ax.set_ylim(-0.38, 1.5)

    arrow_axis(ax, 0, 0, 0, 1.38)
    arrow_axis(ax, -3.75, 0, 4.2, 0, lw=1.0)
    ax.text(0.12, 1.34, r'$I_{\max}$', fontsize=10, ha='left', va='center')
    for v in range(-3, 4):
        tick(ax, v, 0, 0, -0.06)
        ax.text(v, -0.1, f'{v}', fontsize=8, ha='center', va='top')
    ax.text(4.1, -0.2, r'$\Phi$', fontsize=9, ha='center', va='center')
    ax.text(4.1, -0.38, r'$\Phi_0$', fontsize=9, ha='center', va='center')

    x = np.linspace(-3.5, 3.5, 2000)
    ax.plot(x, np.abs(np.cos(np.pi * x)), 'k-', lw=1.4)
    save(fig, '6-22')


# ================================================================ 图6.23
def fig_6_23():
    fig, ax = plt.subplots(figsize=(4.6, 2.15))
    plain_axes(ax)
    ax.set_xlim(-600, 660)
    ax.set_ylim(-0.16, 1.3)

    arrow_axis(ax, 0, 0, 0, 1.2)
    arrow_axis(ax, -570, 0, 640, 0, lw=1.0)
    ax.text(0.16, 1.16, u'最大超电流', fontsize=9, ha='left', va='center')
    for v in range(-400, 401, 200):
        tick(ax, v, 0, 0, -0.035)
        ax.text(v, -0.055, f'{v}', fontsize=8.5, ha='center', va='top')
    ax.text(620, -0.075, r'$B$/mGs', fontsize=9.5, ha='center', va='top')

    B = np.linspace(-560, 560, 9000)
    env = np.abs(np.sinc(B / 240.0))
    y = np.abs(np.cos(np.pi * B / 15.8)) * env
    ax.plot(B, y, 'k-', lw=0.65)
    save(fig, '6-23')


# ================================================================ 图7.1
def fig_7_1():
    fig, ax = plt.subplots(figsize=(4.7, 4.6))
    plain_axes(ax)
    ax.set_xlim(1903.5, 2006)
    ax.set_ylim(-9, 143)

    arrow_axis(ax, 1906, 0, 1906, 138)
    arrow_axis(ax, 1906, 0, 2003, 0, lw=1.0)
    ax.text(1902.5, 137, r'$T_{\rm c}$/K', fontsize=10, ha='right', va='top')
    for v in range(0, 131, 10):
        tick(ax, 1906, v, -1.6, 0)
        if v % 10 == 0:
            ax.text(1903.5, v, f'{v}', fontsize=8, ha='right', va='center')
    for yr in (1910, 1930, 1950, 1970, 1990):
        tick(ax, yr, 0, 0, -2.2)
        ax.text(yr, -3.2, str(yr), fontsize=8.5, ha='center', va='top')
    ax.text(1986.2, 2.2, '1986', fontsize=8.5, ha='center', va='bottom')

    # 阶梯（常规超导体）
    steps = [(1911, 4.2, 'f', 'Hg', (-2.5, -0.4)),
             (1913, 7.3, 'f', 'Pb', (-3.5, 2.6)),
             (1930, 8.3, 'f', 'Nb', (-3.5, 1.4)),
             (1934, 10.2, 'f', 'NbO', (-4.5, 2.2)),
             (1941, 14.3, 'f', 'NbN', (-5.5, 1.6)),
             (1954, 17.4, 'o', 'Nb$_3$Sn', (-9.5, 2.2)),
             (1966, 20.2, 'f', 'Nb-Al-Ge', (-11.5, 2.2)),
             (1973, 23.2, 'f', 'Nb$_3$Ge', (-9.5, 3.0))]
    px, py = 1911, 0
    for yr, tc, mk, lab, (dx, dy) in steps:
        ax.plot([px, px], [py, tc], 'k-', lw=1.5)
        px, py = yr, tc
        ax.plot([px, px], [py, tc], 'k-', lw=1.5)
        px, py = yr, tc
        if mk == 'f':
            ax.plot(px, py, 'ko', ms=3.6)
        else:
            ax.plot(px, py, 'o', mfc='white', mec='k', ms=3.6)
        ax.text(px + dx, py + dy, lab, fontsize=8.5, ha='left', va='center')
    ax.plot([1973, 1986.45], [23.2, 23.2], 'k-', lw=1.5)

    # 铜氧化物竖线 + 各点
    X = 1986.5
    ax.plot([X, X], [23.2, 127], 'k-', lw=1.6)
    pts = [(34.5, '1986.4'), (39, '1986.12'), (45, '1986.12'), (50, '1987.1')]
    for tc, lab in pts:
        ax.plot(X, tc, 'o', mfc='white', mec='k', ms=4)
        ax.text(X + 2.5, tc, lab, fontsize=8.5, ha='left', va='center')
    # La-Sr-Cu-O 花括号
    bx = 1984.6
    ax.annotate('', xy=(bx, 33.5), xytext=(bx, 51.5),
                arrowprops=dict(arrowstyle='-', color='k', lw=0.8,
                                connectionstyle='bar,fraction=-0.18'))
    ax.text(1982.8, 42.5, 'La-Sr-Cu-O', fontsize=8.5, ha='right', va='center')
    for tc, lab in [(92, ('Y-Ba-Cu-O', '1987.2')),
                    (110, ('Bi-Sr-Ca-Cu-O', '1988.1')),
                    (123.5, ('Tl-Ba-Ca-Cu-O', '1988'))]:
        ax.plot(X, tc, 'o', mfc='white', mec='k', ms=4)
        ax.text(X - 2.5, tc, lab[0], fontsize=8.5, ha='right', va='center')
        ax.text(X + 2.5, tc, lab[1], fontsize=8.5, ha='left', va='center')
    ax.annotate('', xy=(X, 136), xytext=(X, 128.5),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                linestyle='dashed', mutation_scale=11))
    # La-Ba-Cu-O 首次发现点
    X2 = 1986.2
    ax.annotate('', xy=(X2, 20.5), xytext=(X2, 8),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                linestyle='dashed', mutation_scale=11))
    ax.plot(X2, 11.5, 'o', mfc='white', mec='k', ms=4)
    ax.text(X2 + 2.0, 17.2, 'La-Ba-Cu-O', fontsize=8.5, ha='left', va='center')
    ax.text(X2 + 2.0, 11.5, '1986.1', fontsize=8.5, ha='left', va='center')
    # 液体温度线
    for tc, lab in [(77.4, u'液 N$_2$'), (27.1, u'液 Ne'), (20.4, u'液 H$_2$')]:
        ax.plot([1906, 1918.5], [tc, tc], 'k-', lw=1.2)
        ax.text(1908, tc + 2.2, lab, fontsize=8.5, ha='left', va='bottom',
                fontfamily='SimSun')
    save(fig, '7-1')


# -------------------------------------------- 三维结构图公用（图7.2 / 7.3）
CAX, SAX = 0.42, 0.26          # b 轴投影方向 (dx, dy)


def P3(u, v, w):
    return (u + CAX * v, w + SAX * v)


def line3(ax, p1, p2, dashed=False, lw=0.9):
    a, b = P3(*p1), P3(*p2)
    if dashed:
        ax.plot([a[0], b[0]], [a[1], b[1]], 'k--', lw=lw, dashes=(3, 1.8))
    else:
        ax.plot([a[0], b[0]], [a[1], b[1]], 'k-', lw=lw)


def atom(ax, p, r, style, zorder=6):
    """style: w=白 k=黑 h=斜线 l=横线 x=交叉线"""
    xy = P3(*p)
    hatch = {'w': None, 'k': None, 'h': '////', 'l': '---', 'x': 'xx'}[style]
    fc = {'w': 'white', 'k': 'black'}.get(style, 'white')
    ax.add_patch(Circle(xy, r, fc=fc, ec='k', lw=0.8, hatch=hatch,
                        zorder=zorder))


def cell_frame(ax, a, b, c, x0=0, z0=0):
    """晶胞框：前面实线，后面虚线；返回8个角点"""
    A = (x0, 0, z0); B = (x0 + a, 0, z0); C = (x0 + a, b, z0); D = (x0, b, z0)
    A2 = (x0, 0, z0 + c); B2 = (x0 + a, 0, z0 + c)
    C2 = (x0 + a, b, z0 + c); D2 = (x0, b, z0 + c)
    line3(ax, A, B, True); line3(ax, B, C, True)          # 底面后缘
    line3(ax, C, D, True); line3(ax, D, A)
    line3(ax, A2, B2); line3(ax, B2, C2, True)            # 顶面
    line3(ax, C2, D2, True); line3(ax, D2, A2)
    line3(ax, A, A2); line3(ax, B, B2)                    # 竖棱
    line3(ax, C, C2, True); line3(ax, D, D2, True)
    return A, B, C, D, A2, B2, C2, D2


def plate_atoms(ax, z, x0, a, b, kind):
    """一层原子面。kind: Bi(角,斜线) Cu(角,黑) Sr(心,横线) Ca(心,交叉) O边中点"""
    mids = [(x0 + a / 2, 0, z), (x0 + a, b / 2, z),
            (x0 + a / 2, b, z), (x0, b / 2, z)]
    corners = [(x0, 0, z), (x0 + a, 0, z), (x0 + a, b, z), (x0, b, z)]
    for p in corners + mids:
        atom(ax, p, 0.048, 'w', zorder=5)
    if kind in ('Bi', 'Cu'):
        st = 'h' if kind == 'Bi' else 'k'
        for p in corners:
            atom(ax, p, 0.072, st, zorder=7)
    else:
        st = 'l' if kind == 'Sr' else 'x'
        atom(ax, (x0 + a / 2, b / 2, z), 0.075, st, zorder=7)


def triad(ax, px, py, s=0.55):
    """c/b/a 坐标小三角"""
    arrow_axis(ax, px, py, px, py + s, lw=0.9)
    arrow_axis(ax, px, py, px + 0.62 * s, py + 0.5 * s, lw=0.9)
    arrow_axis(ax, px, py, px + 0.85 * s, py - 0.28 * s, lw=0.9)
    ax.text(px + 0.06, py + s + 0.1, r'$c$', fontsize=9, ha='left', va='center')
    ax.text(px + 0.62 * s + 0.08, py + 0.5 * s + 0.1, r'$b$', fontsize=9,
            ha='left', va='center')
    ax.text(px + 0.9 * s, py - 0.42 * s, r'$a$', fontsize=9, ha='left',
            va='center')


# ================================================================ 图7.2
def fig_7_2():
    fig, axs = plt.subplots(1, 2, figsize=(8.0, 4.6))
    for ax in axs:
        plain_axes(ax)
        ax.set_aspect('equal', adjustable='datalim')

    # -------- (a) La-214 (K2NiF4 型)
    ax = axs[0]
    a, b, c = 1.0, 0.8, 3.0
    cell_frame(ax, a, b, c)
    for z in (0.0, c):
        for p, r in [((0, 0, z), 0.075), ((a, 0, z), 0.075),
                     ((a, b, z), 0.075), ((0, b, z), 0.075)]:
            atom(ax, p, r, 'h', zorder=7)
        for p in [(a / 2, 0, z), (a, b / 2, z), (a / 2, b, z), (0, b / 2, z)]:
            atom(ax, p, 0.05, 'w', zorder=6)
    # (La,Sr) 黑点
    for p in [(0.5, 0.06, 2.52), (0.05, 0.30, 1.92), (0.62, 0.04, 1.88),
              (0.05, 0.30, 1.08), (0.62, 0.04, 1.04), (0.5, 0.06, 0.48)]:
        atom(ax, p, 0.078, 'k')
    # 中心 CuO6 八面体
    ccu = (0.5, 0.4, 1.5)
    verts = [(0, 0.4, 1.5), (1, 0.4, 1.5), (0.5, 0, 1.5), (0.5, 0.8, 1.5),
             (0.5, 0.4, 2.16), (0.5, 0.4, 0.84)]
    for i, p in enumerate(verts):
        line3(ax, ccu, p, dashed=(i in (0, 3)), lw=0.8)
    for p in verts:
        atom(ax, p, 0.05, 'w')
    atom(ax, ccu, 0.065, 'h', zorder=8)
    # 左下角八面体（部分在胞外）
    ccu2 = (0, 0, 0)
    verts2 = [(-0.5, 0, 0), (0.5, 0, 0), (0, -0.5, 0), (0, 0.5, 0),
              (0, 0, 0.62), (0, 0, -0.62)]
    for i, p in enumerate(verts2):
        line3(ax, ccu2, p, dashed=(i in (2, 3, 5)), lw=0.8)
    for p in verts2:
        atom(ax, p, 0.05, 'w')
    atom(ax, ccu2, 0.065, 'h', zorder=8)
    triad(ax, 1.75, 0.0, s=0.62)
    # 图例
    ly = -0.55
    for lx, st, lab in [(-0.05, 'k', '(La,Sr)'), (0.75, 'h', 'Cu'),
                        (1.45, 'w', 'O')]:
        atom(ax, (lx, 0, ly), 0.08, st)
        ax.text(*P3(lx, 0, ly - 0.22), lab, fontsize=8.5, ha='center', va='top')
    ax.text(0.95, -1.05, u'(a) La$_{2-x}$Sr$_x$CuO$_4$（La-214）',
            fontsize=9, ha='center', va='top', fontfamily='SimSun')

    # -------- (b) Y-123
    ax = axs[1]
    a, b, c = 1.0, 0.8, 3.0
    cell_frame(ax, a, b, c)
    for z in (0.0, c):                                   # 顶/底面：Cu角 + O边中
        for p in [(0, 0, z), (a, 0, z), (a, b, z), (0, b, z)]:
            atom(ax, p, 0.07, 'h', zorder=7)
        for p in [(a / 2, 0, z), (a, b / 2, z), (a / 2, b, z), (0, b / 2, z)]:
            atom(ax, p, 0.048, 'w', zorder=6)
    # Ba 大白圈两层 + 链层 + CuO2 双层 + Y
    for z in (2.55, 0.45):
        atom(ax, (0.5, 0.06, z), 0.10, 'w')
        atom(ax, (0.5, 0.74, z), 0.10, 'w')
        atom(ax, (0, 0.4, z), 0.048, 'w')
        atom(ax, (1, 0.4, z), 0.048, 'w')
    for z in (2.1, 1.05):
        atom(ax, (0, 0.4, z), 0.062, 'h')
        atom(ax, (1, 0.4, z), 0.062, 'h')
        atom(ax, (0.5, 0.4, z), 0.048, 'w')
        atom(ax, (0, 0.0, z), 0.048, 'w')
        atom(ax, (0, 0.8, z), 0.048, 'w')
    for z in (1.62, 1.5, 1.38):
        for xx in (0.0, 1.0):
            atom(ax, (xx, 0.12, z), 0.048, 'w')
            atom(ax, (xx, 0.68, z), 0.048, 'w')
    atom(ax, (0, 0.4, 1.5), 0.065, 'h')
    atom(ax, (1, 0.4, 1.5), 0.065, 'h')
    atom(ax, (0.5, 0.4, 1.5), 0.078, 'k')
    # 左侧 CuO5 角锥（金字塔，顶点朝上偏外）
    ccu = (0, 0.4, 0.75)
    verts = [(-0.42, 0.4, 0.55), (0.42, 0.4, 0.55), (0, -0.05, 0.55),
             (0, 0.85, 0.55), (0, 0.4, 1.25)]
    for i, p in enumerate(verts):
        line3(ax, ccu, p, dashed=(i in (2, 3)), lw=0.8)
    for p in verts:
        atom(ax, p, 0.05, 'w')
    atom(ax, ccu, 0.062, 'h', zorder=8)
    triad(ax, 1.78, 0.0, s=0.62)
    ly = -0.55
    for lx, st, lab in [(-0.30, 'k', 'Y'), (0.15, 'w', 'Ba'),
                        (0.72, 'h', 'Cu'), (1.25, 'w', 'O')]:
        atom(ax, (lx, 0, ly), 0.08 if st != 'w' or lab == 'Ba' else 0.06, st)
        ax.text(*P3(lx, 0, ly - 0.22), lab, fontsize=8.5, ha='center', va='top')
    ax.text(0.95, -1.05, u'(b) YBa$_2$Cu$_3$O$_{6+x}$（Y-123）',
            fontsize=9, ha='center', va='top', fontfamily='SimSun')
    save(fig, '7-2')


# ================================================================ 图7.3
def fig_7_3():
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    plain_axes(ax)
    ax.set_aspect('equal', adjustable='datalim')

    def bi_column(x0, kinds, sublab, formula, tc, panel):
        a, b, h = 1.05, 0.82, 0.60
        n = len(kinds)
        z0 = 0.0
        for i, kd in enumerate(kinds):
            z = z0 + i * h
            line3(ax, (x0, 0, z), (x0 + a, 0, z),
                  dashed=(i not in (0, n - 1)), lw=0.8)
            line3(ax, (x0 + a, 0, z), (x0 + a, b, z), dashed=True, lw=0.8)
            line3(ax, (x0 + a, b, z), (x0, b, z), dashed=True, lw=0.8)
            line3(ax, (x0, b, z), (x0, 0, z), lw=0.8)
            plate_atoms(ax, z, x0, a, b, kd)
        zt = z0 + n * h
        # BiO 双层帽：上层板 + 虚线连接 + 竖杆
        zh = zt + 0.55
        for p, q in [((x0, 0, zt), (x0, 0, zh)), ((x0 + a, 0, zt), (x0 + a, 0, zh)),
                     ((x0 + a, b, zt), (x0 + a, b, zh)), ((x0, b, zt), (x0, b, zh))]:
            line3(ax, p, q, dashed=True, lw=0.8)
        for p in [(x0, 0, zh), (x0 + a, 0, zh), (x0 + a, b, zh), (x0, b, zh)]:
            atom(ax, p, 0.07, 'h', zorder=7)
        for p in [(x0 + a / 2, 0, zh), (x0 + a, b / 2, zh),
                  (x0 + a / 2, b, zh), (x0, b / 2, zh)]:
            atom(ax, p, 0.045, 'w', zorder=6)
        for p in [(x0, 0, zh), (x0 + a / 2, 0, zh), (x0 + a, 0, zh),
                  (x0, b, zh), (x0 + a, b, zh)]:
            line3(ax, p, (p[0], p[1], zh + 0.62), lw=1.0)
        # 底部脚注
        cx = x0 + a / 2 + CAX * b / 2
        ax.text(cx, -0.35, formula, fontsize=8.5, ha='center', va='top')
        ax.text(cx, -0.75, sublab, fontsize=8.5, ha='center', va='top')
        ax.text(cx, -1.10, tc, fontsize=8.5, ha='center', va='top')
        ax.text(cx, -1.48, panel, fontsize=9, ha='center', va='top')

    # (a) Bi-2201, (b) Bi-2212, (c) Bi-2223
    bi_column(0.0, ['Bi', 'Sr', 'Cu', 'Sr', 'Bi'],
              '(Bi-2201)', r'$\mathrm{Bi_2Sr_2Cu_1O_{6+x}}$',
              r'$T_{\rm c}$=10 K', '(a)')
    bi_column(2.6, ['Bi', 'Sr', 'Cu', 'Ca', 'Cu', 'Sr', 'Bi'],
              '(Bi-2212)', r'$\mathrm{Bi_2Sr_2Ca_1Cu_2O_{8+x}}$',
              r'$T_{\rm c}$=85 K', '(b)')
    bi_column(5.2, ['Bi', 'Sr', 'Cu', 'Ca', 'Cu', 'Ca', 'Cu', 'Sr', 'Bi'],
              '(Bi-2223)', r'$\mathrm{Bi_2Sr_2Ca_2Cu_3O_{10+x}}$',
              r'$T_{\rm c}$=110 K', '(c)')
    # 图例
    lx = 0.15
    for dy, st, lab in [(4.6, 'h', 'Bi'), (4.15, 'x', 'Ca'),
                        (3.7, 'l', 'Sr'), (3.25, 'k', 'Cu'), (2.8, 'w', 'O')]:
        atom(ax, (lx, 0, dy), 0.075, st)
        ax.text(lx + 0.22, dy + SAX * 0, lab, fontsize=9, ha='left', va='center')
    ax.set_xlim(-0.55, 7.6)
    ax.set_ylim(-2.1, 9.3)
    save(fig, '7-3')


# ================================================================ 图7.4
def fig_7_4():
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(5.0, 4.4))
    plain_axes(ax)
    ax.set_xlim(-0.055, 0.475)
    ax.set_ylim(-48, 668)

    arrow_axis(ax, 0, 0, 0, 648)
    arrow_axis(ax, 0, 0, 0.455, 0, lw=1.0)
    ax.text(-0.01, 640, r'$T$/K', fontsize=10, ha='right', va='top')
    for v in range(0, 601, 100):
        tick(ax, 0, v, -0.008, 0)
        ax.text(-0.012, v, str(v), fontsize=8.5, ha='right', va='center')
    for v in (0.1, 0.2, 0.3, 0.4):
        tick(ax, v, 0, 0, -10)
        ax.text(v, -16, f'{v:.1f}', fontsize=8.5, ha='center', va='top')
    ax.text(0, -22, r'$O$', fontsize=10, ha='right', va='top')
    ax.text(0.46, -30, u'浓度 $x$', fontsize=9.5, ha='center', va='top',
            fontfamily='SimSun')

    # T_OT 结构线（点划线 + 数据点）
    xs = np.array([0, 0.01, 0.02, 0.04, 0.06, 0.08, 0.10, 0.113, 0.13,
                   0.145, 0.163, 0.178, 0.19])
    ys = np.array([527, 505, 478, 437, 398, 352, 305, 262, 220,
                   187, 138, 96, 58])
    f = PchipInterpolator(xs, ys)
    xx = np.linspace(0, 0.19, 300)
    ax.plot(xx, f(xx), 'k-.', lw=1.2, dashes=(6, 2, 1, 2))
    for x0 in (0, 0.003, 0.018, 0.037, 0.055, 0.10, 0.113, 0.118):
        ax.plot(x0, f(x0), 'o', mfc='white', mec='k', ms=4.2)
    for x0 in (0.105, 0.145, 0.163):
        ax.plot(x0, f(x0), 'ko', ms=4.2)
    ax.plot(0.19, 0, 'ko', ms=4.2)                    # 轴上的实心点
    # T_N 虚线（奈尔线）+ 三角
    xs2 = np.array([0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.008, 0.011])
    ys2 = np.array([300, 262, 230, 198, 170, 140, 112, 68, 25])
    g = PchipInterpolator(xs2, ys2)
    xg = np.linspace(0, 0.011, 200)
    ax.plot(xg, g(xg), 'k--', lw=1.2, dashes=(4, 2))
    for x0 in (0.002, 0.004):
        ax.plot(x0, g(x0), '^', mfc='white', mec='k', ms=4.5)
    # 自旋玻璃小区域（近轴原点，竖直阴影）
    ax.add_patch(Polygon([(0.001, 0), (0.03, 0), (0.012, 36), (0.001, 44)],
                         closed=True, fc='white', ec='none', hatch='|||||'))
    # 绝缘体-金属边界竖直阴影带
    ax.add_patch(Rectangle((0.054, 0), 0.011, 96, fc='white', ec='none',
                           hatch='|||||'))
    # 超导穹顶
    xd = np.array([0.055, 0.065, 0.08, 0.10, 0.115, 0.13, 0.15, 0.17,
                   0.19, 0.21, 0.23, 0.25, 0.27, 0.285, 0.30, 0.315, 0.33])
    yd = np.array([0, 9, 18, 26, 32, 37, 40.5, 42, 41.5, 38, 33, 26,
                   17, 9, 3, 1.2, 0.4])
    fd = PchipInterpolator(xd, yd)
    xx = np.linspace(0.055, 0.33, 400)
    ax.plot(xx, fd(xx), 'k-', lw=1.3)
    for x0 in (0.065, 0.08, 0.095, 0.115, 0.135, 0.155, 0.175, 0.195, 0.215,
               0.235, 0.255, 0.275, 0.29, 0.305, 0.318, 0.332):
        ax.plot(x0, fd(x0), 'kx', ms=4, mew=1.1)
    for x0 in (0.02, 0.03, 0.042, 0.052):
        ax.plot(x0, 1.5, 'kx', ms=3, mew=0.9)         # 轴附近的小杂点
    ax.plot(0.19, 0, 'ko', ms=4)
    # 文字
    ax.annotate(u'正交', xy=(0.002, 300), xytext=(0.02, 305),
                fontsize=9.5, va='center',
                arrowprops=dict(arrowstyle='->', lw=0.9))
    ax.text(0.13, 300, u'四方', fontsize=9.5, ha='left', va='center')
    ax.annotate(u'奈尔态', xy=(0.006, 112), xytext=(0.033, 128),
                fontsize=9.5, va='center',
                arrowprops=dict(arrowstyle='->', lw=0.9))
    ax.annotate(u'绝缘体', xy=(0.0595, 60), xytext=(0.018, 68),
                fontsize=9.5, va='center',
                arrowprops=dict(arrowstyle='->', lw=0.9))
    ax.text(0.115, 82, u'金属', fontsize=9.5, ha='left', va='center')
    ax.text(0.165, 22, u'超导体', fontsize=9.5, ha='center', va='center')
    ax.annotate(u'自旋玻璃', xy=(0.014, 22), xytext=(0.0, 58),
                fontsize=9.5, ha='right', va='center',
                arrowprops=dict(arrowstyle='->', lw=0.9,
                                connectionstyle='arc3,rad=0.35'))
    save(fig, '7-4')


# ================================================================ 图7.5
def fig_7_5():
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    plain_axes(ax)
    ax.set_xlim(-0.06, 1.24)
    ax.set_ylim(-0.1, 1.1)

    arrow_axis(ax, 0, 0, 0, 1.04)
    arrow_axis(ax, 0, 0, 1.22, 0, lw=1.0)
    vtext(ax, -0.035, 0.93, u'温度', fontsize=9.5)
    ax.text(1.2, -0.045, u'掺杂程度', fontsize=9.5, ha='center', va='top')
    # 反铁磁奈尔线
    ax.plot([0.03, 0.10], [0.93, 0.0], 'k-', lw=1.3)
    # 分界虚线
    for xv in (0.30, 0.68):
        ax.plot([xv, xv], [0, 0.97], 'k--', lw=1.0, dashes=(4, 2.2))
    # 超导穹顶
    xd = np.array([0.31, 0.36, 0.42, 0.48, 0.54, 0.60, 0.66])
    yd = np.array([0.02, 0.16, 0.26, 0.295, 0.26, 0.16, 0.02])
    f = PchipInterpolator(xd, yd)
    xx = np.linspace(0.31, 0.66, 300)
    ax.plot(xx, f(xx), 'k-', lw=1.3)
    # 区域文字
    ax.text(0.155, 0.78, u'绝缘体\n(自旋液体)', fontsize=9, ha='center',
            va='center', linespacing=1.5)
    ax.text(0.155, 0.63, '(Ⅱ)', fontsize=9, ha='center', va='center')
    ax.text(0.49, 0.80, u'强关联金属\n(非费密液体)', fontsize=9, ha='center',
            va='center', linespacing=1.5)
    ax.text(0.49, 0.65, '(Ⅲ)', fontsize=9, ha='center', va='center')
    ax.text(0.84, 0.80, u'正常金属\n(费密液体)', fontsize=9, ha='center',
            va='center', linespacing=1.5)
    ax.text(0.84, 0.65, '(Ⅴ)', fontsize=9, ha='center', va='center')
    ax.text(0.062, 0.40, '(Ⅰ)\n反铁磁\n绝缘体', fontsize=9, ha='center',
            va='center', linespacing=1.4)
    vtext(ax, 0.49, 0.435, u'最佳掺杂', fontsize=9)
    ax.text(0.55, 0.325, r'$T_{\rm c}^{\max}$', fontsize=9, ha='left',
            va='center')
    vtext(ax, 0.345, 0.30, u'弱掺杂', fontsize=9)
    vtext(ax, 0.635, 0.30, u'过掺杂', fontsize=9)
    ax.text(0.345, 0.20, r'$T_{\rm c}$', fontsize=9.5, ha='center', va='center')
    ax.text(0.50, 0.215, '(Ⅳ)', fontsize=9, ha='center', va='center')
    ax.text(0.49, 0.115, u'高温超导体', fontsize=9, ha='center', va='center')
    save(fig, '7-5')


# ================================================================ 图7.6
def fig_7_6():
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.75))
    for ax in axs:
        plain_axes(ax)
        ax.set_aspect('equal')
        ax.set_xlim(-1.55, 1.55)
        ax.set_ylim(-1.55, 1.55)
        ax.plot([-1.4, 1.4], [0, 0], 'k-', lw=0.8)
        ax.plot([0, 0], [-1.4, 1.4], 'k-', lw=0.8)
        ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.2, ec='k'))
    # (a) 各向同性 s 波
    axs[0].text(0.5, -1.75, u'(a) 各向同性 s 波', fontsize=9, ha='center',
                va='top', fontfamily='SimSun')
    # (b) d 波：|cos2θ| 四瓣，瓣内标 +
    th = np.linspace(0, 2 * np.pi, 720)
    r = 1.45 * np.abs(np.cos(2 * th))
    axs[1].plot(r * np.cos(th), r * np.sin(th), 'k-', lw=1.1)
    for ang, sg in [(0, '+'), (90, '+'), (180, '+'), (270, '+')]:
        a = np.deg2rad(ang)
        axs[1].text(0.62 * np.cos(a), 0.62 * np.sin(a), sg, fontsize=10,
                    ha='center', va='center')
    axs[1].text(0.5, -1.75, r'(b) d$_{x^2-y^2}$波', fontsize=9,
                ha='center', va='top', fontfamily='SimSun')
    # (c) 各向异性 s 波：交叉椭圆
    for w, h in [(0.42, 2.75), (2.75, 0.42)]:
        axs[2].add_patch(Ellipse((0, 0), w, h, fill=False, lw=1.1, ec='k'))
    axs[2].text(0.5, -1.75, u'(c) 各向异性 s 波', fontsize=9, ha='center',
                va='top', fontfamily='SimSun')
    save(fig, '7-6')


# ================================================================ 图7.7
def fig_7_7():
    fig, axs = plt.subplots(1, 2, figsize=(6.8, 3.6))
    for ax in axs:
        plain_axes(ax)
        ax.set_aspect('equal')
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.42, 1.05)

    def ybco_rect(ax, x0, y0, w, h):
        ax.add_patch(Rectangle((x0, y0), w, h, fc='white', ec='k', lw=1.2,
                               hatch='/////'))

    # -------- (a) 两垂直结组合
    ax = axs[0]
    ax.add_patch(Rectangle((0.02, 0.03), 0.95, 0.94, fc='white', ec='k', lw=1.4))
    ybco_rect(ax, 0.55, 0.03, 0.42, 0.94)          # 右带
    ybco_rect(ax, 0.02, 0.03, 0.53, 0.38)          # 左下块
    ax.add_patch(Rectangle((0.02, 0.41), 0.53, 0.56, fc='white', ec='none'))
    ax.add_patch(Rectangle((0.30, 0.41), 0.25, 0.27, fc='white', ec='k', lw=1.6))
    ax.plot([0.55, 0.55], [0.68, 0.97], 'k--', lw=1.0, dashes=(3.5, 1.8))
    ax.plot([0.02, 0.30], [0.41, 0.41], 'k--', lw=1.0, dashes=(3.5, 1.8))
    ax.text(0.425, 0.545, r'$\Phi$', fontsize=11, ha='center', va='center')
    ax.text(0.12, 0.86, 'Pb', fontsize=10, ha='center', va='center')
    ax.text(0.68, 0.20, 'YBCO', fontsize=9, ha='center', va='center',
            bbox=dict(fc='white', ec='none', pad=0.4))
    for px, py in [(0.44, 0.80), (0.12, 0.55)]:
        ax.add_patch(Circle((px, py), 0.035, fill=False, lw=0.9, ec='k'))
        ax.plot([px - 0.02, px + 0.02], [py, py], 'k-', lw=0.8)
        ax.plot([px, px], [py - 0.02, py + 0.02], 'k-', lw=0.8)
    dclover(ax, 0.79, 0.80, 0.13, rot=0)
    dclover(ax, 0.17, 0.22, 0.13, rot=45)
    arrow_axis(ax, 0.40, -0.12, 0.40, 0.05, lw=0.9)
    arrow_axis(ax, 0.40, -0.12, 0.56, -0.12, lw=0.9)
    ax.text(0.385, 0.05, r'$b$', fontsize=9, ha='right', va='center')
    ax.text(0.58, -0.12, r'$a$', fontsize=9, ha='left', va='center')
    ax.text(0.5, -0.28, u'(a) 两垂直结组合', fontsize=9.5, ha='center', va='top')

    # -------- (b) 两平行结组合
    ax = axs[1]
    ax.add_patch(Rectangle((0.02, 0.03), 0.95, 0.94, fc='white', ec='k', lw=1.4))
    ybco_rect(ax, 0.60, 0.03, 0.37, 0.94)
    ax.plot([0.60, 0.60], [0.03, 0.97], 'k--', lw=1.0, dashes=(3.5, 1.8))
    ax.add_patch(Rectangle((0.38, 0.38), 0.22, 0.27, fc='white', ec='k', lw=1.6))
    ax.text(0.49, 0.515, r'$\Phi$', fontsize=11, ha='center', va='center')
    ax.text(0.13, 0.86, 'Pb', fontsize=10, ha='center', va='center')
    ax.text(0.80, 0.515, 'YBCO', fontsize=9, ha='center', va='center',
            bbox=dict(fc='white', ec='none', pad=0.4))
    for px, py in [(0.16, 0.80), (0.16, 0.20)]:
        ax.add_patch(Circle((px, py), 0.035, fill=False, lw=0.9, ec='k'))
        ax.plot([px - 0.02, px + 0.02], [py, py], 'k-', lw=0.8)
        ax.plot([px, px], [py - 0.02, py + 0.02], 'k-', lw=0.8)
    dclover(ax, 0.80, 0.80, 0.13, rot=0)
    dclover(ax, 0.80, 0.20, 0.13, rot=0)
    arrow_axis(ax, 0.40, -0.12, 0.40, 0.05, lw=0.9)
    arrow_axis(ax, 0.40, -0.12, 0.56, -0.12, lw=0.9)
    ax.text(0.385, 0.05, r'$b$', fontsize=9, ha='right', va='center')
    ax.text(0.58, -0.12, r'$a$', fontsize=9, ha='left', va='center')
    ax.text(0.5, -0.28, u'(b) 两平行结组合', fontsize=9.5, ha='center', va='top')
    save(fig, '7-7')


# ================================================================ 图7.8
def fig_7_8():
    fig, ax = plt.subplots(figsize=(3.5, 3.2))
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    ax.set_xlim(0.05, 0.28)
    ax.set_ylim(0, 43)
    ax.set_xticks([0.05, 0.10, 0.15, 0.20, 0.25])
    ax.set_xticklabels(['0.05', '0.10', '0.15', '0.20', '0.25'])
    ax.set_yticks([0, 10, 20, 30, 40])
    ax.tick_params(direction='in', length=3.5, labelsize=8.5)
    ax2 = ax.twinx()
    ax2.set_ylim(0, 0.86)
    ax2.set_yticks([0, 0.4, 0.8])
    ax2.set_yticklabels(['0.0', '0.4', '0.8'])
    ax2.tick_params(direction='in', length=3.5, labelsize=8.5)
    ax.set_xlabel(r'$x$', fontsize=10)
    ax.set_ylabel(r'$T_{\rm c}$/K', fontsize=10)
    ax2.set_ylabel(r'$\alpha_0$', fontsize=10, rotation=270, labelpad=14)
    xt = [0.07, 0.11, 0.125, 0.15, 0.19, 0.22, 0.27]
    Tc = [21, 29.7, 31.8, 38.2, 34.4, 22.8, 7.8]
    xa = [0.07, 0.11, 0.122, 0.145, 0.185, 0.23, 0.27]
    al = [0.39, 0.63, 0.776, 0.10, 0.05, 0.10, 0.115]
    ax.plot(xt, Tc, 'k-', lw=1.1)
    ax.plot(xt, Tc, 'ks', ms=4.5)
    ax2.plot(xa, al, 'k-', lw=1.1)
    ax2.errorbar([0.122], [0.776], yerr=[[0.028], [0.028]], fmt='ko',
                 mfc='white', mec='k', ms=4.5, lw=0.9, capsize=2.5)
    ax2.plot([xa[0], xa[1], xa[3], xa[4], xa[5], xa[6]],
             [al[0], al[1], al[3], al[4], al[5], al[6]], 'o', mfc='white',
             mec='k', ms=4.5)
    ax.text(0.155, 40.3, r'La$_{2-x}$Sr$_x$CuO$_4$', fontsize=9,
            ha='left', va='center')
    save(fig, '7-8')


# ================================================================ 图7.9
def fig_7_9():
    fig, ax = plt.subplots(figsize=(3.6, 3.3))
    plain_axes(ax)
    ax.set_xlim(-0.012, 0.345)
    ax.set_ylim(-0.075, 1.22)

    arrow_axis(ax, 0, 0, 0, 1.16)
    arrow_axis(ax, 0, 0, 0.335, 0, lw=1.0)
    ax.plot([0, 0.30], [1.13, 1.13], 'k-', lw=0.9)
    ax.plot([0.30, 0.30], [0, 1.13], 'k-', lw=0.9)
    ax.text(-0.005, 1.20, r'$\alpha_{\rm O}$,$\alpha_{\rm Cu}$', fontsize=10,
            ha='left', va='bottom')
    for v in np.arange(0, 1.01, 0.2):
        tick(ax, 0, v, -0.006, 0)
        ax.text(-0.008, v, f'{v:.1f}', fontsize=8, ha='right', va='center')
        if v < 1.0:
            tick(ax, 0, v + 0.1, -0.004, 0)
    for v in np.arange(0.02, 0.301, 0.04):
        tick(ax, v, 0, 0, -0.012)
        ax.text(v, -0.02, f'{v:.2f}', fontsize=7.5, ha='center', va='top')
    ax.text(0.33, -0.025, r'$x$', fontsize=10, ha='center', va='center')

    def ebar(x, y, e):
        ax.plot([x, x], [y - e, y + e], 'k-', lw=0.8)
        ax.plot([x - 0.004, x + 0.004], [y - e, y - e], 'k-', lw=0.8)
        ax.plot([x - 0.004, x + 0.004], [y + e, y + e], 'k-', lw=0.8)

    # M=Sr alpha_O（实心圆折线）
    xs = [0.075, 0.10, 0.113, 0.125, 0.135, 0.145, 0.155, 0.185, 0.23]
    ys = [0.40, 0.545, 0.635, 0.775, 0.565, 0.155, 0.08, 0.05, 0.10]
    ax.plot(xs, ys, 'k-', lw=1.1)
    for x, y in zip(xs, ys):
        ax.plot(x, y, 'ko', ms=4)
    # M=Ba alpha_O（三角折线）
    xs = [0.075, 0.10, 0.113, 0.143, 0.185]
    ys = [0.30, 0.52, 0.61, 0.215, 0.10]
    ax.plot(xs, ys, 'k-', lw=1.1)
    for x, y in zip(xs, ys):
        ax.plot(x, y, '^', mfc='white', mec='k', ms=4.5)
    # alpha_Cu（空心圆）
    for x, y, e in [(0.125, 0.975, 0.045), (0.127, 0.885, 0.045),
                    (0.143, 0.18, 0.03), (0.155, 0.12, 0.02),
                    (0.185, 0.075, 0.02), (0.23, 0.10, 0.02)]:
        ebar(x, y, e)
        ax.plot(x, y, 'o', mfc='white', mec='k', ms=4.5)
    # 图例
    lx, ly0 = 0.175, 1.02
    ax.plot(lx, ly0, 'ko', ms=4)
    ax.text(lx + 0.015, ly0, r'M=Sr  $\alpha_{\rm O}$', fontsize=8.5,
            ha='left', va='center')
    ax.plot(lx, ly0 - 0.09, '^', mfc='white', mec='k', ms=4.5)
    ax.text(lx + 0.015, ly0 - 0.09, r'M=Ba  $\alpha_{\rm O}$', fontsize=8.5,
            ha='left', va='center')
    ax.plot(lx, ly0 - 0.18, 'o', mfc='white', mec='k', ms=4.5)
    ax.text(lx + 0.015, ly0 - 0.18, r'M=Sr  $\alpha_{\rm Cu}$', fontsize=8.5,
            ha='left', va='center')
    save(fig, '7-9')


# ================================================================ 图7.10
def fig_7_10():
    fig, ax = plt.subplots(figsize=(3.3, 3.0))
    plain_axes(ax)
    ax.set_xlim(-0.14, 2.5)
    ax.set_ylim(-0.18, 2.85)

    arrow_axis(ax, 0, 0, 0, 2.72)
    arrow_axis(ax, 0, 0, 2.42, 0, lw=1.0)
    ax.text(-0.04, 2.66, r'$g_{\rm s}(\omega)$', fontsize=10, ha='right',
            va='center')
    D0 = 0.9
    tick(ax, D0, 0, 0, -0.06)
    ax.text(D0, -0.09, r'$\Delta_0$', fontsize=10, ha='center', va='top')
    ax.text(2.36, -0.11, r'$\omega$', fontsize=10, ha='center', va='center')
    ax.plot([0, 2.3], [1, 1], 'k--', lw=0.9, dashes=(4, 2))
    ax.text(-0.02, 1.0, r'$g(0)$', fontsize=9.5, ha='right', va='center')
    # l=0（s 波）：Δ0 以下为 0，以上发散衰减
    x0 = np.linspace(D0 + 0.004, 2.3, 300)
    ax.plot(x0, 1 + 0.134 / np.sqrt(x0 - D0), 'k-', lw=1.4)
    # l=2（d 波）：ω² 上升 → Δ0 处尖峰 → 回到 g(0)
    u = np.linspace(0, D0, 300)
    ax.plot(u, 1 + 1.1 * (u / D0) ** 2 * np.exp(-2.2 * u / D0) - 1, 'k-', lw=1.4)
    x2 = np.linspace(D0, 2.3, 200)
    ax.plot(x2, 1 + 0.16 * np.exp(-(x2 - D0) / 0.35), 'k-', lw=1.4)
    # Δ0 处竖直尖峰
    ax.plot([D0, D0], [1.02, 2.45], 'k-', lw=1.2)
    # 标注
    ax.text(0.34, 0.30, r'$l$=2', fontsize=9, ha='center', va='center')
    ax.text(0.52, 0.09, r'$l$=0', fontsize=9, ha='center', va='center')
    ax.text(1.42, 1.38, r'$l$=0', fontsize=9, ha='center', va='center')
    ax.text(1.42, 1.13, r'$l$=2', fontsize=9, ha='center', va='center')
    save(fig, '7-10')


# ================================================================ 图7.11
def fig_7_11():
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    ax.set_xlim(0, 850)
    ax.set_ylim(0, 640)
    ax.set_xticks([200, 400, 600, 800])
    ax.set_yticks([200, 400, 600])
    ax.tick_params(direction='in', length=3.5, labelsize=8.5)
    ax.set_xlabel(r'$T$/K', fontsize=10)
    ax.set_ylabel(r'$\rho_{\rm ab}$/(10$^{-8}$ $\Omega\cdot$m)', fontsize=9.5)

    def drop(T, r1):
        ax.plot([T, T], [0, r1], 'k-', lw=1.3)

    # Y-123(60K)：凸曲线
    drop(60, 225)
    xc = np.array([60, 70, 90, 120, 160, 200, 250, 300, 350, 392])
    yc = np.array([225, 233, 243, 258, 285, 318, 365, 420, 490, 578])
    from scipy.interpolate import PchipInterpolator
    f = PchipInterpolator(xc, yc)
    xx = np.linspace(60, 392, 300)
    ax.plot(xx, f(xx), 'k-', lw=1.4)
    ax.text(360, 585, r'Y-123($T_{\rm c}$=60 K)', fontsize=9,
            ha='left', va='center')
    # Bi-2201
    drop(13, 95)
    ax.plot([13, 720], [95, 553], 'k-', lw=1.4)
    ax.text(370, 508, 'Bi-2201', fontsize=9, ha='center', va='center')
    ax.text(620, 512, '(10 K)', fontsize=9, ha='center', va='center')
    # La-214
    drop(42, 120)
    ax.plot([42, 770], [120, 455], 'k-', lw=1.4)
    ax.text(500, 445, 'La-214', fontsize=9, ha='center', va='center')
    ax.text(500, 413, '(40 K)', fontsize=9, ha='center', va='center')
    # Bi-2212
    drop(85, 97)
    ax.plot([85, 680], [97, 308], 'k-', lw=1.4)
    ax.text(545, 332, 'Bi-2212(85K)', fontsize=9, ha='center', va='center')
    # Y-123(90K)
    drop(95, 62)
    ax.plot([95, 650], [62, 130], 'k-', lw=1.4)
    ax.text(510, 170, 'Y-123(90 K)', fontsize=9, ha='center', va='center')
    save(fig, '7-11')


# ================================================================ 图7.12
def fig_7_12():
    fig, ax = plt.subplots(figsize=(3.4, 3.3))
    plain_axes(ax)
    ax.set_xlim(-0.022, 0.475)
    ax.set_ylim(-0.022, 0.355)

    arrow_axis(ax, 0, 0, 0, 0.34)
    arrow_axis(ax, 0, 0, 0.46, 0, lw=1.0)
    ax.text(-0.012, 0.335, r'$\rho/\rho_0$', fontsize=10, ha='right', va='center')
    for v in (0.1, 0.2, 0.3):
        tick(ax, 0, v, -0.008, 0)
        ax.text(-0.011, v, f'{v:.1f}', fontsize=8, ha='right', va='center')
    ax.text(-0.011, 0, '0.0', fontsize=8, ha='right', va='center')
    for v in (0.1, 0.2, 0.3, 0.4):
        tick(ax, v, 0, 0, -0.008)
        ax.text(v, -0.011, f'{v:.1f}', fontsize=8, ha='center', va='top')
    ax.text(0.466, -0.013, r'$T/\theta_{\rm D}$', fontsize=10, ha='left',
            va='center')

    # B-G 公式曲线（归一化到 0.4 处为 0.30）
    z = np.linspace(0, 60, 200001)
    integ = np.zeros_like(z)
    integ[1:] = z[1:] ** 5 / (np.expm1(z[1:]) * (1 - np.exp(-z[1:])))
    dz = z[1] - z[0]
    F = np.concatenate([[0.0], np.cumsum((integ[1:] + integ[:-1]) / 2 * dz)])
    u = np.linspace(0.001, 0.46, 500)
    vals = np.interp(1.0 / u, z, F) * u ** 5
    vals = vals * (0.30 / vals[u > 0.399][0])
    ax.plot(u, vals, 'k-', lw=1.4)
    # θD/5 虚线
    u5 = 0.185
    y5 = vals[u > u5 - 0.002][0]
    ax.plot([u5, u5], [0, y5], 'k--', lw=0.9, dashes=(4, 2))
    # 实验点（沿曲线布点，五类金属）
    pts = [('^', 0.150), ('^', 0.190), ('^', 0.230), ('^', 0.255), ('^', 0.275),
           ('^', 0.300), ('^', 0.325), ('s', 0.385),
           ('o', 0.050), ('o', 0.075), ('o', 0.100), ('o', 0.120),
           ('v', 0.135), ('v', 0.155), ('v', 0.175), ('v', 0.195),
           ('o', 0.210), ('o', 0.240),
           ('p', 0.265), ('p', 0.290), ('p', 0.320), ('p', 0.345), ('p', 0.365),
           ('s', 0.400), ('s', 0.415), ('^', 0.355)]
    for mk, uu in pts:
        yy = vals[u > uu - 0.002][0]
        ax.plot(uu, yy, mk, mfc='white', mec='k', ms=3.6 if mk != 'p' else 3.2)
    # 图例文字
    leg = [(u'\u25b2  Au', r'$\theta_{\rm D}$=175K'),
           (u'\u25a1  Na', '202K'), (u'\u25cb  Cu', '333K'),
           (u'\u25bc  Al', '395K'), (u'\u25cf  Ni', '472K')]
    for i, (s1, s2) in enumerate(leg):
        yy = 0.315 - i * 0.026
        ax.text(0.045, yy, s1, fontsize=8, ha='left', va='center',
                fontfamily='SimSun')
        ax.text(0.155, yy, s2, fontsize=8, ha='left', va='center')
    save(fig, '7-12')


# ================================================================ 图7.13
def fig_7_13():
    fig, ax = plt.subplots(figsize=(4.6, 3.3))
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    ax.set_xlim(0, 1500)
    ax.set_ylim(0, 2.3)
    ax.set_xticks([0, 500, 1000, 1500])
    ax.set_xticklabels(['0', '500', '1000', '1500'])
    ax.set_yticks([0, 1, 2])
    ax.tick_params(direction='in', length=3.5, labelsize=8.5)
    ax.set_xlabel(u'光子能量/cm$^{-1}$', fontsize=9.5, fontfamily='SimSun')
    ax.set_ylabel(u'电导率/(10$^3\\Omega\\cdot$m)', fontsize=9.5,
                  fontfamily='SimSun')
    # 顶部 eV 轴
    axTop = ax.twiny()
    axTop.set_xlim(0, 1500)
    axTop.set_xticks([0, 403, 807, 1210])
    axTop.set_xticklabels(['0', '0.05', '0.1', '0.15'])
    axTop.tick_params(direction='in', length=3.5, labelsize=8.5, pad=1)
    axTop.set_xlabel('eV', fontsize=9, labelpad=0)

    from scipy.interpolate import PchipInterpolator
    c1 = PchipInterpolator([0, 20, 40, 80, 150, 250, 400, 700, 1000, 1300],
                           [2, 1.3, 1.0, 0.85, 0.75, 0.63, 0.52, 0.42, 0.36, 0.325])
    c2 = PchipInterpolator([0, 20, 40, 80, 150, 250, 400, 600, 800, 1000, 1200],
                           [2, 1.45, 1.25, 1.05, 0.92, 0.80, 0.68, 0.58, 0.52,
                            0.47, 0.44])
    x1 = np.linspace(0, 1380, 300)
    ax.plot(x1, c1(x1), 'k-', lw=1.4)
    ax.text(240, 0.95, '100 K', fontsize=9, ha='left', va='center')
    ax.plot(x1, c2(x1), 'k-', lw=1.4)
    ax.text(1220, 0.55, '200 K', fontsize=9, ha='left', va='center')
    # 特鲁德拟合（点线）
    cd = PchipInterpolator([0, 50, 100, 150, 200, 250, 300, 360],
                           [2, 1.35, 1.02, 0.75, 0.52, 0.36, 0.25, 0.18])
    xd = np.linspace(0, 360, 200)
    ax.plot(xd, cd(xd), 'k:', lw=1.6)
    # 直流电导率标注
    ax.annotate(u'直流电导率', xy=(45, 2.0), xytext=(260, 2.02),
                fontsize=9, va='center',
                arrowprops=dict(arrowstyle='->', lw=0.9))
    # k_B×200K 箭头
    ax.annotate('', xy=(139, 0.0), xytext=(139, 0.15),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                mutation_scale=10))
    save(fig, '7-13')


# ================================================================ 图7.14
def fig_7_14():
    fig, ax = plt.subplots(figsize=(3.1, 3.0))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-1.75, 1.6)
    ax.add_patch(Circle((0, 0.05), 1.0, fill=False, lw=1.3, ec='k'))
    ax.plot([-0.55, 0.55], [0.47, 0.47], 'k-', lw=1.2)
    ax.plot([-0.55, 0.55], [-0.37, -0.37], 'k-', lw=1.2)
    ax.text(-0.28, 0.53, r'$E_m$', fontsize=9.5, ha='center', va='bottom')
    ax.text(-0.28, -0.44, r'$E_n$', fontsize=9.5, ha='center', va='top')
    ax.annotate('', xy=(0.22, -0.34), xytext=(0.22, 0.44),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                mutation_scale=11))
    ax.text(0.33, 0.05, r'T$_1^{-1}$', fontsize=9.5, ha='left', va='center')
    # 电子入射/出射
    ax.annotate('', xy=(-0.96, 0.45), xytext=(-2.1, -0.35),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.1,
                                mutation_scale=12))
    ax.annotate('', xy=(2.15, -0.55), xytext=(0.99, 0.30),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.1,
                                mutation_scale=12))
    ax.text(-1.75, 0.62, u'电子', fontsize=9.5, ha='center', va='center')
    ax.text(-1.75, -0.30, r'$\varepsilon_{k\alpha}$', fontsize=9.5,
            ha='center', va='center')
    ax.text(1.72, 0.55, u'电子', fontsize=9.5, ha='center', va='center')
    ax.text(1.72, -0.18, r"$\varepsilon_{k'\alpha'}$", fontsize=9.5,
            ha='center', va='center')
    ax.text(0, -1.32, u'核体系', fontsize=9.5, ha='center', va='center')
    save(fig, '7-14')


# ================================================================ 图7.15
def fig_7_15():
    fig, ax = plt.subplots(figsize=(3.6, 3.1))
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    ax.set_xlim(15, 305)
    ax.set_ylim(0, 8.2)
    ax.set_xticks([100, 200, 300])
    ax.set_yticks([0, 2, 4, 6, 8])
    ax.tick_params(direction='in', length=3.5, labelsize=8.5)
    ax.set_xlabel(r'$T$/K', fontsize=10)
    ax.set_ylabel(r'$(T_1T)^{-1}$/(s$^{-1}\cdot$K$^{-1}$)', fontsize=9)
    oc = [55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 120, 130, 140,
          150, 160, 175, 190, 200, 215, 230, 250, 270, 280]
    ov = [2.1, 2.65, 3.1, 3.6, 4.15, 4.6, 5.1, 5.45, 5.55, 5.75, 6.2, 6.25,
          6.75, 6.8, 6.75, 6.7, 6.6, 6.45, 6.05, 5.9, 5.8, 5.6, 5.3, 5.2, 5.1]
    sq = [40, 50, 60, 70, 80, 90, 95, 100, 105, 110, 115, 120, 125, 130, 140,
          150, 160, 175, 190, 205, 220, 235, 255, 270]
    sv = [0.35, 0.45, 0.6, 0.9, 1.45, 2.5, 3.4, 4.35, 5.9, 5.95, 6.5, 6.75,
          6.85, 6.6, 6.25, 5.8, 5.6, 5.1, 4.75, 4.6, 4.5, 4.45, 4.3, 4.1]
    ax.plot(oc, ov, 'o', mfc='white', mec='k', ms=4.2)
    ax.plot(sq, sv, 's', mfc='white', mec='k', ms=4.0)
    save(fig, '7-15')


# ================================================================ 图7.16
def fig_7_16():
    from scipy.interpolate import PchipInterpolator
    fig, axs = plt.subplots(2, 1, figsize=(4.9, 7.2))

    # ---------- (a) 弱掺杂
    ax = axs[0]
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 10)
    ax.set_xticks([0, 200, 400, 600, 800, 1000])
    ax.set_xticklabels(['0', '200', '400', '600', '800', '1000'])
    ax.set_yticks([0, 2, 4, 6, 8, 10])
    ax.tick_params(direction='in', length=3.5, labelsize=8.5)
    ax2 = ax.twinx()
    ax2.set_ylim(0, 30)
    ax2.set_yticks([0, 5, 10, 15, 20, 25, 30])
    ax2.tick_params(direction='in', length=3.5, labelsize=8.5)
    ax.set_xlabel(r'$T$/K', fontsize=10)
    ax.set_ylabel(r'$\rho_{\rm ab}$/(10$^{-5}$ $\Omega\cdot$m)', fontsize=9)
    ax2.set_ylabel(r'$\rho$/(10$^{-5}$ $\Omega\cdot$m)', fontsize=9,
                   rotation=270, labelpad=16)
    ax.text(180, 9.25, r'La$_{2-x}$Sr$_x$CuO$_4$', fontsize=9)

    def curve(pts, ls='-', lw_=1.4):
        f = PchipInterpolator([p[0] for p in pts], [p[1] for p in pts])
        xx = np.linspace(pts[0][0], pts[-1][0], 400)
        if ls == '--':
            ax.plot(xx, f(xx), 'k' + ls, lw=lw_, dashes=(4, 2.2))
        else:
            ax.plot(xx, f(xx), 'k' + ls, lw=lw_)

    curve([(0, 9.8), (25, 4.6), (50, 3.0), (90, 2.25), (140, 2.05),
           (180, 2.08), (300, 2.95), (450, 4.85), (600, 6.7), (750, 8.1),
           (900, 8.45)], ':', 1.6)
    curve([(0, 7.2), (20, 3.4), (40, 2.3), (80, 1.8), (150, 1.6),
           (250, 1.9), (400, 2.85), (600, 4.2), (800, 5.55), (1000, 6.4)])
    curve([(0, 2.3), (30, 1.5), (70, 1.36), (150, 1.38), (300, 1.9),
           (500, 2.85), (700, 3.95), (880, 4.85)], ':', 1.6)
    curve([(0, 1.9), (40, 1.35), (150, 1.42), (350, 2.1), (600, 2.75),
           (800, 3.2), (1000, 3.55)])
    curve([(0, 1.1), (25, 0.62), (60, 0.56), (200, 0.75), (400, 1.15),
           (700, 1.8), (1000, 2.6)])
    curve([(0, 0.35), (20, 0.22), (40, 0.17), (150, 0.30), (300, 0.52),
           (500, 0.78), (700, 1.05), (850, 1.28), (1000, 1.52)])
    curve([(0, 0.10), (30, 0.16), (200, 0.25), (500, 0.40), (800, 0.55),
           (1000, 0.64)], '-.', 1.0)
    ax.text(660, 8.75, '0.04', fontsize=8.5, ha='center', va='bottom')
    ax.text(590, 6.6, '0.05', fontsize=8.5, ha='center', va='bottom')
    ax.text(700, 4.72, '0.07', fontsize=8.5, ha='center', va='bottom')
    ax.text(580, 3.32, '0.075', fontsize=8.5, ha='center', va='bottom')
    ax.annotate('0.1', xy=(660, 1.72), xytext=(720, 2.15), fontsize=8.5,
                va='center', arrowprops=dict(arrowstyle='->', lw=0.8))
    ax.annotate('0.15', xy=(740, 1.32), xytext=(800, 1.75), fontsize=8.5,
                va='center', arrowprops=dict(arrowstyle='->', lw=0.8))
    ax.text(0.5, -0.16, u'(a) 弱掺杂', fontsize=9.5, ha='center', va='top',
            transform=ax.transAxes)

    # ---------- (b) 过掺杂
    ax = axs[1]
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1.0)
    ax.set_xticks([0, 200, 400, 600, 800, 1000])
    ax.set_xticklabels(['0', '200', '400', '600', '800', '1000'])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.tick_params(direction='in', length=3.5, labelsize=8.5)
    ax2 = ax.twinx()
    ax2.set_ylim(0, 4)
    ax2.set_yticks([0, 1, 2, 3, 4])
    ax2.tick_params(direction='in', length=3.5, labelsize=8.5)
    ax.set_xlabel(r'$T$/K', fontsize=10)
    ax.set_ylabel(r'$\rho_{\rm ab}$/(10$^{-5}$ $\Omega\cdot$m)', fontsize=9)
    ax2.set_ylabel(r'$\rho$/(10$^{-5}$ $\Omega\cdot$m)', fontsize=9,
                   rotation=270, labelpad=16)

    def curve2(pts, ls='-', lw_=1.4):
        f = PchipInterpolator([p[0] for p in pts], [p[1] for p in pts])
        xx = np.linspace(pts[0][0], pts[-1][0], 400)
        if ls == '--':
            ax.plot(xx, f(xx), 'k' + ls, lw=lw_, dashes=(4, 2.2))
        else:
            ax.plot(xx, f(xx), 'k' + ls, lw=lw_)

    curve2([(0, 0.07), (12, 0.15), (22, 0.20), (32, 0.215), (60, 0.29),
            (100, 0.375), (200, 0.53), (300, 0.66), (400, 0.82), (470, 1.0)])
    curve2([(0, 0.34), (25, 0.36), (40, 0.395), (200, 0.485), (400, 0.60),
            (600, 0.71), (800, 0.82), (1000, 0.925)])
    curve2([(0, 0.28), (40, 0.31), (400, 0.465), (1000, 0.762)])
    curve2([(0, 0.25), (400, 0.415), (1000, 0.688)])
    curve2([(0, 0.22), (400, 0.36), (1000, 0.60)])
    curve2([(0, 0.05), (200, 0.185), (400, 0.30), (600, 0.405), (750, 0.485),
            (850, 0.545)], ':', 1.6)
    curve2([(0, 0.155), (400, 0.28), (1000, 0.49)])
    curve2([(0, 0.14), (400, 0.25), (1000, 0.45)])
    curve2([(0, 0.12), (400, 0.215), (1000, 0.39)])
    curve2([(0, 0.06), (400, 0.17), (1000, 0.31)], ':', 1.6)
    curve2([(0, 0.09), (400, 0.165), (1000, 0.335)])
    ax.text(150, 0.87, 'x=0.1', fontsize=9)
    # 引线标注
    lab = [('0.15', 700, 0.945, 830, 0.895), ('0.18', 615, 0.85, 740, 0.775),
           ('0.2', 560, 0.78, 690, 0.70), ('0.22', 495, 0.71, 640, 0.615),
           ('0.25', 845, 0.305, 890, 0.465), ('0.275', 770, 0.25, 840, 0.43),
           ('0.3', 690, 0.205, 790, 0.375), ('0.34', 615, 0.15, 720, 0.32)]
    for s, xt, yt, xa_, ya_ in lab:
        ax.annotate(s, xy=(xa_, ya_), xytext=(xt, yt), fontsize=8.5,
                    va='center', ha='center',
                    arrowprops=dict(arrowstyle='-', lw=0.7))
    ax.text(0.5, -0.16, u'(b) 过掺杂', fontsize=9.5, ha='center', va='top',
            transform=ax.transAxes)
    fig.subplots_adjust(hspace=0.3)
    save(fig, '7-16')


# ================================================================ 图7.17
def fig_7_17():
    fig, ax = plt.subplots(figsize=(4.5, 3.4))
    plain_axes(ax)
    ax.set_xlim(-0.06, 1.16)
    ax.set_ylim(-0.14, 1.08)

    # 边框
    ax.plot([0, 1.05, 1.05, 0, 0], [1.0, 1.0, 0, 0, 1.0], 'k-', lw=1.0)
    arrow_axis(ax, 0, 0, 0, 1.06)
    ax.text(0.06, 1.045, u'温度', fontsize=9, ha='left', va='bottom')
    arrow_axis(ax, 0, 0, 1.11, 0, lw=0.9)
    ax.text(1.03, -0.055, u'空穴掺杂', fontsize=9, ha='center', va='top')
    # T* 线（正常能隙）
    xs = np.array([0.32, 0.40, 0.50, 0.60, 0.70, 0.78, 0.84, 0.875])
    ys = np.array([0.985, 0.88, 0.755, 0.625, 0.475, 0.33, 0.20, 0.135])
    from scipy.interpolate import PchipInterpolator
    f = PchipInterpolator(xs, ys)
    xx = np.linspace(0.32, 0.875, 300)
    ax.plot(xx, f(xx), 'k-.', lw=1.2, dashes=(7, 2, 1.5, 2))
    ax.text(0.78, 0.44, r'$T^*$', fontsize=10, ha='left', va='center')
    ang = -46
    ax.text(0.53, 0.66, u'正常能隙', fontsize=9, ha='center', va='center',
            rotation=ang, rotation_mode='anchor')
    # Tc 穹顶
    xd = np.array([0.28, 0.33, 0.40, 0.48, 0.56, 0.64, 0.72, 0.80, 0.86, 0.89])
    yd = np.array([0.06, 0.13, 0.22, 0.28, 0.30, 0.285, 0.245, 0.185, 0.125, 0.10])
    g = PchipInterpolator(xd, yd)
    xx = np.linspace(0.28, 0.89, 300)
    ax.plot(xx, g(xx), 'k-', lw=1.3)
    ax.text(0.585, 0.155, u'超导', fontsize=9, ha='center', va='center')
    ax.text(0.915, 0.20, r'$T_{\rm c}$', fontsize=9.5, ha='left', va='center')
    ax.annotate('', xy=(0.875, 0.145), xytext=(0.905, 0.19),
                arrowprops=dict(arrowstyle='->', lw=0.8))
    # 反铁磁线
    xa = np.array([0.28, 0.272, 0.262, 0.252, 0.245])
    ya = np.array([0.06, 0.30, 0.58, 0.82, 1.0])
    fa = PchipInterpolator(ya, xa)
    yy = np.linspace(0.06, 1.0, 200)
    ax.plot(fa(yy), yy, 'k-', lw=1.2)
    vtext(ax, 0.185, 0.52, u'反铁磁', fontsize=9)
    vtext(ax, 0.755, 0.75, u'最佳掺杂', fontsize=9)
    vtext(ax, 0.47, 0.38, u'弱掺杂', fontsize=9)
    vtext(ax, 0.965, 0.40, u'过掺杂', fontsize=9)
    save(fig, '7-17')


if __name__ == '__main__':
    import sys
    names = ['6-13', '6-14', '6-15', '6-16', '6-17', '6-18', '6-19', '6-20',
             '6-21', '6-22', '6-23', '7-1', '7-2', '7-3', '7-4', '7-5',
             '7-6', '7-7', '7-8', '7-9', '7-10', '7-11', '7-12', '7-13',
             '7-14', '7-15', '7-16', '7-17']
    only = sys.argv[1:] or names
    for n in only:
        globals()['fig_' + n.replace('-', '_')]()
        print(f'fig{n} done')
