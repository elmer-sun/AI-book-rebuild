# -*- coding: utf-8 -*-
"""朗道《量子力学》卷3 中文重排本 插图重绘 第二批：图13-22.

基准：原书页面 PNG 原书转换/pages/p-NNN.png（图13→p179 ... 图22→p232）。
黑白教材风矢量图，PDF+PNG 双输出。
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
PRE = os.path.join(OUT, 'preview')
os.makedirs(PRE, exist_ok=True)

KW = dict(arrowstyle='-|>', color='k', lw=0, mutation_scale=11, shrinkA=0, shrinkB=0)
KWS = dict(arrowstyle='-|>', color='k', lw=1.1, mutation_scale=11, shrinkA=0, shrinkB=0)


def new_ax(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    return fig, ax


def save(fig, n):
    fig.savefig(os.path.join(OUT, f'fig{n}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRE, f'fig{n}.png'), dpi=200, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


# ---------------------------------------------------------------- 图13 (p179)
def fig_13():
    fig, ax = new_ax(2.9, 1.75)
    a, b, E = 0.74, 2.86, 1.0
    x = np.linspace(-1.5, 4.35, 400)
    y = 0.5 + 1.35 * np.exp(-((x - 1.8) ** 2) / (2 * 0.75 ** 2))
    # 曲线
    ax.plot(x, y, 'k-', lw=1.4)
    # 坐标轴
    ax.plot([-1.55, 4.42], [0, 0], 'k-', lw=1.2)          # x 轴
    ax.plot([0, 0], [0, 2.25], 'k-', lw=1.2)              # U(x) 轴
    # E 虚线
    ax.plot([-1.5, 4.35], [E, E], 'k--', lw=0.9, dashes=(5, 3))
    # a、b 处竖直虚线
    for xt in (a, b):
        ax.plot([xt, xt], [0, E], 'k--', lw=0.9, dashes=(3, 2.5))
    # 标注
    ax.text(4.32, E + 0.07, r'$E$', fontsize=11, ha='right', va='bottom')
    ax.text(0.07, 2.14, r'$U(x)$', fontsize=11, ha='left', va='top')
    ax.text(4.50, -0.02, r'$x$', fontsize=11, ha='left', va='center')
    ax.text(a, -0.14, r'$a$', fontsize=11, ha='center', va='top')
    ax.text(b, -0.14, r'$b$', fontsize=11, ha='center', va='top')
    ax.text(-0.60, E - 0.28, 'I', fontsize=11, ha='center', va='center')
    ax.text(1.80, E - 0.28, 'II', fontsize=11, ha='center', va='center')
    ax.text(3.55, E - 0.28, 'III', fontsize=11, ha='center', va='center')
    ax.set_xlim(-1.75, 4.75)
    ax.set_ylim(-0.42, 2.45)
    ax.set_aspect('equal')
    save(fig, 13)


# ---------------------------------------------------------------- 图14 (p181)
def fig_14():
    fig, ax = new_ax(1.9, 2.6)
    U0, E = 1.85, 1.15
    # 坐标轴
    ax.plot([-0.72, 1.58], [0, 0], 'k-', lw=1.2)          # x 轴 (x<0 时 U=0)
    ax.plot([0, 0], [-0.85, 2.55], 'k-', lw=1.2)          # U(x) 轴
    # x>0: U = U0 - Fx 直线（穿过 x 轴继续向下）
    ax.plot([0, 1.42], [U0, -0.62], 'k-', lw=1.4)
    # E 虚线
    ax.plot([-0.62, 1.02], [E, E], 'k--', lw=0.9, dashes=(5, 3))
    ax.text(1.10, E, r'$E$', fontsize=11, ha='left', va='center')
    ax.text(0.07, 2.50, r'$U(x)$', fontsize=11, ha='left', va='top')
    ax.text(1.64, -0.02, r'$x$', fontsize=11, ha='left', va='center')
    ax.text(-0.09, U0, r'$U_0$', fontsize=11, ha='right', va='center')
    ax.set_xlim(-0.92, 1.90)
    ax.set_ylim(-1.05, 2.75)
    ax.set_aspect('equal')
    save(fig, 14)


# ---------------------------------------------------------------- 图15 (p181)
def fig_15():
    fig, ax = new_ax(1.9, 2.3)
    r0, U0w = 0.62, -0.55
    top = 2.30
    # 坐标轴
    ax.plot([0, 2.18], [0, 0], 'k-', lw=1.2)              # r 轴
    ax.plot([0, 0], [-0.85, 2.35], 'k-', lw=1.2)          # U(r) 轴
    # 阱底 (r<r0: U=-U0) 与竖直壁
    ax.plot([0, r0], [U0w, U0w], 'k-', lw=1.4)
    ax.plot([r0, r0], [U0w, top + 0.06], 'k-', lw=1.4)
    # r>r0: U = alpha/r
    rr = np.linspace(r0, 2.15, 300)
    ax.plot(rr, 1.426 / rr, 'k-', lw=1.4)
    # 标注
    ax.text(-0.08, 2.28, r'$U(r)$', fontsize=11, ha='right', va='top')
    ax.text(2.26, -0.02, r'$r$', fontsize=11, ha='left', va='center')
    ax.text(r0 + 0.06, 0.09, r'$r_0$', fontsize=11, ha='left', va='bottom')
    ax.text(-0.09, U0w, r'$-U_0$', fontsize=11, ha='right', va='center')
    ax.set_xlim(-0.72, 2.52)
    ax.set_ylim(-1.05, 2.55)
    ax.set_aspect('equal')
    save(fig, 15)


# ---------------------------------------------------------------- 图16 (p182)
def fig_16():
    fig, ax = new_ax(2.6, 2.3)
    c, k, d = 1.5, 0.1976, 0.35
    U = lambda x: k * (x ** 2 - c ** 2) ** 2 + d
    E2, E0, E1 = 1.33, 1.28, 1.23
    x = np.linspace(-2.38, 2.38, 600)
    ax.plot(x, U(x), 'k-', lw=1.4)
    # 坐标轴
    ax.plot([-2.42, 2.62], [0, 0], 'k-', lw=1.2)
    ax.plot([0, 0], [0, 2.52], 'k-', lw=1.2)
    # 右阱内 E2(dashed)/E0(solid)/E1(dashed)
    def roots(E):
        s = np.sqrt((E - d) / k)
        return np.sqrt(c ** 2 - s), np.sqrt(c ** 2 + s)   # 内侧/外侧交点
    for E, style in ((E2, 'k--'), (E0, 'k-'), (E1, 'k--')):
        xi, xo = roots(E)
        if style == 'k--':
            ax.plot([xi, xo], [E, E], style, lw=1.0, dashes=(4, 2.5))
        else:
            ax.plot([xi, xo], [E, E], style, lw=1.3)
    # a 处竖直虚线（E0 外回点）
    _, ao = roots(E0)
    ax.plot([ao, ao], [0, E0], 'k--', lw=0.9, dashes=(3, 2.5))
    # 标注
    ax.text(0.07, 2.44, r'$U(x)$', fontsize=11, ha='left', va='top')
    ax.text(2.70, -0.02, r'$x$', fontsize=11, ha='left', va='center')
    ax.text(0.09, 1.44, r'$U_0$', fontsize=11, ha='left', va='bottom')
    ax.text(ao + 0.02, -0.15, r'$a$', fontsize=11, ha='center', va='top')
    ax.text(2.20, 1.47, r'$E_2$', fontsize=11, ha='left', va='bottom')
    ax.text(2.42, 1.29, r'$E_0$', fontsize=11, ha='left', va='center')
    ax.text(2.55, 1.10, r'$E_1$', fontsize=11, ha='left', va='center')
    ax.text(-1.45, 2.22, 'II', fontsize=11, ha='center', va='center')
    ax.text(1.45, 2.22, 'I', fontsize=11, ha='center', va='center')
    ax.set_xlim(-2.62, 3.15)
    ax.set_ylim(-0.42, 2.68)
    ax.set_aspect('equal')
    save(fig, 16)


# ---------------------------------------------------------------- 图17 (p184)
def fig_17():
    fig, ax = new_ax(2.1, 2.5)
    E2, E1 = 1.62, 1.28
    U = lambda x: 1.55 / (x + 0.15)
    x = np.linspace(0.40, 2.82, 300)
    # 坐标轴
    ax.plot([0, 3.02], [0, 0], 'k-', lw=1.2)
    ax.plot([0, 0], [0, 2.92], 'k-', lw=1.2)
    # 曲线
    ax.plot(x, U(x), 'k-', lw=1.4)
    # E2、E1 虚线
    ax.plot([0, 2.56], [E2, E2], 'k--', lw=0.9, dashes=(5, 3))
    ax.plot([0, 2.56], [E1, E1], 'k--', lw=0.9, dashes=(5, 3))
    ax.text(2.62, E2, r'$E_2$', fontsize=11, ha='left', va='center')
    ax.text(2.62, E1, r'$E_1$', fontsize=11, ha='left', va='center')
    # 回点 a2、a1 竖直虚线
    a2, a1 = 1.55 / E2 - 0.15, 1.55 / E1 - 0.15
    for xt in (a2, a1):
        ax.plot([xt, xt], [0, 1.55 / (xt + 0.15)], 'k--', lw=0.9, dashes=(3, 2.5))
    ax.text(a2 - 0.03, -0.16, r'$a_2$', fontsize=11, ha='center', va='top')
    ax.text(a1 + 0.09, -0.16, r'$a_1$', fontsize=11, ha='center', va='top')
    # 轴标注
    ax.text(0.07, 3.28, r'$U(x)$', fontsize=11, ha='left', va='top')
    ax.text(3.10, -0.02, r'$x$', fontsize=11, ha='left', va='center')
    ax.set_xlim(-0.28, 3.38)
    ax.set_ylim(-0.55, 3.45)
    ax.set_aspect('equal')
    save(fig, 17)


# ---------------------------------------------------------------- 图18 (p186)
def fig_18():
    fig, ax = new_ax(1.9, 2.4)
    KW2 = dict(KW, mutation_scale=15)
    cx, cy, r = 0.0, 0.60, 0.17
    # x 轴（带右向箭头）
    ax.plot([-1.05, 1.22], [0, 0], 'k-', lw=1.2)
    ax.annotate('', xy=(1.42, 0), xytext=(1.18, 0), arrowprops=KW2)
    ax.text(1.52, 0.02, r'$x$', fontsize=11, ha='left', va='center')
    # 奇点 x0：小圆 + 点
    t = np.linspace(0, 2 * np.pi, 100)
    ax.plot(cx + r * np.cos(t), cy + r * np.sin(t), 'k-', lw=1.2)
    ax.add_patch(plt.Circle((cx, cy), 0.038, color='k'))
    # 两条竖直支线（自上而下、绕过 x0 再向上）
    hw = 0.55 * r
    for xs in (cx - hw, cx + hw):
        ax.plot([xs, xs], [cy + 0.10, 2.30], 'k-', lw=1.2)
    ax.annotate('', xy=(cx - hw, 1.28), xytext=(cx - hw, 1.56), arrowprops=KW2)  # 左线向下
    ax.annotate('', xy=(cx + hw, 1.56), xytext=(cx + hw, 1.28), arrowprops=KW2)  # 右线向上
    ax.text(cx, 0.32, r'$x_0$', fontsize=11, ha='center', va='top')
    ax.set_xlim(-1.35, 1.80)
    ax.set_ylim(-0.30, 2.50)
    ax.set_aspect('equal')
    save(fig, 18)


# ---------------------------------------------------------------- 图19 (p190)
def fig_19():
    fig, ax = new_ax(2.7, 1.8)
    # 实轴
    ax.plot([-1.72, 1.78], [0, 0], 'k-', lw=1.2)
    # 大半圆 C（逆时针：右端上行，越顶向左）
    th = np.linspace(0, np.pi, 200)
    R, ox = 1.50, -0.11
    ax.plot(ox + R * np.cos(th), 1.17 * np.sin(th), 'k-', lw=1.3)
    for ang in (38, 115):
        p = (ox + R * np.cos(np.radians(ang)), 1.17 * np.sin(np.radians(ang)))
        d = (-np.sin(np.radians(ang)), np.cos(np.radians(ang)))
        ax.annotate('', xy=(p[0] + 0.17 * d[0], p[1] + 0.17 * d[1]),
                    xytext=(p[0] - 0.17 * d[0], p[1] - 0.17 * d[1]), arrowprops=KW)
    ax.text(1.20, 1.00, r'$C$', fontsize=12, ha='left', va='bottom')
    # 小回路 C'：x1 出发上行绕 x0 再下行回实轴
    x1, cx0, cy0, r0 = -0.18, -0.18, 0.50, 0.12
    t = np.linspace(0, 2 * np.pi, 100)
    ax.plot(cx0 + r0 * np.cos(t), cy0 + r0 * np.sin(t), 'k-', lw=1.2)
    ax.add_patch(plt.Circle((cx0, cy0), 0.028, color='k'))
    ax.plot([x1 - 0.09, x1 - 0.09], [0, cy0], 'k-', lw=1.2)
    ax.plot([x1 + 0.09, x1 + 0.09], [0, cy0], 'k-', lw=1.2)
    ax.annotate('', xy=(x1 - 0.09, 0.17), xytext=(x1 - 0.09, 0.38), arrowprops=KW)  # 左线向下
    ax.annotate('', xy=(x1 + 0.09, 0.36), xytext=(x1 + 0.09, 0.15), arrowprops=KW)  # 右线向上
    ax.text(cx0 + r0 + 0.03, cy0 + r0 + 0.01, r'$x_0$', fontsize=11, ha='left', va='bottom')
    ax.text(x1 - 0.19, 0.32, r"$C'$", fontsize=12, ha='right', va='center')
    ax.text(x1 - 0.02, -0.10, r'$x_1$', fontsize=11, ha='center', va='top')
    ax.set_xlim(-1.92, 1.98)
    ax.set_ylim(-0.42, 1.80)
    ax.set_aspect('equal')
    save(fig, 19)


# ---------------------------------------------------------------- 图20 (p213)
def fig_20():
    fig, ax = new_ax(2.9, 3.0)
    R = 1.0
    # 球面与赤道
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(R * np.cos(t), R * np.sin(t), 'k-', lw=1.3)
    beq = 0.30
    ax.plot(R * np.cos(t), beq * np.sin(t), 'k-', lw=1.3)          # 赤道椭圆
    ax.plot([-1.30, R], [0, 0], 'k-', lw=1.1)                       # 赤道水平直径（x 轴线）
    # 大倾斜虚椭圆（绕节线转 beta 时 z 端点的大圆）
    rot = np.radians(-22)
    ea, eb = 1.06, 0.88
    xs = ea * np.cos(t); ys = eb * np.sin(t)
    xr = 0.03 + xs * np.cos(rot) - ys * np.sin(rot)
    yr = 0.05 + xs * np.sin(rot) + ys * np.cos(rot)
    ax.plot(xr, yr, 'k--', lw=0.9, dashes=(5, 3.5))
    # z 轴
    ax.plot([0, 0], [0, 1.05], 'k-', lw=1.2)
    ax.annotate('', xy=(0, 1.42), xytext=(0, 1.06), arrowprops=KW)
    ax.text(0.08, 1.36, r'$z$', fontsize=11, ha='left', va='center')
    # x 轴
    ax.annotate('', xy=(-1.42, 0), xytext=(-1.18, 0), arrowprops=KW)
    ax.text(-1.38, 0.09, r'$x$', fontsize=11, ha='right', va='bottom')
    # y 轴（指向观察者，投影左下）
    ay = np.radians(232)
    ax.plot([0, 0.70 * np.cos(ay)], [0, 0.70 * np.sin(ay)], 'k-', lw=1.2)
    ax.annotate('', xy=(0.92 * np.cos(ay), 0.92 * np.sin(ay)),
                xytext=(0.74 * np.cos(ay), 0.74 * np.sin(ay)), arrowprops=KW)
    ax.text(1.00 * np.cos(ay), 1.00 * np.sin(ay), r'$y$', fontsize=11, ha='center', va='center')
    # 节线 ON（点划线，指向赤道上 N 点）与 N
    Npt = (0.614, -0.237)                              # 赤道椭圆上，屏幕角约 -21 度
    thN = np.arctan2(Npt[1], Npt[0])
    ax.plot([0, Npt[0] * 1.08], [0, Npt[1] * 1.08], 'k-.', lw=0.9, dashes=(6, 2, 1, 2))
    ax.text(Npt[0] + 0.06, Npt[1] - 0.13, r'$N$', fontsize=11, ha='left', va='center')
    # alpha 弧（赤道面内，从 x 轴沿前沿到节线方向，箭头指向 ON）
    ta = np.radians(np.linspace(180, 308, 80))
    ax.plot(0.62 * np.cos(ta), 0.186 * np.sin(ta), 'k-', lw=1.0)
    da = (-np.sin(np.radians(308)), 0.30 * np.cos(np.radians(308)))
    nn = np.hypot(*da); da = (da[0] / nn, da[1] / nn)
    pa = (0.62 * np.cos(np.radians(308)), 0.186 * np.sin(np.radians(308)))
    ax.annotate('', xy=(pa[0] + 0.15 * da[0], pa[1] + 0.15 * da[1]),
                xytext=(pa[0] - 0.03 * da[0], pa[1] - 0.03 * da[1]), arrowprops=KW)
    ax.text(-0.36, -0.32, r'$\alpha$', fontsize=12, ha='center', va='center')
    # z' 轴（内侧点划，外侧实线箭头）
    azp = np.radians(150)
    dz = (np.cos(azp), np.sin(azp))
    ax.plot([0, 0.74 * dz[0]], [0, 0.74 * dz[1]], 'k-.', lw=0.9, dashes=(6, 2, 1, 2))
    ax.plot([0.78 * dz[0], 1.12 * dz[0]], [0.78 * dz[1], 1.12 * dz[1]], 'k-', lw=1.2)
    ax.annotate('', xy=(1.32 * dz[0], 1.32 * dz[1]),
                xytext=(1.14 * dz[0], 1.14 * dz[1]), arrowprops=KW)
    ax.text(1.44 * dz[0], 1.44 * dz[1], r"$z'$", fontsize=11, ha='center', va='center')
    # beta 弧（z 到 z'），箭头指向 z'
    b0, b1 = 90, 138
    tb = np.radians(np.linspace(b0, b1, 50))
    ax.plot(0.58 * np.cos(tb), 0.58 * np.sin(tb), 'k-', lw=1.0)
    ddir = (-np.sin(np.radians(b1)), np.cos(np.radians(b1)))
    pe = (0.58 * np.cos(np.radians(b1)), 0.58 * np.sin(np.radians(b1)))
    ax.annotate('', xy=(pe[0] + 0.16 * ddir[0], pe[1] + 0.16 * ddir[1]),
                xytext=(pe[0] - 0.02 * ddir[0], pe[1] - 0.02 * ddir[1]), arrowprops=KW)
    ax.text(-0.28, 0.84, r'$\beta$', fontsize=12, ha='center', va='center')
    # delta alpha（z 旁标注）
    ax.text(-0.09, 1.24, r'$\delta\alpha$', fontsize=11, ha='right', va='center')
    # delta gamma（z' 旁小箭头 + 标注）
    wp = (-np.sin(azp), -np.cos(azp))                  # z' 轴右上侧法向 (0.5, 0.866)
    ax.annotate('', xy=(-0.66, 0.40), xytext=(-0.52, 0.50), arrowprops=KWS)
    ax.text(0.97 * dz[0] + 0.21 * wp[0], 0.97 * dz[1] + 0.21 * wp[1], r'$\delta\gamma$',
            fontsize=11, ha='center', va='center')
    # gamma 弧（节线到 y'）
    ydir = np.radians(-10)
    tg = np.radians(np.linspace(np.degrees(thN), np.degrees(ydir), 30))
    ax.plot(0.50 * np.cos(tg), 0.50 * np.sin(tg), 'k-', lw=1.0)
    dg = (-np.sin(ydir), np.cos(ydir))
    pge = (0.50 * np.cos(ydir), 0.50 * np.sin(ydir))
    ax.annotate('', xy=(pge[0] + 0.15 * dg[0], pge[1] + 0.15 * dg[1]),
                xytext=(pge[0] - 0.03 * dg[0], pge[1] - 0.03 * dg[1]), arrowprops=KW)
    ax.text(0.64 * np.cos(np.radians(-16)), 0.64 * np.sin(np.radians(-16)), r'$\gamma$',
            fontsize=12, ha='center', va='center')
    # y' 轴（虚线 + 实箭头，指向右前）
    ax.plot([0, 0.80 * np.cos(ydir)], [0, 0.80 * np.sin(ydir)], 'k--', lw=0.9, dashes=(4, 2.5))
    ax.annotate('', xy=(0.98 * np.cos(ydir), 0.98 * np.sin(ydir)),
                xytext=(0.84 * np.cos(ydir), 0.84 * np.sin(ydir)), arrowprops=KW)
    ax.text(1.05 * np.cos(ydir), 1.05 * np.sin(ydir) + 0.02, r"$y'$", fontsize=11,
            ha='left', va='center')
    # delta beta（沿节线的小箭头 + 标注）
    ax.annotate('', xy=(0.66 * np.cos(np.radians(-26)), 0.66 * np.sin(np.radians(-26))),
                xytext=(0.40 * np.cos(np.radians(-15)), 0.40 * np.sin(np.radians(-15))),
                arrowprops=KWS)
    ax.text(0.28, -0.30, r'$\delta\beta$', fontsize=11, ha='center', va='center')
    # x' 轴（先虚后实箭头，指向左下）
    axp = np.radians(240)
    dx = (np.cos(axp), np.sin(axp))
    ax.plot([0, 0.66 * dx[0]], [0, 0.66 * dx[1]], 'k--', lw=0.9, dashes=(4, 2.5))
    ax.plot([0.64 * dx[0], 0.92 * dx[0]], [0.64 * dx[1], 0.92 * dx[1]], 'k-', lw=1.2)
    ax.annotate('', xy=(1.08 * dx[0], 1.08 * dx[1]),
                xytext=(0.94 * dx[0], 0.94 * dx[1]), arrowprops=KW)
    ax.text(1.17 * dx[0], 1.17 * dx[1] - 0.04, r"$x'$", fontsize=11, ha='center', va='center')
    ax.text(0.10, 0.09, r'$O$', fontsize=11, ha='left', va='bottom')
    ax.set_xlim(-1.62, 1.55)
    ax.set_ylim(-1.42, 1.72)
    ax.set_aspect('equal')
    save(fig, 20)


# ---------------------------------------------------------------- 图21 (p230)
def _young(ax, x0, ytop, rows, s):
    """画一个杨图：rows 自上而下各行的格数，s 为格边长."""
    n, maxc = len(rows), max(rows)
    cols = [sum(1 for r in rows if r > j) for j in range(maxc)]  # 各列格数
    # 横线：第 i 条(0..n)跨越上下两行的较短者
    for i in range(n + 1):
        if i == 0:
            w = rows[0]
        elif i == n:
            w = rows[-1]
        else:
            w = min(rows[i - 1], rows[i])
        ax.plot([x0, x0 + w * s], [ytop - i * s, ytop - i * s], 'k-', lw=1.3)
    # 竖线：第 j 条(0..maxc)跨越左右两列的较高者
    for j in range(maxc + 1):
        h = cols[0] if j == 0 else cols[j - 1]
        ax.plot([x0 + j * s, x0 + j * s], [ytop, ytop - h * s], 'k-', lw=1.3)


def fig_21():
    fig, ax = new_ax(3.1, 1.55)
    s = 0.3
    _young(ax, 0.0, 0.0, [6, 4, 4, 3, 3, 1, 1], s)
    _young(ax, 2.6, 0.0, [7, 5, 5, 3, 1, 1], s)
    ax.set_xlim(-0.12, 4.85)
    ax.set_ylim(-2.45, 0.12)
    ax.set_aspect('equal')
    save(fig, 21)


# ---------------------------------------------------------------- 图22 (p232)
def fig_22():
    fig, ax = new_ax(2.7, 2.3)
    s = 0.3
    # 上排（phi）
    _young(ax, 0.30, 0.0, [1, 1, 1, 1], s)
    _young(ax, 1.60, 0.0, [2, 1, 1], s)
    _young(ax, 3.10, 0.0, [2, 2], s)
    # 下排（chi）
    y2 = -1.85
    _young(ax, 0.30, y2, [4], s)
    _young(ax, 1.60, y2, [3, 1], s)
    _young(ax, 3.10, y2, [2, 2], s)
    ax.text(0.10, -0.55, r'$\varphi$', fontsize=12, ha='right', va='center')
    ax.text(0.10, y2 - 0.6, r'$\chi$', fontsize=12, ha='right', va='center')
    ax.text(0.30 + 2 * s, y2 - 4.6 * s, r'$S{=}2$', fontsize=10, ha='center', va='top')
    ax.text(1.60 + 1.5 * s, y2 - 4.6 * s, r'$S{=}1$', fontsize=10, ha='center', va='top')
    ax.text(3.10 + 1 * s, y2 - 4.6 * s, r'$S{=}0$', fontsize=10, ha='center', va='top')
    ax.set_xlim(-0.30, 4.30)
    ax.set_ylim(-4.35, 0.15)
    ax.set_aspect('equal')
    save(fig, 22)


if __name__ == '__main__':
    import sys
    args = sys.argv[1:]
    fns = {'13': fig_13, '14': fig_14, '15': fig_15, '16': fig_16, '17': fig_17,
           '18': fig_18, '19': fig_19, '20': fig_20, '21': fig_21, '22': fig_22}
    if args:
        for k in args:
            fns[k]()
    else:
        for k in sorted(fns):
            fns[k]()
    print('done')
