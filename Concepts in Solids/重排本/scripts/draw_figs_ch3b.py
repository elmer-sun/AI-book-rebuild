# -*- coding: utf-8 -*-
"""重绘 Anderson《Concepts in Solids》图 32-41（第 3 章 B.2/C 节，批次 ch3b）。
图 32: p128(书113)  图 33: p129(书114)  图 34: p131(书116)  图 35: p135(书120)
图 36: p137(书122)  图 37: p140(书125)  图 38: p142(书127)  图 39: p143(书128)
图 40: p144(书129)  图 41: p145(书130)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
import numpy as np
import os

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

OUT = r'E:\AI整理书籍\安德森\重排本\figures'
PREV = os.path.join(OUT, 'preview')
os.makedirs(PREV, exist_ok=True)


def save(fig, key):
    fig.savefig(os.path.join(OUT, f'fig_{key}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, f'fig_{key}.png'), bbox_inches='tight', pad_inches=0.03, dpi=150)
    plt.close(fig)


def arrow(ax, p0, p1, ms=11, lw=1.2, style='-|>'):
    """带实心箭头的线段（覆盖在普通线上用）。"""
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, color='k', lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def bez2(p0, p1, p2, n=140):
    """二次 Bezier 采样。"""
    t = np.linspace(0, 1, n)
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    return x, y


def bez3(p0, p1, p2, p3, n=200):
    """三次 Bezier 采样。"""
    t = np.linspace(0, 1, n)
    x = ((1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0]
         + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0])
    y = ((1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1]
         + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1])
    return x, y


def wavy(p0, p1, amp=0.10, nh=4.5, t0=0.0, t1=0.97, n=400):
    """从 p0 到 p1 的波浪线（声子线）。"""
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    d = p1 - p0
    L = np.hypot(*d)
    u = d / L
    perp = np.array([-u[1], u[0]])
    t = np.linspace(t0, t1, n)
    pts = p0 + t[:, None] * d + (amp * np.sin(2 * np.pi * nh * t))[:, None] * perp
    return pts[:, 0], pts[:, 1]


# ---------------------------------------------------------------- 图 32
def fig_32():
    """纵声子波动示意：上方一条完整正弦波，下方 3x9 原子阵列，
    箭头长度按 sin(2pi x/lambda) 变化（节点在 1、5、9 列）。"""
    fig, ax = plt.subplots(figsize=(4.3, 2.2))
    ax.set_xlim(-0.45, 8.45)
    ax.set_ylim(-1.85, 2.55)
    ax.set_aspect('equal')
    ax.axis('off')

    # 正弦波 + 基线
    ax.plot([0, 8], [1.36, 1.36], color='k', lw=1.0)
    xs = np.linspace(0, 8, 500)
    ax.plot(xs, 1.36 + 0.85 * np.sin(2 * np.pi * xs / 8), color='k', lw=1.4)

    # 原子阵列：3 行 x 9 列
    r = 0.16
    for y0 in (0, -0.69, -1.38):
        for j in range(9):
            x = j
            ax.add_patch(Circle((x, y0), r, fill=False, lw=1.1, edgecolor='k'))
            u = np.sin(2 * np.pi * j / 8)
            if abs(u) > 0.05:
                L = 0.58 * u * abs(u)          # 箭长 ~ 位移平方（按原图比例）
                arrow(ax, (x + np.sign(u) * r, y0), (x + np.sign(u) * (r + abs(L)), y0),
                      ms=8, lw=1.0)
    save(fig, 32)


# ---------------------------------------------------------------- 图 33
def _panel33(ax, x0):
    """单个声子谱面板的坐标架：omega 轴、k 轴、BZ 边界线与标注。"""
    ax.plot([x0, x0], [0, 1.25], color='k', lw=1.0)          # omega 轴
    ax.plot([x0, x0 + 1.08], [0, 0], color='k', lw=1.0)      # k 轴
    ax.plot([x0 + 1, x0 + 1], [0, 0.88], color='k', lw=1.0)  # BZ 边界
    ax.text(x0 - 0.06, 1.24, r'$\omega$', ha='center', va='center')
    ax.text(x0 + 1.10, -0.015, r'$k$', ha='left', va='center')
    ax.text(x0 - 0.05, -0.03, r'$0$', ha='center', va='center')
    ax.text(x0 + 1.0, 0.945, 'BZ boundary', ha='center', va='bottom', fontsize=9)


def fig_33():
    """声子谱示意：左单原子（wl, wt），右离子双原子（wlo, wto, wla, wta）。"""
    fig, ax = plt.subplots(figsize=(4.8, 2.6))
    ax.set_xlim(-0.12, 2.68)
    ax.set_ylim(-0.14, 1.46)
    ax.axis('off')

    x1, x2 = 0.0, 1.48   # 两面板原点
    _panel33(ax, x1)
    _panel33(ax, x2)

    # 左：声学支
    xl = np.linspace(0, 1, 250)
    wl = 0.64 * (1 - np.exp(-xl / 0.40))
    wt = 0.40 * (1 - np.exp(-xl / 0.45))
    ax.plot(x1 + xl, wl, 'k', lw=1.3)
    ax.plot(x1 + xl, wt, 'k', lw=1.3)
    ax.text(x1 + 0.50, 0.64 * (1 - np.exp(-0.5 / 0.40)) + 0.07, r'$\omega_{\rm l}$',
            ha='center', fontsize=11)
    ax.text(x1 + 0.58, 0.40 * (1 - np.exp(-0.58 / 0.45)) + 0.06, r'$\omega_{\rm t}$',
            ha='center', fontsize=11)

    # 右：光学支 + 声学支
    bx, by = bez2((0, 0.80), (0.55, 0.78), (1, 0.58))
    ax.plot(x2 + bx, by, 'k', lw=1.3)                         # w_lo
    cx, cy = bez2((0, 0.48), (0.50, 0.475), (1, 0.385))
    ax.plot(x2 + cx, cy, 'k', lw=1.3)                         # w_to
    wla = 0.29 * (1 - np.exp(-1.9 * xl)) / (1 - np.exp(-1.9))
    wta = 0.145 * (1 - np.exp(-1.9 * xl)) / (1 - np.exp(-1.9))
    ax.plot(x2 + xl, wla, 'k', lw=1.3)
    ax.plot(x2 + xl, wta, 'k', lw=1.3)
    ax.text(x2 + 0.30, 0.785, r'$\omega_{\rm lo}$', ha='center', fontsize=11)
    ax.text(x2 + 0.25, 0.525, r'$\omega_{\rm to}$', ha='center', fontsize=11)
    ax.text(x2 + 0.28, 0.295, r'$\omega_{\rm la}$', ha='center', fontsize=11)
    ax.text(x2 + 0.47, 0.135, r'$\omega_{\rm ta}$', ha='center', fontsize=11)
    save(fig, 33)


# ---------------------------------------------------------------- 图 34
def fig_34():
    """电子-声子散射顶点：入射电子 (k,n)，出射电子 (k+K,n')，波状声子线 K。"""
    fig, ax = plt.subplots(figsize=(4.0, 2.5))
    ax.set_xlim(-2.05, 2.65)
    ax.set_ylim(-1.55, 1.65)
    ax.set_aspect('equal')
    ax.axis('off')

    V = (0.0, 0.0)
    # 入射电子线
    ax.plot([-1.55, 0], [-1.05, 0], 'k', lw=1.2)
    arrow(ax, (-0.88, -0.595), (-0.38, -0.257), ms=13, lw=1.2)
    ax.text(-0.52, -0.86, r'$k$, n', ha='center', fontsize=12)
    # 出射电子线
    ax.plot([0, 2.05], [0, 0], 'k', lw=1.2)
    arrow(ax, (0.62, 0), (1.18, 0), ms=13, lw=1.2)
    ax.text(0.95, 0.17, r"$k{+}K,\ \mathrm{n}^{\prime}$", ha='left', fontsize=12)
    # 声子波状线
    wx, wy = wavy(V, (-1.55, 1.25), amp=0.10, nh=4.5)
    ax.plot(wx, wy, 'k', lw=1.2)
    ax.text(-0.88, 0.92, r'$K$', ha='center', fontsize=13)
    save(fig, 34)


# ---------------------------------------------------------------- 图 35
def fig_35():
    """E(k) 抛物线与声子直线 hbar*ck+const. 相切，K_o 标出极小值位置。"""
    fig, ax = plt.subplots(figsize=(3.9, 3.0))
    ax.set_xlim(-0.10, 1.32)
    ax.set_ylim(-0.18, 1.02)
    ax.axis('off')

    ax.plot([0, 0], [0, 0.95], 'k', lw=1.0)          # E 轴
    ax.plot([0, 1.22], [0, 0], 'k', lw=1.0)          # 横轴
    ax.text(-0.055, 0.90, r'$E$', ha='center', va='center', fontsize=13)

    K0, Emin, a = 0.60, 0.36, 3.0
    xp = np.linspace(0.22, 0.98, 300)
    ax.plot(xp, Emin + a * (xp - K0) ** 2, 'k', lw=1.4)
    ax.text(0.255, 0.845, r'$E(k)$', ha='left', fontsize=12)

    # K_o 垂直线
    ax.plot([K0, K0], [Emin, -0.07], 'k', lw=0.9)
    ax.text(K0, -0.135, r'$K_{\rm o}$', ha='center', va='center', fontsize=12)

    # 切线（hbar ck + const.）
    xt = 0.80
    yt = Emin + a * (xt - K0) ** 2
    m = 2 * a * (xt - K0)
    ax.plot([0.50, 1.08], [yt + m * (0.50 - xt), yt + m * (1.08 - xt)], 'k', lw=1.2)
    ax.text(0.665, 0.27, r'$\hbar ck$ + const.', ha='left', fontsize=12)
    save(fig, 35)


# ---------------------------------------------------------------- 图 36
def fig_36():
    """费米球截面内的矢量三角：k 与 k+K 均至球面，K 连接两端点。"""
    fig, ax = plt.subplots(figsize=(3.6, 3.4))
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.45, 1.35)
    ax.set_aspect('equal')
    ax.axis('off')

    R = 1.05
    ax.add_patch(Circle((0, 0), R, fill=False, lw=1.1, edgecolor='k'))
    P = (-0.06, 0.0)
    ktip = (R * np.cos(np.deg2rad(0.5)), R * np.sin(np.deg2rad(0.5)))
    kK = (R * np.cos(np.deg2rad(242)), R * np.sin(np.deg2rad(242)))

    arrow(ax, P, ktip, ms=13, lw=1.4)
    arrow(ax, P, kK, ms=13, lw=1.4)
    arrow(ax, ktip, kK, ms=13, lw=1.4)

    ax.text(0.42, 0.13, r'$k$', ha='center', fontsize=13)
    ax.text(-0.52, -0.28, r'$k{+}K$', ha='center', fontsize=13)
    ax.text(0.34, -0.56, r'$K$', ha='center', fontsize=13)
    save(fig, 36)


# ---------------------------------------------------------------- 图 37
def fig_37():
    """hbar/tau 对 k_B T：强耦合（虚线，~T^3 到 ~T）、斜率 1 直线、弱耦合（~T^3 转线性）。"""
    fig, ax = plt.subplots(figsize=(4.3, 3.5))
    ax.set_xlim(-0.05, 1.14)
    ax.set_ylim(-0.05, 1.10)
    ax.axis('off')

    ax.plot([0, 0], [0, 1.0], 'k', lw=1.0)
    ax.plot([0, 1.05], [0, 0], 'k', lw=1.0)
    ax.text(-0.055, 0.88, r'$\dfrac{\hbar}{\tau}$', ha='center', va='center', fontsize=13)
    ax.text(1.02, 0.05, r'$k_{\rm B}T$', ha='center', fontsize=12)

    # 斜率 = 1 直线
    ax.plot([0, 0.575], [0, 0.865], 'k', lw=1.2)
    ax.text(0.60, 0.755, 'Slope = 1', ha='left', fontsize=11)

    # 强耦合虚线
    sx, sy = bez3((0, 0), (0.085, 0.004), (0.155, 0.30), (0.272, 0.875))
    ax.plot(sx, sy, 'k', lw=1.2, ls=(0, (5, 4)))
    ax.text(0.285, 0.865, r'$\sim T$', ha='left', fontsize=12)
    ax.text(0.055, 0.99, '"Strong\ncoupling"', ha='left', va='top', fontsize=10.5)

    # 弱耦合实线
    wx, wy = bez3((0, 0), (0.135, 0.002), (0.295, 0.125), (0.80, 0.475))
    ax.plot(wx, wy, 'k', lw=1.3)
    ax.text(0.815, 0.545, '"Weak\ncoupling"', ha='left', va='top', fontsize=10.5)

    ax.text(0.155, 0.175, r'$\sim T^3$', ha='left', fontsize=11)
    ax.text(0.27, 0.09, r'$\sim T^3$', ha='left', fontsize=11)
    save(fig, 37)


# ---------------------------------------------------------------- 图 38
def fig_38():
    """费米面附近的散射几何：k' -> k'+q；k_F+a=k 及 k -> k-q。"""
    fig, ax = plt.subplots(figsize=(4.3, 3.0))
    ax.set_xlim(-1.30, 2.75)
    ax.set_ylim(-1.60, 1.25)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.add_patch(Circle((0, 0), 1.0, fill=False, lw=1.2, edgecolor='k'))

    # k' -> k'+q
    kp = (-0.01, -0.70)
    kpq = (0.21, -1.28)
    arrow(ax, kp, kpq, ms=12, lw=1.3)
    ax.text(0.11, -0.63, r"$k'$", ha='left', fontsize=13)
    ax.text(0.30, -1.28, r"$k'{+}q$", ha='left', va='center', fontsize=13)

    # a: 费米面上一点 -> k
    kF = (0.853, -0.522)
    kk = (1.39, -0.86)
    arrow(ax, kF, kk, ms=12, lw=1.3)
    ax.text(1.03, -0.55, r'$a$', ha='left', fontsize=13)
    ax.text(1.47, -0.88, r'$k_F + a = k$', ha='left', va='center', fontsize=13)

    # k -> k-q
    kq = (1.19, -0.25)
    arrow(ax, kk, kq, ms=12, lw=1.3)
    ax.text(1.13, -0.09, r'$k{-}q$', ha='left', fontsize=13)
    save(fig, 38)


# ---------------------------------------------------------------- 图 39
def fig_39():
    """两球几何：大球（费米球，k_F 半径线）与上球相交；公共弦、竖直线、
    k/k-q（左）、k'+q/k'（右）、虚线水平线与两个 theta 角。"""
    fig, ax = plt.subplots(figsize=(3.8, 4.1))
    ax.set_xlim(-1.80, 1.80)
    ax.set_ylim(-1.60, 2.15)
    ax.set_aspect('equal')
    ax.axis('off')

    R, r, c = 1.4, 1.0, 0.95     # 大球半径 / 上球半径 / 上球心高度
    ax.add_patch(Circle((0, 0), R, fill=False, lw=1.2, edgecolor='k'))
    ax.add_patch(Circle((0, c), r, fill=False, lw=1.2, edgecolor='k'))

    # 交点（圆心均在 y 轴上）
    yI = (R ** 2 - r ** 2 + c ** 2) / (2 * c)
    xI = np.sqrt(R ** 2 - yI ** 2)
    IL, IR = (-xI, yI), (xI, yI)

    # 竖直线、公共弦
    for x in (IL[0], IR[0]):
        ax.plot([x, x], [0.50, 1.80], 'k', lw=1.0)
    ax.plot([IL[0], IR[0]], [yI, yI], 'k', lw=1.1)

    # 上下虚线（k 与 k-q 能级）
    for y in (1.07, 0.89):
        ax.plot([IL[0], IR[0]], [y, y], 'k', lw=1.0, ls=(0, (5, 4)))

    # 左：q 向下箭头；右：向上箭头
    arrow(ax, (IL[0], 1.07), (IL[0], 0.89), ms=9, lw=1.2)
    arrow(ax, (IR[0], 0.89), (IR[0], 1.07), ms=9, lw=1.2)

    # 两交点到大球心的连线 + 球心点 + k_F 半径线
    ax.plot([IL[0], 0], [yI, 0], 'k', lw=1.0)
    ax.plot([IR[0], 0], [yI, 0], 'k', lw=1.0)
    ax.plot([0], [0], 'ko', ms=3.5)
    kFend = (R * np.cos(np.deg2rad(-76)), R * np.sin(np.deg2rad(-76)))
    ax.plot([0, kFend[0]], [0, kFend[1]], 'k', lw=1.1)
    ax.text(0.17, -0.46, r'$k_F$', ha='left', fontsize=13)

    # theta 角弧线
    th = np.degrees(np.arctan2(yI, xI))
    ax.add_patch(Arc(IL, 0.76, 0.76, theta1=-th, theta2=0, lw=0.9, color='k'))
    ax.add_patch(Arc(IR, 0.76, 0.76, theta1=180, theta2=180 + th, lw=0.9, color='k'))
    ax.text(-0.50, 0.775, r'$\theta$', ha='center', fontsize=13)
    ax.text(0.56, 1.00, r'$\theta$', ha='center', fontsize=13)

    # 标注
    ax.text(-0.92, 1.13, r'$k$', ha='left', fontsize=13)
    ax.text(-1.13, 0.885, r'$k - q$', ha='right', va='center', fontsize=13)
    ax.text(IL[0] + 0.14, 1.005, r'$a$', ha='left', fontsize=10.5)
    ax.text(1.06, 1.075, r"$k'{+}q$", ha='left', fontsize=13)
    ax.text(1.06, 0.70, r"$k'$", ha='left', fontsize=13)
    ax.text(-1.28, 1.16, r'$q$', ha='center', fontsize=13)
    save(fig, 39)


# ---------------------------------------------------------------- 图 40
def fig_40():
    """G_k(t)：初始快衰减后的阻尼振荡，包络 ±e^{-t/tau}。"""
    fig, ax = plt.subplots(figsize=(4.4, 3.1))
    ax.set_xlim(-0.16, 1.30)
    ax.set_ylim(-1.35, 1.38)
    ax.axis('off')

    ax.plot([0, 0], [-1.12, 1.14], 'k', lw=1.0)
    ax.plot([0, 1.12], [0, 0], 'k', lw=1.0)
    ax.text(-0.055, 1.06, r'$G_k(t)$', ha='right', fontsize=13)
    ax.text(1.15, 0.02, r'$t$', ha='left', fontsize=13)

    tau = 0.55
    xe = np.linspace(0, 1.02, 300)
    env = np.exp(-xe / tau)
    ax.plot(xe, env, 'k', lw=0.9)
    ax.plot(xe, -env, 'k', lw=0.9)

    # 分段升余弦穿过各极值点
    ts = [0, 0.075, 0.17, 0.28, 0.385, 0.48, 0.575, 0.665, 0.755, 0.855]
    As = [1.0, -0.40, 0.44, -0.60, 0.46, -0.44, 0.31, -0.29, 0.20, -0.145]
    xs, ys = [], []
    for i in range(len(ts) - 1):
        u = np.linspace(0, 1, 60)
        y = (As[i] + As[i + 1]) / 2 + (As[i] - As[i + 1]) / 2 * np.cos(np.pi * u)
        xs.append(ts[i] + (ts[i + 1] - ts[i]) * u)
        ys.append(y)
    ax.plot(np.concatenate(xs), np.concatenate(ys), 'k', lw=1.4)

    # 包络标注 e^{-t/tau}
    ax.text(0.52, 0.70, r'$\mathrm{e}^{-t/\tau}$', ha='center', fontsize=12)
    arrow(ax, (0.475, 0.635), (0.425, 0.49), ms=8, lw=0.9)
    save(fig, 40)


# ---------------------------------------------------------------- 图 41
def fig_41():
    """谱密度 Im G_k(w)：金属（尖峰叠在连续背景上）与绝缘体（delta 尖峰 + 连续带）。"""
    fig, ax = plt.subplots(figsize=(4.8, 2.4))
    ax.set_xlim(-0.42, 2.85)
    ax.set_ylim(-0.34, 1.10)
    ax.axis('off')

    # ---------- Metal ----------
    ax.plot([0, 0], [0, 0.80], 'k', lw=1.0)
    ax.plot([0, 0.80], [0, 0], 'k', lw=1.0)
    ax.text(0.40, 0.93, 'Metal', ha='center', fontsize=12)
    ax.text(-0.035, 0.775, r'Im $G_k(\omega)$', ha='right', va='center', fontsize=11)
    ax.text(0.83, 0.015, r'$\hbar\omega$', ha='left', va='center', fontsize=12)

    xm = np.linspace(0, 0.76, 700)
    b = 0.07 * xm + 0.55 * xm ** 2
    pk = 0.38 / (1 + (np.abs(xm - 0.405) / 0.034) ** 2.5)
    ax.plot(xm, b + pk, 'k', lw=1.3)

    arrow(ax, (0.377, 0.335), (0.433, 0.335), ms=5.5, lw=0.9, style='<|-|>')
    ax.text(0.452, 0.335, r'$2\hbar/\tau$', ha='left', va='center', fontsize=12)

    ax.plot([0.405, 0.405], [-0.005, -0.035], 'k', lw=0.9)
    ax.text(0.405, -0.10, r'$E_k$', ha='center', fontsize=12)
    arrow(ax, (0.305, -0.155), (0.505, -0.155), ms=8, lw=0.9, style='<|-|>')
    ax.plot([0.305, 0.305], [-0.142, -0.168], 'k', lw=0.9)
    ax.plot([0.505, 0.505], [-0.142, -0.168], 'k', lw=0.9)
    ax.text(0.405, -0.235, r'$\epsilon$', ha='center', fontsize=13)

    # ---------- Insulator ----------
    X = 1.60
    ax.plot([X, X], [0, 0.80], 'k', lw=1.0)
    ax.plot([X, X + 0.80], [0, 0], 'k', lw=1.0)
    ax.text(X + 0.40, 0.93, 'Insulator', ha='center', fontsize=12)
    ax.text(X - 0.035, 0.775, r'Im $G_k(\omega)$', ha='right', va='center', fontsize=11)
    ax.text(X + 0.83, 0.015, r'$\hbar\omega$', ha='left', va='center', fontsize=12)

    xsp = X + 0.26
    ax.plot([xsp, xsp], [0, 0.46], 'k', lw=1.4)
    ax.text(xsp, -0.10, r'$E_k$', ha='center', fontsize=12)

    xc = np.linspace(X + 0.42, X + 0.78, 200)
    ax.plot(xc, 0.30 * np.sqrt((xc - (X + 0.42)) / 0.36), 'k', lw=1.3)
    save(fig, 41)


if __name__ == '__main__':
    for f in (fig_32, fig_33, fig_34, fig_35, fig_36,
              fig_37, fig_38, fig_39, fig_40, fig_41):
        f()
        print(f.__name__, 'done')
