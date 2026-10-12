# -*- coding: utf-8 -*-
"""
朗道《统计物理学I》（卷5）中文重排本 插图重绘 第二批：图12-图19
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p-237/238/242/243/244）。
图12 §81 T-V 两相区（杠杆规则）；图13 §81 P-T 三相点；
图14 §81 三相点邻域 T-V 图；图15 §81 两相化学势曲线；
图16 §83 临界压强对温度；图17 §83 T-V 临界点；
图18 §83 P-V 等温线与双节点/旋节线；图19 §84 范德瓦尔斯等温线。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Circle
from scipy.interpolate import PchipInterpolator

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = r"E:\AI整理书籍\朗道理论物理教程\卷5统计物理I\重排本"
FIGD = os.path.join(BASE, 'figures')
PRED = os.path.join(FIGD, 'preview')
os.makedirs(PRED, exist_ok=True)

LW_MAIN, LW_AUX, LW_HATCH = 1.2, 0.8, 0.55


def save(fig, n):
    fig.savefig(os.path.join(FIGD, f'fig{n}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRED, f'fig{n}.png'), bbox_inches='tight',
                pad_inches=0.03, dpi=220)
    plt.close(fig)


def arrow_axis(ax, x0, y0, x1, y1, lw=LW_MAIN):
    """带箭头的坐标轴（自绘）"""
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=12))


def plain_axes(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def bezier(p0, p1, p2, n=100):
    """二次贝塞尔"""
    t = np.linspace(0, 1, n)[:, None]
    p = (1 - t) ** 2 * np.asarray(p0) + 2 * t * (1 - t) * np.asarray(p1) \
        + t ** 2 * np.asarray(p2)
    return p[:, 0], p[:, 1]


def curve(ax, pts, lw=LW_MAIN, ls='-', dashes=None, n=300):
    """Pchip 平滑曲线（允许 x 递减输入，内部排序后绘制）"""
    pts = np.asarray(pts, float)
    if pts[0, 0] > pts[-1, 0]:
        order = np.argsort(pts[:, 0])
        xs, ys = pts[order, 0], pts[order, 1]
    else:
        xs, ys = pts[:, 0], pts[:, 1]
    f = PchipInterpolator(xs, ys)
    x = np.linspace(xs[0], xs[-1], n)
    y = f(x)
    kw = {'dashes': dashes} if dashes else {}
    ax.plot(x, y, color='k', lw=lw, ls=ls, **kw)
    return f


def strict_inc(pts, eps=0.006):
    """强制 x 严格递增（近竖直曲线取值抖动时使用）"""
    pts = np.array(pts, float)
    for i in range(1, len(pts)):
        if pts[i, 0] <= pts[i - 1, 0]:
            pts[i, 0] = pts[i - 1, 0] + eps
    return pts


def hline_hatch(ax, xlo, xhi, y0, y1, dy, lw=LW_HATCH, clip_poly=None):
    """水平线阴影，clip_poly 为闭合多边形(数组)"""
    clip = None
    if clip_poly is not None:
        clip = Polygon(clip_poly, closed=True, transform=ax.transData,
                       facecolor='none', edgecolor='none')
        ax.add_patch(clip)
    ys = np.arange(y0 + dy / 2, y1, dy)
    for y in ys:
        xx0 = xlo(y) if callable(xlo) else xlo
        xx1 = xhi(y) if callable(xhi) else xhi
        ln, = ax.plot([xx0, xx1], [y, y], color='k', lw=lw)
        if clip is not None:
            ln.set_clip_path(clip)


# ---------------------------------------------------------------- 图12
def fig_12():
    """§81 T-V 图：两相共存区（水平线阴影），a 为区内一点，
    过 a 的水平线交边界于 1、2（杠杆规则）"""
    fig, ax = plt.subplots(figsize=(2.6, 2.15))
    plain_axes(ax)
    ax.set_xlim(-1.75, 11.7)
    ax.set_ylim(-1.8, 9.3)

    arrow_axis(ax, 0, 0, 0, 8.6)
    arrow_axis(ax, 0, 0, 11.2, 0)
    ax.text(-0.55, 8.1, r'$T$', fontsize=11, ha='center', va='center')
    ax.text(10.65, -0.65, r'$V$', fontsize=11, ha='center', va='center')

    # 共存区边界：上/下水平边 + 外凸两侧弧
    ytop, ybot = 4.55, 1.56
    lbx, lby = bezier((3.45, ytop), (2.30, 3.06), (2.19, ybot))
    rbx, rby = bezier((6.40, ytop), (7.14, 3.07), (7.40, ybot))
    poly = np.concatenate([
        np.column_stack([lbx[::-1], lby[::-1]]),
        [[2.19, ybot], [7.40, ybot]],
        np.column_stack([rbx, rby]),
        [[6.40, ytop], [3.45, ytop]],
    ])
    ax.plot([2.19, 7.40], [ybot, ybot], 'k-', lw=1.25)
    ax.plot([3.45, 6.40], [ytop, ytop], 'k-', lw=1.25)
    ax.plot(lbx, lby, 'k-', lw=1.25)
    ax.plot(rbx, rby, 'k-', lw=1.25)

    # 水平线阴影（内部按左右边界函数裁剪）
    fl = PchipInterpolator(lby[::-1], lbx[::-1])
    fr = PchipInterpolator(rby[::-1], rbx[::-1])
    hline_hatch(ax, fl, fr, ybot, ytop, 0.30, clip_poly=poly)

    # 过 a 的水平连线（杠杆规则），在字母 a 处留缺口
    ya = 3.00
    x1, x2 = float(fl(np.array([ya]))[0]), float(fr(np.array([ya]))[0])
    ax.plot([x1, 3.28], [ya, ya], 'k-', lw=0.7)
    ax.plot([4.05, x2], [ya, ya], 'k-', lw=0.7)
    ax.add_patch(Circle((3.48, ya), 0.10, facecolor='white',
                        edgecolor='k', lw=0.9, zorder=5))
    ax.text(3.82, 3.38, r'$a$', fontsize=10, ha='center', va='center')

    ax.text(x1 - 0.25, 2.80, '1', fontsize=10, ha='right', va='center')
    ax.text(x2 + 0.25, 3.05, '2', fontsize=10, ha='left', va='center')
    ax.text(1.56, 4.05, 'I', fontsize=10.5, ha='center', va='center')
    ax.text(8.66, 4.05, 'II', fontsize=10.5, ha='center', va='center')
    save(fig, 12)


# ---------------------------------------------------------------- 图13
def fig_13():
    """§81 P-T 三相点：升华/汽化/熔化曲线交于三相点，虚线标 P_tr、T_tr"""
    fig, ax = plt.subplots(figsize=(2.45, 2.35))
    plain_axes(ax)
    ax.set_xlim(-1.2, 6.1)
    ax.set_ylim(-1.2, 5.6)

    arrow_axis(ax, 0, 0, 0, 5.05)
    arrow_axis(ax, 0, 0, 5.6, 0)
    ax.text(-0.52, 4.65, r'$P$', fontsize=11, ha='center', va='center')
    ax.text(5.22, -0.62, r'$T$', fontsize=11, ha='center', va='center')

    tr = (2.94, 1.66)   # 三相点
    # 熔化曲线（近竖直，略右倾）
    curve(ax, [tr, (3.05, 2.24), (3.16, 2.88), (3.24, 3.39), (3.26, 3.77)])
    # 汽化曲线（右上，微凹向上）
    curve(ax, [tr, (3.26, 1.81), (3.59, 2.01), (3.92, 2.23), (4.26, 2.48),
               (4.59, 2.74), (4.91, 3.01), (5.10, 3.15)])
    # 升华曲线（左下，凹向上）
    curve(ax, [tr, (2.68, 1.43), (2.41, 1.22), (2.11, 1.04), (1.81, 0.92),
               (1.58, 0.84)])

    ax.plot([0, tr[0]], [tr[1], tr[1]], 'k--', lw=0.9, dashes=(5, 2.4))
    ax.plot([tr[0], tr[0]], [0, tr[1]], 'k--', lw=0.9, dashes=(5, 2.4))
    ax.text(-0.18, tr[1], r'$P_{\rm tr}$', fontsize=10, ha='right', va='center')
    ax.text(tr[0], -0.64, r'$T_{\rm tr}$', fontsize=10, ha='center', va='center')

    ax.text(2.14, 2.81, 'III', fontsize=10.5, ha='center', va='center')
    ax.text(3.89, 2.81, 'II', fontsize=10.5, ha='center', va='center')
    ax.text(3.94, 1.17, 'I', fontsize=10.5, ha='center', va='center')
    save(fig, 13)


# ---------------------------------------------------------------- 图14
def fig_14():
    """§81 三相点邻域 T-V 图：三个两相区 I-II、II-III、I-III（水平线阴影），
    单相区 I、II、III，T_tr 处三点 1、2、3"""
    fig, ax = plt.subplots(figsize=(2.95, 2.55))
    plain_axes(ax)
    ax.set_xlim(-1.4, 9.0)
    ax.set_ylim(-1.65, 8.7)

    arrow_axis(ax, 0, 0, 0, 8.0)
    arrow_axis(ax, 0, 0, 8.5, 0)
    ax.text(-0.52, 7.45, r'$T$', fontsize=11, ha='center', va='center')
    ax.text(8.05, -0.75, r'$V$', fontsize=11, ha='center', va='center')

    p1 = (1.27, 3.55)   # 点1
    p2 = (3.93, 3.56)   # 点2（三相点）
    p3 = (6.40, 3.56)   # 点3
    yt = 5.91           # 上部两条带顶边
    yb = 1.43           # 底带底边

    # 边界曲线（用采样点拟合）
    lw_edge = PchipInterpolator([3.55, 4.32, 5.00, 5.62, 5.92],
                                [1.27, 1.30, 1.33, 1.36, 1.37])    # I-II 左
    ww_left = PchipInterpolator([3.56, 4.32, 5.00, 5.62, 5.90],
                                [3.93, 3.76, 3.63, 3.52, 3.52])    # 楔左
    ww_right = PchipInterpolator([3.56, 4.32, 5.00, 5.62, 5.90],
                                 [3.93, 4.34, 4.69, 5.10, 5.10])   # 楔右
    rw_edge = PchipInterpolator([3.56, 4.32, 5.00, 5.62, 5.92],
                                [6.40, 6.67, 6.84, 6.98, 6.98])    # II-III 右
    bl_x, bl_y = bezier(p1, (1.13, 2.50), (1.13, yb))              # 底带左
    br_x, br_y = bezier(p3, (6.80, 2.50), (6.80, yb))              # 底带右

    # 画实线边界
    yy = np.linspace(3.55, 5.92, 100)
    ax.plot(lw_edge(yy), yy, 'k-', lw=1.25)
    ax.plot(ww_left(yy), yy, 'k-', lw=1.25)
    ax.plot(ww_right(yy), yy, 'k-', lw=1.25)
    ax.plot(rw_edge(yy), yy, 'k-', lw=1.25)
    ax.plot(bl_x, bl_y, 'k-', lw=1.25)
    ax.plot(br_x, br_y, 'k-', lw=1.25)
    ax.plot([p1[0], p3[0]], [p1[1], p3[1]], 'k-', lw=1.25)         # 带顶边
    ax.plot([1.13, 6.80], [yb, yb], 'k-', lw=1.25)                 # 带底边
    ax.plot([lw_edge(5.92), ww_left(5.90)], [5.92, 5.90], 'k-', lw=1.25)
    ax.plot([ww_right(5.90), rw_edge(5.92)], [5.90, 5.92], 'k-', lw=1.25)

    # 三个两相区（水平线阴影）
    ysu = np.linspace(3.56, 5.90, 60)
    hline_hatch(ax, lambda y: float(lw_edge(y)), lambda y: float(ww_left(y)),
                3.56, 5.91, 0.28,
                clip_poly=np.column_stack([
                    np.concatenate([lw_edge(ysu), ww_left(ysu[::-1])]),
                    np.concatenate([ysu, ysu[::-1]])]))
    hline_hatch(ax, lambda y: float(ww_right(y)), lambda y: float(rw_edge(y)),
                3.56, 5.91, 0.28,
                clip_poly=np.column_stack([
                    np.concatenate([ww_right(ysu), rw_edge(ysu[::-1])]),
                    np.concatenate([ysu, ysu[::-1]])]))
    ysl = np.linspace(yb, 3.55, 60)
    hline_hatch(ax, lambda y: float(PchipInterpolator(bl_y[::-1], bl_x[::-1])(y)),
                lambda y: float(PchipInterpolator(br_y[::-1], br_x[::-1])(y)),
                yb, 3.55, 0.28,
                clip_poly=np.column_stack([
                    np.concatenate([bl_x[::-1], br_x]),
                    np.concatenate([bl_y[::-1], br_y])]))

    # T_tr 虚线
    ax.plot([0, p1[0]], [p1[1], p1[1]], 'k--', lw=0.9, dashes=(5, 2.4))
    ax.text(-0.50, 3.42, r'$T_{\rm tr}$', fontsize=10, ha='center', va='center')

    # 标注（阴影区内的加白底）
    bbox = dict(facecolor='white', edgecolor='none', pad=0.6)
    ax.text(1.05, 4.32, 'I', fontsize=10.5, ha='center', va='center')
    ax.text(2.48, 4.73, 'I–II', fontsize=9.5, ha='center', va='center', bbox=bbox)
    ax.text(4.10, 5.02, 'II', fontsize=10.5, ha='center', va='center', bbox=bbox)
    ax.text(5.83, 4.88, 'II–III', fontsize=9.5, ha='center', va='center', bbox=bbox)
    ax.text(7.35, 4.32, 'III', fontsize=10.5, ha='center', va='center')
    ax.text(2.43, 3.05, '1', fontsize=10, ha='center', va='center', bbox=bbox)
    ax.text(3.90, 3.05, '2', fontsize=10, ha='center', va='center', bbox=bbox)
    ax.text(6.86, 3.72, '3', fontsize=10, ha='center', va='center')
    ax.text(3.93, 1.87, 'I–III', fontsize=9.5, ha='center', va='center', bbox=bbox)
    save(fig, 14)


# ---------------------------------------------------------------- 图15
def fig_15():
    """§81 两相化学势对温度：μ1(T)、μ2(T) 交于 T0（虚线），
    T<T0 时第一相稳定"""
    fig, ax = plt.subplots(figsize=(2.9, 2.5))
    plain_axes(ax)
    ax.set_xlim(-1.05, 9.5)
    ax.set_ylim(-1.35, 8.0)

    arrow_axis(ax, 0, 0, 0, 7.25)
    arrow_axis(ax, 0, 0, 9.05, 0)
    ax.text(-0.52, 6.85, r'$\mu$', fontsize=11, ha='center', va='center')
    ax.text(8.62, -0.62, r'$T$', fontsize=11, ha='center', va='center')

    # 两条直线：μ1 平缓、μ2 陡
    x1a, y1a, x1b, y1b = 1.16, 5.66, 6.43, 2.81
    x2a, y2a, x2b, y2b = 1.57, 6.58, 5.61, 1.89
    ax.plot([x1a, x1b], [y1a, y1b], 'k-', lw=1.3)
    ax.plot([x2a, x2b], [y2a, y2b], 'k-', lw=1.3)
    s1 = (y1b - y1a) / (x1b - x1a)
    s2 = (y2b - y2a) / (x2b - x2a)
    xc = (y2a - s2 * x2a - y1a + s1 * x1a) / (s1 - s2)
    yc = y1a + s1 * (xc - x1a)
    ax.plot([xc, xc], [0, yc], 'k--', lw=0.9, dashes=(5, 2.4))
    ax.text(xc, -0.64, r'$T_0$', fontsize=10, ha='center', va='center')

    ax.text(x1b + 0.14, y1b + 0.18, r'$\mu_1$', fontsize=10,
            ha='left', va='center')
    ax.text(x2b + 0.12, y2b - 0.02, r'$\mu_2$', fontsize=10,
            ha='left', va='center')
    save(fig, 15)


# ---------------------------------------------------------------- 图16
def fig_16():
    """§83 饱和蒸气压曲线：从原点升至临界点 (Tc, Pc)，虚线投到两轴"""
    fig, ax = plt.subplots(figsize=(2.35, 1.75))
    plain_axes(ax)
    ax.set_xlim(-1.2, 7.9)
    ax.set_ylim(-1.0, 4.6)

    arrow_axis(ax, 0, 0, 0, 4.0)
    arrow_axis(ax, 0, 0, 7.4, 0)
    ax.text(-0.5, 3.62, r'$P$', fontsize=11, ha='center', va='center')
    ax.text(7.05, -0.64, r'$T$', fontsize=11, ha='center', va='center')

    kc = (5.74, 2.78)
    curve(ax, [(0, 0), (0.6, 0.06), (1.2, 0.19), (1.9, 0.42), (2.6, 0.72),
               (3.3, 1.09), (4.0, 1.51), (4.6, 1.91), (5.1, 2.28),
               (5.45, 2.54), kc],
          lw=1.35)

    ax.plot([0, kc[0]], [kc[1], kc[1]], 'k--', lw=0.9, dashes=(5, 2.4))
    ax.plot([kc[0], kc[0]], [0, kc[1]], 'k--', lw=0.9, dashes=(5, 2.4))
    ax.text(-0.20, kc[1], r'$P_{\rm c}$', fontsize=10, ha='right', va='center')
    ax.text(kc[0], -0.66, r'$T_{\rm c}$', fontsize=10, ha='center', va='center')
    save(fig, 16)


# ---------------------------------------------------------------- 图17
def fig_17():
    """§83 T-V 临界点：钟形共存曲线（水平线阴影），K 为临界点，
    虚线标 Tc、Vc"""
    fig, ax = plt.subplots(figsize=(2.95, 2.3))
    plain_axes(ax)
    ax.set_xlim(-1.35, 7.9)
    ax.set_ylim(-1.4, 6.2)

    arrow_axis(ax, 0, 0, 0, 5.5)
    arrow_axis(ax, 0, 0, 7.45, 0)
    ax.text(-0.52, 5.1, r'$T$', fontsize=11, ha='center', va='center')
    ax.text(7.05, -0.7, r'$V$', fontsize=11, ha='center', va='center')

    pts = [(0.76, 1.13), (0.91, 1.44), (1.21, 1.99), (1.61, 2.60),
           (2.12, 3.21), (2.61, 3.67), (2.85, 3.82), (3.01, 3.89),
           (3.20, 3.86), (3.44, 3.80), (3.95, 3.52), (4.44, 3.07),
           (4.96, 2.50), (5.48, 1.93), (5.86, 1.44), (6.09, 1.13)]
    p = np.asarray(pts, float)
    fd = PchipInterpolator(p[:, 0], p[:, 1])
    xx = np.linspace(0.76, 6.09, 300)
    ax.plot(xx, fd(xx), 'k-', lw=1.35)
    # 底部弦（最低一条水平连线）
    ax.plot([0.85, 5.84], [1.29, 1.29], 'k-', lw=1.0)

    poly = np.column_stack([xx, fd(xx)])
    ylo, yhi = 1.29, 3.86
    ys_d = fd(xx)

    def dome_span(y):
        """钟形曲线内某高度的水平弦左右端"""
        idx = np.where(ys_d >= y)[0]
        return xx[idx[0]] + 0.02, xx[idx[-1]] - 0.02

    hline_hatch(ax, lambda y: dome_span(y)[0], lambda y: dome_span(y)[1],
                ylo, yhi, 0.24, clip_poly=poly)

    # 虚线 Tc、Vc
    ax.plot([0, 3.01], [3.89, 3.89], 'k--', lw=0.9, dashes=(5, 2.4))
    ax.plot([3.01, 3.01], [0, 3.89], 'k--', lw=0.9, dashes=(5, 2.4))
    ax.text(-0.22, 3.89, r'$T_{\rm c}$', fontsize=10, ha='right', va='center')
    ax.text(2.73, 4.30, r'$K$', fontsize=11, ha='center', va='center')
    ax.text(2.89, -0.72, r'$V_{\rm c}$', fontsize=10, ha='center', va='center')
    save(fig, 17)


# ---------------------------------------------------------------- 图18
def fig_18():
    """§83 P-V 图：液体/气体等温线 abc、def；实线双节点曲线 bKe；
    虚线亚稳边界 cKd（旋节线）；水平虚线 be 为平衡相变段。
    液、气 为均单相区标注"""
    fig, ax = plt.subplots(figsize=(3.55, 2.8))
    plain_axes(ax)
    ax.set_xlim(-1.4, 11.15)
    ax.set_ylim(-1.45, 8.8)

    arrow_axis(ax, 0, 0, 0, 8.05)
    arrow_axis(ax, 0, 0, 10.65, 0)
    ax.text(-0.55, 7.62, r'$P$', fontsize=11, ha='center', va='center')
    ax.text(10.22, -0.7, r'$V$', fontsize=11, ha='center', va='center')

    b_pt, c_pt = (1.75, 3.11), (2.73, 2.33)
    d_pt, e_pt, f_pt = (4.74, 3.81), (6.09, 3.11), (8.96, 1.54)
    K = (3.99, 4.60)

    # 等温线 abc（液体，过热液体段 bc 为亚稳延伸）
    curve(ax, [(0.75, 7.90), (0.83, 6.90), (0.97, 5.80), (1.15, 4.85),
               (1.36, 4.12), (1.55, 3.60), b_pt, (1.95, 2.92), (2.15, 2.77),
               (2.35, 2.63), (2.52, 2.51), (2.65, 2.41), c_pt], lw=1.35)
    # 等温线 def（气体，de 为过冷蒸气段）
    curve(ax, [d_pt, (4.90, 3.78), (5.15, 3.66), (5.51, 3.43), (5.99, 3.20),
               (6.45, 2.94), (6.94, 2.65), (7.43, 2.36), (8.00, 2.04),
               (8.58, 1.75), f_pt], lw=1.35)

    # 双节点（相平衡曲线，实线）b-K-e
    curve(ax, [(0.86, 1.11), (1.01, 1.75), (1.26, 2.33), (1.47, 2.77),
               b_pt, (2.07, 3.52), (2.45, 3.96), (2.87, 4.31), (3.42, 4.55),
               (3.70, 4.59), (3.90, 4.598), K, (4.25, 4.52), (4.56, 4.22),
               (5.14, 3.81), (5.71, 3.43),
               e_pt, (6.57, 2.77), (7.03, 2.33), (7.52, 1.89), (8.04, 0.96)],
          lw=1.35)

    # 旋节线（等温线终点轨迹，虚线）A-c-K-d-B
    curve(ax, [(2.64, 0.76), (2.66, 1.20), (2.70, 1.70), (2.72, 2.10),
               c_pt, (2.81, 2.79), (2.99, 3.29), (3.21, 3.73), (3.56, 4.17),
               (3.80, 4.45), K, (4.42, 4.22), d_pt, (5.02, 3.37), (5.31, 2.91),
               (5.57, 2.42), (5.71, 1.92), (5.78, 1.46), (5.80, 0.99)],
          lw=0.95, ls=(0, (5, 2.6)))

    # 平衡相变水平虚线 b-e
    ax.plot([b_pt[0], e_pt[0]], [b_pt[1], e_pt[1]], 'k--', lw=0.95,
            dashes=(5, 2.6))

    # 标注
    ax.text(0.97, 7.92, r'$a$', fontsize=10.5, ha='left', va='center')
    ax.text(1.60, 3.56, r'$b$', fontsize=10.5, ha='center', va='center')
    ax.text(3.01, 2.33, r'$c$', fontsize=10.5, ha='left', va='center')
    ax.text(4.28, 3.92, r'$d$', fontsize=10.5, ha='center', va='center')
    ax.text(6.24, 3.44, r'$e$', fontsize=10.5, ha='center', va='center')
    ax.text(8.70, 1.90, r'$f$', fontsize=10.5, ha='center', va='center')
    ax.text(K[0], 4.97, r'$K$', fontsize=11, ha='center', va='center')
    ax.text(2.64, 0.48, r'$A$', fontsize=10.5, ha='center', va='center')
    ax.text(5.80, 0.62, r'$B$', fontsize=10.5, ha='center', va='center')
    ax.text(0.55, 3.29, '液', fontsize=10.5, ha='center', va='center')
    ax.text(7.86, 3.32, '气', fontsize=10.5, ha='center', va='center')
    save(fig, 18)


# ---------------------------------------------------------------- 图19
def fig_19():
    """§84 范德瓦尔斯等温线：T>Tc 两条单调、临界等温线过 K、
    T<Tc 三条（亚稳段实线、(∂P/∂V)_T>0 不稳定段用点线）；
    水平点划线为麦克斯韦平衡段；虚线为两相共存曲线（过水平线段端点，
    顶点相切于 K）；阴影面积相等（一条等温线）"""
    fig, ax = plt.subplots(figsize=(3.3, 4.1))
    plain_axes(ax)
    ax.set_xlim(-1.4, 9.2)
    ax.set_ylim(-1.55, 11.4)

    arrow_axis(ax, 0, 0, 0, 10.65)
    arrow_axis(ax, 0, 0, 8.4, 0)
    ax.text(-0.52, 10.2, r'$P$', fontsize=11, ha='center', va='center')
    ax.text(7.98, -0.7, r'$V$', fontsize=11, ha='center', va='center')

    K = (2.14, 6.73)
    XR = 8.35     # 曲线右端

    # --- 液体分支（近竖直陡降，底部拐入极小值）---
    def liquid(top_x, ytop, swing):
        """swing: (x_min, y_min)；分支先保持近竖直，接近底部再拐入极小值"""
        pts = [(top_x, ytop)]
        for yy in np.arange(ytop - 1.2, swing[1], -1.6):
            frac = (ytop - yy) / (ytop - swing[1])
            pts.append((top_x + (swing[0] - top_x) * frac ** 2.6, yy))
        pts.append(swing)
        return pts

    # 两条 T>Tc 等温线（单调）
    curve(ax, [(1.60, 10.5), (1.85, 9.88), (2.20, 9.55), (2.70, 9.12),
               (3.51, 8.33), (4.41, 7.52), (5.40, 6.68), (6.44, 5.84),
               (7.49, 5.05), (XR, 4.42)], lw=1.3)
    curve(ax, [(1.50, 10.5), (1.68, 10.02), (1.95, 9.86), (2.40, 9.60),
               (2.99, 9.00), (3.81, 8.20), (4.72, 7.32), (5.62, 6.51),
               (6.60, 5.68), (7.56, 4.85), (XR, 4.20)], lw=1.3)

    # 临界等温线（K 处拐点、水平切线）
    curve(ax, [(1.40, 10.5), (1.48, 8.5), (1.58, 7.40), (1.75, 6.88),
               (1.94, 6.76), K, (2.34, 6.70), (2.60, 6.55), (2.92, 6.01),
               (3.44, 5.56), (4.05, 5.11), (4.72, 4.66), (5.46, 4.21),
               (6.21, 3.76), (6.97, 3.31), (7.71, 2.86), (XR, 2.47)], lw=1.3)

    # --- 三条 T<Tc 亚临界等温线 ---
    mu_min, mu_max = (1.64, 5.55), (2.60, 5.90)     # Mu
    m1_min, m1_max = (1.64, 3.38), (2.99, 4.89)     # M1（画阴影）
    m2_min, m2_max = (1.56, 2.05), (3.30, 4.10)     # M2
    tie1, tie2, tie3 = 5.74, 4.47, 3.42             # 三条水平线高度
    t1r, t2r, t3r = 2.99, 3.93, 4.68                # 各水平线右端（气体分支上）

    # 液体分支（实线），并求与各自水平线的交点（水平线左端）
    f_mu = curve(ax, liquid(1.30, 10.5, mu_min), lw=1.3)
    f_m1 = curve(ax, liquid(1.22, 10.5, m1_min), lw=1.3)
    f_m2 = curve(ax, liquid(1.14, 10.5, m2_min), lw=1.3)

    def branch_x_at(pts, yq):
        """液体分支上 y=yq 处的 x（按 y 反插值）"""
        p = np.asarray(pts, float)
        return float(PchipInterpolator(p[::-1, 1], p[::-1, 0])(yq))

    lp_mu, lp_m1, lp_m2 = (liquid(1.30, 10.5, mu_min),
                           liquid(1.22, 10.5, m1_min),
                           liquid(1.14, 10.5, m2_min))
    t1l, t2l, t3l = (branch_x_at(lp_mu, tie1), branch_x_at(lp_m1, tie2),
                     branch_x_at(lp_m2, tie3))

    # 不稳定段（点线）：极小 -> 极大
    def hump(mn, mx, n=6):
        pts = [mn]
        for i in range(1, n):
            u = i / n
            pts.append((mn[0] + (mx[0] - mn[0]) * u ** 0.85,
                        mn[1] + (mx[1] - mn[1]) * u ** 1.5))
        pts.append(mx)
        return pts

    curve(ax, hump(mu_min, mu_max), lw=1.15, ls=(0, (1, 1.5)))
    curve(ax, hump(m1_min, m1_max), lw=1.15, ls=(0, (1, 1.5)))
    curve(ax, hump(m2_min, m2_max), lw=1.15, ls=(0, (1, 1.5)))

    # 气体分支（实线，均保持在上邻曲线之下，右端渐平）
    curve(ax, [mu_max, (2.99, tie1), (3.60, 5.22), (4.30, 4.70), (5.10, 4.15),
               (6.00, 3.55), (7.00, 2.98), (7.80, 2.52), (XR, 1.96)], lw=1.3)
    curve(ax, [m1_max, (3.40, 4.70), (t2r, tie2), (4.60, 4.12), (5.40, 3.68),
               (6.30, 3.20), (7.20, 2.70), (7.90, 2.28), (XR, 1.50)], lw=1.3)
    curve(ax, [m2_max, (3.80, 3.90), (t3r, tie3), (5.40, 3.00), (6.20, 2.55),
               (7.10, 2.08), (7.90, 1.62), (XR, 1.05)], lw=1.3)

    # --- 麦克斯韦水平线段（点划线）---
    for y0, xl, xr in [(tie1, t1l, t1r), (tie2, t2l, t2r), (tie3, t3l, t3r)]:
        ax.plot([xl, xr], [y0, y0], color='k', lw=0.95,
                dashes=(7, 3, 1.5, 3))

    # --- 两相共存曲线（虚线）：过各水平线端点，顶部与 K 下方相触 ---
    Kap = (2.14, 6.68)   # 顶点略低于临界等温线
    bino = strict_inc([(0.92, 1.90), (0.96, 2.20), (1.02, 2.52), (1.15, 2.65),
                       (1.32, 2.95), (t3l, tie3),
                       (1.51, 3.90), (t2l, tie2), (1.56, 5.10), (t1l, tie1),
                       (1.80, 6.15), (1.98, 6.44), (2.08, 6.60), Kap,
                       (2.22, 6.63), (2.40, 6.44), (2.60, 6.22), (2.99, tie1),
                       (3.45, 5.15), (3.93, tie2), (4.35, 3.90),
                       (4.68, tie3), (5.00, 3.15), (5.24, 2.97)])
    curve(ax, list(map(tuple, bino)), lw=1.0, ls=(0, (5, 2.6)))

    # --- 阴影：对 M1 一条等温线的两块相等面积（斜线）---
    # 构造 M1 各段采样点
    m1_hump = hump(m1_min, m1_max, n=40)
    m1_liq_all = liquid(1.22, 10.5, m1_min)
    fl1 = PchipInterpolator([p[1] for p in m1_liq_all[::-1]],
                            [p[0] for p in m1_liq_all[::-1]])
    t2l = float(fl1(tie2))                       # 液体分支与水平线交点
    m1_gas_all = [m1_max, (3.40, 4.70), (t2r, tie2), (4.60, 4.12), (5.40, 3.68),
                  (6.30, 3.20), (7.20, 2.70), (7.90, 2.28), (XR, 1.50)]
    fh1 = PchipInterpolator([p[1] for p in m1_hump], [p[0] for p in m1_hump])
    xcross = float(fh1(tie2))                    # 点线上升段与水平线交点

    # 左块：水平线之下、液体分支与点线上升段之间
    left = [(t2l, tie2), (xcross, tie2)]
    left += [p for p in m1_hump if p[1] <= tie2][::-1]      # 交点 -> 极小
    left += [p for p in m1_liq_all if p[1] <= tie2][::-1]   # 极小 -> 交点
    ax.add_patch(Polygon(left, closed=True, facecolor='white',
                         edgecolor='none', hatch='//////', zorder=1))
    # 右块：水平线之上、点线上升段与气体分支之间（透镜形）
    right = [(xcross, tie2), (t2r, tie2)]
    right += [p for p in m1_gas_all if p[0] <= t2r]         # 交点 -> 极大
    right += [p for p in m1_hump if p[1] >= tie2][::-1]     # 极大 -> 交点
    ax.add_patch(Polygon(right, closed=True, facecolor='white',
                         edgecolor='none', hatch='//////', zorder=1))

    ax.text(2.20, 7.05, r'$K$', fontsize=11, ha='center', va='center')
    save(fig, 19)


if __name__ == '__main__':
    for i in range(12, 20):
        globals()[f'fig_{i}']()
        print(f'fig{i} done')
