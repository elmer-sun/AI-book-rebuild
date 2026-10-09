# -*- coding: utf-8 -*-
"""
Concepts in Solids 第 3 章 Wannier 激子/时空图部分插图重绘（批次 ch3d）
  fig_46 : p166 能级随 b 展宽（p 线 X 交叉、Exciton、E_o、→k）
  fig_47 : p166 Band 抛物线与 Localized exciton 水平线
  fig_48 : p168 t-x 图：电子/空穴世界线经 wavy 相互作用（-e²/κ|R_j-R_k|）
  fig_49 : p169 双面板 (a) X-T-X 湮灭-传播-产生图；(b) b_jk / b_kj 虚跳变与 U 线
  fig_50 : p169 t-x 图：电子/空穴路径交叉的单 wavy 相互作用
  fig_51 : p170 顶点辐射 wavy 光子的 V 形费米子线（有效偶极矩）
  fig_52 : p170 "backwards diagram"：b_i…b_l† 双圈阶梯图
输出 figures/fig_{key}.pdf 与 figures/preview/fig_{key}.png
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

BASE = r'E:\AI整理书籍\安德森\重排本'
FIGS = os.path.join(BASE, 'figures')
PREV = os.path.join(FIGS, 'preview')
os.makedirs(PREV, exist_ok=True)


def _canvas(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    return fig, ax


def _save(fig, key):
    fig.savefig(os.path.join(FIGS, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, 'fig_%s.png' % key), dpi=150,
                bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


def _arrow(ax, p0, p1, ms=10, lw=1.1, style='-|>'):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, mutation_scale=ms,
                                lw=lw, color='k'))


def _lerp(p0, p1, f):
    return (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)


def _seg(ax, p0, p1, lw=1.8):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], 'k-', lw=lw,
            solid_capstyle='round')


def _seg_arrow(ax, p0, p1, f0, f1, ms=15, lw=1.8):
    """在 p0->p1 线段的 f0..f1 段上叠加箭头（f1 端为箭头尖）。"""
    a, b = _lerp(p0, p1, f0), _lerp(p0, p1, f1)
    _arrow(ax, a, b, ms=ms, lw=lw)


def _wavy(ax, p0, p1, n, amp=0.6, lw=1.8, npts=None):
    """连接 p0、p1 的波纹线（两端为节点），n 个波峰周期。"""
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    v = p1 - p0
    L = np.hypot(*v)
    u = v / L
    nv = np.array([-u[1], u[0]])
    if npts is None:
        npts = 26 * n
    t = np.linspace(0.0, 1.0, npts)
    off = amp * np.sin(2 * np.pi * n * t)
    pts = p0[None, :] + v[None, :] * t[:, None] + nv[None, :] * off[:, None]
    ax.plot(pts[:, 0], pts[:, 1], 'k-', lw=lw)


def _smooth(pts, n=60):
    """Catmull-Rom 样条平滑过点曲线，返回 (x, y)。"""
    pts = np.asarray(pts, float)
    P = np.vstack([pts[0], pts, pts[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (p2 - p0) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-2])
    return np.array(out).T


def _bezier(p0, c1, c2, p3, n=80):
    """三次贝塞尔；返回采样点数组与取点函数。"""
    t = np.linspace(0, 1, n)[:, None]
    P0, C1, C2, P3 = map(lambda p: np.asarray(p, float), (p0, c1, c2, p3))
    pts = ((1 - t) ** 3 * P0 + 3 * (1 - t) ** 2 * t * C1
           + 3 * (1 - t) * t ** 2 * C2 + t ** 3 * P3)
    return pts


# ----------------------------------------------------------------------
def fig_46():
    fig, ax = _canvas(4.6, 2.95)
    # E 指向下的小箭头（能量正向朝下）
    ax.text(3.3, 48.3, r'$E$', ha='center', va='center')
    _arrow(ax, (3.3, 46.6), (3.3, 43.8), ms=9, lw=1.0)
    # p 水平线（no b）
    ax.text(5.4, 44.5, r'$p$', ha='right', va='center')
    ax.plot([6.5, 86.8], [44.5, 44.5], 'k-', lw=1.2)
    ax.text(88.2, 44.5, 'no b', ha='left', va='center')
    # X 交叉点及四条臂
    X = (30.6, 44.3)
    ax.plot([25.0, X[0]], [47.8, X[1]], 'k-', lw=1.7)          # 左上直臂
    ax.plot([24.8, X[0]], [41.0, X[1]], 'k-', lw=1.7)          # 左下直臂
    up = _smooth([X, (38.0, 49.5), (46.0, 53.0), (54.0, 55.3), (64.0, 56.6)])
    ax.plot(up[0], up[1], 'k-', lw=1.7)                          # 右上升曲线
    dn = _smooth([X, (38.0, 40.0), (46.0, 36.6), (54.0, 34.2), (64.5, 32.3)])
    ax.plot(dn[0], dn[1], 'k-', lw=1.7)                          # 右下降曲线
    ax.text(65.5, 56.6, 'with b', ha='left', va='center')
    ax.text(66.0, 32.3, 'with b', ha='left', va='center')
    # U 双向箭头
    _arrow(ax, (30.6, 44.0), (30.6, 29.2), ms=10, lw=1.1, style='<|-|>')
    ax.text(29.8, 36.8, r'$U$', ha='right', va='center')
    # Exciton 水平线（no b）及其 with b 曲线
    ax.text(6.0, 29.0, 'Exciton', ha='right', va='center')
    ax.plot([6.5, 86.4], [29.0, 29.0], 'k-', lw=1.2)
    ax.text(88.2, 29.0, 'no b', ha='left', va='center')
    ex = _smooth([(25.0, 28.7), (35.0, 28.3), (45.0, 27.4),
                  (55.0, 26.2), (65.0, 25.0)])
    ax.plot(ex[0], ex[1], 'k-', lw=1.7)
    ax.text(80.5, 24.4, 'with b', ha='left', va='center')
    # E_o 双向箭头
    _arrow(ax, (21.0, 28.9), (21.0, 7.9), ms=10, lw=1.1, style='<|-|>')
    ax.text(19.3, 18.4, r'$E_o$', ha='right', va='center')
    # s 水平线与 →k
    ax.text(4.6, 7.8, r'$s$', ha='right', va='center')
    ax.plot([6.5, 87.0], [7.8, 7.8], 'k-', lw=1.2)
    _arrow(ax, (59.0, 5.6), (61.6, 5.6), ms=9, lw=1.0)
    ax.text(62.6, 5.6, r'$k$', ha='left', va='center')
    ax.set_xlim(0, 92)
    ax.set_ylim(0, 59)
    _save(fig, '46')


# ----------------------------------------------------------------------
def fig_47():
    fig, ax = _canvas(4.3, 1.45)
    # Band 曲线（左支陡、右支平缓的抛物线形）
    c = _smooth([(10.1, 32.4), (14.5, 26.5), (20.0, 18.5), (23.5, 15.2),
                 (30.0, 11.9), (37.0, 10.8), (44.0, 11.6), (50.9, 15.2),
                 (60.0, 17.6), (75.0, 19.4), (90.5, 20.5)], n=50)
    ax.plot(c[0], c[1], 'k-', lw=2.0)
    ax.text(13.8, 32.0, 'Band', ha='left', va='center')
    # Localized exciton 水平线
    ax.plot([1.8, 65.8], [15.2, 15.2], 'k-', lw=1.3)
    ax.text(67.5, 15.2, 'Localized exciton', ha='left', va='center')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 34)
    _save(fig, '47')


# ----------------------------------------------------------------------
def fig_48():
    fig, ax = _canvas(3.5, 2.7)
    # 坐标轴（无箭头直线）
    ax.plot([6.0, 6.0], [11.5, 44.5], 'k-', lw=1.3)
    ax.plot([6.0, 52.0], [11.5, 11.5], 'k-', lw=1.3)
    ax.text(4.6, 43.2, r'$t$', ha='right', va='center')
    ax.text(53.2, 11.5, r'$x$', ha='left', va='center')
    # R_j / R_k 刻度
    for xt, lab in ((18.9, r'$R_j$'), (33.6, r'$R_k$')):
        ax.plot([xt, xt], [11.5, 13.0], 'k-', lw=1.3)
        ax.text(xt, 9.4, lab, ha='center', va='center')
    V1, V2 = (20.0, 31.0), (33.6, 31.0)
    # 相互作用波纹线
    _wavy(ax, V1, V2, n=5, amp=0.55, lw=1.8)
    # 电子世界线：k_e 入射 + k_e' 出射
    ein0 = (13.75, 20.25)
    _seg(ax, ein0, V1)
    _seg_arrow(ax, ein0, V1, 0.72, 0.93)
    eout1 = (18.0, 42.75)
    _seg(ax, V1, eout1)
    _seg_arrow(ax, V1, eout1, 0.80, 1.0)
    ax.text(12.0, 23.4, r'$k_e$', ha='right', va='center')
    ax.text(19.6, 36.3, r"$k_e'$", ha='left', va='center')
    # 空穴世界线：k_h 入射 + k_h' 出射
    hin0 = (37.75, 18.5)
    _seg(ax, hin0, V2)
    _seg_arrow(ax, hin0, V2, 0.76, 0.93)
    hout1 = (27.5, 42.25)
    _seg(ax, V2, hout1)
    _seg_arrow(ax, V2, hout1, 0.80, 1.0)
    ax.text(38.4, 25.3, r'$k_h$', ha='left', va='center')
    ax.text(30.6, 40.3, r"$k_h'$", ha='left', va='center')
    # 相互作用标注
    ax.text(25.9, 27.2, 'Interaction', ha='center', va='center')
    ax.text(25.9, 21.6, r'$-\;\dfrac{e^2}{\kappa\,|\,R_j-R_k\,|}$',
            ha='center', va='center', fontsize=10)
    ax.set_xlim(0, 57)
    ax.set_ylim(0, 46)
    _save(fig, '48')


# ----------------------------------------------------------------------
def _panel_axes(ax, x0=0.0, rj=17.0, rk=34.15):
    """图 49 单面板坐标系：t 轴、x 轴、R_j / R_k 刻度。"""
    ax.plot([4.75 + x0, 4.75 + x0], [9.5, 36.5], 'k-', lw=1.3)
    ax.plot([4.75 + x0, 44.5 + x0], [9.5, 9.5], 'k-', lw=1.3)
    ax.text(3.0 + x0, 35.4, r'$t$', ha='right', va='center')
    ax.text(45.4 + x0, 9.5, r'$x$', ha='left', va='center')
    for xt, lab in ((rj, r'$R_j$'), (rk, r'$R_k$')):
        ax.plot([xt + x0, xt + x0], [9.5, 10.8], 'k-', lw=1.3)
        ax.text(xt + x0, 6.9, lab, ha='center', va='center')


def fig_49():
    fig, ax = _canvas(4.8, 2.1)
    # ---------- (a) ----------
    P1 = (17.75, 28.75)                 # 左 X（湮灭）
    P2 = (34.25, 28.75)                 # 右 X（产生）
    _panel_axes(ax, 0.0)
    _wavy(ax, P1, P2, n=7, amp=0.5, lw=1.8)
    # 左下汇聚双线（电子+空穴一起走到 R_j）
    lo0, lo1 = (15.75, 15.0), (18.25, 14.9)
    _seg(ax, lo0, P1)
    _seg_arrow(ax, lo0, P1, 0.50, 0.65)
    _seg(ax, lo1, P1)
    _seg_arrow(ax, lo1, P1, 0.50, 0.65)
    # 右上发散双线（在 R_k 重新产生）
    up0, up1 = (33.0, 42.0), (35.5, 42.25)
    _seg(ax, P2, up0)
    _seg_arrow(ax, P2, up0, 0.85, 1.0)
    _seg(ax, P2, up1)
    _seg_arrow(ax, P2, up1, 0.85, 1.0)
    ax.text(16.9, 31.3, r'$X$', ha='center', va='center')
    ax.text(25.3, 26.6, r'$T$', ha='center', va='center')
    ax.text(34.9, 26.6, r'$X$', ha='center', va='center')
    ax.text(23.3, 3.4, '(a)', ha='center', va='center')
    # ---------- (b) ----------
    dx = 58.0
    _panel_axes(ax, dx, rj=14.25, rk=27.75)
    # U 细水平线
    ax.plot([10.25 + dx, 35.25 + dx], [27.75, 27.75], 'k-', lw=1.0)
    ax.text(37.0 + dx, 27.9, r'$U$', ha='left', va='center')
    # 电子阶梯：R_j 上升 -> 顶部横跳(b_jk) -> R_k 处继续上升
    eA, eB = (12.9 + dx, 11.6), (13.1 + dx, 31.35)    # 左竖
    eC = (27.25 + dx, 31.4)                           # 横跳右端
    eD = (27.15 + dx, 41.0)                           # 继续上升末端
    _seg(ax, eA, eB)
    _seg_arrow(ax, eA, eB, 0.28, 0.40)
    _seg(ax, eB, eC)
    _seg(ax, eC, eD)
    _seg_arrow(ax, eC, eD, 0.80, 1.0)
    ax.text(32.5 + dx, 31.65, r'$b_{jk}$', ha='center', va='center')
    # 空穴阶梯：R_k 上方下行 -> 穿 U -> 低处横跳(b_kj) -> R_j 旁下行
    hA, hB = (30.4 + dx, 41.0), (30.4 + dx, 20.5)
    hC = (15.6 + dx, 20.25)
    hD = (15.75 + dx, 11.5)
    _seg(ax, hA, hB)
    _seg_arrow(ax, hA, hB, 0.28, 0.40)
    _seg(ax, hB, hC)
    _seg(ax, hC, hD)
    _seg_arrow(ax, hC, hD, 0.62, 0.80)
    ax.text(32.6 + dx, 20.4, r'$b_{kj}$', ha='center', va='center')
    ax.text(23.0 + dx, 3.4, '(b)', ha='center', va='center')
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 46)
    _save(fig, '49')


# ----------------------------------------------------------------------
def fig_50():
    fig, ax = _canvas(2.9, 3.0)
    # 坐标轴（无标注 L 形）
    ax.plot([4.0, 4.0], [8.0, 57.7], 'k-', lw=1.3)
    ax.plot([4.0, 55.3], [8.0, 8.0], 'k-', lw=1.3)
    A, B = (29.8, 26.0), (37.7, 25.9)
    _wavy(ax, A, B, n=3, amp=0.55, lw=1.8)
    # 左入射线（箭头指向 A）
    l1 = (17.7, 15.2)
    _seg(ax, l1, A)
    _seg_arrow(ax, l1, A, 0.30, 0.46)
    # A 向下的出线（时间反向）
    l2 = (27.2, 12.1)
    _seg(ax, A, l2)
    _seg_arrow(ax, A, l2, 0.82, 1.0)
    # B 向左上的长出线
    l3 = (25.2, 42.1)
    _seg(ax, B, l3)
    _seg_arrow(ax, B, l3, 0.85, 1.0)
    # 右上入射线（箭头指向 B）
    l4 = (49.3, 39.5)
    _seg(ax, l4, B)
    _seg_arrow(ax, l4, B, 0.10, 0.24)
    ax.set_xlim(0, 58)
    ax.set_ylim(0, 60)
    _save(fig, '50')


# ----------------------------------------------------------------------
def fig_51():
    fig, ax = _canvas(2.8, 2.95)
    ax.plot([7.2, 7.2], [7.7, 56.8], 'k-', lw=1.3)
    ax.plot([7.2, 54.0], [7.7, 7.7], 'k-', lw=1.3)
    V = (26.1, 23.5)
    # 竖直波纹（辐射的光子）
    _wavy(ax, V, (25.8, 33.5), n=4, amp=0.55, lw=1.8)
    # 左腿（下行、时间反向）与右腿（上行入射）
    l1 = (18.3, 12.25)
    _seg(ax, V, l1)
    _seg_arrow(ax, V, l1, 0.82, 1.0)
    l2 = (34.5, 12.75)
    _seg(ax, l2, V)
    _seg_arrow(ax, l2, V, 0.44, 0.58)
    ax.set_xlim(0, 56)
    ax.set_ylim(0, 59)
    _save(fig, '51')


# ----------------------------------------------------------------------
def fig_52():
    fig, ax = _canvas(4.6, 3.25)
    # 坐标轴与四个刻度
    ax.plot([4.85, 4.85], [10.6, 58.2], 'k-', lw=1.4)
    ax.plot([4.85, 88.5], [10.6, 10.6], 'k-', lw=1.4)
    ax.text(89.7, 10.4, r'$x$', ha='left', va='center')
    for xt, lab in ((23.0, r'$R_i$'), (40.0, r'$R_j$'),
                    (57.6, r'$R_k$'), (74.2, r'$R_l$')):
        ax.plot([xt, xt], [10.6, 12.1], 'k-', lw=1.3)
        ax.text(xt, 7.2, lab, ha='center', va='center')
    lwW = 1.8
    # ---- R_i 处 backwards 折线 b_i ----
    Pi = (23.2, 38.2)
    ax.text(21.9, 41.0, r'$b_i$', ha='center', va='center')
    la = (20.5, 19.1)
    _seg(ax, Pi, la, lwW)
    _seg_arrow(ax, Pi, la, 0.82, 1.0, lw=lwW)
    lb = (26.1, 19.7)
    _seg(ax, lb, Pi, lwW)
    _seg_arrow(ax, lb, Pi, 0.10, 0.26, lw=lwW)
    # ---- wavy b_i -> b_j ----
    Pj = (39.7, 38.2)
    _wavy(ax, Pi, Pj, n=6, amp=0.6, lw=lwW)
    ax.text(38.6, 41.2, r'$b_j$', ha='center', va='center')
    # ---- R_j 处小圈：b_j -> b_j^\dagger ----
    Pjd = (40.2, 21.5)
    ax.text(39.4, 17.6, r'$b_j^\dagger$', ha='center', va='center')
    w1, h1 = 1.75, Pj[1] - Pjd[1]
    L1 = _bezier(Pjd, (Pjd[0] - w1, Pjd[1] + 0.60 * h1),
                 (Pj[0] - w1, Pj[1] - 0.55 * h1), Pj)
    R1 = _bezier(Pjd, (Pjd[0] + w1, Pjd[1] + 0.60 * h1),
                 (Pj[0] + w1, Pj[1] - 0.55 * h1), Pj)
    ax.plot(L1[:, 0], L1[:, 1], 'k-', lw=lwW)
    ax.plot(R1[:, 0], R1[:, 1], 'k-', lw=lwW)
    _arrow(ax, tuple(L1[38]), tuple(L1[52]), ms=14, lw=lwW)      # 左侧向上
    _arrow(ax, tuple(R1[42]), tuple(R1[24]), ms=14, lw=lwW)      # 右侧向下
    # ---- wavy b_j^\dagger -> b_k^\dagger ----
    Pkd = (57.3, 21.3)
    _wavy(ax, Pjd, Pkd, n=6, amp=0.6, lw=lwW)
    ax.text(56.8, 17.9, r'$b_k^\dagger$', ha='center', va='center')
    # ---- R_k 处大圈：b_k^\dagger -> b_k ----
    Pk = (57.6, 46.4)
    ax.text(56.3, 49.4, r'$b_k$', ha='center', va='center')
    w2, h2 = 2.6, Pk[1] - Pkd[1]
    L2 = _bezier(Pkd, (Pkd[0] - w2, Pkd[1] + 0.58 * h2),
                 (Pk[0] - w2, Pk[1] - 0.52 * h2), Pk)
    R2 = _bezier(Pkd, (Pkd[0] + w2, Pkd[1] + 0.58 * h2),
                 (Pk[0] + w2, Pk[1] - 0.52 * h2), Pk)
    ax.plot(L2[:, 0], L2[:, 1], 'k-', lw=lwW)
    ax.plot(R2[:, 0], R2[:, 1], 'k-', lw=lwW)
    _arrow(ax, tuple(L2[42]), tuple(L2[58]), ms=14, lw=lwW)      # 左侧向上
    _arrow(ax, tuple(R2[44]), tuple(R2[26]), ms=14, lw=lwW)      # 右侧向下
    # ---- wavy b_k -> b_l^\dagger ----
    Pl = (74.5, 46.4)
    _wavy(ax, Pk, Pl, n=6, amp=0.6, lw=lwW)
    ax.text(77.0, 45.9, r'$b_l^\dagger$', ha='left', va='center')
    # ---- R_l 处上方 V 形 ----
    ma = (71.5, 63.0)
    _seg(ax, Pl, ma, lwW)
    _seg_arrow(ax, Pl, ma, 0.84, 1.0, lw=lwW)
    mb = (77.3, 63.0)
    _seg(ax, mb, Pl, lwW)
    _seg_arrow(ax, mb, Pl, 0.16, 0.32, lw=lwW)
    ax.set_xlim(0, 93)
    ax.set_ylim(0, 66)
    _save(fig, '52')


if __name__ == '__main__':
    for f in (fig_46, fig_47, fig_48, fig_49, fig_50, fig_51, fig_52):
        f()
        print('done:', f.__name__)
