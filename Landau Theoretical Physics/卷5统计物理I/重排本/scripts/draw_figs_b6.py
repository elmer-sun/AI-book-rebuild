# -*- coding: utf-8 -*-
"""
朗道《统计物理学I》（卷5）中文重排本 插图重绘 第六批：图60-图70
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p-401..p-443，按 figures_manifest.md 哈希反查页码）：
  图60 -> p401；图61 -> p402；图62 -> p405；图63、64 -> p410；图65 -> p420；
  图66 -> p438；图67、68、69 -> p441；图70 -> p443。
内容：第十四章 二级相变与临界现象。
  图60 §142 BaTiO3 钙钛矿立方晶胞；图61 §142 CuZn 有序(a)/无序(b)晶胞；
  图62 §143 热力学势 Phi(eta)（A>0 / A<0）；图63 §144 方程左端 η 曲线（t>0/t<0）；
  图64 §144 序参量对场 η(h)（t>0/t<0，亚稳段虚线）；图65 §145 有序合金超晶格
  （2x2x2 胞原子分布 a/b）；图66 §150 二级相变临界点 K（实线一级/虚线二级）；
  图67 §150 二级线 AC 与一级线 BD 相交（双临界点）；图68 §150 几条二级线相交
  （四临界点）；图69 §150 孤立连续相变点 O 的两种情形 (a)(b)；图70 §150 习题
  栗弗希兹点 L 相图。
线型约定（§150 各图）：实线=一级相变线，虚线=二级相变线。
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
DASH_2ND = (4.5, 2.0)          # 二级相变线 / 虚辅助线
DASH_CUBE = (3.2, 1.8)         # 晶胞内虚线


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


def line(ax, pts, lw=LW_MAIN, dashes=None, z=2):
    pts = np.asarray(pts, float)
    if dashes is not None:
        ln, = ax.plot(pts[:, 0], pts[:, 1], color='k', lw=lw, zorder=z,
                      dashes=dashes)
    else:
        ln, = ax.plot(pts[:, 0], pts[:, 1], color='k', lw=lw, zorder=z)
    return ln


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


def tlabel(ax, x, y, s, fs=10, ha='center', va='center', rot=None, white=False):
    kw = {}
    if white:
        kw['bbox'] = dict(boxstyle='square', fc='white', ec='none', pad=0.12)
    if rot is not None:
        kw['rotation'] = rot
        kw['rotation_mode'] = 'anchor'
    ax.text(x, y, s, fontsize=fs, ha=ha, va=va, zorder=5, **kw)


def cross_mark(ax, x, y, r=0.055, lw=1.0, z=3):
    """× 记号（两条短斜线）。"""
    ax.plot([x - r, x + r], [y - r, y + r], color='k', lw=lw, zorder=z)
    ax.plot([x - r, x + r], [y + r, y - r], color='k', lw=lw, zorder=z)


def circ_x_mark(ax, x, y, r=0.062, lw=1.0, z=3):
    """⊗ 记号（圆圈中叉）。"""
    ax.add_patch(plt.Circle((x, y), r, fill=False, lw=lw, ec='k', zorder=z))
    rr = r * 0.62
    ax.plot([x - rr, x + rr], [y - rr, y + rr], color='k', lw=lw, zorder=z)
    ax.plot([x - rr, x + rr], [y + rr, y - rr], color='k', lw=lw, zorder=z)


def atom_O(ax, x, y, r=0.052, z=4):
    """图60 的 O 原子：圆圈内左下一个小实心点。"""
    ax.add_patch(plt.Circle((x, y), r, facecolor='white', edgecolor='k',
                            lw=1.0, zorder=z))
    ax.add_patch(plt.Circle((x - 0.28 * r, y - 0.30 * r), 0.34 * r,
                            facecolor='k', edgecolor='none', zorder=z + 0.1))


def atom_Ti(ax, x, y, r=0.062, z=4):
    """图60 的 Ti 原子：实心圆内左下一个小白点。"""
    ax.add_patch(plt.Circle((x, y), r, facecolor='k', edgecolor='k',
                            lw=0.8, zorder=z))
    ax.add_patch(plt.Circle((x - 0.26 * r, y - 0.28 * r), 0.30 * r,
                            facecolor='white', edgecolor='none', zorder=z + 0.1))


# ---------------------------------------------------------------- 图60
def fig_60():
    """§142 图60：BaTiO3 钙钛矿立方晶胞（Ba 顶点、O 面心、Ti 体心）"""
    fig, ax = plt.subplots(figsize=(2.15, 2.45))
    plain_axes(ax)
    ax.set_xlim(-0.18, 1.72)
    ax.set_ylim(-0.62, 1.42)
    ax.set_aspect('equal')

    d = np.array([0.42, 0.26])                    # 深度方向（斜二测）
    front = [np.array(p, float) for p in
             [(0, 0), (1, 0), (1, 1), (0, 1)]]
    back = [p + d for p in front]
    # 棱
    for p, q in zip(front, back):
        ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=1.1, zorder=2)
    for i in range(4):
        p, q = front[i], front[(i + 1) % 4]
        ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=1.1, zorder=2)
        p, q = back[i], back[(i + 1) % 4]
        ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=1.1, zorder=2)

    # O：6 个面心
    fcmid = lambda a, b, c, e: (a + b + c + e) / 4.0
    O_faces = [
        fcmid(*front),                     # 前
        fcmid(*back),                      # 后
        fcmid(front[0], front[3], back[0], back[3]),   # 左
        fcmid(front[1], front[2], back[1], back[2]),   # 右
        fcmid(front[2], front[3], back[2], back[3]),   # 顶
        fcmid(front[0], front[1], back[0], back[1]),   # 底
    ]
    Ti = (front[0] + back[2]) / 2.0                # 体心
    # 后面 O 先画
    atom_O(ax, *O_faces[1], z=2.5)
    for p in (O_faces[2], O_faces[3], O_faces[4], O_faces[5]):
        atom_O(ax, *p, z=2.6)
    atom_Ti(ax, *Ti, z=3.0)
    atom_O(ax, *O_faces[0], z=3.5)                 # 前面 O 最后

    # Ba：8 个顶点小实心点
    for p in front + back:
        ax.add_patch(plt.Circle(p, 0.030, facecolor='k', edgecolor='k',
                                lw=0.6, zorder=4))

    # 图例
    y0 = -0.38
    ax.add_patch(plt.Circle((-0.02, y0), 0.026, facecolor='k',
                            edgecolor='k', lw=0.6, zorder=4))
    ax.text(0.10, y0, 'Ba', fontsize=10, ha='left', va='center')
    atom_O(ax, 0.62, y0, r=0.052, z=4)
    ax.text(0.74, y0, 'O', fontsize=10, ha='left', va='center')
    atom_Ti(ax, 1.22, y0, r=0.062, z=4)
    ax.text(1.34, y0, 'Ti', fontsize=10, ha='left', va='center')
    save(fig, 60)


# ---------------------------------------------------------------- 图61
def fig_61():
    """§142 图61：CuZn 合金 (a) 有序简立方 (b) 无序体心立方"""
    fig, axes = plt.subplots(1, 2, figsize=(3.25, 1.85))
    d = np.array([0.40, 0.24])

    def cube(ax, mark, center_mark):
        front = [np.array(p, float) for p in [(0, 0), (1, 0), (1, 1), (0, 1)]]
        back = [p + d for p in front]
        for p, q in zip(front, back):
            ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=1.0, zorder=2)
        for i in range(4):
            p, q = front[i], front[(i + 1) % 4]
            ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=1.0, zorder=2)
            p, q = back[i], back[(i + 1) % 4]
            ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=1.0, zorder=2)
        for p in front + back:
            mark(ax, p[0], p[1])
        center_mark(ax, *(np.array(front[0]) + np.array(back[2])) / 2.0)

    # (a) 顶点 ×，体心 ○
    cube(axes[0], lambda a, x, y: cross_mark(a, x, y, r=0.062, lw=1.1),
         lambda a, x, y: a.add_patch(plt.Circle((x, y), 0.055, fill=False,
                                                lw=1.1, ec='k', zorder=4)))
    # (b) 顶点与体心均 ⊗
    cube(axes[1], lambda a, x, y: circ_x_mark(a, x, y, r=0.070, lw=1.0),
         lambda a, x, y: circ_x_mark(a, x, y, r=0.070, lw=1.0))

    for i, ax in enumerate(axes):
        plain_axes(ax)
        ax.set_xlim(-0.22, 1.62)
        ax.set_ylim(-0.78, 1.42)
        ax.set_aspect('equal')
        ax.text(0.6, -0.48, f'({chr(97 + i)})', fontsize=10, ha='center',
                va='center')
    fig.text(0.52, 0.035, r'$\times$ Zn$\;\;\;\circ$ Cu', fontsize=10,
             ha='center', va='center')
    save(fig, 61)


# ---------------------------------------------------------------- 图62
def fig_62():
    """§143 图62：热力学势 Phi(eta)，A>0 单谷 / A<0 双谷（仅 η>=0）"""
    fig, ax = plt.subplots(figsize=(2.55, 2.5))
    plain_axes(ax)
    ax.set_xlim(-0.16, 1.42)
    ax.set_ylim(-0.68, 1.32)

    # 坐标轴（十字，箭头）
    ax.annotate('', xy=(0, 1.28), xytext=(0, -0.62),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2,
                                shrinkA=0, shrinkB=0, mutation_scale=12))
    ax.annotate('', xy=(1.38, 0), xytext=(-0.07, 0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2,
                                shrinkA=0, shrinkB=0, mutation_scale=12))
    ax.text(-0.05, 1.26, r'$\Phi$', fontsize=11, ha='right', va='center')
    ax.text(1.30, -0.10, r'$\eta$', fontsize=11, ha='center', va='center')

    e1 = np.linspace(0, 0.655, 100)
    ax.plot(e1, 2.6 * e1 ** 2, 'k-', lw=1.2, zorder=3)          # A>0
    e2 = np.linspace(0, 0.95, 100)
    ax.plot(e2, -1.1 * e2 ** 2 + 2.55 * e2 ** 4, 'k-', lw=1.2, zorder=3)

    ax.text(0.30, 0.52, r'$A>0$', fontsize=10, ha='center', va='center')
    ax.text(0.80, 0.52, r'$A<0$', fontsize=10, ha='center', va='center')
    save(fig, 62)


# ---------------------------------------------------------------- 图63
def fig_63():
    """§144 图63：方程(144.4)左端 f(η)=2aηt+4Bη³（a t>0，b t<0）"""
    fig, axes = plt.subplots(1, 2, figsize=(3.9, 2.05))

    def frame(ax, formula):
        plain_axes(ax)
        ax.set_xlim(-1.45, 1.62)
        ax.set_ylim(-1.42, 1.42)
        arrow_axis(ax, 0, -1.06, 0, 1.10)
        arrow_axis(ax, -1.16, 0, 1.30, 0)
        ax.text(1.22, -0.115, r'$\eta$', fontsize=11, ha='center', va='center')
        ax.text(0.02, 1.24, formula, fontsize=10, ha='center', va='bottom')

    ax = axes[0]
    frame(ax, r'$2a\eta t + 4B\eta^3$')
    e = np.linspace(-1.05, 1.18, 100)
    ax.plot(e, 0.40 * e + 0.16 * e ** 3, 'k-', lw=1.2, zorder=3)
    ax.text(0.48, -0.72, r'$t>0$', fontsize=10, ha='center', va='center')
    ax.text(0, -1.28, '(a)', fontsize=10, ha='center', va='center')

    ax = axes[1]
    frame(ax, r'$-2a\,|t|\,\eta + 4B\eta^3$')
    e = np.linspace(-1.32, 1.32, 200)
    ax.plot(e, -0.95 * e + 0.85 * e ** 3, 'k-', lw=1.2, zorder=3)
    ax.text(0.48, -0.72, r'$t<0$', fontsize=10, ha='center', va='center')
    ax.text(0, -1.28, '(b)', fontsize=10, ha='center', va='center')
    save(fig, 63)


# ---------------------------------------------------------------- 图64
def fig_64():
    """§144 图64：序参量对场 η(h)（a t>0 单值；b t<0 多值，虚线=亚稳/不稳段）"""
    fig, axes = plt.subplots(1, 2, figsize=(3.9, 2.0))

    # (a)
    ax = axes[0]
    plain_axes(ax)
    ax.set_xlim(-1.55, 1.62)
    ax.set_ylim(-1.62, 1.52)
    arrow_axis(ax, 0, -1.28, 0, 1.32)
    arrow_axis(ax, -1.22, 0, 1.32, 0)
    ax.text(-0.06, 1.30, r'$\eta$', fontsize=11, ha='right', va='center')
    ax.text(1.24, -0.12, r'$h$', fontsize=11, ha='center', va='center')
    x = np.linspace(-1.02, 1.02, 200)
    ax.plot(x, 0.82 * np.tanh(1.15 * x), 'k-', lw=1.2, zorder=3)
    ax.text(0.52, -0.88, r'$t>0$', fontsize=10, ha='center', va='center')
    ax.text(0, -1.48, '(a)', fontsize=10, ha='center', va='center')

    # (b)  曲线 h(η) = -η + η³，作 η(h)
    ax = axes[1]
    plain_axes(ax)
    ax.set_xlim(-1.42, 1.58)
    ax.set_ylim(-1.80, 1.62)

    hfun = lambda e: -e + e ** 3
    eA = 1 / np.sqrt(2)            # A 点（h=0, η>0）
    eD = 1.28
    # 实线：稳定段 D-A 与 A'-D'
    e1 = np.linspace(eA, eD, 60)
    ax.plot(hfun(e1), e1, 'k-', lw=1.2, zorder=3)
    e2 = np.linspace(-eD, -eA, 60)
    ax.plot(hfun(e2), e2, 'k-', lw=1.2, zorder=3)
    # 虚线：亚稳 A-B、不稳 B-B'（过原点）、B'-A'
    e3 = np.linspace(-eA, eA, 120)
    ax.plot(hfun(e3), e3, 'k-', lw=1.0, zorder=2.5, dashes=DASH_2ND)

    h_t = hfun(1 / np.sqrt(3))     # ±0.385
    e_s = 1.155                    # 稳定支上 h=±h_t 的 η
    # 两条竖直虚辅助线：B 到下支、上支到 B'（端点均落在曲线上）
    ax.plot([h_t, h_t], [1 / np.sqrt(3), -e_s], 'k-', lw=0.8, zorder=2,
            dashes=(2.2, 1.6))
    ax.plot([-h_t, -h_t], [e_s, -1 / np.sqrt(3)], 'k-', lw=0.8, zorder=2,
            dashes=(2.2, 1.6))

    arrow_axis(ax, 0, -1.52, 0, 1.42)
    arrow_axis(ax, -1.12, 0, 1.28, 0)
    ax.text(-0.05, 1.40, r'$\eta$', fontsize=11, ha='right', va='center')
    ax.text(1.20, -0.13, r'$h$', fontsize=11, ha='center', va='center')

    fs = 10
    ax.text(0.56, 1.24, r'$D$', fontsize=fs, ha='right', va='center')
    ax.text(-0.09, 0.775, r'$A$', fontsize=fs, ha='right', va='center')
    ax.text(-0.47, 0.60, r'$B$', fontsize=fs, ha='right', va='center')
    ax.text(0.07, 0.10, r'$O$', fontsize=fs, ha='left', va='center')
    ax.text(0.46, -0.61, r"$B'$", fontsize=fs, ha='left', va='center')
    ax.text(-0.09, -0.755, r"$A'$", fontsize=fs, ha='right', va='center')
    ax.text(-0.46, -1.37, r"$D'$", fontsize=fs, ha='center', va='center')
    ax.text(0.52, -1.42, r'$t<0$', fontsize=10, ha='center', va='center')
    ax.text(0, -1.66, '(b)', fontsize=10, ha='center', va='center')
    save(fig, 64)


# ---------------------------------------------------------------- 图65
def fig_65():
    """§145 图65：体立方合金 2x2x2 胞中的有序超晶格
    (a) 内立方 8 角均为 C，外格点黑白棋盘；(b) 全部格点黑白棋盘（A/B 交替）。"""
    fig, axes = plt.subplots(2, 1, figsize=(2.95, 4.55))
    d = np.array([0.42, 0.26])       # 每格深度平移（斜投影）

    def proj(p):
        return p[0] * np.array([1, 0]) + p[1] * d / 1.0 + p[2] * np.array([0, 1])

    # 注意：proj 输入 (i, j深度, k竖直) → 平面坐标 x=i+0.42j, y=0.26j+k
    def P(i, j, k):
        return np.array([i + 0.42 * j, 0.26 * j + k])

    def draw_panel(ax, inner_kind, outer_phase):
        plain_axes(ax)
        ax.set_xlim(-0.30, 2.95)
        ax.set_ylim(-0.84, 2.78)
        ax.set_aspect('equal')
        # 格线（三个方向各 9 条）
        lw = 0.95
        for j in range(3):
            for k in range(3):
                a, b = P(0, j, k), P(2, j, k)
                ax.plot([a[0], b[0]], [a[1], b[1]], 'k-', lw=lw, zorder=1.5)
        for i in range(3):
            for k in range(3):
                a, b = P(i, 0, k), P(i, 2, k)
                ax.plot([a[0], b[0]], [a[1], b[1]], 'k-', lw=lw, zorder=1.5)
        for i in range(3):
            for j in range(3):
                a, b = P(i, j, 0), P(i, j, 2)
                ax.plot([a[0], b[0]], [a[1], b[1]], 'k-', lw=lw, zorder=1.5)
        # 内立方（虚线，12 条棱）
        for ci in (0, 1):
            for cj in (0, 1):
                a, b = P(ci + .5, cj + .5, .5), P(ci + .5, cj + .5, 1.5)
                ax.plot([a[0], b[0]], [a[1], b[1]], 'k-', lw=0.8, zorder=1.4,
                        dashes=DASH_CUBE)
        for cj in (0, 1):
            for ck in (0, 1):
                a, b = P(.5, cj + .5, ck + .5), P(1.5, cj + .5, ck + .5)
                ax.plot([a[0], b[0]], [a[1], b[1]], 'k-', lw=0.8, zorder=1.4,
                        dashes=DASH_CUBE)
        for ci in (0, 1):
            for ck in (0, 1):
                a, b = P(ci + .5, .5, ck + .5), P(ci + .5, 1.5, ck + .5)
                ax.plot([a[0], b[0]], [a[1], b[1]], 'k-', lw=0.8, zorder=1.4,
                        dashes=DASH_CUBE)

        def open_c(p, r=0.058):
            ax.add_patch(plt.Circle(p, r, facecolor='white', edgecolor='k',
                                    lw=1.0, zorder=3))

        def fill_c(p, r=0.030):
            ax.add_patch(plt.Circle(p, r, facecolor='k', edgecolor='k',
                                    lw=0.6, zorder=3))

        def C_c(p):
            ax.add_patch(plt.Circle(p, 0.062, facecolor='white', edgecolor='k',
                                    lw=1.0, zorder=3))
            ax.add_patch(plt.Circle(p, 0.030, facecolor='k', edgecolor='k',
                                    lw=0.6, zorder=3.1))

        # 外层 27 点（按深度从后往前画）
        atoms = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    par = (i + j + k) % 2
                    kind = 'O' if par == outer_phase else 'B'
                    atoms.append((j, P(i, j, k), kind))
        # 内层 8 点
        for ci in range(2):
            for cj in range(2):
                for ck in range(2):
                    if inner_kind == 'C':
                        kind = 'C'
                    else:
                        par = (ci + cj + ck) % 2 == 0
                        kind = 'O' if par else 'B'
                    atoms.append((cj + 0.5, P(ci + .5, cj + .5, ck + .5), kind))
        for _, p, kind in sorted(atoms, key=lambda t: -t[0]):
            if kind == 'O':
                open_c(p)
            elif kind == 'B':
                fill_c(p)
            else:
                C_c(p)

    # (a)：内 8 点全 C；外层棋盘取 (i+j+k) 偶 -> ○
    draw_panel(axes[0], 'C', 0)
    axes[0].text(1.32, -0.55, '(a)', fontsize=10, ha='center', va='center')
    # (b)：全棋盘；内层 (ci+cj+ck) 偶 -> ○；外层相位相反
    draw_panel(axes[1], 'AB', 1)
    axes[1].text(1.32, -0.44, '(b)', fontsize=10, ha='center', va='center')
    # 图例（居中于面板下方）
    y0 = -0.78
    ax = axes[1]
    ax.add_patch(plt.Circle((0.78, y0), 0.040, facecolor='white',
                            edgecolor='k', lw=1.0, zorder=3))
    ax.text(0.89, y0, r'$A$', fontsize=10, ha='left', va='center')
    ax.add_patch(plt.Circle((1.42, y0), 0.028, facecolor='k', edgecolor='k',
                            lw=0.6, zorder=3))
    ax.text(1.52, y0, r'$B$', fontsize=10, ha='left', va='center')
    ax.add_patch(plt.Circle((2.02, y0), 0.048, facecolor='white',
                            edgecolor='k', lw=1.0, zorder=3))
    ax.add_patch(plt.Circle((2.02, y0), 0.024, facecolor='k', edgecolor='k',
                            lw=0.6, zorder=3.1))
    ax.text(2.14, y0, r'$C$', fontsize=10, ha='left', va='center')
    save(fig, 65)


# ---------------------------------------------------------------- 图66
def fig_66():
    """§150 图66：二级相变线在 K 点跨入一级相变线（实线一级、虚线二级）"""
    fig, ax = plt.subplots(figsize=(2.3, 2.1))
    plain_axes(ax)
    ax.set_xlim(-0.10, 1.60)
    ax.set_ylim(-0.16, 1.52)

    arrow_axis(ax, 0, 0, 0, 1.44)
    arrow_axis(ax, 0, 0, 1.52, 0)
    ax.text(-0.055, 1.42, r'$P$', fontsize=11, ha='right', va='center')
    ax.text(1.44, -0.115, r'$T$', fontsize=11, ha='center', va='center')

    K = (0.66, 0.70)
    ax.plot([0.44, K[0]], [0.30, K[1]], 'k-', lw=1.2, zorder=3)
    dd = catmull([K, (0.84, 0.90), (1.10, 1.10)])
    ax.plot(dd[:, 0], dd[:, 1], 'k-', lw=1.2, zorder=3, dashes=DASH_2ND)
    ax.text(0.585, 0.635, r'$K$', fontsize=11, ha='right', va='center')
    save(fig, 66)


# ---------------------------------------------------------------- 图67
def fig_67():
    """§150 图67：二级相变线 AC（虚）与一级相变线 BD（实）相交于 B（双临界点）"""
    fig, ax = plt.subplots(figsize=(2.45, 2.3))
    plain_axes(ax)
    ax.set_xlim(0, 1.10)
    ax.set_ylim(-0.08, 1.10)

    ac = catmull([(0.80, 0.99), (0.63, 0.76), (0.47, 0.51),
                  (0.39, 0.26), (0.32, 0.02)])
    ax.plot(ac[:, 0], ac[:, 1], 'k-', lw=1.2, zorder=3, dashes=DASH_2ND)
    bd = catmull([(0.47, 0.51), (0.60, 0.40), (0.75, 0.25), (0.95, 0.02)])
    ax.plot(bd[:, 0], bd[:, 1], 'k-', lw=1.2, zorder=3)

    fs = 11
    ax.text(0.765, 0.985, r'$A$', fontsize=fs, ha='right', va='center')
    ax.text(0.435, 0.525, r'$B$', fontsize=fs, ha='right', va='center')
    ax.text(0.285, 0.03, r'$C$', fontsize=fs, ha='right', va='center')
    ax.text(0.975, 0.03, r'$D$', fontsize=fs, ha='left', va='center')
    fr = 10.5
    ax.text(0.31, 0.80, r'$\mathrm{I}$', fontsize=fr, ha='center', va='center')
    ax.text(0.88, 0.54, r'$\mathrm{II}$', fontsize=fr, ha='center', va='center')
    ax.text(0.63, 0.14, r'$\mathrm{III}$', fontsize=fr, ha='center', va='center')
    save(fig, 67)


# ---------------------------------------------------------------- 图68
def fig_68():
    """§150 图68：几条二级相变线（虚线）相交于一点（四相 I II III IV）"""
    fig, ax = plt.subplots(figsize=(2.45, 2.3))
    plain_axes(ax)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(-0.06, 1.06)

    c1 = catmull([(0.15, 0.96), (0.31, 0.81), (0.45, 0.64), (0.55, 0.50),
                  (0.64, 0.35), (0.75, 0.17), (0.83, 0.03)])
    ax.plot(c1[:, 0], c1[:, 1], 'k-', lw=1.2, zorder=3, dashes=DASH_2ND)
    c2 = catmull([(0.02, 0.20), (0.20, 0.30), (0.38, 0.42), (0.55, 0.50),
                  (0.72, 0.63), (0.88, 0.82), (0.97, 1.00)])
    ax.plot(c2[:, 0], c2[:, 1], 'k-', lw=1.2, zorder=3, dashes=DASH_2ND)

    fr = 10.5
    ax.text(0.57, 0.87, r'$\mathrm{I}$', fontsize=fr, ha='center', va='center')
    ax.text(0.16, 0.60, r'$\mathrm{II}$', fontsize=fr, ha='center', va='center')
    ax.text(0.94, 0.53, r'$\mathrm{III}$', fontsize=fr, ha='center', va='center')
    ax.text(0.46, 0.24, r'$\mathrm{IV}$', fontsize=fr, ha='center', va='center')
    save(fig, 68)


# ---------------------------------------------------------------- 图69
def fig_69():
    """§150 图69：孤立连续相变点 O (a) 三相交界 (b) 两一级线相切+一支线"""
    fig, axes = plt.subplots(1, 2, figsize=(3.35, 1.8))

    # (a)
    ax = axes[0]
    plain_axes(ax)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(-0.16, 1.05)
    main = catmull([(0.09, 0.93), (0.30, 0.82), (0.52, 0.69), (0.72, 0.50),
                    (0.88, 0.24)])
    ax.plot(main[:, 0], main[:, 1], 'k-', lw=1.2, zorder=3)
    br = catmull([(0.52, 0.69), (0.44, 0.49), (0.32, 0.24), (0.24, 0.06)])
    ax.plot(br[:, 0], br[:, 1], 'k-', lw=1.2, zorder=3)
    ax.text(0.555, 0.73, r'$O$', fontsize=10.5, ha='left', va='center')
    ax.text(0.72, 0.89, r'$\mathrm{I}$', fontsize=10.5, ha='center', va='center')
    ax.text(0.24, 0.52, r'$\mathrm{II}$', fontsize=10.5, ha='center', va='center')
    ax.text(0.55, 0.33, r'$\mathrm{III}$', fontsize=10.5, ha='center', va='center')
    ax.text(0.46, -0.11, '(a)', fontsize=10, ha='center', va='center')

    # (b)
    ax = axes[1]
    plain_axes(ax)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(-0.16, 1.05)
    c1 = catmull([(0.21, 0.92), (0.35, 0.78), (0.49, 0.63), (0.60, 0.44),
                  (0.71, 0.17)])
    ax.plot(c1[:, 0], c1[:, 1], 'k-', lw=1.2, zorder=3)
    c2 = catmull([(0.16, 0.72), (0.33, 0.665), (0.49, 0.63), (0.66, 0.52),
                  (0.86, 0.35)])
    ax.plot(c2[:, 0], c2[:, 1], 'k-', lw=1.2, zorder=3)
    c3 = catmull([(0.03, 0.0), (0.20, 0.25), (0.36, 0.47), (0.49, 0.63)])
    ax.plot(c3[:, 0], c3[:, 1], 'k-', lw=1.2, zorder=3)
    ax.text(0.525, 0.685, r'$O$', fontsize=10.5, ha='left', va='center')
    fr = 10.5
    ax.text(0.155, 0.955, r'$\mathrm{II}$', fontsize=fr, ha='center', va='center')
    ax.text(0.74, 0.79, r'$\mathrm{I}$', fontsize=fr, ha='center', va='center')
    ax.text(0.23, 0.49, r'$\mathrm{IV}$', fontsize=fr, ha='center', va='center')
    ax.text(0.44, 0.21, r'$\mathrm{V}$', fontsize=fr, ha='center', va='center')
    ax.text(0.82, 0.13, r'$\mathrm{III}$', fontsize=fr, ha='center', va='center')
    ax.text(0.50, -0.11, '(b)', fontsize=10, ha='center', va='center')
    save(fig, 69)


# ---------------------------------------------------------------- 图70
def fig_70():
    """§150 习题 图70：栗弗希兹点 L——二级线（虚）与一级线（实）分岔"""
    fig, ax = plt.subplots(figsize=(2.85, 2.05))
    plain_axes(ax)
    ax.set_xlim(-0.10, 1.80)
    ax.set_ylim(-0.20, 1.44)

    arrow_axis(ax, 0, 0, 0, 1.36)
    arrow_axis(ax, 0, 0, 1.72, 0)
    ax.text(0.055, 1.34, r'$T$', fontsize=11, ha='left', va='center')
    ax.text(1.63, -0.125, r'$P$', fontsize=11, ha='center', va='center')

    L = (0.94, 0.72)
    dd = catmull([(0.22, 1.03), (0.50, 0.945), (0.72, 0.855), L,
                  (1.15, 0.665), (1.30, 0.655), (1.50, 0.70)])
    ax.plot(dd[:, 0], dd[:, 1], 'k-', lw=1.2, zorder=3, dashes=DASH_2ND)
    so = catmull([L, (1.08, 0.55), (1.20, 0.40), (1.32, 0.27)])
    ax.plot(so[:, 0], so[:, 1], 'k-', lw=1.2, zorder=3)
    ax.add_patch(plt.Circle(L, 0.030, facecolor='white', edgecolor='k',
                            lw=1.1, zorder=4))

    ax.text(0.86, 0.575, r'$L$', fontsize=11, ha='center', va='center')
    ax.text(0.86, 0.96, r'$\mathrm{I}$', fontsize=10.5, ha='center', va='center')
    ax.text(0.33, 0.53, r'$\mathrm{II}$', fontsize=10.5, ha='center', va='center')
    ax.text(1.40, 0.52, r'$\mathrm{III}$', fontsize=10.5, ha='center', va='center')
    save(fig, 70)


if __name__ == '__main__':
    for f in (fig_60, fig_61, fig_62, fig_63, fig_64, fig_65,
              fig_66, fig_67, fig_68, fig_69, fig_70):
        f()
        print(f.__name__, 'ok')
