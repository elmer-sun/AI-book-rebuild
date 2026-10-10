# -*- coding: utf-8 -*-
# 批次 FA：图1–图6 重绘（朗道《场论》卷2 重排本）
# 图1(p017) 两惯性系 K/K' 与信号传播；图2(p022) 光锥；
# 图3(p050) 衰变粒子动量椭圆 V<v0 / V>v0；图4(p058) 碰撞动量三角形 m1>m2 / m1<m2；
# 图5(p059) 等质量粒子最小分离角；图6(p078) 正交电磁场中漂移轨迹 (a)(b)(c)。
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Ellipse

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


def new_ax(fig, rect):
    ax = fig.add_axes(rect)
    ax.set_aspect('equal')
    ax.axis('off')
    return ax


def arrow(ax, x0, y0, x1, y1, lw=LW_MAIN, ms=10):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), zorder=5,
                arrowprops=dict(arrowstyle='-|>', color='k',
                                lw=lw, mutation_scale=ms,
                                shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------- 图 1
def fig_1():
    fig = plt.figure(figsize=(3.35, 2.45))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-1.15, 4.0)
    ax.set_ylim(-1.05, 2.75)
    lw = 1.0
    # K 系
    ax.plot([0, 0], [0, 2.3], 'k-', lw=lw)                    # z
    ax.plot([0, 3.35], [0, 0], 'k-', lw=lw)                   # x
    ax.plot([0, -0.71], [0, -0.60], 'k-', lw=lw)              # y
    # K' 系（原点在右上）
    ox, oy = 0.85, 0.26
    ax.plot([ox, ox], [oy, 2.3], 'k-', lw=lw)                 # z'
    ax.plot([ox, 3.35], [oy, oy], 'k-', lw=lw)                # x'
    ax.plot([ox, -0.03], [oy, -0.50], 'k-', lw=lw)            # y'
    # 轴标
    ax.text(0, 2.44, r'$z$', ha='center', va='bottom', fontsize=10)
    ax.text(ox, 2.44, r"$z'$", ha='center', va='bottom', fontsize=10)
    ax.text(3.48, 0.0, r'$x$', ha='left', va='center', fontsize=10)
    ax.text(3.48, oy, r"$x'$", ha='left', va='center', fontsize=10)
    ax.text(-0.84, -0.72, r'$y$', ha='center', va='center', fontsize=10)
    ax.text(-0.20, -0.68, r"$y'$", ha='center', va='center', fontsize=10)
    # x' 轴上的点 B, A, C（刻度短线）
    yb = oy
    for xb, lab in [(1.60, r'$B$'), (2.40, r'$A$'), (3.19, r'$C$')]:
        ax.plot([xb, xb], [yb - 0.09, yb + 0.09], 'k-', lw=0.9)
        ax.text(xb, yb + 0.22, lab, ha='center', va='bottom', fontsize=10)
    # 从 A 发出的两个相反方向的信号箭头
    arrow(ax, 2.11, yb + 0.12, 1.72, yb + 0.12, lw=0.9, ms=8)
    arrow(ax, 2.69, yb + 0.12, 3.12, yb + 0.12, lw=0.9, ms=8)
    save(fig, 1)


# ---------------------------------------------------------------- 图 2
def fig_2():
    fig = plt.figure(figsize=(2.75, 2.75))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-1.72, 1.78)
    ax.set_ylim(-1.72, 1.72)
    # 坐标轴 t, x（细线，无箭头）
    ax.plot([0, 0], [-1.55, 1.55], 'k-', lw=0.9)
    ax.plot([-1.42, 1.50], [0, 0], 'k-', lw=0.9)
    ax.text(-0.12, 1.58, r'$t$', ha='center', va='bottom', fontsize=10)
    ax.text(1.58, 0.02, r'$x$', ha='left', va='center', fontsize=10)
    ax.text(-0.20, -0.26, r'$O$', ha='center', va='center', fontsize=10)
    # 四条 45° 世界线：a、c（带箭头，指向上方），b、d（不带箭头）
    L = 1.28
    s = 1.0 / np.sqrt(2.0)
    arrow(ax, 0.04 * s, 0.04 * s, -L * s, L * s, lw=1.4, ms=11)
    arrow(ax, 0.04 * s, 0.04 * s, L * s, L * s, lw=1.4, ms=11)
    ax.plot([0, L * s], [0, -L * s], 'k-', lw=1.4)
    ax.plot([0, -L * s], [0, -L * s], 'k-', lw=1.4)
    ax.text(-L * s - 0.13, L * s + 0.06, r'$a$', ha='center', va='center', fontsize=10)
    ax.text(L * s + 0.13, L * s + 0.06, r'$c$', ha='center', va='center', fontsize=10)
    ax.text(-L * s - 0.13, -L * s - 0.08, r'$d$', ha='center', va='center', fontsize=10)
    ax.text(L * s + 0.15, -L * s - 0.08, r'$b$', ha='center', va='center', fontsize=10)
    # 区域标注（照原书中文）
    ax.text(0.10, 0.78, '绝对未来', ha='center', va='center', fontsize=8.5)
    ax.text(0.02, -0.84, '绝对过去', ha='center', va='center', fontsize=8.5)
    ax.text(-0.82, 0.10, '绝对分隔', ha='center', va='center', fontsize=8.5)
    ax.text(0.84, 0.10, '绝对分隔', ha='center', va='center', fontsize=8.5)
    save(fig, 2)


# ---------------------------------------------------------------- 图 3
def _tangent_m(xc, a, b, xa):
    """过椭圆 (x-xc)^2/a^2 + y^2/b^2 = 1、点 (xa,0)（长轴上外侧）的切线斜率。"""
    u = b**2 / ((xa - xc)**2 - a**2)      # m^2, 由判别式=0
    return np.sqrt(u)


def fig_3():
    fig = plt.figure(figsize=(3.6, 1.85))
    a, b = 1.15, 0.73

    # ---- (a) V < v0 : A 在椭圆内部
    ax = new_ax(fig, [0.005, 0.02, 0.44, 0.90])
    ax.set_xlim(-1.50, 1.40)
    ax.set_ylim(-1.15, 1.05)
    ax.add_patch(Ellipse((0, 0), 2 * a, 2 * b, fill=False, lw=LW_MAIN))
    ax.plot([-a, a], [0, 0], 'k--', lw=LW_AUX)
    A = np.array([-0.50, 0.0])
    tP = np.deg2rad(57.0)
    P = np.array([a * np.cos(tP), b * np.sin(tP)])
    ax.plot([0, P[0]], [0, P[1]], 'k-', lw=0.8)               # 细线 O->P
    arrow(ax, A[0], A[1], P[0], P[1], lw=1.3, ms=11)          # 矢量 p
    ax.plot(0, 0, 'ko', ms=2.5)
    th = np.rad2deg(np.arctan2(P[1] - A[1], P[0] - A[0]))
    ax.add_patch(Arc(A, 0.60, 0.60, angle=0, theta1=0, theta2=th, lw=0.8))
    ax.text(A[0] + 0.44, 0.13, r'$\theta$', ha='left', va='center', fontsize=10)
    ax.text(-0.33, 0.36, r'$\boldsymbol{p}$', ha='center', va='bottom', fontsize=10)
    ax.text(A[0], -0.22, r'$A$', ha='center', va='top', fontsize=10)
    ax.text(0.10, -0.22, r'$O$', ha='center', va='top', fontsize=10)
    ax.text(-0.05, -0.92, r'(a) $V < v_0$', ha='center', va='center', fontsize=9)

    # ---- (b) V > v0 : A 在椭圆外部, 有切线 theta_max
    ax = new_ax(fig, [0.475, 0.02, 0.52, 0.90])
    xc = 0.55
    ax.set_xlim(-1.80, 2.25)
    ax.set_ylim(-1.15, 1.05)
    ax.add_patch(Ellipse((xc, 0), 2 * a, 2 * b, fill=False, lw=LW_MAIN))
    A = np.array([-1.05, 0.0])
    # 切线
    m = _tangent_m(xc, a, b, A[0])
    # 切点: 重根位置
    u = m * m
    xt = (b**2 * xc + a**2 * u * A[0]) / (b**2 + a**2 * u)
    yt = m * (xt - A[0])
    ax.plot([A[0], xt], [A[1], yt], 'k--', lw=LW_AUX)          # 切线(虚线)
    ax.plot([A[0], xc + a], [0, 0], 'k--', lw=LW_AUX)          # 长轴虚线
    tP = np.deg2rad(52.0)
    P = np.array([xc + a * np.cos(tP), b * np.sin(tP)])
    ax.plot([xc, P[0]], [0, P[1]], 'k-', lw=0.8)
    arrow(ax, A[0], A[1], P[0], P[1], lw=1.3, ms=11)
    ax.plot(xc, 0, 'ko', ms=2.5)
    th = np.rad2deg(np.arctan2(P[1], P[0] - A[0]))
    ax.add_patch(Arc(A, 1.10, 1.10, angle=0, theta1=0, theta2=th, lw=0.8))
    ax.text(A[0] + 0.78, 0.11, r'$\theta$', ha='center', va='center', fontsize=10)
    thm = np.rad2deg(np.arctan(m))
    ax.add_patch(Arc(A, 0.76, 0.76, angle=0, theta1=0, theta2=thm, lw=0.8))
    ax.text(A[0] + 0.17, 0.47, r'$\theta_{\mathrm{max}}$', ha='center',
            va='bottom', fontsize=10)
    ax.text(0.43, 0.52, r'$\boldsymbol{p}$', ha='center', va='bottom', fontsize=10)
    ax.text(A[0], -0.22, r'$A$', ha='center', va='top', fontsize=10)
    ax.text(xc + 0.10, -0.22, r'$O$', ha='center', va='top', fontsize=10)
    ax.text(0.25, -0.92, r'(b) $V > v_0$', ha='center', va='center', fontsize=9)
    save(fig, 3)


# ---------------------------------------------------------------- 图 4
def fig_4():
    fig = plt.figure(figsize=(3.6, 2.0))
    a, b = 1.30, 0.82

    def panel(ax, Ax, tag, cond):
        ax.set_xlim(-2.95, 2.05)
        ax.set_ylim(-1.30, 1.35)
        ax.add_patch(Ellipse((0, 0), 2 * a, 2 * b, fill=False, lw=LW_MAIN))
        A = np.array([Ax, 0.0])
        B = np.array([a, 0.0])
        C = np.array([0.0, b])
        if Ax < -a:          # (a) 虚线: 无
            pass
        else:                # (b) A 在椭圆内, 左顶点到 A 虚线
            ax.plot([-a, Ax], [0, 0], 'k--', lw=LW_AUX)
        arrow(ax, A[0], A[1], B[0], B[1], lw=1.3, ms=11)      # p1
        arrow(ax, A[0], A[1], C[0], C[1], lw=1.3, ms=11)      # p1'
        arrow(ax, C[0], C[1], B[0], B[1], lw=1.3, ms=11)      # p2'
        ax.plot(0, 0, 'ko', ms=2.5)
        # theta1 (at A), theta2 (at B)
        th1 = np.rad2deg(np.arctan2(C[1], C[0] - A[0]))
        r1 = 0.30 if Ax < -a else 0.27
        ax.add_patch(Arc(A, 2 * r1, 2 * r1, angle=0, theta1=0, theta2=th1, lw=0.8))
        ax.text(A[0] + r1 + (0.30 if Ax < -a else 0.20), 0.12, r'$\theta_1$',
                ha='left', va='center', fontsize=10)
        th2 = np.rad2deg(np.arctan2(C[1], C[0] - B[0]))
        ax.add_patch(Arc(B, 0.70, 0.70, angle=0, theta1=th2, theta2=180, lw=0.8))
        ax.text(B[0] - 0.62, 0.15, r'$\theta_2$', ha='center', va='center', fontsize=10)
        # 矢量标号
        xm = (A[0] + B[0]) / 2
        ax.text(0.06 if Ax < -a else -0.17, -0.20, r'$\boldsymbol{p}_1$',
                ha='center', va='top', fontsize=10)
        if Ax < -a:
            ax.text(-0.42, 0.35, r"$\boldsymbol{p}'_1$", ha='center', va='center', fontsize=10)
            ax.text(0.10, 0.46, r"$\boldsymbol{p}'_2$", ha='center', va='center', fontsize=10)
        else:
            ax.text(-0.63, 0.35, r"$\boldsymbol{p}'_1$", ha='center', va='center', fontsize=10)
            ax.text(0.18, 0.46, r"$\boldsymbol{p}'_2$", ha='center', va='center', fontsize=10)
        ax.text(A[0], -0.22, r'$A$', ha='center', va='top', fontsize=10)
        ax.text(B[0] + 0.17, 0.0, r'$B$', ha='left', va='center', fontsize=10)
        ax.text(0.0, b + 0.16, r'$C$', ha='center', va='bottom', fontsize=10)
        ax.text(-0.2 if Ax < -a else 0.1, -1.02, tag, ha='center', va='center', fontsize=9)

    ax = new_ax(fig, [0.005, 0.02, 0.46, 0.90])
    panel(ax, -2.25, r'(a) $m_1 > m_2$', None)
    ax = new_ax(fig, [0.50, 0.02, 0.47, 0.90])
    panel(ax, -0.65, r'(b) $m_1 < m_2$', None)
    save(fig, 4)


# ---------------------------------------------------------------- 图 5
def fig_5():
    fig = plt.figure(figsize=(3.15, 2.25))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-2.20, 2.30)
    ax.set_ylim(-1.30, 1.80)
    a, b = 1.50, 0.90
    ax.add_patch(Ellipse((0, 0), 2 * a, 2 * b, fill=False, lw=LW_MAIN))
    A = np.array([-a, 0.0])
    B = np.array([a, 0.0])
    C = np.array([0.0, b])
    arrow(ax, A[0], A[1], B[0], B[1], lw=1.3, ms=11)          # A->B
    arrow(ax, A[0], A[1], C[0], C[1], lw=1.3, ms=11)          # A->C
    arrow(ax, C[0], C[1], B[0], B[1], lw=1.3, ms=11)          # C->B
    # C 到中心的虚线 + 中心点
    ax.plot([C[0], 0], [C[1], 0], 'k--', lw=LW_AUX)
    ax.plot(0, 0, 'ko', ms=2.5)
    # AC 延长虚线
    u = (C - A) / np.linalg.norm(C - A)
    E = C + 0.78 * u
    ax.plot([C[0], E[0]], [C[1], E[1]], 'k--', lw=LW_AUX)
    # theta_min 在 C 处: 延长线方向与 CB 方向之间
    dir_ext = np.rad2deg(np.arctan2(u[1], u[0]))
    dir_cb = np.rad2deg(np.arctan2(B[1] - C[1], B[0] - C[0]))
    ax.add_patch(Arc(C, 0.84, 0.84, angle=0, theta1=dir_cb, theta2=dir_ext, lw=0.8))
    ax.text(C[0] + 0.60, C[1] + 0.04, r'$\theta_{\mathrm{min}}$',
            ha='left', va='center', fontsize=10)
    # theta1 at A, theta2 at B
    th1 = np.rad2deg(np.arctan2(C[1], C[0] - A[0]))
    ax.add_patch(Arc(A, 0.80, 0.80, angle=0, theta1=0, theta2=th1, lw=0.8))
    ax.text(-0.92, 0.13, r'$\theta_1$', ha='center', va='center', fontsize=10)
    th2 = np.rad2deg(np.arctan2(C[1], C[0] - B[0]))
    ax.add_patch(Arc(B, 0.80, 0.80, angle=0, theta1=th2, theta2=180, lw=0.8))
    ax.text(0.92, 0.13, r'$\theta_2$', ha='center', va='center', fontsize=10)
    # 顶点标号
    ax.text(A[0] - 0.18, -0.06, r'$A$', ha='right', va='center', fontsize=10)
    ax.text(B[0] + 0.16, -0.05, r'$B$', ha='left', va='center', fontsize=10)
    ax.text(0.0, b + 0.17, r'$C$', ha='center', va='bottom', fontsize=10)
    save(fig, 5)


# ---------------------------------------------------------------- 图 6
def _trochoid_arrow(ax, phi, alpha, h=0.12):
    """在 x=alpha*phi-sin(phi), y=1-cos(phi) 曲线上 phi 处画顺流箭头."""
    p1 = np.array([alpha * (phi - h) - np.sin(phi - h), 1 - np.cos(phi - h)])
    p2 = np.array([alpha * (phi + h) - np.sin(phi + h), 1 - np.cos(phi + h)])
    arrow(ax, p1[0], p1[1], p2[0], p2[1], lw=1.3, ms=9)


def _panel6(ax, alpha, phi0, phi1, xlim, ylim, ytop, xleft, xext, tag, tagy,
            arrows):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    # 坐标轴: y 轴过第一个触点/尖点 (x=0), x 轴沿 y=0
    ax.plot([0, 0], [0, ytop], 'k-', lw=0.9)
    ax.plot([xleft, xext], [0, 0], 'k-', lw=0.9)
    ax.text(0, ytop + 0.05 * (ylim[1] - ylim[0]), r'$y$', ha='center',
            va='bottom', fontsize=10)
    ax.text(xext + 0.04 * (xlim[1] - xlim[0]), 0, r'$x$', ha='left',
            va='center', fontsize=10)
    # 轨迹
    phi = np.linspace(phi0, phi1, 1200)
    X = alpha * phi - np.sin(phi)
    Y = 1 - np.cos(phi)
    ax.plot(X, Y, 'k-', lw=1.4)
    for pa in arrows:
        _trochoid_arrow(ax, pa, alpha)
    ax.text((xleft + xext) / 2, tagy, tag, ha='center', va='center', fontsize=9)


def fig_6():
    twopi = 2 * np.pi
    # 各面板独立等比、尽量充满面板框（与原书一致: 三个面板绘幅相近）
    fig = plt.figure(figsize=(2.45, 4.55))
    # (a) a > cE_y/H : 有环
    ax = new_ax(fig, [0.10, 0.6088, 0.88, 0.3692])
    _panel6(ax, 0.55, -2.35, twopi + 2.35, (-0.45, 4.85), (-0.90, 3.00),
            2.82, -0.32, 4.73, r'(a)', -0.55,
            [-2.05, 1.9, 4.6, twopi + 2.05])
    # (b) a < cE_y/H : 波浪
    ax = new_ax(fig, [0.10, 0.3560, 0.88, 0.2418])
    _panel6(ax, 2.3, -2.1, twopi + 2.1, (-4.3, 18.8), (-1.95, 9.55),
            9.2, -2.0, 16.9, r'(b)', -1.30,
            [-1.7, 1.2, twopi - 1.2, twopi + 1.2])
    # (c) a = cE_y/H : 普通摆线（尖点）
    ax = new_ax(fig, [0.10, 0.0110, 0.88, 0.3341])
    _panel6(ax, 1.0, -2.18, twopi + 2.18, (-1.40, 8.90), (-1.40, 5.70),
            5.45, -2.1, 8.80, r'(c)', -1.00,
            [-1.6, 1.7, twopi - 1.7, twopi + 1.7])
    save(fig, 6)


if __name__ == '__main__':
    for f in (fig_1, fig_2, fig_3, fig_4, fig_5, fig_6):
        f()
