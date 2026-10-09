# -*- coding: utf-8 -*-
"""
《时空与几何》(Carroll, Spacetime and Geometry) 第 8、9 章插图重绘
黑白教材风矢量图, matplotlib Agg 输出。
产物: figures/fig_8.1.pdf ... fig_9.3.pdf  (+ figures/preview/*.png 自检)
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Ellipse, Polygon, PathPatch, FancyArrowPatch
from matplotlib.path import Path

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

OUT = r'E:\AI整理书籍\卡罗尔\重排本\figures'
PREVIEW = os.path.join(OUT, 'preview')
os.makedirs(PREVIEW, exist_ok=True)


def _save(fig, key):
    fig.savefig(os.path.join(OUT, f'fig_{key}.pdf'),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREVIEW, f'fig_{key}.png'), dpi=200,
                bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


def _arrow(ax, xy_from, xy_to, lw=1.0, color='k', style='-|>', ms=9):
    ax.annotate('', xy=xy_to, xytext=xy_from,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def _smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- 图 8.1
def fig_8_1():
    fig, ax = plt.subplots(figsize=(3.1, 2.9))
    s = 1.0
    ax.plot([0, s], [s, s], 'k-', lw=1.2)            # 顶边 t'=+pi/2
    ax.plot([0, s], [-s, -s], 'k-', lw=1.2)          # 底边 t'=-pi/2
    ax.plot([0, 0], [-s, s], 'k--', lw=1.1)          # 左边 chi=0 (虚线)
    ax.plot([s, s], [-s, s], 'k--', lw=1.1)          # 右边 chi=pi (虚线)
    ax.plot([0, s], [-s, s], 'k-', lw=1.4)           # 类光对角线
    ax.plot([0, s], [s, -s], 'k-', lw=1.4)
    ax.text(-0.06, 1.03, r"$t'=\dfrac{\pi}{2}$", ha='right', va='center', fontsize=11)
    ax.text(-0.06, -1.03, r"$t'=-\dfrac{\pi}{2}$", ha='right', va='center', fontsize=11)
    ax.text(-0.44, 0.0, "de Sitter\nspace", ha='center', va='center', fontsize=11)
    ax.text(0.10, -1.38, r"$\chi=0$", ha='center', va='center')
    ax.text(0.90, -1.38, r"$\chi=\pi$", ha='center', va='center')
    ax.set_xlim(-1.38, 1.12)
    ax.set_ylim(-1.52, 1.20)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '8.1')


# ---------------------------------------------------------------- 图 8.2
def fig_8_2():
    fig, ax = plt.subplots(figsize=(3.0, 3.7))
    H, W = 1.9, 1.0
    y0, y1 = -0.52, 2.46
    # 边界: 左 chi=0 虚线, 右 chi=pi/2 实线(类时无限远)
    ax.plot([0, 0], [y0, y1], 'k--', lw=1.1)
    ax.plot([W, W], [y0, y1], 'k-', lw=1.2)
    A = (0.0, 0.0)          # t'=0
    B = (0.0, H)            # t'=pi  (类时测地线再聚焦点)
    C = (W, 0.95)           # 右边界上的转折点
    # 类光测地线(粗): A->C 与 B->C, 以及 A 向下的过去类光线
    ax.plot([A[0], C[0]], [A[1], C[1]], 'k-', lw=1.8)
    ax.plot([B[0], C[0]], [B[1], C[1]], 'k-', lw=1.8)
    ax.plot([A[0], 0.49], [A[1], -0.50], 'k-', lw=1.8)
    # 类光线(细): B 向右上的未来类光线
    ax.plot([B[0], 0.55], [B[1], 2.46], 'k-', lw=1.0)
    # 类时测地线(细): A 出发向右弯再聚焦于 B (两条)
    u = np.linspace(0.0, 1.0, 200)
    for a in (0.20, 0.45):
        ax.plot(a * np.sin(np.pi * u), H * u, 'k-', lw=1.0)
    # 类空测地线(细): 从 A 到右边界, 趋于平坦
    x = np.linspace(0.0, W, 200)
    for c in (0.31, -0.31):
        ax.plot(x, c * (2 * x - x * x), 'k-', lw=1.0)
    # 从 A 向下的类时测地线(细, 陡)
    ax.plot([A[0], 0.13], [A[1], -0.50], 'k-', lw=1.0)
    ax.text(-0.07, H, r"$t'=\pi$", ha='right', va='center')
    ax.text(-0.07, 0.0, r"$t'=0$", ha='right', va='center')
    ax.text(-0.62, 0.98, "anti\u2013de Sitter", ha='center', va='center')
    ax.text(0.02, -0.66, r"$\chi=0$", ha='center', va='center')
    ax.text(1.10, -0.66, r"$\chi=\dfrac{\pi}{2}$", ha='center', va='center')
    ax.set_xlim(-1.15, 1.28)
    ax.set_ylim(-0.82, 2.52)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '8.2')


# ---------------------------------------------------------------- 图 8.3
def fig_8_3():
    fig, ax = plt.subplots(figsize=(4.6, 2.9))

    def clip(x, a):
        m = (x >= -1.0) & (x <= 1.5) & (a >= 0.0) & (a <= 2.0)
        return x[m], a[m]

    # (Omega_M, Omega_Lambda) = (0.3, 0.7)
    y = np.linspace(1e-4, 2.18, 400)
    a1 = 0.7539 * np.sinh(y) ** (2.0 / 3.0)
    x1 = (y - 1.226) / 1.255
    # (0.3, 0.0) 开宇宙
    e = np.linspace(1e-4, 3.03, 400)
    a2 = (0.3 / 1.4) * (np.cosh(e) - 1.0)
    x2 = (0.3 / (2 * 0.7 ** 1.5)) * (np.sinh(e) - e) - 0.810
    # (1.0, 0.0) 平直物质宇宙
    x3 = np.linspace(-2.0 / 3.0, 1.5, 400)
    a3 = (1.5 * (x3 + 2.0 / 3.0)) ** (2.0 / 3.0)
    # (4.0, 0.0) 闭合宇宙, 会再坍缩
    n = np.linspace(1e-4, 4.237, 400)
    a4 = (4.0 / 6.0) * (1.0 - np.cos(n))
    x4 = (4.0 / (2 * 3 ** 1.5)) * (n - np.sin(n)) - 0.473

    for x, a in clip(x1, a1), clip(x2, a2), clip(x3, a3), clip(x4, a4):
        ax.plot(x, a, 'k-', lw=1.5)

    ax.set_xlim(-1, 1.5)
    ax.set_ylim(0, 2)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1, 1.5])
    ax.set_xticklabels(['-1', '-0.5', '0', '0.5', '1', '1.5'])
    ax.set_yticks([0, 0.5, 1, 1.5, 2])
    ax.set_yticklabels(['0', '.5', '1', '1.5', '2'])
    ax.tick_params(direction='in', top=True, right=True, labeltop=False,
                   labelright=False, length=4)
    ax.text(-1.30, 1.12, r"$a(t)$", ha='center', va='center')
    ax.text(0.25, -0.22, r"$H_0(t-t_0)$", ha='center', va='top')
    _save(fig, '8.3')


# ---------------------------------------------------------------- 图 8.4
def fig_8_4():
    fig, ax = plt.subplots(figsize=(3.7, 3.7))
    # Omega_total = 1 对角线
    ax.plot([0, 2], [1, -1], 'k-', lw=1.4)
    # 永久膨胀 / 再坍缩 分界线 (式 8.94)
    xm = np.linspace(1.0, 2.24, 300)
    ym = 4 * xm * np.cos(np.arccos(np.clip((1 - xm) / xm, -1, 1)) / 3
                         + 4 * np.pi / 3) ** 3
    ax.plot([0, 1.0], [0, 0], 'k-', lw=1.4)
    ax.plot(xm, ym, 'k-', lw=1.4)
    ax.plot([1.0], [0.0], 'ko', ms=4.5)
    # 观测值区域 (圆)
    ax.add_patch(Ellipse((0.32, 0.69), 0.48, 0.48, fill=False,
                         ec='k', lw=1.0))
    grey = '0.55'
    _arrow(ax, (0.64, 0.41), (0.80, 0.56), lw=1.2, color=grey, ms=11)
    _arrow(ax, (1.31, -0.32), (1.15, -0.48), lw=1.2, color=grey, ms=11)
    _arrow(ax, (1.685, 0.02), (1.685, 0.23), lw=1.2, color=grey, ms=11)
    _arrow(ax, (1.954, -0.01), (1.954, -0.23), lw=1.2, color=grey, ms=11)
    ax.text(1.05, 0.73, "positive\nspatial\ncurvature",
            ha='center', va='center', fontsize=10, linespacing=1.1)
    ax.text(0.95, -0.49, "negative\nspatial\ncurvature",
            ha='center', va='center', fontsize=10, linespacing=1.1)
    ax.text(1.685, 0.41, "expands\nforever", ha='center', va='center',
            fontsize=10, linespacing=1.1)
    ax.text(1.92, -0.33, "recollapses", ha='center', va='center', fontsize=10)
    ax.set_xlim(0, 2.24)
    ax.set_ylim(-1.0, 1.25)
    ax.set_xticks([0, 0.5, 1, 1.5, 2])
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax.tick_params(direction='in', top=True, right=True, labeltop=False,
                   labelright=False, length=4)
    ax.text(1.12, -1.24, r"$\Omega_{\rm M}$", ha='center', va='top')
    ax.text(-0.14, 0.17, r"$\Omega_\Lambda$", ha='right', va='center')
    _save(fig, '8.4')


# ---------------------------------------------------------------- 图 8.5
def fig_8_5():
    fig, ax = plt.subplots(figsize=(4.8, 2.9))
    img = (0.90, 4.75)      # Image 斑点
    src = (0.90, 3.55)      # Source 斑点
    L = (5.21, 3.27)        # 透镜处光线弯折点
    star = (5.27, 1.86)     # 透镜天体
    eye = (9.55, 1.76)      # 观测者
    ec = (9.15, 1.78)       # 眼睛左角(三条线的汇聚端)
    m_img = -0.36           # 表象方向(虚线 Image--L, 与出射线共线)
    ipL = (1.16, 4.73)      # Image 线在斑点右缘处
    m_src = -0.213
    spL = (1.18, 3.48)      # Source 线在斑点右缘处

    # 光线
    ax.plot([ipL[0], L[0]], [ipL[1], L[1]], 'k--', lw=1.1)          # 像方向(虚线)
    ax.plot([src[0], 1.18], [src[1], 3.57], 'k-', lw=1.1)           # 源->L (实线)
    ax.plot([1.18, L[0]], [3.57, L[1]], 'k-', lw=1.1)
    ax.plot([L[0], ec[0]], [L[1], ec[1]], 'k-', lw=1.1)             # L->观测者
    ax.plot([spL[0], ec[0]], [spL[1], ec[1]], 'k--', lw=1.1)        # 源方向(虚线)
    ax.plot([5.62, 9.10], [1.84, 1.77], 'k-', lw=0.8)               # 透镜->观测者(细)

    # 斑点 / 透镜星形 / 观测之眼
    for c in (img, src):
        ax.add_patch(Circle(c, 0.30, fc='0.88', ec='0.25', lw=0.8))
    pts = []
    n = 8
    for i in range(2 * n):
        r = 0.46 if i % 2 == 0 else 0.18
        th = np.pi / 2 + i * np.pi / n
        pts.append((star[0] + r * np.cos(th), star[1] + r * np.sin(th)))
    ax.add_patch(Polygon(pts, closed=True, fc='0.9', ec='0.3', lw=0.7))
    eye_path = Path([(9.06, 1.74), (9.30, 2.04), (9.80, 2.06), (10.12, 1.84),
                     (9.80, 1.44), (9.30, 1.44), (9.06, 1.74)],
                    [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4,
                     Path.CURVE4, Path.CURVE4, Path.CURVE4])
    ax.add_patch(PathPatch(eye_path, fc='white', ec='k', lw=0.9))
    ax.add_patch(Circle((9.46, 1.75), 0.20, fc='white', ec='k', lw=0.9))
    ax.add_patch(Circle((9.46, 1.75), 0.09, fc='k', ec='k'))

    # 角度弧线: 顶点、两侧目标点、半径
    def arc(v, p1, p2, r):
        a1 = np.degrees(np.arctan2(p1[1] - v[1], p1[0] - v[0]))
        a2 = np.degrees(np.arctan2(p2[1] - v[1], p2[0] - v[0]))
        ax.add_patch(Arc(v, 2 * r, 1.82 * r, theta1=min(a1, a2),
                         theta2=max(a1, a2), ec='k', lw=0.9))

    arc(L, ipL, (1.18, 3.57), 1.75)          # alpha_hat
    arc(ec, L, spL, 3.05)                    # alpha
    arc(ec, star, spL, 2.30)                 # beta
    arc(ec, star, ipL, 1.70)                 # theta
    ax.text(3.42, 3.88, r"$\hat{\alpha}$", ha='center', va='bottom')
    ax.text(6.11, 2.74, r"$\alpha$", ha='center', va='center')
    ax.text(6.81, 2.05, r"$\beta$", ha='center', va='center')
    ax.text(7.55, 1.93, r"$\theta$", ha='center', va='center')

    # 距离箭头
    ah = dict(arrowstyle='<|-|>', color='k', lw=1.0, mutation_scale=10,
              shrinkA=0, shrinkB=0)
    ax.annotate('', xy=(5.13, 1.13), xytext=(0.95, 1.13), arrowprops=ah)
    ax.annotate('', xy=(9.50, 1.13), xytext=(5.39, 1.13), arrowprops=ah)
    ax.annotate('', xy=(9.50, 0.67), xytext=(0.95, 0.67), arrowprops=ah)
    ax.text(3.05, 1.26, r"$d_{LS}$", ha='center', va='bottom')
    ax.text(7.40, 1.26, r"$d_{L}$", ha='center', va='bottom')
    ax.text(4.88, 0.80, r"$d_{S}$", ha='center', va='bottom')

    ax.text(0.88, 5.28, "Image", ha='center', va='bottom')
    ax.text(0.88, 3.00, "Source", ha='center', va='top')
    ax.text(4.42, 1.86, "Lens", ha='right', va='center')
    ax.text(9.35, 2.66, "Observer", ha='center', va='bottom')
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0.2, 5.6)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '8.5')


# ---------------------------------------------------------------- 图 8.6
def fig_8_6():
    fig, ax = plt.subplots(figsize=(2.7, 2.2))
    x0, x1, ya, yb = 0.14, 0.90, 0.16, 0.86   # 画布内绘图区
    _arrow(ax, (x0, 0.10), (x0, 0.90), lw=1.0)
    _arrow(ax, (0.06, ya), (0.95, ya), lw=1.0)
    ax.text(x0 + 0.03, 0.87, r"$V(\phi)$", ha='left', va='center', fontsize=12)
    ax.text(0.93, 0.06, r"$\phi$", ha='center', va='center', fontsize=12)

    # 势能曲线: 缓慢下降 -> 平坦 (慢滚区) -> 陡然下跌
    curve = Path([(0.19, 0.67),
                  (0.30, 0.65), (0.38, 0.615), (0.46, 0.585),
                  (0.53, 0.560), (0.58, 0.550), (0.64, 0.548),
                  (0.70, 0.547), (0.74, 0.50), (0.79, 0.43),
                  (0.83, 0.37), (0.85, 0.325), (0.87, 0.32)],
                 [Path.MOVETO,
                  Path.CURVE4, Path.CURVE4, Path.CURVE4,
                  Path.CURVE4, Path.CURVE4, Path.CURVE4,
                  Path.CURVE4, Path.CURVE4, Path.CURVE4,
                  Path.CURVE4, Path.CURVE4, Path.CURVE4])
    ax.add_patch(PathPatch(curve, fc='none', ec='k', lw=1.8,
                           capstyle='round'))
    ax.plot([0.459], [0.578], 'ko', ms=4.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    _save(fig, '8.6')


# ---------------------------------------------------------------- 图 8.7
def fig_8_7():
    fig, ax = plt.subplots(figsize=(3.8, 3.3))
    yb = 0.32          # x 轴高度
    # 坐标轴
    _arrow(ax, (0.68, yb), (0.68, 6.30), lw=0.9)
    _arrow(ax, (0.68, yb), (7.05, yb), lw=0.9)
    ax.text(0.86, 6.10, r"$t$", ha='left', va='center', fontsize=12)
    ax.text(6.98, 0.02, r"$x$", ha='center', va='center', fontsize=12)
    # CMB 虚线
    ax.plot([0.68, 6.68], [0.80, 0.80], 'k--', lw=1.0)
    ax.text(5.95, 1.02, "CMB", ha='center', va='bottom', fontsize=12)
    # 过去光锥大帐: 顶点 today, 两翼止于 CMB 线
    peak = (3.72, 5.45)
    for sgn in (1, -1):
        p1 = (peak[0] + sgn * 1.04, 3.95)
        p2 = (peak[0] + sgn * 1.68, 0.80)
        t = np.linspace(0, 1, 100)[:, None]
        pts = ((1 - t) ** 2 * np.array(peak) + 2 * (1 - t) * t * np.array(p1)
               + t ** 2 * np.array(p2))
        ax.plot(pts[:, 0], pts[:, 1], 'k-', lw=1.5)
    ax.text(4.37, 5.42, "today", ha='left', va='center', fontsize=12)
    # CMB 点各自的过去光锥 (四个到达 Big Bang 的小分支)
    for xa in (2.00, 5.40):
        for xe in (xa - 0.95, xa + 1.00):
            v = np.linspace(0, 1, 100)
            ax.plot(xa + (xe - xa) * v, yb + (0.80 - yb) * (1 - v) ** 2,
                    'k-', lw=1.5)
    ax.set_xlim(0.2, 7.3)
    ax.set_ylim(-0.35, 6.6)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '8.7')


# ---------------------------------------------------------------- 图 9.1
def fig_9_1():
    fig, ax = plt.subplots(figsize=(4.1, 3.4))
    # 细坐标轴
    _arrow(ax, (0, -2.10), (0, 2.42), lw=0.9)
    _arrow(ax, (-1.95, 0), (3.15, 0), lw=0.9)
    ax.text(0.10, 2.32, r"$t$", ha='left', va='center', fontsize=12)
    ax.text(3.08, -0.24, r"$x$", ha='center', va='center', fontsize=12)
    # Killing 视界 H^+- (粗对角线)
    ax.plot([-1.95, 2.08], [-1.95, 2.08], 'k-', lw=2.0)
    ax.plot([-1.95, 2.08], [1.95, -2.08], 'k-', lw=2.0)
    ax.text(2.22, 2.10, r"$H^+$", ha='left', va='center', fontsize=12)
    ax.text(2.22, -2.00, r"$H^-$", ha='left', va='center', fontsize=12)
    # 区 I 内: Rindler 坐标方向 (eta 提升方向, xi 转动方向)
    _arrow(ax, (0, 0), (1.90, 1.71), lw=1.0)
    _arrow(ax, (0, 0), (2.55, 1.16), lw=1.0)
    ax.text(2.02, 1.74, r"$\eta$", ha='left', va='center', fontsize=12)
    ax.text(2.67, 1.16, r"$\xi$", ha='left', va='center', fontsize=12)
    # 区 IV 内: 指向相反
    for d in ((-1.62, -1.41), (-1.78, -1.16), (-2.25, -1.00)):
        _arrow(ax, (0, 0), d, lw=1.0)
    # constant-xi 双曲线 (区 I 右开, 区 IV 左开)
    t = np.linspace(-2.05, 2.05, 400)
    for a in (0.95, 1.40):
        ax.plot(np.sqrt(a * a + t * t), t, 'k-', lw=0.9)
        ax.plot(-np.sqrt(a * a + t * t), t, 'k-', lw=0.9)
    # 区域标号
    ax.text(-0.17, 0.43, "II", ha='center', va='center', fontsize=12)
    ax.text(0.74, 0.18, "I", ha='center', va='center', fontsize=12)
    ax.text(-0.75, 0.18, "IV", ha='center', va='center', fontsize=12)
    ax.text(-0.17, -0.38, "III", ha='center', va='center', fontsize=12)
    ax.set_xlim(-2.55, 3.45)
    ax.set_ylim(-2.30, 2.60)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '9.1')


# ---------------------------------------------------------------- 图 9.2
def fig_9_2():
    fig, ax = plt.subplots(figsize=(3.5, 3.1))
    # 坐标轴
    _arrow(ax, (0, -0.75), (0, 3.49), lw=0.9)
    _arrow(ax, (0, 0), (4.76, 0), lw=0.9)
    ax.text(0.14, 3.42, r"$t$", ha='left', va='center', fontsize=12)
    ax.text(4.68, -0.28, r"$r$", ha='center', va='center', fontsize=12)
    # 视界 r = 2GM (虚线)
    ax.plot([1.56, 1.56], [-0.61, 3.20], 'k--', lw=1.0)
    ax.text(1.98, -0.78, r"$r=2GM$", ha='center', va='center', fontsize=12)
    # 真空涨落: 一支坠入黑洞, 一支逃逸
    verts = [(1.10, 2.94),
             (1.45, 2.59), (1.62, 2.28), (1.80, 2.06),
             (1.88, 1.97), (1.82, 1.90), (1.82, 1.76),
             (1.82, 1.50),
             (1.82, 1.36), (2.06, 1.36), (2.06, 1.50),
             (2.06, 1.76),
             (2.06, 1.90), (2.00, 1.97), (2.08, 2.06),
             (2.28, 2.30), (2.46, 2.52), (2.62, 2.70)]
    codes = [Path.MOVETO,
             Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.LINETO,
             Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.LINETO,
             Path.CURVE4, Path.CURVE4, Path.CURVE4,
             Path.CURVE4, Path.CURVE4, Path.CURVE4]
    ax.add_patch(PathPatch(Path(verts, codes), fc='none', ec='k', lw=1.6,
                           capstyle='round'))
    _arrow(ax, (1.16, 2.88), (1.03, 3.01), lw=1.6, ms=13)
    _arrow(ax, (2.56, 2.64), (2.69, 2.77), lw=1.6, ms=13)
    ax.text(0.98, 2.56, r"$e^+$", ha='right', va='center', fontsize=12)
    ax.text(2.82, 2.74, r"$e^-$", ha='left', va='center', fontsize=12)
    # 虚粒子对圈 (湮灭)
    leaf = Path([(2.71, 0.36),
                 (2.55, 0.72), (2.70, 1.02), (3.14, 1.07),
                 (3.05, 0.74), (2.93, 0.48), (2.71, 0.36)],
                [Path.MOVETO,
                 Path.CURVE4, Path.CURVE4, Path.CURVE4,
                 Path.CURVE4, Path.CURVE4, Path.CURVE4])
    ax.add_patch(PathPatch(leaf, fc='none', ec='k', lw=1.4))
    ax.text(2.50, 0.88, r"$e^-$", ha='right', va='center', fontsize=12)
    ax.text(3.24, 0.62, r"$e^+$", ha='left', va='center', fontsize=12)
    ax.set_xlim(-0.35, 5.0)
    ax.set_ylim(-1.0, 3.7)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '9.2')


# ---------------------------------------------------------------- 图 9.3
def fig_9_3():
    fig, ax = plt.subplots(figsize=(2.9, 3.7))
    im = (0.0, 0.0)        # i-
    i0 = (2.18, 2.15)      # i0
    ip = (1.01, 3.30)      # i+
    pL = (0.0, 2.29)       # 奇点左端 (坍缩发生)
    pR = (1.01, 2.29)      # 奇点右端 (蒸发完毕)
    # 边界
    ax.plot([im[0], pL[0]], [im[1], pL[1]], 'k-', lw=1.1)       # 下部 r=0
    ax.plot([pR[0], ip[0]], [pR[1], ip[1]], 'k-', lw=1.1)       # 上部 r=0
    ax.plot([im[0], i0[0]], [im[1], i0[1]], 'k-', lw=1.1)       # I-
    ax.plot([i0[0], ip[0]], [i0[1], ip[1]], 'k-', lw=1.1)       # I+
    # 奇点 r=0 (波浪线)
    xs = np.linspace(pL[0], pR[0], 400)
    ax.plot(xs, np.full_like(xs, pL[1]), 'k-', lw=0.8)
    ax.plot(xs, pL[1] - 0.062 * np.sin(2 * np.pi * (xs - pL[0]) / 0.2525),
            'k-', lw=1.1)
    # 事件视界 (虚线): 从蒸发结束事件回到 r=0
    ax.plot([pR[0], pL[0]], [pR[1], pR[1] - 1.01], 'k--', lw=1.0)
    # Hawking 辐射箭头
    _arrow(ax, (0.35, 1.43), (0.86, 1.87), lw=1.0, ms=10)
    _arrow(ax, (0.44, 1.32), (0.95, 1.76), lw=1.0, ms=10)
    ax.text(0.98, 1.94, "radiation", ha='left', va='center', fontsize=11)
    # 标注点
    for c in (im, i0, ip, pL, pR):
        ax.add_patch(Circle(c, 0.05, fc='k', ec='k'))
    ax.text(0.0, -0.16, r"$i^-$", ha='center', va='top', fontsize=12)
    ax.text(1.01, 3.44, r"$i^+$", ha='center', va='bottom', fontsize=12)
    ax.text(2.28, 2.15, r"$i^0$", ha='left', va='center', fontsize=12)
    ax.text(-0.10, 0.80, r"$r=0$", ha='right', va='center', fontsize=12)
    ax.text(0.55, 3.02, r"$r=0$", ha='center', va='center', fontsize=12)
    ax.text(0.24, 2.52, r"$r=0$", ha='center', va='bottom', fontsize=12)
    ax.text(1.38, 0.95, r"$\mathcal{I}^-$", ha='center', va='center', fontsize=12)
    ax.text(1.71, 3.06, r"$\mathcal{I}^+$", ha='center', va='center', fontsize=12)
    ax.set_xlim(-0.75, 2.55)
    ax.set_ylim(-0.55, 3.75)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, '9.3')


if __name__ == '__main__':
    for key, fn in sorted({f.__name__: f for f in
                           [fig_8_1, fig_8_2, fig_8_3, fig_8_4, fig_8_5,
                            fig_8_6, fig_8_7, fig_9_1, fig_9_2, fig_9_3]
                           }.items()):
        fn()
        print('done:', key)
