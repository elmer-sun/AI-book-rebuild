# -*- coding: utf-8 -*-
"""
李正中《固体理论》（第2版）中文重排本 插图重绘 第二批：
第四章 图4.1-4.10、第五章 图5.1-5.7、第六章 图6.1-6.12，共 29 幅。
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p-111/112/126/127/131/132/155/156/159/160/163/164/
173/174/180/183/190/193/194/195/196/200/207）。
注：图4.2 无裁剪图，以 p-112 页面为准；图4.2 纵轴截距原书印作 ω_r（疑为 ω_p 误排），
    本图按正文与图4.5 一致取 ω_p。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Rectangle, Wedge, Polygon, FancyArrowPatch
from matplotlib.path import Path
import matplotlib.patches as mpatches
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
    'hatch.linewidth': 0.55,
})

BASE = r"E:\AI整理书籍\李正中\重排本"
FIGD = os.path.join(BASE, 'figures')
PRED = os.path.join(FIGD, 'preview')
os.makedirs(PRED, exist_ok=True)

LW_MAIN, LW_AUX = 1.2, 0.8


def save(fig, name):
    fig.savefig(os.path.join(FIGD, name + '.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRED, name + '.png'), bbox_inches='tight',
                pad_inches=0.03, dpi=220)
    plt.close(fig)


def arrow_axis(ax, x0, y0, x1, y1, lw=LW_MAIN):
    """带箭头的坐标轴（自绘）"""
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=12))


def plain_axes(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def vec(ax, x0, y0, x1, y1, lw=LW_MAIN, ms=11, ls='-'):
    """实线箭头"""
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw, ls=ls,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def dot(ax, x, y, ms=4.5, open=False):
    if open:
        ax.plot([x], [y], 'o', ms=ms, mfc='white', mec='k', mew=1.0)
    else:
        ax.plot([x], [y], 'ko', ms=ms)


def tick(ax, x, y, dx, dy, label=None, lx=0.0, ly=0.0, fs=8.5, ha='center',
         va='center', lw=0.9):
    """小刻度线 + 标注"""
    ax.plot([x, x + dx], [y, y + dy], 'k-', lw=lw)
    if label is not None:
        ax.text(x + dx + lx, y + dy + ly, label, fontsize=fs, ha=ha, va=va)


def wavy(ax, x0, y0, x1, y1, n=6, amp=None, lw=1.0):
    """声子波浪线（直线段）"""
    x0, y0, x1, y1 = map(float, (x0, y0, x1, y1))
    L = np.hypot(x1 - x0, y1 - y0)
    if amp is None:
        amp = 0.30 * L / n
    t = np.linspace(0, 1, 240)
    xs = x0 + (x1 - x0) * t
    ys = y0 + (y1 - y0) * t
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    px, py = -uy, ux
    off = amp * np.sin(2 * np.pi * n * t)
    ax.plot(xs + px * off, ys + py * off, 'k-', lw=lw)


def wavy_arc(ax, cx, cy, r, a0, a1, n=6, amp=0.035, lw=1.0, arrow_at=None):
    """声子波浪弧（角度制 a0->a1，度）"""
    t = np.linspace(0, 1, 400)
    ang = np.deg2rad(a0 + (a1 - a0) * t)
    rr = r + amp * np.sin(2 * np.pi * n * t)
    ax.plot(cx + rr * np.cos(ang), cy + rr * np.sin(ang), 'k-', lw=lw)
    if arrow_at is not None:  # arrow_at: ('end'|'start')
        if arrow_at == 'end':
            a_a, a_b = np.deg2rad(a1), np.deg2rad(a1 - (a1 - a0) * 0.06)
        else:
            a_a, a_b = np.deg2rad(a0), np.deg2rad(a0 + (a1 - a0) * 0.06)
        p_a = (cx + (r + amp) * np.cos(a_a), cy + (r + amp) * np.sin(a_a))
        p_b = (cx + r * np.cos(a_b), cy + r * np.sin(a_b))
        vec(ax, p_b[0], p_b[1], p_a[0], p_a[1], lw=lw, ms=9)


def thick_arrow(ax, x0, y0, x1, y1, lw=3.6, ms=26):
    """粗黑速度箭头（图5.5）"""
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def brace(ax, x, y0, y1, w, lw=1.0):
    """竖放大括号 }（尖朝右），从 y0 到 y1"""
    h = y1 - y0
    verts = [(x, y0), (x + w, y0 + 0.10 * h), (x + 0.62 * w, y0 + 0.32 * h),
             (x + 1.05 * w, y0 + 0.50 * h),
             (x + 0.62 * w, y0 + 0.68 * h), (x + w, y1 - 0.10 * h), (x, y1)]
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3,
             Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3]
    # CURVE3 需要成对（控制点,端点），重排:
    verts = [(x, y0),
             (x + w, y0 + 0.08 * h), (x + 0.66 * w, y0 + 0.30 * h),
             (x + 1.05 * w, y0 + 0.50 * h),
             (x + 0.66 * w, y0 + 0.70 * h), (x + w, y1 - 0.08 * h), (x, y1)]
    codes = [Path.MOVETO] + [Path.CURVE3] * 6
    ax.add_patch(mpatches.PathPatch(Path(verts, codes), fill=False, lw=lw,
                                    edgecolor='k'))


# ================================================================ 第四章
def fig_4_1():
    """费密球位移 q 的允许激发区：(a) q<2k_F 两球交叠 (b) q>2k_F 两球分离"""
    fig, axs = plt.subplots(1, 2, figsize=(5.5, 2.15))
    for ax in axs:
        plain_axes(ax)
        ax.set_aspect('equal')

    # ---------- (a)
    ax = axs[0]
    ax.set_xlim(-1.45, 1.75)
    ax.set_ylim(-1.30, 1.42)
    c1 = (0.0, 0.0); r1 = 1.0
    c2 = (0.44, 0.14); r2 = 0.90
    ax.add_patch(Circle(c2, r2, facecolor='white', edgecolor='k', lw=1.25,
                        hatch='/////////'))
    ax.add_patch(Circle(c1, r1, facecolor='none', edgecolor='k', lw=1.4))
    # 中心虚线 k_F + 箭头 q（终点落在电子激发弯月内）
    u = np.array([0.912, 0.410])
    ax.plot([0, 1.0 * u[0]], [0, 1.0 * u[1]], 'k--', lw=0.9, dashes=(4, 2.4))
    vec(ax, 1.0 * u[0], 1.0 * u[1], 1.30 * u[0], 1.30 * u[1], lw=1.1, ms=10)
    ax.text(1.38 * u[0] - 0.02, 1.30 * u[1] - 0.22, r'$\boldsymbol{q}$',
            fontsize=10, ha='center', va='center')
    ax.text(0.47, 0.13, r'$\boldsymbol{k}_{\rm F}$', fontsize=9.5,
            ha='left', va='center')
    # 顶部小箭头 + q（球位移方向）
    p0 = (-0.36, 0.845)
    d = np.array([0.95, 0.31]) / np.hypot(0.95, 0.31)
    vec(ax, p0[0], p0[1], p0[0] + 0.26 * d[0], p0[1] + 0.26 * d[1],
        lw=1.0, ms=8)
    ax.text(-0.50, 1.02, r'$\boldsymbol{q}$', fontsize=10, ha='center',
            va='center')

    # ---------- (b)
    ax = axs[1]
    ax.set_xlim(-1.35, 3.45)
    ax.set_ylim(-1.45, 2.05)
    ax.add_patch(Circle((0, 0), 1.0, facecolor='white', edgecolor='k',
                        lw=1.25, hatch='/////////'))
    ax.add_patch(Circle((2.10, 0.95), 0.97, facecolor='white', edgecolor='k',
                        lw=1.25, hatch='/////////'))
    vec(ax, 0, 0, 2.10, 0.95, lw=1.2, ms=11)
    ax.text(1.02, 0.62, r'$\boldsymbol{q}$', fontsize=10, ha='center',
            va='center')
    v = np.array([0.945, -0.327])
    ax.plot([0, 0.97 * v[0]], [0, 0.97 * v[1]], 'k--', lw=0.9, dashes=(4, 2.4))
    vec(ax, 0.80 * v[0], 0.80 * v[1], 0.97 * v[0], 0.97 * v[1], lw=1.0, ms=9)
    ax.text(1.02 * v[0] + 0.06, 1.02 * v[1] - 0.10, r'$\boldsymbol{k}_{\rm F}$',
            fontsize=9.5, ha='left', va='center')
    save(fig, 'fig4-1')


def fig_4_2():
    """等离激元色散与对激发区（p112，manifest 无裁剪图）"""
    fig, ax = plt.subplots(figsize=(3.5, 2.62))
    plain_axes(ax)
    ax.set_xlim(-0.16, 2.06)
    ax.set_ylim(-0.30, 2.86)
    xmax, ytop = 1.92, 2.60

    # 对激发区阴影
    poly = Polygon([(0, 0), (0.76, ytop), (1.83, 2.30), (1.0, 0)],
                   closed=True, facecolor='white', edgecolor='k', lw=0.0,
                   hatch='////////')
    ax.add_patch(poly)
    # 边界曲线
    xx = np.linspace(0, 0.76, 100)
    ax.plot(xx, ytop / 0.76 * xx, 'k-', lw=1.5)                    # omega_max
    xx = np.linspace(1.0, 1.83, 100)
    ax.plot(xx, 2.30 / 0.83 * (xx - 1.0), 'k-', lw=1.5)            # omega_min
    ax.plot([0.76, 1.83], [ytop, 2.30], 'k-', lw=0.0)              # (顶部连线随多边形)
    # 等离激元色散
    xx = np.linspace(0, 0.34, 100)
    ax.plot(xx, 1.04 + 0.82 * xx ** 2, 'k-', lw=1.5)
    # q_c 虚线
    ax.plot([0.34, 0.34], [0, 1.135], 'k--', lw=0.9, dashes=(4, 2.4))
    # 坐标轴
    arrow_axis(ax, 0, 0, 0, 2.74)
    arrow_axis(ax, 0, 0, xmax, 0)
    ax.text(-0.10, 2.66, r'$\omega$', fontsize=11, ha='center', va='center')
    ax.text(xmax - 0.03, 0.10, r'$q$', fontsize=11, ha='center', va='center')
    # 标注
    ax.text(0.16, 1.62, r'$\omega_q$', fontsize=10, ha='center', va='center')
    ax.plot([0.155, 0.205], [1.52, 1.27], 'k-', lw=0.8)
    # 原书此处印作 omega_r，按正文与图4.5 应为 omega_p
    ax.text(-0.055, 1.04, r'$\omega_{\rm p}$', fontsize=10, ha='right',
            va='center')
    ax.text(0.44, 2.16, r'$\omega_{kq}^{\rm max}$', fontsize=9.5,
            ha='center', va='center')
    ax.text(1.70, 1.76, r'$\omega_{kq}^{\rm min}$', fontsize=9.5,
            ha='left', va='center')
    for ch, xc, yc in (('对', 1.26, 1.94), ('激', 1.04, 1.44),
                       ('发', 0.82, 0.94), ('区', 0.60, 0.44)):
        ax.text(xc, yc, ch, fontsize=9.5, ha='center', va='center',
                bbox=dict(facecolor='white', edgecolor='none', pad=1.2))
    ax.text(0.34, -0.16, r'$q_{\rm c}$', fontsize=10, ha='center', va='center')
    ax.text(1.0, -0.16, r'$2k_{\rm F}$', fontsize=10, ha='center', va='center')
    save(fig, 'fig4-2')


def fig_4_3():
    """确定 q 值时电子系统的元激发 (q<2k_F)：F(w) 与直线 1=F(w) 的交点"""
    fig, ax = plt.subplots(figsize=(6.2, 2.85))
    plain_axes(ax)
    ax.set_xlim(-0.10, 1.10)
    ax.set_ylim(-1.18, 1.92)

    F1 = 0.95
    ytop, ybot = 1.55, -0.92
    xd = [0.155, 0.275, 0.395, 0.515, 0.665]
    # 水平直线 F=1
    ax.plot([0, 0.905], [F1, F1], 'k-', lw=1.0)
    # 虚竖线（共振边界）与轴上结点
    for x in xd:
        ax.plot([x, x], [ybot, ytop], 'k--', lw=0.9, dashes=(4, 2.6))
        dot(ax, x, 0, ms=4.2)
    # 左端自 O 出发的下降支
    xx = np.linspace(0.002, xd[0] - 0.012, 200)
    ax.plot(xx, -0.90 * (xx / xd[0]) ** 2.0, 'k-', lw=1.4)
    # 各支（相邻虚线间的陡降曲线）
    for xa, xb in zip(xd[:-1], xd[1:]):
        u = np.linspace(0.045, 0.955, 200)
        xs = xa + (xb - xa) * u
        ys = ytop - (ytop - ybot) * (1 + np.tanh(9 * (u - 0.35))) / 2
        ax.plot(xs, ys, 'k-', lw=1.4)
        # 与 F=1 直线的交点
        i = np.argmin(np.abs(ys - F1))
        dot(ax, xs[i], F1, ms=4.2)
    # 等离激元支
    xp = [0.675, 0.71, 0.75, 0.80, 0.86, 0.92, 0.955]
    yp = [1.50, 1.30, 1.10, 0.95, 0.72, 0.54, 0.44]
    f = PchipInterpolator(xp, yp)
    xx = np.linspace(0.672, 0.955, 200)
    ax.plot(xx, f(xx), 'k-', lw=1.4)
    dot(ax, 0.80, F1, ms=4.2)
    ax.plot([0.80, 0.80], [F1, 0], 'k--', lw=0.9, dashes=(4, 2.6))
    # 坐标轴
    arrow_axis(ax, 0, -1.0, 0, 1.80)
    arrow_axis(ax, 0, 0, 1.06, 0)
    ax.text(-0.055, 1.72, r'$F(\omega)$', fontsize=10, ha='center',
            va='center')
    ax.text(1.045, -0.09, r'$\omega$', fontsize=11, ha='center', va='center')
    ax.text(-0.028, -0.075, r'$O$', fontsize=10, ha='right', va='center')
    # 标注
    ax.text(0.075, -0.26, r'$\omega_{kq}^{\rm min}$', fontsize=9.5,
            ha='center', va='center')
    ax.text(0.735, -0.24, r'$\omega_{kq}^{\rm max}$', fontsize=9.5,
            ha='left', va='center')
    ax.text(0.80, -0.24, r'$\omega_{\rm p}$', fontsize=9.5, ha='center',
            va='top')
    ax.text(0.88, 1.30, '等离激元', fontsize=9.5, ha='left', va='center')
    ax.text(0.40, 1.76, '电子-空穴对个别激发', fontsize=9.5, ha='center',
            va='center')
    # omega_kq 折线引导
    ax.text(0.335, -0.30, r'$\omega_{kq}$', fontsize=9.5, ha='center',
            va='center')
    ax.plot([0.365, 0.415, 0.385, 0.435, 0.40], [-0.235, -0.16, -0.115,
            -0.045, 0.0], 'k-', lw=0.8)
    save(fig, 'fig4-3')


def fig_4_4():
    """电子-空穴对激发：费密球内 k 态电子激发到 k+q"""
    fig, ax = plt.subplots(figsize=(2.9, 2.6))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-1.35, 2.10)
    ax.set_ylim(-1.30, 1.55)
    ax.add_patch(Circle((0, 0), 1.0, facecolor='none', edgecolor='k', lw=1.4))
    vec(ax, 0, 0, -0.766, 0.643, lw=1.2, ms=10)      # k_F 箭头（至球面）
    dot(ax, 0, 0, ms=4.5)
    dot(ax, 0.47, 0.52, ms=5, open=True)             # k（空心）
    vec(ax, 0.47, 0.52, 1.53, 1.20, lw=1.2, ms=10)   # q
    dot(ax, 1.53, 1.20, ms=4.5)
    ax.text(-0.42, 0.22, r'$\boldsymbol{k}_{\rm F}$', fontsize=10,
            ha='center', va='center')
    ax.text(0.30, 0.42, r'$\boldsymbol{k}$', fontsize=10, ha='right',
            va='center')
    ax.text(1.62, 1.24, r'$\boldsymbol{k+q}$', fontsize=10, ha='left',
            va='center')
    save(fig, 'fig4-4')


def fig_4_5():
    """图4.5：同图4.2，注明各区域的 eps2"""
    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    plain_axes(ax)
    ax.set_xlim(-0.18, 2.10)
    ax.set_ylim(-0.32, 2.86)

    # omega_kq^max 支（自 O 微上凹）
    s = np.linspace(0, 1, 100)
    xa, ya = 0.836, 2.60
    ax.plot(xa * s, ya * s ** 1.22, 'k-', lw=1.5)
    # omega_kq^min 支（自 2k_F）
    s = np.linspace(0, 1, 100)
    ax.plot(1.0 + 0.909 * s, 2.60 * s ** 1.18, 'k-', lw=1.5)
    # 等离激元（虚线）及 q_c
    xx = np.linspace(0, 0.502, 100)
    ax.plot(xx, 1.083 + 0.104 * (xx / 0.502) ** 2 * 1.0, 'k--', lw=1.0,
            dashes=(4, 2.4))
    ax.plot([0.502, 0.502], [0, 1.344], 'k--', lw=1.0, dashes=(4, 2.4))
    # 支上的方向箭头
    ax.annotate('', xy=(0.552, 1.50), xytext=(0.60, 1.72),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.1,
                                shrinkA=0, shrinkB=0, mutation_scale=11))
    ax.annotate('', xy=(1.325, 0.70), xytext=(1.27, 0.50),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.1,
                                shrinkA=0, shrinkB=0, mutation_scale=11))
    # 坐标轴
    arrow_axis(ax, 0, 0, 0, 2.74)
    arrow_axis(ax, 0, 0, 2.02, 0)
    ax.text(-0.09, 2.64, r'$\omega$', fontsize=11, ha='center', va='center')
    ax.text(1.99, 0.10, r'$q$', fontsize=11, ha='center', va='center')
    ax.text(-0.03, -0.06, r'$O$', fontsize=10, ha='right', va='top')
    ax.text(-0.055, 1.083, r'$\omega_{\rm p}$', fontsize=10, ha='right',
            va='center')
    ax.text(0.502, -0.17, r'$q_{\rm c}$', fontsize=10, ha='center',
            va='center')
    ax.text(1.0, -0.17, r'$2k_{\rm F}$', fontsize=10, ha='center',
            va='center')
    ax.text(0.145, 2.24, '集体激发', fontsize=9.5, ha='center', va='center')
    ax.text(0.185, 1.94, r'Im $\varepsilon$=0', fontsize=9.5, ha='center',
            va='center')
    ax.text(1.02, 1.90, r'Im $\varepsilon\neq$0 区', fontsize=9.5,
            ha='center', va='center')
    ax.text(1.06, 1.60, '个别激发', fontsize=9.5, ha='center', va='center')
    save(fig, 'fig4-5')


def fig_4_6():
    """屏蔽参数 lambda^2 S 随 q 的变化（2k_F 处奇性）"""
    fig, ax = plt.subplots(figsize=(3.1, 2.1))
    plain_axes(ax)
    ax.set_xlim(-0.10, 2.42)
    ax.set_ylim(-0.14, 1.22)

    def S(x):
        x = np.asarray(x, dtype=float)
        y = np.empty_like(x)
        m = np.abs(x - 1.0) > 1e-6
        xm = x[m]
        y[m] = 0.5 * (1 + (1 - xm ** 2) / (2 * xm) *
                      np.log(np.abs((1 + xm) / (1 - xm))))
        y[~m] = 0.5
        return y

    xs = np.concatenate([np.linspace(0.0, 0.97, 500),
                         np.linspace(1.03, 2.15, 500)])
    xs = np.insert(xs, 500, 1.0)
    ax.plot(xs, S(xs), 'k-', lw=1.6)
    ax.plot([1, 1], [0, 0.5], 'k--', lw=0.9, dashes=(4, 2.4))
    arrow_axis(ax, 0, 0, 0, 1.12)
    arrow_axis(ax, 0, 0, 2.32, 0)
    ax.text(-0.06, 1.06, r'$\lambda^2S$', fontsize=10, ha='center',
            va='center')
    ax.text(-0.045, 1.0, r'$\lambda^2$', fontsize=9.5, ha='right',
            va='center')
    ax.text(2.30, -0.08, r'$q/2k_{\rm F}$', fontsize=9.5, ha='center',
            va='center')
    ax.text(-0.025, -0.075, r'$0$', fontsize=9, ha='right', va='center')
    ax.text(1.0, -0.075, r'$1$', fontsize=9, ha='center', va='center')
    save(fig, 'fig4-6')


def fig_4_7():
    """一维系中电子与声子谱的共振特征（I 对激发区, II 空隙区, III 声子色散）"""
    fig, ax = plt.subplots(figsize=(3.7, 2.7))
    plain_axes(ax)
    ax.set_xlim(-0.28, 3.86)
    ax.set_ylim(-0.55, 6.45)

    xx = np.linspace(0, 1.55, 200)
    ax.plot(xx, xx ** 2 + 2 * xx, 'k-', lw=1.4)               # omega_max
    xx = np.linspace(0, 2.0, 200)
    ax.plot(xx, 2 * xx - xx ** 2, 'k-', lw=1.4)               # 弧（下界）
    xx = np.linspace(2.0, 3.30, 200)
    ax.plot(xx, xx ** 2 - 2 * xx, 'k-', lw=1.4)               # omega_min
    xx = np.linspace(0, 3.50, 50)
    ax.plot(xx, 0.31 * xx, 'k--', lw=1.0, dashes=(6, 3))      # 声子色散
    arrow_axis(ax, 0, 0, 0, 6.15)
    arrow_axis(ax, 0, 0, 3.72, 0)
    ax.text(-0.13, 6.02, r'$\omega$', fontsize=11, ha='center', va='center')
    ax.text(3.66, -0.14, r'$q$', fontsize=11, ha='center', va='center')
    ax.text(-0.075, -0.13, r'$O$', fontsize=10, ha='right', va='top')
    ax.text(2.0, -0.38, r'$2k_{\rm F}$', fontsize=10, ha='center',
            va='center')
    ax.text(2.22, 4.70, r'(Ⅰ)', fontsize=10, ha='center', va='center')
    ax.text(1.34, 2.78, r'(Ⅱ)', fontsize=10, ha='center', va='center')
    ax.text(3.44, 1.22, r'(Ⅲ)', fontsize=10, ha='left', va='center')
    save(fig, 'fig4-7')


def fig_4_8():
    """(a) 夫里德耳振荡势（虚线）；(b) 汤川势（实线）"""
    fig, ax = plt.subplots(figsize=(3.4, 2.85))
    plain_axes(ax)
    ax.set_xlim(-0.55, 3.95)
    ax.set_ylim(-2.35, 6.35)
    arrow_axis(ax, 0, -2.0, 0, 6.05)
    arrow_axis(ax, 0, 0, 3.80, 0)
    ax.text(-0.30, 5.85, r'$V(r)$', fontsize=10, ha='center', va='center')
    ax.text(3.72, -0.28, r'$r$', fontsize=11, ha='center', va='center')
    # (b) 汤川势（实线）
    yb = [5.3, 4.15, 3.05, 2.05, 1.45, 1.05, 0.78, 0.55, 0.32, 0.15, 0.06]
    xb = [0.06, 0.30, 0.55, 0.82, 1.15, 1.50, 1.85, 2.20, 2.60, 2.90, 3.10]
    fb = PchipInterpolator(xb, yb)
    xx = np.linspace(0.06, 3.10, 400)
    ax.plot(xx, fb(xx), 'k-', lw=1.5)
    # (a) 夫里德耳振荡（虚线）
    xa = [0.06, 0.45, 0.82, 1.00, 1.17, 1.32, 1.47, 1.58, 1.70, 1.82, 1.93,
          2.04, 2.15, 2.30, 2.42, 2.52, 2.64, 2.78, 2.90, 3.05]
    ya = [5.3, 2.60, 0.0, -0.95, -1.55, -1.05, 0.0, 0.55, 0.90, 0.55, 0.0,
          -0.40, -0.62, -0.35, 0.0, 0.30, 0.42, 0.20, 0.0, 0.12]
    fa = PchipInterpolator(xa, ya)
    xx = np.linspace(0.06, 3.05, 500)
    ax.plot(xx, fa(xx), 'k--', lw=1.0, dashes=(5, 2.6))
    ax.text(1.00, 1.55, r'(b)', fontsize=10, ha='center', va='center')
    ax.text(0.72, -1.05, r'(a)', fontsize=10, ha='center', va='center')
    save(fig, 'fig4-8')


def fig_4_9():
    """谱函数示意图：尖峰（准粒子）+ 平滑背景 A1"""
    fig, ax = plt.subplots(figsize=(5.8, 3.85))
    plain_axes(ax)
    ax.set_xlim(-0.10, 1.14)
    ax.set_ylim(-0.09, 0.665)
    W, H = 1.0, 0.55
    ax.add_patch(Rectangle((0, 0), W, H, facecolor='none', edgecolor='k',
                           lw=1.0))
    arrow_axis(ax, 0, 0, 0, H + 0.045, lw=1.0)
    arrow_axis(ax, 0, 0, W + 0.045, 0, lw=1.0)
    x = np.linspace(0.001, W, 1200)
    bg = 0.030 + 0.011 * np.sin(2 * np.pi * 2.2 * x + 2.6) + \
        0.007 * np.sin(2 * np.pi * 4.6 * x + 0.5)
    pk = 0.46 * 0.006 ** 2 / ((x - 0.66) ** 2 + 0.006 ** 2)
    ax.plot(x, np.clip(bg + pk, 0, None), 'k-', lw=1.2)
    ax.text(0.018, 0.615, r'$A(k,\omega)$', fontsize=10, ha='left',
            va='center')
    ax.text(W + 0.062, -0.022, r'$\omega$', fontsize=11, ha='center',
            va='center')
    ax.text(-0.022, -0.028, r'$O$', fontsize=10, ha='right', va='center')
    save(fig, 'fig4-9')


def fig_4_10():
    """相互作用电子系中占据数的动量分布：实线（互作用），虚线（零温费密分布）"""
    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    plain_axes(ax)
    ax.set_xlim(-0.14, 1.98)
    ax.set_ylim(-0.16, 1.34)
    # 虚线：零温阶跃
    ax.plot([0, 1.0], [1, 1], 'k--', lw=1.0, dashes=(5, 2.6))
    ax.plot([1.0, 1.0], [1, 0], 'k--', lw=1.0, dashes=(5, 2.6))
    # 实线：相互作用占据数（k_F 处断成两支，上下连续段）
    xs1 = [0.0, 0.30, 0.60, 0.80, 0.92, 1.0]
    ys1 = [0.985, 0.975, 0.955, 0.925, 0.885, 0.82]
    xs2 = [1.0, 1.06, 1.15, 1.30, 1.50, 1.68, 1.82]
    ys2 = [0.26, 0.20, 0.135, 0.068, 0.024, 0.007, 0.002]
    f1 = PchipInterpolator(xs1, ys1)
    f2 = PchipInterpolator(xs2, ys2)
    xx1 = np.linspace(0, 1.0, 200)
    ax.plot(xx1, f1(xx1), 'k-', lw=1.5)
    xx2 = np.linspace(1.0, 1.72, 200)
    ax.plot(xx2, f2(xx2), 'k-', lw=1.5)
    arrow_axis(ax, 0, 0, 0, 1.26)
    arrow_axis(ax, 0, 0, 1.88, 0)
    ax.text(-0.055, 1.20, r'$n_{k\sigma}$', fontsize=10, ha='center',
            va='center')
    ax.text(1.86, -0.10, r'$k$', fontsize=11, ha='center', va='center')
    ax.text(-0.04, -0.06, r'$O$', fontsize=10, ha='right', va='center')
    ax.text(-0.045, 1.0, r'$1$', fontsize=9, ha='right', va='center')
    ax.plot([0, 0.02], [1, 1], 'k-', lw=0.9)
    ax.text(1.0, -0.095, r'$k_{\rm F}$', fontsize=9.5, ha='center',
            va='center')
    ax.plot([1.0, 1.0], [-0.03, 0], 'k-', lw=0.9)
    ax.text(1.055, 0.56, r'$Z_k$', fontsize=10, ha='left', va='center')
    save(fig, 'fig4-10')


# ================================================================ 第五章
def fig_5_1():
    """电子-声子互作用的一级过程：(a) 声子吸收 (b) 声子发射"""
    fig, axs = plt.subplots(1, 2, figsize=(4.7, 2.05))
    for ax in axs:
        plain_axes(ax)
        ax.set_aspect('equal')

    # (a)
    ax = axs[0]
    ax.set_xlim(-1.10, 1.15)
    ax.set_ylim(-1.15, 1.65)
    vec(ax, -0.62, -0.92, 0, 0, lw=1.3)
    wavy(ax, 0.70, -0.92, 0, 0, n=5, lw=1.1)
    vec(ax, 0.135, -0.185, 0.03, -0.045, lw=1.1, ms=9)   # 声子箭头（指向顶点，吸收）
    vec(ax, 0, 0, 0, 1.30, lw=1.3)
    ax.text(-0.50, -0.48, r'$\boldsymbol{k}$', fontsize=10, ha='center',
            va='center')
    ax.text(0.44, -0.50, r'$\boldsymbol{q}$', fontsize=10, ha='center',
            va='center')
    ax.text(0.10, 1.10, r'$\boldsymbol{k+q}$', fontsize=10, ha='left',
            va='center')

    # (b)
    ax = axs[1]
    ax.set_xlim(-1.15, 1.25)
    ax.set_ylim(-1.55, 1.35)
    vec(ax, 0, -1.25, 0, 0, lw=1.3)
    vec(ax, 0, 0, -0.70, 0.92, lw=1.3)
    wavy(ax, 0, 0, 0.70, 0.92, n=4, lw=1.1)
    vec(ax, 0.60, 0.79, 0.70, 0.92, lw=1.1, ms=9)        # 声子箭头（发射，指离顶点）
    ax.text(0.11, -0.62, r'$\boldsymbol{k}$', fontsize=10, ha='left',
            va='center')
    ax.text(-0.92, 0.70, r'$\boldsymbol{k-q}$', fontsize=10, ha='center',
            va='center')
    ax.text(0.86, 0.55, r'$\boldsymbol{q}$', fontsize=10, ha='left',
            va='center')
    save(fig, 'fig5-1')


def fig_5_2():
    """电子-空穴对的产生与复合（箭头朝上=电子，朝下=空穴）"""
    fig, axs = plt.subplots(1, 2, figsize=(4.9, 2.1))
    for ax in axs:
        plain_axes(ax)
        ax.set_aspect('equal')

    # (a) 电子-空穴对复合发射声子
    ax = axs[0]
    ax.set_xlim(-1.25, 1.30)
    ax.set_ylim(-1.30, 1.70)
    vec(ax, -0.85, -0.72, 0, 0, lw=1.3)            # 电子 k（入射）
    vec(ax, 0, 0, 0.85, -0.78, lw=1.3)             # 空穴 k-q（离顶点向下）
    wavy(ax, 0, 0, 0, 1.38, n=5, lw=1.1)
    vec(ax, 0, 1.22, 0, 1.38, lw=1.1, ms=9)        # 声子箭头（向上发射）
    ax.text(-0.62, -0.36, r'$\boldsymbol{k}$', fontsize=10, ha='center',
            va='center')
    ax.text(0.62, -0.40, r'$\boldsymbol{k-q}$', fontsize=10, ha='center',
            va='center')
    ax.text(0.11, 0.72, r'$\boldsymbol{q}$', fontsize=10, ha='left',
            va='center')

    # (b) 吸收声子产生电子-空穴对
    ax = axs[1]
    ax.set_xlim(-1.20, 1.30)
    ax.set_ylim(-1.60, 1.45)
    wavy(ax, 0, -1.30, 0, 0, n=5, lw=1.1)          # 声子入射
    vec(ax, 0, -1.16, 0, -1.30, lw=1.1, ms=9)      # 声子箭头（朝下，指离顶点）
    vec(ax, 0, 0, -0.70, 0.92, lw=1.3)             # 电子 k+q（离开顶点）
    vec(ax, 0.70, 0.92, 0, 0, lw=1.3)              # 空穴 k（箭头指向顶点）
    ax.text(0.11, -0.65, r'$\boldsymbol{q}$', fontsize=10, ha='left',
            va='center')
    ax.text(-0.92, 0.70, r'$\boldsymbol{k+q}$', fontsize=10, ha='center',
            va='center')
    ax.text(0.62, 0.75, r'$\boldsymbol{k}$', fontsize=10, ha='left',
            va='center')
    save(fig, 'fig5-2')


def fig_5_3():
    """二级过程：(a) 电子自能修正 (b) 声子自能修正 (c) 电子-声子-电子互作用"""
    fig, axs = plt.subplots(1, 3, figsize=(6.3, 2.2),
                            gridspec_kw=dict(width_ratios=[1, 1, 1.45],
                                             wspace=0.05))
    for ax in axs:
        plain_axes(ax)
        ax.set_aspect('equal')

    # ---- (a)
    ax = axs[0]
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-0.80, 2.42)
    cx, cy, r = 0, 0.75, 0.55
    # 左侧实弧（费米子线 k-q，自底结点绕行至顶结点）
    th = np.linspace(270, 90, 120)
    ax.plot(cx + r * np.cos(np.deg2rad(th)),
            cy + r * np.sin(np.deg2rad(th)), 'k-', lw=1.2)
    # 右侧声子波浪弧（自底至顶，箭头指入顶结点）
    wavy_arc(ax, cx, cy, r, -90, 90, n=4, amp=0.035, lw=1.1, arrow_at='end')
    # 左弧箭头（近顶端，顺绕行方向指向顶结点）
    p1 = (cx + r * np.cos(np.deg2rad(100)), cy + r * np.sin(np.deg2rad(100)))
    p0 = (cx + r * np.cos(np.deg2rad(118)), cy + r * np.sin(np.deg2rad(118)))
    vec(ax, p0[0], p0[1], p1[0], p1[1], lw=1.1, ms=9)
    vec(ax, 0, -0.52, 0, 0.20, lw=1.3)             # 入射电子 k（箭头指入底结点）
    vec(ax, 0, 1.30, 0, 2.10, lw=1.3)              # 出射电子 k
    ax.text(0.10, -0.30, r'$\boldsymbol{k}$', fontsize=10, ha='left',
            va='center')
    ax.text(0.10, 1.66, r'$\boldsymbol{k}$', fontsize=10, ha='left',
            va='center')
    ax.text(-0.72, 0.75, r'$\boldsymbol{k-q}$', fontsize=10, ha='center',
            va='center')
    ax.text(0.72, 0.72, r'$\boldsymbol{q}$', fontsize=10, ha='center',
            va='center')

    # ---- (b)
    ax = axs[1]
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.55, 2.75)
    cx, cy, r = 0, 0.75, 0.55
    ax.plot(np.cos(np.deg2rad(np.linspace(95, 265, 100))) * r + cx,
            cy + np.sin(np.deg2rad(np.linspace(95, 265, 100))) * r, 'k-',
            lw=1.2)                                 # 左弧
    ax.plot(np.cos(np.deg2rad(np.linspace(-85, 85, 100))) * r + cx,
            cy + np.sin(np.deg2rad(np.linspace(-85, 85, 100))) * r, 'k-',
            lw=1.2)                                 # 右弧
    # 左弧箭头（近底端，指向底结点）
    aa = np.deg2rad(248)
    p1 = (cx + r * np.cos(aa), cy + r * np.sin(aa))
    p0 = (cx + r * np.cos(np.deg2rad(230)), cy + r * np.sin(np.deg2rad(230)))
    vec(ax, p0[0], p0[1], p1[0], p1[1], lw=1.1, ms=9)
    # 右弧箭头（近顶端，指向顶结点）
    aa = np.deg2rad(72)
    p1 = (cx + r * np.cos(aa), cy + r * np.sin(aa))
    p0 = (cx + r * np.cos(np.deg2rad(55)), cy + r * np.sin(np.deg2rad(55)))
    vec(ax, p0[0], p0[1], p1[0], p1[1], lw=1.1, ms=9)
    wavy(ax, 0, -1.50, 0, 0.20, n=4, lw=1.1)        # 底部声子
    wavy(ax, 0, 1.30, 0, 2.55, n=4, lw=1.1)
    vec(ax, 0, 2.38, 0, 2.55, lw=1.1, ms=9)
    ax.text(0.11, -1.15, r'$\boldsymbol{q}$', fontsize=10, ha='left',
            va='center')
    ax.text(0.11, 2.15, r'$\boldsymbol{q}$', fontsize=10, ha='left',
            va='center')
    ax.text(-0.72, 0.75, r'$\boldsymbol{k}$', fontsize=10, ha='center',
            va='center')
    ax.text(0.72, 0.75, r'$\boldsymbol{k+q}$', fontsize=10, ha='center',
            va='center')

    # ---- (c)
    ax = axs[2]
    ax.set_xlim(-1.05, 3.35)
    ax.set_ylim(-1.15, 1.45)
    wavy(ax, 1.95, 0, 0, 0, n=6, lw=1.1)
    vec(ax, 0.22, 0, 0, 0, lw=1.1, ms=9)           # 声子箭头（向左）
    vec(ax, -0.60, -0.85, 0, 0, lw=1.3)
    vec(ax, 0, 0, -0.55, 0.85, lw=1.3)
    vec(ax, 2.55, -0.85, 1.95, 0, lw=1.3)
    vec(ax, 1.95, 0, 2.50, 0.85, lw=1.3)
    ax.text(0.97, -0.20, r'$\boldsymbol{q}$', fontsize=10, ha='center',
            va='center')
    ax.text(-0.10, -0.50, r'$\boldsymbol{k}$', fontsize=10, ha='center',
            va='center')
    ax.text(-0.60, 0.98, r'$\boldsymbol{k+q}$', fontsize=10, ha='center',
            va='center')
    ax.text(2.22, -0.50, r"$\boldsymbol{k'}$", fontsize=10, ha='left',
            va='center')
    ax.text(2.58, 0.98, r"$\boldsymbol{k'-q}$", fontsize=10, ha='left',
            va='center')
    save(fig, 'fig5-3')


def fig_5_4():
    """U 过程：六角 BZ 与费密圆，k + q 越出 BZ，K_n 折回"""
    fig, ax = plt.subplots(figsize=(4.35, 3.95))
    plain_axes(ax)
    ax.set_aspect('equal')
    R = 1.0                       # 六角外接半径
    ap = R * np.sqrt(3) / 2       # 内切半径

    def hexagon(cx, cy):
        angs = np.deg2rad([90, 150, 210, 270, 330, 30, 90])
        return [(cx + R * np.cos(a), cy + R * np.sin(a)) for a in angs]

    cells = [(0, 0), (2 * ap, 0), (ap, 1.5 * R), (ap, -1.5 * R)]
    for cx, cy in cells:
        pts = hexagon(cx, cy)
        ax.plot([p[0] for p in pts], [p[1] for p in pts], 'k-', lw=1.3)
        ax.add_patch(Circle((cx, cy), ap, facecolor='none', edgecolor='k',
                            lw=1.3))
    ax.set_xlim(-1.05, 3.05)
    ax.set_ylim(-1.95, 2.55)

    # 矢量链：J -k-> B -q-> T，T -K_n-> A（k' 点，中圆左缘）
    J = (0.0, 0.0)
    B = (0.866 * np.cos(np.deg2rad(-28)), 0.866 * np.sin(np.deg2rad(-28)))
    Q = (0.60, 0.42)                    # q 矢头
    T = (B[0] + Q[0], B[1] + Q[1])      # k+q 矢头（右圆内）
    A = (-0.866, T[1])                  # k' 点（中圆左缘）
    vec(ax, J[0], J[1], B[0], B[1], lw=1.2, ms=10)
    vec(ax, J[0], J[1], Q[0], Q[1], lw=1.2, ms=10)
    vec(ax, B[0], B[1], T[0], T[1], lw=1.2, ms=10)
    # K_n 长箭头（附中途方向箭头）
    ax.annotate('', xy=(A[0], A[1]), xytext=(T[0], T[1]),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2,
                                shrinkA=0, shrinkB=0, mutation_scale=13))
    ax.annotate('', xy=(0.25, T[1]), xytext=(0.55, T[1]),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2,
                                shrinkA=0, shrinkB=0, mutation_scale=11))
    ax.text(B[0] - 0.10, B[1] - 0.15, r'$\boldsymbol{k}$', fontsize=10,
            ha='center', va='center')
    ax.text(Q[0] + 0.09, Q[1] + 0.06, r'$\boldsymbol{q}$', fontsize=10,
            ha='left', va='center')
    ax.text(T[0] + 0.10, T[1] + 0.02, r'$\boldsymbol{k+q}$', fontsize=10,
            ha='left', va='center')
    ax.text(0.28, T[1] - 0.17, r'$\boldsymbol{K}_n$', fontsize=10,
            ha='center', va='center')
    ax.text(-0.18, 0.45,
            r"$\boldsymbol{k+q+K}_n=\boldsymbol{k'}$", fontsize=7.5,
            ha='center', va='center')
    save(fig, 'fig5-4')


def fig_5_5():
    """U 过程散射的电子速度图：v(k') = v(k+q)"""
    fig, ax = plt.subplots(figsize=(4.6, 2.75))
    plain_axes(ax)
    ax.set_aspect('equal')
    C2 = (2.72, -0.52)
    ax.add_patch(Circle((0, 0), 1.0, facecolor='none', edgecolor='k', lw=1.5))
    ax.add_patch(Circle(C2, 1.0, facecolor='none', edgecolor='k', lw=1.5))
    # k' 半径（197°，线上附方向箭头），粗箭头 v(k')
    a1 = np.deg2rad(197)
    E1 = (np.cos(a1), np.sin(a1))
    ax.plot([0, 1.06 * E1[0]], [0, 1.06 * E1[1]], 'k-', lw=1.1)
    vec(ax, 0.62 * E1[0], 0.62 * E1[1], 0.74 * E1[0], 0.74 * E1[1],
        lw=1.1, ms=9)
    thick_arrow(ax, 1.01 * E1[0], 1.01 * E1[1],
                1.01 * E1[0] - 0.30, 1.01 * E1[1] - 0.17)
    ax.text(-0.44, -0.02, r"$\boldsymbol{k'}$", fontsize=10, ha='center',
            va='center')
    ax.text(-1.34, -0.66, r"$\boldsymbol{v}(\boldsymbol{k'})$", fontsize=10,
            ha='center', va='center')
    # k 半径（-39°），粗箭头 v(k)
    a2 = np.deg2rad(-39)
    E2 = (np.cos(a2), np.sin(a2))
    ax.plot([0, 1.06 * E2[0]], [0, 1.06 * E2[1]], 'k-', lw=1.1)
    vec(ax, 0.62 * E2[0], 0.62 * E2[1], 0.74 * E2[0], 0.74 * E2[1],
        lw=1.1, ms=9)
    thick_arrow(ax, 1.01 * E2[0], 1.01 * E2[1],
                1.01 * E2[0] + 0.25, 1.01 * E2[1] - 0.24)
    ax.text(0.33, -0.42, r'$\boldsymbol{k}$', fontsize=10, ha='center',
            va='center')
    ax.text(1.10, -1.06, r'$\boldsymbol{v}(\boldsymbol{k})$', fontsize=10,
            ha='center', va='center')
    # k+q：连心线（略下斜）与右圆交点 P，P->C2 半径段，粗箭头 v(k+q)
    # 直线：过原点方向 (cos(-10.7),sin(-10.7))；P = C2 + (单位矢量指向原点)
    d = np.array([np.cos(np.deg2rad(-10.7)), np.sin(np.deg2rad(-10.7))])
    u = (np.array([0, 0]) - np.array(C2))
    u = u / np.hypot(*u)
    P = np.array(C2) + u                       # 右圆左缘上的 k+q 点
    ax.plot([0, P[0]], [0, P[1]], 'k-', lw=1.1)
    ax.plot([P[0], C2[0]], [P[1], C2[1]], 'k-', lw=1.1)
    mid = 0.60 * P
    vec(ax, 0.48 * P[0], 0.48 * P[1], mid[0], mid[1], lw=1.1, ms=9)
    thick_arrow(ax, P[0] + 0.02, P[1] - 0.06,
                P[0] - 0.30, P[1] - 0.29)
    ax.text(1.32, -0.06, r'$\boldsymbol{k+q}$', fontsize=10, ha='center',
            va='center')
    ax.text(1.78, -0.94, r'$\boldsymbol{v}(\boldsymbol{k+q})$',
            fontsize=10, ha='center', va='center')
    save(fig, 'fig5-5')


def fig_5_6():
    """电子-电子有效互作用：电子经过使晶格离子畸变（虚线为位移后位置）"""
    fig, ax = plt.subplots(figsize=(5.6, 2.25))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(0.0, 13.3)
    ax.set_ylim(0.0, 5.2)
    rr = 0.36

    def ion(x, y, dashed=False):
        ax.add_patch(Circle((x, y), rr, facecolor='none', edgecolor='k',
                            lw=1.5, ls=(0, (3, 1.8)) if dashed else '-'))
        ax.plot([x - 0.14, x + 0.14], [y, y], 'k-', lw=1.0)
        ax.plot([x, x], [y - 0.14, y + 0.14], 'k-', lw=1.0)

    # 四列离子（外侧两列不动，内侧两列向电子路径位移，虚线为位移后）
    cols = [2.2, 5.4, 8.6, 11.8]
    ion(cols[0], 4.30); ion(cols[0], 0.90)
    ion(cols[3], 4.30); ion(cols[3], 0.90)
    for cx, sx in ((cols[1], +1), (cols[2], -1)):
        dh = np.array([sx * 0.61, -0.792])          # 位移方向单位矢量
        for y0 in (4.30, 0.90):
            sgn = 1.0 if y0 > 2.6 else -1.0
            dvec = np.array([sx * 0.61, -sgn * 0.792])
            xd, yd = cx + dvec[0], y0 + dvec[1]
            ion(cx, y0)
            ion(xd, yd, dashed=True)
            p0 = (cx + rr * dvec[0], y0 + rr * dvec[1])
            p1 = (xd - rr * dvec[0], yd - rr * dvec[1])
            ax.annotate('', xy=p1, xytext=p0,
                        arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2,
                                        mutation_scale=9))
    # 电子运动箭头（均向左）
    ax.annotate('', xy=(1.00, 2.60), xytext=(6.10, 2.60),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.4,
                                shrinkA=0, shrinkB=0, mutation_scale=15))
    ax.annotate('', xy=(7.80, 2.60), xytext=(12.20, 2.60),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.4,
                                shrinkA=0, shrinkB=0, mutation_scale=15))
    ax.text(0.80, 2.60, '电子1', fontsize=10.5, ha='right', va='center')
    ax.text(12.45, 2.60, '电子2', fontsize=10.5, ha='left', va='center')
    save(fig, 'fig5-6')


def fig_5_7():
    """电子-声子-电子互作用：(a) k' 发射 q 声子 (b) k 发射 (-q) 声子"""
    fig, axs = plt.subplots(1, 2, figsize=(4.9, 2.1))
    for ax in axs:
        plain_axes(ax)
        ax.set_aspect('equal')

    for ax, qdir, qlab in ((axs[0], 'R', r'$-\boldsymbol{q}$'),
                           (axs[1], 'L', r'$\boldsymbol{q}$')):
        ax.set_xlim(-1.30, 3.30)
        ax.set_ylim(-1.30, 1.55)
        L, R = (0.0, 0.0), (1.90, 0.0)
        if qdir == 'R':
            wavy(ax, L[0], L[1], R[0], R[1], n=6, lw=1.1)
            vec(ax, 1.58, 0, 1.88, 0, lw=1.1, ms=9)   # 声子箭头（指向右顶点）
        else:
            wavy(ax, R[0], R[1], L[0], L[1], n=6, lw=1.1)
            vec(ax, 0.32, 0, 0.02, 0, lw=1.1, ms=9)   # 声子箭头（指向左顶点）
        vec(ax, -0.62, -0.88, L[0], L[1], lw=1.3)
        vec(ax, L[0], L[1], -0.55, 0.88, lw=1.3)
        vec(ax, 2.52, -0.88, R[0], R[1], lw=1.3)
        vec(ax, R[0], R[1], 2.45, 0.88, lw=1.3)
        ax.text(0.95, 0.17, qlab, fontsize=10, ha='center', va='center')
        ax.text(-0.52, -0.48, r'$\boldsymbol{k,\sigma}$', fontsize=9.5,
                ha='right', va='center')
        ax.text(-0.72, 0.98, r'$\boldsymbol{k+q,\sigma}$', fontsize=9.5,
                ha='center', va='center')
        ax.text(2.28, -0.48, r"$\boldsymbol{k',\sigma'}$", fontsize=9.5,
                ha='left', va='center')
        ax.text(2.55, 0.98, r"$\boldsymbol{k'-q,\sigma'}$", fontsize=9.5,
                ha='left', va='center')
    save(fig, 'fig5-7')


# ================================================================ 第六章
def fig_6_1():
    """超导体的电子比热容：c_S 指数律与 T_c 跳变，c_N 线性"""
    fig, ax = plt.subplots(figsize=(4.0, 2.7))
    plain_axes(ax)
    ax.set_xlim(-0.10, 1.42)
    ax.set_ylim(-0.72, 3.20)
    # c_N 虚线
    ax.plot([0, 1.20], [0, 1.35 / 1.0 * 1.20], 'k--', lw=1.0, dashes=(5, 2.6))
    # c_S 实线
    t = np.linspace(0.055, 1.0, 400)
    cs = 2.7 * np.exp(-2.38 * (1.0 / t - 1.0))
    ax.plot(t, cs, 'k-', lw=1.5)
    ax.plot([1.0, 1.0], [2.7, 1.35], 'k-', lw=1.5)     # T_c 处跳变
    ax.plot([1.0, 1.0], [0, 1.35], 'k--', lw=0.9, dashes=(4, 2.4))
    arrow_axis(ax, 0, 0, 0, 3.08)
    arrow_axis(ax, 0, 0, 1.34, 0)
    ax.text(-0.045, 3.02, r'$c$', fontsize=11, ha='center', va='center')
    ax.text(1.32, -0.13, r'$T$', fontsize=11, ha='center', va='center')
    ax.text(-0.035, -0.12, r'$O$', fontsize=10, ha='right', va='center')
    ax.text(0.50, 1.28, r'$c_{\rm S}$', fontsize=10, ha='center',
            va='center')
    ax.text(1.16, 1.86, r'$c_{\rm N}$', fontsize=10, ha='center',
            va='center')
    ax.text(1.0, -0.155, r'$T_{\rm c}$', fontsize=10, ha='center',
            va='center')
    ax.plot([1.0, 1.0], [-0.045, 0], 'k-', lw=0.9)
    ax.text(0.40, -0.42, r'$c_{\rm S}\sim k_{\rm B}\mathrm{e}^{-\Delta/k_{\rm B}T}$',
            fontsize=8.5, ha='center', va='center')
    ax.text(0.98, -0.42, r'$c_{\rm N}\sim k_{\rm B}^{2}T/E_{\rm F}$',
            fontsize=8.5, ha='center', va='center')
    save(fig, 'fig6-1')


def fig_6_2():
    """超导体的临界磁场 H_c(T)/H_c(0) = 1-(T/T_c)^2"""
    fig, ax = plt.subplots(figsize=(3.7, 2.7))
    plain_axes(ax)
    ax.set_xlim(-0.10, 1.42)
    ax.set_ylim(-0.14, 1.26)
    t = np.linspace(0, 1.0, 200)
    ax.plot(t, 1 - t ** 2, 'k-', lw=1.5)
    arrow_axis(ax, 0, 0, 0, 1.16)
    arrow_axis(ax, 0, 0, 1.34, 0)
    ax.plot([0, 0.025], [1, 1], 'k-', lw=0.9)
    ax.plot([1, 1], [0, 0.025], 'k-', lw=0.9)
    ax.text(-0.045, 1.0, r'$1$', fontsize=9, ha='right', va='center')
    ax.text(1.0, -0.075, r'$1$', fontsize=9, ha='center', va='center')
    ax.text(0.075, 1.13, r'$H_{\rm c}(T)\,/\,H_{\rm c}(0)$', fontsize=10,
            ha='left', va='center')
    ax.text(1.33, -0.085, r'$T/T_{\rm c}$', fontsize=10, ha='center',
            va='center')
    ax.text(-0.035, -0.065, r'$O$', fontsize=10, ha='right', va='center')
    save(fig, 'fig6-2')


def fig_6_3():
    """隧道效应 I-V：实线（T<Tc），虚线（T>Tc 直线）"""
    fig, ax = plt.subplots(figsize=(3.1, 2.85))
    plain_axes(ax)
    ax.set_xlim(-0.10, 1.14)
    ax.set_ylim(-0.13, 1.10)
    # 虚线（正常态直线）
    ax.plot([0, 1.02], [0, 0.92], 'k--', lw=1.0, dashes=(5, 2.6))
    # 实线（超导态）：平坦 + 陡升（略过冲后并入虚线）
    x1 = np.linspace(0.0, 0.70, 60)
    y1 = 0.004 + 0.003 * np.exp(9.0 * (x1 - 0.70))
    x2 = np.linspace(0.70, 1.00, 320)
    s = 1.0 / (1.0 + np.exp(-(x2 - 0.795) / 0.020))
    y2 = 0.92 * x2 * s + 0.022 * np.exp(-((x2 - 0.88) / 0.09) ** 2)
    ax.plot(x1, y1, 'k-', lw=1.5)
    ax.plot(x2, y2, 'k-', lw=1.5)
    ax.plot([0.78, 0.78], [0, 0.23], 'k--', lw=0.9, dashes=(4, 2.4))
    arrow_axis(ax, 0, 0, 0, 1.02)
    arrow_axis(ax, 0, 0, 1.08, 0)
    ax.text(-0.045, 0.70, r'$I$', fontsize=11, ha='center', va='center')
    ax.text(1.06, -0.09, r'$V$', fontsize=11, ha='center', va='center')
    ax.text(-0.032, -0.055, r'$O$', fontsize=10, ha='right', va='center')
    ax.text(0.78, -0.095, r'$\Delta/e$', fontsize=10, ha='center',
            va='center')
    save(fig, 'fig6-3')


def fig_6_4():
    """总波矢为 K 时电子对的吸引区（阴影区）"""
    fig, ax = plt.subplots(figsize=(4.0, 3.0))
    plain_axes(ax)
    ax.set_aspect('equal')
    ax.set_xlim(-1.45, 2.80)
    ax.set_ylim(-1.45, 1.45)
    d, R, Ri = 1.05, 1.0, 0.80
    for cx in (0.0, d):
        for r in (R, Ri):
            ax.add_patch(Circle((cx, 0), r, facecolor='none', edgecolor='k',
                                lw=1.4))

    def arc(cx, cy, r, a0, a1, n=40):
        t = np.linspace(np.deg2rad(a0), np.deg2rad(a1), n)
        return [(cx + r * np.cos(t), cy + r * np.sin(t)) for t in t]

    xt = d / 2.0
    x1 = (R ** 2 - Ri ** 2 + d ** 2) / (2 * d)     # 左外圆 与 右内圆 交点 x
    x2 = d - x1                                    # 左内圆 与 右外圆 交点 x
    aA = np.degrees(np.arccos(xt / R))             # A: 外-外交点(左外圆)
    aB = np.degrees(np.arccos(x1 / R))             # B: 左外圆-右内圆(左外圆)
    aB2 = np.degrees(np.arccos((x1 - d) / Ri))     # B 在右内圆上的角
    aC2 = np.degrees(np.arccos((xt - d) / Ri))     # C 在右内圆上的角
    aC1 = np.degrees(np.arccos(xt / Ri))           # C 在左内圆上的角
    aD = np.degrees(np.arccos(x2 / Ri))            # D 在左内圆上的角

    def patch(sgn):
        pts = []
        pts += arc(0, 0, R, sgn * aA, sgn * aB)            # A->B 左外圆
        pts += arc(d, 0, Ri, sgn * aB2, sgn * aC2)         # B->C 右内圆
        pts += arc(0, 0, Ri, sgn * aC1, sgn * aD)          # C->D 左内圆
        pts += arc(d, 0, R, 180 - sgn * aB, 180 - sgn * aA)  # D->A 右外圆
        return pts

    for sgn in (+1, -1):
        ax.add_patch(Polygon(patch(sgn), closed=True, facecolor='white',
                             edgecolor='k', lw=0.5, hatch='////'))
    # 矢量
    vec(ax, 0, 0, 0.52, 0.74, lw=1.2, ms=10)
    vec(ax, 0, 0, 0.52, -0.74, lw=1.2, ms=10)
    vec(ax, 0, 0, 1.42, 0, lw=1.2, ms=11)
    ax.text(0.10, 0.44, r'$\boldsymbol{k}$', fontsize=10, ha='left',
            va='center')
    ax.text(-0.02, -0.46, r'$\boldsymbol{K-k}$', fontsize=10, ha='right',
            va='center')
    ax.text(1.50, 0.0, r'$\boldsymbol{K}$', fontsize=10, ha='left',
            va='center')
    save(fig, 'fig6-4')


def fig_6_5():
    """超导体的元激发：xi_k = sqrt(eps_k^2 + Delta^2) 与 |eps_k|"""
    fig, ax = plt.subplots(figsize=(4.3, 2.8))
    plain_axes(ax)
    ax.set_xlim(-5.35, 5.75)
    ax.set_ylim(-0.62, 4.85)
    xx = np.linspace(-4.55, 4.55, 500)
    ax.plot(xx, np.sqrt(xx ** 2 + 1), 'k-', lw=1.5)
    ax.plot([-4.35, 0, 4.35], [4.35, 0, 4.35], 'k--', lw=1.0, dashes=(5, 2.8))
    arrow_axis(ax, 0, -0.35, 0, 4.45, lw=1.0)
    arrow_axis(ax, -4.85, 0, 5.15, 0, lw=1.0)
    for i in range(-4, 5):
        if i == 0:
            continue
        ax.plot([i, i], [-0.07, 0.07], 'k-', lw=0.9)
        lab = (r'$-4\Delta$', r'$-3\Delta$', r'$-2\Delta$', r'$-\Delta$',
               r'$\Delta$', r'$2\Delta$', r'$3\Delta$', r'$4\Delta$')
        ax.text(i, -0.30, lab[i + 4] if i < 0 else lab[i + 3], fontsize=8.5,
                ha='center', va='center')
    ax.text(0.13, -0.30, r'$0$', fontsize=8.5, ha='left', va='center')
    ax.plot([0.10], [1.005], marker='^', ms=6, mfc='white', mec='k',
            mew=0.9, ls='none')                    # 原书以小三角形标能隙
    ax.text(2.55, 4.15, r'$\xi_k=\sqrt{\varepsilon_k^2+\Delta^2}$',
            fontsize=9.5, ha='center', va='center')
    ax.annotate('', xy=(2.62, 2.95), xytext=(2.42, 3.85),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=0.9,
                                shrinkA=0, shrinkB=0, mutation_scale=9))
    ax.text(-2.62, 2.42, r'$|\varepsilon_k|$', fontsize=9.5, ha='center',
            va='center')
    ax.text(2.62, 2.42, r'$|\varepsilon_k|$', fontsize=9.5, ha='center',
            va='center')
    ax.text(5.30, -0.28, r'$\varepsilon_k=E_k-E_{\rm F}$', fontsize=9.5,
            ha='left', va='center')
    save(fig, 'fig6-5')


def fig_6_6():
    """超导体中的零温粒子分布 v_k^2（含原书公式）"""
    fig, ax = plt.subplots(figsize=(3.4, 3.1))
    plain_axes(ax)
    ax.set_xlim(-2.75, 2.15)
    ax.set_ylim(-0.72, 1.24)
    x0 = -2.30
    xx = np.linspace(x0, 1.42, 400)
    ax.plot(xx, 0.5 * (1 - xx / np.sqrt(xx ** 2 + 1)), 'k-', lw=1.5)
    ax.plot([x0, 0], [1, 1], 'k--', lw=1.0, dashes=(5, 2.6))
    ax.plot([0, 0], [1, 0], 'k--', lw=1.0, dashes=(5, 2.6))
    ax.plot([x0, 1.85], [0, 0], 'k-', lw=1.0)
    ax.plot([x0, x0], [0, 1.10], 'k-', lw=1.0)
    # x 轴箭头与 y 轴刻度
    ax.annotate('', xy=(1.97, 0), xytext=(1.80, 0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                shrinkA=0, shrinkB=0, mutation_scale=10))
    for yv in (0.5, 1.0):
        ax.plot([x0 - 0.03, x0], [yv, yv], 'k-', lw=0.9)
        ax.text(x0 - 0.06, yv, ('0.5' if yv < 0.75 else '1.0'), fontsize=8,
                ha='right', va='center')
    for xv, lab in ((-1, r'$E_{\rm F}-\Delta$'), (0, r'$E_{\rm F}$'),
                    (1, r'$E_{\rm F}+\Delta$')):
        ax.plot([xv, xv], [-0.04, 0], 'k-', lw=0.9)
        ax.text(xv, -0.115, lab, fontsize=8, ha='center', va='center')
    ax.text(x0 - 0.06, 1.17, r'$v_k^2$', fontsize=10, ha='right',
            va='center')
    ax.text(1.99, -0.10, r'$E_k$', fontsize=10, ha='center', va='center')
    ax.text(x0 - 0.06, -0.09, r'$O$', fontsize=9, ha='right', va='center')
    ax.text(-1.15, 0.62, r'$T$=0 K', fontsize=9, ha='center', va='center')
    # 原书图下公式
    ax.text(-0.28, -0.50,
            r'$v_k^2=\dfrac{1}{2}\left\{1-\dfrac{(E_k-E_{\rm F})}'
            r'{\sqrt{(E_k-E_{\rm F})^2+\Delta^2}}\right\}$',
            fontsize=9.5, ha='center', va='center')
    save(fig, 'fig6-6')


def fig_6_7():
    """超导体的 BCS 模型图像：xi_k 抛物线与 mu 线上的库柏对态"""
    fig, ax = plt.subplots(figsize=(3.1, 2.1))
    plain_axes(ax)
    ax.set_xlim(-0.10, 4.72)
    ax.set_ylim(-0.60, 1.78)
    ax.plot([0, 4.05], [0, 0], 'k-', lw=1.1)
    xx = np.linspace(0.35, 3.85, 300)
    ax.plot(xx, 0.55 + 0.28 * (xx - 2.1) ** 2, 'k-', lw=1.6)
    ax.plot([2.1, 2.1], [0, 0.55], 'k--', lw=0.9, dashes=(4, 2.4))
    for xc in (0.85, 0.99, 2.02, 2.16, 3.20, 3.34):
        dot(ax, xc, 0, ms=6.5, open=True)
    ax.text(4.18, 0, r'$\mu$', fontsize=11, ha='left', va='center')
    ax.text(3.98, 1.62, r'$\xi_k$', fontsize=11, ha='center', va='center')
    ax.text(2.30, -0.36, r'$\Delta$', fontsize=10, ha='left', va='center')
    save(fig, 'fig6-7')


def _ns_panel(ax, kind):
    """图6.8 单面板：N-S 接触能谱（N 侧满液海 + 势垒 + S 侧 xi_k 抛物线）"""
    dl = 0.22                       # Delta
    if kind == 'a':
        yL, yR = 0.90, 0.90
    elif kind == 'b':
        yL, yR = 1.00, 0.68
    else:
        yL, yR = 0.62, 0.98
    x0, x1 = 0.0, 1.28
    aa = 5.5                        # 抛物线曲率
    pxc = 0.88
    ytop = max(yL, yR + dl + 0.70)
    ax.set_xlim(-0.02, 1.40)
    ax.set_ylim(min(yL, yR) - 0.55, ytop + 0.16)
    # 势垒双线
    xb0, xb1 = 0.46, 0.52
    ylo, yhi = ax.get_ylim()
    ax.plot([xb0, xb0], [ylo + 0.06, yhi - 0.28], 'k-', lw=1.6)
    ax.plot([xb1, xb1], [ylo + 0.06, yhi - 0.28], 'k-', lw=1.6)
    # N 侧：mu_L 线 + 满液海（斜线阴影四分之一圆）
    ax.plot([x0 + 0.03, xb0], [yL, yL], 'k-', lw=1.1)
    ax.add_patch(Wedge((xb0, yL), 0.44, 180, 270, facecolor='white',
                       edgecolor='k', lw=0.8, hatch='/////'))
    ax.text(0.015, yL + 0.12, r'$\mu_L$', fontsize=10, ha='left',
            va='center')
    ax.text(0.10, yhi - 0.13, r'$N$', fontsize=11, ha='center', va='center')
    # S 侧：xi_k 抛物线
    ax.plot([xb1, 1.26], [yR, yR], 'k-', lw=1.1)
    xx = np.linspace(0.585, 1.175, 200)
    ax.plot(xx, yR + dl + aa * (xx - pxc) ** 2, 'k-', lw=1.6)
    ax.text(0.86, yR + dl + 0.60, r'$S$', fontsize=11, ha='center',
            va='center')
    ax.text(1.19, yR + dl + 0.56, r'$\xi_k$', fontsize=10, ha='left',
            va='center')
    # mu_R 线上的态（开圆点对）
    for xc in (0.585, 0.635, 0.845, 0.895, 1.065, 1.115):
        dot(ax, xc, yR, ms=5, open=True)
    ax.text(1.29, yR, r'$\mu_R$', fontsize=10, ha='left', va='center')
    # Delta 标记
    if kind in ('a', 'b'):
        ax.plot([pxc, pxc], [yR, yR + dl], 'k-', lw=1.0)
        ax.text(pxc + 0.035, yR + dl * 0.78, r'$\Delta$', fontsize=10,
                ha='left', va='center')
    else:
        vec(ax, pxc, yR, pxc, yR + dl - 0.01, lw=1.0, ms=9)
        ax.text(pxc + 0.035, yR + dl * 0.55, r'$\Delta$', fontsize=10,
                ha='left', va='center')
    if kind == 'b':
        # 注入电子：N 费密面上势垒处 -> xi_k 左支（等能水平箭头）
        a = aa
        xs_ = pxc - np.sqrt((yL - yR - dl) / a)
        dot(ax, 0.435, yL, ms=4.5, open=True)
        vec(ax, 0.435, yL, xs_ - 0.02, yL, lw=1.2, ms=10)
        dot(ax, xs_, yL, ms=4.5, open=True)
    if kind == 'c':
        # 注入空穴：mu_R 中心态 -> N 费密面（斜向下箭头）
        vec(ax, 0.855, yR - 0.01, 0.40, yL + 0.015, lw=1.2, ms=11)


def fig_6_8():
    """超导与正常金属接触：(a) V=0 (b) 注入电子 (c) 注入空穴"""
    fig = plt.figure(figsize=(5.2, 4.7))
    axa = fig.add_axes([0.02, 0.545, 0.46, 0.44])
    axb = fig.add_axes([0.53, 0.545, 0.45, 0.44])
    axc = fig.add_axes([0.27, 0.03, 0.46, 0.44])
    for ax in (axa, axb, axc):
        plain_axes(ax)
        ax.set_aspect('auto')
    _ns_panel(axa, 'a')
    _ns_panel(axb, 'b')
    _ns_panel(axc, 'c')
    save(fig, 'fig6-8')


def fig_6_9():
    """电子-空穴对型激发：mu 线上一对态激发到 xi_k 两支"""
    fig, ax = plt.subplots(figsize=(3.1, 2.4))
    plain_axes(ax)
    ax.set_xlim(-0.08, 4.30)
    ax.set_ylim(-0.75, 1.90)
    ax.plot([0, 3.45], [0, 0], 'k-', lw=1.1)
    pxc = 1.95
    xx = np.linspace(0.45, 3.35, 300)
    ax.plot(xx, 0.44 + 0.46 * (xx - pxc) ** 2, 'k-', lw=1.6)
    for xc in (0.78, 0.94, 1.88, 2.04, 2.82, 2.98):
        dot(ax, xc, 0, ms=6.5, open=True)
    vec(ax, 1.90, 0.02, 1.50, 0.56, lw=1.1, ms=9)
    vec(ax, 2.00, 0.02, 2.40, 0.56, lw=1.1, ms=9)
    brace(ax, 2.58, 0.0, 0.44, 0.09)
    ax.text(2.86, 0.20, r'$\Delta$', fontsize=10, ha='left', va='center')
    ax.text(3.58, 0, r'$\mu$', fontsize=11, ha='left', va='center')
    ax.text(3.42, 1.62, r'$\xi_k$', fontsize=11, ha='center', va='center')
    save(fig, 'fig6-9')


def fig_6_10():
    """载流超导体中的库柏对：(a) 超导基态 (b) 载流超导态"""
    fig, axs = plt.subplots(1, 2, figsize=(5.5, 2.45))
    for ax in axs:
        plain_axes(ax)
        ax.set_aspect('equal')
        ax.set_xlim(-1.42, 1.42)
        ax.set_ylim(-1.42, 1.42)

    ax = axs[0]
    ax.add_patch(Circle((0, 0), 0.92, facecolor='none', edgecolor='k',
                        lw=1.4))
    arrow_axis(ax, -1.30, 0, 1.32, 0, lw=1.0)
    arrow_axis(ax, 0, -1.30, 0, 1.32, lw=1.0)
    vec(ax, 0, 0, 0.65, 0.65, lw=1.5, ms=12)
    vec(ax, 0, 0, -0.65, -0.65, lw=1.5, ms=12)
    ax.text(0.78, 0.70, r'$\boldsymbol{k}\uparrow$', fontsize=10, ha='left',
            va='center')
    ax.text(-0.80, -0.78, r'$-\boldsymbol{k}\downarrow$', fontsize=10,
            ha='right', va='center')
    ax.text(1.28, -0.13, r'$k_x$', fontsize=10, ha='center', va='center')
    ax.text(-0.15, 1.30, r'$k_y$', fontsize=10, ha='center', va='center')

    ax = axs[1]
    ax.add_patch(Circle((0, 0), 0.92, facecolor='none', edgecolor='k',
                        lw=1.4))
    arrow_axis(ax, -1.30, 0, 1.32, 0, lw=1.0)
    arrow_axis(ax, 0, -1.30, 0, 1.32, lw=1.0)
    u = np.array([np.cos(np.pi / 4), np.sin(np.pi / 4)])
    ax.plot([0, 0.92 * u[0]], [0, 0.92 * u[1]], 'k--', lw=0.9, dashes=(4, 2.4))
    ax.plot([0, -0.92 * u[0]], [0, -0.92 * u[1]], 'k--', lw=0.9,
            dashes=(4, 2.4))
    # 位移后库柏对（δk 沿 k_x 轴，两端仍在圆上但不再共线）
    dk = np.array([0.17, 0.0])
    p1 = 0.92 * (u + dk / 0.92) / np.hypot(*(u + dk / 0.92))
    p2 = 0.92 * (-u + dk / 0.92) / np.hypot(*(-u + dk / 0.92))
    vec(ax, 0, 0, p1[0], p1[1], lw=1.5, ms=12)
    vec(ax, 0, 0, p2[0], p2[1], lw=1.5, ms=12)
    ax.annotate('', xy=(0.30, 0.035), xytext=(0.045, 0.035),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.1,
                                shrinkA=0, shrinkB=0, mutation_scale=9))
    ax.text(0.80, 0.72, r'$\boldsymbol{k+}\delta\boldsymbol{k}\uparrow$',
            fontsize=9.5, ha='left', va='center')
    ax.text(0.40, 0.435, r'$\boldsymbol{k}$', fontsize=9.5, ha='left',
            va='center')
    ax.text(0.06, -0.15, r'$\delta\boldsymbol{k}$', fontsize=9,
            ha='center', va='center')
    ax.text(-0.24, -0.42, r'$-\boldsymbol{k}$', fontsize=9.5, ha='center',
            va='center')
    ax.text(-0.88, -0.86, r'$-\boldsymbol{k+}\delta\boldsymbol{k}\downarrow$',
            fontsize=9.5, ha='right', va='center')
    ax.text(1.28, -0.13, r'$k_x$', fontsize=10, ha='center', va='center')
    ax.text(-0.15, 1.30, r'$k_y$', fontsize=10, ha='center', va='center')
    save(fig, 'fig6-10')


def _bcs_gap():
    """数值求解 BCS 约化能隙方程，返回 t=T/Tc 网格与 delta=Delta(T)/Delta(0)。
    约化形式 ln d = L(d,t)：令 xi=d·sinh u 消去 1/E 奇异，kBTc=Delta0/1.764。"""
    def g(d, t):
        U = np.arcsinh(60.0 / d)
        u = np.linspace(0.0, U, 4000)
        return np.log(d) - np.trapezoid(
            np.tanh(0.882 * d * np.cosh(u) / t) - 1.0, u)

    ts = np.linspace(0.02, 0.9995, 140)
    ds = []
    for t in ts:
        grid = np.logspace(-4, np.log10(1.02), 90)
        gv = np.array([g(d, t) for d in grid])
        j = np.where((gv[:-1] <= 0) & (gv[1:] > 0))[0][-1]
        ds.append(brentq(lambda d: g(d, t), grid[j], grid[j + 1], xtol=1e-9))
    return ts, np.array(ds)


def fig_6_11():
    """能隙与温度关系 Delta(T)/Delta(0) ~ T/Tc（BCS）"""
    fig, ax = plt.subplots(figsize=(4.0, 3.2))
    plain_axes(ax)
    ax.set_xlim(-0.10, 1.24)
    ax.set_ylim(-0.13, 1.22)
    ts, ds = _bcs_gap()
    ax.plot(ts, ds, 'k-', lw=1.6)
    arrow_axis(ax, 0, 0, 0, 1.13)
    arrow_axis(ax, 0, 0, 1.15, 0)
    for v in (0.2, 0.4, 0.6, 0.8, 1.0):
        ax.plot([0, 0.018], [v, v], 'k-', lw=0.9)
        ax.plot([v, v], [0, 0.018], 'k-', lw=0.9)
        ax.text(-0.032, v, ('%.1f' % v), fontsize=8, ha='right', va='center')
        ax.text(v, -0.062, ('%.1f' % v), fontsize=8, ha='center',
                va='center')
    ax.text(0.10, 1.14, r'$\dfrac{\Delta(T)}{\Delta(0)}$', fontsize=12,
            ha='center', va='center')
    ax.text(1.17, -0.075, r'$T/T_{\rm c}$', fontsize=10, ha='center',
            va='center')
    ax.text(-0.035, -0.06, r'$O$', fontsize=9, ha='right', va='center')
    save(fig, 'fig6-11')


def fig_6_12():
    """实际临界磁场与经验曲线 [1-(T/Tc)^2] 的差别 D(T)"""
    fig, ax = plt.subplots(figsize=(3.7, 3.6))
    plain_axes(ax)
    ax.set_xlim(-0.14, 1.30)
    ax.set_ylim(-0.062, 0.040)
    # 坐标轴
    ax.plot([0, 0], [-0.048, 0.030], 'k-', lw=1.0)
    ax.annotate('', xy=(0, 0.036), xytext=(0, 0.028),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                shrinkA=0, shrinkB=0, mutation_scale=10))
    ax.plot([0, 1.06], [0, 0], 'k-', lw=1.0)
    ax.annotate('', xy=(1.10, 0), xytext=(1.055, 0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                shrinkA=0, shrinkB=0, mutation_scale=10))
    # 刻度
    for v in (0.2, 0.4, 0.6, 0.8, 1.0):
        ax.plot([v, v], [-0.002, 0.002], 'k-', lw=0.9)
        ax.text(v, -0.0055, ('%.1f' % v), fontsize=8, ha='center',
                va='center')
    for yv, lab in ((0.02, r'$0.02$'), (0, r'$0$'), (-0.02, r'$-0.02$'),
                    (-0.04, r'$-0.04$')):
        ax.plot([-0.004, 0], [yv, yv], 'k-', lw=0.9)
        ax.text(-0.012, yv, lab, fontsize=8, ha='right', va='center')
    ax.text(-0.115, 0.031, r'$D(T)$', fontsize=10, ha='center', va='center')
    ax.text(1.115, 0.004, r'$(T/T_{\rm c})^2$', fontsize=10, ha='left',
            va='center')
    # 曲线（示意图形态，参照原书）
    def curve(pts):
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        f = PchipInterpolator(xs, ys)
        xx = np.linspace(xs[0], xs[-1], 300)
        return xx, f(xx)

    Pb = [(0, 0), (0.10, 0.0045), (0.25, 0.0105), (0.45, 0.0150),
          (0.62, 0.0138), (0.80, 0.0080), (0.95, 0.0022), (1.0, 0)]
    Sn = [(0, 0), (0.10, -0.0080), (0.30, -0.0225), (0.50, -0.0305),
          (0.62, -0.0310), (0.80, -0.0225), (0.95, -0.0060), (1.0, 0)]
    Al = [(0, 0), (0.10, -0.0100), (0.30, -0.0272), (0.50, -0.0355),
          (0.62, -0.0358), (0.80, -0.0255), (0.95, -0.0070), (1.0, 0)]
    BC = [(0, 0), (0.10, -0.0090), (0.30, -0.0250), (0.52, -0.0332),
          (0.65, -0.0340), (0.80, -0.0250), (0.95, -0.0065), (1.0, 0)]
    for pts, ls in ((Pb, '-'), (Sn, '-'), (Al, '-'), (BC, (0, (5, 2.6)))):
        xx, yy = curve(pts)
        ax.plot(xx, yy, color='k', ls=ls, lw=1.4)
    ax.text(0.62, 0.0130, 'Pb', fontsize=9.5, ha='left', va='center')
    ax.text(0.56, -0.0285, 'Sn', fontsize=9.5, ha='center', va='center')
    ax.text(0.30, -0.0400, 'Al', fontsize=9.5, ha='center', va='center')
    ax.text(0.87, -0.0290, 'BCS', fontsize=9.5, ha='left', va='center')
    save(fig, 'fig6-12')


if __name__ == '__main__':
    import sys
    names = sys.argv[1:]
    allfigs = ['4-1', '4-2', '4-3', '4-4', '4-5', '4-6', '4-7', '4-8',
               '4-9', '4-10', '5-1', '5-2', '5-3', '5-4', '5-5', '5-6',
               '5-7', '6-1', '6-2', '6-3', '6-4', '6-5', '6-6', '6-7',
               '6-8', '6-9', '6-10', '6-11', '6-12']
    todo = names if names else allfigs
    for nm in todo:
        globals()['fig_' + nm.replace('-', '_')]()
        print('fig%s done' % nm)
