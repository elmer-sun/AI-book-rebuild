# -*- coding: utf-8 -*-
"""
朗道《理论物理学教程》第9卷《统计物理学II》中文重排本 插图重绘 第二批：图10-图18
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p226/227/228/229/237/257/260/330/336）。
  图10 p226  §55习题1  克里尼希-彭尼模型周期方势阱 U(x)，区域 I/II/III
  图11 p227  §55习题1  方程(6)右侧 cos(k1a)+P sin(k1a)/(k1a) 图解（P=4，按公式计算）
  图12 p228  §55      弱周期场能谱：(a) 扩展区图 k 全轴 (b) 简约区图头两条能带
  图13 p229  §55习题3  准经典周期对称势（正弦势），阱底能级 ε0，特征点 x0
  图14 p237  §57      k 空间两条相邻轨道，最近间距 δk（抛物线型轨道支）
  图15 p257  §63      哑铃形费米面及三个极值截面（斜线阴影），箭头指场方向
  图16 p260  §63      H(B) 曲线的麦克斯韦等面积构造（ab/cd 亚稳段），上回线虚线
  图17 p330  §81      两固体 1、2 之间间隙 3（宽 l），x 轴垂直于表面
  图18 p336  §82      函数 φ_II、φ_IM、φ_AI(ε0)——按公式(82.4)数值积分绘制
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
from scipy.integrate import quad

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
    'hatch.linewidth': 0.55,
})

BASE = r"E:\AI整理书籍\朗道理论物理教程\卷9统计物理II"
FIGD = os.path.join(BASE, '重排本', 'figures')
PRED = os.path.join(BASE, '原书转换')
os.makedirs(FIGD, exist_ok=True)

LW_MAIN, LW_AUX = 1.4, 0.8
DASH = (4.5, 2.4)


def save(fig, n):
    fig.savefig(os.path.join(FIGD, f'fig{n}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRED, f'fig{n}_preview.png'), bbox_inches='tight',
                pad_inches=0.03, dpi=150)
    plt.close(fig)


def plain_axes(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def aline(ax, x0, y0, x1, y1, lw=1.1):
    """无箭头直线（坐标轴线）"""
    ax.plot([x0, x1], [y0, y1], 'k-', lw=lw, solid_capstyle='butt', zorder=5)


def pchip(pts):
    p = np.array(pts, dtype=float)
    return PchipInterpolator(p[:, 0], p[:, 1])


# ================================================================ 图 10
# p226  §55 习题1  周期方势阱：II (-b,0) 与 III (a,a+b) 为势垒，I (0,a) 为势阱。
def fig_10():
    b, a, h = 0.50, 0.90, 0.82
    fig, ax = plt.subplots(figsize=(2.75, 2.0))
    plain_axes(ax)
    ax.set_xlim(-1.05, 2.65)
    ax.set_ylim(-0.42, 1.62)
    # 底部基线（势阱底，粗）
    aline(ax, -0.72, 0, 2.48, 0, lw=1.7)
    # U(x) 竖轴：位于 -b（势垒 II 左缘）
    aline(ax, -b, 0, -b, h + 0.50, lw=1.2)
    ax.text(-b + 0.10, h + 0.44, r'$U(x)$', fontsize=12)
    # 两个势垒矩形（II 与 III）
    for x0 in (-b, a):
        ax.plot([x0, x0, x0 + b, x0 + b], [0, h, h, 0], 'k-', lw=1.5,
                solid_capstyle='butt', zorder=4)
    # 区域标号
    ax.text(-b + b / 2, 0.50 * h, r'$\mathrm{II}$', fontsize=12, ha='center', va='center')
    ax.text(a / 2, 0.50 * h, r'$\mathrm{I}$', fontsize=12, ha='center', va='center')
    ax.text(a + b / 2, 0.50 * h, r'$\mathrm{III}$', fontsize=12, ha='center', va='center')
    # 横轴刻度标号
    ax.text(-b, -0.20, r'$-b$', fontsize=12, ha='center', va='top')
    ax.text(0, -0.20, r'$0$', fontsize=12, ha='center', va='top')
    ax.text(a, -0.20, r'$a$', fontsize=12, ha='center', va='top')
    ax.text(a + b, -0.20, r'$a+b$', fontsize=12, ha='center', va='top')
    save(fig, 10)


# ================================================================ 图 11
# p227  §55 习题1  方程(6)右侧 f(k1a)=cos x + P sin x / x 的图解；±1 水平线，
# 允带边界处以竖线段投影到横轴。中心峰高 1+P ≈ 5.0（按页面测量，取 P=4）。
def _f11(x, P=4.0):
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    sm = np.abs(x) < 1e-9
    out[~sm] = np.cos(x[~sm]) + P * np.sin(x[~sm]) / x[~sm]
    out[sm] = 1.0 + P
    return out


def fig_11():
    P = 4.0
    XMAX = 4 * np.pi
    # 求所有 |f|=1 交点（允带边界）
    xs = np.linspace(1e-6, XMAX, 20000)
    fs = _f11(xs, P)
    cross = []
    for lev in (1.0, -1.0):
        g = fs - lev
        for i in np.where(g[:-1] * g[1:] < 0)[0]:
            cross.append(brentq(lambda t: _f11(t, P) - lev, xs[i], xs[i + 1]))
        for i in np.where(np.abs(g) < 2e-4)[0]:      # 恰在 nπ 处相切
            cross.append(xs[i])
    cross = sorted(set(round(c, 6) for c in cross))

    fig, ax = plt.subplots(figsize=(4.75, 1.75))
    plain_axes(ax)
    ax.set_xlim(-XMAX - 0.4, XMAX + 2.35)
    ax.set_ylim(-2.05, 5.85)
    # ±1 水平线（实线）
    aline(ax, -XMAX - 0.35, 1, XMAX + 1.15, 1, lw=1.0)
    aline(ax, -XMAX - 0.35, -1, XMAX + 1.15, -1, lw=1.0)
    # y=0 横轴：中段虚线 + 右端实线箭头
    ax.plot([-XMAX - 0.35, XMAX + 0.55], [0, 0], 'k--', lw=0.95, dashes=DASH)
    ax.annotate('', xy=(XMAX + 1.85, 0), xytext=(XMAX + 0.55, 0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                mutation_scale=11, shrinkA=0, shrinkB=0))
    ax.text(XMAX + 1.15, -0.42, r'$\kappa_1 a$', fontsize=12)
    # 中央竖轴
    aline(ax, 0, -1.62, 0, 5.42, lw=1.0)
    # 曲线
    xx = np.linspace(-XMAX, XMAX, 2500)
    ax.plot(xx, _f11(xx, P), 'k-', lw=LW_MAIN, zorder=4)
    # 允带边界竖线段：从横轴画到 ±1
    for c in cross:
        lev = 1.0 if _f11(c, P) > 0 else -1.0
        aline(ax, c, 0, c, lev, lw=0.85)
        aline(ax, -c, 0, -c, lev, lw=0.85)
    # 标号
    ax.text(0.32 * np.pi, 1.30, r'$+1$', fontsize=11, ha='left')
    ax.text(0.32 * np.pi, -1.42, r'$-1$', fontsize=11, ha='left', va='top')
    ax.text(0.14 * np.pi, 0.22, r'$0$', fontsize=11, ha='left')
    lab = {-4: (-4, -0.48, 'top'), -3: (-3, 0.30, 'bottom'), -2: (-2, -0.48, 'top'),
           -1: (-1, 0.30, 'bottom'), 1: (1, 0.30, 'bottom'), 2: (2, -0.48, 'top'),
           3: (3, 0.30, 'bottom'), 4: (4, -0.48, 'top')}
    for k, (x, y, va) in lab.items():
        t = (r'$-\pi$' if k == -1 else r'$\pi$') if abs(k) == 1 else r'$%d\pi$' % k
        ax.text(k * np.pi, y, t, fontsize=11, ha='center', va=va)
    save(fig, 11)


# ================================================================ 图 12
# p228  §55  弱周期场一维能谱。(a) 扩展区：ε(k) 抛物线在 ±π/a、±2π/a 处留间隙；
# (b) 简约区 [−π/a, π/a] 内头两条能带。
def _band1(k, w=0.075):
    """双平面波公式（以 ε0(π/a)=1 为单位）：第 1 支，|k|<=1，端点切线水平。"""
    k = np.asarray(k, dtype=float)
    e0, e0b = k * k, (k - 2.0) ** 2
    return 0.5 * (e0 + e0b) - np.sqrt((0.5 * (e0 - e0b)) ** 2 + w * w)


def fig_12():
    fig = plt.figure(figsize=(5.35, 2.55))
    axa = fig.add_axes([0.035, 0.17, 0.575, 0.80])
    axb = fig.add_axes([0.695, 0.17, 0.285, 0.80])
    for ax in (axa, axb):
        plain_axes(ax)

    # ---------- (a) 扩展区 ----------
    axa.set_xlim(-2.42, 2.62)
    axa.set_ylim(-0.30, 1.10)
    E1 = 0.33           # ε0(π/a) 的画面高度
    GAP = 0.055         # 禁带宽度画面值
    w = GAP / 2 / E1
    aline(axa, -2.32, 0, 2.42, 0, lw=1.3)          # k 轴
    axa.text(2.50, -0.13, r'$k$', fontsize=12, ha='center', va='top')
    aline(axa, 0, 0, 0, 1.06, lw=1.2)              # ε 轴
    axa.text(0.07, 1.0, r'$\varepsilon$', fontsize=12, ha='left')
    for s in (-1, 1):
        axa.plot([s, s], [0, 1.0], 'k--', lw=0.95, dashes=DASH)      # ±π/a 全高
        axa.plot([2 * s, 2 * s], [0, 0.55], 'k--', lw=0.95, dashes=DASH)  # ±2π/a 半高
    kk = np.linspace(-1, 1, 400)
    axa.plot(kk, E1 * _band1(kk, w), 'k-', lw=LW_MAIN, zorder=4)
    # 第 2 支：自 ±π/a 端点上方（水平切线）上升，接近 ±2π/a，虚线小段越界
    pts = [(1.0, E1 + GAP), (1.09, E1 + GAP + 0.004), (1.22, E1 + GAP + 0.025),
           (1.38, E1 + GAP + 0.075), (1.55, E1 + GAP + 0.16),
           (1.72, E1 + GAP + 0.28), (1.87, E1 + GAP + 0.43), (1.98, 0.95)]
    f2 = pchip(pts)
    k2 = np.linspace(1.0, 1.98, 200)
    axa.plot(k2, f2(k2), 'k-', lw=LW_MAIN, zorder=4)
    axa.plot([1.98, 2.17], [0.95, 1.05], 'k--', lw=1.1, dashes=DASH, zorder=4)
    k2m = np.linspace(-1.98, -1.0, 200)
    axa.plot(k2m, f2(-k2m), 'k-', lw=LW_MAIN, zorder=4)
    axa.plot([-2.17, -1.98], [1.05, 0.95], 'k--', lw=1.1, dashes=DASH, zorder=4)
    for x, t, s in ((-2, r'$-\dfrac{2\pi}{a}$', -2), (-1, r'$-\dfrac{\pi}{a}$', -1),
                    (1, r'$\dfrac{\pi}{a}$', 1), (2, r'$\dfrac{2\pi}{a}$', 2)):
        axa.text(x, -0.13, t, fontsize=11, ha='center', va='top')
    axa.text(0, -0.30, '(a)', fontsize=12, ha='center', va='top')

    # ---------- (b) 简约区 ----------
    axb.set_xlim(-1.42, 1.62)
    axb.set_ylim(-0.30, 1.10)
    aline(axb, -1.32, 0, 1.44, 0, lw=1.3)
    axb.text(1.52, -0.13, r'$k$', fontsize=12, ha='center', va='top')
    aline(axb, 0, 0, 0, 1.06, lw=1.2)
    axb.text(0.07, 1.0, r'$\varepsilon$', fontsize=12, ha='left')
    for s in (-1, 1):
        axb.plot([s, s], [0, 1.0], 'k--', lw=0.95, dashes=DASH)
    kk = np.linspace(-1, 1, 400)
    b1 = 0.10 - 0.075 * np.cos(np.pi * kk)          # 第 1 条能带：谷在 k=0
    axb.plot(kk, b1, 'k-', lw=LW_MAIN, zorder=4)
    b2 = 0.42 + 0.30 * np.cos(np.pi * kk / 2) ** 2.4  # 第 2 条能带：钟形，峰在 k=0
    axb.plot(kk, b2, 'k-', lw=LW_MAIN, zorder=4)
    axb.text(-1, -0.13, r'$-\dfrac{\pi}{a}$', fontsize=11, ha='center', va='top')
    axb.text(1, -0.13, r'$\dfrac{\pi}{a}$', fontsize=11, ha='center', va='top')
    axb.text(0, -0.30, '(b)', fontsize=12, ha='center', va='top')
    save(fig, 12)


# ================================================================ 图 13
# p229  §55 习题3  准经典周期对称势 U(x)∝1−cos(2πx/a)；ε0 虚线交曲线于 x0。
def fig_13():
    fig, ax = plt.subplots(figsize=(3.9, 1.62))
    plain_axes(ax)
    ax.set_xlim(-1.62, 1.78)
    ax.set_ylim(-0.34, 1.06)
    U0 = 0.21   # 振幅（半高）
    U = lambda x: (U0) - U0 * np.cos(2 * np.pi * x) + 0.21  # 0.21-0.42-0.63
    xx = np.linspace(-1.5, 1.5, 1200)
    ax.plot(xx, U(xx), 'k-', lw=LW_MAIN, zorder=4)
    x0 = 0.25
    e0 = U(x0)
    aline(ax, -1.52, 0, 1.62, 0, lw=1.3)            # x 轴
    ax.text(1.70, -0.12, r'$x$', fontsize=12, ha='center', va='top')
    aline(ax, 0, 0, 0, 0.99, lw=1.2)                # U(x) 轴
    ax.text(0.05, 0.90, r'$U(x)$', fontsize=12, ha='left')
    # 虚线：ε0 水平线（横过中央阱）、x0 与 ±a/2 竖线
    ax.plot([-x0, x0], [e0, e0], 'k--', lw=0.95, dashes=DASH)
    ax.plot([x0, x0], [0, e0], 'k--', lw=0.95, dashes=DASH)
    for s in (-0.5, 0.5):
        ax.plot([s, s], [0, U(s)], 'k--', lw=0.95, dashes=DASH)
    ax.plot([x0], [e0], 'k.', ms=3)
    ax.text(x0 + 0.05, e0 + 0.015, r'$\varepsilon_0$', fontsize=12, ha='left')
    ax.text(-0.5, -0.14, r'$-\dfrac{a}{2}$', fontsize=11, ha='center', va='top')
    ax.text(x0, -0.14, r'$x_0$', fontsize=12, ha='center', va='top')
    ax.text(0.5, -0.14, r'$\dfrac{a}{2}$', fontsize=11, ha='center', va='top')
    save(fig, 13)


# ================================================================ 图 14
# p237  §57  k 空间两条相邻轨道（抛物线型支），最近间距 δk，双箭头标出。
def fig_14():
    fig, ax = plt.subplots(figsize=(2.4, 2.42))
    plain_axes(ax)
    ax.set_xlim(-1.32, 1.42)
    ax.set_ylim(-1.30, 1.36)
    d, al = 0.30, 0.33
    yy = np.linspace(-1.0, 1.0, 300)
    ax.plot(-(d + al * yy ** 2), yy, 'k-', lw=LW_MAIN)
    ax.plot(d + al * yy ** 2, yy, 'k-', lw=LW_MAIN)
    aline(ax, 0, -1.18, 0, 1.18, lw=1.1)            # k_y 轴
    ax.text(0.07, 1.02, r'$k_y$', fontsize=12, ha='left')
    aline(ax, -1.18, 0, 1.18, 0, lw=1.1)            # k_x 轴
    ax.text(1.02, -0.16, r'$k_x$', fontsize=12, ha='left', va='top')
    # δk 双箭头（沿 k_x 轴，指向两支顶点）
    ax.annotate('', xy=(-d, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                mutation_scale=9, shrinkA=0, shrinkB=0))
    ax.annotate('', xy=(d, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                                mutation_scale=9, shrinkA=0, shrinkB=0))
    ax.text(-0.06, 0.17, r'$\delta k$', fontsize=13, ha='center', va='bottom')
    save(fig, 14)


# ================================================================ 图 15
# p257  §63  哑铃形费米面：两极大截面 + 颈部极小截面（斜线阴影），箭头指场方向。
def fig_15():
    fig, ax = plt.subplots(figsize=(3.45, 2.0))
    plain_axes(ax)
    ax.set_xlim(-0.28, 5.42)
    ax.set_ylim(-0.88, 2.62)
    # 轮廓（上半），中心线 y=1.075
    up = [(0.00, 1.075), (0.05, 1.28), (0.22, 1.62), (0.55, 1.95), (1.05, 2.15),
          (1.55, 2.02), (2.02, 1.70), (2.40, 1.51), (2.78, 1.70), (3.05, 2.02),
          (3.55, 2.15), (4.05, 1.95), (4.38, 1.62), (4.55, 1.28), (4.60, 1.075)]
    fup = pchip(up)
    xs = np.linspace(0, 4.6, 600)
    ys_up = fup(xs)
    ys_lo = 2.15 - ys_up
    ax.plot(np.r_[xs, xs[::-1]], np.r_[ys_up, ys_lo[::-1]], 'k-', lw=1.5, zorder=4)
    # 三个极值截面（旋转椭圆，斜线阴影）
    for (cx, cy, rx, ry, ang) in ((1.075, 1.075, 0.33, 1.03, -17),
                                  (2.40, 1.075, 0.19, 0.47, -16),
                                  (3.525, 1.075, 0.33, 1.03, -17)):
        ax.add_patch(Ellipse((cx, cy), 2 * rx, 2 * ry, angle=ang,
                             facecolor='white', edgecolor='k', lw=1.1,
                             hatch='////', zorder=5))
    # 场方向箭头（右下方，指向左上）
    ax.annotate('', xy=(4.42, -0.08), xytext=(5.12, -0.50),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2,
                                mutation_scale=12, shrinkA=0, shrinkB=0))
    save(fig, 15)


# ================================================================ 图 16
# p260  §63  H(B) 曲线：ad 水平平衡线，ab/cd 段（实线回线+等面积斜线阴影）；
# 上部第二个回线为虚线（无阴影）。曲线形状按页面数字化。
def _wiggle(m, h, A, n=300):
    """关于中点反对称的回线：g(s)=-sin(pi s)(1-s^2)，端点值为 0、切线水平。"""
    s = np.linspace(-1, 1, n)
    return m + h * s, A * (-np.sin(np.pi * s) * (1 - s ** 2))


def fig_16():
    fig, ax = plt.subplots(figsize=(2.62, 3.05))
    plain_axes(ax)
    ax.set_xlim(-0.10, 3.55)
    ax.set_ylim(-0.42, 3.30)
    yA = 1.22           # 平衡线 ad 高度
    xa, xd = 0.55, 1.52
    aline(ax, 0.0, 0.0, 0.0, 3.10, lw=1.3)          # H 轴
    aline(ax, xa, yA, xd, yA, lw=1.5)               # 平衡水平线 ad
    ax.text(0.09, 2.96, r'$H$', fontsize=12, ha='left')
    aline(ax, 0.0, 0.0, 3.40, 0.0, lw=1.3)          # B 轴
    ax.text(3.32, -0.20, r'$B$', fontsize=12, ha='left', va='top')
    # 主支（下方）：起点 → a
    f_lo = pchip([(0.22, 0.26), (0.30, 0.55), (0.40, 0.88), (0.48, 1.08),
                  (0.53, 1.17), (xa, yA)])
    x1 = np.linspace(0.22, xa, 120)
    ax.plot(x1, f_lo(x1), 'k-', lw=LW_MAIN, zorder=4)
    # ab/cd 回线（实线，反对称 → 等面积）
    mx, hh, A1 = (xa + xd) / 2, (xd - xa) / 2, 0.44
    xw, dw = _wiggle(mx, hh, A1)
    ax.plot(xw, yA + dw, 'k-', lw=LW_MAIN, zorder=4)
    # d → 第二平衡线
    f_md = pchip([(xd, yA), (1.62, 1.42), (1.74, 1.75), (1.85, 2.05), (1.92, 2.29)])
    x2 = np.linspace(xd, 1.92, 120)
    ax.plot(x2, f_md(x2), 'k-', lw=LW_MAIN, zorder=4)
    y2 = 2.285
    aline(ax, 1.92, y2, 2.87, y2, lw=1.5)           # 第二水平线
    # 第二回线（虚线）
    mx2, hh2, A2 = (1.92 + 2.87) / 2, (2.87 - 1.92) / 2, 0.50
    xw2, dw2 = _wiggle(mx2, hh2, A2)
    ax.plot(xw2, y2 + dw2, 'k--', lw=1.15, dashes=DASH, zorder=4)
    # 末支上升
    f_hi = pchip([(2.87, y2), (2.96, 2.50), (3.06, 2.76), (3.13, 2.92)])
    x3 = np.linspace(2.87, 3.13, 100)
    ax.plot(x3, f_hi(x3), 'k-', lw=LW_MAIN, zorder=4)
    # 等面积阴影（ab 上方 / cd 下方）
    xs = np.linspace(xa, xd, 600)
    curve = yA + A1 * (-np.sin(np.pi * (xs - mx) / hh) * (1 - ((xs - mx) / hh) ** 2))
    ax.fill_between(xs, yA, curve, where=curve >= yA, facecolor='none',
                    edgecolor='k', lw=0.0, hatch='///', zorder=3)
    ax.fill_between(xs, yA, curve, where=curve < yA, facecolor='none',
                    edgecolor='k', lw=0.0, hatch='///', zorder=3)
    # 标号
    ax.text(xa - 0.13, yA + 0.02, r'$a$', fontsize=13, ha='right', va='center')
    ax.text(0.81, 1.55 + 0.13, r'$b$', fontsize=13, ha='center', va='bottom')
    ax.text(1.26, 0.91 - 0.13, r'$c$', fontsize=13, ha='center', va='top')
    ax.text(xd + 0.10, yA - 0.02, r'$d$', fontsize=13, ha='left', va='center')
    save(fig, 16)


# ================================================================ 图 17
# p330  §81  两固体 1、2 之间的真空间隙 3（宽 l）；x 轴垂直于表面，原点取物体 1 表面。
def fig_17():
    fig, ax = plt.subplots(figsize=(2.05, 2.9))
    plain_axes(ax)
    ax.set_xlim(-1.62, 1.95)
    ax.set_ylim(-0.28, 2.72)
    W, L, H = 0.32, 0.58, 2.30      # 板厚 / 间隙 / 板高；物体1表面 x=0，物体2表面 x=l
    ymid = 1.12
    for x0 in (-W, L):
        ax.add_patch(Rectangle((x0, 0), W, H, facecolor='none', edgecolor='k',
                               lw=1.2, hatch='\\' * 3, zorder=4))
    # x 轴：自物体1表面起虚线，穿过物体 2 后成实线箭头
    ax.plot([0, L + W], [ymid, ymid], 'k--', lw=1.0, dashes=(4.5, 2.6), zorder=5)
    ax.annotate('', xy=(1.52, ymid), xytext=(L + W, ymid),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.1,
                                mutation_scale=11, shrinkA=0, shrinkB=0))
    ax.text(L - 0.09, ymid - 0.15, r'$l$', fontsize=13, ha='center', va='top')
    ax.text(1.44, ymid - 0.15, r'$x$', fontsize=13, ha='center', va='top')
    # 区域标号
    ax.text(-W - 0.13, H + 0.12, r'$1$', fontsize=13, ha='center', va='bottom')
    ax.text(L / 2, H + 0.12, r'$3$', fontsize=13, ha='center', va='bottom')
    ax.text(L + W + 0.12, H + 0.12, r'$2$', fontsize=13, ha='center', va='bottom')
    ax.text(-W - 0.13, ymid, r'$0$', fontsize=13, ha='right', va='center')
    save(fig, 17)


# ================================================================ 图 18
# p336  §82  函数 φ_II、φ_IM、φ_AI(ε0)：由公式(82.4)数值积分求出。
#   φ_II(ε) = J(ε,ε)        / [C ((ε-1)/(ε+1))^2]   （两相同电介质，式 82.6）
#   φ_IM(ε) = J(ε,∞)        / [C (ε-1)/(ε+1)]       （电介质-金属，式 82.7）
#   φ_AI(ε) = ∂J/∂ε2|ε2=1   / [3 (ε-1)/(ε+1)]       （原子-电介质壁，习题2）
#   其中 J = ∫∫ x^3/p^2 {[...]^{-1}+[...]^{-1}} dp dx，C = 2π^4/15（金属极限值）。
def fig_18():
    C = 2 * np.pi ** 4 / 15

    def Jpair(e1, e2, x):
        s1 = lambda p: np.sqrt(max(e1 - 1, 0) + p * p)
        s2 = lambda p: np.sqrt(max(e2 - 1, 0) + p * p)
        METAL = 1e12

        def f(p):
            r1 = (s1(p) + p) / (s1(p) - p) if e1 < METAL else 1.0
            r2 = (s2(p) + p) / (s2(p) - p) if e2 < METAL else 1.0
            q1 = (s1(p) + p * e1) / (s1(p) - p * e1) if e1 < METAL else -1.0
            q2 = (s2(p) + p * e2) / (s2(p) - p * e2) if e2 < METAL else -1.0
            ex = np.exp(min(x, 700.0))
            return (1.0 / (r1 * r2 * ex - 1.0) + 1.0 / (q1 * q2 * ex - 1.0)) / p ** 2
        val, _ = quad(f, 1, np.inf, limit=300, epsabs=1e-13, epsrel=1e-11)
        return val

    def J(e1, e2):
        val, _ = quad(lambda x: x ** 3 * Jpair(e1, e2, x), 0, np.inf,
                      limit=300, epsabs=1e-12, epsrel=1e-10)
        return val

    def G(e1):
        """dJ/de2 在 e2=1 处（解析求导后的被积式）"""
        s1 = lambda p: np.sqrt(max(e1 - 1, 0) + p * p)
        A0 = lambda p: 1.0 / (1.0 - 1.0 / (2 * p * p))
        METAL = 1e12

        def fx(x):
            def fp(p):
                r1 = (s1(p) + p) / (s1(p) - p) if e1 < METAL else 1.0
                q1 = (s1(p) + p * e1) / (s1(p) - p * e1) if e1 < METAL else -1.0
                return np.exp(-x) * (1.0 / (4 * p * p * r1)
                                     - 1.0 / (2 * A0(p) * q1)) / p ** 2
            val, _ = quad(fp, 1, np.inf, limit=200, epsabs=1e-13, epsrel=1e-11)
            return x ** 3 * val
        val, _ = quad(fx, 0, np.inf, limit=300, epsabs=1e-12, epsrel=1e-10)
        return val

    eps = np.array([1.0 + 1e-3, 1.003, 1.007, 1.015, 1.03, 1.06, 1.10, 1.16,
                    1.25, 1.4, 1.6, 1.9, 2.3, 2.8, 3.5, 4.5, 6.0, 8.0, 11.0,
                    15.0, 22.0, 33.0, 50.0, 80.0, 130.0, 220.0, 400.0, 800.0,
                    2000.0, 6000.0])
    pII, pIM, pAI = [], [], []
    for e in eps:
        s = (e - 1.0) / (e + 1.0)
        pII.append(J(e, e) / (C * s * s))
        pIM.append(J(e, 1e12) / (C * s))
        pAI.append(G(e) / (3 * s))
    xarr = 1.0 / eps

    fig, ax = plt.subplots(figsize=(3.42, 3.42))
    plain_axes(ax)
    ax.set_xlim(-0.055, 1.30)
    ax.set_ylim(-0.155, 1.185)
    # 网格框
    for gx in (0.2, 0.4, 0.6, 0.8):
        aline(ax, gx, 0, gx, 1.0, lw=0.75)
    for gy in (0.2, 0.4, 0.6, 0.8):
        aline(ax, 0, gy, 1.0, gy, lw=0.75)
    aline(ax, 0, 0, 1.0, 0, lw=1.1)     # 底边
    aline(ax, 1.0, 0, 1.0, 1.0, lw=1.1)  # 右边
    aline(ax, 0, 0, 0, 1.0, lw=1.1)      # 左边
    aline(ax, 0, 1.0, 1.0, 1.0, lw=1.1)  # 顶边
    # 三条曲线（按公式计算），从 x=1/ε 趋近 0 处补到 x=0
    for ys, lab in ((pAI, 'AI'), (pIM, 'IM'), (pII, 'II')):
        xx = np.r_[0.0, xarr[::-1]]
        yy = np.r_[1.0, ys[::-1]]
        ax.plot(xx, yy, 'k-', lw=1.35, zorder=4)
    # 标号（画在曲线上，白底断线）
    for x0, y0, t in ((0.735, 0.780, 'AI'), (0.665, 0.490, 'IM'), (0.715, 0.402, 'II')):
        ax.text(x0, y0, r'$\mathrm{%s}$' % t, fontsize=12, ha='center', va='center',
                bbox=dict(fc='white', ec='none', pad=1.2), zorder=6)
    # 坐标标号
    ax.text(0.015, 1.055, r'$\phi(\varepsilon_0)$', fontsize=12, ha='left', va='bottom')
    for gy in (0.2, 0.4, 0.6, 0.8, 1.0):
        ax.text(-0.028, gy, ('%.1f' % gy), fontsize=10.5, ha='right', va='center')
    ax.text(0, -0.035, r'$0$', fontsize=10.5, ha='center', va='top')
    for gx in (0.2, 0.4, 0.6, 0.8):
        ax.text(gx, -0.035, ('%.1f' % gx), fontsize=10.5, ha='center', va='top')
    ax.text(1.02, -0.035, r'$1/\varepsilon_0$', fontsize=11.5, ha='left', va='top')
    save(fig, 18)


# ================================================================== main
if __name__ == '__main__':
    fig_10()
    fig_11()
    fig_12()
    fig_13()
    fig_14()
    fig_15()
    fig_16()
    fig_17()
    fig_18()
    print('figs 10-18 done')
