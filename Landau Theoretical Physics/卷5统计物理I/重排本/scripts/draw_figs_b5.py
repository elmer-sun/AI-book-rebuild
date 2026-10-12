# -*- coding: utf-8 -*-
"""朗道《统计物理学Ⅰ》（卷5）中文重排本插图重绘 · 第五批：图50–图59.

图50  §107 星体密度分布 rho(r)/rho(0) 曲线 1、2（Lane-Emden 多方球 n=3/2 与 n=3）
图51  §107 白矮星质量-半径曲线 M(R)
图52  §109 中子球质量-半径曲线 M(R)
图53  §123 omega 平面围道 C 及其在 alpha 平面的映像 C'
图54  §123 克拉默斯-克勒尼希积分围道（在 0 与 omega_0 处绕开）
图55  §130 布拉维格子旋转对称性定理图（A,B,A',B' 与 phi 角）
图56  §130 十四种布拉维格子
图57  §130 六方(Γ_h)与三方(Γ_rh)格子逐层堆垛示意
图58  §130 简单四方格子加底心点后重联回简单四方
图59  §130 立方格子 Γ_c^f 与 Γ_c^v 的原胞（菱面体）
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch
from scipy.interpolate import CubicSpline, PchipInterpolator

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

OUT = r'E:\AI整理书籍\朗道理论物理教程\卷5统计物理I\重排本\figures'
PRE = OUT + r'\preview'


def save(fig, n):
    fig.savefig(r'%s\fig%d.pdf' % (OUT, n), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(r'%s\fig%d.png' % (PRE, n), dpi=150, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


def arrow(ax, p0, p1, ms=8, lw=1.1, z=6):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=ms,
                                 color='k', lw=lw, shrinkA=0, shrinkB=0, zorder=z))


def lane_emden(n, dxi=2e-3, xi0=0.05):
    """RK4 解 Lane-Emden 方程（级数展开起值, 避开原点奇性）."""
    def f(y, x):
        return np.array([y[1], -2 * y[1] / x - y[0] ** n])
    xi = xi0
    y = np.array([1 - xi0 ** 2 / 6 + xi0 ** 4 / 150,
                  -xi0 / 3 + xi0 ** 3 / 30])
    XIS, TH = [xi], [y[0]]
    h = dxi
    while True:
        k1 = f(y, xi)
        k2 = f(y + h / 2 * k1, xi + h / 2)
        k3 = f(y + h / 2 * k2, xi + h / 2)
        k4 = f(y + h * k3, xi + h)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        xi += h
        if not np.isfinite(y[0]) or y[0] <= 0:
            th_prev = TH[-1]
            xi_prev = XIS[-1]
            frac = th_prev / (th_prev - y[0]) if np.isfinite(y[0]) else 0.5
            XIS.append(xi_prev + h * min(frac, 1.0))
            TH.append(0.0)
            break
        XIS.append(xi)
        TH.append(y[0])
    return np.array(XIS), np.array(TH)


def param_spline(pts, n=500):
    """按弦长参数化的三次样条, pts: (N,2) 有序点列."""
    pts = np.asarray(pts, float)
    d = np.sqrt(((pts[1:] - pts[:-1]) ** 2).sum(1))
    s = np.concatenate([[0], np.cumsum(d)])
    cs_x = CubicSpline(s, pts[:, 0])
    cs_y = CubicSpline(s, pts[:, 1])
    t = np.linspace(s[0], s[-1], n)
    return cs_x(t), cs_y(t)


def dash_line(ax, x0, y0, x1, y1, lw=0.8, dashes=(4, 2.5)):
    ax.plot([x0, x1], [y0, y1], 'k-', lw=lw, dashes=dashes, solid_capstyle='butt')


def pt_circle(ax, x, y, r, filled=False, lw=0.9, z=5):
    ax.add_patch(Circle((x, y), r, fc='k' if filled else 'white',
                        ec='k', lw=lw, zorder=z))


def draw_arc(ax, cx, cy, r, a0, a1, lw=0.8, n=60):
    """数据坐标圆弧点列, 角度制, a0>a1 时顺时针."""
    t = np.radians(np.linspace(a0, a1, n))
    ax.plot(cx + r * np.cos(t), cy + r * np.sin(t), 'k-', lw=lw)


# ---------------------------------------------------------------- 图 50
def fig_50():
    # 两条曲线均按原书图面读数样条复现（原书为手绘曲线, 与严格 Lane-Emden
    # 解在中段略有出入; 验收以页面 PNG 为准）:
    # 曲线1 ≈ n=3/2 多方球 rho/rho0 = theta^(3/2), 曲线2 ≈ 相对论性分布.
    pts1 = [(0, 1), (0.05, 0.985), (0.10, 0.953), (0.15, 0.916), (0.20, 0.872),
            (0.25, 0.823), (0.30, 0.772), (0.35, 0.713), (0.40, 0.650),
            (0.45, 0.578), (0.50, 0.505), (0.55, 0.438), (0.60, 0.372),
            (0.65, 0.310), (0.70, 0.250), (0.75, 0.192), (0.80, 0.135),
            (0.85, 0.088), (0.90, 0.050), (0.95, 0.020), (1.0, 0.0)]
    pts2 = [(0, 1), (0.05, 0.996), (0.10, 0.945), (0.15, 0.775), (0.20, 0.560),
            (0.25, 0.435), (0.30, 0.345), (0.35, 0.262), (0.40, 0.187),
            (0.45, 0.126), (0.50, 0.078), (0.55, 0.042), (0.60, 0.020),
            (0.65, 0.008), (0.70, 0.003), (0.80, 0.0005), (0.90, 0.0),
            (1.0, 0.0)]
    P1 = PchipInterpolator(*np.array(pts1).T)
    P2 = PchipInterpolator(*np.array(pts2).T)
    xx = np.linspace(0, 1, 400)

    fig = plt.figure(figsize=(3.0, 2.75))
    ax = fig.add_axes([0.21, 0.16, 0.70, 0.76])
    ax.set_aspect('equal')
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.03)
    for g in np.arange(0, 1.001, 0.1):
        ax.plot([g, g], [0, 1], 'k-', lw=0.55, zorder=1)
        ax.plot([0, 1], [g, g], 'k-', lw=0.55, zorder=1)
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    ax.plot(xx, P1(xx), 'k-', lw=1.4, zorder=3)
    ax.plot(xx, P2(xx), 'k-', lw=1.4, zorder=3)
    ax.text(0.208, 0.445, '2', fontsize=11, ha='center', va='center', zorder=4)
    ax.text(0.552, 0.425, '1', fontsize=11, ha='center', va='center', zorder=4)
    ax.set_xticks(np.arange(0, 1.01, 0.2))
    ax.set_xticklabels(['0', '0.2', '0.4', '0.6', '0.8', '1.0'])
    ax.set_yticks(np.arange(0.2, 1.01, 0.2))
    ax.tick_params(labelsize=9, length=3, width=0.8)
    ax.set_xlabel(r'$r/R$', fontsize=11, labelpad=2)
    ax.set_ylabel(r'$\dfrac{\rho(r)}{\rho(0)}$', fontsize=12, labelpad=2)
    save(fig, 50)


# ---------------------------------------------------------------- 图 51
def fig_51():
    pts = [(0, 1.455), (1, 1.44), (2, 1.41), (3, 1.35), (4, 1.24), (5, 1.11),
           (6, 0.99), (7, 0.888), (8, 0.78), (9, 0.65), (10, 0.535),
           (11, 0.43), (12, 0.35), (13.25, 0.28)]
    P = PchipInterpolator(*np.array(pts).T)
    xx = np.linspace(0, 13.25, 300)

    fig = plt.figure(figsize=(2.25, 2.72))
    ax = fig.add_axes([0.24, 0.16, 0.68, 0.76])
    ax.set_xlim(0, 13.25)
    ax.set_ylim(0, 1.49)
    for gx in np.arange(0, 12.01, 2):
        ax.plot([gx, gx], [0, 1.49], 'k-', lw=0.55, zorder=1)
    for gy in np.arange(0.2, 1.41, 0.2):
        ax.plot([0, 13.25], [gy, gy], 'k-', lw=0.55, zorder=1)
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    ax.plot(xx, P(xx), 'k-', lw=1.4, zorder=3)
    ax.set_xticks(np.arange(0, 12.01, 2))
    ax.set_yticks(np.arange(0.2, 1.41, 0.2))
    ax.tick_params(labelsize=9, length=3, width=0.8)
    ax.set_xlabel(r'$R/10^8\ \mathrm{cm}$', fontsize=10, labelpad=2)
    ax.set_ylabel(r'$\dfrac{M}{\odot}$', fontsize=12, labelpad=2, rotation=90)
    save(fig, 51)


# ---------------------------------------------------------------- 图 52
def fig_52():
    pts = [(9.42, 0.76), (10.5, 0.755), (12, 0.725), (13, 0.70), (14, 0.655),
           (15, 0.615), (16, 0.565), (17, 0.52), (18, 0.475), (19, 0.43),
           (20, 0.385), (21, 0.345), (22, 0.305), (23, 0.27), (24, 0.24),
           (25, 0.213), (26, 0.19), (27, 0.168), (28, 0.148), (30, 0.118),
           (32, 0.098), (35.3, 0.075)]
    P = PchipInterpolator(*np.array(pts).T)
    xx = np.linspace(9.42, 35.3, 300)

    fig = plt.figure(figsize=(3.4, 2.35))
    ax = fig.add_axes([0.115, 0.20, 0.855, 0.72])
    ax.set_xlim(0, 35.3)
    ax.set_ylim(0, 0.80)
    for gx in np.arange(0, 32.01, 4):
        ax.plot([gx, gx], [0, 0.80], 'k-', lw=0.55, zorder=1)
    for gy in np.arange(0.2, 0.61, 0.2):
        ax.plot([0, 35.3], [gy, gy], 'k-', lw=0.55, zorder=1)
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    dash_line(ax, 0, 0.76, 9.42, 0.76, lw=0.8)
    dash_line(ax, 9.42, 0, 9.42, 0.76, lw=0.8)
    ax.plot(xx, P(xx), 'k-', lw=1.4, zorder=3)
    ax.set_xticks(np.arange(0, 32.01, 4))
    ax.set_yticks(np.arange(0.2, 0.61, 0.2))
    ax.tick_params(labelsize=9, length=3, width=0.8)
    ax.text(9.42, -0.075, r'$R_{\rm min}$', fontsize=9, ha='center', va='top')
    ax.text(-0.8, 0.775, r'$M_{\rm max}$', fontsize=9, ha='right', va='center',
            clip_on=False)
    ax.set_xlabel(r'$R/\mathrm{km}$', fontsize=10, labelpad=1)
    ax.set_ylabel(r'$\dfrac{M}{\odot}$', fontsize=12, labelpad=4, rotation=90)
    save(fig, 52)


# ---------------------------------------------------------------- 图 53
def fig_53():
    fig = plt.figure(figsize=(3.1, 4.4))
    ax = fig.add_axes([0.05, 0.02, 0.90, 0.96])
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(385, 725)
    ax.set_ylim(955, 420)   # 页面坐标（y 向下）

    # ---- alpha 平面（上）
    ax.plot([397, 703], [613, 613], 'k-', lw=0.9, zorder=2)   # 实轴
    up = [(414, 613), (416, 575), (420, 530), (430, 498),
          (446, 483), (464, 479), (480, 483),
          (492, 492), (499, 507), (501, 525), (501, 538),
          (498, 558), (491, 572), (479, 577), (469, 568),
          (471, 554), (482, 546), (495, 549),
          (502, 534), (512, 512), (524, 496), (538, 486),
          (552, 479), (566, 481), (578, 489),
          (587, 502), (592, 519), (593, 537),
          (590, 556), (583, 568), (571, 573), (561, 566),
          (562, 553), (571, 546), (583, 549),
          (592, 541), (604, 537), (618, 539),
          (634, 549), (650, 553), (664, 563), (674, 580), (681, 597), (688, 613)]
    lo = [(x, 1226 - y) for (x, y) in up]
    for pts in (up, lo):
        X, Y = param_spline(pts, 600)
        ax.plot(X, Y, 'k-', lw=1.3, zorder=3)
    # C' 上的箭头（上半支从 alpha_0 走向 0，下半支从 0 走向 alpha_0）
    arrow(ax, (429, 509), (423, 524))            # 左叶左翼: 向下
    arrow(ax, (505, 502), (496, 490))            # 左叶右翼: 向上
    arrow(ax, (594, 505), (585, 493))            # 右叶右翼: 向上
    arrow(ax, (667, 566), (657, 556))            # 右端爬升: 向上
    arrow(ax, (423, 703), (429, 717))            # 左下半支: 离开 0 向下
    arrow(ax, (499, 731), (510, 721))            # 左叶底部: 向右
    arrow(ax, (584, 731), (596, 721))            # 右叶底部: 向右
    arrow(ax, (658, 662), (670, 650))            # 右端爬升: 向右
    # 标记
    pt_circle(ax, 414, 613, 4.5, filled=True)
    ax.text(403, 634, '0', fontsize=10, ha='center')
    pt_circle(ax, 584, 613, 4, filled=False)
    ax.text(584, 640, r'$a$', fontsize=10, ha='center')
    ax.text(700, 640, r'$\alpha_0$', fontsize=10, ha='center')
    ax.text(468, 500, r"$C'$", fontsize=11, ha='center')
    ax.add_patch(Circle((637, 494), 16, fill=False, lw=0.9, zorder=4))
    ax.text(637, 494, r'$\alpha$', fontsize=11, ha='center', va='center')

    # ---- omega 平面（下）
    cx, cy, R = 559, 890, 141
    ax.plot([418, 700], [890, 890], 'k-', lw=1.2, zorder=2)   # 实轴
    t = np.linspace(0, np.pi, 120)
    ax.plot(cx + R * np.cos(t), cy - R * np.sin(t), 'k-', lw=1.2, zorder=2)
    ax.plot([cx, cx], [cy, cy - R], 'k-', lw=0.7, zorder=1)   # 细竖线(虚轴)
    arrow(ax, (465, 783), (452, 796))                          # 圆弧箭头(向左下)
    ax.text(505, 812, r'$C$', fontsize=11, ha='center')
    ax.text(438, 916, r'$-\infty$', fontsize=10, ha='center')
    ax.text(559, 916, '0', fontsize=10, ha='center')
    ax.text(676, 916, r'$+\infty$', fontsize=10, ha='center')
    ax.add_patch(Circle((697, 790), 16, fill=False, lw=0.9, zorder=4))
    ax.text(697, 790, r'$\omega$', fontsize=11, ha='center', va='center')
    save(fig, 53)


# ---------------------------------------------------------------- 图 54
def fig_54():
    fig = plt.figure(figsize=(2.9, 1.85))
    ax = fig.add_axes([0.03, 0.03, 0.94, 0.94])
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(716, 1028)
    ax.set_ylim(648, 434)   # 页面坐标（y 向下）

    cx, cy, R = 874, 596, 127.5
    t = np.linspace(0, np.pi, 120)
    ax.plot(cx + R * np.cos(t), cy - R * np.sin(t), 'k-', lw=1.2, zorder=2)
    ax.plot([cx, cx], [cy, cy - R], 'k-', lw=0.7, zorder=1)
    ax.plot([cx - R, cx - 17], [cy, cy], 'k-', lw=1.2, zorder=2)
    for cxb in (cx, cx + 67):
        tb = np.linspace(0, np.pi, 40)
        ax.plot(cxb + 17 * np.cos(tb), cy - 17 * np.sin(tb), 'k-', lw=1.2, zorder=2)
        ax.plot([cxb + 17, cxb + 50], [cy, cy], 'k-', lw=1.2, zorder=2)
    ax.plot([cx + 117, cx + R], [cy, cy], 'k-', lw=1.2, zorder=2)
    pt_circle(ax, cx, cy, 5, filled=True)
    pt_circle(ax, cx + 67, cy, 5, filled=True)
    arrow(ax, (826, cy), (850, cy))
    arrow(ax, (964, cy), (988, cy))
    ar, ar2 = 40, 141
    pr = (cx + R * np.cos(np.radians(ar2)), cy - R * np.sin(np.radians(ar2)))
    arrow(ax, (pr[0] + 6, pr[1] + 8), (pr[0] - 6, pr[1] - 8))
    pl = (cx + R * np.cos(np.radians(ar)), cy - R * np.sin(np.radians(ar)))
    arrow(ax, (pl[0] + 7, pl[1] - 9), (pl[0] - 6, pl[1] + 8))
    ax.text(749, 618, r'$-\infty$', fontsize=10, ha='center')
    ax.text(cx, 622, '0', fontsize=10, ha='center')
    ax.text(cx + 67, 626, r'$\omega_0$', fontsize=10, ha='center')
    ax.text(1002, 618, r'$+\infty$', fontsize=10, ha='center')
    ax.text(767, 496, r'$C$', fontsize=11, ha='center')
    ax.add_patch(Circle((996, 470), 16, fill=False, lw=0.9, zorder=4))
    ax.text(996, 470, r'$\omega$', fontsize=11, ha='center', va='center')
    save(fig, 54)


# ---------------------------------------------------------------- 图 55
def fig_55():
    fig = plt.figure(figsize=(2.9, 1.75))
    ax = fig.add_axes([0.05, 0.06, 0.90, 0.88])
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-0.98, 2.0)
    ax.set_ylim(-0.28, 1.02)

    phi = 131.0
    ph = np.radians(phi)
    A = np.array([0.0, 0.0])
    B = np.array([1.0, 0.0])
    Bp = A + np.array([np.cos(ph), np.sin(ph)])      # B' = A 绕轴转 phi
    Ap = B + np.array([-np.cos(ph), np.sin(ph)])     # A' = B 绕轴转 -phi（镜像对称）

    ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', lw=1.6, solid_capstyle='round')
    ax.plot([A[0], Bp[0]], [A[1], Bp[1]], 'k-', lw=1.6, solid_capstyle='round')
    ax.plot([B[0], Ap[0]], [B[1], Ap[1]], 'k-', lw=1.6, solid_capstyle='round')
    ax.plot([Bp[0], Ap[0]], [Bp[1], Ap[1]], 'k-', lw=0.8)
    dash_line(ax, A[0], A[1], A[0], Bp[1], lw=0.8)
    dash_line(ax, B[0], B[1], B[0], Bp[1], lw=0.8)
    draw_arc(ax, A[0], A[1], 0.235, 0, phi, lw=0.8)
    draw_arc(ax, B[0], B[1], 0.235, 180 - phi, 180, lw=0.8)
    ax.text(0.272, 0.150, r'$\varphi$', fontsize=11, ha='center')
    ax.text(0.728, 0.150, r'$\varphi$', fontsize=11, ha='center')
    for P in (A, B, Bp, Ap):
        pt_circle(ax, P[0], P[1], 0.028)
    ax.text(0.02, -0.13, r'$A$', fontsize=11, ha='center')
    ax.text(0.98, -0.13, r'$B$', fontsize=11, ha='center')
    ax.text(Bp[0] - 0.02, Bp[1] + 0.10, r"$B'$", fontsize=11, ha='right')
    ax.text(Ap[0] + 0.02, Ap[1] + 0.10, r"$A'$", fontsize=11, ha='left')
    ax.text(0.5, -0.09, r'$a$', fontsize=11, ha='center')
    ax.text(-0.40, 0.36, r'$a$', fontsize=11, ha='right')
    ax.text(0.79, 0.36, r'$a$', fontsize=11, ha='left')
    save(fig, 55)


# ---------------------------------------------------------------- 图 56 公用
LW = 1.0
DASH = (0, (4, 2.5))


def edges_of_box(O, e1, e2, e3):
    V = {}
    for i in (0, 1):
        for j in (0, 1):
            for k in (0, 1):
                V[(i, j, k)] = O + i * e1 + j * e2 + k * e3
    E = []
    for k in (0, 1):
        for (p, q) in [((0, 0, k), (1, 0, k)), ((1, 0, k), (1, 1, k)),
                       ((1, 1, k), (0, 1, k)), ((0, 1, k), (0, 0, k))]:
            E.append((V[p], V[q]))
    for (i, j) in [(0, 0), (1, 0), (1, 1), (0, 1)]:
        E.append((V[(i, j, 0)], V[(i, j, 1)]))
    return V, E


def plot_poly(ax, pts, lw=LW, ls='-', z=2):
    pts = np.asarray(pts)
    ax.plot(np.append(pts[:, 0], pts[0, 0]), np.append(pts[:, 1], pts[0, 1]),
            'k-', lw=lw, ls=ls, zorder=z)


def seg(ax, P, Q, lw=LW, ls='-', z=2):
    ax.plot([P[0], Q[0]], [P[1], Q[1]], 'k-', lw=lw, ls=ls, zorder=z)


def box_cell(ax, O, e1, e2, e3, circles=True, lw=LW, r=0.55):
    V, E = edges_of_box(np.asarray(O, float), np.asarray(e1, float),
                        np.asarray(e2, float), np.asarray(e3, float))
    for P, Q in E:
        seg(ax, P, Q, lw=lw)
    if circles:
        for P in V.values():
            pt_circle(ax, P[0], P[1], r, lw=0.9)
    return V


def face_diag_dashed(ax, V, keys, lw=0.7):
    a, b, c, d = (V[k] for k in keys)
    seg(ax, a, c, lw=lw, ls=DASH, z=1.5)
    seg(ax, b, d, lw=lw, ls=DASH, z=1.5)


def body_diagonals(ax, V, lw=0.7):
    for p, q in [((0, 0, 0), (1, 1, 1)), ((1, 0, 0), (0, 1, 1)),
                 ((0, 1, 0), (1, 0, 1)), ((0, 0, 1), (1, 1, 0))]:
        seg(ax, V[p], V[q], lw=lw, ls=DASH, z=1.5)


def label_at(ax, x, y, s, fs=10):
    ax.text(x, y, s, fontsize=fs, ha='center', va='center', zorder=6)


FACES6 = [[(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
          [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)],
          [(0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)],
          [(0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)],
          [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)],
          [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)]]


def cell_gamma(ax, O, s):
    """Γ_t: 三斜格子, 三个棱角与棱长标记."""
    O = np.asarray(O, float)
    a = s * np.array([-0.30, -0.62])
    b = s * np.array([0.95, 0.30])
    c = s * np.array([-0.22, 1.15])
    box_cell(ax, O, a, b, c, r=0.07 * s)
    A = lambda t, r: O + r * np.array([np.cos(np.radians(t)), np.sin(np.radians(t))])
    draw_arc(ax, O[0], O[1], 0.18 * s, 17.0, 100.0, lw=0.8)
    draw_arc(ax, O[0], O[1], 0.18 * s, 100.0, 241.5, lw=0.8)
    draw_arc(ax, O[0], O[1], 0.18 * s, 241.5, 377.0, lw=0.8)
    label_at(ax, *(A(58, 0.30 * s)), r'$\alpha$')
    label_at(ax, *(A(171, 0.30 * s)), r'$\beta$')
    label_at(ax, *(A(309, 0.30 * s)), r'$\gamma$')
    label_at(ax, *(O + 0.58 * c + s * np.array([-0.09, 0.02])), r'$c$')
    label_at(ax, *(O + 0.55 * b + s * np.array([0.02, 0.11])), r'$b$')
    label_at(ax, *(O + 0.60 * a + s * np.array([-0.11, 0.0])), r'$a$')


def cell_m(ax, O, s, centered=False):
    """Γ_m / Γ_m^b: 单斜（底面平行四边形, 棱 c 竖直）."""
    O = np.asarray(O, float)
    e1 = s * np.array([1.0, 0.0])
    e2 = s * np.array([0.43, 0.43])
    e3 = s * np.array([0.0, 1.95])
    V = box_cell(ax, O, e1, e2, e3, r=0.07 * s)
    if not centered:
        P = O + e2                       # 底面左后顶点
        draw_arc(ax, P[0], P[1], 0.21 * s, 225, 360, lw=0.8)
        label_at(ax, *(P + 0.34 * s * np.array([np.cos(np.radians(135)),
                                                np.sin(np.radians(135))])), r'$\beta$')
        label_at(ax, *(O + e2 + 0.5 * (-e2) + s * np.array([-0.10, 0.10])), r'$b$')
        label_at(ax, *(O + e1 + s * np.array([0.11, 0.10])), r'$a$')
        label_at(ax, *(O + s * np.array([0.62, 1.00])), r'$c$')
    else:
        for keys in (FACES6[0], FACES6[1]):
            face_diag_dashed(ax, V, keys)
        for P in (O + 0.5 * (e1 + e2), O + e3 + 0.5 * (e1 + e2)):
            pt_circle(ax, P[0], P[1], 0.07 * s)


def cell_o(ax, O, s, kind='plain'):
    """Γ_0 系列: kind = plain / base / body / face."""
    O = np.asarray(O, float)
    e1 = s * np.array([1.0, 0.0])
    e2 = s * np.array([0.34, 0.26])
    e3 = s * np.array([0.0, 1.85])
    V = box_cell(ax, O, e1, e2, e3, r=0.07 * s)
    if kind == 'plain':
        label_at(ax, *(O + e2 + 0.55 * e1 + s * np.array([0.0, 0.11])), r'$b$')
        label_at(ax, *(O + e1 + s * np.array([0.10, 0.12])), r'$a$')
        label_at(ax, *(O + s * np.array([0.14, 0.93])), r'$c$')
    elif kind == 'base':
        for keys in (FACES6[0], FACES6[1]):
            face_diag_dashed(ax, V, keys)
        for P in (O + 0.5 * (e1 + e2), O + e3 + 0.5 * (e1 + e2)):
            pt_circle(ax, P[0], P[1], 0.07 * s)
    elif kind == 'body':
        body_diagonals(ax, V)
        P = O + 0.5 * (e1 + e2 + e3)
        pt_circle(ax, P[0], P[1], 0.07 * s)
    elif kind == 'face':
        for keys in FACES6:
            face_diag_dashed(ax, V, keys)
        for keys in FACES6:
            P = sum(V[k] for k in keys) / 4.0
            pt_circle(ax, P[0], P[1], 0.07 * s)


def cell_h(ax, O, s):
    """Γ_h: 六角柱（正六边形底面在斜投影中纵向压扁, 同原书）."""
    O = np.asarray(O, float)
    R = 1.0 * s            # 六边形半宽
    H = 1.9 * s            # 棱柱高
    sq = 0.30              # 纵向压缩系数
    pts = [(1, 0), (0.5, sq), (-0.5, sq), (-1, 0), (-0.5, -sq), (0.5, -sq)]
    base = [O + R * np.array([a, b]) for (a, b) in pts]
    top = [P + np.array([0, H]) for P in base]
    plot_poly(ax, base, lw=LW)
    plot_poly(ax, top, lw=LW)
    for P, Q in zip(base, top):
        seg(ax, P, Q, lw=LW)
    C0, C1 = O, O + np.array([0, H])
    seg(ax, C0, C1, lw=0.7, ls=DASH, z=1.5)
    for P in base + top:
        pt_circle(ax, P[0], P[1], 0.07 * s)
    pt_circle(ax, C0[0], C0[1], 0.07 * s)
    pt_circle(ax, C1[0], C1[1], 0.07 * s)
    label_at(ax, O[0] + 0.55 * R, O[1] + 0.45 * H, r'$c$')
    label_at(ax, O[0] - 0.24 * R, O[1] - 0.60 * R, r'$a$')
    label_at(ax, O[0] + 0.78 * R, O[1] - 0.38 * R, r'$a$')


def cell_rh(ax, O, s):
    """Γ_rh: 菱面体（顶点朝上, 顶点处标 alpha）."""
    O = np.asarray(O, float)
    d1 = s * np.array([0.55, -0.72])
    d2 = s * np.array([-0.62, -0.55])
    d3 = s * np.array([-0.06, -0.98])
    box_cell(ax, O, d1, d2, d3, r=0.07 * s)
    a1 = np.degrees(np.arctan2(d1[1], d1[0]))
    a2 = np.degrees(np.arctan2(d2[1], d2[0]))
    draw_arc(ax, O[0], O[1], 0.24 * s, a2, a1, lw=0.8)
    label_at(ax, *(O + 0.40 * s * np.array([np.cos(np.radians(-96)),
                                            np.sin(np.radians(-96))])), r'$\alpha$')
    Vb = O + d1 + d2 + d3                     # 底部顶点
    label_at(ax, *(O + d2 + d3 + 0.5 * d1 + s * np.array([0.10, -0.02])), r'$a$')
    label_at(ax, *(O + d1 + d3 + 0.5 * d2 + s * np.array([0.10, 0.02])), r'$a$')
    label_at(ax, *(O + d1 + d2 + 0.5 * d3 + s * np.array([-0.11, 0.0])), r'$a$')


def cell_q(ax, O, s, body=False):
    """Γ_q / Γ_q^v: 四方柱."""
    O = np.asarray(O, float)
    e1 = s * np.array([0.72, 0.0])
    e2 = s * np.array([0.30, 0.24])
    e3 = s * np.array([0.0, 1.70])
    V = box_cell(ax, O, e1, e2, e3, r=0.07 * s)
    if not body:
        label_at(ax, *(O + e3 + 0.5 * e1 + s * np.array([0.0, 0.12])), r'$a$')
        label_at(ax, *(O + e2 + 0.55 * e1 + s * np.array([0.10, 0.08])), r'$a$')
        label_at(ax, *(O + s * np.array([0.20, 0.18])), r'$c$')
    else:
        body_diagonals(ax, V)
        P = O + 0.5 * (e1 + e2 + e3)
        pt_circle(ax, P[0], P[1], 0.07 * s)


def cell_c(ax, O, s, kind='plain'):
    """Γ_c / Γ_c^v / Γ_c^f: 立方."""
    O = np.asarray(O, float)
    e1 = s * np.array([0.88, 0.0])
    e2 = s * np.array([0.36, 0.28])
    e3 = s * np.array([0.0, 0.88])
    V = box_cell(ax, O, e1, e2, e3, r=0.07 * s)
    if kind == 'plain':
        label_at(ax, *(O + e3 + 0.5 * e1 + s * np.array([0.0, 0.12])), r'$a$')
        label_at(ax, *(O + e2 + e3 + 0.52 * e1 + s * np.array([0.10, 0.07])), r'$a$')
        label_at(ax, *(O + s * np.array([-0.13, 0.44])), r'$a$')
    elif kind == 'body':
        body_diagonals(ax, V)
        P = O + 0.5 * (e1 + e2 + e3)
        pt_circle(ax, P[0], P[1], 0.07 * s)
    elif kind == 'face':
        for keys in FACES6:
            face_diag_dashed(ax, V, keys)
        for keys in FACES6:
            P = sum(V[k] for k in keys) / 4.0
            pt_circle(ax, P[0], P[1], 0.07 * s)


def fig_56():
    fig = plt.figure(figsize=(4.13, 3.83))
    ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(0, 104)
    ax.set_ylim(0, 97)

    # 第一行（上）: Γ_t Γ_m Γ_m^b Γ_0 Γ_0^b，基线 y=70
    cell_gamma(ax, np.array([11.9, 70 + 0.62 * 14]), 14.0)
    lab56(ax, 13.4, 65.0, r'$\Gamma_t$')
    cell_m(ax, np.array([28.3, 70]), 11.0)
    lab56(ax, 36.2, 65.0, r'$\Gamma_m$')
    cell_m(ax, np.array([46.5, 70]), 11.0, centered=True)
    lab56(ax, 54.4, 65.0, r'$\Gamma_m^b$')
    cell_o(ax, np.array([64.7, 70]), 13.0, 'plain')
    lab56(ax, 73.4, 65.0, r'$\Gamma_0$')
    cell_o(ax, np.array([84.6, 70]), 13.0, 'base')
    lab56(ax, 93.3, 65.0, r'$\Gamma_0^b$')

    # 第二行（中）: Γ_0^v Γ_0^f Γ_h Γ_rh Γ_q，基线 y=36
    cell_o(ax, np.array([1.0, 36]), 13.0, 'body')
    lab56(ax, 9.7, 31.5, r'$\Gamma_0^v$')
    cell_o(ax, np.array([20.9, 36]), 13.0, 'face')
    lab56(ax, 29.6, 31.5, r'$\Gamma_0^f$')
    cell_h(ax, np.array([50.0, 36 + 0.30 * 9.5]), 9.5)
    lab56(ax, 50.0, 31.5, r'$\Gamma_h$')
    cell_rh(ax, np.array([67.8, 36 + 2.25 * 10]), 10.0)
    lab56(ax, 67.2, 31.5, r'$\Gamma_{rh}$')
    cell_q(ax, np.array([76.0, 36]), 12.0)
    lab56(ax, 82.1, 31.5, r'$\Gamma_q$')

    # 第三行（下）: Γ_q^v Γ_c Γ_c^v Γ_c^f，基线 y=9
    cell_q(ax, np.array([3.0, 9]), 12.0, body=True)
    lab56(ax, 8.6, 3.5, r'$\Gamma_q^v$')
    cell_c(ax, np.array([24.0, 9]), 17.0, 'plain')
    lab56(ax, 34.5, 3.5, r'$\Gamma_c$')
    cell_c(ax, np.array([50.0, 9]), 17.0, 'body')
    lab56(ax, 60.5, 3.5, r'$\Gamma_c^v$')
    cell_c(ax, np.array([76.0, 9]), 17.0, 'face')
    lab56(ax, 86.5, 3.5, r'$\Gamma_c^f$')
    save(fig, 56)


def lab56(ax, x, y, s):
    ax.text(x, y, s, fontsize=10, ha='center', va='center')


# ---------------------------------------------------------------- 图 57
def fig_57():
    fig = plt.figure(figsize=(3.0, 2.6))
    ax = fig.add_axes([0.04, 0.03, 0.92, 0.94])
    ax.set_aspect('equal')
    ax.axis('off')
    h = np.sqrt(3) / 2
    top = [(0, 1), (1, 1), (2, 1)]
    mid = [(-0.5, 0), (0.5, 0), (1.5, 0), (2.5, 0)]
    bot = [(0, -1), (1, -1), (2, -1)]
    ls = (0, (7, 2.5, 1, 2.5))

    def net(cy):
        for row in (top, mid, bot):
            for px, py in zip(row[:-1], row[1:]):
                ax.plot([px[0], py[0]], [cy + px[1] * h, cy + py[1] * h],
                        'k-', lw=0.8, ls=ls)
        for A in (top, bot):
            for P in A:
                for Q in mid:
                    if abs(P[0] - Q[0]) == 0.5:
                        ax.plot([P[0], Q[0]], [cy + P[1] * h, cy + Q[1] * h],
                                'k-', lw=0.8, ls=ls)

    def dots(cy):
        for P in top + mid + bot:
            pt_circle(ax, P[0], cy + P[1] * h, 0.062)

    def crosses(cy):
        for (cx0, cy0) in [(0, 1 / 3), (1, 1 / 3), (2, 1 / 3),
                           (0.5, -2 / 3), (1.5, -2 / 3)]:
            X, Y = cx0, cy + cy0 * h
            ax.plot([X - 0.075, X + 0.075], [Y - 0.075, Y + 0.075], 'k-', lw=1.0)
            ax.plot([X - 0.075, X + 0.075], [Y + 0.075, Y - 0.075], 'k-', lw=1.0)

    net(0)
    dots(0)
    ax.text(2.72, 0.42, r'$\Gamma_h$', fontsize=10, ha='left')
    net(-3.1)
    dots(-3.1)
    crosses(-3.1)
    ax.text(2.72, -3.1 + 0.26, r'$\Gamma_{rh}$', fontsize=10, ha='left')
    ax.set_xlim(-0.85, 3.35)
    ax.set_ylim(-4.6, 1.4)
    save(fig, 57)


# ---------------------------------------------------------------- 图 58
def fig_58():
    fig = plt.figure(figsize=(1.95, 2.15))
    ax = fig.add_axes([0.05, 0.03, 0.90, 0.94])
    ax.set_aspect('equal')
    ax.axis('off')
    d = np.array([0.62, 0.42])          # 进深方向（右上）
    c = np.array([0.0, 2.3])            # 竖直棱
    F = np.array([0.0, 0.0])            # 前下角
    corners = {(i, j, k): F + i * np.array([1, 0]) + j * d + k * c
               for i in (0, 1) for j in (0, 1) for k in (0, 1)}
    ls = (0, (5, 3))
    ctr_t = F + 0.5 * np.array([1, 0]) + 0.5 * d + c
    ctr_b = F + 0.5 * np.array([1, 0]) + 0.5 * d
    nbr_t, nbr_b = ctr_t + np.array([1, 0]), ctr_b + np.array([1, 0])
    seg(ax, ctr_t, corners[(1, 1, 1)], lw=0.9, ls=ls)
    seg(ax, ctr_t, corners[(1, 0, 1)], lw=0.9, ls=ls)
    seg(ax, nbr_t, corners[(1, 1, 1)], lw=0.9, ls=ls)
    seg(ax, nbr_t, corners[(1, 0, 1)], lw=0.9, ls=ls)
    seg(ax, ctr_b, corners[(1, 1, 0)], lw=0.9, ls=ls)
    seg(ax, ctr_b, corners[(1, 0, 0)], lw=0.9, ls=ls)
    seg(ax, nbr_b, corners[(1, 1, 0)], lw=0.9, ls=ls)
    seg(ax, nbr_b, corners[(1, 0, 0)], lw=0.9, ls=ls)
    seg(ax, ctr_t, ctr_b, lw=0.9, ls=ls)
    seg(ax, nbr_t, nbr_b, lw=0.9, ls=ls)
    # 棱（背面右竖棱省略）
    for (i, j) in [(0, 0), (1, 0), (0, 1)]:
        seg(ax, corners[(i, j, 0)], corners[(i, j, 1)], lw=1.2)
    for k in (0, 1):
        plot_poly(ax, [corners[(0, 0, k)], corners[(1, 0, k)],
                       corners[(1, 1, k)], corners[(0, 1, k)]], lw=1.2)
    for P in list(corners.values()) + [ctr_t, ctr_b, nbr_t, nbr_b]:
        pt_circle(ax, P[0], P[1], 0.055, filled=True, lw=0.6)
    ax.set_xlim(-0.18, 2.0)
    ax.set_ylim(-0.28, 2.95)
    save(fig, 58)


# ---------------------------------------------------------------- 图 59
def fig_59():
    fig = plt.figure(figsize=(3.5, 1.85))

    def make_proj():
        ux = np.array([1.0, 0.0])
        uy = np.array([0.28, 0.24])
        uz = np.array([0.0, 1.0])
        return lambda x, y, z: x * ux + y * uy + z * uz

    P3 = make_proj()

    def cube(ax):
        V = {(i, j, k): P3(i, j, k)
             for i in (0, 1) for j in (0, 1) for k in (0, 1)}
        ls = (0, (5, 3))
        for k in (0, 1):
            plot_poly(ax, [V[(0, 0, k)], V[(1, 0, k)], V[(1, 1, k)], V[(0, 1, k)]],
                      lw=0.9, ls=ls, z=1.5)
        for (i, j) in [(0, 0), (1, 0), (1, 1), (0, 1)]:
            seg(ax, V[(i, j, 0)], V[(i, j, 1)], lw=0.9, ls=ls, z=1.5)
        for P in V.values():
            pt_circle(ax, P[0], P[1], 0.037)
        return V

    # ---- 左: Γ_c^f 原胞
    ax = fig.add_axes([0.005, 0.02, 0.475, 0.95])
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-0.16, 1.48)
    ax.set_ylim(-0.10, 1.46)
    cube(ax)
    rh = [(0, 0, 0), (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5),
          (1, 0.5, 0.5), (0.5, 1, 0.5), (0.5, 0.5, 1), (1, 1, 1)]
    rp = {t: P3(*t) for t in rh}
    E = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 4), (2, 6), (3, 5),
         (3, 6), (4, 7), (5, 7), (6, 7)]
    for i, j in E:
        seg(ax, rp[rh[i]], rp[rh[j]], lw=1.3, z=3)
    for t in rh:
        pt_circle(ax, rp[t][0], rp[t][1], 0.037)
    for t in [(0.5, 0, 0), (0, 0.5, 0), (0, 0, 0.5),
              (1, 0.5, 0), (1, 0, 0.5), (0.5, 1, 0)]:
        Q = P3(*t)
        pt_circle(ax, Q[0], Q[1], 0.037)

    # ---- 右: Γ_c^v 原胞
    ax = fig.add_axes([0.52, 0.02, 0.475, 0.95])
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-0.16, 1.85)
    ax.set_ylim(-0.10, 1.85)
    cube(ax)
    On = P3(0, 0, 0)
    C = P3(0.5, 0.5, 0.5)      # 本胞体心
    D2 = P3(0.5, -0.5, 0.5)    # 前邻胞体心（画出：位于图下方）
    B4 = P3(1, 0, 1)
    B5 = P3(0, 1, 1)
    B6 = P3(0, 0, 1)
    BT = P3(0.5, 0.5, 1.5)     # 上邻胞体心
    A2 = P3(1, 0, 0)
    A12 = P3(1, 1, 0)
    TT = P3(1.5, 0.5, 0.5)     # 右邻胞体心
    K111 = P3(1, 1, 1)
    for P, Q in [(On, C), (On, D2),
                 (C, B4), (C, B5), (C, BT), (C, A12), (C, TT),
                 (D2, B4), (D2, B6), (D2, A2), (D2, TT),
                 (B6, BT), (B4, BT), (A12, BT), (K111, TT)]:
        seg(ax, P, Q, lw=1.3, z=3)
    for Q in [C, D2, BT, TT]:
        pt_circle(ax, Q[0], Q[1], 0.037)
    save(fig, 59)


if __name__ == '__main__':
    for f in (fig_50, fig_51, fig_52, fig_53, fig_54, fig_55,
              fig_56, fig_57, fig_58, fig_59):
        f()
        print(f.__name__, 'ok')
