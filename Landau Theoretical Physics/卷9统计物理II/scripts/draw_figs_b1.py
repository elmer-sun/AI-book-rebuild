# -*- coding: utf-8 -*-
"""
朗道《理论物理学教程》第9卷《统计物理学II》中文重排本 插图重绘 第一批：图1-图9
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p049/091/116/119/162/189/193/196）。
  图1 p049  §10  费米液体粒子分布 N(p)（T=0，实线）与理想气体（虚线）
  图2 p091  §22  液氦He-II 元激发谱 ε(K)-p/ħ（实验曲线，数字化重绘）
  图3 p116  §29  习题1 涡环几何：P、dl、R、R0、θ
  图4 p119  §30  近理想玻色气体涡线芯 f(ξ)（方程30.7 数值解，打靶法）
  图5 p162  §39  超流费米气体准粒子谱（上曲线）与正常态 ε=vF|p-pF|（V线）
  图6 p189  §46  κ<<1 表面层：B(x)、ψ(x)=tanh 分布与 κ^{-1/2}、1/κ
  图7 p193  §47  Hc1、Hc2（实线）与 Hc3（虚线）相图（数字化重绘）
  图8 p193  §47  双势阱（x=0 面对称的两条势阱，虚线为单阱延伸）
  图9 p196  §48  单涡线：|ψ|^2 芯（宽 ξ）与 B(r) 峰（宽 δ），两面板
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle
from scipy.interpolate import PchipInterpolator
from scipy.integrate import solve_ivp

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = r"E:\AI整理书籍\朗道理论物理教程\卷9统计物理II"
FIGD = os.path.join(BASE, '重排本', 'figures')
PRED = os.path.join(BASE, '原书转换')
os.makedirs(FIGD, exist_ok=True)

LW_MAIN, LW_AUX = 1.4, 0.8


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


# ================================================================ 图 1
# p049  §10  费米液体动量分布 N(p)；虚线=理想气体 N=1。
# 原图为示意图（球内缓降依赖 g(w,p)，书未给解析式），按页面逐点数字化。
def fig_1():
    pts = [(0.00, 0.990), (0.17, 0.981), (0.32, 0.974), (0.40, 0.970),
           (0.48, 0.964), (0.55, 0.964), (0.63, 0.957), (0.71, 0.953),
           (0.78, 0.946), (0.86, 0.927), (0.93, 0.883), (0.965, 0.850),
           (0.98, 0.750), (0.995, 0.550), (1.01, 0.280), (1.025, 0.130),
           (1.045, 0.095), (1.09, 0.072), (1.16, 0.043), (1.20, 0.030),
           (1.28, 0.017), (1.40, 0.014), (1.72, 0.012)]
    f = pchip(pts)
    fig, ax = plt.subplots(figsize=(2.55, 2.02))
    plain_axes(ax)
    ax.set_xlim(-0.30, 1.80)
    ax.set_ylim(-0.22, 1.70)
    xx = np.linspace(0, 1.72, 400)
    ax.plot(xx, f(xx), 'k-', lw=LW_MAIN, zorder=3)
    aline(ax, 0, 0, 0, 1.55)                 # 纵轴
    aline(ax, 0, 0, 1.72, 0)                 # 横轴
    ax.plot([0, 1.03], [1, 1], 'k--', lw=0.95, dashes=(4.5, 2.4))   # N=1 虚线
    ax.plot([1, 1], [1, 0], 'k--', lw=0.95, dashes=(3, 2.2))        # p_F 虚线
    ax.text(-0.05, 1.40, r'$N(\mathbf{\mathit{p}})$', fontsize=10,
            ha='right', va='center')
    ax.text(-0.045, 1.0, '1', fontsize=9.5, ha='right', va='center')
    ax.text(1.0, -0.105, r'$p_{\rm F}$', fontsize=10, ha='center', va='top')
    ax.text(1.69, -0.105, r'$p$', fontsize=10, ha='center', va='top')
    save(fig, 1)


# ================================================================ 图 2
# p091  §22  He-II 元激发谱（Henshaw-Woods 实验曲线）。
# 从 300dpi 页面数字化（每 2K、1/3 单位一刻度，"10" 对准第 5 刻度），
# 控制点为像素提取值；roton 谷底按原图 ≈10K（原书图未画到 8.6K 精确值）。
FIG2 = [
    (0.000, 0.00), (0.085, 2.28), (0.219, 4.59), (0.319, 6.28), (0.452, 8.33),
    (0.552, 9.73), (0.685, 11.42), (0.785, 12.51), (0.918, 13.69),
    (1.018, 14.41), (1.151, 15.13), (1.251, 15.41), (1.384, 15.54),
    (1.484, 15.39), (1.617, 14.83), (1.717, 14.08), (1.850, 12.54),
    (1.950, 11.30), (2.083, 10.28), (2.183, 10.13), (2.316, 10.67),
    (2.416, 11.60), (2.550, 13.33), (2.649, 14.62), (2.783, 16.06),
    (2.883, 16.98), (3.016, 17.96), (3.116, 18.48), (3.249, 18.95),
    (3.349, 19.15), (3.482, 19.24), (3.582, 19.26), (3.715, 19.27),
    (4.000, 19.20),
]


def fig_2():
    f = pchip(FIG2)
    fig, ax = plt.subplots(figsize=(3.15, 2.35))
    plain_axes(ax)
    ax.set_xlim(-0.75, 4.15)
    ax.set_ylim(-7.0, 21.0)
    xx = np.linspace(0, 4.0, 500)
    ax.plot(xx, f(xx), 'k-', lw=1.5, zorder=3)
    aline(ax, 0, 0, 0, 19.2)                 # 纵轴（顶端略低于曲线平台）
    aline(ax, 0, 0, 4.05, 0)                 # 横轴
    # 刻度：y 每 2K（轴向右），x 每 1/3 单位（轴向上）
    for k in range(2, 19, 2):
        aline(ax, 0, k, 0.085, k, lw=0.9)
    for k in range(1, 13):
        aline(ax, k / 3.0, 0, k / 3.0, 0.38, lw=0.9)
    ax.text(-0.10, 10, '10', fontsize=9.5, ha='right', va='center')
    for u in (1, 2, 3):
        ax.text(u, -1.5, '%g' % u, fontsize=9.5, ha='center', va='top')
    ax.text(-0.10, 18.6, r'$\varepsilon/\mathrm{K}$', fontsize=10,
            ha='right', va='center')
    ax.text(2.0, -4.9, r'$p/\hbar/(10^{8}\,\mathrm{cm}^{-1})$', fontsize=10,
            ha='center', va='top')
    save(fig, 2)


# ================================================================ 图 3
# p116  §29 习题1  涡环：圆环上半径 R0(中心->P)、环元 dl 处的张量线 R（弦）、
# 中心角 θ（双向箭头弧）。
def fig_3():
    fig, ax = plt.subplots(figsize=(2.15, 2.25))
    plain_axes(ax)
    ax.set_xlim(-1.42, 1.40)
    ax.set_ylim(-1.50, 1.30)
    ax.set_aspect('equal')
    th = np.deg2rad(205.0)
    dl = np.array([np.cos(th), np.sin(th)])          # dl 所在点
    ax.add_patch(Arc((0, 0), 2, 2, theta1=0, theta2=360, lw=LW_MAIN, color='k'))
    ax.plot([0, 0], [0, 1], 'k-', lw=1.0)            # 半径 R0
    ax.plot([0, dl[0]], [0, dl[1]], 'k-', lw=1.0)    # 半径至 dl
    ax.plot([dl[0], 0], [dl[1], 1], 'k-', lw=1.0)    # 弦 R
    # θ 弧（两端箭头分别抵住 R0 线与 dl 半径线）
    ax.add_patch(Arc((0, 0), 0.80, 0.80, theta1=95, theta2=203,
                     lw=0.95, color='k'))
    for a0, dirc in ((95, (0.99, 0.12)), (203, (-0.39, -0.92))):
        a = np.deg2rad(a0)
        tip = 0.40 * np.array([np.cos(a), np.sin(a)])
        tail = tip - 0.10 * np.array(dirc)
        ax.annotate('', xy=tip, xytext=tail, arrowprops=dict(
            arrowstyle='-|>', color='k', lw=0.95, shrinkA=0, shrinkB=0,
            mutation_scale=9))
    ax.text(0.03, 1.10, r'$P$', fontsize=10.5, ha='center', va='bottom')
    ax.text(dl[0] - 0.03, dl[1] - 0.14, r'$\mathbf{d}\mathbf{\mathit{l}}$',
            fontsize=10, ha='right', va='top')
    ax.text(-0.47, 0.42, r'$\mathbf{\mathit{R}}$', fontsize=10.5,
            ha='center', va='center')
    ax.text(0.17, 0.30, r'$\mathbf{\mathit{R}}_0$', fontsize=10.5,
            ha='left', va='center')
    am = np.deg2rad(148)
    ax.text(0.30 * np.cos(am), 0.30 * np.sin(am), r'$\theta$', fontsize=11,
            ha='center', va='center')
    save(fig, 3)


# ================================================================ 图 4
# p119  §30  方程 (30.7): (1/ξ)d/dξ(ξ df/dξ) - f/ξ^2 + f - f^3 = 0,
# f(0)=0, f(inf)=1。小 ξ 展开 f = a ξ - (a/8) ξ^3，对 a 打靶。
def fig_4():
    def shoot(a):
        xi0 = 1e-4
        s0 = [a * xi0 - a / 8 * xi0 ** 3, a - 3 * a / 8 * xi0 ** 2]
        sol = solve_ivp(lambda x, y: [y[1],
                                      -y[1] / x + y[0] / x ** 2 - y[0] + y[0] ** 3],
                        (xi0, 12.0), s0, rtol=1e-10, atol=1e-12, dense_output=True)
        return sol

    lo, hi = 0.2, 1.2
    for _ in range(48):
        mid = 0.5 * (lo + hi)
        s = shoot(mid)
        if (not np.isfinite(s.y[0, -1])) or abs(s.y[0, -1]) > 5:
            hi = mid              # 超临界：发散
        else:
            lo = mid              # 亚临界：有限
    a = 0.5 * (lo + hi)
    sol = shoot(a * (1 - 1e-7))
    xi = np.linspace(0, 6, 400)
    fv = sol.sol(xi)[0]
    fv = np.clip(fv, 0, None)
    fv[0] = 0.0
    print('  fig4: a =', round(a, 5), ' f(1)=%.3f f(3)=%.3f f(6)=%.3f'
          % (sol.sol(1)[0], sol.sol(3)[0], sol.sol(6)[0]))

    fig, ax = plt.subplots(figsize=(3.25, 1.48))
    ax.set_xlim(-0.42, 6.42)
    ax.set_ylim(-0.145, 1.115)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    # 网格与边框
    for gx in range(1, 6):
        ax.plot([gx, gx], [0, 1], 'k-', lw=0.7, zorder=1)
    for gy in (0.5, 1.0):
        ax.plot([0, 6], [gy, gy], 'k-', lw=0.7, zorder=1)
    ax.add_patch(Rectangle((0, 0), 6, 1, fill=False, lw=1.0, edgecolor='k'))
    ax.plot(xi, fv, 'k-', lw=1.5, zorder=3)
    ax.text(0.02, 1.078, r'$f(\xi)$', fontsize=10, ha='left', va='center')
    ax.text(6.42, -0.085, r'$\xi$', fontsize=10.5, ha='left', va='center')
    for gx in range(7):
        ax.text(gx, -0.075, '%g' % gx, fontsize=9,
                ha='center', va='top')
    ax.text(-0.09, 0.5, '0.5', fontsize=9, ha='right', va='center')
    ax.text(-0.09, 1.0, '1', fontsize=9, ha='right', va='center')
    save(fig, 4)


# ================================================================ 图 5
# p162  §39  ε(p)=sqrt(Δ^2 + vF^2(p-pF)^2)（上曲线）与正常费米液体
# ε = vF|p-pF|（两条直线，原书印为粗单线，扫描中的双线为印刷缝）。
def fig_5():
    D = 0.433
    fig, ax = plt.subplots(figsize=(2.75, 2.25))
    plain_axes(ax)
    ax.set_xlim(-1.82, 1.80)
    ax.set_ylim(-0.36, 1.62)
    ax.set_aspect(1.47)
    xx = np.linspace(-1, 1, 400)
    ax.plot(xx, np.sqrt(D ** 2 + xx ** 2), 'k-', lw=1.3, zorder=3)
    ax.plot([0, 1], [0, 1], 'k-', lw=1.6, zorder=2)
    ax.plot([0, -1], [0, 1], 'k-', lw=1.6, zorder=2)
    aline(ax, -1.79, 0, 1.77, 0)             # 横轴
    aline(ax, 0, 0, 0, 1.43)                 # 纵轴
    ax.text(0.09, 1.36, r'$\varepsilon$', fontsize=11, ha='left', va='center')
    ax.text(0.075, 0.55, r'$\Delta$', fontsize=11, ha='left', va='center')
    ax.text(1.30, -0.20, r'$p-p_{\rm F}$', fontsize=10, ha='center', va='top')
    save(fig, 5)


# ================================================================ 图 6
# p189  §46  κ<<1: ψ=(1+tanh((x-x0)/w))/2 型（x=0 取在场减弱区内），
# B(x) 按页面锚点用 erfc 下降；下方 κ^{-1/2} 与 1/κ 双向箭头。
def fig_6():
    xB, sB = -0.052, 0.19
    xc, wc = 0.20, 0.446
    B = lambda x: 0.5 * _erfc((x - xB) / sB)
    psi = lambda x: 0.5 * (1 + np.tanh((x - xc) / wc))
    fig, ax = plt.subplots(figsize=(3.55, 1.95))
    plain_axes(ax)
    ax.set_xlim(-1.72, 1.34)
    ax.set_ylim(-1.22, 1.52)
    xx = np.linspace(-1.12, 0.60, 400)
    ax.plot(xx, B(xx), 'k-', lw=1.4, zorder=3)
    xx = np.linspace(-0.40, 1.20, 400)
    ax.plot(xx, psi(xx), 'k-', lw=1.4, zorder=3)
    aline(ax, -1.56, 0, 1.22, 0, lw=1.0)     # 横轴
    aline(ax, 0, 0, 0, 1.34, lw=0.9)         # x=0 竖线
    _dbl_arrow(ax, -0.315, 0, -0.30)         # κ^{-1/2}
    ax.text(-0.13, -0.47, r'$\kappa^{-1/2}$', fontsize=10, ha='center', va='top')
    _dbl_arrow(ax, -0.315, 0.685, -0.80)     # 1/κ
    ax.text(0.28, -0.93, r'$1/\kappa$', fontsize=10, ha='center', va='top')
    ax.text(-1.18, 0.79, r'$B=1$', fontsize=10, ha='center', va='center')
    ax.text(1.00, 0.68, r'$\psi=1$', fontsize=10, ha='center', va='center')
    ax.text(-0.24, 0.50, r'$B(\mathbf{\mathit{x}})$', fontsize=10,
            ha='center', va='center')
    ax.text(0.49, 0.30, r'$\psi(\mathbf{\mathit{x}})$', fontsize=10,
            ha='center', va='center')
    save(fig, 6)


def _erfc(x):
    from math import erfc as e
    return np.vectorize(e)(x)


def _dbl_arrow(ax, x0, x1, y):
    ax.annotate('', xy=(x1, y), xytext=(x0, y), arrowprops=dict(
        arrowstyle='<|-|>', color='k', lw=1.0, shrinkA=0, shrinkB=0,
        mutation_scale=11))


# ================================================================ 图 7
# p193  §47  Hc1、Hc2（实线）与表面超导边界 Hc3（虚线），三者会于 Tc。
# 曲线为原书示意图，自 300dpi 页面数字化。
F7C1 = [
    (0.008, 0.231), (0.051, 0.231), (0.095, 0.228), (0.138, 0.225),
    (0.181, 0.225), (0.222, 0.222), (0.265, 0.219), (0.309, 0.213),
    (0.352, 0.209), (0.395, 0.204), (0.438, 0.199), (0.482, 0.189),
    (0.525, 0.180), (0.568, 0.168), (0.611, 0.158), (0.652, 0.146),
    (0.696, 0.130), (0.739, 0.107), (0.782, 0.081), (0.825, 0.049),
]
F7C2 = [
    (0.008, 0.515), (0.047, 0.512), (0.088, 0.509), (0.127, 0.505),
    (0.168, 0.501), (0.207, 0.498), (0.248, 0.490), (0.287, 0.481),
    (0.326, 0.474), (0.367, 0.461), (0.406, 0.451), (0.447, 0.436),
    (0.486, 0.417), (0.525, 0.402), (0.566, 0.379), (0.605, 0.353),
    (0.646, 0.326), (0.685, 0.294), (0.726, 0.253), (0.765, 0.201),
]
F7C3 = [
    (0.008, 0.673), (0.062, 0.669), (0.118, 0.663), (0.147, 0.658),
    (0.203, 0.649), (0.257, 0.635), (0.298, 0.624), (0.358, 0.603),
    (0.404, 0.585), (0.447, 0.564), (0.486, 0.540), (0.510, 0.529),
    (0.549, 0.500),
]
MEET = 0.846          # 三线会合点（Tc）


def fig_7():
    fig, ax = plt.subplots(figsize=(2.62, 2.72))
    plain_axes(ax)
    ax.set_xlim(-0.075, 1.075)
    ax.set_ylim(-0.115, 1.075)
    ax.set_aspect(1.30)
    c1 = pchip(F7C1 + [(MEET, 0.0)])
    c2 = pchip(F7C2 + [(0.79, 0.135), (0.816, 0.062), (0.836, 0.022),
                       (MEET, 0.0)])
    c3 = pchip(F7C3 + [(0.66, 0.435), (0.72, 0.325), (0.775, 0.21),
                       (0.815, 0.105), (0.838, 0.032), (MEET, 0.0)])
    xx = np.linspace(F7C1[0][0], MEET, 300)
    ax.plot(xx, c1(xx), 'k-', lw=LW_MAIN, zorder=3)
    xx = np.linspace(F7C2[0][0], MEET, 300)
    ax.plot(xx, c2(xx), 'k-', lw=LW_MAIN, zorder=3)
    xx = np.linspace(F7C3[0][0], MEET, 300)
    ax.plot(xx, c3(xx), 'k--', lw=1.1, dashes=(4.5, 2.6), zorder=3)
    aline(ax, 0, 0, 1.0, 0)                  # T 轴
    aline(ax, 0, 0, 0, 1.0)                  # Φ 轴
    ax.text(0.045, 0.95, r'$\Phi$', fontsize=11, ha='left', va='center')
    ax.text(0.985, -0.062, r'$T$', fontsize=11, ha='center', va='top')
    ax.text(0.50, 0.80, 'n 相', fontsize=10.5, ha='center', va='center')
    ax.text(0.735, 0.585, r'$H_{c3}$', fontsize=10.5, ha='left', va='center')
    ax.text(0.42, 0.525, r'$H_{c2}$', fontsize=10.5, ha='center', va='center')
    ax.text(0.31, 0.33, '混合相', fontsize=10.5, ha='center', va='center')
    ax.text(0.585, 0.20, r'$H_{c1}$', fontsize=10.5, ha='left', va='center')
    ax.text(0.175, 0.12, 's 相', fontsize=10.5, ha='center', va='center')
    save(fig, 7)


# ================================================================ 图 8
# p193  §47  双势阱：对 x=0 对称的两条相同势阱（实线各取半边），
# 虚线为右侧单阱在 x<0 半空间的延伸。原书图形明显比抛物线平缓，
# 按页面锚点用余弦阱 U=A[1-cos(pi(x∓x0)/L)] 拟合（U(0)=1, U(±x0)=0）。
def fig_8():
    L, A = 2.3, 1.2547

    def UR(x):
        return A * (1 - np.cos(np.pi * (x - 1) / L))

    def UL(x):
        return A * (1 - np.cos(np.pi * (x + 1) / L))

    fig, ax = plt.subplots(figsize=(3.3, 2.15))
    plain_axes(ax)
    ax.set_xlim(-2.92, 3.80)
    ax.set_ylim(-0.52, 4.95)
    xx = np.linspace(-2.65, 0, 300)
    ax.plot(xx, UL(xx), 'k-', lw=LW_MAIN, zorder=3)
    xx = np.linspace(0, 2.85, 300)
    ax.plot(xx, UR(xx), 'k-', lw=LW_MAIN, zorder=3)
    xx = np.linspace(-0.80, 0, 100)
    ax.plot(xx, UR(xx), 'k--', lw=1.1, dashes=(4.5, 2.6), zorder=3)
    aline(ax, -2.75, 0, 3.56, 0)             # x 轴
    aline(ax, 0, 0, 0, 4.5)                  # U(x) 轴
    ax.text(0.09, 4.35, r'$U(\mathbf{\mathit{x}})$', fontsize=10.5,
            ha='left', va='center')
    ax.text(-1.0, -0.38, r'$-x_0$', fontsize=10.5, ha='center', va='top')
    ax.text(1.0, -0.38, r'$x_0$', fontsize=10.5, ha='center', va='top')
    ax.text(3.28, -0.38, r'$x$', fontsize=10.5, ha='center', va='top')
    save(fig, 8)


# ================================================================ 图 9
# p196  §48  单涡线（κ>>1）：|ψ|^2 在芯部（宽 ξ）陡降为零、远处为常数；
# B(r) 为宽 δ 的钟形峰。两面板。均按解析式绘制。
def fig_9():
    fig = plt.figure(figsize=(6.9, 1.72))
    # ---- 左：|ψ|^2（单位 ξ=相干长度；dip 半高半宽≈0.28ξ）----
    ax = fig.add_axes([0.055, 0.24, 0.475, 0.66])
    plain_axes(ax)
    ax.set_xlim(-7.6, 7.6)
    ax.set_ylim(-1.02, 1.80)
    r = np.linspace(-4.8, 5.5, 800)
    ax.plot(r, np.tanh(r / 0.23) ** 4, 'k-', lw=1.4, zorder=3)
    aline(ax, -6.95, 0, 6.95, 0, lw=1.0)
    aline(ax, 0, 0, 0, 1.45, lw=0.8)
    _dbl_arrow(ax, -1, 1, -0.33)
    ax.text(0, -0.66, r'$\xi$', fontsize=10.5, ha='center', va='top')
    ax.text(0.5, 1.55, r'$|\psi|^2$', fontsize=10.5, ha='left', va='center')
    ax.text(6.80, -0.42, r'$r$', fontsize=10.5, ha='center', va='top')
    # ---- 右：B(r)（单位 δ=穿透深度；高斯 σ≈0.55δ）----
    ax = fig.add_axes([0.575, 0.24, 0.345, 0.66])
    plain_axes(ax)
    ax.set_xlim(-1.55, 1.85)
    ax.set_ylim(-1.02, 1.80)
    r = np.linspace(-1.35, 1.35, 600)
    ax.plot(r, np.exp(-r ** 2 / (2 * 0.55 ** 2)), 'k-', lw=1.4, zorder=3)
    aline(ax, -1.35, 0, 1.35, 0, lw=1.0)
    aline(ax, 0, 0, 0, 1.50, lw=0.8)
    _dbl_arrow(ax, -0.7, 1.3, -0.33)
    ax.text(0.05, -0.66, r'$\delta$', fontsize=10.5, ha='center', va='top')
    ax.text(0.15, 1.55, r'$B(\mathbf{\mathit{r}})$', fontsize=10.5,
            ha='left', va='center')
    ax.text(1.50, -0.42, r'$r$', fontsize=10.5, ha='center', va='top')
    save(fig, 9)


if __name__ == '__main__':
    for i in range(1, 10):
        globals()[f'fig_{i}']()
        print(f'fig{i} done')
