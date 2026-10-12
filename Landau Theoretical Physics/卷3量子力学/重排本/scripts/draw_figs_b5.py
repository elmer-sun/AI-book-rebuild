# -*- coding: utf-8 -*-
"""
朗道《量子力学》（卷3）中文重排本插图重绘 —— 第五批（最后一批）：图41–图51
图41 §100 NH3 三角锥（等边三角锥，N 顶点，3H 底角）   (原书 p364 / PDF p377)
图42 §100 H2O 三个简正振动 + 平衡位形（四面板）       (原书 p365 / PDF p378)
图43 §100 分子位形七面板 CHCl3/CH4/C6H6/OsF8/UF6/C2H6/C2H4 (p366 / PDF p379)
图44 §105 NH3 两个反演位形（镜面反射）                (p389 / PDF p402)
图45 §108 6j 符号：不规则四面体 6 棱 j1..j6            (p403 / PDF p416)
图46 §129 色散关系 E' 复平面钥匙孔围道                 (p486 / PDF p499)
图47 §129 实轴积分从下方绕过 E=E' 极点                 (p486 / PDF p499)
图48 §130 q 复平面极点绕行 (a)与上半平面直线+封闭圈 (b) (p488 / PDF p501)
图49 §138 函数 h(x)=Re psi(i/x)+ln x 网格曲线          (p525 / PDF p538)
图50 §147 反应阈附近 dσ/dE 四种行为 (a)-(d)            (p562 / PDF p575)
图51 §147 阈下共振：σe 在 0 与 4π/ka² 之间振荡         (p565 / PDF p578)
统一黑白教材风；输出 figures/figN.pdf + figures/preview/figN.png
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

LW_MAIN = 1.2      # 主体线
LW_AUX = 0.8       # 辅助线
FS = 9             # 基准字号


def save(fig, n):
    for ext, path in (('pdf', os.path.join(FIGDIR, 'fig%d.pdf' % n)),
                      ('png', os.path.join(PREVDIR, 'fig%d.png' % n))):
        fig.savefig(path, bbox_inches='tight', pad_inches=0.03, dpi=300)
    plt.close(fig)
    print('fig%d done' % n)


def bare_axes(fig, rect, xlim, ylim):
    """无框、等比、全隐 spines 的子坐标系。"""
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    return ax


def arrow(ax, x0, y0, x1, y1, lw=0.9, ms=7):
    """自绘黑色箭头（-|> 实心头）。"""
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k',
                                lw=lw, mutation_scale=ms))


def circ_dot(ax, x, y, ms=4.6):
    """实心原子点（H 等），ms 为 markersize（pt，直径）。"""
    ax.plot([x], [y], 'ko', markersize=ms, zorder=5)


def circ_open(ax, x, y, ms=5.2, lw=1.0):
    """空心原子圈（N、O、C 等）。"""
    ax.plot([x], [y], 'o', ms=ms, mfc='white', mec='k', mew=lw, zorder=5)


def seg(ax, pts, lw=LW_MAIN, ls='-'):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax.plot(xs, ys, ls=ls, lw=lw, color='k')


# =====================================================================
# 图 41  NH3 三角锥
# =====================================================================
def fig_41():
    fig = plt.figure(figsize=(2.4, 1.5))
    ax = bare_axes(fig, [0, 0, 1, 1], (-1.5, 1.5), (-0.9, 0.85))
    Hl, Hr, Hb = (-1.15, 0.0), (1.15, 0.0), (-0.16, -0.58)
    N = (0.0, 0.45)
    # 棱：N 到三个 H（可见，实线）
    seg(ax, [N, Hl]); seg(ax, [N, Hr]); seg(ax, [N, Hb])
    # 底边两条可见棱
    seg(ax, [Hl, Hb]); seg(ax, [Hb, Hr])
    # 被遮住的底边（虚线）
    seg(ax, [Hl, Hr], lw=LW_AUX, ls=(0, (5, 4)))
    # 锥体的高：N 垂直向下到虚线底边，端点带小横标
    seg(ax, [N, (0.0, -0.02)], lw=LW_AUX, ls=(0, (4, 3)))
    seg(ax, [(-0.07, 0.0), (0.07, 0.0)], lw=LW_AUX)
    # 原子
    circ_open(ax, *N, ms=5.6)
    for P in (Hl, Hr, Hb):
        circ_dot(ax, *P, ms=4.6)
    # 标注
    ax.text(N[0], N[1] + 0.13, r'$\mathrm{N}$', ha='center', va='bottom', fontsize=FS + 1)
    ax.text(Hl[0] - 0.12, Hl[1], r'$\mathrm{H}$', ha='right', va='center', fontsize=FS + 1)
    ax.text(Hr[0] + 0.12, Hr[1], r'$\mathrm{H}$', ha='left', va='center', fontsize=FS + 1)
    ax.text(Hb[0], Hb[1] - 0.12, r'$\mathrm{H}$', ha='center', va='top', fontsize=FS + 1)
    save(fig, 41)


# =====================================================================
# 图 42  H2O 三个简正振动 + 平衡位形（四面板）
# =====================================================================
def _h2o_tri(ax, ox):
    """画一个 H2O 骨架：O 空心圈在顶点，两个 H 实心点在底角。返回三原子坐标。"""
    O = (ox + 0.0, 0.62); Hl = (ox - 0.52, 0.0); Hr = (ox + 0.52, 0.0)
    seg(ax, [O, Hl]); seg(ax, [O, Hr]); seg(ax, [Hl, Hr])
    circ_open(ax, *O, ms=5.0)
    circ_dot(ax, *Hl, ms=4.2); circ_dot(ax, *Hr, ms=4.2)
    return O, Hl, Hr


def fig_42():
    fig = plt.figure(figsize=(3.45, 1.25))
    ax = bare_axes(fig, [0, 0, 1, 1], (0, 8.0), (-0.62, 1.55))
    # 面板 1：A1 全对称伸缩 —— O 向上，两 H 向下外
    O, Hl, Hr = _h2o_tri(ax, 0.72)
    arrow(ax, O[0], O[1] + 0.07, O[0], O[1] + 0.60)
    arrow(ax, Hl[0] - 0.04, Hl[1] - 0.04, Hl[0] - 0.36, Hl[1] - 0.42)
    arrow(ax, Hr[0] + 0.04, Hr[1] - 0.04, Hr[0] + 0.36, Hr[1] - 0.42)
    ax.text(1.44, 0.34, r'$A_1$', ha='left', va='center', fontsize=FS)
    # 面板 2：A1 全对称弯曲 —— O 向下，两 H 向上外
    O, Hl, Hr = _h2o_tri(ax, 2.98)
    arrow(ax, O[0], O[1] - 0.07, O[0], O[1] - 0.50)
    arrow(ax, Hl[0] - 0.04, Hl[1] + 0.04, Hl[0] - 0.36, Hl[1] + 0.44)
    arrow(ax, Hr[0] + 0.04, Hr[1] + 0.04, Hr[0] + 0.36, Hr[1] + 0.44)
    ax.text(3.72, 0.78, r'$A_1$', ha='left', va='center', fontsize=FS)
    # 面板 3：B1 非对称 —— O 向右，左 H 向下外，右 H 沿键向下外
    O, Hl, Hr = _h2o_tri(ax, 5.24)
    arrow(ax, O[0] + 0.07, O[1] + 0.01, O[0] + 0.52, O[1] + 0.03)
    arrow(ax, Hl[0] - 0.04, Hl[1] + 0.04, Hl[0] - 0.38, Hl[1] - 0.36)
    arrow(ax, Hr[0] + 0.045, Hr[1] - 0.045, Hr[0] + 0.30, Hr[1] - 0.35)
    ax.text(5.98, 0.78, r'$B_1$', ha='left', va='center', fontsize=FS)
    # 面板 4：平衡位形，带 O/H 标注
    O, Hl, Hr = _h2o_tri(ax, 7.50)
    ax.text(O[0], O[1] + 0.10, r'$\mathrm{O}$', ha='center', va='bottom', fontsize=FS + 1)
    ax.text(Hl[0] - 0.10, Hl[1], r'$\mathrm{H}$', ha='right', va='center', fontsize=FS + 1)
    ax.text(Hr[0] + 0.10, Hr[1], r'$\mathrm{H}$', ha='left', va='center', fontsize=FS + 1)
    save(fig, 42)


# =====================================================================
# 图 43  七面板分子位形 (a)CHCl3 (b)CH4 (c)C6H6 (d)OsF8 (e)UF6 (f)C2H6 (g)C2H4
# =====================================================================
def fig_43():
    fig = plt.figure(figsize=(4.35, 4.75))
    ax = bare_axes(fig, [0, 0, 1, 1], (-0.6, 10.0), (-0.6, 9.9))
    MSD, MSO = 4.4, 5.0   # 实心点 / 空心圈 的 markersize（pt）

    # ---------- (a) CHCl3：C 中心，Cl 上（⊗），三个 H 下 ----------
    ox, oy = 0.0, 8.0
    C = (ox, oy); Cl = (ox, oy + 1.05)
    H1 = (ox - 0.72, oy - 0.62); H2 = (ox, oy - 0.78); H3 = (ox + 0.72, oy - 0.62)
    seg(ax, [C, Cl]); seg(ax, [C, H1]); seg(ax, [C, H2]); seg(ax, [C, H3])
    circ_open(ax, *C, ms=MSO)
    # Cl：⊗（空心圈加叉）
    circ_open(ax, *Cl, ms=9, lw=1.0)
    ax.plot([Cl[0] - 0.065, Cl[0] + 0.065], [Cl[1] - 0.065, Cl[1] + 0.065],
            'k-', lw=0.9, zorder=6)
    ax.plot([Cl[0] - 0.065, Cl[0] + 0.065], [Cl[1] + 0.065, Cl[1] - 0.065],
            'k-', lw=0.9, zorder=6)
    for P in (H1, H2, H3):
        circ_dot(ax, *P, ms=MSD)
    ax.text(Cl[0], Cl[1] + 0.16, r'$\mathrm{Cl}$', ha='center', va='bottom', fontsize=FS + 1)
    ax.text(C[0] - 0.14, C[1] + 0.07, r'$\mathrm{C}$', ha='right', va='center', fontsize=FS + 1)
    for P in (H1, H2, H3):
        ax.text(P[0], P[1] - 0.13, r'$\mathrm{H}$', ha='center', va='top', fontsize=FS + 1)
    ax.text(ox, oy - 1.15, '(a)', ha='center', va='top', fontsize=FS)

    # ---------- (b) CH4：底面三角形三 H，C 在中央，近处一个 H ----------
    ox, oy = 2.35, 8.3
    T = (ox + 0.10, oy + 1.0)          # 顶 H（实心）
    BL = (ox - 0.72, oy - 0.38)        # 左下 H（实心）
    BR = (ox + 0.88, oy - 0.44)        # 右下 H（空心）
    Cc = (ox - 0.02, oy + 0.28)        # C（空心）
    Hn = (ox + 0.30, oy + 0.20)        # 近处 H（实心）
    seg(ax, [T, BL]); seg(ax, [BL, BR]); seg(ax, [BR, T])       # 底面三角形
    seg(ax, [T, Hn]); seg(ax, [BL, Hn]); seg(ax, [BR, Hn])      # 近 H 的三条棱
    seg(ax, [Cc, Hn], lw=1.0)                                    # C–H 键
    seg(ax, [T, (ox + 0.04, oy + 0.06)], lw=LW_AUX, ls=(0, (4, 3)))  # 过 C 的竖直虚线
    circ_open(ax, *Cc, ms=MSO)
    circ_dot(ax, *T, ms=MSD); circ_dot(ax, *BL, ms=MSD); circ_dot(ax, *Hn, ms=MSD)
    circ_open(ax, *BR, ms=MSO)
    ax.text(T[0], T[1] + 0.13, r'$\mathrm{H}$', ha='center', va='bottom', fontsize=FS + 1)
    ax.text(BL[0] - 0.09, BL[1] - 0.10, r'$\mathrm{H}$', ha='center', va='top', fontsize=FS + 1)
    ax.text(BR[0] + 0.03, BR[1] - 0.12, r'$\mathrm{H}$', ha='center', va='top', fontsize=FS + 1)
    ax.text(Cc[0] - 0.15, Cc[1], r'$\mathrm{C}$', ha='right', va='center', fontsize=FS + 1)
    ax.text(Hn[0] + 0.13, Hn[1] - 0.19, r'$\mathrm{H}$', ha='left', va='center', fontsize=FS + 1)
    ax.text(ox, oy - 0.95, '(b)', ha='center', va='top', fontsize=FS)

    # ---------- (c) C6H6：六角环 + 六个 H ----------
    ox, oy = 5.55, 8.25
    R = 0.60
    hexv = [(ox + R * np.cos(a), oy + R * np.sin(a))
            for a in np.deg2rad([0, 60, 120, 180, 240, 300])]
    for i in range(6):
        seg(ax, [hexv[i], hexv[(i + 1) % 6]])
    for i, P in enumerate(hexv):
        circ_open(ax, *P, ms=4.4, lw=0.9)
        # C 标注：环内侧
        dx, dy = ox - P[0], oy - P[1]
        n = np.hypot(dx, dy)
        ax.text(P[0] + 0.26 * dx / n, P[1] + 0.26 * dy / n,
                r'$\mathrm{C}$', ha='center', va='center', fontsize=FS + 1)
        # 键 + H
        ux, uy = -dx / n, -dy / n
        Q = (P[0] + 0.44 * ux, P[1] + 0.44 * uy)
        seg(ax, [P, Q], lw=1.1)
        circ_dot(ax, *Q, ms=MSD)
        ax.text(Q[0] + 0.15 * ux, Q[1] + 0.16 * uy,
                r'$\mathrm{H}$', ha='center', va='center', fontsize=FS + 1)
    ax.text(ox, oy - 1.28, '(c)', ha='center', va='top', fontsize=FS)

    # ---------- (d) OsF8：立方体，Os 在中心 ----------
    ox, oy = 0.0, 4.3
    a, d = 0.75, 0.30
    F = {}
    for name, (u, v) in dict(A=(0, 0), B=(a, 0), Cc=(a, a), D=(0, a),
                             A2=(d, d), B2=(a + d, d), C2=(a + d, a + d),
                             D2=(d, a + d)).items():
        F[name] = (ox + u, oy + v)
    edges = [('A', 'B'), ('B', 'Cc'), ('Cc', 'D'), ('D', 'A'),
             ('A2', 'B2'), ('B2', 'C2'), ('C2', 'D2'), ('D2', 'A2'),
             ('A', 'A2'), ('B', 'B2'), ('Cc', 'C2'), ('D', 'D2')]
    for u, v in edges:
        seg(ax, [F[u], F[v]], lw=1.0)
    for P in F.values():
        circ_dot(ax, *P, ms=MSD)
    Oc = (ox + (a + d) / 2, oy + (a + d) / 2)
    circ_open(ax, *Oc, ms=4.8)
    ax.text(Oc[0] - 0.02, Oc[1] + 0.12, r'$\mathrm{Os}$', ha='center', va='bottom', fontsize=FS + 1)
    lab = [('D', (-0.15, 0.10), 'right'), ('D2', (0.0, 0.16), 'center'),
           ('C2', (0.15, 0.10), 'left'), ('Cc', (0.16, 0.02), 'left'),
           ('A', (-0.15, -0.10), 'right'), ('A2', (0.0, -0.16), 'center'),
           ('B2', (0.15, -0.10), 'left'), ('B', (0.15, -0.09), 'left')]
    for k, dxy, ha in lab:
        ax.text(F[k][0] + dxy[0], F[k][1] + dxy[1], r'$\mathrm{F}$',
                ha=ha, va='center', fontsize=FS + 1)
    ax.text(ox + a / 2, oy - 0.32, '(d)', ha='center', va='top', fontsize=FS)

    # ---------- (e) UF6：八面体，U 在中心 ----------
    ox, oy = 2.45, 4.35
    T = (ox + 0.10, oy + 1.18); Bo = (ox + 0.10, oy - 1.12)
    L = (ox - 0.72, oy + 0.05); R = (ox + 1.02, oy - 0.02)
    Ff = (ox - 0.08, oy - 0.22); Fb = (ox + 0.55, oy + 0.16)
    for P, Q in [(T, L), (T, Ff), (T, R), (L, Ff), (Ff, R),
                 (L, Bo), (Ff, Bo), (R, Bo)]:
        seg(ax, [P, Q])
    for P, Q in [(T, Fb), (L, Fb), (Fb, R), (Fb, Bo)]:
        seg(ax, [P, Q], lw=LW_AUX, ls=(0, (5, 4)))
    for P in (T, Bo, L, R, Ff, Fb):
        circ_open(ax, *P, ms=MSO)
    U = (ox + 0.24, oy + 0.02)
    circ_dot(ax, *U, ms=4.6)
    ax.text(T[0], T[1] + 0.13, r'$\mathrm{F}$', ha='center', va='bottom', fontsize=FS + 1)
    ax.text(Bo[0], Bo[1] - 0.13, r'$\mathrm{F}$', ha='center', va='top', fontsize=FS + 1)
    ax.text(L[0] - 0.12, L[1], r'$\mathrm{F}$', ha='right', va='center', fontsize=FS + 1)
    ax.text(R[0] + 0.12, R[1], r'$\mathrm{F}$', ha='left', va='center', fontsize=FS + 1)
    ax.text(Ff[0] - 0.14, Ff[1] - 0.14, r'$\mathrm{F}$', ha='center', va='top', fontsize=FS + 1)
    ax.text(Fb[0] - 0.11, Fb[1] + 0.11, r'$\mathrm{F}$', ha='center', va='bottom', fontsize=FS + 1)
    ax.text(U[0] + 0.10, U[1] - 0.01, r'$\mathrm{U}$', ha='left', va='center', fontsize=FS + 1)
    ax.text(ox + 0.1, oy - 1.58, '(e)', ha='center', va='top', fontsize=FS)

    # ---------- (f) C2H6：交错乙烷侧视 ----------
    ox, oy = 4.35, 4.3
    C1 = (ox + 0.10, oy + 0.85); C2 = (ox + 0.12, oy - 0.45)
    seg(ax, [C1, C2])
    circ_open(ax, *C1, ms=MSO); circ_open(ax, *C2, ms=MSO)
    ax.text(C1[0] + 0.14, C1[1] - 0.11, r'$\mathrm{C}$', ha='left', va='center', fontsize=FS + 1)
    ax.text(C2[0] + 0.14, C2[1] + 0.03, r'$\mathrm{C}$', ha='left', va='center', fontsize=FS + 1)
    # 上面三个 H
    ht = [(ox - 0.30, oy + 1.18), (ox + 0.72, oy + 1.62), (ox + 0.86, oy + 0.98)]
    # 下面三个 H
    hb = [(ox - 0.35, oy - 0.62), (ox - 0.50, oy - 1.28), (ox + 0.80, oy - 0.88)]
    for P in ht:
        seg(ax, [C1, P], lw=1.1); circ_dot(ax, *P, ms=MSD)
    for P in hb:
        seg(ax, [C2, P], lw=1.1); circ_dot(ax, *P, ms=MSD)
    ax.text(ht[0][0] - 0.04, ht[0][1] + 0.12, r'$\mathrm{H}$', ha='center', va='bottom', fontsize=FS + 1)
    ax.text(ht[1][0] + 0.13, ht[1][1], r'$\mathrm{H}$', ha='left', va='center', fontsize=FS + 1)
    ax.text(ht[2][0] + 0.13, ht[2][1], r'$\mathrm{H}$', ha='left', va='center', fontsize=FS + 1)
    ax.text(hb[0][0] - 0.13, hb[0][1], r'$\mathrm{H}$', ha='right', va='center', fontsize=FS + 1)
    ax.text(hb[1][0] - 0.13, hb[1][1] - 0.02, r'$\mathrm{H}$', ha='right', va='center', fontsize=FS + 1)
    ax.text(hb[2][0] + 0.03, hb[2][1] - 0.13, r'$\mathrm{H}$', ha='center', va='top', fontsize=FS + 1)
    # 虚线：从左上 H 竖直向下，再水平折到右下 H
    seg(ax, [ht[0], (ox - 0.26, oy - 0.86)], lw=LW_AUX, ls=(0, (5, 4)))
    seg(ax, [(ox - 0.26, oy - 0.86), hb[2]], lw=LW_AUX, ls=(0, (5, 4)))
    ax.text(ox + 0.1, oy - 1.62, '(f)', ha='center', va='top', fontsize=FS)

    # ---------- (g) C2H4：平面乙烯 + x, y 轴 ----------
    ox, oy = 1.35, 0.75
    C1 = (ox, oy); C2 = (ox + 1.35, oy)
    seg(ax, [C1, C2])
    H = [(ox - 0.68, oy + 0.66), (ox - 0.68, oy - 0.66),
         (ox + 2.03, oy + 0.66), (ox + 2.03, oy - 0.66)]
    seg(ax, [C1, H[0]]); seg(ax, [C1, H[1]])
    seg(ax, [C2, H[2]]); seg(ax, [C2, H[3]])
    ax.text(C1[0] + 0.16, C1[1] + 0.12, r'$\mathrm{C}$', ha='left', va='center', fontsize=FS + 1)
    ax.text(C2[0] - 0.16, C2[1] + 0.12, r'$\mathrm{C}$', ha='right', va='center', fontsize=FS + 1)
    ax.text(H[0][0] - 0.06, H[0][1] + 0.08, r'$\mathrm{H}$', ha='center', va='bottom', fontsize=FS + 1)
    ax.text(H[1][0] - 0.06, H[1][1] - 0.08, r'$\mathrm{H}$', ha='center', va='top', fontsize=FS + 1)
    ax.text(H[2][0] + 0.06, H[2][1] + 0.08, r'$\mathrm{H}$', ha='center', va='bottom', fontsize=FS + 1)
    ax.text(H[3][0] + 0.06, H[3][1] - 0.08, r'$\mathrm{H}$', ha='center', va='top', fontsize=FS + 1)
    # y 轴（竖直虚线，由 C=C 中点向上）与 x 轴（由右 C 向右）
    seg(ax, [(ox + 0.675, oy), (ox + 0.675, oy + 1.05)], lw=LW_AUX, ls=(0, (5, 4)))
    ax.text(ox + 0.675, oy + 1.16, r'$y$', ha='center', va='bottom', fontsize=FS + 1)
    seg(ax, [(C2[0], C2[1]), (ox + 2.45, oy)], lw=LW_AUX, ls=(0, (5, 4)))
    ax.text(ox + 2.56, oy, r'$x$', ha='left', va='center', fontsize=FS + 1)
    ax.text(ox + 0.675, oy - 0.92, '(g)', ha='center', va='top', fontsize=FS)
    save(fig, 43)


# =====================================================================
# 图 44  NH3 两个反演位形（对平行于底面的平面反射互得）
# =====================================================================
def _nh3_flat(ax, oy, flip):
    """扁平三角锥：flip=+1 N 在上；flip=-1 N 在下。"""
    s = flip
    Hl = (-1.45, oy); Hr = (1.45, oy)
    Hm = (-0.42, oy + 0.21 * s)
    N = (-0.12, oy + 0.44 * s)
    seg(ax, [Hl, Hr])                      # 底边（压扁的 H3 三角形底棱）
    seg(ax, [Hl, Hm]); seg(ax, [Hm, Hr])   # 底面另两条棱
    seg(ax, [Hl, N]); seg(ax, [Hr, N]); seg(ax, [N, Hm])
    seg(ax, [N, (-0.14, oy + 0.02 * s)], lw=LW_AUX, ls=(0, (4, 3)))  # 高（虚线）
    circ_open(ax, *N, ms=4.8); circ_open(ax, *Hl, ms=4.4)
    circ_open(ax, *Hr, ms=4.4); circ_open(ax, *Hm, ms=4.4)
    ax.text(N[0] + 0.02, N[1] + 0.13 * s, r'$\mathrm{N}$',
            ha='center', va='bottom' if s > 0 else 'top', fontsize=FS + 1)
    ax.text(Hl[0] - 0.11, Hl[1], r'$\mathrm{H}$', ha='right', va='center', fontsize=FS + 1)
    ax.text(Hr[0] + 0.11, Hr[1], r'$\mathrm{H}$', ha='left', va='center', fontsize=FS + 1)
    ax.text(Hm[0] - 0.15, Hm[1] - 0.07 * s, r'$\mathrm{H}$',
            ha='right', va='center', fontsize=FS + 1)


def fig_44():
    fig = plt.figure(figsize=(2.75, 1.62))
    ax = bare_axes(fig, [0, 0, 1, 1], (-1.90, 1.90), (-1.0, 1.0))
    _nh3_flat(ax, 0.26, +1)     # N 在上
    seg(ax, [(-1.74, 0.0), (1.74, 0.0)], lw=1.0)   # 反射平面
    _nh3_flat(ax, -0.26, -1)    # N 在下
    save(fig, 44)


# =====================================================================
# 图 45  6j 符号：不规则四面体的 6 条棱
# =====================================================================
def fig_45():
    fig = plt.figure(figsize=(1.75, 2.05))
    ax = bare_axes(fig, [0, 0, 1, 1], (-0.25, 1.32), (-1.18, 0.72))
    T = (0.77, 0.42); L = (0.0, 0.0); R = (1.0, 0.02); B = (0.35, -0.90)
    seg(ax, [T, L]); seg(ax, [T, R]); seg(ax, [L, R])
    seg(ax, [L, B]); seg(ax, [R, B])
    seg(ax, [T, B], lw=LW_AUX, ls=(0, (5, 4)))
    ax.text(0.40, 0.32, r'$\boldsymbol{j}_1$', ha='center', va='center', fontsize=FS)
    ax.text(1.10, 0.34, r'$\boldsymbol{j}_2$', ha='center', va='center', fontsize=FS)
    ax.text(0.35, -0.19, r'$\boldsymbol{j}_3$', ha='center', va='center', fontsize=FS)
    ax.text(0.66, -0.30, r'$\boldsymbol{j}_6$', ha='center', va='center', fontsize=FS)
    ax.text(0.07, -0.60, r'$\boldsymbol{j}_5$', ha='center', va='center', fontsize=FS)
    ax.text(0.88, -0.49, r'$\boldsymbol{j}_4$', ha='center', va='center', fontsize=FS)
    save(fig, 45)


# =====================================================================
# 图 46  色散关系：E' 平面上绕右半轴割线的钥匙孔围道
# =====================================================================
def fig_46():
    fig = plt.figure(figsize=(1.95, 2.15))
    ax = bare_axes(fig, [0, 0, 1, 1], (-1.25, 1.62), (-1.25, 1.42))
    R = 1.0; r0 = 0.10
    # 大圆：从割线上沿逆时针转到下沿
    th0 = np.arcsin(r0 / R)
    th = np.linspace(th0, 2 * np.pi - th0, 300)
    ax.plot(R * np.cos(th), R * np.sin(th), 'k-', lw=LW_MAIN)
    # 割线上下沿
    seg(ax, [(0, r0), (R * np.cos(th0), r0)], lw=LW_MAIN)
    seg(ax, [(0, -r0), (R * np.cos(th0), -r0)], lw=LW_MAIN)
    # 割线内端小圆（绕原点）
    th2 = np.linspace(0, 2 * np.pi, 60)
    ax.plot(r0 * np.cos(th2), r0 * np.sin(th2), 'k-', lw=LW_MAIN)
    # 极点 E1, E2（×）与省略点
    for x, lab in [(-0.30, 'E_1'), (-0.60, 'E_2')]:
        ax.plot([x - 0.038, x + 0.038], [-0.038, 0.038], 'k-', lw=1.0)
        ax.plot([x - 0.038, x + 0.038], [0.038, -0.038], 'k-', lw=1.0)
        ax.text(x, 0.09, r'$%s$' % lab, ha='center', va='bottom', fontsize=FS)
    for x in (-0.86, -0.80, -0.74):
        circ_dot(ax, x, 0.0, ms=2.8)
    # 所求点 E（割线上方）
    circ_dot(ax, 0.36, 0.34, ms=3.6)
    ax.text(0.36, 0.42, r'$E$', ha='center', va='bottom', fontsize=FS + 1)
    # 平面标签 E'
    thc = np.linspace(0, 2 * np.pi, 40)
    ax.plot(1.32 + 0.15 * np.cos(thc), 1.15 + 0.15 * np.sin(thc), 'k-', lw=1.0)
    ax.text(1.32, 1.15, r"$E'$", ha='center', va='center', fontsize=FS)
    save(fig, 46)


# =====================================================================
# 图 47  实轴积分从下方绕过 E = E' 极点
# =====================================================================
def fig_47():
    fig = plt.figure(figsize=(2.5, 0.95))
    ax = bare_axes(fig, [0, 0, 1, 1], (-1.85, 1.85), (-0.45, 0.85))
    # 实轴：O 点到右端，E 处以下方小半圆绕过
    r0 = 0.15
    seg(ax, [(-1.55, 0), (-r0, 0)], lw=1.0)
    th = np.linspace(np.pi, 2 * np.pi, 50)
    ax.plot(r0 * np.cos(th), r0 * np.sin(th), 'k-', lw=1.0)
    seg(ax, [(r0, 0), (1.55, 0)], lw=1.0)
    circ_dot(ax, -1.55, 0, ms=3.6)
    ax.text(-1.58, -0.10, r'$O$', ha='center', va='top', fontsize=FS + 1)
    circ_dot(ax, 0, 0, ms=3.6)
    ax.text(0, 0.11, r'$E$', ha='center', va='bottom', fontsize=FS + 1)
    # 两个方向箭头（向右）
    arrow(ax, -1.05, 0, -0.72, 0, lw=1.0, ms=9)
    arrow(ax, 0.55, 0, 0.88, 0, lw=1.0, ms=9)
    # 平面标签 E'
    thc = np.linspace(0, 2 * np.pi, 40)
    ax.plot(1.10 + 0.15 * np.cos(thc), 0.52 + 0.15 * np.sin(thc), 'k-', lw=1.0)
    ax.text(1.10, 0.52, r"$E'$", ha='center', va='center', fontsize=FS)
    save(fig, 47)


# =====================================================================
# 图 48  q 平面：(a) 极点从上/下方绕过  (b) 直线移入上半平面 + 绕 q=k 封闭圈
# =====================================================================
def fig_48():
    fig = plt.figure(figsize=(3.6, 1.25))
    ax = bare_axes(fig, [0, 0, 1, 1], (-2.1, 7.3), (-0.75, 1.15))

    # ---- (a) ----
    r0 = 0.14
    seg(ax, [(-1.75, 0), (-0.7 - r0, 0)], lw=1.0)
    th = np.linspace(0, np.pi, 40)
    ax.plot(-0.7 + r0 * np.cos(th), r0 * np.sin(th), 'k-', lw=1.0)   # 上半小圆
    seg(ax, [(-0.7 + r0, 0), (0.7 - r0, 0)], lw=1.0)
    th = np.linspace(np.pi, 2 * np.pi, 40)
    ax.plot(0.7 + r0 * np.cos(th), r0 * np.sin(th), 'k-', lw=1.0)    # 下半小圆
    seg(ax, [(0.7 + r0, 0), (1.9, 0)], lw=1.0)
    circ_dot(ax, -0.7, 0, ms=3.4); circ_dot(ax, 0.7, 0, ms=3.4)
    arrow(ax, -1.62, 0, -1.32, 0, lw=0.9, ms=7)
    arrow(ax, -0.25, 0, 0.05, 0, lw=0.9, ms=7)
    arrow(ax, 1.35, 0, 1.65, 0, lw=0.9, ms=7)
    thc = np.linspace(0, 2 * np.pi, 40)
    ax.plot(-1.62 + 0.15 * np.cos(thc), 0.62 + 0.15 * np.sin(thc), 'k-', lw=1.0)
    ax.text(-1.62, 0.62, r'$q$', ha='center', va='center', fontsize=FS)
    ax.text(0.1, -0.42, '(a)', ha='center', va='center', fontsize=FS)

    # ---- (b) ----
    ox = 4.5
    seg(ax, [(ox - 1.55, 0), (ox + 1.75, 0)], lw=0.8)                # 实轴（细）
    circ_dot(ax, ox + 0.7, 0, ms=3.0)                                # 极点 q = k
    thc = np.linspace(0, 2 * np.pi, 60)
    rc = 0.16
    ax.plot(ox + 0.7 + rc * np.cos(thc), rc * np.sin(thc), 'k-', lw=1.0)
    # 逆时针方向箭头两枚（沿圆周切向）
    for ang in (60, 240):
        a = np.deg2rad(ang); px = ox + 0.7 + rc * np.cos(a); py = rc * np.sin(a)
        tx, ty = -np.sin(a), np.cos(a)                                # 切向（逆时针）
        arrow(ax, px - 0.05 * tx, py - 0.05 * ty, px + 0.05 * tx, py + 0.05 * ty,
              lw=0.9, ms=6)
    # 上半平面平行的粗直线（向右）
    ax.plot([ox - 1.55, ox + 1.75], [0.42, 0.42], 'k-', lw=1.5)
    for xa in (ox - 1.15, ox - 0.15, ox + 0.85, ox + 1.45):
        arrow(ax, xa - 0.14, 0.42, xa + 0.14, 0.42, lw=1.1, ms=8)
    ax.text(ox + 0.7, -0.42, '(b)', ha='center', va='center', fontsize=FS)
    save(fig, 48)


# =====================================================================
# 图 49  函数 h(x) = Re psi(i/x) + ln x（无 scipy 依赖的 digamma）
# =====================================================================
def _digamma(z):
    """digamma 的复数实现：递推 + 渐近级数。"""
    z = complex(z)
    s = 0j
    while abs(z) < 8:
        s -= 1 / z
        z += 1
    z2 = z * z
    return s + np.log(z) - 1 / (2 * z) - 1 / (12 * z2) + 1 / (120 * z2**2) - 1 / (252 * z2**3)


def _h(x):
    return np.real(_digamma(1j / x)) + np.log(x)


def fig_49():
    fig = plt.figure(figsize=(2.75, 2.95))
    ax = fig.add_axes([0.17, 0.13, 0.80, 0.84])
    ax.set_xlim(1, 5); ax.set_ylim(0.1, 1.1)
    # 网格：竖线每 0.5，横线每 0.1
    for gx in np.arange(1, 5.01, 0.5):
        ax.axvline(gx, lw=0.6, color='k')
    for gy in np.arange(0.2, 1.01, 0.1):
        ax.axhline(gy, lw=0.6, color='k')
    # 边框
    for s in ax.spines.values():
        s.set_linewidth(1.1)
    # 曲线
    xs = np.linspace(1, 5, 400)
    ax.plot(xs, [_h(x) for x in xs], 'k-', lw=1.9)
    # 刻度标注
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xticklabels(['1', '2', '3', '4', '5'], fontsize=FS + 1)
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=FS + 1)
    ax.tick_params(length=0, pad=4)
    ax.text(-0.22, 0.5, r'$h(x)$', transform=ax.transAxes,
            ha='center', va='center', fontsize=FS + 1, rotation=90)
    ax.text(0.5, -0.115, r'$x$', transform=ax.transAxes,
            ha='center', va='top', fontsize=FS + 1)
    save(fig, 49)


# =====================================================================
# 图 50  反应阈附近 dσ/dE 的四种行为 (a)-(d)
# =====================================================================
def _panel50(ax, kind):
    """L 形坐标轴 + 阈值虚线 + 曲线。kind: a/b/c/d"""
    # 坐标轴（横轴比纵轴长约 1.35 倍）
    seg(ax, [(0, 0), (0, 1.02)], lw=1.1)
    seg(ax, [(0, 0), (1.34, 0)], lw=1.1)
    ax.text(-0.05, 0.97, r'$\dfrac{\mathrm{d}\sigma}{\mathrm{d}E}$',
            ha='right', va='center', fontsize=FS + 2)
    ax.text(1.39, 0.0, r'$E$', ha='left', va='center', fontsize=FS + 1)
    xt = 0.55          # 阈值位置
    # 虚线
    dash = dict(a=(0.93, 0.14), b=(0.96, 0.20), c=(0.92, 0.10), d=(0.96, 0.12))[kind]
    seg(ax, [(xt, dash[0]), (xt, dash[1])], lw=0.9, ls=(0, (5, 4)))
    # 曲线：σ0 ± c·sqrt|E-Eth|（两分支，公共垂直切线在阈上）
    if kind == 'a':      # 尖点向上，顶点在虚线上
        x = np.linspace(0.40, 0.70, 200)
        y = 0.72 - 0.72 * np.sqrt(np.abs(x - xt))
    elif kind == 'b':    # 自左上降，经垂直切线转右下
        xl = np.linspace(0.38, xt, 100); yl = 0.50 + 0.95 * np.sqrt(xt - xl)
        xr = np.linspace(xt, 0.73, 100); yr = 0.50 - 0.65 * np.sqrt(xr - xt)
        x = np.concatenate([xl, xr]); y = np.concatenate([yl, yr])
    elif kind == 'c':    # 尖点向下，谷底在虚线上
        x = np.linspace(0.40, 0.70, 200)
        y = 0.26 + 0.72 * np.sqrt(np.abs(x - xt))
    else:                # (d) 自左下升，经垂直切线转右上
        xl = np.linspace(0.37, xt, 100); yl = 0.47 - 0.65 * np.sqrt(xt - xl)
        xr = np.linspace(xt, 0.72, 100); yr = 0.47 + 0.95 * np.sqrt(xr - xt)
        x = np.concatenate([xl, xr]); y = np.concatenate([yl, yr])
    ax.plot(x, y, 'k-', lw=1.5)


def fig_50():
    fig = plt.figure(figsize=(3.7, 2.7))
    W, H = 0.47, 0.44
    slots = {'a': [0.06, 0.55], 'b': [0.53, 0.55], 'c': [0.06, 0.06], 'd': [0.53, 0.06]}
    for k, (l, b) in slots.items():
        ax = bare_axes(fig, [l, b, W, H], (-0.42, 1.56), (-0.24, 1.12))
        _panel50(ax, k)
        ax.text(0.52, -0.155, '(%s)' % k, ha='center', va='top', fontsize=FS)
    save(fig, 50)


# =====================================================================
# 图 51  阈下区 σe 在 0 与 4π/ka² 之间振荡（频率向 E阈 增密）
# =====================================================================
def fig_51():
    fig = plt.figure(figsize=(2.05, 1.75))
    ax = bare_axes(fig, [0, 0, 1, 1], (-0.30, 1.42), (-0.28, 1.28))
    # 坐标轴
    seg(ax, [(0, 0), (0, 1.08)], lw=1.1)
    seg(ax, [(0, 0), (1.30, 0)], lw=1.1)
    ax.text(-0.04, 1.13, r'$\sigma_\mathrm{e}$', ha='center', va='bottom', fontsize=FS + 1)
    ax.text(1.36, 0.0, r'$E$', ha='left', va='center', fontsize=FS + 1)
    Eth = 1.0
    # 振荡曲线：相位 phi = pi + (u-u0)*pi/Δ, u = ln(1/(Eth-E))
    u0 = np.log(1 / (Eth - 0.18)); dphi = 0.335
    Eend = Eth - 3e-4
    E = np.linspace(0.18, Eend, 6000)
    u = np.log(1 / (Eth - E))
    phi = np.pi + (u - u0) * np.pi / dphi
    sig = (1 - np.cos(phi)) / 2
    ax.plot(E, sig, 'k-', lw=1.3)
    # 阈值处的竖直线与阈上常数截面水平线
    seg(ax, [(Eth, 0), (Eth, 1.0)], lw=1.3)
    seg(ax, [(Eth, 0.45), (1.24, 0.45)], lw=1.1)
    # E阈 标注（E 斜体 + 汉字下标）
    ax.text(Eth - 0.01, -0.06, r'$E$', ha='center', va='top', fontsize=FS + 1)
    ax.text(Eth + 0.055, -0.115, '阈', ha='left', va='top', fontsize=FS - 2)
    save(fig, 51)


if __name__ == '__main__':
    for f in (fig_41, fig_42, fig_43, fig_44, fig_45,
              fig_46, fig_47, fig_48, fig_49, fig_50, fig_51):
        f()
