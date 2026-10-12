# -*- coding: utf-8 -*-
"""
朗道《统计物理学I》（卷5）中文重排本 插图重绘 第四批：图36-图49
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p-276..p-281）。
  图36、37 -> p276；图38、39、40 -> p277；图41(a-g) -> p278；
  图42、43、44 -> p279；图45、46、47、48 -> p280；图49 -> p281。
内容：§98 相图举例后半（图36-40，T-x 相图）、§99 平衡曲面特征线相交
（图41，PT 投影示意 7 小图）、§100 气液（图42-49，PT 投影与 Px/Tx 截面）。
线型约定（图41-47）：点线=临界线，实线=纯物质线，虚线=等浓度线，点划线=三相线。
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
DASH_EQ = (4.5, 2.0)                 # 等浓度线（虚线）
DASHDOT_3P = (6.0, 2.0, 1.0, 2.0)    # 三相线（点划线）
DOT_CRIT = (0.8, 1.5)                # 临界线（点线）


def save(fig, n):
    fig.savefig(os.path.join(FIGD, f'fig{n}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRED, f'fig{n}.png'), bbox_inches='tight',
                pad_inches=0.03, dpi=220)
    plt.close(fig)


def plain_axes(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def arrow_axis(ax, x0, y0, x1, y1, lw=LW_MAIN):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=12))


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


def hatch_region(ax, loop, dy=0.045, lw=0.75):
    """闭合回路内画水平阴影线（不画边界线）。"""
    loop = np.asarray(loop, float)
    patch = plt.Polygon(loop, closed=True, facecolor='none',
                        edgecolor='none', zorder=1)
    ax.add_patch(patch)
    y0, y1 = loop[:, 1].min(), loop[:, 1].max()
    x0, x1 = loop[:, 0].min(), loop[:, 0].max()
    for y in np.arange(y0 + dy * 0.55, y1 - 1e-9, dy):
        (ln,) = ax.plot([x0 - 0.05, x1 + 0.05], [y, y], color='k', lw=lw,
                        zorder=0.9, solid_capstyle='butt')
        ln.set_clip_path(patch)
    return patch


def plot_curve(ax, pts, lw=LW_MAIN, dashes=None, z=2):
    pts = np.asarray(pts, float)
    if dashes is not None:
        ln, = ax.plot(pts[:, 0], pts[:, 1], color='k', lw=lw, zorder=z,
                      dashes=dashes)
    else:
        ln, = ax.plot(pts[:, 0], pts[:, 1], color='k', lw=lw, zorder=z)
    return ln


def tlabel(ax, x, y, s, fs=10, ha='center', va='center', rot=None, white=False):
    kw = {}
    if white:
        kw['bbox'] = dict(boxstyle='square', fc='white', ec='none', pad=0.12)
    if rot is not None:
        kw['rotation'] = rot
        kw['rotation_mode'] = 'anchor'
    ax.text(x, y, s, fontsize=fs, ha=ha, va=va, zorder=4, **kw)


def tx_frame(ax, H, right_top=None):
    """T-x 相图框：左右竖线 + 底线，T/x 标注。right_top: 右竖线顶端高度分数。"""
    ax.plot([0, 0], [0, H], 'k-', lw=1.1, zorder=2)
    h2 = H if right_top is None else H * (1 - right_top)
    ax.plot([1, 1], [0, h2], 'k-', lw=1.1, zorder=2)
    ax.plot([0, 1], [0, 0], 'k-', lw=1.1, zorder=2)
    ax.text(-0.05, H + 0.045, r'$T$', fontsize=11, ha='right', va='center')
    ax.text(0.965, -0.07, r'$x$', fontsize=11, ha='center', va='center')


def panel_frame(ax, ox, letter, pw, ph=1.0):
    """P-x / T-x 截面小图框（左、右竖线 + 底线），左上字母，右下 x。"""
    ax.plot([ox, ox], [0, -ph], 'k-', lw=1.0, zorder=2)
    ax.plot([ox + pw, ox + pw], [0, -ph], 'k-', lw=1.0, zorder=2)
    ax.plot([ox, ox + pw], [0, 0], 'k-', lw=1.0, zorder=2)
    ax.text(ox - 0.07 * pw, 0.0, rf'${letter}$', fontsize=10.5,
            ha='right', va='center')
    ax.text(ox + pw, -ph - 0.065, r'$x$', fontsize=10.5, ha='center',
            va='center')


def panel_cap(ax, ox, pw, s, ph=1.0):
    ax.text(ox + pw / 2, -ph - 0.21, s, fontsize=10, ha='center', va='center')


# ---------------------------------------------------------------- 图36
def fig_36():
    """§98 图36：液态无限互溶、固态有限互溶 T-x 相图（液线 ADC、固线 ABF/CEG、三相线 DBE）"""
    H = 1.05
    fig, ax = plt.subplots(figsize=(2.7, 2.65))
    plain_axes(ax)
    ax.set_xlim(-0.15, 1.13)
    ax.set_ylim(-0.125, H + 0.09)

    def Y(v):
        return H * (1 - v)

    tx_frame(ax, H)

    A = (0.0, Y(0.72)); D = (0.42, Y(0.55)); C = (1.0, Y(0.19))
    B = (0.585, Y(0.55)); E = (0.72, Y(0.55))
    F = (0.615, 0.0); G = (0.83, 0.0)

    liq1 = catmull([A, (0.10, Y(0.685)), (0.22, Y(0.645)),
                    (0.33, Y(0.60)), D])                       # 液线 A-D
    liq2 = catmull([D, (0.55, Y(0.475)), (0.68, Y(0.40)),
                    (0.82, Y(0.315)), (0.93, Y(0.245)), C])    # 液线 D-C
    sol1 = catmull([A, (0.13, Y(0.674)), (0.27, Y(0.624)),
                    (0.41, Y(0.585)), (0.50, Y(0.568)), B])    # 固线 A-B
    sol2 = catmull([B, (0.592, Y(0.70)), (0.602, Y(0.85)), F])  # 固线 B-F
    sol3 = catmull([C, (0.92, Y(0.27)), (0.83, Y(0.36)),
                    (0.76, Y(0.45)), E])                       # 固线 C-E
    sol4 = catmull([E, (0.735, Y(0.70)), (0.765, Y(0.85)), G])  # 固线 E-G

    # 整块阴影（液+固与固+固连通，三相线处不描线）
    loop = np.vstack([liq1, liq2[1:], sol3[1:], sol4[1:],
                      np.array([[1.0, 0.0]]), np.array([[F[0], 0.0]]),
                      sol2[::-1][1:], sol1[::-1][1:]])
    hatch_region(ax, loop, dy=0.044)

    for c in (liq1, liq2, sol1, sol2, sol3, sol4):
        plot_curve(ax, c)

    tlabel(ax, -0.05, Y(0.72) - 0.005, r'$A$', ha='right')
    tlabel(ax, 0.365, Y(0.475), r'$D$')
    tlabel(ax, 0.535, Y(0.655), r'$B$', white=True)
    tlabel(ax, 0.79, Y(0.515), r'$E$')
    tlabel(ax, 1.045, Y(0.185), r'$C$', ha='left')
    tlabel(ax, 0.615, -0.065, r'$F$')
    tlabel(ax, 0.845, -0.065, r'$G$')
    save(fig, 36)


# ---------------------------------------------------------------- 图37
def fig_37():
    """§98 图37：固态完全不互溶、低共熔型 T-x 相图（液线 DBE，共晶点 B）"""
    H = 1.08
    fig, ax = plt.subplots(figsize=(2.55, 2.6))
    plain_axes(ax)
    ax.set_xlim(-0.15, 1.13)
    ax.set_ylim(-0.125, H + 0.09)

    def Y(v):
        return H * (1 - v)

    tx_frame(ax, H, right_top=0.385)   # 右竖线只到 E

    Dp = (0.0, Y(0.47)); Bp = (0.50, Y(0.70)); Ep = (1.0, Y(0.385))
    curve = catmull([Dp, (0.20, Y(0.555)), (0.38, Y(0.655)), Bp,
                     (0.68, Y(0.60)), (0.85, Y(0.475)), Ep])

    loop = np.vstack([np.array([[0.0, Y(0.47)]]), curve[1:],
                      np.array([[1.0, 0.0]]), np.array([[0.0, 0.0]])])
    hatch_region(ax, loop, dy=0.047)
    plot_curve(ax, curve)

    tlabel(ax, -0.05, Y(0.47), r'$D$', ha='right')
    tlabel(ax, -0.05, Y(0.72), r'$A$', ha='right')
    tlabel(ax, 0.525, Y(0.775), r'$B$', white=True)
    tlabel(ax, 1.045, Y(0.72), r'$C$', ha='left')
    tlabel(ax, 1.045, Y(0.375), r'$E$', ha='left')
    save(fig, 37)


# ---------------------------------------------------------------- 图38
def fig_38():
    """§98 图38：形成固定化合物的 T-x 相图（化合物成分线 DE，两个三相点 B、G）"""
    fig, ax = plt.subplots(figsize=(2.5, 2.35))
    plain_axes(ax)
    ax.set_xlim(-0.15, 1.13)
    ax.set_ylim(-0.125, 1.09)
    H = 1.0

    def Y(v):
        return H * (1 - v)

    tx_frame(ax, H)

    A = (0.0, Y(0.44)); Bv = (0.315, Y(0.84)); Dp = (0.60, Y(0.30))
    Vk = (0.79, Y(0.545)); Rk = (1.0, Y(0.22))

    c1 = catmull([A, (0.15, Y(0.645)), (0.24, Y(0.775)), Bv])
    c2 = catmull([Bv, (0.345, Y(0.60)), (0.42, Y(0.43)), (0.52, Y(0.345)), Dp])
    c3 = catmull([Dp, (0.68, Y(0.375)), (0.74, Y(0.475)), Vk])
    c4 = catmull([Vk, (0.87, Y(0.36)), (0.95, Y(0.27)), Rk])

    loop = np.vstack([np.array([[0.0, Y(0.44)]]), c1[1:], c2[1:], c3[1:],
                      c4[1:], np.array([[1.0, 0.0]]), np.array([[0.0, 0.0]])])
    hatch_region(ax, loop, dy=0.043)
    for c in (c1, c2, c3, c4):
        plot_curve(ax, c)
    # 化合物等浓度竖线 D->E（至底线）
    ax.plot([Dp[0], Dp[0]], [Dp[1], 0.0], 'k-', lw=LW_MAIN, zorder=2)

    tlabel(ax, -0.05, Y(0.44), r'$A$', ha='right')
    tlabel(ax, -0.05, Y(0.79), r'$C$', ha='right')
    tlabel(ax, 0.585, Y(0.225), r'$D$')
    tlabel(ax, 0.295, Y(0.915), r'$B$', white=True)
    tlabel(ax, 0.53, Y(0.78), r'$E$', white=True)
    tlabel(ax, 0.645, Y(0.665), r'$G$', white=True)
    save(fig, 38)


# ---------------------------------------------------------------- 图39
def fig_39():
    """§98 图39：液相分层型（三相点 A 与等浓度点，图30 型）T-x 相图"""
    fig, ax = plt.subplots(figsize=(2.5, 2.5))
    plain_axes(ax)
    ax.set_xlim(-0.15, 1.13)
    ax.set_ylim(-0.125, 1.09)
    H = 1.0

    def Y(v):
        return H * (1 - v)

    tx_frame(ax, H)

    S0 = (0.0, Y(0.30)); Ak = (0.30, Y(0.50)); Vk = (0.60, Y(0.73))
    Rk = (1.0, Y(0.30))
    c1 = catmull([S0, (0.10, Y(0.365)), (0.20, Y(0.435)), Ak])   # 折点前陡
    c2 = catmull([Ak, (0.42, Y(0.60)), (0.52, Y(0.69)), Vk])     # 折点后缓
    c3 = catmull([Vk, (0.72, Y(0.585)), (0.85, Y(0.42)),
                  (0.94, Y(0.345)), Rk])

    loop = np.vstack([np.array([[0.0, Y(0.30)]]), c1[1:], c2[1:], c3[1:],
                      np.array([[1.0, 0.0]]), np.array([[0.0, 0.0]])])
    hatch_region(ax, loop, dy=0.043)
    for c in (c1, c2, c3):
        plot_curve(ax, c)
    # 三相水平线（穿过 A 标注，留缺口）
    yA = Y(0.50)
    ax.plot([0.0, 0.115], [yA, yA], 'k-', lw=LW_MAIN, zorder=2)
    ax.plot([0.245, Ak[0]], [yA, yA], 'k-', lw=LW_MAIN, zorder=2)
    # 等浓度竖线
    ax.plot([Ak[0], Ak[0]], [yA, 0.0], 'k-', lw=LW_MAIN, zorder=2)
    tlabel(ax, 0.178, yA, r'$A$')
    save(fig, 39)


# ---------------------------------------------------------------- 图40
def fig_40():
    """§98 图40：两液相分层 + 两个三相点 B、D 的 T-x 相图（曲线 ABC、DE、直线 CD）"""
    fig, ax = plt.subplots(figsize=(2.5, 2.52))
    plain_axes(ax)
    ax.set_xlim(-0.15, 1.15)
    ax.set_ylim(-0.125, 1.10)
    H = 1.01

    def Y(v):
        return H * (1 - v)

    ax.plot([0, 0], [0, H], 'k-', lw=1.1, zorder=2)
    ax.plot([1, 1], [0, Y(0.245)], 'k-', lw=1.1, zorder=2)   # 右竖线到 E
    ax.plot([0, 1], [0, 0], 'k-', lw=1.1, zorder=2)
    ax.text(-0.05, H + 0.045, r'$T$', fontsize=11, ha='right', va='center')
    ax.text(0.955, -0.07, r'$x$', fontsize=11, ha='center', va='center')

    A = (0.0, Y(0.545)); Bv = (0.255, Y(0.665)); Ck = (0.55, Y(0.40))
    Dk = (0.79, Y(0.40)); Ek = (1.0, Y(0.245)); Fk = (1.0, Y(0.40))

    cAB = catmull([A, (0.10, Y(0.585)), (0.19, Y(0.64)), Bv])
    cBC = catmull([Bv, (0.33, Y(0.555)), (0.45, Y(0.455)), Ck])
    domeL = catmull([(0.425, H), (0.435, Y(0.09)),
                     (0.47, Y(0.245)), Ck])            # 穹顶左臂（上->C）
    domeR = catmull([Dk, (0.783, Y(0.21)),
                     (0.772, Y(0.08)), (0.768, H)])    # 穹顶右臂（D->上）
    cDE = catmull([Dk, (0.90, Y(0.30)), (0.96, Y(0.262)), Ek])

    # 阴影：穹顶（CD 线以上两液相区）、三角 DEF、下方大区域
    dome = np.vstack([domeL, np.array([[Dk[0], Dk[1]]]), domeR[1:]])
    hatch_region(ax, dome, dy=0.043)
    tri = np.vstack([np.array([[Dk[0], Dk[1]]]), cDE[1:],
                     np.array([[Fk[0], Fk[1]]])])
    hatch_region(ax, tri, dy=0.043)
    low = np.vstack([np.array([[0.0, Y(0.545)]]), cAB[1:], cBC[1:],
                     np.array([[Fk[0], Fk[1]]]),
                     np.array([[1.0, 0.0]]), np.array([[0.0, 0.0]])])
    hatch_region(ax, low, dy=0.043)

    for c in (cAB, cBC, domeL, domeR, cDE):
        plot_curve(ax, c)
    ax.plot([Ck[0], 1.0], [Ck[1], Ck[1]], 'k-', lw=LW_MAIN, zorder=2)  # C-D-F

    tlabel(ax, -0.05, Y(0.545), r'$A$', ha='right')
    tlabel(ax, -0.05, Y(0.715), r'$H$', ha='right')
    tlabel(ax, 0.245, Y(0.585), r'$B$', white=True)
    tlabel(ax, 0.452, Y(0.375), r'$C$', ha='right')
    tlabel(ax, 0.80, Y(0.265), r'$D$')
    tlabel(ax, 1.045, Y(0.245), r'$E$', ha='left')
    tlabel(ax, 1.045, Y(0.40), r'$F$', ha='left')
    tlabel(ax, 1.045, Y(0.715), r'$G$', ha='left')
    save(fig, 40)


# ---------------------------------------------------------------- 图41
def fig_41():
    """§99 图41：平衡曲面特征曲线的相交 (a)-(g)，PT 投影示意"""
    fig, ax = plt.subplots(figsize=(3.95, 2.28))
    plain_axes(ax)
    ax.set_xlim(0, 15.3)
    ax.set_ylim(0.2, 8.95)
    PW, PH = 3.3, 3.5
    DOT = dict(dashes=DOT_CRIT, lw=1.15)
    DASH = dict(dashes=DASH_EQ, lw=1.0)
    DASHDOT = dict(dashes=DASHDOT_3P, lw=1.0)

    def mk(cx, cy):
        def T(u, v):
            return (cx + (u - 0.5) * PW, cy - (v - 0.5) * PH)
        return T

    def tag(cx, cy, s):
        ax.text(cx, cy - PH / 2 - 0.38, '(%s)' % s, fontsize=10.5,
                ha='center', va='center')

    def P(ax, pts, **kw):
        plot_curve(ax, np.asarray(pts, float), **kw)

    # ---------------- 第一行 (a)(b)(c)(d)
    T = mk(1.95, 6.4); tag(1.95, 6.4, 'a')
    P(ax, [T(u, v) for u, v in catmull([(0.05, 0.10), (0.30, 0.33),
                                        (0.50, 0.48), (0.63, 0.55)])], **DOT)
    P(ax, [T(u, v) for u, v in catmull([(0.63, 0.55), (0.42, 0.72),
                                        (0.22, 0.86), (0.04, 0.96)])])
    tlabel(ax, *T(0.22, 0.02), r'$ab$')
    tlabel(ax, *T(0.28, 0.52), r'$a$-$b$')
    tlabel(ax, *T(0.42, 0.83), r'$b$')

    T = mk(5.6, 6.4); tag(5.6, 6.4, 'b')
    P(ax, [T(u, v) for u, v in catmull([(0.05, 0.26), (0.32, 0.40),
                                        (0.55, 0.50), (0.76, 0.55)])], **DOT)
    P(ax, [T(u, v) for u, v in catmull([(0.02, 0.97), (0.30, 0.82),
                                        (0.55, 0.66), (0.76, 0.55)])],
      dashes=(4.0, 1.4), lw=1.0)
    tlabel(ax, *T(0.28, 0.13), r'$ab$-$c$')
    tlabel(ax, *T(0.44, 0.575), r'$a$-$b$-$c$')
    tlabel(ax, *T(0.54, 0.79), r'$a$-$c$')

    T = mk(9.45, 6.4); tag(9.45, 6.4, 'c')
    P(ax, [T(u, v) for u, v in catmull([(0.04, 0.80), (0.24, 0.655),
                                        (0.45, 0.605), (0.66, 0.635),
                                        (0.82, 0.705)])])
    P(ax, [T(u, v) for u, v in catmull([(0.20, 0.07), (0.34, 0.32),
                                        (0.45, 0.52), (0.505, 0.645)])],
      **DASH)
    tlabel(ax, *T(0.36, 0.20), r'$ac$')
    tlabel(ax, *T(0.115, 0.50), r'$a$-$b$-$c$')
    tlabel(ax, *T(0.44, 0.795), r'$b$-$c$')

    T = mk(13.45, 6.4); tag(13.45, 6.4, 'd')
    P(ax, [T(u, v) for u, v in catmull([(0.03, 0.78), (0.22, 0.55),
                                        (0.45, 0.435), (0.68, 0.52),
                                        (0.87, 0.78)])], **DOT)
    P(ax, [T(u, v) for u, v in [(0.47, 0.425), (0.93, 0.415)]], **DASH)
    tlabel(ax, *T(0.63, 0.345), r'$a$')
    tlabel(ax, *T(0.375, 0.60), r'$a$-$b$')
    tlabel(ax, *T(0.82, 0.585), r'$a$-$b$-$c$')

    # ---------------- 第二行 (e)(f)(g)
    T = mk(3.75, 2.3); tag(3.75, 2.3, 'e')
    P(ax, [T(u, v) for u, v in [(0.04, 0.38), (0.37, 0.47)]])
    P(ax, [T(u, v) for u, v in [(0.37, 0.47), (0.88, 0.505)]], **DASH)
    P(ax, [T(u, v) for u, v in catmull([(0.50, 0.72), (0.43, 0.585),
                                        (0.37, 0.47)])], **DASHDOT)
    tlabel(ax, *T(0.52, 0.40), r'$a$-$d$')
    tlabel(ax, *T(0.655, 0.615), r'$a$-$b$-$c$-$d$')
    tlabel(ax, *T(0.14, 0.68), r'$a$-$b$-$d$')

    T = mk(7.8, 2.3); tag(7.8, 2.3, 'f')
    P(ax, [T(u, v) for u, v in catmull([(0.08, 0.12), (0.28, 0.28),
                                        (0.42, 0.41), (0.50, 0.47)])], **DASHDOT)
    P(ax, [T(u, v) for u, v in catmull([(0.50, 0.47), (0.60, 0.555),
                                        (0.78, 0.70), (0.95, 0.80)])], **DASHDOT)
    P(ax, [T(u, v) for u, v in catmull([(0.03, 0.73), (0.25, 0.62),
                                        (0.40, 0.525), (0.50, 0.47)])], **DASHDOT)
    P(ax, [T(u, v) for u, v in catmull([(0.50, 0.47), (0.53, 0.60),
                                        (0.57, 0.80), (0.60, 0.97)])], **DASHDOT)
    tlabel(ax, *T(0.13, 0.43), r'$a$-$b$-$d$')
    tlabel(ax, *T(0.67, 0.215), r'$a$-$d$')
    tlabel(ax, *T(0.72, 0.535), r'$a$-$c$-$d$')
    tlabel(ax, *T(0.215, 0.80), r'$a$-$b$-$c$-$d$')

    T = mk(12.1, 2.3); tag(12.1, 2.3, 'g')
    P(ax, [T(u, v) for u, v in catmull([(0.06, 0.80), (0.32, 0.63),
                                        (0.545, 0.485), (0.76, 0.36),
                                        (0.92, 0.28)])])
    P(ax, [T(u, v) for u, v in catmull([(0.43, 0.08), (0.47, 0.26),
                                        (0.515, 0.41), (0.545, 0.485)])])
    P(ax, [T(u, v) for u, v in catmull([(0.545, 0.485), (0.65, 0.595),
                                        (0.76, 0.71), (0.88, 0.82)])], **DASH)
    tlabel(ax, *T(0.585, 0.155), r'$b$-$c$')
    tlabel(ax, *T(0.375, 0.465), r'$c$')
    tlabel(ax, *T(0.715, 0.475), r'$a$-$b$-$c$')
    tlabel(ax, *T(0.475, 0.685), r'$a$-$c$')
    save(fig, 41)


# ---------------------------------------------------------------- 图42
def fig_42():
    """§100 图42：两纯物质线 + 临界线（点线 gl）的 PT 投影"""
    fig, ax = plt.subplots(figsize=(2.7, 2.2))
    plain_axes(ax)
    ax.set_xlim(-0.13, 1.10)
    ax.set_ylim(-0.13, 1.02)

    def Y(v):
        return 1 - v

    O = (0.02, Y(0.88))
    arrow_axis(ax, O[0], O[1], O[0], Y(0.055))
    arrow_axis(ax, O[0], O[1], 1.0, O[1])
    tlabel(ax, -0.045, Y(0.05), r'$P$', fs=11, ha='right')
    tlabel(ax, 0.962, Y(0.955), r'$T$', fs=11)

    A = (0.52, Y(0.27)); B = (0.80, Y(0.56))
    cl = catmull([O, (0.30, Y(0.635)), (0.42, Y(0.43)), A])
    cg = catmull([O, (0.30, Y(0.815)), (0.55, Y(0.675)), B])
    arc = catmull([A, (0.615, Y(0.205)), (0.70, Y(0.31)), B])

    plot_curve(ax, cl, lw=1.35)
    plot_curve(ax, cg, lw=1.35)
    plot_curve(ax, arc, lw=1.1, dashes=DOT_CRIT)

    tlabel(ax, 0.37, Y(0.515), r'$l$')
    tlabel(ax, 0.495, Y(0.225), r'$A$')
    tlabel(ax, 0.60, Y(0.125), r'$gl$')
    tlabel(ax, 0.545, Y(0.355), r'$g$-$l$')
    tlabel(ax, 0.62, Y(0.71), r'$g$')
    tlabel(ax, 0.835, Y(0.55), r'$B$', ha='left')
    save(fig, 42)


# ---------------------------------------------------------------- 图43
def fig_43():
    """§100 图43：两纯物质线 + 两条等浓度线（虚线），D 为投影交点"""
    fig, ax = plt.subplots(figsize=(2.75, 2.25))
    plain_axes(ax)
    ax.set_xlim(-0.13, 1.16)
    ax.set_ylim(-0.13, 1.03)

    def Y(v):
        return 1 - v

    O = (0.02, Y(0.88))
    arrow_axis(ax, O[0], O[1], O[0], Y(0.05))
    arrow_axis(ax, O[0], O[1], 1.05, O[1])
    tlabel(ax, -0.045, Y(0.045), r'$P$', fs=11, ha='right')
    tlabel(ax, 1.012, Y(0.955), r'$T$', fs=11)

    A = (0.545, Y(0.10)); B = (0.82, Y(0.10))
    D = (0.72, Y(0.47)); C = (1.03, Y(0.43))
    cOB = catmull([O, (0.40, Y(0.70)), (0.58, Y(0.545)), D,
                   (0.77, Y(0.30)), (0.80, Y(0.16)), B])
    cOC = catmull([O, (0.45, Y(0.775)), (0.75, Y(0.565)), C])
    lineOA = np.array([O, A])
    arc = catmull([A, (0.615, Y(0.26)), (0.67, Y(0.385)), D,
                   (0.83, Y(0.455)), (0.95, Y(0.44)), C])

    plot_curve(ax, cOB, lw=1.35)
    plot_curve(ax, cOC, lw=1.35)
    plot_curve(ax, lineOA, lw=1.0, dashes=DASH_EQ)
    plot_curve(ax, arc, lw=1.0, dashes=DASH_EQ)

    tlabel(ax, 0.505, Y(0.075), r'$A$')
    tlabel(ax, 0.845, Y(0.09), r'$B$', ha='left')
    tlabel(ax, 1.0, Y(0.355), r'$C$')
    tlabel(ax, 0.77, Y(0.52), r'$D$', ha='left')
    tlabel(ax, 0.265, Y(0.47), r'$l$')
    tlabel(ax, 0.632, Y(0.28), r'$gl_1$-$l_2$', rot=58)
    tlabel(ax, 0.588, Y(0.51), r'$l_1$-$g$-$l_2$', rot=52)
    tlabel(ax, 0.705, Y(0.68), r'$l_1$-$g$')
    tlabel(ax, 0.885, Y(0.575), r'$g$')
    save(fig, 43)


# ---------------------------------------------------------------- 图44
def fig_44():
    """§100 图44：图43 的一系列 T 截面（P-x），T<T_A / T_A<T<T_B / T_B<T<T_C"""
    fig, ax = plt.subplots(figsize=(3.95, 1.82))
    plain_axes(ax)
    PW = 0.76; GAP = 0.40
    x0s = [0.0, PW + GAP, 2 * (PW + GAP)]
    ax.set_xlim(-0.13, 3 * PW + 2 * GAP + 0.05)
    ax.set_ylim(-1.45, 0.10)

    def P(pts, x0):
        return np.asarray([(x0 + u * PW, -v) for u, v in pts], float)

    def cap(i, s):
        panel_cap(ax, x0s[i], PW, s)

    # ---- 面板1 T<T_A
    x0 = x0s[0]; panel_frame(ax, x0, 'P', PW)
    up = catmull([(0, 0.50), (0.14, 0.24), (0.30, 0.15), (0.52, 0.19),
                  (0.75, 0.30), (1.0, 0.40)])
    lo = catmull([(0, 0.52), (0.20, 0.40), (0.42, 0.335), (0.68, 0.36),
                  (1.0, 0.43)])
    hatch_region(ax, P(np.vstack([up, lo[::-1]]), x0), dy=0.05)
    plot_curve(ax, P(up, x0)); plot_curve(ax, P(lo, x0))
    tlabel(ax, x0 + 0.35 * PW, -0.09, r'$l$')
    tlabel(ax, x0 + 0.045 * PW, -0.27, r'$l_1$')
    tlabel(ax, x0 + 0.40 * PW, -0.44, r'$g$')
    tlabel(ax, x0 + 0.885 * PW, -0.145, r'$l_2$')
    cap(0, r'$T<T_A$')

    # ---- 面板2 T_A<T<T_B
    x0 = x0s[1]; panel_frame(ax, x0, 'P', PW)
    lens1 = catmull([(0, 0.52), (0.16, 0.33), (0.32, 0.235), (0.43, 0.225),
                     (0.465, 0.27), (0.43, 0.33), (0.30, 0.415),
                     (0.14, 0.48), (0, 0.545)])
    lens2 = catmull([(1.0, 0.405), (0.88, 0.285), (0.73, 0.17), (0.62, 0.125),
                     (0.555, 0.16), (0.60, 0.235), (0.70, 0.30),
                     (0.85, 0.375), (1.0, 0.44)])
    hatch_region(ax, P(lens1, x0), dy=0.05)
    hatch_region(ax, P(lens2, x0), dy=0.05)
    plot_curve(ax, P(lens1, x0)); plot_curve(ax, P(lens2, x0))
    tlabel(ax, x0 + 0.10 * PW, -0.20, r'$l_1$')
    tlabel(ax, x0 + 0.42 * PW, -0.40, r'$g$')
    tlabel(ax, x0 + 0.585 * PW, -0.075, r'$l_2$')
    cap(1, r'$T_A<T<T_B$')

    # ---- 面板3 T_B<T<T_C
    x0 = x0s[2]; panel_frame(ax, x0, 'P', PW)
    lens = catmull([(0, 0.50), (0.13, 0.34), (0.25, 0.295), (0.315, 0.325),
                    (0.30, 0.385), (0.17, 0.44), (0, 0.52)])
    hatch_region(ax, P(lens, x0), dy=0.05)
    plot_curve(ax, P(lens, x0))
    tlabel(ax, x0 + 0.105 * PW, -0.245, r'$l_1$')
    tlabel(ax, x0 + 0.30 * PW, -0.50, r'$g$')
    cap(2, r'$T_B<T<T_C$')
    save(fig, 44)


# ---------------------------------------------------------------- 图45
def fig_45():
    """§100 图45：图43 的一系列 P 截面（T-x），P<P_C / P_C<P<P_A / P_A<P<P_B"""
    fig, ax = plt.subplots(figsize=(3.95, 1.82))
    plain_axes(ax)
    PW = 0.76; GAP = 0.40
    x0s = [0.0, PW + GAP, 2 * (PW + GAP)]
    ax.set_xlim(-0.13, 3 * PW + 2 * GAP + 0.05)
    ax.set_ylim(-1.45, 0.10)

    def P(pts, x0):
        return np.asarray([(x0 + u * PW, -v) for u, v in pts], float)

    def cap(i, s):
        panel_cap(ax, x0s[i], PW, s)

    # ---- 面板1 P<P_C
    x0 = x0s[0]; panel_frame(ax, x0, 'T', PW)
    up1 = catmull([(0, 0.28), (0.30, 0.49), (0.55, 0.665), (0.78, 0.795)])
    lo1 = catmull([(0, 0.42), (0.30, 0.60), (0.55, 0.73), (0.78, 0.80)])
    up2 = catmull([(0.78, 0.795), (0.90, 0.615), (1.0, 0.475)])
    lo2 = catmull([(0.78, 0.80), (0.88, 0.70), (1.0, 0.565)])
    band = np.vstack([up1, up2[1:], np.array([[1.0, 0.565]]),
                      lo2[::-1][1:-1], np.array([[0.78, 0.80]]),
                      lo1[::-1][1:], np.array([[0.0, 0.42]])])
    lens = np.vstack([up2, np.array([[1.0, 0.475]]),
                      np.array([[1.0, 0.565]]), lo2[::-1][1:-1],
                      np.array([[0.78, 0.795]])])
    hatch_region(ax, P(band, x0), dy=0.05)
    hatch_region(ax, P(lens, x0), dy=0.05)
    for c in (up1, lo1, up2, lo2):
        plot_curve(ax, P(c, x0))
    tlabel(ax, x0 + 0.72 * PW, -0.33, r'$g$')
    tlabel(ax, x0 + 0.085 * PW, -0.52, r'$l_1$')
    tlabel(ax, x0 + 0.56 * PW, -0.70, r'$l_2$')
    tlabel(ax, x0 + 0.79 * PW, -0.885, r'$l$')
    cap(0, r'$P<P_C$')

    # ---- 面板2 P_C<P<P_A
    x0 = x0s[1]; panel_frame(ax, x0, 'T', PW)
    up1 = catmull([(0.25, 0.335), (0.42, 0.50), (0.62, 0.675), (0.80, 0.79)])
    lo1 = catmull([(0.80, 0.81), (0.66, 0.745), (0.50, 0.665), (0.36, 0.555),
                   (0.27, 0.455), (0.225, 0.385), (0.25, 0.335)])
    up2 = catmull([(0.80, 0.79), (0.90, 0.625), (1.0, 0.505)])
    lo2 = catmull([(0.80, 0.81), (0.885, 0.705), (1.0, 0.585)])
    blob = np.vstack([up1, up2[1:], np.array([[1.0, 0.585]]),
                      lo2[::-1][1:-1], np.array([[0.80, 0.81]]),
                      lo1[::-1][1:-1], np.array([[0.25, 0.335]])])
    lens = np.vstack([up2, np.array([[1.0, 0.505]]),
                      np.array([[1.0, 0.585]]), lo2[::-1][1:-1],
                      np.array([[0.80, 0.79]])])
    hatch_region(ax, P(blob, x0), dy=0.05)
    hatch_region(ax, P(lens, x0), dy=0.05)
    for c in (up1, lo1, up2, lo2):
        plot_curve(ax, P(c, x0))
    tlabel(ax, x0 + 0.74 * PW, -0.36, r'$g$')
    tlabel(ax, x0 + 0.165 * PW, -0.535, r'$l_1$')
    tlabel(ax, x0 + 0.60 * PW, -0.71, r'$l_2$')
    tlabel(ax, x0 + 0.815 * PW, -0.885, r'$l$')
    cap(1, r'$P_C<P<P_A$')

    # ---- 面板3 P_A<P<P_B
    x0 = x0s[2]; panel_frame(ax, x0, 'T', PW)
    lens = catmull([(0.74, 0.515), (0.86, 0.545), (1.0, 0.528),
                    (1.0, 0.60), (0.86, 0.585), (0.745, 0.55),
                    (0.70, 0.533)])
    hatch_region(ax, P(lens, x0), dy=0.05)
    plot_curve(ax, P(lens, x0))
    tlabel(ax, x0 + 0.755 * PW, -0.475, r'$g$')
    tlabel(ax, x0 + 0.80 * PW, -0.665, r'$l_2$')
    cap(2, r'$P_A<P<P_B$')
    save(fig, 45)


# ---------------------------------------------------------------- 图46
def fig_46():
    """§100 图46：三相线在两纯物质线上方的 PT 投影（临界线 C-A 与 B-上方）"""
    fig, ax = plt.subplots(figsize=(2.75, 2.2))
    plain_axes(ax)
    ax.set_xlim(-0.13, 1.10)
    ax.set_ylim(-0.13, 1.04)

    def Y(v):
        return 1 - v

    O = (0.03, Y(0.91))
    arrow_axis(ax, O[0], O[1], O[0], Y(0.17))
    arrow_axis(ax, O[0], O[1], 1.0, O[1])
    tlabel(ax, -0.04, Y(0.155), r'$P$', fs=11, ha='right')
    tlabel(ax, 0.96, Y(0.98), r'$T$', fs=11)

    A = (0.59, Y(0.585)); B = (0.70, Y(0.755)); C = (0.455, Y(0.40))
    s1 = catmull([O, (0.35, Y(0.82)), (0.48, Y(0.70)), A])
    s2 = catmull([O, (0.35, Y(0.855)), (0.52, Y(0.835)), (0.63, Y(0.80)), B])
    t3 = catmull([O, (0.24, Y(0.745)), (0.36, Y(0.565)), C])
    arcCA = catmull([C, (0.545, Y(0.49)), A])
    arcB = catmull([B, (0.80, Y(0.555)), (0.845, Y(0.375)),
                    (0.868, Y(0.25)), (0.878, Y(0.11))])

    plot_curve(ax, s1, lw=1.35)
    plot_curve(ax, s2, lw=1.35)
    plot_curve(ax, t3, lw=1.0, dashes=DASHDOT_3P)
    plot_curve(ax, arcCA, lw=1.1, dashes=DOT_CRIT)
    plot_curve(ax, arcB, lw=1.1, dashes=DOT_CRIT)

    tlabel(ax, 0.25, Y(0.63), r'$l_1$-$l_2$')
    tlabel(ax, 0.395, Y(0.715), r'$l_1$-$g$-$l_2$', rot=48)
    tlabel(ax, 0.60, Y(0.435), r'$l_1$-$gl_2$')
    tlabel(ax, 0.50, Y(0.825), r'$l_1$-$g$')
    tlabel(ax, 0.535, Y(0.945), r'$g$')
    tlabel(ax, 0.615, Y(0.615), r'$A$', ha='left')
    tlabel(ax, 0.725, Y(0.775), r'$B$', ha='left')
    tlabel(ax, 0.475, Y(0.355), r'$C$')
    save(fig, 46)


# ---------------------------------------------------------------- 图47
def fig_47():
    """§100 图47：三相线在两纯物质线之间的 PT 投影（临界线 A-B 与 C-上方）"""
    fig, ax = plt.subplots(figsize=(2.75, 2.2))
    plain_axes(ax)
    ax.set_xlim(-0.13, 1.10)
    ax.set_ylim(-0.13, 1.04)

    def Y(v):
        return 1 - v

    O = (0.03, Y(0.91))
    arrow_axis(ax, O[0], O[1], O[0], Y(0.17))
    arrow_axis(ax, O[0], O[1], 1.0, O[1])
    tlabel(ax, -0.04, Y(0.155), r'$P$', fs=11, ha='right')
    tlabel(ax, 0.96, Y(0.98), r'$T$', fs=11)

    A = (0.475, Y(0.27)); B = (0.725, Y(0.84)); C = (0.545, Y(0.62))
    s1 = catmull([O, (0.30, Y(0.55)), (0.42, Y(0.38)), A])
    s2 = catmull([O, (0.40, Y(0.815)), (0.60, Y(0.775)), (0.68, Y(0.79)), B])
    t3 = catmull([O, (0.30, Y(0.775)), C])
    arcAB = catmull([A, (0.53, Y(0.365)), (0.585, Y(0.48)), (0.635, Y(0.62)),
                     (0.68, Y(0.74)), B])
    arcCup = catmull([C, (0.60, Y(0.455)), (0.635, Y(0.30)), (0.67, Y(0.10))])

    plot_curve(ax, s1, lw=1.35)
    plot_curve(ax, s2, lw=1.35)
    plot_curve(ax, t3, lw=1.0, dashes=DASHDOT_3P)
    plot_curve(ax, arcAB, lw=1.1, dashes=DOT_CRIT)
    plot_curve(ax, arcCup, lw=1.1, dashes=DOT_CRIT)

    tlabel(ax, 0.255, Y(0.635), r'$l_1$-$l_2$')
    tlabel(ax, 0.465, Y(0.45), r'$l_1$-$l_2$-$g$', rot=36)
    tlabel(ax, 0.38, Y(0.91), r'$l_1$-$g$')
    tlabel(ax, 0.615, Y(0.965), r'$g$')
    tlabel(ax, 0.475, Y(0.21), r'$A$')
    tlabel(ax, 0.76, Y(0.865), r'$B$', ha='left')
    tlabel(ax, 0.575, Y(0.665), r'$C$', ha='left')
    save(fig, 47)


# ---------------------------------------------------------------- 图48
def fig_48():
    """§100 图48：图46 情形的一系列 T 截面（P-x），T<T_C / T_C<T<T_A / T_A<T<T_B / T_B<T"""
    fig, ax = plt.subplots(figsize=(3.95, 1.52))
    plain_axes(ax)
    PW = 0.82; GAP = 0.28
    x0s = [i * (PW + GAP) for i in range(4)]
    ax.set_xlim(-0.12, 4 * PW + 3 * GAP + 0.03)
    ax.set_ylim(-1.48, 0.10)

    def P(pts, x0):
        return np.asarray([(x0 + u * PW, -v) for u, v in pts], float)

    def cap(i, s):
        panel_cap(ax, x0s[i], PW, s)

    # ---- 面板1 T<T_C：顶部 l1-l2 带 + 两条腿（三相线处连通）
    x0 = x0s[0]; panel_frame(ax, x0, 'P', PW)
    top = catmull([(0.18, 0.118), (0.50, 0.105), (0.82, 0.103)])
    sideL = catmull([(0.18, 0.118), (0.227, 0.287), (0.279, 0.456),
                     (0.291, 0.559)])
    sideR = catmull([(0.82, 0.103), (0.779, 0.287), (0.727, 0.456),
                     (0.703, 0.559)])
    BL = (0.291, 0.559); BR = (0.703, 0.559); Gp = (0.512, 0.559)
    legLup = catmull([BL, (0.227, 0.618), (0.122, 0.70), (0, 0.706)])
    legLdn = catmull([Gp, (0.424, 0.639), (0.285, 0.728), (0.134, 0.831),
                      (0, 0.868)])
    legRup = catmull([BR, (0.779, 0.618), (0.878, 0.669), (1.0, 0.691)])
    legRdn = catmull([Gp, (0.610, 0.639), (0.75, 0.713), (0.901, 0.787),
                      (1.0, 0.816)])
    band = np.vstack([top, sideR[1:], np.array([BR]), np.array([Gp]),
                      np.array([BL]), sideL[::-1][1:]])
    leg1 = np.vstack([np.array([BL]), legLup[1:], np.array([[0.0, 0.868]]),
                      legLdn[::-1][1:]])
    leg2 = np.vstack([np.array([Gp]), legRdn[1:], np.array([[1.0, 0.691]]),
                      legRup[::-1][1:]])
    for lp in (band, leg1, leg2):
        hatch_region(ax, P(lp, x0), dy=0.045)
    for c in (top, sideL, sideR, legLup, legLdn, legRup, legRdn):
        plot_curve(ax, P(c, x0))
    plot_curve(ax, P(np.array([BL, Gp, BR]), x0))
    tlabel(ax, x0 + 0.157 * PW, -0.493, r'$l_1$')
    tlabel(ax, x0 + 0.86 * PW, -0.493, r'$l_2$')
    tlabel(ax, x0 + 0.512 * PW, -0.838, r'$g$')
    cap(0, r'$T<T_C$')

    # ---- 面板2 T_C<T<T_A
    x0 = x0s[1]; panel_frame(ax, x0, 'P', PW)
    big = np.vstack([
        catmull([(0, 0.928), (0.0625, 0.674), (0.108, 0.456),
                 (0.159, 0.254), (0.222, 0.145)]),
        catmull([(0.222, 0.145), (0.426, 0.087), (0.631, 0.072)])[1:],
        catmull([(0.631, 0.072), (0.614, 0.167), (0.568, 0.37), (0.489, 0.58),
                 (0.375, 0.761), (0.199, 0.913), (0, 0.928)])[1:]])
    lens = catmull([(1.0, 0.55), (0.93, 0.51), (0.845, 0.488), (0.77, 0.483),
                    (0.725, 0.52), (0.74, 0.575), (0.81, 0.615),
                    (0.90, 0.635), (1.0, 0.61)])
    hatch_region(ax, P(big, x0), dy=0.045)
    hatch_region(ax, P(lens, x0), dy=0.045)
    plot_curve(ax, P(big, x0)); plot_curve(ax, P(lens, x0))
    tlabel(ax, x0 + 0.148 * PW, -0.413, r'$l_1$')
    tlabel(ax, x0 + 0.82 * PW, -0.425, r'$l_2$')
    tlabel(ax, x0 + 0.66 * PW, -0.80, r'$g$')
    cap(1, r'$T_C<T<T_A$')

    # ---- 面板3 T_A<T<T_B
    x0 = x0s[2]; panel_frame(ax, x0, 'P', PW)
    shape = np.vstack([
        catmull([(0, 0.90), (0.067, 0.80), (0.128, 0.657), (0.161, 0.453),
                 (0.189, 0.08)]),
        catmull([(0.189, 0.08), (0.378, 0.051), (0.533, 0.036),
                 (0.639, 0.029)])[1:],
        catmull([(0.639, 0.029), (0.606, 0.132), (0.544, 0.27), (0.467, 0.416),
                 (0.372, 0.562), (0.256, 0.701), (0.133, 0.832), (0, 0.90)])[1:]])
    hatch_region(ax, P(shape, x0), dy=0.045)
    plot_curve(ax, P(shape, x0))
    tlabel(ax, x0 + 0.13 * PW, -0.36, r'$l_1$')
    tlabel(ax, x0 + 0.56 * PW, -0.585, r'$gl_2$')
    cap(2, r'$T_A<T<T_B$')

    # ---- 面板4 T_B<T
    x0 = x0s[3]; panel_frame(ax, x0, 'P', PW)
    lens = np.vstack([
        catmull([(0.295, 0.245), (0.40, 0.235), (0.53, 0.23)]),
        catmull([(0.53, 0.23), (0.545, 0.33), (0.55, 0.41), (0.545, 0.49),
                 (0.52, 0.565), (0.475, 0.62), (0.42, 0.655), (0.36, 0.675),
                 (0.30, 0.675), (0.25, 0.655), (0.22, 0.615), (0.215, 0.56),
                 (0.225, 0.49), (0.245, 0.40), (0.27, 0.31),
                 (0.295, 0.245)])[1:]])
    hatch_region(ax, P(lens, x0), dy=0.045)
    plot_curve(ax, P(lens, x0))
    tlabel(ax, x0 + 0.09 * PW, -0.45, r'$l_1$')
    tlabel(ax, x0 + 0.62 * PW, -0.57, r'$gl_2$')
    cap(3, r'$T_B<T$')
    save(fig, 48)


# ---------------------------------------------------------------- 图49
def fig_49():
    """§100 图49：图47 情形的一系列 P 截面（T-x），P<P_B / P_B<P<P_A / P_A<P<P_C / P_C<P"""
    fig, ax = plt.subplots(figsize=(3.95, 1.62))
    plain_axes(ax)
    PW = 0.75; GAP = 0.30
    x0s = [i * (PW + GAP) for i in range(4)]
    ax.set_xlim(-0.12, 4 * PW + 3 * GAP + 0.03)
    ax.set_ylim(-1.48, 0.10)

    def P(pts, x0):
        return np.asarray([(x0 + u * PW, -v) for u, v in pts], float)

    def cap(i, s):
        panel_cap(ax, x0s[i], PW, s)

    # ---- 面板1 P<P_B：垂耳（左耳贴轴、右耳触轴）
    x0 = x0s[0]; panel_frame(ax, x0, 'T', PW)
    W1 = (0.354, 0.685); W2 = (0.731, 0.685); Ap = (0.503, 0.661)
    earL = np.vstack([
        catmull([(0.0, 0.244), (0.24, 0.363), (0.44, 0.46), Ap]),
        catmull([Ap, (0.42, 0.60), (0.30, 0.52), (0.149, 0.411),
                 (0.0, 0.244)])[1:]])
    earR = np.vstack([
        catmull([(1.0, 0.399), (0.90, 0.455), (0.811, 0.595), W2]),
        catmull([W2, (0.764, 0.537), (0.848, 0.451), (0.927, 0.327),
                 (1.0, 0.399)])[1:]])
    body = np.vstack([np.array([W1]), np.array([W2]),
                      catmull([W2, (0.811, 0.80), (0.846, 0.917),
                               (0.857, 1.0)])[1:],
                      np.array([[0.217, 1.0]]),
                      catmull([(0.217, 1.0), (0.229, 0.917), (0.274, 0.80),
                               W1])[1:], np.array([W1])])
    for lp in (earL, earR, body):
        hatch_region(ax, P(lp, x0), dy=0.042)
        plot_curve(ax, P(lp, x0))
    tlabel(ax, x0 + 0.526 * PW, -0.559, r'$g$')
    tlabel(ax, x0 + 0.183 * PW, -0.66, r'$l_1$')
    tlabel(ax, x0 + 0.88 * PW, -0.714, r'$l_2$')
    cap(0, r'$P<P_B$')

    # ---- 面板2 P_B<P<P_A：左耳圆头、右耳触轴
    x0 = x0s[1]; panel_frame(ax, x0, 'T', PW)
    W1 = (0.292, 0.568); W2 = (0.685, 0.568)
    earL = np.vstack([
        catmull([W1, (0.25, 0.47), (0.165, 0.34), (0.135, 0.22),
                 (0.165, 0.14), (0.27, 0.185), (0.365, 0.31),
                 (0.415, 0.445), W1])])
    earR = np.vstack([
        catmull([W2, (0.75, 0.46), (0.85, 0.34), (0.945, 0.25),
                 (1.0, 0.216)]),
        catmull([(1.0, 0.216), (0.93, 0.33), (0.85, 0.45), (0.775, 0.53),
                 W2])[1:]])
    body = np.vstack([np.array([W1]), np.array([W2]),
                      catmull([W2, (0.725, 0.697), (0.753, 0.858),
                               (0.764, 1.0)])[1:],
                      np.array([[0.247, 1.0]]),
                      catmull([(0.247, 1.0), (0.253, 0.858), (0.27, 0.697),
                               W1])[1:], np.array([W1])])
    for lp in (earL, earR, body):
        hatch_region(ax, P(lp, x0), dy=0.042)
        plot_curve(ax, P(lp, x0))
    tlabel(ax, x0 + 0.478 * PW, -0.432, r'$g$')
    tlabel(ax, x0 + 0.197 * PW, -0.574, r'$l_1$')
    tlabel(ax, x0 + 0.787 * PW, -0.612, r'$l_2$')
    cap(1, r'$P_B<P<P_A$')

    # ---- 面板3 P_A<P<P_C：左耳高、右耳小圆
    x0 = x0s[2]; panel_frame(ax, x0, 'T', PW)
    W1 = (0.294, 0.413); W2 = (0.688, 0.413)
    earL = np.vstack([
        catmull([W1, (0.453, 0.356), (0.371, 0.244), (0.288, 0.088),
                 (0.218, 0.038), (0.159, 0.106), (0.165, 0.219),
                 (0.235, 0.363), W1])])
    earR = np.vstack([
        catmull([W2, (0.747, 0.319), (0.776, 0.25), (0.741, 0.294), W2])])
    body = np.vstack([np.array([W1]), np.array([W2]),
                      catmull([W2, (0.747, 0.531), (0.776, 0.719),
                               (0.794, 1.0)])[1:],
                      np.array([[0.229, 1.0]]),
                      catmull([(0.229, 1.0), (0.253, 0.719), (0.282, 0.531),
                               W1])[1:], np.array([W1])])
    for lp in (earL, earR, body):
        hatch_region(ax, P(lp, x0), dy=0.042)
        plot_curve(ax, P(lp, x0))
    tlabel(ax, x0 + 0.553 * PW, -0.281, r'$g$')
    tlabel(ax, x0 + 0.182 * PW, -0.44, r'$l_1$')
    tlabel(ax, x0 + 0.776 * PW, -0.48, r'$l_2$')
    cap(2, r'$P_A<P<P_C$')

    # ---- 面板4 P_C<P：圆顶
    x0 = x0s[3]; panel_frame(ax, x0, 'T', PW)
    dome = np.vstack([catmull([
        (0.21, 1.0), (0.222, 0.882), (0.245, 0.634), (0.281, 0.422),
        (0.339, 0.286), (0.409, 0.242), (0.468, 0.235), (0.527, 0.242),
        (0.573, 0.298), (0.643, 0.447), (0.702, 0.634), (0.737, 0.845),
        (0.754, 1.0)]), np.array([[0.21, 1.0]])])
    hatch_region(ax, P(dome, x0), dy=0.042)
    plot_curve(ax, P(dome[:-1], x0))
    tlabel(ax, x0 + 0.16 * PW, -0.63, r'$l_1$')
    tlabel(ax, x0 + 0.77 * PW, -0.63, r'$l_2$')
    cap(3, r'$P_C<P$')
    save(fig, 49)


if __name__ == '__main__':
    for i in range(36, 50):
        globals()[f'fig_{i}']()
        print(f'fig{i} done')
