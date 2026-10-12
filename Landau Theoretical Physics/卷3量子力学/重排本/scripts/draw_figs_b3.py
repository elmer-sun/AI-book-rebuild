# -*- coding: utf-8 -*-
"""
朗道《量子力学》（卷3）中文重排本插图重绘 —— 第三批：图23–图31
图23 §70 托马斯–费米 χ(x) 曲线族        (原书 p245 / PDF p258)
图24 §73 元素电离势                      (原书 p252 / PDF p265, 横排)
图25/26 §77 电场中氢原子 U1(ξ), U2(η)   (原书 p271 / PDF p284)
图27 §79 谱项相交（避免交叉）            (原书 p282 / PDF p295)
图28 §79 双椭圆锥面                      (原书 p283 / PDF p296)
图29 §81 H2 势能曲线 3Σu+ / 1Σg+        (原书 p287 / PDF p300)
图30 §90 预离解 U_J 势能曲线             (原书 p317 / PDF p330)
图31 §90 U_J1, U_J2 交点的分裂           (原书 p321 / PDF p334)
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

LW_MAIN = 1.2      # 主体曲线
LW_AUX = 0.8       # 辅助线
FS = 9             # 基准字号


def save(fig, n):
    for ext, path in (('pdf', os.path.join(FIGDIR, 'fig%d.pdf' % n)),
                      ('png', os.path.join(PREVDIR, 'fig%d.png' % n))):
        fig.savefig(path, bbox_inches='tight', pad_inches=0.03, dpi=300)
    plt.close(fig)
    print('fig%d done' % n)


def cubic_spline(xa, ya, xq):
    """自然三次样条（无 scipy 依赖）。"""
    xa = np.asarray(xa, float); ya = np.asarray(ya, float)
    n = len(xa); h = np.diff(xa)
    A = np.zeros((n, n)); rhs = np.zeros(n)
    A[0, 0] = 1.0; A[-1, -1] = 1.0
    for i in range(1, n - 1):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2.0 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        rhs[i] = 6.0 * ((ya[i + 1] - ya[i]) / h[i] - (ya[i] - ya[i - 1]) / h[i - 1])
    M = np.linalg.solve(A, rhs)
    xq = np.asarray(xq, float)
    out = np.empty_like(xq)
    idx = np.clip(np.searchsorted(xa, xq) - 1, 0, n - 2)
    for k, i in enumerate(idx):
        t = xq[k] - xa[i]
        a = (xa[i + 1] - xq[k]) / h[i]
        b = t / h[i]
        out[k] = (a * ya[i] + b * ya[i + 1]
                  + ((a**3 - a) * M[i] + (b**3 - b) * M[i + 1]) * h[i] * h[i] / 6.0)
    return out


def curve_from_anchors(pts, n=300):
    pts = np.asarray(pts, float)
    xq = np.linspace(pts[0, 0], pts[-1, 0], n)
    return xq, cubic_spline(pts[:, 0], pts[:, 1], xq)


# =====================================================================
# 图 23  托马斯–费米 χ(x) 曲线族
# =====================================================================
# 图 23  托马斯–费米 χ(x) 曲线族
# =====================================================================
# 中性原子 TF 函数 χ(x) 标准表值（朗道书同源数据），样条插值
_TF_TABLE = [
    (0.0, 1.000), (0.05, 0.966), (0.1, 0.886), (0.15, 0.836), (0.2, 0.795),
    (0.3, 0.721), (0.4, 0.658), (0.5, 0.607), (0.6, 0.563), (0.7, 0.525),
    (0.8, 0.491), (0.9, 0.461), (1.0, 0.424), (1.2, 0.374), (1.4, 0.333),
    (1.6, 0.298), (1.8, 0.268), (2.0, 0.243), (2.5, 0.190), (3.0, 0.157),
    (3.5, 0.133), (4.0, 0.114), (4.5, 0.0995), (5.0, 0.0876), (5.5, 0.0783),
    (6.0, 0.0704), (7.0, 0.0582), (8.0, 0.0493), (9.0, 0.0424),
    (10.0, 0.0371), (11.0, 0.0331), (12.0, 0.0296),
]
# 离子曲线（x0 处过零）与 φ0<0 上升曲线的锚点（按原书图迹）
_ION_A = [(0.0, 1.0), (0.4, 0.650), (0.8, 0.502), (1.2, 0.366),
          (1.6, 0.250), (2.0, 0.152), (2.4, 0.060), (2.75, 0.0)]
_ION_B = [(0.0, 1.0), (0.5, 0.601), (1.0, 0.413), (1.5, 0.307),
          (2.0, 0.235), (3.0, 0.149), (4.0, 0.103), (5.0, 0.071),
          (6.0, 0.025), (6.35, 0.0)]
_UP1 = [(0.0, 1.0), (0.4, 0.671), (0.8, 0.503), (1.2, 0.425),
        (1.6, 0.407), (1.9, 0.406), (2.2, 0.420), (2.6, 0.462)]
_UP2 = [(0.0, 1.0), (0.5, 0.612), (1.0, 0.429), (1.6, 0.306),
        (2.2, 0.253), (2.8, 0.246), (3.4, 0.251), (4.0, 0.269),
        (4.45, 0.292)]


def fig_23():
    fig, ax = plt.subplots(figsize=(3.35, 1.78))
    # 网格（x 整数、χ 每 0.2）
    for gx in range(0, 13):
        ax.axvline(gx, lw=0.5, color='k', zorder=0)
    for gy in np.arange(0.2, 1.01, 0.2):
        ax.axhline(gy, lw=0.5, color='k', zorder=0)

    tx, ty = zip(*_TF_TABLE)
    xs = np.linspace(0, 12, 800)
    ys = cubic_spline(np.array(tx), np.array(ty), xs)
    ax.plot(xs, ys, lw=2.4, color='k')                       # 中性原子（粗）
    for pts in (_ION_A, _ION_B, _UP1, _UP2):
        xq, yq = curve_from_anchors(pts, 400)
        ax.plot(xq, yq, lw=1.3, color='k')

    # 切线虚线：离子曲线在 x0 处切线的纵轴截距 = z/Z
    ax.plot([0, 2.75], [0.52, 0], ls=(0, (6, 4)), lw=0.9, color='k')
    ax.plot([0, 6.35], [0.215, 0], ls=(0, (6, 4)), lw=0.9, color='k')
    # 过原点的切线：φ0<0 第一条曲线上的 x1 点（χ(x1)=x1χ'(x1)）
    u = np.linspace(1.6, 2.6, 200)
    uu = cubic_spline(*zip(*_UP1), u)
    sl = np.gradient(uu, u)
    f = uu - u * sl
    k = np.where(np.diff(np.sign(f)) > 0)[0]
    x1 = u[k[0]] if len(k) else 2.45
    y1 = float(cubic_spline(*zip(*_UP1), np.array([x1]))[0])
    ax.plot([0, x1], [0, y1], ls=(0, (6, 4)), lw=0.9, color='k')

    # 标注
    ax.text(x1 + 0.1, y1 + 0.04, r'$x_1$', fontsize=FS)
    ax.text(2.9, 0.05, r'$x_0$', fontsize=FS)
    ax.text(-0.62, 0.53, r'$\chi$', fontsize=FS + 1)
    ax.text(6.3, -0.125, r'$x$', fontsize=FS + 1)

    ax.set_xlim(0, 12); ax.set_ylim(0, 1.0)
    ax.set_xticks(range(0, 13)); ax.set_yticks(np.arange(0.2, 1.01, 0.2))
    ax.set_xticks(np.arange(0.5, 12.1, 0.5), minor=True)
    ax.set_yticks(np.arange(0.1, 1.01, 0.1), minor=True)
    ax.tick_params(labelsize=8, length=3)
    ax.tick_params(which='minor', length=2)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.spines[['left', 'bottom']].set_linewidth(0.8)
    save(fig, 23)


# =====================================================================
# 图 24  元素电离势（光谱学数据）
# =====================================================================
_ELEM = [
    (1, 'H', 13.598), (2, 'He', 24.587), (3, 'Li', 5.392), (4, 'Be', 9.322),
    (5, 'B', 8.298), (6, 'C', 11.260), (7, 'N', 14.534), (8, 'H', 13.618),
    (9, 'F', 17.423), (10, 'Ne', 21.564), (11, 'Na', 5.139), (12, 'Mg', 7.646),
    (13, 'Al', 5.986), (14, 'Si', 8.151), (15, 'P', 10.486), (16, 'S', 10.360),
    (17, 'Cl', 12.967), (18, 'Ar', 15.759), (19, 'K', 4.341), (20, 'Ca', 6.113),
    (21, 'Sc', 6.561), (22, 'Ti', 6.828), (23, 'V', 6.746), (24, 'Cr', 6.766),
    (25, 'Mn', 7.434), (26, 'Fe', 7.902), (27, 'Co', 7.881), (28, 'Ni', 7.639),
    (29, 'Cu', 7.726), (30, 'Zn', 9.394), (31, 'Ga', 5.999), (32, 'Ge', 7.899),
    (33, 'As', 9.815), (34, 'Se', 9.752), (35, 'Br', 11.814), (36, 'Kr', 13.999),
    (37, 'Rb', 4.177), (38, 'Sr', 5.695), (39, 'Y', 6.217), (40, 'Zr', 6.634),
    (41, 'Nb', 6.759), (42, 'Mo', 7.092), (43, 'Tc', 7.28), (44, 'Ru', 7.360),
    (45, 'Rh', 7.459), (46, 'Pd', 8.337), (47, 'Ag', 7.576), (48, 'Cd', 8.994),
    (49, 'In', 5.786), (50, 'Sn', 7.344), (51, 'Sb', 8.608), (52, 'Te', 9.010),
    (53, 'I', 10.451), (54, 'Xe', 12.130), (55, 'Cs', 3.894), (56, 'Ba', 5.212),
    (57, 'La', 5.577), (58, 'Ce', 5.539), (59, 'Pr', 5.473), (60, 'Nd', 5.525),
    (61, 'Pm', 5.582), (62, 'Sm', 5.644), (63, 'Eu', 5.670), (64, 'Gd', 6.150),
    (65, 'Tb', 5.864), (66, 'Dy', 5.939), (67, 'Ho', 6.022), (68, 'Er', 6.108),
    (69, 'Tm', 6.184), (70, 'Yb', 6.254), (71, 'Lu', 5.426), (72, 'Hf', 6.825),
    (73, 'Ta', 7.550), (74, 'W', 7.864), (75, 'Re', 7.834), (76, 'Os', 8.438),
    (77, 'Ir', 8.967), (78, 'Pt', 8.959), (79, 'Au', 9.226), (80, 'Hg', 10.438),
    (81, 'Tl', 6.108), (82, 'Pb', 7.417), (83, 'Bi', 7.286), (84, 'Po', 8.417),
    (86, 'Rn', 10.749), (88, 'Ra', 5.20), (89, 'Ac', 6.70), (92, 'U', 3.60),
]
# 逐元素标签位（Z → (dx, dy, ha, size|None)，仿原书上下交错排布）
_LAB = {
    1: (0.9, 0.0, 'left', None), 2: (0.7, 0.55, 'left', None),
    3: (0.2, -0.9, 'left', None), 4: (-0.5, 0.5, 'right', None),
    5: (0.25, -0.75, 'left', None), 6: (0.8, -0.1, 'left', None),
    7: (-0.45, 0.5, 'right', None), 8: (0.45, -0.5, 'left', None),
    9: (-0.75, 0.1, 'right', None), 10: (-0.3, 0.65, 'right', None),
    11: (0, -1.0, 'center', None), 12: (-0.55, 0.45, 'right', None),
    13: (0.3, -0.75, 'left', None), 14: (0.6, -0.5, 'left', None),
    15: (-0.7, 0.2, 'right', None), 16: (0.45, -0.6, 'left', None),
    17: (-0.8, 0.0, 'right', None), 18: (-0.3, 0.65, 'right', None),
    19: (0, -1.0, 'center', None), 20: (0.3, -0.85, 'left', None),
    21: (-0.65, 0.3, 'right', 4.8), 22: (-0.3, 0.55, 'right', 4.8),
    23: (0.0, -0.75, 'center', 4.8), 24: (0.3, -0.72, 'left', 4.8),
    25: (0.55, -0.5, 'left', 4.8), 26: (-0.75, 0.2, 'right', 4.8),
    27: (0.15, 0.42, 'center', 4.8), 28: (0.65, 0.05, 'left', 4.8),
    29: (0.5, -0.6, 'left', 4.8), 30: (-0.35, 0.6, 'right', 4.8),
    31: (0.3, -0.8, 'left', 4.8), 32: (0.7, -0.3, 'left', 4.8),
    33: (0.45, 0.22, 'left', 4.8), 34: (0.5, -0.55, 'left', 4.8),
    35: (-0.8, 0.1, 'right', 4.8), 36: (-0.25, 0.6, 'right', 4.8),
    37: (0.3, -0.9, 'left', 4.8), 38: (0.4, -0.7, 'left', 4.8),
    39: (-0.65, 0.25, 'right', 4.8), 40: (-0.35, 0.45, 'right', 4.8),
    41: (0.3, -0.65, 'left', 4.8), 42: (-0.15, 0.42, 'center', 4.8),
    43: (0.3, -0.6, 'left', 4.8), 44: (0.0, 0.62, 'center', 4.8),
    45: (0.55, -0.6, 'left', 4.8), 46: (-0.55, 0.4, 'right', 4.8),
    47: (0.55, -0.45, 'left', 4.8), 48: (-0.5, 0.55, 'right', 4.8),
    49: (0.35, -0.8, 'left', 4.8), 50: (0.6, -0.55, 'left', 4.8),
    51: (-0.8, 0.15, 'right', 4.8), 52: (0.6, 0.3, 'left', 4.8),
    53: (-0.75, 0.15, 'right', None), 54: (-0.3, 0.6, 'right', None),
    55: (0.3, -0.95, 'left', None), 56: (-0.7, 0.2, 'right', None),
    57: (0.0, 0.5, 'center', 4.6), 58: (0.0, -0.66, 'center', 4.6),
    59: (0.0, 0.5, 'center', 4.6), 60: (0.0, -0.68, 'center', 4.6),
    61: (0.0, 0.5, 'center', 4.6), 62: (-0.3, -0.68, 'center', 4.6),
    63: (0.4, -0.62, 'center', 4.6), 64: (0.0, 0.52, 'center', 4.6),
    65: (0.0, -0.66, 'center', 4.6), 66: (0.0, 0.5, 'center', 4.6),
    67: (0.0, -0.66, 'center', 4.6), 68: (0.0, 0.5, 'center', 4.6),
    69: (0.0, -0.66, 'center', 4.6), 70: (0.0, 0.5, 'center', 4.6),
    71: (0.4, -0.6, 'left', 4.8), 72: (0.5, -0.55, 'left', 4.8),
    73: (-0.5, 0.4, 'right', 4.8), 74: (-0.2, 0.55, 'right', 4.8),
    75: (0.45, -0.6, 'left', 4.8), 76: (0.5, -0.5, 'left', 4.8),
    77: (-0.6, 0.3, 'right', 4.8), 78: (0.55, -0.55, 'left', 4.8),
    79: (-0.4, 0.45, 'right', 4.8), 80: (-0.3, 0.55, 'right', None),
    81: (0.25, -0.85, 'left', None), 82: (-0.6, 0.35, 'right', 4.8),
    83: (0.4, -0.65, 'left', 4.8), 84: (0.6, 0.25, 'left', 4.8),
    86: (-0.4, 0.55, 'right', None), 88: (0.3, -0.9, 'left', None),
    89: (0.4, 0.4, 'left', None), 92: (0.35, -0.8, 'left', None),
}
_DASH_SEG = [(84, 86), (86, 88), (89, 92)]   # Po–Rn, Rn–Ra, Ac–U 为虚线


def fig_24():
    fig, ax = plt.subplots(figsize=(3.94, 2.75))
    Z = [e[0] for e in _ELEM]; I = [e[2] for e in _ELEM]
    zarr = np.array(Z); iarr = np.array(I)
    # 实线折线（相邻元素都在表内且不属虚线段）
    for k in range(len(_ELEM) - 1):
        z1, z2 = _ELEM[k][0], _ELEM[k + 1][0]
        dashed = (min(z1, z2), max(z1, z2)) in _DASH_SEG
        ax.plot([z1, z2], [_ELEM[k][2], _ELEM[k + 1][2]],
                ls='--' if dashed else '-', lw=0.9, color='k',
                dash_capstyle='butt')
    # 数据点：小空心圆
    ax.plot(zarr, iarr, 'o', mfc='w', mec='k', ms=2.6, mew=0.7, linestyle='none')
    # 元素符号
    for z, sym, ei in _ELEM:
        dx, dy, ha, fs = _LAB.get(z, (0.5, 0.5, 'left', None))
        ax.text(z + dx, ei + dy, sym, ha=ha, va='center',
                fontsize=fs or 5.2)
    ax.set_xlim(0.4, 95.5); ax.set_ylim(2.0, 26.4)
    ax.set_xticks(range(5, 91, 5)); ax.set_yticks([5, 10, 15, 20, 25])
    ax.tick_params(labelsize=7, length=3)
    ax.text(96.3, 2.9, r'$Z$', fontsize=FS + 1, ha='left')
    ax.set_ylabel(r'$E$/eV', fontsize=FS, rotation=90, labelpad=6)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.spines[['left', 'bottom']].set_linewidth(0.8)
    save(fig, 24)


# =====================================================================
# 图 25  U1(ξ)   图 26  U2(η)  （电场中的氢原子，斯塔克效应）
# =====================================================================
def _stark_panel(fname, axis_sym, curve, ulab, dashes_end, ylim, xlim,
                 turning_xs, e4=-0.276):
    fig, ax = plt.subplots(figsize=(1.68, 1.45))
    xq, yq = curve_from_anchors(curve)
    ax.plot(xq, yq, lw=1.3, color='k')
    # 竖轴
    ax.plot([0.10, 0.10], [ylim[0], ylim[1]], lw=0.9, color='k')
    # ξ(η) 轴：U=0 处实横线，右端标 ξ / η
    ax.plot([0.10, xlim[1]], [0, 0], lw=0.9, color='k')
    # E/4 虚线
    ax.plot([0.10, dashes_end], [e4, e4], ls=(0, (5, 3)), lw=0.9, color='k')
    # 标注
    ax.text(0.075, 0.97, ulab, fontsize=FS, ha='right')
    ax.text(xlim[1] + 0.02, 0.02, r'$\%s$' % axis_sym, fontsize=FS + 1,
            ha='left', va='center')
    ax.text(0.065, e4, r'$\dfrac{E}{4}$', fontsize=8, ha='right',
            va='center')
    for x0, k in zip(turning_xs, (1, 2)):
        ax.text(x0, 0.06, r'$\%s_%d$' % (axis_sym, k), fontsize=FS,
                ha='center')
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.axis('off')
    save(fig, fname)


def fig_25():
    curve = [(0.115, 0.98), (0.20, 0.72), (0.32, 0.48), (0.46, 0.24),
             (0.60, 0.03), (0.74, -0.14), (0.88, -0.26), (1.02, -0.32),
             (1.18, -0.352), (1.35, -0.360), (1.50, -0.352), (1.65, -0.33),
             (1.80, -0.30), (1.92, -0.26), (2.02, -0.14), (2.10, 0.02),
             (2.16, 0.16), (2.21, 0.40), (2.245, 0.65)]
    _stark_panel(25, 'xi', curve, r'$U_1$', 2.03,
                 (-0.64, 1.0), (0.0, 2.36), (0.93, 1.93), e4=-0.276)


def fig_26():
    curve = [(0.11, 0.98), (0.18, 0.70), (0.26, 0.45), (0.35, 0.22),
             (0.44, 0.0), (0.52, -0.18), (0.62, -0.33), (0.74, -0.44),
             (0.86, -0.50), (0.98, -0.515), (1.10, -0.49), (1.22, -0.42),
             (1.35, -0.30), (1.48, -0.14), (1.60, 0.03), (1.70, 0.15),
             (1.80, 0.235), (1.90, 0.26), (2.00, 0.24), (2.10, 0.13),
             (2.18, -0.03), (2.25, -0.22), (2.30, -0.45), (2.34, -0.75),
             (2.36, -1.0)]
    _stark_panel(26, 'eta', curve, r'$U_2$', 2.30,
                 (-1.05, 1.0), (0.0, 2.48), (0.49, 1.38), e4=-0.29)


# =====================================================================
# 图 27  谱项相交（对称性相同 → 实线分开，虚线交叉）
# =====================================================================
def fig_27():
    fig, ax = plt.subplots(figsize=(1.97, 1.70))
    # 坐标轴（无刻度）
    ax.plot([0, 0], [0, 1.0], lw=0.9, color='k')
    ax.plot([0, 1.0], [0, 0], lw=0.9, color='k')
    ax.text(-0.02, 1.0, r'$U(r)$', fontsize=FS, ha='left', va='bottom')
    ax.text(1.02, -0.01, r'$r$', fontsize=FS + 1, ha='left', va='center')
    # 实线：相互排斥的两条谱项
    up = [(0.02, 0.46), (0.12, 0.435), (0.24, 0.425), (0.36, 0.425),
          (0.47, 0.44), (0.55, 0.475), (0.63, 0.545), (0.72, 0.635),
          (0.82, 0.74), (0.92, 0.86), (0.98, 0.945)]
    lo = [(0.02, 0.16), (0.14, 0.20), (0.27, 0.245), (0.40, 0.283),
          (0.50, 0.305), (0.60, 0.322), (0.70, 0.333), (0.80, 0.337),
          (0.88, 0.336), (0.98, 0.330)]
    for pts in (up, lo):
        xq, yq = curve_from_anchors(pts, 240)
        ax.plot(xq, yq, lw=1.3, color='k')
    # 虚线：不相考虑微扰时的交叉（X 形）
    ax.plot([0.46, 0.71], [0.315, 0.515], ls=(0, (6, 4)), lw=0.9, color='k')
    ax.plot([0.45, 0.74], [0.446, 0.398], ls=(0, (6, 4)), lw=0.9, color='k')
    ax.set_xlim(-0.06, 1.10); ax.set_ylim(-0.06, 1.05)
    ax.axis('off')
    save(fig, 27)


# =====================================================================
# 图 28  双椭圆锥面
# =====================================================================
def _ellipse_arc(c, w, h, ang, n=90):
    t = np.linspace(0, 2 * np.pi, n)
    x0 = w / 2 * np.cos(t); y0 = h / 2 * np.sin(t)
    ca, sa = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
    return c[0] + x0 * ca - y0 * sa, c[1] + x0 * sa + y0 * ca


def fig_28():
    fig, ax = plt.subplots(figsize=(2.36, 1.82))
    ax.set_aspect('equal')
    O = (1.7, 1.55)
    ax.plot([O[0], O[0]], [O[1], 6.9], lw=0.9, color='k')          # U
    ax.plot([O[0], 9.6], [O[1], O[1]], lw=0.9, color='k')          # r2
    ax.plot([O[0], 0.45], [O[1], 0.55], lw=0.9, color='k')         # r1
    ax.text(O[0] + 0.25, 6.85, r'$U$', fontsize=FS)
    ax.text(9.7, O[1] - 0.35, r'$r_2$', fontsize=FS, ha='left')
    ax.text(0.62, 0.22, r'$r_1$', fontsize=FS)
    apex = (5.05, 4.55)
    # 上锥：底椭圆 + 锥面刻线
    c_up, (wu, hu), ang_u = (3.80, 5.40), (3.3, 0.90), 13
    xs, ys = _ellipse_arc(c_up, wu, hu, ang_u)
    ax.plot(xs, ys, lw=1.5, color='k')
    for t in np.linspace(0.14, 0.90, 10):
        cc = (c_up[0] + t * (apex[0] - c_up[0]), c_up[1] + t * (apex[1] - c_up[1]))
        xs, ys = _ellipse_arc(cc, wu * (1 - t), hu * (1 - t), ang_u, 60)
        ax.plot(xs, ys, lw=0.4, color='k')
    # 下锥
    c_lo, (wl, hl), ang_l = (6.20, 3.35), (3.7, 1.00), 11
    xs, ys = _ellipse_arc(c_lo, wl, hl, ang_l)
    ax.plot(xs, ys, lw=1.5, color='k')
    for t in np.linspace(0.14, 0.90, 10):
        cc = (c_lo[0] + t * (apex[0] - c_lo[0]), c_lo[1] + t * (apex[1] - c_lo[1]))
        xs, ys = _ellipse_arc(cc, wl * (1 - t), hl * (1 - t), ang_l, 60)
        ax.plot(xs, ys, lw=0.4, color='k')
    # 轮廓素线
    for (cc, ww, hh, aa) in ((c_up, wu, hu, ang_u), (c_lo, wl, hl, ang_l)):
        t = np.linspace(0, 2 * np.pi, 361)
        x0 = ww / 2 * np.cos(t); y0 = hh / 2 * np.sin(t)
        ca, sa = np.cos(np.deg2rad(aa)), np.sin(np.deg2rad(aa))
        px = cc[0] + x0 * ca - y0 * sa; py = cc[1] + x0 * sa + y0 * ca
        for k in (np.argmax(px), np.argmin(px)):
            ax.plot([px[k], apex[0]], [py[k], apex[1]], lw=1.1, color='k')
    ax.set_xlim(0, 10.4); ax.set_ylim(0, 7.6)
    ax.axis('off')
    save(fig, 28)


# =====================================================================
# 图 29  氢分子的 3Σu+（排斥）与 1Σg+（成键）势能曲线
# =====================================================================
def fig_29():
    fig, ax = plt.subplots(figsize=(2.36, 3.19))
    ax.plot([0, 0], [-0.35, 1.0], lw=0.9, color='k')               # 竖轴
    ax.plot([0, 1.14], [0, 0], lw=0.8, color='k')                  # r 轴（细）
    ax.text(0.035, 0.965, r'$U(r)$', fontsize=FS)
    ax.text(1.13, -0.055, r'$r$', fontsize=FS + 1)
    t = np.linspace(0, 1, 300)
    # 3Σu+：单调下降，从上方趋近轴线
    p3 = [(0.24, 0.98), (0.265, 0.72), (0.30, 0.47), (0.35, 0.30),
          (0.42, 0.185), (0.52, 0.105), (0.64, 0.058), (0.78, 0.028),
          (0.92, 0.011), (1.04, 0.003)]
    # 1Σg+：深极小，从下方趋近轴线
    p1 = [(0.035, 0.175), (0.045, 0.02), (0.062, -0.155), (0.085, -0.27),
          (0.105, -0.315), (0.13, -0.30), (0.17, -0.225), (0.23, -0.125),
          (0.31, -0.062), (0.42, -0.030), (0.56, -0.013), (0.72, -0.005),
          (0.88, -0.0015), (1.02, -0.0003)]
    for pts in (p3, p1):
        xq, yq = curve_from_anchors(pts, 320)
        ax.plot(xq, yq, lw=1.5, color='k')
    ax.text(0.35, 0.66, r'$^3\Sigma_u^+$', fontsize=FS + 1)
    ax.text(0.40, -0.27, r'$^1\Sigma_g^+$', fontsize=FS + 1)
    ax.set_xlim(-0.05, 1.25); ax.set_ylim(-0.40, 1.03)
    ax.axis('off')
    save(fig, 29)


# =====================================================================
# 图 30  预离解：两条有效势能 U_J(r) 曲线
# =====================================================================
def fig_30():
    fig, ax = plt.subplots(figsize=(2.76, 2.14))
    ax.plot([0.25, 0.25], [0, 10.2], lw=0.9, color='k')            # 竖轴
    ax.plot([0.25, 10.4], [0, 0], lw=0.9, color='k')               # r 轴
    ax.text(0.12, 9.85, r'$U_J(r)$', fontsize=FS, ha='right')
    ax.text(10.45, 0.05, r'$r$', fontsize=FS + 1, ha='left', va='center')
    # 水平虚线 E 与 E'
    ax.plot([1.02, 9.55], [9.15, 9.15], ls=(0, (6, 4)), lw=0.9, color='k')
    ax.plot([1.82, 9.55], [6.90, 6.90], ls=(0, (6, 4)), lw=0.9, color='k')
    ax.text(9.70, 9.15, r'$E$', fontsize=FS + 1, va='center')
    ax.text(9.70, 6.90, r"$E'$", fontsize=FS + 1, va='center')
    # 曲线 2（深阱，右端渐近线高于 E'）
    c2 = [(1.05, 9.75), (1.13, 7.6), (1.22, 5.7), (1.35, 4.05), (1.52, 2.75),
          (1.75, 1.80), (2.05, 1.10), (2.45, 0.62), (2.95, 0.42), (3.40, 0.37),
          (3.80, 0.45), (4.30, 0.85), (4.80, 1.60), (5.25, 2.60), (5.60, 3.80),
          (5.90, 5.00), (6.25, 6.05), (6.70, 6.62), (7.25, 6.87), (7.80, 7.05),
          (8.40, 7.32), (8.80, 7.55)]
    # 曲线 1（浅阱，右端渐近线略低于 E'）
    c1 = [(1.82, 6.90), (1.95, 6.10), (2.12, 5.20), (2.35, 4.30), (2.62, 3.65),
          (2.90, 3.38), (3.20, 3.30), (3.55, 3.42), (4.00, 3.80), (4.50, 4.42),
          (5.00, 5.05), (5.50, 5.55), (5.90, 5.85), (6.40, 6.03), (7.00, 6.16),
          (7.70, 6.26), (8.40, 6.31), (8.80, 6.33)]
    for pts in (c2, c1):
        xq, yq = curve_from_anchors(pts, 320)
        ax.plot(xq, yq, lw=1.4, color='k')
    # r0 处竖虚线（交点）
    ax.plot([5.90, 5.90], [0, 5.85], ls=(0, (5, 3)), lw=0.9, color='k')
    ax.text(5.90, -0.85, r'$r_0$', fontsize=FS, ha='center')
    # a2（曲线2在 E 处的左转折点）、a1（曲线1在 E' 处的左转折点）
    ax.plot([1.08, 1.08], [0, 9.15], ls=(0, (5, 3)), lw=0.9, color='k')
    ax.plot([1.82, 1.82], [0, 6.90], ls=(0, (5, 3)), lw=0.9, color='k')
    ax.text(1.02, -0.85, r'$a_2$', fontsize=FS, ha='center')
    ax.text(1.90, -0.85, r'$a_1$', fontsize=FS, ha='center')
    # 曲线标号
    ax.text(8.30, 8.15, r'$2$', fontsize=FS + 1)
    ax.text(8.62, 5.90, r'$1$', fontsize=FS + 1)
    ax.set_xlim(0, 10.6); ax.set_ylim(-1.35, 10.4)
    ax.axis('off')
    save(fig, 30)


# =====================================================================
# 图 31  计及 V12 后交点分裂为 U_b(r)（1'—2）与 U_a(r)（2'—1）
# =====================================================================
def fig_31():
    fig, ax = plt.subplots(figsize=(2.56, 2.30))
    ax.plot([0.30, 0.30], [0, 10.3], lw=0.9, color='k')
    ax.plot([0.30, 10.3], [0, 0], lw=0.9, color='k')
    ax.text(0.15, 9.9, r'$U_J$', fontsize=FS, ha='right')
    ax.text(10.35, 0.05, r'$r$', fontsize=FS + 1, ha='left', va='center')
    # E 水平虚线
    ax.plot([0.72, 9.55], [8.80, 8.80], ls=(0, (6, 4)), lw=0.9, color='k')
    ax.text(9.70, 8.80, r'$E$', fontsize=FS + 1, va='center')
    # 上面一条连续曲线 U_b（1'—2）
    cb = [(0.72, 8.80), (0.83, 7.45), (0.95, 6.15), (1.12, 5.05), (1.35, 4.40),
          (1.65, 4.05), (2.00, 3.93), (2.35, 4.02), (2.75, 4.28), (3.20, 4.62),
          (3.65, 4.95), (4.10, 5.18), (4.60, 5.42), (4.95, 5.85), (5.40, 6.50),
          (5.90, 7.05), (6.50, 7.45), (7.20, 7.72), (7.90, 7.90), (8.55, 8.00)]
    # 下面一条连续曲线 U_a（2'—1）
    ca = [(0.95, 8.80), (1.03, 7.20), (1.13, 5.55), (1.25, 3.95), (1.38, 2.55),
          (1.52, 1.45), (1.70, 0.72), (1.92, 0.38), (2.15, 0.28), (2.40, 0.35),
          (2.70, 0.62), (3.05, 1.10), (3.45, 1.78), (3.85, 2.60), (4.20, 3.45),
          (4.45, 4.10), (4.58, 4.55), (4.70, 4.85), (4.95, 5.02), (5.40, 5.18),
          (6.10, 5.26), (7.00, 5.34), (8.00, 5.40), (8.55, 5.42)]
    for pts in (cb, ca):
        xq, yq = curve_from_anchors(pts, 340)
        ax.plot(xq, yq, lw=1.4, color='k')
    # r0 竖虚线（至两曲线最接近处）
    ax.plot([4.60, 4.60], [0, 4.72], ls=(0, (5, 3)), lw=0.9, color='k')
    ax.text(4.60, -0.90, r'$r_0$', fontsize=FS, ha='center')
    # 标号
    ax.text(2.70, 4.72, r"$1'$", fontsize=FS + 1)
    ax.text(2.45, 1.15, r"$2'$", fontsize=FS + 1)
    ax.text(7.95, 7.28, r'$2$', fontsize=FS + 1)
    ax.text(8.72, 8.12, r'$b$', fontsize=FS + 1)
    ax.text(8.15, 4.62, r'$1$', fontsize=FS + 1)
    ax.text(8.72, 5.52, r'$a$', fontsize=FS + 1)
    ax.set_xlim(0, 10.6); ax.set_ylim(-1.45, 10.5)
    ax.axis('off')
    save(fig, 31)


if __name__ == '__main__':
    import sys
    only = [int(a) for a in sys.argv[1:] if a.isdigit()]
    funcs = {23: fig_23, 24: fig_24, 25: fig_25, 26: fig_26, 27: fig_27,
             28: fig_28, 29: fig_29, 30: fig_30, 31: fig_31}
    for n in (only if only else sorted(funcs)):
        funcs[n]()
