# -*- coding: utf-8 -*-
# 批次 FC：图18-图25 重绘（朗道《场论》卷2 重排本）
# 图18(p275) 信号世界线 A/B；图19(p303) 矢量沿闭合回路平移（曲率）；
# 图20(p360) Lemaitre 坐标时空图（r=0/r=rg、光锥 a/a'）；图21(p364) U(r) 有效势能曲线族；
# 图22(p365) 圆轨道半径-角动量；图23(p366) 光子转折点 rho(r)（阴影=禁区）；
# 图24(p370) 收缩膨胀时空（Kruskal 型）；图25(p450) Kasner 指数 p1,p2,p3 对 1/u。
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(OUT, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

LW_MAIN = 1.2
LW_AUX = 0.8


def save(fig, n):
    fig.savefig(os.path.join(FIGDIR, 'fig%d.pdf' % n),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREVDIR, 'fig%d.png' % n),
                bbox_inches='tight', pad_inches=0.03, dpi=200)
    plt.close(fig)
    print('fig%d done' % n)


def new_ax(fig, rect, equal=True):
    ax = fig.add_axes(rect)
    if equal:
        ax.set_aspect('equal')
    ax.axis('off')
    return ax


def arrow(ax, x0, y0, x1, y1, lw=LW_MAIN, ms=10):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), zorder=6,
                arrowprops=dict(arrowstyle='-|>', color='k',
                                lw=lw, mutation_scale=ms,
                                shrinkA=0, shrinkB=0))


def bez(p0, p1, p2, n=100):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * t * (1 - t) * np.array(p1) \
        + t ** 2 * np.array(p2)


# ---------------------------------------------------------------- 图 18
def fig_18():
    fig = plt.figure(figsize=(2.6, 2.2))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-0.95, 2.75)
    ax.set_ylim(-0.35, 2.55)
    # 两条竖直世界线 A、B
    ax.plot([0, 0], [0, 2.15], 'k-', lw=LW_MAIN)
    ax.plot([1.05, 1.05], [0, 2.15], 'k-', lw=LW_MAIN)
    # 信号世界线（虚线）：A 上 x0 点 <-> B 上两点
    ya, yb1, yb2 = 1.32, 0.72, 2.02
    ax.plot([0, 1.05], [ya, yb2], 'k--', lw=LW_AUX)
    ax.plot([0, 1.05], [ya, yb1], 'k--', lw=LW_AUX)
    # 中途箭头：上行指向 B 上端；下行从 B 下端指向 x0
    arrow(ax, 0.50, ya + 0.50 * (yb2 - ya), 0.60, ya + 0.60 * (yb2 - ya),
          lw=LW_AUX, ms=11)
    arrow(ax, 0.60, ya + 0.60 * (yb1 - ya), 0.50, ya + 0.50 * (yb1 - ya),
          lw=LW_AUX, ms=11)
    # 标注
    ax.text(-0.08, ya, r'$x^0$', ha='right', va='center', fontsize=10)
    ax.text(1.13, yb2, r'$x^0+\mathrm{d}x^{0(2)}$', ha='left', va='center',
            fontsize=10)
    ax.text(1.13, yb1, r'$x^0+\mathrm{d}x^{0(1)}$', ha='left', va='center',
            fontsize=10)
    ax.text(0, -0.18, r'$A$', ha='center', va='top', fontsize=10)
    ax.text(1.05, -0.18, r'$B$', ha='center', va='top', fontsize=10)
    save(fig, 18)


# ---------------------------------------------------------------- 图 19
def fig_19():
    fig = plt.figure(figsize=(3.0, 2.6))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-1.85, 2.35)
    ax.set_ylim(-1.65, 1.85)
    A = (-0.95, -0.80)
    B = (1.38, 0.03)
    C = (0.0, 0.98)
    # 汇聚于中心的虚线（半径方向），端点外延
    ax.plot([0, 0], [0, 1.45], 'k--', lw=LW_AUX)          # 过 C 向上
    ax.plot([0, 1.80], [0, 0.045], 'k--', lw=LW_AUX)      # 过 B 向右
    ax.plot([0, -1.22], [0, -1.03], 'k--', lw=LW_AUX)     # 过 A 向左下
    # 三条弧（二次贝塞尔）
    arc_CA = bez(C, (-0.80, 0.42), A)
    arc_AB = bez(A, (0.18, -0.90), B)
    arc_BC = bez(B, (0.72, 0.70), C)
    for arc in (arc_CA, arc_AB, arc_BC):
        ax.plot(arc[:, 0], arc[:, 1], 'k-', lw=1.0)
    # 矢量 3（C 处，指右上）、2（B 处，指右上）、1（A 处水平）、1'（A 处近竖直）
    arrow(ax, C[0], C[1], C[0] + 0.42, C[1] + 0.34, ms=11)
    arrow(ax, B[0], B[1], B[0] + 0.38, B[1] + 0.38, ms=11)
    arrow(ax, A[0], A[1], A[0] + 0.50, A[1], ms=11)
    arrow(ax, A[0], A[1], A[0] - 0.06, A[1] + 0.52, ms=11)
    # 标注
    ax.text(C[0] - 0.10, C[1] + 0.06, r'$C$', ha='right', va='bottom',
            fontsize=10)
    ax.text(B[0] + 0.05, B[1] - 0.10, r'$B$', ha='left', va='top',
            fontsize=10)
    ax.text(A[0] - 0.10, A[1] - 0.02, r'$A$', ha='right', va='center',
            fontsize=10)
    ax.text(C[0] + 0.46, C[1] + 0.42, r'$\mathbf{3}$', ha='left', va='bottom',
            fontsize=10)
    ax.text(B[0] + 0.46, B[1] + 0.42, r'$\mathbf{2}$', ha='left', va='bottom',
            fontsize=10)
    ax.text(A[0] + 0.30, A[1] - 0.14, r'$\mathbf{1}$', ha='left', va='top',
            fontsize=10)
    ax.text(A[0] - 0.16, A[1] + 0.42, r"$\mathbf{1'}$", ha='right',
            va='center', fontsize=10)
    save(fig, 19)


# ---------------------------------------------------------------- 图 20
def fig_20():
    fig = plt.figure(figsize=(3.1, 3.0))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-1.30, 3.35)
    ax.set_ylim(-1.90, 2.72)
    k = 0.95

    def fam(x, c):
        return k * x + c

    # 倾斜直线族 R - c*t = const：r=0（粗）、r=r_g（实）、其余虚线
    ax.plot([-0.92, 1.93], [fam(-0.92, 0.10), fam(1.93, 0.10)], 'k-',
            lw=1.5)
    ax.plot([-0.85, 1.90], [fam(-0.85, -0.48), fam(1.90, -0.48)], 'k--',
            lw=LW_AUX)
    ax.plot([-0.05, 2.45], [fam(-0.05, -1.02), fam(2.45, -1.02)], 'k-',
            lw=1.1)
    ax.plot([0.55, 2.85], [fam(0.55, -1.62), fam(2.85, -1.62)], 'k--',
            lw=LW_AUX)
    ax.plot([1.05, 2.95], [fam(1.05, -2.20), fam(2.95, -2.20)], 'k--',
            lw=LW_AUX)
    # 线上标注（沿线旋转）
    ax.text(0.70, fam(0.70, 0.10) + 0.16, r'$r=0$', rotation=43.5,
            ha='center', va='bottom', fontsize=9)
    ax.text(1.95, fam(1.95, -1.02) + 0.15, r'$r=r_\mathrm{g}$', rotation=43.5,
            ha='center', va='bottom', fontsize=9)
    # 静止粒子竖直虚线（两条）
    ax.plot([0.62, 0.62], [-0.95, 2.12], 'k--', lw=LW_AUX)
    ax.plot([1.55, 1.55], [-0.95, 1.95], 'k--', lw=LW_AUX)
    # a' 处光锥：陡 X 形虚线，箭头指向 a'
    xa, ya = 0.62, 0.28
    dirs = [((0.375, 0.927), 0.72), ((-0.375, 0.927), 0.45),
            ((-0.375, -0.927), 0.55), ((0.375, -0.927), 0.45)]
    for d, L in dirs:
        x1, y1 = xa + d[0] * L, ya + d[1] * L
        ax.plot([xa, x1], [ya, y1], 'k--', lw=LW_AUX)
        # 中段指向 a' 的箭头
        xt, yt = xa + d[0] * L * 0.48, ya + d[1] * L * 0.48
        arrow(ax, xt, yt, xa + d[0] * L * 0.26, ya + d[1] * L * 0.26,
              lw=LW_AUX, ms=8)
    ax.text(xa + 0.13, ya - 0.12, r"$a'$", ha='left', va='top', fontsize=10)
    # a 处光锥：上下两个扁椭圆 + 外侧短虚线 + 中间小箭头
    xa, ya = 1.55, 0.35
    for yc in (ya + 0.075, ya - 0.075):
        e = Ellipse((xa, yc), 0.52, 0.085, fill=False, lw=1.0, zorder=5)
        ax.add_patch(e)
    # 椭圆外侧的虚线短枝
    stubs = [((xa - 0.26, ya + 0.075), (xa - 0.42, ya + 0.13)),
             ((xa + 0.26, ya + 0.075), (xa + 0.42, ya + 0.13)),
             ((xa - 0.26, ya - 0.075), (xa - 0.42, ya - 0.13)),
             ((xa + 0.26, ya - 0.075), (xa + 0.42, ya - 0.13))]
    for p0, p1 in stubs:
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], 'k--', lw=LW_AUX)
    arrow(ax, xa - 0.09, ya + 0.038, xa + 0.05, ya + 0.038, ms=8)
    arrow(ax, xa + 0.09, ya - 0.038, xa - 0.05, ya - 0.038, ms=8)
    ax.text(xa + 0.20, ya - 0.02, r'$a$', ha='left', va='center', fontsize=10)
    # 坐标轴
    ax.plot([0, 0], [-1.72, 2.52], 'k-', lw=1.0)
    ax.plot([-0.95, 2.40], [0, 0], 'k-', lw=1.0)
    ax.text(-0.06, 2.56, r'$\tau$', ha='right', va='bottom', fontsize=10)
    ax.text(2.48, -0.02, r'$R$', ha='left', va='center', fontsize=10)
    save(fig, 20)


# ---------------------------------------------------------------- 图 21
def fig_21():
    fig = plt.figure(figsize=(3.6, 2.4))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96], equal=False)
    ax.set_xlim(-0.45, 9.85)
    ax.set_ylim(-0.42, 1.58)
    # 轴：纵轴在左，横轴即 y=1 渐近线
    ax.plot([0.25, 0.25], [-0.30, 1.50], 'k-', lw=1.0)
    ax.plot([0.25, 9.0], [1, 1], 'k-', lw=1.0)
    ax.text(0.16, 1.52, r'$U/mc^2$', ha='right', va='bottom', fontsize=10)
    ax.text(9.06, 1.0, r'$r/r_\mathrm{g}$', ha='left', va='center',
            fontsize=10)
    ax.text(0.16, 1.0, r'$1$', ha='right', va='center', fontsize=9)
    ax.text(0.16, 0.943, r'$0.943$', ha='right', va='center', fontsize=8)
    # 横轴刻度数字 1 2 3（在 y=1 上方）
    for x in (1.0, 2.0, 3.0):
        ax.text(x, 1.03, '$%d$' % x, ha='center', va='bottom', fontsize=9)
    ax.plot([2.0, 2.0], [1.0, 1.035], 'k-', lw=0.8)   # "2" 处小刻度
    # 辅助虚线
    ax.plot([0.72, 0.72], [-0.28, 1.48], 'k--', lw=LW_AUX)
    ax.plot([0.25, 3.0], [0.943, 0.943], 'k--', lw=LW_AUX)
    ax.plot([3.0, 3.0], [0.943, 1.0], 'k--', lw=LW_AUX)

    # M = 2 mc r_g：高峰超过 1，缓降在标注右侧穿过 y=1，降至极小后回升
    xs1 = np.array([1.10, 1.30, 1.50, 1.65, 1.90, 2.30, 2.80, 3.30, 3.90,
                    4.50, 5.20, 5.90, 6.80, 8.00, 9.00])
    ys1 = np.array([0.25, 0.75, 1.15, 1.38, 1.33, 1.26, 1.20, 1.14, 1.045,
                    1.000, 0.982, 0.972, 0.974, 0.982, 0.988])
    ax.plot(xs1, ys1, 'k-', lw=1.2)
    ax.plot([5.2, 5.2], [0.974, 0.990], 'k-', lw=0.8)  # 曲线上小刻度
    # M = sqrt(3) mc r_g：峰恰触 y=1（x=2），降至 0.943（x=3）再回升
    xs2 = np.array([1.15, 1.35, 1.55, 1.75, 1.90, 2.00, 2.10, 2.25, 2.45,
                    2.70, 3.00, 3.40, 3.90, 4.50, 5.30, 6.30, 7.50, 9.00])
    ys2 = np.array([0.05, 0.35, 0.62, 0.82, 0.93, 0.985, 1.00, 0.99, 0.968,
                    0.952, 0.944, 0.944, 0.946, 0.949, 0.953, 0.959,
                    0.963, 0.967])
    ax.plot(xs2, ys2, 'k-', lw=1.2)
    # M = 0 ：单调上升趋于 1
    xs3 = np.array([1.25, 1.45, 1.70, 2.00, 2.40, 2.90, 3.50, 4.20, 5.00,
                    6.00, 7.50, 9.00])
    ys3 = np.array([-0.25, 0.10, 0.32, 0.48, 0.62, 0.74, 0.79, 0.84, 0.875,
                    0.905, 0.922, 0.935])
    ax.plot(xs3, ys3, 'k-', lw=1.2)
    # 曲线标注（置于楔形区内，小字号，同原书）
    ax.text(3.5, 0.976, r'$M=2mc\,r_\mathrm{g}$', ha='center',
            va='center', fontsize=5.5)
    ax.text(3.5, 0.912, r'$M=\sqrt{3}\,mc\,r_\mathrm{g}$', ha='center',
            va='center', fontsize=6)
    ax.text(2.85, 0.825, r'$M=0$', ha='center', va='center', fontsize=7)
    save(fig, 21)


# ---------------------------------------------------------------- 图 22
def fig_22():
    fig = plt.figure(figsize=(2.7, 2.5))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96], equal=False)
    ax.set_xlim(0.3, 4.35)
    ax.set_ylim(-2.6, 22.4)
    # 轴
    ax.plot([1, 1], [0, 20.0], 'k-', lw=1.0)
    ax.plot([1, 3.60], [0, 0], 'k-', lw=1.0)
    ax.text(0.94, 20.6, r'$r/r_\mathrm{g}$', ha='right', va='bottom',
            fontsize=10)
    ax.text(3.28, -1.05, r'$M/(mc\,r_\mathrm{g})$', ha='left', va='top',
            fontsize=9)
    # 刻度与数字
    for y in (5, 10, 15):
        ax.plot([1, 1.06], [y, y], 'k-', lw=0.8)
        ax.text(0.90, y, '$%d$' % y, ha='right', va='center', fontsize=9)
    ax.text(0.90, 0, r'$0$', ha='right', va='center', fontsize=9)
    for x in (2, 3):
        ax.plot([x, x], [0, -0.5], 'k-', lw=0.8)
        ax.text(x, -0.85, '$%d$' % x, ha='center', va='top', fontsize=9)
    ax.text(1.0, -0.85, r'$1$', ha='center', va='top', fontsize=9)
    # sqrt(3) 处竖直虚线
    s3 = np.sqrt(3)
    ax.plot([s3, s3], [0, 3], 'k--', lw=LW_AUX)
    ax.text(s3 - 0.10, 1.35, r'$\sqrt{3}$', ha='right', va='center',
            fontsize=10)
    # 曲线：r/rg = mu^2 (1 +- sqrt(1-3/mu^2))，尖点在 (sqrt3, 3)
    mu = np.linspace(s3, 3.25, 200)
    rt = np.sqrt(np.clip(1 - 3 / mu ** 2, 0, None))
    ax.plot(mu, mu ** 2 * (1 + rt), 'k-', lw=1.2)   # 上半支（稳定轨道）
    ax.plot(mu, mu ** 2 * (1 - rt), 'k-', lw=1.2)   # 下半支（不稳定轨道）
    save(fig, 22)


# ---------------------------------------------------------------- 图 23
def fig_23():
    fig = plt.figure(figsize=(3.2, 2.9))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-0.65, 7.75)
    ax.set_ylim(-1.55, 8.65)
    # 轴
    ax.plot([0.55, 0.55], [0, 7.7], 'k-', lw=1.0)
    ax.plot([0.55, 6.75], [0, 0], 'k-', lw=1.0)
    ax.text(0.50, 7.85, r'$\rho/r_\mathrm{g}$', ha='right', va='bottom',
            fontsize=10)
    ax.text(6.83, -0.05, r'$r/r_\mathrm{g}$', ha='left', va='center',
            fontsize=10)
    # y 刻度
    for y in (1, 2, 3, 4, 5):
        ax.plot([0.55, 0.62], [y, y], 'k-', lw=0.8)
    for y, lab in ((1, '1'), (4, '4'), (5, '5')):
        ax.text(0.47, y, '$%s$' % lab, ha='right', va='center', fontsize=9)
    ax.text(0.47, 2.598, r'$\dfrac{3\sqrt{3}}{2}$', ha='right', va='center',
            fontsize=9)
    # x 刻度
    for x in (1, 1.5, 3, 4, 5, 6):
        ax.plot([x, x], [0, -0.22], 'k-', lw=0.8)
    ax.text(1.0, -0.42, r'$1$', ha='center', va='top', fontsize=9)
    ax.text(1.5, -0.50, r'$\dfrac{3}{2}$', ha='center', va='top', fontsize=9)
    for x in (3, 4, 5, 6):
        ax.text(x, -0.42, '$%d$' % x, ha='center', va='top', fontsize=9)
    # 渐近竖线与顶部水平线
    ax.plot([1, 1], [0, 7.2], 'k-', lw=1.1)
    ax.plot([1, 5.95], [7.2, 7.2], 'k-', lw=1.1)
    # 曲线 rho = r^{3/2}/sqrt(r-1)，右端延伸与顶部线相接（原书画法）
    xl = np.array([1.005, 1.01, 1.02, 1.04, 1.06, 1.09, 1.13, 1.2, 1.28,
                   1.38, 1.5])
    yl = xl ** 1.5 / np.sqrt(xl - 1)
    yl = np.minimum(yl, 7.2)
    xr = np.array([1.5, 1.7, 1.95, 2.25, 2.6, 3.0, 3.5, 4.0, 4.5, 5.0,
                   5.5, 5.95])
    yr = np.array([2.598, 2.68, 2.83, 3.06, 3.38, 3.80, 4.42, 5.02, 5.62,
                   6.25, 6.85, 7.2])
    ax.plot(xl, yl, 'k-', lw=1.2)
    ax.plot(xr, yr, 'k-', lw=1.2)
    # 阴影（斜线阴影填充曲线与顶部线之间）
    poly_x = np.concatenate([[1.0], xr[::-1], xl[::-1]])
    poly_y = np.concatenate([[7.2], yr[::-1], yl[::-1]])
    ax.fill(poly_x, poly_y, facecolor='none', edgecolor='k', lw=0.0,
            hatch='/////', zorder=1)
    # 辅助虚线
    ax.plot([1.5, 1.5], [0, 2.598], 'k--', lw=LW_AUX)
    ax.plot([0.55, 1.5], [2.598, 2.598], 'k--', lw=LW_AUX)
    save(fig, 23)


# ---------------------------------------------------------------- 图 24
def fig_24():
    fig = plt.figure(figsize=(2.9, 3.3))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-1.15, 1.28)
    ax.set_ylim(-1.78, 1.92)
    # 轴
    ax.plot([0, 0], [-1.62, 1.66], 'k-', lw=1.0)
    ax.plot([-0.85, 1.0], [0, 0], 'k-', lw=1.0)
    ax.text(-0.05, 1.70, r'$\tau$', ha='right', va='bottom', fontsize=10)
    ax.text(1.06, 0, r'$R$', ha='left', va='center', fontsize=10)
    ax.text(-0.05, -0.05, r'$O$', ha='right', va='top', fontsize=10)
    # r=0 双曲线（粗，上下两支）
    x = np.linspace(-0.55, 0.55, 200)
    ax.plot(x, 0.62 + 2.4 * x ** 2, 'k-', lw=1.5)
    ax.plot(x, -(0.62 + 2.4 * x ** 2), 'k-', lw=1.5)
    # r=r_g 曲线（细，过 O 的两支）
    xt = np.linspace(-0.65, 0.65, 200)
    ythin = 1.35 * np.sinh(1.55 * xt) / np.sinh(1.55 * 0.65)
    ax.plot(xt, -ythin, 'k-', lw=1.0)   # A O A'
    ax.plot(xt, ythin, 'k-', lw=1.0)    # B O B'
    # 端点与顶点标注
    ax.text(-0.53, 1.42, r'$A$', ha='right', va='bottom', fontsize=10)
    ax.text(0.53, 1.42, r'$B$', ha='left', va='bottom', fontsize=10)
    ax.text(-0.07, 0.70, r'$C$', ha='right', va='bottom', fontsize=10)
    ax.text(-0.07, -0.70, r"$C'$", ha='right', va='top', fontsize=10)
    ax.text(0.55, -1.44, r"$A'$", ha='left', va='top', fontsize=10)
    ax.text(-0.55, -1.44, r"$B'$", ha='right', va='top', fontsize=10)
    # 沿线标注 r=0 / r=rg
    ax.text(0.34, 1.06, r'$r=0$', rotation=55, ha='center', va='bottom',
            fontsize=9)
    ax.text(0.34, -1.00, r'$r=0$', rotation=-55, ha='center', va='top',
            fontsize=9)
    ax.text(0.56, 0.92, r'$r=r_\mathrm{g}$', rotation=66, ha='left',
            va='bottom', fontsize=9)
    ax.text(0.56, -0.86, r'$r=r_\mathrm{g}$', rotation=-66, ha='left',
            va='top', fontsize=9)
    # 静止粒子世界线（竖直虚线）与点 a b c d
    xp = 0.33
    yd = 0.62 + 2.4 * xp ** 2
    yc = 1.35 * np.sinh(1.55 * xp) / np.sinh(1.55 * 0.65)
    ax.plot([xp, xp], [-yd, yd], 'k--', lw=LW_AUX)
    arrow(ax, xp, 0.12, xp, 0.34, lw=LW_AUX, ms=10)
    ax.text(xp + 0.05, yd - 0.04, r'$d$', ha='left', va='top', fontsize=10)
    ax.text(xp + 0.05, yc - 0.05, r'$c$', ha='left', va='top', fontsize=10)
    ax.text(xp + 0.08, -yc - 0.02, r'$b$', ha='left', va='top', fontsize=10)
    ax.text(xp - 0.07, -yd + 0.10, r'$a$', ha='right', va='bottom',
            fontsize=10)
    save(fig, 24)


# ---------------------------------------------------------------- 图 25
def fig_25():
    fig = plt.figure(figsize=(3.1, 2.9))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-0.24, 1.36)
    ax.set_ylim(-0.62, 1.24)
    # 网格
    for x in np.arange(0.2, 1.01, 0.2):
        ax.plot([x, x], [-0.4, 1.0], 'k-', lw=0.5)
    for y in np.arange(-0.4, 1.01, 0.2):
        ax.plot([0, 1.0], [y, y], 'k-', lw=0.5)
    # 带箭头的轴
    ax.plot([0, 0], [-0.45, 1.02], 'k-', lw=1.0)
    arrow(ax, 0, 1.0, 0, 1.13, lw=1.0, ms=9)
    ax.plot([-0.01, 1.04], [0, 0], 'k-', lw=1.0)
    arrow(ax, 1.02, 0, 1.16, 0, lw=1.0, ms=9)
    ax.text(0.05, 1.06, r'$p$', ha='left', va='bottom', fontsize=10)
    ax.text(1.10, -0.09, r'$1/u$', ha='right', va='top', fontsize=10)
    # 刻度数字
    for y in np.arange(-0.4, 1.01, 0.2):
        lab = ('%.1f' % y)
        ax.text(-0.04, y, '$%s$' % lab, ha='right', va='center', fontsize=7.5)
    for x in np.arange(0.2, 1.01, 0.2):
        ax.text(x, -0.46, '$%.1f$' % x, ha='center', va='top', fontsize=7.5)
    # 曲线 p1, p2, p3
    s = np.linspace(0, 1, 200)
    den = 1 + s + s ** 2
    ax.plot(s, -s / den, 'k-', lw=1.2)          # p1
    ax.plot(s, (s + s ** 2) / den, 'k-', lw=1.2)   # p2
    ax.plot(s, (1 + s) / den, 'k-', lw=1.2)        # p3
    # 曲线标注
    ax.text(0.47, 0.905, r'$p_3$', ha='center', va='bottom', fontsize=10)
    ax.text(0.40, 0.44, r'$p_2$', ha='center', va='bottom', fontsize=10)
    ax.text(0.30, -0.185, r'$p_1$', ha='center', va='bottom', fontsize=10)
    # 右端极限值
    ax.text(1.035, 2 / 3., r'$\dfrac{2}{3}$', ha='left', va='center',
            fontsize=9)
    ax.text(1.035, -1 / 3., r'$-\dfrac{1}{3}$', ha='left', va='center',
            fontsize=9)
    save(fig, 25)


if __name__ == '__main__':
    import sys
    which = sys.argv[1:] if len(sys.argv) > 1 else []
    fns = {18: fig_18, 19: fig_19, 20: fig_20, 21: fig_21, 22: fig_22,
           23: fig_23, 24: fig_24, 25: fig_25}
    for n in (which or [18, 19, 20, 21, 22, 23, 24, 25]):
        fns[int(n)]()
