# -*- coding: utf-8 -*-
"""
朗道《统计物理学I》（卷5）中文重排本 插图重绘 第三批：图20-图35
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p-270..276），逐幅测量比对。
内容：§97 平衡曲线（图20-30）、§98 相图举例（图31-35）。
图20-23、28-30、31-37 型图为三边框（左/下/右脊线，无上边）；
图24-27 为箭头坐标轴（T 上、P 右）。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = r"E:\AI整理书籍\朗道理论物理教程\卷5统计物理I\重排本"
FIGD = os.path.join(BASE, 'figures')
PRED = os.path.join(FIGD, 'preview')
os.makedirs(PRED, exist_ok=True)


def save(fig, n):
    fig.savefig(os.path.join(FIGD, f'fig{n}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRED, f'fig{n}.png'), bbox_inches='tight',
                pad_inches=0.03, dpi=220)
    plt.close(fig)


def arrow_axis(ax, x0, y0, x1, y1, lw=1.3):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=12))


def plain_axes(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def frame3(ax, x0, y0, x1, y1, lw=1.1):
    """三边框：左脊线、下脊线、右脊线（原书此批图形均无上边）"""
    ax.plot([x0, x0], [y0, y1], 'k-', lw=lw)
    ax.plot([x0, x1], [y0, y0], 'k-', lw=lw)
    ax.plot([x1, x1], [y0, y1], 'k-', lw=lw)


def qbez(p0, p1, p2, n=100):
    """二次贝塞尔曲线采样"""
    t = np.linspace(0.0, 1.0, n)
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    return x, y


def bez_pt(p0, p1, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1])


def pchip_xy(pts, n=240):
    pts = np.asarray(pts, float)
    f = PchipInterpolator(pts[:, 0], pts[:, 1])
    xx = np.linspace(pts[0, 0], pts[-1, 0], n)
    return xx, f(xx)


def pchip_yx(pts, n=240):
    """以 y 为自变量（x 可非单调）的曲线：pts 为 (x, y)，按 y 排序插值"""
    pts = np.asarray(sorted(pts, key=lambda p: p[1]), float)
    f = PchipInterpolator(pts[:, 1], pts[:, 0])
    yy = np.linspace(pts[0, 1], pts[-1, 1], n)
    return f(yy), yy


def pchip_loop(pts, n=500):
    """闭合/回头曲线：按点序参数化插值"""
    pts = np.asarray(pts, float)
    idx = np.arange(len(pts))
    fx = PchipInterpolator(idx, pts[:, 0])
    fy = PchipInterpolator(idx, pts[:, 1])
    u = np.linspace(0, len(pts) - 1, n)
    return fx(u), fy(u)


def box_fig(w, h):
    """开一个原书比例的空白画布（数据坐标 0..w, 0..h，约 2.2-3.0 英寸宽）"""
    fig, ax = plt.subplots(figsize=(w / 4.35, h / 4.35))
    plain_axes(ax)
    ax.set_xlim(-0.055 * w, 1.095 * w)
    ax.set_ylim(-0.10 * h, 1.10 * h)
    ax.set_aspect('equal')
    return fig, ax


def label_PT(ax, x, y):
    ax.text(x, y, r'$P$, $T$', fontsize=11, ha='center', va='center')


def label_T(ax, x, y):
    ax.text(x, y, r'$T$', fontsize=11, ha='center', va='center')


def label_x(ax, x, y):
    ax.text(x, y, r'$x$', fontsize=11, ha='center', va='center')


# ================================================================ 图20
def fig_20():
    """§97 临界点附近平衡曲线：半椭圆穹顶，内部水平阴影，K 为顶点"""
    fig, ax = box_fig(10.0, 10.0)
    frame3(ax, 0, 0, 10, 10)

    cx, yb, hw, hh = 5.19, 3.60, 2.86, 3.05       # 穹顶：中心、底、半宽、高
    th = np.linspace(0, np.pi, 200)
    ax.plot(cx + hw * np.cos(th), yb + hh * np.sin(th), 'k-', lw=1.5)
    # 底边封线（两端略出头的小钩）
    ax.plot([cx - hw - 0.10, cx + hw + 0.10], [yb, yb], 'k-', lw=1.4)
    ax.plot([cx - hw, cx - hw - 0.10], [yb, yb - 0.24], 'k-', lw=1.4)
    ax.plot([cx + hw, cx + hw + 0.10], [yb, yb - 0.24], 'k-', lw=1.4)
    for i in range(1, 6):                          # 内部水平阴影
        yy = yb + hh * i / 6.0
        xx = hw * np.sqrt(1 - ((yy - yb) / hh) ** 2)
        ax.plot([cx - xx, cx + xx], [yy, yy], 'k-', lw=0.9)
    ax.text(cx, yb + hh + 0.75, r'$K$', fontsize=12, ha='center', va='center')
    label_PT(ax, 1.40, 9.50)
    label_x(ax, 10.42, -0.60)
    save(fig, 20)


# ================================================================ 图21
def fig_21():
    """§97 等浓度点附近：两曲线在极大点 K 相切，之间区域为两相分离区"""
    fig, ax = box_fig(10.0, 10.0)
    frame3(ax, 0, 0, 10, 10)

    kx, ky = 4.86, 6.55
    ul, ur = 3.05, 1.69                            # 截止处外/内半宽
    ybot = 3.07
    a = (ky - ybot) / ul ** 2                      # 外(平)抛物线
    b = (ky - ybot) / ur ** 2                      # 内(陡)抛物线
    for sgn in (-1, 1):
        uo = sgn * np.linspace(0, ul, 120)
        ui = sgn * np.linspace(0, ur, 120)
        ax.plot(kx + uo, ky - a * uo ** 2, 'k-', lw=1.5)
        ax.plot(kx + ui, ky - b * ui ** 2, 'k-', lw=1.5)
    for yy in np.linspace(ky - 0.30, ybot, 10):    # 腿上水平梯级
        uo = np.sqrt((ky - yy) / a)
        ui = np.sqrt((ky - yy) / b)
        ax.plot([kx - uo, kx - ui], [yy, yy], 'k-', lw=0.9)
        ax.plot([kx + ui, kx + uo], [yy, yy], 'k-', lw=0.9)
    ax.text(kx, ky + 0.72, r'$K$', fontsize=12, ha='center', va='center')
    label_PT(ax, 1.05, 9.30)
    label_x(ax, 10.42, -0.60)
    save(fig, 21)


# ================================================================ 图22
def fig_22():
    """§97 低浓度极限：两条直线交于纵轴，之间楔形为两相分离区"""
    fig, ax = box_fig(9.6, 10.0)
    frame3(ax, 0, 0, 9.6, 10)

    vx, vy = 0.08, 6.70
    x1, x2, yb = 3.20, 1.36, 3.54                  # 上(缓)线与下(陡)线底端
    ax.plot([vx, x1], [vy, yb], 'k-', lw=1.4)
    ax.plot([vx, x2], [vy, yb], 'k-', lw=1.4)
    for yy in np.linspace(vy - 0.53, yb, 6):
        t = (vy - yy) / (vy - yb)
        ax.plot([vx + (x2 - vx) * t, vx + (x1 - vx) * t], [yy, yy], 'k-', lw=0.9)
    label_PT(ax, 1.10, 9.20)
    label_x(ax, 10.02, -0.62)
    save(fig, 22)


# ================================================================ 图23
def fig_23():
    """§97 三相点附近：平衡曲线 12/23/13，三相线 A-B-C，单相区 I II III"""
    fig, ax = box_fig(12.0, 11.6)
    frame3(ax, 0, 0, 12, 11.6)

    y3 = 5.94
    A, B, C = (2.51, y3), (5.24, y3), (8.32, y3)
    t12a, t12b = (1.37, 8.63), (4.15, 8.63)
    t23a, t23b = (6.42, 8.63), (9.97, 8.63)
    e13a, e13b = (1.37, 2.78), (9.36, 2.78)

    # 曲线（12/23 各两支 + 13 两支）
    ax.plot(*qbez(t12a, (1.42, 7.20), A), 'k-', lw=1.4)
    ax.plot(*qbez(t12b, (4.74, 7.25), B), 'k-', lw=1.4)
    ax.plot(*qbez(t23a, (5.72, 7.25), B), 'k-', lw=1.4)
    ax.plot(*qbez(t23b, (9.90, 7.25), C), 'k-', lw=1.4)
    ax.plot(*qbez(A, (1.15, 4.35), e13a), 'k-', lw=1.4)
    ax.plot(*qbez(C, (9.55, 4.35), e13b), 'k-', lw=1.4)
    # 顶端、底端封线与三相线
    ax.plot([t12a[0], t12b[0]], [8.63, 8.63], 'k-', lw=1.2)
    ax.plot([t23a[0], t23b[0]], [8.63, 8.63], 'k-', lw=1.2)
    ax.plot([e13a[0], e13b[0]], [2.78, 2.78], 'k-', lw=1.2)
    ax.plot([A[0], C[0]], [y3, y3], 'k-', lw=1.2)

    # 阴影：12 带、23 带（参数梯级），13 带（高度梯级）
    for tt in np.linspace(0.10, 0.92, 6):
        xa, ya = bez_pt(t12a, (1.42, 7.20), A, tt)
        xb, yb_ = bez_pt(t12b, (4.74, 7.25), B, tt)
        ax.plot([xa, xb], [ya, yb_], 'k-', lw=0.9)
        xa, ya = bez_pt(t23a, (5.72, 7.25), B, tt)
        xb, yb_ = bez_pt(t23b, (9.90, 7.25), C, tt)
        ax.plot([xa, xb], [ya, yb_], 'k-', lw=0.9)
    for yy in np.linspace(3.08, 5.62, 7):
        ta = (yy - A[1]) / (e13a[1] - A[1])
        tb = (yy - C[1]) / (e13b[1] - C[1])
        xa, _ = bez_pt(A, (1.15, 4.35), e13a, ta)
        xb, _ = bez_pt(C, (9.55, 4.35), e13b, tb)
        ax.plot([xa, xb], [yy, yy], 'k-', lw=0.9)

    # 标注
    for xx_, s_ in [(1.37, '12'), (4.15, '12'), (6.42, '23'), (9.97, '23')]:
        ax.text(xx_, 9.16, s_, fontsize=10, ha='center', va='center')
    ax.text(1.22, 2.20, '13', fontsize=10, ha='center', va='center')
    ax.text(9.50, 2.20, '13', fontsize=10, ha='center', va='center')
    ax.text(0.86, 6.94, 'I', fontsize=11, ha='center', va='center')
    ax.text(5.20, 7.78, 'II', fontsize=11, ha='center', va='center')
    ax.text(10.42, 7.03, 'III', fontsize=11, ha='center', va='center')
    ax.text(1.80, 5.62, r'$A$', fontsize=11, ha='center', va='center')
    ax.text(5.05, 5.37, r'$B$', fontsize=11, ha='center', va='center')
    ax.text(8.83, y3, r'$C$', fontsize=11, ha='center', va='center')
    label_PT(ax, 1.32, 11.03)
    label_x(ax, 12.40, -0.72)
    save(fig, 23)


# ---------------------------------------------------------- 图24-27 公用
def pt_axes(ax, w=8.6, h=7.8):
    arrow_axis(ax, 0, 0, 0, h)
    arrow_axis(ax, 0, 0, w, 0)
    ax.text(-0.62, h - 0.42, r'$T$', fontsize=11, ha='center', va='center')
    ax.text(w - 0.40, -0.70, r'$P$', fontsize=11, ha='center', va='center')


def pt_fig(h=7.8):
    fig, ax = plt.subplots(figsize=(2.35, 2.1 if h < 8 else 2.2))
    plain_axes(ax)
    ax.set_xlim(-1.35, 9.65)
    ax.set_ylim(-1.45, h + 0.95)
    ax.set_aspect('equal')
    pt_axes(ax, 8.6, h)
    return fig, ax


# ================================================================ 图24
def fig_24():
    """§97 临界曲线在 PT 面投影（点线）：上侧 ab（ merged 单相），下侧 a-b"""
    fig, ax = pt_fig()
    xx, yy = pchip_xy([(1.81, 3.67), (2.97, 4.58), (4.33, 5.09), (5.68, 5.46),
                       (6.34, 5.77)])
    ax.plot(xx, yy, 'k-', lw=1.6, dashes=(0.4, 1.9))
    ax.text(2.37, 5.67, r'$ab$', fontsize=11, ha='center', va='center')
    ax.text(4.02, 3.90, r'$a$-$b$', fontsize=11, ha='center', va='center')
    save(fig, 24)


# ================================================================ 图25
def fig_25():
    """§97 三相线在 PT 面投影（点划线）：上侧 a-c，下侧 a-b-c"""
    fig, ax = pt_fig()
    xx, yy = pchip_xy([(0.77, 1.30), (2.46, 2.60), (4.20, 3.53), (5.89, 4.16),
                       (6.76, 4.31)])
    ax.plot(xx, yy, 'k-', lw=1.25, dashes=(5.5, 1.8, 1.2, 1.8))
    ax.text(2.81, 3.95, r'$a$-$c$', fontsize=11, ha='center', va='center')
    ax.text(3.44, 1.35, r'$a$-$b$-$c$', fontsize=11, ha='center', va='center')
    save(fig, 25)


# ================================================================ 图26
def fig_26():
    """§97 等浓度点曲线在 PT 面投影（虚线）：上侧 ac，下侧 a-b-c"""
    fig, ax = pt_fig()
    xx, yy = pchip_xy([(1.57, 2.95), (3.15, 3.79), (4.93, 4.48), (6.30, 4.90),
                       (7.34, 5.11)])
    ax.plot(xx, yy, 'k-', lw=1.25, dashes=(4.8, 2.4))
    ax.text(2.88, 5.01, r'$ac$', fontsize=11, ha='center', va='center')
    ax.text(4.67, 3.53, r'$a$-$b$-$c$', fontsize=11, ha='center', va='center')
    save(fig, 26)


# ================================================================ 图27
def fig_27():
    """§97 纯物质相平衡曲线（实线，本在 PT 面上）：上侧 b，下侧 a-b"""
    fig, ax = pt_fig(h=8.4)
    xx, yy = pchip_xy([(1.51, 1.91), (2.68, 3.20), (3.97, 4.20), (4.90, 4.82),
                       (5.40, 5.08)])
    ax.plot(xx, yy, 'k-', lw=1.3)
    ax.text(2.42, 4.28, r'$b$', fontsize=11, ha='center', va='center')
    ax.text(3.37, 2.99, r'$a$-$b$', fontsize=11, ha='center', va='center')
    save(fig, 27)


# ================================================================ 图28
def fig_28():
    """§97 纯物质相（x=0）线与纵轴重合：轴与一条斜线间的楔形阴影"""
    fig, ax = box_fig(9.6, 9.7)
    frame3(ax, 0, 0, 9.6, 9.7)

    vx, vy = 0.08, 7.19
    x1, yb = 1.91, 3.17
    ax.plot([vx, x1 + 0.10], [vy, yb - 0.28], 'k-', lw=1.4)   # 斜线（下端出头）
    ax.plot([0, x1], [yb, yb], 'k-', lw=1.2)                  # 底部封线
    for yy in np.linspace(vy - 0.50, yb, 6):
        t = (vy - yy) / (vy - yb)
        ax.plot([0, vx + (x1 - vx) * t], [yy, yy], 'k-', lw=0.9)
    label_PT(ax, 1.00, 9.30)
    label_x(ax, 10.02, -0.60)
    save(fig, 28)


# ================================================================ 图29
def fig_29():
    """§97 化合物相（等浓度区域退化为竖线）：钟形曲线，中线两侧阴影"""
    fig, ax = box_fig(9.6, 9.7)
    frame3(ax, 0, 0, 9.6, 9.7)

    cx, yb, yt, hw = 4.72, 3.64, 6.55, 1.94
    s = np.linspace(0, 1, 160)
    w = hw * (1 - s ** 2.1) ** 0.50
    xx = np.concatenate([cx - w[::-1], cx + w])
    yy = np.concatenate([(yb + (yt - yb) * s[::-1]), (yb + (yt - yb) * s)])
    ax.plot(xx, yy, 'k-', lw=1.4)
    ax.plot([cx, cx], [yb - 0.42, yt], 'k-', lw=1.3)          # 化合物竖线
    for i in range(1, 8):                                      # 两侧梯级
        yy_ = yb + 0.12 + (yt - yb - 0.30) * (i - 1) / 6.0
        sidx = (yy_ - yb) / (yt - yb)
        ww = hw * (1 - sidx ** 2.1) ** 0.50
        ax.plot([cx - ww, cx], [yy_, yy_], 'k-', lw=0.9)
        ax.plot([cx, cx + ww], [yy_, yy_], 'k-', lw=0.9)
    ax.plot([cx - hw, cx + hw], [yb, yb], 'k-', lw=0.9)       # 底线梯级
    label_PT(ax, 1.00, 9.37)
    label_x(ax, 10.02, -0.60)
    save(fig, 29)


# ================================================================ 图30
def fig_30():
    """§97 三相点处化合物相（区域II退化为竖线）：沙漏形+中央竖线"""
    fig, ax = box_fig(9.6, 9.7)
    frame3(ax, 0, 0, 9.6, 9.7)

    cx, yw = 5.07, 5.63
    ytop, ybot = 8.37, 3.12
    g, wtop, wbot = 1.95, 3.74, 3.65               # 腰半隙、上/下端半宽
    ht, hb = ytop - yw, yw - ybot
    u = np.linspace(0, 1, 140)
    wl_u = g + (wtop - g) * u ** 0.75
    wl_l = g + (wbot - g) * u ** 0.75
    xL = np.concatenate([cx - wl_u[::-1], cx - wl_l])
    yy = np.concatenate([(yw + ht * u[::-1]), (yw - hb * u)])
    xR = 2 * cx - xL
    ax.plot(xL, yy, 'k-', lw=1.4)
    ax.plot(xR, yy, 'k-', lw=1.4)
    for xt, yt_, d in [(xL[0], ytop, -1), (xR[0], ytop, 1),
                       (xL[-1], ybot, -1), (xR[-1], ybot, 1)]:   # 端部小外钩
        ax.plot([xt, xt + d * 0.12], [yt_, yt_ - 0.12], 'k-', lw=1.2)
    ax.plot([xL[0], xR[0]], [ytop, ytop], 'k-', lw=1.2)       # 上封线
    ax.plot([xL[-1], xR[-1]], [ybot, ybot], 'k-', lw=1.2)     # 下封线
    ax.plot([cx, cx], [yw + 0.02, ytop], 'k-', lw=1.3)        # 化合物竖线
    for yy_ in np.linspace(ybot + 0.24, ytop - 0.24, 13):     # 满宽梯级
        if yy_ >= yw:
            wl = g + (wtop - g) * ((yy_ - yw) / ht) ** 0.75
        else:
            wl = g + (wbot - g) * ((yw - yy_) / hb) ** 0.75
        ax.plot([cx - wl, cx + wl], [yy_, yy_], 'k-', lw=0.9)
    label_PT(ax, 0.90, 9.32)
    label_x(ax, 10.02, -0.60)
    save(fig, 30)


# ================================================================ 图31
def fig_31():
    """§98 雪茄型相图：下沸点线/上凝聚线，竖虚线 AD，水平虚线 C-B 与 D-E"""
    fig, ax = box_fig(11.0, 10.2)
    frame3(ax, 0, 0, 11, 10.2)

    up_pts = [(0, 2.53), (1.50, 4.35), (3.00, 5.45), (4.50, 6.35), (6.00, 7.10),
              (7.11, 7.62), (8.80, 8.42), (9.90, 8.92), (11, 9.51)]
    lo_pts = [(0, 2.53), (1.65, 3.26), (3.30, 4.03), (4.95, 4.85), (7.11, 6.10),
              (8.80, 6.99), (9.86, 7.85), (10.45, 8.47), (11, 9.51)]
    xu, yu = pchip_xy(up_pts)
    xl, yl = pchip_xy(lo_pts)
    ax.plot(xu, yu, 'k-', lw=1.5)
    ax.plot(xl, yl, 'k-', lw=1.5)

    xA = 7.11
    yD = float(np.interp(xA, xu, yu))              # D：竖线交上曲线
    yB = float(np.interp(xA, xl, yl))              # B：竖线交下曲线
    xC = float(np.interp(yB, yu, xu))              # C：B 等温线交上曲线
    xE = float(np.interp(yD, yl, xl))              # E：D 等温线交下曲线
    yA = 2.62

    ax.plot([xA, xA], [yA, yD], 'k--', lw=0.95, dashes=(4.5, 2.4))
    ax.plot([xC, xA], [yB, yB], 'k--', lw=0.95, dashes=(4.5, 2.4))
    ax.plot([xA, xE], [yD, yD], 'k--', lw=0.95, dashes=(4.5, 2.4))

    for yy_ in np.linspace(2.95, 9.20, 12):        # 雪茄内部水平阴影
        a_ = float(np.interp(yy_, yl, xl))
        b_ = float(np.interp(yy_, yu, xu))
        if b_ - a_ > 0.18:
            ax.plot([a_, b_], [yy_, yy_], 'k-', lw=0.85)

    ax.text(-0.58, 2.25, r'$F$', fontsize=11, ha='center', va='center')
    ax.text(11.48, 9.45, r'$G$', fontsize=11, ha='center', va='center')
    ax.text(xA - 0.30, yA - 0.62, r'$A$', fontsize=11, ha='center', va='center')
    ax.text(xA + 0.48, yB - 0.60, r'$B$', fontsize=11, ha='center', va='center')
    ax.text(xA - 0.28, yD + 0.62, r'$D$', fontsize=11, ha='center', va='center')
    ax.text(xC - 0.72, yB + 0.60, r'$C$', fontsize=11, ha='center', va='center')
    ax.text(xE + 0.60, yD - 0.55, r'$E$', fontsize=11, ha='center', va='center')
    label_T(ax, -0.75, 9.75)
    label_x(ax, 11.40, -0.68)
    save(fig, 31)


# ================================================================ 图32
def fig_32():
    """§98 有等浓度点的相图：两曲线在极大点相切，之间阴影（无标注）"""
    fig, ax = box_fig(10.4, 10.0)
    frame3(ax, 0, 0, 10.4, 10)

    kx, ky = 5.36, 7.30
    dxl, dxr = 5.36, 5.04
    yl_, yr_ = 4.40, 5.30

    def W(x):
        if x <= kx:
            return ky - (ky - yl_) * ((kx - x) / dxl) ** 2
        return ky - (ky - yr_) * ((x - kx) / dxr) ** 2

    def N(x):
        if x <= kx:
            return ky - (ky - yl_) * ((kx - x) / dxl) ** 1.15
        return ky - (ky - yr_) * ((x - kx) / dxr) ** 1.15

    xs = np.linspace(0, 10.4, 320)
    ax.plot(xs, [W(x) for x in xs], 'k-', lw=1.5)
    ax.plot(xs, [N(x) for x in xs], 'k-', lw=1.5)
    for yy_ in np.linspace(4.62, 7.14, 10):
        for lo, hi in [(0.0, kx), (kx, 10.4)]:
            try:
                xn = brentq(lambda x: N(x) - yy_, lo, hi)
                xw = brentq(lambda x: W(x) - yy_, lo, hi)
            except ValueError:
                continue
            if abs(xw - xn) > 0.14:
                ax.plot([xn, xw], [yy_, yy_], 'k-', lw=0.9)
    label_T(ax, -0.85, 9.50)
    label_x(ax, 10.82, -0.62)
    save(fig, 32)


# ================================================================ 图33
def fig_33():
    """§98 液气两相具临界点 K：泪滴形环路，竖虚线 A-C-B（逆行凝聚）"""
    fig, ax = box_fig(10.4, 11.4)
    frame3(ax, 0, 0, 10.4, 11.4)

    pts = [(0, 5.10), (0.20, 5.80), (0.50, 6.50), (0.96, 7.15), (1.61, 7.90),
           (2.46, 8.65), (3.27, 9.25), (3.76, 9.50), (4.02, 9.66),
           (4.32, 8.80), (4.72, 8.00), (4.52, 7.30), (4.32, 7.06),
           (3.27, 6.75), (1.61, 5.90), (0.60, 5.50), (0, 5.10)]
    xx, yy = pchip_loop(pts)

    xA, yC, yB, yA = 4.32, 8.80, 7.06, 4.15
    ax.plot(xx, yy, 'k-', lw=1.4)
    ax.plot([xA, xA], [11.4, yA], 'k--', lw=0.95, dashes=(4.5, 2.4))
    for yy_ in np.linspace(5.35, 9.35, 11):        # 环内水平阴影
        cross = []
        for i in range(len(xx) - 1):
            if (yy[i] - yy_) * (yy[i + 1] - yy_) < 0:
                t = (yy_ - yy[i]) / (yy[i + 1] - yy[i])
                cross.append(xx[i] + t * (xx[i + 1] - xx[i]))
        if len(cross) >= 2:
            ax.plot([min(cross), max(cross)], [yy_, yy_], 'k-', lw=0.85)

    ax.text(3.37, 10.30, r'$K$', fontsize=12, ha='center', va='center')
    ax.text(xA + 0.55, yC + 0.45, r'$C$', fontsize=11, ha='center', va='center')
    ax.text(xA + 0.55, yB - 0.45, r'$B$', fontsize=11, ha='center', va='center')
    ax.text(xA - 0.12, yA - 0.42, r'$A$', fontsize=11, ha='center', va='center')
    label_T(ax, -0.80, 10.95)
    label_x(ax, 10.82, -0.72)
    save(fig, 33)


# ================================================================ 图34
def fig_34():
    """§98 两种液体有限互溶：底部钟形两相区，K 为上部临界点"""
    fig, ax = box_fig(10.4, 11.4)
    frame3(ax, 0, 0, 10.4, 11.4)

    cx, hw, hgt = 4.89, 2.70, 6.15
    s = np.linspace(0, 1, 160)
    w = hw * (1 - s ** 2.2) ** 0.52
    xx = np.concatenate([cx - w[::-1], cx + w])
    yy = np.concatenate([(hgt * s[::-1]), (hgt * s)])
    ax.plot(xx, yy, 'k-', lw=1.4)
    for i in range(11):                            # 满宽梯级
        yy_ = 0.38 + (hgt - 0.60) * i / 10.0
        sidx = min(yy_ / hgt, 1.0)
        ww = hw * (1 - sidx ** 2.2) ** 0.52
        ax.plot([cx - ww, cx + ww], [yy_, yy_], 'k-', lw=0.9)
    ax.text(cx - 0.10, hgt + 0.80, r'$K$', fontsize=12, ha='center', va='center')
    label_T(ax, -0.80, 10.95)
    label_x(ax, 10.82, -0.72)
    save(fig, 34)


# ================================================================ 图35
def fig_35():
    """§98 有限互溶（共晶）：液相线 A-B-C，固相线 A-D-F / C-E-G，三相线 D-B-E"""
    fig, ax = box_fig(11.0, 10.8)
    frame3(ax, 0, 0, 11, 10.8)

    y3 = 3.48
    A = (0.10, 5.76)
    D, E = (3.08, y3), (8.47, y3)

    lql = [(0.10, 5.76), (1.72, 4.88), (3.21, 4.22), (4.40, 3.82), (5.00, 3.62),
           (5.47, y3)]
    lqr = [(5.47, y3), (6.80, 4.05), (8.00, 4.70), (9.10, 5.40), (10.00, 6.10),
           (10.50, 6.90), (10.89, 7.99)]
    xlql, ylql = pchip_xy(lql)
    xlqr, ylqr = pchip_xy(lqr)
    ax.plot(xlql, ylql, 'k-', lw=1.4)
    ax.plot(xlqr, ylqr, 'k-', lw=1.4)
    sd1 = [(0.10, 5.76), (0.75, 5.15), (1.40, 4.60), (2.00, 4.18), (2.55, 3.80),
           (3.08, y3)]
    xs1, ys1 = pchip_xy(sd1)
    ax.plot(xs1, ys1, 'k-', lw=1.4)
    sd2 = [(3.08, y3), (2.82, 2.90), (2.60, 2.30), (2.40, 1.65), (2.22, 1.00),
           (2.05, 0.45), (1.95, 0.0)]
    xs2, ys2 = pchip_yx(sd2)
    ax.plot(xs2, ys2, 'k-', lw=1.4)
    se1 = [(10.89, 7.99), (10.62, 7.45), (10.30, 6.85), (9.90, 6.15), (9.50, 5.50),
           (9.10, 4.85), (8.75, 4.20), (8.47, y3)]
    xe1, ye1 = pchip_yx(se1)
    ax.plot(xe1, ye1, 'k-', lw=1.4)
    se2 = [(8.47, y3), (8.53, 2.92), (8.58, 2.27), (8.66, 1.62), (8.72, 0.97),
           (8.76, 0.45), (8.80, 0.0)]
    xe2, ye2 = pchip_xy(se2)
    ax.plot(xe2, ye2, 'k-', lw=1.4)
    ax.plot([D[0], E[0]], [y3, y3], 'k-', lw=1.2)  # 三相线 D-B-E

    def along(xs, ys, yy_):
        return float(np.interp(yy_, ys, xs))
    for yy_ in np.linspace(5.42, 3.62, 6):         # ADB 梯级（液+固1）
        ax.plot([along(xs1, ys1, yy_), along(xlql, ylql, yy_)], [yy_, yy_],
                'k-', lw=0.85)
    for yy_ in np.linspace(3.90, 7.55, 6):         # CBE 梯级（液+固2）
        ax.plot([along(xlqr, ylqr, yy_), along(xe1, ye1, yy_)], [yy_, yy_],
                'k-', lw=0.85)
    for yy_ in np.linspace(0.35, 3.20, 8):         # DEGF 梯级（固1+固2）
        ax.plot([along(xs2, ys2, yy_), along(xe2, ye2, yy_)], [yy_, yy_],
                'k-', lw=0.85)

    ax.text(-0.60, 5.70, r'$A$', fontsize=11, ha='center', va='center')
    ax.text(5.39, 4.86, r'$B$', fontsize=11, ha='center', va='center')
    ax.text(11.42, 8.28, r'$C$', fontsize=11, ha='center', va='center')
    ax.text(2.16, 3.42, r'$D$', fontsize=11, ha='center', va='center')
    ax.text(9.02, y3, r'$E$', fontsize=11, ha='center', va='center')
    ax.text(1.80, -0.85, r'$F$', fontsize=11, ha='center', va='center')
    ax.text(9.15, -0.85, r'$G$', fontsize=11, ha='center', va='center')
    label_T(ax, -0.95, 10.45)
    label_x(ax, 11.40, -0.85)
    save(fig, 35)


# ================================================================ 图36
def fig_36():
    """§98 有限互溶（转熔型）：液相线 A-D-C，固相线 A-B-F / C-E-G，三相线 D-B-E"""
    fig, ax = box_fig(11.0, 11.2)
    frame3(ax, 0, 0, 11, 11.2)

    y3 = 5.76
    A = (0.10, 2.97)
    D, B, E = (4.07, y3), (7.04, y3), (8.69, y3)
    C = (10.95, 9.28)

    xd1, yd1 = pchip_xy([(0.10, 2.97), (1.50, 3.72), (2.95, 4.51), (4.07, y3)])
    ax.plot(xd1, yd1, 'k-', lw=1.4)
    xd2, yd2 = pchip_xy([(4.07, y3), (5.50, 6.44), (7.15, 7.34), (8.80, 8.23),
                         (9.90, 8.74), (10.95, 9.28)])
    ax.plot(xd2, yd2, 'k-', lw=1.4)
    xab, yab = pchip_xy([(0.10, 2.97), (1.65, 3.58), (3.30, 4.20), (4.95, 4.82),
                         (6.05, 5.26), (7.04, y3)])
    ax.plot(xab, yab, 'k-', lw=1.4)
    xbf, ybf = pchip_yx([(7.04, y3), (6.90, 4.93), (6.65, 4.03), (6.35, 3.13),
                         (6.08, 2.24), (5.85, 1.35), (5.68, 0.56), (5.61, 0.10)])
    ax.plot(xbf, ybf, 'k-', lw=1.4)
    xce, yce = pchip_yx([(10.95, 9.28), (10.62, 8.62), (10.12, 7.84), (9.57, 6.94),
                         (9.13, 6.27), (8.80, 5.82), (8.69, y3)])
    ax.plot(xce, yce, 'k-', lw=1.4)
    xeg, yeg = pchip_xy([(8.69, y3), (8.80, 4.93), (8.97, 3.92), (9.19, 2.80),
                         (9.41, 1.79), (9.57, 0.90), (9.68, 0.10)])
    ax.plot(xeg, yeg, 'k-', lw=1.4)
    ax.plot([D[0], E[0]], [y3, y3], 'k-', lw=1.2)  # 三相线 D-B-E

    def along(xs, ys, yy_):
        return float(np.interp(yy_, ys, xs))
    for yy_ in np.linspace(3.35, 5.45, 6):         # ADB 梯级
        ax.plot([along(xab, yab, yy_), along(xd1, yd1, yy_)], [yy_, yy_],
                'k-', lw=0.85)
    for yy_ in np.linspace(6.20, 8.75, 8):         # CDE 梯级
        ax.plot([along(xd2, yd2, yy_), along(xce, yce, yy_)], [yy_, yy_],
                'k-', lw=0.85)
    blab = (5.50, 4.30)
    for yy_ in np.linspace(0.40, 5.35, 11):        # BEGF 梯级（绕开 B 标注）
        xa = along(xbf, ybf, yy_)
        xb = along(xeg, yeg, yy_)
        if abs(yy_ - blab[1]) < 0.62:
            segs = [(xa, blab[0] - 0.60), (blab[0] + 0.60, xb)]
        else:
            segs = [(xa, xb)]
        for s0, s1 in segs:
            if s1 - s0 > 0.12:
                ax.plot([s0, s1], [yy_, yy_], 'k-', lw=0.85)

    ax.text(-0.60, 2.97, r'$A$', fontsize=11, ha='center', va='center')
    ax.text(3.55, 6.15, r'$D$', fontsize=11, ha='center', va='center')
    ax.text(blab[0] - 0.05, blab[1], r'$B$', fontsize=11, ha='center', va='center')
    ax.text(11.42, 9.50, r'$C$', fontsize=11, ha='center', va='center')
    ax.text(9.22, 6.00, r'$E$', fontsize=11, ha='center', va='center')
    ax.text(5.50, -0.85, r'$F$', fontsize=11, ha='center', va='center')
    ax.text(9.90, -0.85, r'$G$', fontsize=11, ha='center', va='center')
    label_T(ax, -0.95, 10.75)
    label_x(ax, 11.40, -0.85)
    save(fig, 36)


# ================================================================ 图37
def fig_37():
    """§98 固态完全不互溶的共晶相图：液相线 D-B-E，共晶线 A-B-C，全域阴影"""
    fig, ax = box_fig(11.0, 11.6)
    frame3(ax, 0, 0, 11, 11.6)

    y3 = 2.41                                      # 共晶线 A-B-C 高度
    yv = 3.28                                      # 液相线 V 谷（略高于共晶线）
    B = (5.40, yv)

    xlb, ylb = pchip_xy([(0, 6.25), (1.50, 5.72), (2.87, 4.73), (4.28, 3.97),
                         (5.40, yv)])
    ax.plot(xlb, ylb, 'k-', lw=1.4)
    xrb, yrb = pchip_xy([(5.40, yv), (6.60, 3.72), (7.57, 4.71), (8.70, 5.75),
                         (9.45, 6.18), (10.20, 6.90), (11, 7.66)])
    ax.plot(xrb, yrb, 'k-', lw=1.4)
    ax.plot([0, 11], [y3, y3], 'k-', lw=1.2)       # 共晶线 A-B-C

    def along(xs, ys, yy_):
        return float(np.interp(yy_, ys, xs))
    blab = (5.20, 1.97)
    for yy_ in np.linspace(0.32, 6.00, 14):        # 液相线以下全域阴影
        if yy_ >= yv:
            segs = [(0.0, along(xlb, ylb, yy_)), (along(xrb, yrb, yy_), 11.0)]
        else:
            segs = [(0.0, 11.0)]
        for s0, s1 in segs:
            if abs(yy_ - blab[1]) < 0.50 and s0 < blab[0] < s1:
                segs2 = [(s0, blab[0] - 0.62), (blab[0] + 0.62, s1)]
            else:
                segs2 = [(s0, s1)]
            for u0, u1 in segs2:
                if u1 - u0 > 0.15:
                    ax.plot([u0, u1], [yy_, yy_], 'k-', lw=0.85)

    ax.text(-0.60, 6.25, r'$D$', fontsize=11, ha='center', va='center')
    ax.text(-0.60, y3, r'$A$', fontsize=11, ha='center', va='center')
    ax.text(blab[0] + 0.05, blab[1], r'$B$', fontsize=11, ha='center', va='center')
    ax.text(11.55, y3, r'$C$', fontsize=11, ha='center', va='center')
    ax.text(11.55, 7.66, r'$E$', fontsize=11, ha='center', va='center')
    label_T(ax, -0.95, 11.15)
    label_x(ax, 11.40, -0.80)
    save(fig, 37)


# ================================================================ 图35 补：本批至 35
# 注：图36、图37 属下一批（本批为图20-35），以上 fig_36/fig_37 仅供自检，
# __main__ 中不输出，避免越批覆盖。

if __name__ == '__main__':
    import sys
    ns = [int(a) for a in sys.argv[1:]] or list(range(20, 36))
    for i in ns:
        globals()[f'fig_{i}']()
        print(f'fig{i} done')
