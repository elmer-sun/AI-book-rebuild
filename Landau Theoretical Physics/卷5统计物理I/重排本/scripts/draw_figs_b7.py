# -*- coding: utf-8 -*-
"""
朗道《统计物理学I》（卷5）中文重排本 插图重绘 第七批（末批）：图71-图80
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p-444..p-473，页码以 figures_manifest.md 哈希反查为准）。
  图71 -> p444；图72、73 -> p445；图74 -> p452；图75 -> p455；图76 -> p458；
  图77 -> p462；图78 -> p472；图79、80 -> p473。
内容：§151 二维晶格闭合图（71-73）、§152 临界点附近等温线（74）、
  §153 ηt 相图与不对称变形（75、76）、§155 台阶状晶面（77）、
  §160 μ'(γ) 润湿五型曲线（78）、§161 接触角与液滴透镜（79、80）。
排版宽度（ch14/ch15.tex）：71:10cm, 72:7cm, 73:7cm, 74:7.5cm, 75:8cm,
  76:6cm, 77:7cm, 78:11cm, 79:5.5cm, 80:5.5cm。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = r"E:\AI整理书籍\朗道理论物理教程\卷5统计物理I\重排本"
FIGD = os.path.join(BASE, 'figures')
PRED = os.path.join(FIGD, 'preview')
os.makedirs(PRED, exist_ok=True)

LW_MAIN, LW_AUX = 1.2, 0.8
DASH = (4.0, 2.2)          # 虚线（辅助/分子膜区）
DOTS_DASH = (1.2, 1.6)     # 点线（不稳定段）


def save(fig, n):
    fig.savefig(os.path.join(FIGD, f'fig{n}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRED, f'fig{n}.png'), bbox_inches='tight',
                pad_inches=0.03, dpi=220)
    plt.close(fig)


def plain_axes(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def arrow_axis(ax, x0, y0, x1, y1, lw=LW_MAIN, ms=11):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def catmull(pts, n=24):
    """Catmull-Rom 平滑曲线过点列。"""
    pts = np.asarray(pts, float)
    if len(pts) < 3:
        return pts
    p = np.vstack([pts[0], pts, pts[-1]])
    out = []
    for i in range(len(p) - 3):
        p0, p1, p2, p3 = p[i], p[i + 1], p[i + 2], p[i + 3]
        t = np.linspace(0, 1, n, endpoint=False)[:, None]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                          + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(pts[-1][None, :])
    return np.vstack(out)


def dots(ax, xs, ys, size=13):
    ax.scatter(xs, ys, s=size, c='k', zorder=3, linewidths=0)


# ---------------------------------------------------------------- 图 71
def fig_71():
    fig, ax = plt.subplots(figsize=(3.94, 1.55))
    plain_axes(ax)
    ax.set_aspect('equal')

    def grid(x0, nx, ny):
        xs, ys = [], []
        for i in range(nx):
            for j in range(ny):
                xs.append(x0 + i); ys.append(-j)
        dots(ax, xs, ys)

    def bond(p, q):
        ax.plot([p[0], q[0]], [p[1], q[1]], color='k', lw=1.5,
                solid_capstyle='round', zorder=2)

    def lab(x, y, s, ha='center'):
        ax.text(x, y, s, ha=ha, va='center', fontsize=7.5, zorder=4)

    # (a) 5×4 格点，两键折线
    grid(0, 5, 4)
    bond((1, 0), (2, 0)); bond((2, 0), (2, -1))
    lab(0.82, 0.28, '$k,l$', 'right')
    lab(2.28, 0.28, '$k{+}1,l$', 'left')
    lab(2.3, -1.34, '$k{+}1,l{-}1$', 'left')

    # (b) 5×5 格点，8 键闭合图，(k,l-1) 处自交
    grid(6.2, 5, 5)
    P = dict(kl=(7.2, -1), k1l=(8.2, -1), k1l1=(8.2, -2), kl1=(7.2, -2),
             k_1l1=(6.2, -2), k_1l2=(6.2, -3), kl2=(7.2, -3))
    for p, q in [('kl', 'k1l'), ('k1l', 'k1l1'), ('k1l1', 'kl1'), ('kl1', 'k_1l1'),
                 ('k_1l1', 'k_1l2'), ('k_1l2', 'kl2'), ('kl2', 'kl1'), ('kl1', 'kl')]:
        bond(P[p], P[q])
    lab(7.05, -0.72, '$k,l$')
    lab(8.42, -0.72, '$k{+}1,l$', 'left')
    lab(6.0, -1.62, '$k{-}1,l{-}1$', 'right')
    lab(7.04, -1.62, '$k,l{-}1$', 'right')
    lab(8.35, -2.36, '$k{+}1,l{-}1$', 'left')
    lab(6.35, -3.36, '$k{-}1,l{-}2$', 'right')
    lab(7.05, -3.36, '$k,l{-}2$', 'left')

    # (c) 7×6 格点，两圈图：方框 + 6 键圈
    grid(12.4, 7, 6)
    sq = [(16.4, -1), (17.4, -1), (17.4, -2), (16.4, -2), (16.4, -1)]
    for i in range(4):
        bond(sq[i], sq[i + 1])
    loop = [(15.4, -2), (14.4, -2), (14.4, -3), (14.4, -4), (15.4, -4),
            (15.4, -3), (15.4, -2)]
    for i in range(6):
        bond(loop[i], loop[i + 1])
    lab(16.22, -0.72, '$k,l$')
    lab(17.58, -0.72, '$k{+}1,l$')
    lab(14.55, -1.7, '$k{-}2,l{-}1$', 'right')
    lab(14.9, -1.7, '$k{-}1,l{-}1$', 'left')
    lab(16.08, -2.34, '$k,l{-}1$')
    lab(17.52, -2.34, '$k{+}1,l{-}1$')
    lab(14.1, -3.0, '$k{-}2,l{-}2$', 'right')
    lab(14.1, -4.0, '$k{-}2,l{-}3$', 'right')
    lab(15.72, -3.1, '$k{-}1,l{-}2$', 'left')
    lab(15.55, -4.36, '$k{-}1,l{-}3$')

    ax.text(2.0, -4.0, '(a)', ha='center', va='center', fontsize=9)
    ax.text(8.2, -4.95, '(b)', ha='center', va='center', fontsize=9)
    ax.text(15.4, -5.9, '(c)', ha='center', va='center', fontsize=9)
    ax.set_xlim(-0.65, 19.1)
    ax.set_ylim(-6.5, 0.85)
    save(fig, 71)


# ---------------------------------------------------------------- 图 72
def fig_72():
    fig, ax = plt.subplots(figsize=(2.76, 1.05))
    plain_axes(ax)
    ax.set_aspect('equal')
    lw = 1.4

    def curve(pts, **kw):
        c = catmull(pts)
        ax.plot(c[:, 0], c[:, 1], color='k', lw=lw, **kw)

    def seg(p, q):
        ax.plot([p[0], q[0]], [p[1], q[1]], color='k', lw=lw)

    # 面板 1：单一无自交圈，两方框经 S 形过渡相连（+）
    curve([(0.5, 1.0), (0.74, 1.0), (0.92, 1.05), (1.0, 1.18), (1.0, 1.35), (1.0, 1.52)])
    curve([(1.5, 1.0), (1.26, 1.0), (1.08, 0.95), (1.0, 0.82), (1.0, 0.65), (1.0, 0.48)])
    seg((0, 1), (0.5, 1)); seg((1, 1.52), (1, 2)); seg((1, 2), (2, 2)); seg((2, 2), (2, 1))
    seg((2, 1), (1.5, 1)); seg((1, 0.48), (1, 0)); seg((1, 0), (0, 0)); seg((0, 0), (0, 1))
    ax.text(1.0, -0.52, '$+$', ha='center', va='center', fontsize=11)

    # 面板 2：两个分离的圆角方圈（+）
    x0 = 3.0
    r = 0.36
    a = np.linspace(0, np.pi / 2, 20)
    arc = np.stack([1 - r + r * np.cos(a), 1 - r + r * np.sin(a)], 1)  # 圆角圆心(1-r,1-r)
    p1 = [(0, 1), (0, 0), (1, 0), (1, 1 - r)]
    p2 = np.vstack([p1, arc, [(1 - r, 1), (0, 1)]])
    ax.plot(p2[:, 0] + x0, p2[:, 1], color='k', lw=lw)
    a2 = np.linspace(-np.pi / 2, -np.pi, 20)
    arc_u = np.stack([1 + r + r * np.cos(a2), 1 + r + r * np.sin(a2)], 1)  # 圆心(1+r,1+r)
    q1 = [(1, 2), (2, 2), (2, 1), (1 + r, 1)]
    q2 = np.vstack([q1, arc_u, [(1, 1 + r), (1, 2)]])
    ax.plot(q2[:, 0] + x0, q2[:, 1], color='k', lw=lw)
    ax.text(x0 + 1.0, -0.52, '$+$', ha='center', va='center', fontsize=11)

    # 面板 3：单一自交圈，角点处 S 形扭动跨过公共棱（-）
    x0 = 6.0
    s = np.linspace(0, 1, 60)
    xw = 1 - 0.14 * np.sin(2 * np.pi * s)
    yw = 1.16 - 0.32 * s
    ax.plot(x0 + xw, yw, color='k', lw=lw)
    seg((x0 + 0, 1), (x0 + 2, 1))
    seg((x0 + 1, 1.16), (x0 + 1, 2)); seg((x0 + 1, 2), (x0 + 2, 2)); seg((x0 + 2, 2), (x0 + 2, 1))
    seg((x0 + 1, 0.84), (x0 + 1, 0)); seg((x0 + 1, 0), (x0 + 0, 0)); seg((x0 + 0, 0), (x0 + 0, 1))
    ax.text(x0 + 1.0, -0.52, '$-$', ha='center', va='center', fontsize=11)

    ax.set_xlim(-0.3, 8.3)
    ax.set_ylim(-0.85, 2.35)
    save(fig, 72)


# ---------------------------------------------------------------- 图 73
def fig_73():
    fig, ax = plt.subplots(figsize=(2.76, 1.55))
    plain_axes(ax)
    ax.set_aspect('equal')
    lw = 1.4
    w, h = 0.85, 0.9          # 半块高

    # (a) 共享中棱的双联方框
    x0 = 0.0
    ax.plot([x0, x0 + w, x0 + w, x0, x0], [0, 0, 2 * h, 2 * h, 0], color='k', lw=lw)
    ax.plot([x0, x0 + w], [h, h], color='k', lw=lw)
    ax.text(x0 + w / 2, -0.42, '(a)', ha='center', va='center', fontsize=9)

    # (b) 分离的两方框，+ 在上
    x0 = 1.75
    g = 0.2
    ax.plot([x0, x0 + w, x0 + w, x0, x0], [0, 0, h, h, 0], color='k', lw=lw)
    ax.plot([x0, x0 + w, x0 + w, x0, x0], [h + g, h + g, 2 * h + g, 2 * h + g, h + g],
            color='k', lw=lw)
    ax.text(x0 + w / 2, -0.42, '(b)', ha='center', va='center', fontsize=9)
    ax.text(x0 + w / 2, 2 * h + g + 0.28, '$+$', ha='center', va='center', fontsize=11)

    # (c) 中棱处自交（X 交叉）的双联圈，- 在上
    x0 = 3.5
    d = 0.15                  # 交叉区半高
    for xe in (x0, x0 + w):
        ax.plot([xe, xe], [0, h - d], color='k', lw=lw)
        ax.plot([xe, xe], [h + d, 2 * h], color='k', lw=lw)
    ax.plot([x0, x0 + w], [0, 0], color='k', lw=lw)
    ax.plot([x0, x0 + w], [2 * h, 2 * h], color='k', lw=lw)
    # 两条对角斜线在中心交叉
    ax.plot([x0, x0 + w], [h - d, h + d], color='k', lw=lw)
    ax.plot([x0 + w, x0], [h - d, h + d], color='k', lw=lw)
    ax.text(x0 + w / 2, -0.42, '(c)', ha='center', va='center', fontsize=9)
    ax.text(x0 + w / 2, 2 * h + 0.28, '$-$', ha='center', va='center', fontsize=11)

    ax.set_xlim(-0.35, 4.75)
    ax.set_ylim(-0.75, 2.55)
    save(fig, 73)


# ---------------------------------------------------------------- 图 74
def fig_74():
    fig, ax = plt.subplots(figsize=(2.95, 2.45))
    plain_axes(ax)

    # 轴
    ax.plot([0, 0], [-4.35, 2.25], color='k', lw=LW_MAIN)
    ax.plot([-2.1, 2.1], [0, 0], color='k', lw=LW_MAIN)
    ax.text(-0.13, 2.3, '$p$', ha='right', va='center', fontsize=10)
    ax.text(2.05, -0.32, r'$\eta$', ha='center', va='center', fontsize=10)

    # 临界等温线 t=0（拐点平贴 η 轴）
    e = np.linspace(-1.95, 1.95, 200)
    ax.plot(e, 0.105 * e ** 3, color='k', lw=LW_MAIN)

    # t<0 纯回路（亚稳/不稳段点线）
    f = 0.55 * e ** 3 - 1.35 * e
    m = np.abs(e) < 0.92
    ax.plot(e[~m], f[~m], color='k', lw=LW_MAIN)
    ax.plot(e[m], f[m], color='k', lw=LW_MAIN, ls=(0, DOTS_DASH))

    # t<0 带水平段 AD（Maxwell 构图）
    shift = -1.9
    g = f + shift
    ax.plot(e[e < -0.92], g[e < -0.92], color='k', lw=LW_MAIN)
    ax.plot(e[e > 0.92], g[e > 0.92], color='k', lw=LW_MAIN)
    ax.plot(e[m], g[m], color='k', lw=LW_MAIN, ls=(0, DOTS_DASH))
    eA = 1.342
    ax.plot([-eA, eA], [shift, shift], color='k', lw=LW_MAIN)

    # 竖直虚线（液气密度位置）
    for xd in (-eA, eA):
        ax.plot([xd, xd], [0, shift], color='k', lw=LW_AUX, ls=(0, DASH))
    ax.text(-1.72, -0.35, r'$\eta_2$', ha='center', va='center', fontsize=10)
    ax.text(1.56, 0.24, r'$\eta_1$', ha='left', va='center', fontsize=10)

    # 字母标注
    ax.text(eA + 0.09, shift - 0.12, '$A$', ha='left', va='center', fontsize=10)
    ax.text(-eA - 0.09, shift - 0.18, '$D$', ha='right', va='center', fontsize=10)
    ax.text(-0.92, -0.72, '$C$', ha='center', va='center', fontsize=10)
    ax.text(0.92, -2.95, '$B$', ha='center', va='center', fontsize=10)

    ax.set_xlim(-2.35, 2.45)
    ax.set_ylim(-4.5, 2.55)
    save(fig, 74)


# ---------------------------------------------------------------- 图 75
def fig_75():
    fig, ax = plt.subplots(figsize=(3.15, 2.0))
    plain_axes(ax)

    # 轴
    ax.plot([0, 0], [-1.62, 1.68], color='k', lw=LW_MAIN)
    ax.plot([-2.35, 2.45], [0, 0], color='k', lw=LW_MAIN)
    ax.text(0.1, 1.72, '$t$', ha='center', va='center', fontsize=10)
    ax.text(2.52, 0.02, r'$\eta$', ha='left', va='center', fontsize=10)

    # 共存曲线（立方型穹顶，t<0），内部水平阴影
    xe = np.linspace(-0.955, 0.955, 200)
    td = -0.92 * (np.abs(xe) / 0.955) ** 3
    for y in np.arange(-0.05, -0.80, -0.048):
        xw = 0.955 * (abs(y) / 0.92) ** (1 / 3)
        ax.plot([-xw, xw], [y, y], color='k', lw=0.7, zorder=1)
    ax.plot(xe, td, color='k', lw=LW_MAIN, zorder=2)

    # 虚线：|t| 与 |eta|^{1/beta} 的分界（立方型）
    def dash(c, e0, e1, sgn=+1):
        ee = np.linspace(e0, e1, 60)
        ax.plot(ee, sgn * c * np.abs(ee) ** 3, color='k', lw=LW_AUX, ls=(0, DASH))
    dash(0.50, -1.22, -0.10, +1)          # 左上 1 条
    dash(0.50, 0.10, 1.22, +1)            # 右上陡
    dash(0.175, 0.12, 1.18, +1)           # 右上缓（p=0 线上方）
    dash(0.50, -1.22, -0.10, -1)          # 左下陡
    dash(0.175, -1.18, -0.12, -1)         # 左下缓
    dash(0.50, 0.10, 1.22, -1)            # 右下陡
    dash(0.175, 0.12, 1.18, -1)           # 右下缓

    # 标注
    ax.text(-0.62, 0.86, r'$|t|\gg|\eta|^{1/\beta}$', ha='center', va='center', fontsize=9)
    ax.text(1.10, 0.14, r'$p=0$', ha='left', va='center', fontsize=9)
    ax.text(-1.7, -0.52, r'$|t|\ll|\eta|^{1/\beta}$', ha='center', va='center', fontsize=9)
    ax.text(1.74, -0.52, r'$|t|\ll|\eta|^{1/\beta}$', ha='center', va='center', fontsize=9)
    ax.text(-1.0, -1.06, r'$\eta_2\propto-|t|^{\beta}$', ha='center', va='center', fontsize=9)
    ax.text(1.02, -1.06, r'$\eta_1\propto|t|^{\beta}$', ha='center', va='center', fontsize=9)

    ax.set_xlim(-2.5, 2.75)
    ax.set_ylim(-1.3, 1.85)
    save(fig, 75)


# ---------------------------------------------------------------- 图 76
def fig_76():
    fig, ax = plt.subplots(figsize=(2.36, 1.95))
    plain_axes(ax)

    # 轴
    ax.plot([0, 0], [-1.08, 1.25], color='k', lw=LW_MAIN)
    ax.plot([-1.4, 1.45], [0, 0], color='k', lw=LW_MAIN)
    ax.text(0.09, 1.3, '$t$', ha='center', va='center', fontsize=10)
    ax.text(1.5, 0.03, r'$\eta$', ha='left', va='center', fontsize=10)

    # 变形穹顶（右支略宽），底部横线闭合，内部水平阴影
    yb = -0.81
    xL, xR = -0.62, 0.94
    for y in np.arange(-0.05, yb + 0.02, -0.045):
        r = (abs(y) / abs(yb)) ** (1 / 3)
        ax.plot([xL * r, xR * r], [y, y], color='k', lw=0.7, zorder=1)
    ee = np.linspace(-xL, -0.001, 80)
    ax.plot(-ee, yb * (ee / abs(xL)) ** 3, color='k', lw=LW_MAIN, zorder=2)
    ee = np.linspace(0.001, xR, 80)
    ax.plot(ee, yb * (ee / xR) ** 3, color='k', lw=LW_MAIN, zorder=2)
    ax.plot([xL, xR], [yb, yb], color='k', lw=LW_MAIN, zorder=2)

    # 直径线（连原点与 eta1+eta2）
    xd = 0.22
    ax.plot([0, xd], [0, yb], color='k', lw=LW_MAIN, zorder=3)

    ax.text(xL - 0.06, yb - 0.18, r'$\eta_2$', ha='center', va='center', fontsize=10)
    ax.text(0.38, yb - 0.18, r'$\eta_1{+}\eta_2$', ha='center', va='center', fontsize=9)
    ax.text(xR + 0.05, yb - 0.18, r'$\eta_1$', ha='center', va='center', fontsize=10)

    ax.set_xlim(-1.5, 1.75)
    ax.set_ylim(-1.15, 1.4)
    save(fig, 76)


# ---------------------------------------------------------------- 图 77
def fig_77():
    fig, ax = plt.subplots(figsize=(2.76, 0.92))
    plain_axes(ax)
    ax.set_aspect('equal')
    lw = 0.9

    # 台阶状正方网格：3+6+6+6 列，高 4,3,2,1
    hs = [4] * 3 + [3] * 6 + [2] * 6 + [1] * 6
    n = len(hs)
    for i, hgt in enumerate(hs):
        ax.plot([i, i], [0, hgt], color='k', lw=lw)
    ax.plot([n, n], [0, 1], color='k', lw=lw)
    ax.plot([0, n], [0, 0], color='k', lw=1.2)
    ax.plot([0, n], [1, 1], color='k', lw=lw)
    ax.plot([0, 15], [2, 2], color='k', lw=lw)
    ax.plot([0, 9], [3, 3], color='k', lw=lw)
    ax.plot([0, 3], [4, 4], color='k', lw=1.2)

    # 虚边线 (1n)：过各台阶凸角 (3,4),(9,3),(15,2),(21,1)
    xd = np.array([-0.9, 23.2])
    yd = 4 - (xd - 3) / 6.0
    ax.plot(xd, yd, color='k', lw=LW_AUX, ls=(0, (6, 3)))

    # phi 角：虚线与水平方向的夹角（画竖直小刻线连到下方台面）
    xt = 11.5
    yt = 4 - (xt - 3) / 6.0
    ax.plot([xt, xt], [2, yt], color='k', lw=LW_AUX)
    ax.text(10.7, 2.38, r'$\varphi$', ha='center', va='center', fontsize=10)

    # 晶格周期 a
    ax.plot([1, 1], [0, -0.62], color='k', lw=LW_AUX)
    ax.plot([2, 2], [0, -0.62], color='k', lw=LW_AUX)
    arrow_axis(ax, 0.3, -0.45, 1.0, -0.45, lw=LW_AUX, ms=8)
    arrow_axis(ax, 2.7, -0.45, 2.0, -0.45, lw=LW_AUX, ms=8)
    ax.text(1.72, -0.32, '$a$', ha='center', va='center', fontsize=10)

    ax.set_xlim(-1.15, 23.6)
    ax.set_ylim(-0.95, 4.55)
    save(fig, 77)


# ---------------------------------------------------------------- 图 78
def _panel78(ax, ox, oy):
    """一个面板的 mu'(gamma) 坐标架。"""
    arrow_axis(ax, ox, oy - 1.15, ox, oy + 1.18, lw=1.0, ms=8)
    arrow_axis(ax, ox, oy, ox + 1.78, oy, lw=1.0, ms=8)
    ax.text(ox - 0.08, oy + 1.26, r"$\mu'$", ha='right', va='center', fontsize=9)
    ax.text(ox + 1.86, oy, r'$\gamma$', ha='left', va='center', fontsize=9)


def _curve78(ax, ox, oy, pts_d, pts_s):
    """虚段 + 实段。"""
    if pts_d:
        c = catmull([(ox + x, oy + y) for x, y in pts_d])
        ax.plot(c[:, 0], c[:, 1], color='k', lw=LW_MAIN, ls=(0, DASH))
    c = catmull([(ox + x, oy + y) for x, y in pts_s])
    ax.plot(c[:, 0], c[:, 1], color='k', lw=LW_MAIN)


def fig_78():
    fig, ax = plt.subplots(figsize=(4.33, 2.85))
    plain_axes(ax)

    # (a) 单调下降（峰在分子区）
    ox, oy = 0.0, 0.0
    _panel78(ax, ox, oy)
    _curve78(ax, ox, oy,
             [(0.02, -1.1), (0.02, 0.1), (0.028, 0.5), (0.05, 0.8), (0.08, 0.93), (0.105, 0.975)],
             [(0.135, 1.0), (0.18, 0.93), (0.25, 0.78), (0.35, 0.6), (0.5, 0.42),
              (0.7, 0.27), (0.95, 0.16), (1.25, 0.1), (1.55, 0.07)])
    ax.text(ox + 0.9, -1.5, '(a)', ha='center', va='center', fontsize=9)

    # (b) 单调上升、处处为负
    ox, oy = 2.6, 0.0
    _panel78(ax, ox, oy)
    _curve78(ax, ox, oy,
             [(0.02, -1.1), (0.02, -0.75), (0.035, -0.85), (0.06, -0.68), (0.09, -0.55)],
             [(0.13, -0.45), (0.18, -0.37), (0.26, -0.28), (0.38, -0.21),
              (0.55, -0.15), (0.78, -0.1), (1.05, -0.065), (1.35, -0.04), (1.6, -0.03)])
    ax.text(ox + 0.9, -1.5, '(b)', ha='center', va='center', fontsize=9)

    # (c) 穿过零点且有极大值：A 零点，B 极大，C 其后
    ox, oy = 5.2, 0.0
    _panel78(ax, ox, oy)
    _curve78(ax, ox, oy,
             [(0.02, -1.1), (0.02, -0.35), (0.035, -0.75), (0.06, -0.45), (0.09, -0.25)],
             [(0.12, -0.12), (0.16, 0.04), (0.22, 0.2), (0.3, 0.36), (0.38, 0.45),
              (0.48, 0.44), (0.62, 0.38), (0.82, 0.31), (1.08, 0.26), (1.35, 0.235), (1.58, 0.225)])
    ax.text(ox + 0.22, oy + 0.05, '$A$', ha='left', va='center', fontsize=9)
    ax.text(ox + 0.38, oy + 0.56, '$B$', ha='center', va='center', fontsize=9)
    ax.text(ox + 0.78, oy + 0.41, '$C$', ha='center', va='center', fontsize=9)
    ax.text(ox + 0.9, oy - 1.5, '(c)', ha='center', va='center', fontsize=9)

    # (d) 一定厚度区不稳定：直线 BF 截等面积
    # A 上升分支 -> B(=虚线水平) -> 极大 C -> D(=虚线水平) -> 极小 E -> F(=虚线水平) -> G
    ox, oy = 1.3, -3.15
    _panel78(ax, ox, oy)
    yBF = -0.52
    _curve78(ax, ox, oy,
             [(0.02, -1.1), (0.02, -0.95), (0.045, -1.02), (0.075, -0.93)],
             [(0.105, -0.86), (0.15, -0.72), (0.2, -0.61), (0.26, yBF),
              (0.33, -0.42), (0.42, -0.33), (0.52, -0.28), (0.62, -0.31),
              (0.7, -0.38), (0.78, yBF), (0.86, -0.66), (0.94, -0.74),
              (1.04, -0.7), (1.12, -0.6), (1.22, yBF), (1.32, -0.42),
              (1.48, -0.33), (1.62, -0.29)])
    ax.plot([ox + 0.26, ox + 1.22], [oy + yBF, oy + yBF], color='k',
            lw=LW_AUX, ls=(0, DASH), zorder=1)
    ax.text(ox + 0.16, oy - 0.88, '$A$', ha='left', va='center', fontsize=9)
    ax.text(ox + 0.22, oy + yBF + 0.1, '$B$', ha='right', va='center', fontsize=9)
    ax.text(ox + 0.52, oy - 0.16, '$C$', ha='center', va='center', fontsize=9)
    ax.text(ox + 0.72, oy + yBF - 0.15, '$D$', ha='center', va='center', fontsize=9)
    ax.text(ox + 0.94, oy - 0.9, '$E$', ha='center', va='center', fontsize=9)
    ax.text(ox + 1.27, oy + yBF + 0.1, '$F$', ha='left', va='center', fontsize=9)
    ax.text(ox + 1.5, oy - 0.15, '$G$', ha='left', va='center', fontsize=9)
    ax.text(ox + 0.9, oy - 1.5, '(d)', ha='center', va='center', fontsize=9)

    # (e) 峰 + 谷后趋于平缓
    ox, oy = 4.15, -3.15
    _panel78(ax, ox, oy)
    _curve78(ax, ox, oy,
             [(0.02, -1.1), (0.02, 0.45), (0.03, 0.7), (0.05, 0.88), (0.075, 0.96)],
             [(0.1, 0.99), (0.14, 0.93), (0.2, 0.75), (0.28, 0.45), (0.36, 0.1),
              (0.45, -0.22), (0.55, -0.39), (0.66, -0.4), (0.8, -0.33),
              (1.0, -0.24), (1.25, -0.17), (1.5, -0.135), (1.6, -0.125)])
    ax.text(ox + 0.24, oy + 0.6, '$A$', ha='left', va='center', fontsize=9)
    ax.text(ox + 0.62, oy - 0.52, '$B$', ha='center', va='center', fontsize=9)
    ax.text(ox + 1.45, oy - 0.24, '$C$', ha='center', va='center', fontsize=9)
    ax.text(ox + 0.9, oy - 1.5, '(e)', ha='center', va='center', fontsize=9)

    ax.set_xlim(-0.55, 7.15)
    ax.set_ylim(-4.85, 1.55)
    save(fig, 78)


# ---------------------------------------------------------------- 图 79
def fig_79():
    fig, ax = plt.subplots(figsize=(2.17, 2.5))
    plain_axes(ax)
    ax.set_aspect('equal')

    # 固体表面（竖直线）
    ax.plot([0, 0], [-2.35, 2.5], color='k', lw=LW_MAIN)
    yc = 0.7  # 接触点

    # 液体表面（气液界面）
    pts = np.array([(0, yc), (0.28, 0.22), (0.6, -0.2), (1.0, -0.55),
                    (1.45, -0.85), (1.9, -1.05), (2.15, -1.15)])
    c = catmull(pts)
    ax.plot(c[:, 0], c[:, 1], color='k', lw=LW_MAIN)

    # 表面张力箭头
    arrow_axis(ax, 0, 1.2, 0, 1.8, lw=LW_MAIN, ms=10)
    ax.text(0.08, 1.72, r'$\alpha_{13}$', ha='left', va='center', fontsize=10)
    arrow_axis(ax, 0, -0.75, 0, -1.35, lw=LW_MAIN, ms=10)
    ax.text(0.08, -1.27, r'$\alpha_{12}$', ha='left', va='center', fontsize=10)
    arrow_axis(ax, 0.34, 0.1, 0.66, -0.42, lw=LW_MAIN, ms=10)
    ax.text(0.78, -0.56, r'$\alpha_{23}$', ha='left', va='center', fontsize=10)

    # 接触角 theta：竖直向下方向与界面切线之间
    from matplotlib.patches import Arc
    ax.add_patch(Arc((0, yc), 0.9, 0.9, theta1=270, theta2=300,
                     color='k', lw=LW_AUX))
    ax.text(0.1, 0.32, r'$\theta$', ha='left', va='center', fontsize=10)

    # 区域
    ax.text(-0.3, 0.45, '1', ha='right', va='center', fontsize=10)
    ax.text(1.2, 1.3, '3', ha='center', va='center', fontsize=10)
    ax.text(1.15, -1.6, '2', ha='center', va='center', fontsize=10)

    ax.set_xlim(-0.75, 2.35)
    ax.set_ylim(-2.45, 2.6)
    save(fig, 79)


# ---------------------------------------------------------------- 图 80
def fig_80():
    fig, ax = plt.subplots(figsize=(2.17, 1.9))
    plain_axes(ax)
    ax.set_aspect('equal')

    # 1-2 界面（左侧实线 + 左指箭头），右侧虚线（未扰动平面延长）
    ax.plot([-1.75, 0], [0, 0], color='k', lw=LW_MAIN)
    arrow_axis(ax, -0.62, 0, -1.1, 0, lw=LW_MAIN, ms=10)
    ax.text(-1.06, -0.26, r'$\alpha_{12}$', ha='center', va='center', fontsize=10)
    ax.plot([0, 2.1], [0, 0], color='k', lw=LW_AUX, ls=(0, DASH))
    ax.text(2.18, 0.02, '3', ha='left', va='center', fontsize=10)

    # 透镜两条界面线
    up = catmull([(0, 0), (0.3, 0.4), (0.62, 0.66), (1.0, 0.84), (1.4, 0.94), (1.72, 0.985)])
    dn = catmull([(0, 0), (0.3, -0.4), (0.62, -0.66), (1.0, -0.84), (1.4, -0.94), (1.72, -0.985)])
    ax.plot(up[:, 0], up[:, 1], color='k', lw=LW_MAIN)
    ax.plot(dn[:, 0], dn[:, 1], color='k', lw=LW_MAIN)

    # 三个表面张力箭头（沿各自界面、背离接触线）
    arrow_axis(ax, 0.04, 0.06, 1.02, 1.24, lw=LW_MAIN, ms=10)
    ax.text(1.12, 1.3, r'$\alpha_{23}$', ha='left', va='center', fontsize=10)
    arrow_axis(ax, 0.04, -0.06, 1.02, -1.24, lw=LW_MAIN, ms=10)
    ax.text(1.12, -1.4, r'$\alpha_{13}$', ha='left', va='center', fontsize=10)

    # 接触角 theta1、theta2（相对虚线水平面）
    from matplotlib.patches import Arc
    ax.add_patch(Arc((0, 0), 1.3, 1.3, theta1=8, theta2=51, color='k', lw=LW_AUX))
    ax.add_patch(Arc((0, 0), 1.3, 1.3, theta1=-51, theta2=-8, color='k', lw=LW_AUX))
    ax.text(0.86, 0.52, r'$\theta_2$', ha='left', va='center', fontsize=10)
    ax.text(0.86, -0.56, r'$\theta_1$', ha='left', va='center', fontsize=10)

    # 区域
    ax.text(-0.85, 0.55, '2', ha='center', va='center', fontsize=10)
    ax.text(-0.85, -1.0, '1', ha='center', va='center', fontsize=10)

    ax.set_xlim(-2.0, 2.5)
    ax.set_ylim(-1.65, 1.6)
    save(fig, 80)


if __name__ == '__main__':
    for f in (fig_71, fig_72, fig_73, fig_74, fig_75,
              fig_76, fig_77, fig_78, fig_79, fig_80):
        f()
        print(f.__name__, 'ok')
