# -*- coding: utf-8 -*-
# 批次 FB：图7-图17 重绘（朗道《场论》卷2 重排本）
# 图7(p164) 波面主曲率线元与曲率中心；图8(p172) 纵向均匀磁场"磁透镜"；
# 图9(p179) 衍射面积元 df 到 P 点；图10(p181) 波面 ab 与焦散面 a'b'；
# 图11(p184) 屏边缘线半平面（阴影边缘）；图12(p187) 直边衍射 I/I0 对 w；
# 图13(p189) 狭缝夫琅禾费衍射几何；图14(p190) sin^2 x / x^2 曲线；
# 图15(p236) 同步辐射辐射锥（w, v/c, n, chi, alpha）；
# 图16(p238) 圆轨道运动电荷的辐射几何（z,x,y,H,k,r,v,theta,phi）；
# 图17(p241) 谱函数 F(xi)=xi*int_xi^inf K_{5/3}。
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Ellipse
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
FS = 10


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


def arrow(ax, x0, y0, x1, y1, lw=LW_MAIN, ms=10, zorder=6):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), zorder=zorder,
                arrowprops=dict(arrowstyle='-|>', color='k',
                                lw=lw, mutation_scale=ms,
                                shrinkA=0, shrinkB=0))


def bez(p0, p1, p2, n=120):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * t * (1 - t) * np.array(p1) \
        + t ** 2 * np.array(p2)


def catmull(pts, n=24):
    """Catmull-Rom 样条（开放），返回 (2, N) 便于 ax.plot(*arr)。"""
    P = np.asarray(pts, float)
    m = len(P)
    out = []
    for i in range(m - 1):
        p0 = P[max(i - 1, 0)]
        p1 = P[i]
        p2 = P[i + 1]
        p3 = P[min(i + 2, m - 1)]
        t = np.linspace(0, 1, n, endpoint=(i == m - 2))[:, None]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t +
                          (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2 +
                          (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    return np.vstack(out).T


def wavy(p0, p1, amp=0.035, n=40, seed=1):
    """两点间带小波浪的线（原书'锯齿形截断边'）。"""
    p0 = np.array(p0, float)
    p1 = np.array(p1, float)
    t = np.linspace(0, 1, n)
    base = p0[None, :] + t[:, None] * (p1 - p0)[None, :]
    d = p1 - p0
    L = np.hypot(*d)
    nvec = np.array([-d[1], d[0]]) / L
    rng = np.random.RandomState(seed)
    ph = rng.uniform(0, 2 * np.pi, 3)
    fr = rng.uniform(6, 10, 3)
    off = sum(a * np.sin(fr[k] * np.pi * t + ph[k])
              for k, a in enumerate([amp, amp * 0.6, amp * 0.4]))
    return base + nvec[None, :] * off[:, None]


# ---------------------------------------------------------------- 图 7
def fig_7():
    fig = plt.figure(figsize=(3.4, 1.5))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-1.05, 3.50)
    ax.set_ylim(-1.00, 0.95)
    O = (0.0, 0.0)
    O1 = (2.66, -0.06)
    O2 = (1.58, -0.02)
    A = (-0.62, 0.03)
    B = (3.10, -0.04)
    a = (-0.32, -0.29)
    b = (0.27, 0.57)
    c = (0.33, 0.14)
    d = (0.02, -0.43)
    TR = (0.53, 0.61)     # 面片右上角
    RC = (0.32, -0.29)    # 面片右下角
    TIP = (-0.27, -0.63)  # 面片下角
    xe = (-0.38, 0.005)   # 光轴与面片左缘交点
    # 面片边界（四条弧）
    ax.plot(*catmull([TIP, a, (-0.34, 0.00), (-0.20, 0.30), b]),
            'k-', lw=LW_MAIN)
    ax.plot(*catmull([b, (0.41, 0.615), TR]), 'k-', lw=LW_MAIN)
    ax.plot(*catmull([TR, (0.38, 0.25), (0.34, 0.05), RC]),
            'k-', lw=LW_MAIN)
    ax.plot(*catmull([RC, d, TIP]), 'k-', lw=LW_MAIN)
    # 主截线（虚线）：a-O-c 与 b-O-d
    ax.plot(*bez(a, (-0.005, 0.075), c).T, 'k--', lw=LW_AUX)
    ax.plot(*bez(b, (-0.145, -0.07), d).T, 'k--', lw=LW_AUX)
    # 光轴：A 到面片为实线，面片之后到 O 为虚线（被波面挡住），O 以后实线
    ax.plot([A[0], xe[0]], [A[1], xe[1]], 'k-', lw=1.0)
    ax.plot([xe[0], O[0]], [xe[1], O[1]], 'k--', lw=LW_AUX)
    ax.plot([O[0], B[0]], [O[1], B[1]], 'k-', lw=1.0)
    # 四根光线：a、c 汇于 O1；b、d 汇于 O2
    ax.plot([a[0], O1[0]], [a[1], O1[1]], 'k-', lw=1.0)
    ax.plot([c[0], O1[0]], [c[1], O1[1]], 'k-', lw=1.0)
    ax.plot([b[0], O2[0]], [b[1], O2[1]], 'k-', lw=1.0)
    ax.plot([d[0], O2[0]], [d[1], O2[1]], 'k-', lw=1.0)
    # 点
    for P in (O, O1, O2):
        ax.plot(*P, 'ko', ms=2.5)
    # 标注
    ax.text(A[0] - 0.08, A[1], r'$A$', ha='right', va='center', fontsize=FS)
    ax.text(B[0] + 0.07, B[1], r'$B$', ha='left', va='center', fontsize=FS)
    ax.text(-0.08, 0.08, r'$O$', ha='right', va='bottom', fontsize=FS)
    ax.text(O2[0] - 0.03, O2[1] - 0.07, r'$O_2$', ha='center', va='top',
            fontsize=FS)
    ax.text(O1[0] + 0.03, O1[1] - 0.07, r'$O_1$', ha='center', va='top',
            fontsize=FS)
    ax.text(a[0] - 0.08, a[1] - 0.02, r'$a$', ha='right', va='center',
            fontsize=FS)
    ax.text(b[0] - 0.03, b[1] + 0.07, r'$b$', ha='center', va='bottom',
            fontsize=FS)
    ax.text(c[0] + 0.09, c[1] + 0.05, r'$c$', ha='left', va='bottom',
            fontsize=FS)
    ax.text(d[0] + 0.03, d[1] - 0.08, r'$d$', ha='left', va='top',
            fontsize=FS)
    save(fig, 7)


# ---------------------------------------------------------------- 图 8
def fig_8():
    fig = plt.figure(figsize=(2.6, 1.1))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-1.45, 2.45)
    ax.set_ylim(-0.52, 0.52)
    x0, xl = 0.0, 1.35
    # 虚线轴
    ax.plot([-1.30, x0], [0, 0], 'k--', lw=LW_AUX)
    ax.plot([xl, 2.10], [0, 0], 'k--', lw=LW_AUX)
    ax.text(2.10, -0.10, r'$x$', ha='center', va='top', fontsize=FS)
    # 两条竖直线
    for x in (x0, xl):
        ax.plot([x, x], [-0.30, 0.30], 'k-', lw=1.1)
    # 三根箭头
    for y in (0.17, 0.0, -0.17):
        arrow(ax, x0, y, xl, y, lw=1.1, ms=11)
    # 标注
    ax.text(-0.62, 0.07, r'$1$', ha='center', va='bottom', fontsize=FS)
    ax.text(0.68, 0.28, r'$3$', ha='center', va='bottom', fontsize=FS)
    ax.text(1.72, 0.07, r'$2$', ha='center', va='bottom', fontsize=FS)
    ax.text(x0, -0.36, r'$x=0$', ha='center', va='top', fontsize=FS)
    ax.text(xl, -0.36, r'$x=l$', ha='center', va='top', fontsize=FS)
    save(fig, 8)


# ---------------------------------------------------------------- 图 9
def fig_9():
    fig = plt.figure(figsize=(2.4, 2.5))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-1.10, 1.55)
    ax.set_ylim(-1.25, 1.30)
    xs = -0.55
    # 屏（上下两段实线）
    ax.plot([xs, xs], [0.55, 1.10], 'k-', lw=1.1)
    ax.plot([xs, xs], [-0.55, -1.10], 'k-', lw=1.1)
    # 孔上面元 df：向右凸的虚线弧
    arc = bez((xs, 0.55), (0.10, 0.0), (xs, -0.55))
    ax.plot(arc[:, 0], arc[:, 1], 'k--', lw=LW_AUX)
    P = (-0.233, 0.088)   # 弧上的 df 点
    # 法线 n
    arrow(ax, P[0], P[1], 0.10, 0.03, lw=1.3, ms=12)
    ax.text(0.10, -0.06, r'$\boldsymbol{n}$', ha='center', va='top',
            fontsize=FS)
    # R 线到 P 点
    Pt = (0.98, 1.02)
    ax.plot([P[0], Pt[0]], [P[1], Pt[1]], 'k-', lw=1.0)
    arrow(ax, P[0] + 0.30 * (Pt[0] - P[0]), P[1] + 0.30 * (Pt[1] - P[1]),
          P[0] + 0.42 * (Pt[0] - P[0]), P[1] + 0.42 * (Pt[1] - P[1]),
          lw=1.0, ms=10)
    ax.plot(*Pt, 'ko', ms=3)
    ax.text(Pt[0] + 0.06, Pt[1] + 0.03, r'$P$', ha='left', va='center',
            fontsize=FS)
    ax.text(0.33, 0.60, r'$R$', ha='center', va='bottom', fontsize=FS)
    ax.text(P[0] - 0.08, P[1] - 0.02, r'$\mathrm{d}f$', ha='right',
            va='center', fontsize=FS)
    save(fig, 9)


# ---------------------------------------------------------------- 图 10
def fig_10():
    fig = plt.figure(figsize=(3.5, 2.1))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-3.75, 1.85)
    ax.set_ylim(-0.95, 2.85)
    O = (0.0, 0.0)
    Q = (-3.2, 0.0)
    Qp = (-2.36, 1.89)
    ae = (-3.15, -0.55)   # a
    be = (-1.76, 2.41)    # b
    ap = (-1.17, 1.24)    # a'
    Op = (-0.45, 0.17)    # O'
    bp = (1.27, 0.73)     # b'
    C = (0.0, 1.14)       # O 处曲率中心
    Ppt = (0.0, 0.33)
    # 波面 ab（粗弧）
    ax.plot(*catmull([ae, Q, Qp, be]), 'k-', lw=1.4)
    # 焦散面 a'b'（粗 U 形）
    ax.plot(*catmull([ap, (-0.83, 0.65), Op, O, (0.62, 0.28), bp]),
            'k-', lw=1.4)
    # 光线 QO（水平）与切线 Q'O'
    ax.plot([Q[0], O[0]], [Q[1], O[1]], 'k-', lw=1.0)
    V = (-0.26, 0.0)   # 切线与 QO 延线的交点
    ax.plot([Qp[0], V[0]], [Qp[1], V[1]], 'k-', lw=1.0)
    # O 处法线（竖直线）与虚半径 C-O'
    ax.plot([O[0], C[0]], [O[1], C[1]], 'k-', lw=1.0)
    ax.plot([C[0], Op[0]], [C[1], Op[1]], 'k--', lw=LW_AUX)
    # 角弧：底部 theta（QO 与切线）、顶部 theta（CO 与 CO'）
    ax.add_patch(Arc(V, 0.66, 0.66, theta1=138, theta2=180, lw=0.8))
    th = np.deg2rad(159)
    ax.text(V[0] + 0.50 * np.cos(th), V[1] + 0.50 * np.sin(th),
            r'$\theta$', ha='center', va='center', fontsize=FS)
    ax.add_patch(Arc(C, 0.60, 0.60, theta1=245, theta2=270, lw=0.8))
    th = np.deg2rad(257)
    ax.text(C[0] + 0.44 * np.cos(th), C[1] + 0.44 * np.sin(th),
            r'$\theta$', ha='center', va='center', fontsize=FS)
    # P 点与 x
    ax.plot(*Ppt, 'ko', ms=3)
    ax.text(Ppt[0] + 0.09, Ppt[1] - 0.01, r'$P$', ha='left', va='center',
            fontsize=FS)
    ax.text(-0.08, 0.17, r'$x$', ha='right', va='center', fontsize=FS)
    ax.text(0.09, 0.78, r'$\rho$', ha='left', va='center', fontsize=FS)
    # 各点字母
    ax.text(O[0], O[1] - 0.16, r'$O$', ha='center', va='top', fontsize=FS)
    ax.text(Op[0] - 0.07, Op[1] + 0.12, r"$O'$", ha='right', va='bottom',
            fontsize=FS)
    ax.text(Q[0] - 0.10, Q[1] - 0.02, r'$Q$', ha='right', va='center',
            fontsize=FS)
    ax.text(Qp[0] - 0.08, Qp[1] + 0.08, r"$Q'$", ha='right', va='bottom',
            fontsize=FS)
    ax.text(ae[0] + 0.02, ae[1] - 0.10, r'$a$', ha='center', va='top',
            fontsize=FS)
    ax.text(be[0] + 0.08, be[1] + 0.04, r'$b$', ha='left', va='center',
            fontsize=FS)
    ax.text(ap[0] - 0.02, ap[1] + 0.10, r"$a'$", ha='right', va='bottom',
            fontsize=FS)
    ax.text(bp[0] + 0.08, bp[1] + 0.08, r"$b'$", ha='left', va='bottom',
            fontsize=FS)
    ax.text(-1.6, -0.20, r'$D$', ha='center', va='top', fontsize=FS)
    save(fig, 10)


# ---------------------------------------------------------------- 图 11
def fig_11():
    fig = plt.figure(figsize=(3.2, 2.3))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-2.45, 2.85)
    ax.set_ylim(-2.05, 1.75)
    O = (0.0, 0.0)
    a_y = np.deg2rad(38.0)    # y 轴仰角
    a_ed = np.deg2rad(23.0)   # 屏边缘线仰角
    ey = (np.cos(a_y), np.sin(a_y))
    # 屏半平面（阴影线填充），边界：边缘线 + 三条波浪截断边
    e1 = (-0.97, -0.46)
    e2 = (1.02, 0.42)
    r1 = (1.21, -0.68)
    r2 = (-0.93, -1.61)
    poly = np.vstack([
        np.linspace(e1[0], e2[0], 2), np.linspace(e1[1], e2[1], 2)
    ]).T
    right = wavy(e2, r1, amp=0.045, seed=3)
    bot = wavy(r1, r2, amp=0.05, seed=7)
    left = wavy(r2, e1, amp=0.045, seed=5)
    ax.fill(np.vstack([poly, right, bot, left])[:, 0],
            np.vstack([poly, right, bot, left])[:, 1],
            facecolor='none', edgecolor='k', lw=0.0, hatch='/////////',
            zorder=1)
    # 边缘线（粗）
    ax.plot([e1[0], e2[0]], [e1[1], e2[1]], 'k-', lw=1.3, zorder=3)
    # 坐标轴（画在阴影之上）
    ax.plot([-1.18 * ey[0], 1.72 * ey[0]], [-1.18 * ey[1], 1.72 * ey[1]],
            'k-', lw=1.0, zorder=4)
    ax.plot([-1.85, 2.35], [0, 0], 'k-', lw=1.0, zorder=4)
    ax.plot([0, 0], [-1.60, 1.28], 'k-', lw=1.0, zorder=4)
    ax.text(1.72 * ey[0] + 0.06, 1.72 * ey[1] + 0.02, r'$y$', ha='left',
            va='center', fontsize=FS)
    ax.text(2.42, 0.0, r'$x$', ha='left', va='center', fontsize=FS)
    ax.text(0.0, 1.34, r'$z$', ha='center', va='bottom', fontsize=FS)
    ax.text(0.05, -0.08, r'$O$', ha='left', va='top', fontsize=FS)
    # 角 alpha（y 轴与边缘线之间）
    ax.add_patch(Arc(O, 0.64, 0.64, theta1=23, theta2=38, lw=0.8))
    th = np.deg2rad(30.5)
    ax.text(0.46 * np.cos(th), 0.46 * np.sin(th), r'$\alpha$',
            ha='center', va='center', fontsize=FS)
    # Q、Dq、Dp、P、d
    ax.plot(-1.55, 0, 'ko', ms=3)
    ax.text(-1.58, 0.11, r'$Q$', ha='center', va='bottom', fontsize=FS)
    ax.text(-0.89, 0.11, r'$D_q$', ha='center', va='bottom', fontsize=FS)
    ax.text(1.40, 0.11, r'$D_p$', ha='center', va='bottom', fontsize=FS)
    ax.plot(1.99, 0.38, 'ko', ms=3)
    ax.plot([1.99, 1.99], [0.0, 0.38], 'k--', lw=LW_AUX)
    ax.text(2.03, 0.46, r'$P$', ha='left', va='bottom', fontsize=FS)
    ax.text(1.87, 0.19, r'$d$', ha='right', va='center', fontsize=FS)
    save(fig, 11)


# ---------------------------------------------------------------- 图 12
def fig_12():
    from scipy.special import fresnel
    fig = plt.figure(figsize=(3.6, 2.0))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96], equal=False)
    ax.set_xlim(-5.35, 13.35)
    ax.set_ylim(-0.14, 1.66)
    v = np.linspace(-4.6, 11.6, 1500)
    s, c = fresnel(v / np.sqrt(np.pi / 2.0))  # 标准 Fresnel C(v),S(v)
    I = 0.5 * ((c + 0.5) ** 2 + (s + 0.5) ** 2)
    ax.plot(v, I, 'k-', lw=1.3, zorder=5)
    # 轴
    ax.plot([-5.0, 12.9], [0, 0], 'k-', lw=1.0)
    ax.plot([0, 0], [0, 1.52], 'k-', lw=1.0)
    ax.text(13.1, -0.02, r'$w$', ha='left', va='center', fontsize=FS)
    ax.text(-0.18, 1.55, r'$\dfrac{I}{I_0}$', ha='right', va='center',
            fontsize=FS)
    # 渐近线 I=1（虚线）
    ax.plot([0, 12.5], [1, 1], 'k--', lw=LW_AUX)
    # 区域标注（照原书中文）
    ax.text(-2.55, 0.22, '几何影区', ha='center', va='center', fontsize=7.5)
    ax.text(6.3, 0.50, '照明区', ha='center', va='center', fontsize=7.5)
    save(fig, 12)


# ---------------------------------------------------------------- 图 13
def fig_13():
    fig = plt.figure(figsize=(2.3, 2.3))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-1.35, 1.25)
    ax.set_ylim(-1.15, 1.25)
    # 屏截面（y 轴上的两段，中间为狭缝 -a..+a）
    ax.plot([-1.05, -0.30], [0, 0], 'k-', lw=1.1)
    ax.plot([0.30, 0.95], [0, 0], 'k-', lw=1.1)
    ax.text(0.99, 0.05, r'$y$', ha='left', va='bottom', fontsize=FS)
    ax.text(-0.44, -0.13, r'$-a$', ha='center', va='top', fontsize=FS)
    ax.text(0.44, -0.13, r'$+a$', ha='center', va='top', fontsize=FS)
    # x 轴（竖直虚线，指向下）
    ax.plot([0, 0], [0.95, -0.78], 'k--', lw=LW_AUX)
    ax.text(0.0, -0.86, r'$x$', ha='center', va='top', fontsize=FS)
    # 入射波矢 k（实箭头，位于虚线上）
    arrow(ax, 0, 0.72, 0, 0.42, lw=1.2, ms=12)
    ax.text(0.08, 0.60, r'$\boldsymbol{k}$', ha='left', va='center',
            fontsize=FS)
    # 衍射波矢 k'（虚线 + 中途实箭头）
    kd = (0.38, -0.78)
    ax.plot([0, kd[0]], [0, kd[1]], 'k--', lw=LW_AUX)
    arrow(ax, kd[0] * 0.78, kd[1] * 0.78, kd[0] * 0.92, kd[1] * 0.92,
          lw=1.2, ms=12)
    ax.text(kd[0] + 0.09, kd[1] * 0.78 + 0.02, r"$\boldsymbol{k}'$",
            ha='left', va='center', fontsize=FS)
    # 角 theta（x 轴向下方向与 k' 之间的小角）
    ang = np.degrees(np.arctan2(kd[1], kd[0]))  # ≈ -64°
    ax.add_patch(Arc((0, 0), 0.34, 0.34, theta1=-90, theta2=ang, lw=0.8))
    th = np.deg2rad((-90 + ang) / 2)
    ax.text(0.30 * np.cos(th), 0.30 * np.sin(th), r'$\theta$',
            ha='center', va='center', fontsize=FS)
    save(fig, 13)


# ---------------------------------------------------------------- 图 14
def fig_14():
    fig = plt.figure(figsize=(3.3, 1.9))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96], equal=False)
    ax.set_xlim(-18.3, 18.8)
    ax.set_ylim(-0.10, 1.42)
    x = np.linspace(-16.5, 16.5, 3000)
    y = np.sinc(x / np.pi) ** 2   # sin^2 x / x^2, 归一峰=1
    ax.plot(x, y, 'k-', lw=1.2)
    ax.plot([-17.3, 17.3], [0, 0], 'k-', lw=1.0)
    ax.plot([0, 0], [0, 1.12], 'k-', lw=0.8)   # 纵标线（原书峰处竖线）
    ax.text(0.0, -0.075, r'$0$', ha='center', va='top', fontsize=FS)
    ax.text(17.6, 0.0, r'$x$', ha='left', va='center', fontsize=FS)
    ax.text(0.35, 1.14, r'$\dfrac{\sin^2 x}{x^2}$', ha='left', va='bottom',
            fontsize=FS)
    save(fig, 14)


# ---------------------------------------------------------------- 图 15
def fig_15():
    fig = plt.figure(figsize=(2.0, 2.3))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-0.85, 1.45)
    ax.set_ylim(-1.50, 1.50)
    O = (0.0, 0.0)
    # 竖直实线（加速度 w 方向）
    ax.plot([0, 0], [-1.20, 0.98], 'k-', lw=1.2)
    arrow(ax, 0, 0.40, 0, 0.62, lw=1.2, ms=12)
    ax.text(-0.10, 0.52, r'$\boldsymbol{w}$', ha='right', va='center',
            fontsize=FS)
    # 右侧竖直虚线（两支 n 的终点连线）
    ax.plot([1.05, 1.05], [-1.32, 1.32], 'k--', lw=LW_AUX)
    # 三支粗箭头
    arrow(ax, *O, 1.05, 1.22, lw=1.6, ms=13)
    arrow(ax, *O, 1.05, 0.28, lw=1.6, ms=13)
    arrow(ax, *O, 1.05, -1.05, lw=1.6, ms=13)
    ax.text(0.38, 0.76, r'$\boldsymbol{n}$', ha='center', va='bottom',
            fontsize=FS)
    ax.text(0.50, 0.02, r'$\boldsymbol{v}/c$', ha='center', va='top',
            fontsize=FS)
    ax.text(0.85, -0.56, r'$\boldsymbol{n}$', ha='center', va='bottom',
            fontsize=FS)
    # 角弧：chi（上，w 与 n 之间，原书为双弧）、alpha（上 n 与 v/c 之间）、chi（下）
    ax.add_patch(Arc(O, 0.56, 0.56, theta1=49.3, theta2=90, lw=0.8))
    ax.add_patch(Arc(O, 0.72, 0.72, theta1=49.3, theta2=90, lw=0.8))
    th = np.deg2rad(70)
    ax.text(0.50 * np.cos(th), 0.50 * np.sin(th), r'$\chi$',
            ha='center', va='center', fontsize=FS)
    ax.add_patch(Arc(O, 0.80, 0.80, theta1=14.9, theta2=49.3, lw=0.8))
    th = np.deg2rad(32)
    ax.text(0.55 * np.cos(th), 0.55 * np.sin(th), r'$\alpha$',
            ha='center', va='center', fontsize=FS)
    ax.add_patch(Arc(O, 0.64, 0.64, theta1=270, theta2=315, lw=0.8))
    th = np.deg2rad(292)
    ax.text(0.45 * np.cos(th), 0.45 * np.sin(th), r'$\chi$',
            ha='center', va='center', fontsize=FS)
    save(fig, 15)


# ---------------------------------------------------------------- 图 16
def fig_16():
    fig = plt.figure(figsize=(2.7, 2.2))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(-1.05, 1.75)
    ax.set_ylim(-1.40, 1.40)
    O = (0.0, 0.0)
    # 轨道圆（透视椭圆）
    ax.add_patch(Ellipse(O, 1.75, 0.62, fill=False, lw=1.0, zorder=2))
    # 轴
    ax.plot([0, 0], [0, 1.18], 'k-', lw=1.0, zorder=3)
    ax.plot([0, 1.48], [0, 0], 'k-', lw=1.0, zorder=3)
    ax.plot([0, -0.72], [0, -0.63], 'k-', lw=1.0, zorder=3)
    ax.text(-0.06, 1.24, r'$z$', ha='right', va='bottom', fontsize=FS)
    ax.text(1.50, -0.10, r'$y$', ha='left', va='top', fontsize=FS)
    ax.text(-0.68, -0.78, r'$x$', ha='center', va='top', fontsize=FS)
    # 粗箭头 H, k, r, v
    arrow(ax, *O, 0, -1.08, lw=1.6, ms=13)
    ax.text(0.10, -1.02, r'$\boldsymbol{H}$', ha='left', va='center',
            fontsize=FS)
    arrow(ax, *O, 0.66, 0.97, lw=1.6, ms=13)
    ax.text(0.70, 0.88, r'$\boldsymbol{k}$', ha='left', va='center',
            fontsize=FS)
    rp = (0.42, -0.28)
    arrow(ax, *O, *rp, lw=1.6, ms=13)
    ax.text(0.27, -0.15, r'$\boldsymbol{r}$', ha='center', va='bottom',
            fontsize=FS)
    arrow(ax, rp[0], rp[1], rp[0] + 0.54, rp[1] + 0.10, lw=1.6, ms=13)
    ax.text(rp[0] + 0.60, rp[1] + 0.02, r'$\boldsymbol{v}$', ha='left',
            va='center', fontsize=FS)
    # 角弧 theta（z 与 k）、phi（x 与 r）
    ax.add_patch(Arc(O, 0.34, 0.34, theta1=55.8, theta2=90, lw=0.8))
    th = np.deg2rad(74)
    ax.text(0.27 * np.cos(th), 0.27 * np.sin(th), r'$\theta$',
            ha='center', va='center', fontsize=FS)
    ax.add_patch(Arc(O, 0.34, 0.34, theta1=221, theta2=326, lw=0.8))
    th = np.deg2rad(294)
    ax.text(0.21 * np.cos(th), 0.21 * np.sin(th), r'$\varphi$',
            ha='center', va='center', fontsize=FS)
    save(fig, 16)


# ---------------------------------------------------------------- 图 17
def fig_17():
    from scipy.special import kv
    from scipy.integrate import quad

    def F(x):
        return x * quad(lambda t: kv(5.0 / 3.0, t), x, np.inf)[0]

    fig = plt.figure(figsize=(3.3, 1.75))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96], equal=False)
    ax.set_xlim(-0.42, 4.52)
    ax.set_ylim(-0.135, 1.17)
    xs = np.geomspace(0.0015, 4.0, 400)
    ys = np.array([F(x) for x in xs])
    ax.plot(xs, ys, 'k-', lw=1.3, zorder=5)
    # 框（矩形坐标）
    ax.plot([0, 4, 4, 0, 0], [0, 0, 1.0, 1.0, 0], 'k-', lw=0.9)
    # 细网格：竖线 xi=1,2,3；横线 0.5
    for g in (1, 2, 3):
        ax.plot([g, g], [0, 1.0], 'k-', lw=0.5, zorder=1)
    ax.plot([0, 4], [0.5, 0.5], 'k-', lw=0.5, zorder=1)
    # 峰位虚线 xi=0.29
    ax.plot([0.29, 0.29], [0, 0.918], 'k--', lw=LW_AUX)
    # 刻度
    for y in (0.92, 0.5):
        ax.plot([-0.05, 0], [y, y], 'k-', lw=0.8)
    for g in (1, 2, 3, 4):
        ax.plot([g, g], [-0.035, 0], 'k-', lw=0.8)
    # 标注
    ax.text(-0.09, 0.92, r'$0.92$', ha='right', va='center', fontsize=9)
    ax.text(-0.09, 0.5, r'$0.5$', ha='right', va='center', fontsize=9)
    ax.text(-0.09, -0.02, r'$0$', ha='right', va='center', fontsize=9)
    ax.text(0.29, -0.055, r'$0.29$', ha='center', va='top', fontsize=9)
    for g in (1, 2, 3, 4):
        ax.text(g, -0.055, r'$%d$' % g, ha='center', va='top', fontsize=9)
    ax.text(0.0, 1.05, r'$F$', ha='left', va='bottom', fontsize=FS)
    ax.text(4.07, 0.0, r'$\xi$', ha='left', va='center', fontsize=FS)
    save(fig, 17)


if __name__ == '__main__':
    import sys
    which = sys.argv[1:] if len(sys.argv) > 1 else []
    fns = {7: fig_7, 8: fig_8, 9: fig_9, 10: fig_10, 11: fig_11,
           12: fig_12, 13: fig_13, 14: fig_14, 15: fig_15, 16: fig_16,
           17: fig_17}
    for n in (which or [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]):
        fns[int(n)]()
