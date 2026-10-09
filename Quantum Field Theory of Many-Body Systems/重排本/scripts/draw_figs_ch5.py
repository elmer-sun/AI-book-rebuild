# -*- coding: utf-8 -*-
# 批次 B4：文小刚《多体量子场论》第5章插图 5.1–5.21（黑白矢量重绘）
# 依据：原书转换/pages/p202–p260（书页 187–245，pNNN = 书页 + 15）
# 输出：figures/fig_{key}.pdf + figures/preview/fig_{key}.png
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = r"E:\AI整理书籍\文小刚\重排本"
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

GRAY = '0.82'      # 谱/密度阴影
FS = 10            # 默认字号
DASH = (0, (5, 3.2))     # 相互作用虚线
DASH_S = (0, (4, 2.6))   # 短虚线


def save(key):
    for ext, kw in (('pdf', {}), ('png', {'dpi': 160})):
        plt.savefig(os.path.join(FIGDIR if ext == 'pdf' else PREVDIR,
                                 f'fig_{key}.{ext}'),
                    bbox_inches='tight', pad_inches=0.03, **kw)
    plt.close()


def arr(ax, p, q, lw=1.1, ms=11, style='-|>', **kw):
    """自绘箭头（合同要求 annotate + arrowstyle '-|>'）。"""
    ax.annotate('', xy=q, xytext=p,
                arrowprops=dict(arrowstyle=style, lw=lw,
                                mutation_scale=ms, color='black',
                                shrinkA=0, shrinkB=0, **kw))


def head(ax, p, q, ms=11):
    """在已有线条上叠加箭头头部（lw≈0 只画面）。"""
    ax.annotate('', xy=q, xytext=p,
                arrowprops=dict(arrowstyle='-|>', lw=0.1, color='k',
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def fline(ax, p, q, arrows=(0.5,), lw=1.1, ms=11, ls='-'):
    """费米子线（直线 + 若干箭头，arrows 为 0-1 参数位置）。"""
    p = np.asarray(p, float); q = np.asarray(q, float)
    ax.plot([p[0], q[0]], [p[1], q[1]], color='k', lw=lw, ls=ls,
            solid_capstyle='butt')
    for t in np.atleast_1d(arrows):
        a = p + (q - p) * max(t - 0.06, 0)
        b = p + (q - p) * min(t + 0.06, 1)
        head(ax, a, b, ms)


def dline(ax, p, q, lw=1.0, dash=DASH):
    p = np.asarray(p, float); q = np.asarray(q, float)
    ax.plot([p[0], q[0]], [p[1], q[1]], color='k', lw=lw, ls=dash)


def wavy(ax, p, q, cycles=5.5, amp=0.045, lw=0.95, arrow=True):
    """光子波浪线（5.1 的 gamma），末端箭头。"""
    p = np.asarray(p, float); q = np.asarray(q, float)
    d = q - p
    L = np.hypot(*d)
    u = d / L
    n = np.array([-u[1], u[0]])
    t = np.linspace(0, 1, 220)
    pts = (p[None] + t[:, None] * d[None]
           + (amp * np.sin(2 * np.pi * cycles * t))[:, None] * n[None])
    if arrow:   # 末段不含波峰，直接连线到端点
        pts = pts[:-14]
        pts = np.vstack([pts, q])
    ax.plot(pts[:, 0], pts[:, 1], color='k', lw=lw)
    if arrow:
        a = p + d * 0.86
        head(ax, a, q, ms=9)


def on_circle(c, r, deg):
    a = np.deg2rad(deg)
    return np.array([c[0] + r * np.cos(a), c[1] + r * np.sin(a)])


def bubble(ax, c, r, lw=1.05, arrow='wen'):
    """费米泡泡圆圈；arrow: 'wen'=10点半径向三角(原书样式),
    'topcw'=顶部顺时针切向箭头(5.14/5.16), 'none'。"""
    ax.add_patch(plt.Circle(c, r, facecolor='none', edgecolor='k',
                            lw=lw, zorder=3))
    if arrow == 'wen':
        p1 = on_circle(c, r, 99); p2 = on_circle(c, r, 127)
        apex = on_circle(c, r * 1.30, 113)
        ax.add_patch(plt.Polygon([p1, p2, apex], closed=True,
                                 facecolor='k', edgecolor='k', zorder=4))
    elif arrow == 'topcw':
        a = on_circle(c, r, 99); b = on_circle(c, r, 68)
        head(ax, a, b, ms=11)


def varrow(ax, p, h, lw=0.9, ms=8, up=True):
    q = (p[0], p[1] + h if up else p[1] - h)
    arr(ax, p, q, lw=lw, ms=ms)


def axes_ar(ax, o=(0, 0), xl=1.4, yl=1.1, klabel='$k$', ylabel='$\\omega$',
            ms=9, fs=FS):
    """L 形坐标轴（竖直向上、水平向右带箭头）。"""
    ox, oy = o
    ax.plot([ox, ox], [oy, oy + yl], color='k', lw=0.9)
    ax.plot([ox, ox + xl], [oy, oy], color='k', lw=0.9)
    arr(ax, (ox, oy + yl * 0.82), (ox, oy + yl), lw=0.9, ms=ms)
    arr(ax, (ox + xl * 0.85, oy), (ox + xl, oy), lw=0.9, ms=ms)
    ax.text(ox - 0.055 * xl, oy + yl, ylabel, fontsize=fs,
            ha='right', va='center')
    ax.text(ox + xl, oy - 0.07 * yl, klabel, fontsize=fs, ha='center',
            va='top')


# ---------------------------------------------------------------- 5.1
def fig_5_1():
    fig = plt.figure(figsize=(5.7, 2.5))
    axa = fig.add_axes([0.005, 0.0, 0.315, 1.0])
    panels = [(0.345, 0.535), (0.345, 0.0), (0.675, 0.535), (0.675, 0.0)]

    # ---- (a) 物理模型
    a = axa
    a.set_xlim(-1.65, 3.55)
    a.set_ylim(-0.75, 3.35)
    a.set_aspect('equal')
    a.axis('off')
    # 抛物线导带
    xs = np.linspace(-1.12, 1.92, 300)
    a.plot(xs, 1.0 + 1.5 * (xs - 0.4) ** 2, color='k', lw=1.1)
    # mu 虚线
    a.plot([-1.05, 2.25], [2.2, 2.2], color='k', lw=0.8, ls=(0, (5, 3)))
    a.text(-1.13, 2.2, '$\\mu$', fontsize=FS, ha='right', va='center')
    # 芯能级
    a.plot([-1.05, 3.3], [0, 0], color='k', lw=1.0)
    # 吸收：芯电子(实心点) -> 导带
    a.add_patch(plt.Circle((-0.72, 0), 0.055, color='k', zorder=5))
    fline(a, (-0.72, 0.05), (-0.72, 2.86), arrows=(0.94,), lw=1.1)
    # E_C 双箭头
    a.annotate('', xy=(0.55, 0.03), xytext=(0.55, 2.17),
               arrowprops=dict(arrowstyle='<|-|>', lw=1.0, color='k',
                               mutation_scale=10, shrinkA=0, shrinkB=0))
    a.text(0.33, 1.22, '$E_C$', fontsize=FS, ha='right', va='center')
    # 发射：导带电子 -> 芯空穴(空心圈)
    a.add_patch(plt.Circle((1.15, 0), 0.055, facecolor='white',
                           edgecolor='k', lw=1.0, zorder=5))
    fline(a, (1.15, 1.83), (1.15, 0.07), arrows=(0.90,), lw=1.1)
    # 光子 gamma（两条入射波浪线）
    wavy(a, (-1.5, 1.15), (-0.80, 0.10), amp=0.05)
    a.text(-1.52, 1.32, '$\\gamma$', fontsize=FS)
    wavy(a, (0.62, 1.02), (1.08, 0.12), amp=0.045)
    a.text(0.56, 1.12, '$\\gamma$', fontsize=FS)
    # 出射电子（斜箭头到实心点）+ gamma'
    a.add_patch(plt.Circle((2.42, 1.18), 0.055, color='k', zorder=5))
    fline(a, (1.28, 0.15), (2.33, 1.12), arrows=(0.88,), lw=1.0)
    wavy(a, (1.52, 0.85), (1.95, 1.38), amp=0.04)
    a.text(2.0, 1.42, "$\\gamma'$", fontsize=FS)
    a.text(2.0, 2.45, 'Emission', fontsize=FS, ha='left')
    a.text(-0.72, -0.30, 'Absorption', fontsize=FS, ha='center', va='top')
    a.text(-1.6, 3.15, '(a)', fontsize=FS)

    # ---- (b)(c) 四个谱面板
    def spec(ax, kind, inter, title, show_ec):
        ax.set_xlim(0, 1.06)
        ax.set_ylim(-0.16, 1.06)
        ax.axis('off')
        ax.set_aspect('auto')
        # 轴
        ax.plot([0.06, 0.06], [0.02, 0.92], color='k', lw=0.9)
        ax.plot([0.06, 1.0], [0.02, 0.02], color='k', lw=0.9)
        arr(ax, (0.06, 0.80), (0.06, 0.92), lw=0.9, ms=8)
        arr(ax, (0.90, 0.02), (1.0, 0.02), lw=0.9, ms=8)
        ax.text(0.10, 0.93, title, fontsize=FS, ha='left', va='bottom')
        ax.text(1.0, -0.03, '$\\omega$', fontsize=FS, ha='center',
                va='top')
        ec = 0.60
        if kind == 'abs':
            xs = np.linspace(0.20, 1.0, 300)
            ys = np.where(xs < 0.36,
                          0.40 * np.sqrt(np.clip((xs - 0.20) / 0.16, 0, 1)),
                          0.40 + 0.86 * (xs - 0.36))
            ys = np.clip(ys, 0, 0.96)
            ax.plot(xs, ys, color='k', lw=1.1, zorder=3)
            if not inter:
                m = xs >= ec
                ax.fill_between(xs[m], 0.02, ys[m], color=GRAY, lw=0,
                                zorder=2)
            else:
                yend = np.interp(0.97, xs, ys)
                xs2 = np.linspace(ec, 0.97, 200)
                ys2 = 0.02 + (yend - 0.02) * ((xs2 - ec) / 0.37) ** 0.42
                ax.fill_between(xs2, ys2, np.interp(xs2, xs, ys),
                                color=GRAY, lw=0, zorder=2)
                ax.plot(xs2, ys2, color='k', lw=1.1, zorder=3)
            ax.plot([ec, ec], [0.02, np.interp(ec, xs, ys)],
                    color='k', lw=0.9, zorder=3)
        else:  # emission
            xs = np.linspace(0.20, 1.0, 300)
            ys = np.where(xs < 0.36,
                          0.45 * np.sqrt(np.clip((xs - 0.20) / 0.16, 0, 1)),
                          0.45 + 0.60 * (xs - 0.36))
            ax.plot(xs, ys, color='k', lw=1.0, zorder=3)
            if not inter:
                m = xs <= ec
                ax.fill_between(xs[m], 0.02, ys[m], color=GRAY, lw=0,
                                zorder=2)
            else:
                y36 = np.interp(0.36, xs, ys)
                ts = np.linspace(0, 1, 100)
                bx = ((1 - ts) ** 2 * 0.36 + 2 * (1 - ts) * ts * 0.44
                      + ts ** 2 * ec)
                by = ((1 - ts) ** 2 * y36 + 2 * (1 - ts) * ts * 0.74
                      + ts ** 2 * 0.02)
                px = np.concatenate([xs[xs <= 0.36], bx])
                py = np.concatenate([ys[xs <= 0.36], by])
                ax.fill_between(px, 0.02, py, color=GRAY, lw=0, zorder=2)
                ax.plot(bx, by, color='k', lw=1.1, zorder=3)
            ax.plot([ec, ec], [0.02, np.interp(ec, xs, ys)],
                    color='k', lw=0.9, zorder=3)
        if show_ec:
            ax.text(ec, -0.03, '$E_C$', fontsize=FS, ha='center', va='top')

    titles = ['Absorption', 'Emission', 'Absorption', 'Emission']
    for (x0, y0), t, inter, ec in zip(
            panels, titles, [False, False, True, True],
            [False, True, False, True]):
        ax = fig.add_axes([x0, y0, 0.30, 0.44])
        spec(ax, 'abs' if 'Abs' in t else 'emi', inter, t, ec)
        tag = '(b)' if x0 < 0.6 else '(c)'
        if y0 > 0.5:
            ax.text(0.0, 1.02, tag, fontsize=FS, transform=ax.transAxes)
    save('5.1')


# ---------------------------------------------------------------- 5.2
def fig_5_2():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0, 1.55))
    for a, deformed in ((a1, False), (a2, True)):
        a.set_xlim(-0.45, 1.55)
        a.set_ylim(-0.62, 0.80)
        a.set_aspect('equal')
        a.axis('off')
        # 基线
        a.plot([-0.42, 1.45], [0, 0], color='k', lw=0.8)
        # 导带电子密度方块
        if not deformed:
            a.add_patch(plt.Rectangle((0, 0), 1.0, 0.62, facecolor=GRAY,
                                      edgecolor='k', lw=1.0))
        else:
            xs = np.linspace(0, 1.0, 300)
            top = 0.62 - 0.20 * np.exp(-((xs - 0.5) / 0.14) ** 2)
            poly = np.concatenate([[[-0.0, 0.0]], np.column_stack([xs, top]),
                                   [[1.0, 0.0]]])
            a.add_patch(plt.Polygon(poly, facecolor=GRAY, edgecolor='k',
                                    lw=1.0))
        # 方块内部横线
        a.plot([0, 1.0], [0.13, 0.13], color='k', lw=0.9)
        # 下方芯能级短线
        a.plot([0.42, 0.58], [-0.30, -0.30], color='k', lw=0.9)
        if deformed:
            a.add_patch(plt.Circle((0.5, -0.30), 0.038, color='k',
                                   zorder=5))
            fline(a, (0.35, 0.10), (0.478, -0.26), arrows=(0.88,), lw=0.9)
    save('5.2')


# ---------------------------------------------------------------- 5.3
def fig_5_3():
    fig, ax = plt.subplots(figsize=(3.5, 2.55))
    ax.set_xlim(-0.18, 1.62)
    ax.set_ylim(-0.22, 2.30)
    ax.axis('off')
    # 轴
    ax.plot([0, 0], [0, 2.12], color='k', lw=1.0)
    ax.plot([0, 1.5], [0, 0], color='k', lw=1.0)
    arr(ax, (0, 1.95), (0, 2.12), lw=1.0, ms=9)
    arr(ax, (1.38, 0), (1.5, 0), lw=1.0, ms=9)
    ax.text(-0.05, 2.14, '$\\omega$', fontsize=FS + 1, ha='right',
            va='center')
    ax.text(1.48, -0.05, '$k$', fontsize=FS + 1, ha='center', va='top')
    # 粒子-空穴连续谱阴影
    k1 = 1.03          # 上界曲线拐点
    ktop = 1.52        # 顶边右端
    ke = 1.0           # 2 k_F
    H = 1.78
    xs_u = np.linspace(0, k1, 120)
    ys_u = H * (xs_u / k1) ** 0.60
    xs_r = np.linspace(ke, ktop, 120)
    ys_r = H * ((xs_r - ke) / (ktop - ke)) ** 0.65
    px = np.concatenate([xs_u, [ktop], xs_r[::-1], [0]])
    py = np.concatenate([ys_u, [H], ys_r[::-1], [0]])
    ax.fill(px, py, color=GRAY, lw=0)
    ax.plot(xs_u, ys_u, color='k', lw=1.0)
    ax.plot([k1, ktop], [H, H], color='k', lw=1.0)
    ax.plot(xs_r, ys_r, color='k', lw=1.0)
    # 线性模式（粗线）
    ax.plot([0, 0.62], [0, 0.35], color='k', lw=1.7,
            solid_capstyle='butt')
    ax.text(ke, -0.06, '$2k_F$', fontsize=FS + 1, ha='center', va='top')
    save('5.3')


# ---------------------------------------------------------------- 5.4
def fig_5_4():
    fig = plt.figure(figsize=(5.7, 2.05))
    axs = [fig.add_axes([0.005, 0.0, 0.36, 1.0]),
           fig.add_axes([0.365, 0.0, 0.31, 1.0]),
           fig.add_axes([0.685, 0.0, 0.31, 1.0])]
    th = np.linspace(0, 2 * np.pi, 400)

    # (a) 起伏的费米面
    a = axs[0]
    a.set_xlim(-1.75, 2.1)
    a.set_ylim(-1.6, 1.75)
    a.set_aspect('equal')
    a.axis('off')
    r = 1 + 0.13 * np.sin(5 * th + 0.65)
    a.fill(r * np.cos(th), r * np.sin(th), facecolor='0.90', lw=0)
    a.add_patch(plt.Circle((0, 0), 1, facecolor='none', edgecolor='k',
                           lw=0.7))
    a.plot(r * np.cos(th), r * np.sin(th), color='k', lw=1.35)
    a.add_patch(plt.Circle((0, 0), 0.028, color='k'))
    a.plot([0, 1.62], [0, 0], color='k', lw=0.7)               # theta=0 基线
    kk = np.deg2rad(52)
    a.plot([0, 1.5 * np.cos(kk)], [0, 1.5 * np.sin(kk)], color='k', lw=0.7)
    fline(a, (0.42 * np.cos(kk), 0.42 * np.sin(kk)),
          (1.02 * np.cos(kk), 1.02 * np.sin(kk)), arrows=(0.9,), lw=0.9)
    a.text(0.74 * np.cos(kk) - 0.17, 0.74 * np.sin(kk) + 0.10,
           r'$\hat{\boldsymbol{k}}$', fontsize=FS, ha='right')
    ts = np.linspace(0.06, np.deg2rad(52) - 0.03, 40)
    a.plot(0.42 * np.cos(ts), 0.42 * np.sin(ts), color='k', lw=0.7)
    a.text(0.62 * np.cos(np.deg2rad(27)), 0.62 * np.sin(np.deg2rad(27)),
           '$\\theta$', fontsize=FS, ha='center')
    hh = np.deg2rad(-33)
    fline(a, (0.55 * np.cos(hh), 0.55 * np.sin(hh)),
          (1.07 * np.cos(hh), 1.07 * np.sin(hh)), arrows=(0.92,), lw=0.9)
    a.text(1.24 * np.cos(hh) + 0.05, 1.24 * np.sin(hh), '$h$',
           fontsize=FS)
    a.text(-1.7, 1.45, '(a)', fontsize=FS)

    # (b) l=1 偶极涨落
    a = axs[1]
    a.set_xlim(-1.45, 1.45)
    a.set_ylim(-1.5, 1.55)
    a.set_aspect('equal')
    a.axis('off')
    a.add_patch(plt.Circle((0, 0), 1.0, facecolor='none', edgecolor='k',
                           lw=0.7))
    a.add_patch(plt.Circle((-0.17, -0.12), 1.0, facecolor='0.90',
                           edgecolor='k', lw=1.35))
    a.text(-1.4, 1.25, '(b)', fontsize=FS)

    # (c) l=2 四极涨落
    a = axs[2]
    a.set_xlim(-1.5, 1.5)
    a.set_ylim(-1.5, 1.55)
    a.set_aspect('equal')
    a.axis('off')
    a.add_patch(plt.Circle((0, 0), 1.0, facecolor='none', edgecolor='k',
                           lw=0.7))
    a.add_patch(Ellipse((0, 0), 2.44, 1.72, facecolor='0.90',
                            edgecolor='k', lw=1.35))
    a.text(-1.45, 1.25, '(c)', fontsize=FS)
    save('5.4')


# ---------------------------------------------------------------- 5.5
def fig_5_5():
    fig, ax = plt.subplots(figsize=(3.05, 2.85))
    ax.set_xlim(-1.35, 1.95)
    ax.set_ylim(-1.28, 1.45)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.add_patch(plt.Circle((0, 0), 1.0, facecolor='0.90', edgecolor='k',
                            lw=1.15))
    ax.plot([0, 1.82], [0, 0], color='k', lw=0.7)
    # k 方向（117 度）与空穴
    ak = np.deg2rad(117)
    ax.plot([0, 1.32 * np.cos(ak)], [0, 1.32 * np.sin(ak)], color='k',
            lw=0.8)
    fline(ax, (0.40 * np.cos(ak), 0.40 * np.sin(ak)),
          (0.78 * np.cos(ak), 0.78 * np.sin(ak)), arrows=(0.9,), lw=0.9)
    ax.text(0.82 * np.cos(ak) - 0.12, 0.82 * np.sin(ak) - 0.06,
            r'$\hat{\boldsymbol{k}}$', fontsize=FS, ha='right')
    hole = (np.cos(ak), np.sin(ak))
    ax.add_patch(plt.Circle(hole, 0.05, facecolor='white', edgecolor='k',
                            lw=1.0, zorder=5))
    # 粒子（实心点）与 q 箭头
    part = (hole[0] + 0.20, hole[1] + 0.13)
    ax.add_patch(plt.Circle(part, 0.052, color='k', zorder=5))
    fline(ax, (hole[0] + 0.055, hole[1] + 0.03), part, arrows=(0.62,),
          lw=0.9)
    ax.text(hole[0] + 0.03, hole[1] + 0.20, r'$\boldsymbol{q}$',
            fontsize=FS)
    # q 方向（47 度）
    aq = np.deg2rad(47)
    ax.plot([0, 1.58 * np.cos(aq)], [0, 1.58 * np.sin(aq)], color='k',
            lw=0.8)
    fline(ax, (0.42 * np.cos(aq), 0.42 * np.sin(aq)),
          (0.80 * np.cos(aq), 0.80 * np.sin(aq)), arrows=(0.9,), lw=0.9)
    ax.text(0.92 * np.cos(aq), 0.92 * np.sin(aq) + 0.09,
            r'$\hat{\boldsymbol{q}}$', fontsize=FS)
    # 角度弧
    ts = np.linspace(0, aq, 40)
    ax.plot(0.30 * np.cos(ts), 0.30 * np.sin(ts), color='k', lw=0.7)
    ts = np.linspace(0, ak, 60)
    ax.plot(0.42 * np.cos(ts), 0.42 * np.sin(ts), color='k', lw=0.7)
    ax.text(0.52 * np.cos(np.deg2rad(21)), 0.52 * np.sin(np.deg2rad(21)),
            r'$\theta_{\boldsymbol{q}}$', fontsize=FS)
    ax.text(0.62 * np.cos(np.deg2rad(62)), 0.62 * np.sin(np.deg2rad(62)),
            '$\\theta$', fontsize=FS)
    save('5.5')


# ---------------------------------------------------------------- 5.6
def fig_5_6():
    fig = plt.figure(figsize=(5.7, 2.1))

    # (a) f_l = 0 的连续谱（密排横线）
    a = fig.add_axes([0.01, 0.0, 0.17, 1.0])
    a.set_xlim(-0.32, 1.32)
    a.set_ylim(-0.72, 0.72)
    a.set_aspect('equal')
    a.axis('off')
    ys = np.linspace(-0.45, 0.45, 11)
    for y in ys:
        a.plot([0, 1.0], [y, y], color='k', lw=1.3)
    a.fill_between([0, 1.0], -0.45, 0.45, color=GRAY, lw=0, zorder=0)
    for y in ys:
        a.plot([0, 1.0], [y, y], color='k', lw=1.2, zorder=2)
    a.plot([-0.15, 1.15], [-0.27, -0.27], color='k', lw=0.7, zorder=3)
    a.text(-0.28, 0.62, '(a)', fontsize=FS)

    # (b) 相应的粒子-空穴谱
    a = fig.add_axes([0.205, 0.0, 0.26, 1.0])
    a.set_xlim(-0.30, 1.38)
    a.set_ylim(-0.18, 1.25)
    a.axis('off')
    a.plot([0, 0], [0, 1.08], color='k', lw=0.9)
    a.plot([0, 1.30], [0, 0], color='k', lw=0.9)
    arr(a, (0, 0.97), (0, 1.08), lw=0.9, ms=8)
    arr(a, (1.20, 0), (1.30, 0), lw=0.9, ms=8)
    a.text(-0.05, 1.10, '$\\omega$', fontsize=FS + 1, ha='right')
    a.text(1.28, -0.03, '$q$', fontsize=FS + 1, ha='center', va='top')
    poly = [(0, 0), (0.56, 1.0), (1.12, 1.0), (0.94, 0)]
    a.add_patch(plt.Polygon(poly, facecolor=GRAY, edgecolor='k', lw=1.0))
    a.plot([0.30, 0.30], [-0.07, 1.07], color='k', lw=0.9, ls=DASH_S)
    a.text(-0.28, 1.22, '(b)', fontsize=FS)

    # (c) f_l > 0：连续谱 + 孤立能级
    a = fig.add_axes([0.50, 0.0, 0.17, 1.0])
    a.set_xlim(-0.32, 1.32)
    a.set_ylim(-0.72, 0.72)
    a.set_aspect('equal')
    a.axis('off')
    a.fill_between([0, 1.0], -0.45, 0.36, color=GRAY, lw=0, zorder=0)
    for y in np.linspace(-0.45, 0.36, 10):
        a.plot([0, 1.0], [y, y], color='k', lw=1.2, zorder=2)
    a.plot([0, 1.0], [0.60, 0.60], color='k', lw=1.2, zorder=2)
    a.plot([-0.15, 1.15], [-0.18, -0.18], color='k', lw=0.7, zorder=3)
    a.text(-0.28, 0.62, '(c)', fontsize=FS)

    # (d) 相应谱：集体模 + 连续谱
    a = fig.add_axes([0.695, 0.0, 0.295, 1.0])
    a.set_xlim(-0.30, 1.38)
    a.set_ylim(-0.18, 1.25)
    a.axis('off')
    a.plot([0, 0], [0, 1.08], color='k', lw=0.9)
    a.plot([0, 1.30], [0, 0], color='k', lw=0.9)
    arr(a, (0, 0.97), (0, 1.08), lw=0.9, ms=8)
    arr(a, (1.20, 0), (1.30, 0), lw=0.9, ms=8)
    a.text(-0.05, 1.10, '$\\omega$', fontsize=FS + 1, ha='right')
    a.text(1.28, -0.03, '$q$', fontsize=FS + 1, ha='center', va='top')
    poly = [(0, 0), (0.74, 0.44), (0.95, 0.44), (0.81, 0)]
    a.add_patch(plt.Polygon(poly, facecolor=GRAY, edgecolor='k', lw=1.0))
    fline(a, (0, 0), (0.37, 1.14), arrows=(), lw=1.0)
    a.plot([0.24, 0.24], [-0.07, 1.08], color='k', lw=0.9, ls=DASH_S)
    a.text(-0.28, 1.22, '(d)', fontsize=FS)
    save('5.6')


# ---------------------------------------------------------------- 5.7
def fig_5_7():
    fig = plt.figure(figsize=(5.6, 1.8))
    # (a) 两个断开的泡泡图
    a = fig.add_axes([0.0, 0.0, 0.52, 1.0])
    a.set_xlim(0, 4.1)
    a.set_ylim(0, 2.1)
    a.set_aspect('equal')
    a.axis('off')
    for cx in (0.95, 3.05):
        bubble(a, (cx, 1.12), 0.60)
        a.text(cx, 1.12, '$(-1)$', fontsize=FS, ha='center', va='center')
        a.text(cx, 0.30, r'$\mathrm{i}G_0(0)$', fontsize=FS, ha='center',
               va='top')
    dline(a, (1.56, 1.12), (2.44, 1.12))
    a.text(1.62, 1.20, '$x$', fontsize=FS, ha='left', va='bottom')
    a.text(2.38, 1.20, "$x'$", fontsize=FS, ha='right', va='bottom')
    a.text(2.0, 0.86, r"$-\mathrm{i}V(x,x')$", fontsize=FS, ha='center',
           va='top')
    a.text(0.12, 1.85, '(a)', fontsize=FS)

    # (b) 单个泡泡（大圆 + 弦）
    a = fig.add_axes([0.50, 0.0, 0.50, 1.0])
    a.set_xlim(0, 4.1)
    a.set_ylim(0, 2.1)
    a.set_aspect('equal')
    a.axis('off')
    c, r = (2.85, 1.05), 0.86
    a.add_patch(plt.Circle(c, r, facecolor='none', edgecolor='k', lw=1.05))
    # 弦（虚线）
    dline(a, (c[0] - r, c[1]), (c[0] + r, c[1]))
    # 上弧箭头（顺时针，1 点钟方向）与下弧箭头（5 点钟方向）
    head(a, on_circle(c, r, 78), on_circle(c, r, 60), ms=12)
    head(a, on_circle(c, r, -60), on_circle(c, r, -78), ms=12)
    a.text(c[0] - 0.06, c[1] + 0.62, '$(-1)$', fontsize=FS, ha='center')
    a.text(c[0] - r + 0.13, c[1] + 0.09, '$x$', fontsize=FS, ha='left')
    a.text(c[0] + r - 0.13, c[1] + 0.09, "$x'$", fontsize=FS, ha='right')
    a.text(c[0], c[1] - 0.24, r"$-\mathrm{i}V(x,x')$", fontsize=FS,
           ha='center', va='top')
    a.text(c[0] - r - 0.12, c[1] + 0.52, r"$\mathrm{i}G_0(x',x)$",
           fontsize=FS, ha='right')
    a.text(c[0] - r - 0.12, c[1] - 0.52, r"$\mathrm{i}G_0(x,x')$",
           fontsize=FS, ha='right', va='top')
    a.text(0.25, 1.85, '(b)', fontsize=FS)
    save('5.7')


# ---------------------------------------------------------------- 5.8
def fig_5_8():
    fig = plt.figure(figsize=(5.6, 1.62))
    y0 = 0.42

    # (a) Hartree（泡泡 + 竖直虚线）
    a = fig.add_axes([0.0, 0.0, 0.50, 1.0])
    a.set_xlim(0, 4.1)
    a.set_ylim(0, 1.75)
    a.set_aspect('equal')
    a.axis('off')
    fline(a, (0.42, y0), (3.55, y0), arrows=(0.17, 0.80), lw=1.1)
    dline(a, (2.0, y0), (2.0, 1.12))
    a.text(2.12, y0 - 0.06, r'$-\mathrm{i}V_0$', fontsize=FS, ha='left',
           va='top')
    bubble(a, (2.0, 1.52), 0.42)
    a.text(2.0, 1.52, '$(-1)$', fontsize=FS - 1.5, ha='center',
           va='center')
    a.text(2.55, 1.68, r"$\mathrm{i}G_{0,\boldsymbol{k}'\nu}$",
           fontsize=FS, ha='left')
    varrow(a, (1.52, 1.55), 0.30, up=True)
    varrow(a, (1.63, 1.55), 0.30, up=False)
    varrow(a, (0.42, y0 + 0.03), 0.26)
    varrow(a, (3.55, y0 + 0.03), 0.26)
    a.text(0.15, 1.6, '(a)', fontsize=FS)

    # (b) Fock（虚线大弧）
    a = fig.add_axes([0.48, 0.0, 0.52, 1.0])
    a.set_xlim(0, 4.3)
    a.set_ylim(0, 1.75)
    a.set_aspect('equal')
    a.axis('off')
    fline(a, (0.42, y0), (4.05, y0), arrows=(0.13, 0.47, 0.85), lw=1.1)
    ts = np.linspace(0, 1, 100)
    ax_ = 1.35 + 2.25 * ts
    ay = y0 + 1.12 * np.sin(np.pi * ts)
    a.plot(ax_, ay, color='k', lw=1.0, ls=DASH)
    a.text(2.48, 1.62, r'$-\mathrm{i}V_{\boldsymbol{q}}$', fontsize=FS,
           ha='center', va='bottom')
    a.text(0.85, 0.14, r'$\mathrm{i}G_{0,\boldsymbol{k}\omega}$',
           fontsize=FS, ha='center')
    a.text(2.48, 0.14,
           r'$\mathrm{i}G_{0,\boldsymbol{k}-\boldsymbol{q},\omega-\nu}$',
           fontsize=FS, ha='center')
    a.text(3.85, 0.14, r'$\mathrm{i}G_{0,\boldsymbol{k}\omega}$',
           fontsize=FS, ha='center')
    varrow(a, (2.48, y0 + 0.06), 0.30)
    varrow(a, (0.42, y0 + 0.03), 0.26)
    varrow(a, (4.05, y0 + 0.03), 0.26)
    a.text(0.15, 1.6, '(b)', fontsize=FS)
    save('5.8')


# ---------------------------------------------------------------- 5.9
def fig_5_9():
    fig = plt.figure(figsize=(4.7, 1.95))
    y0 = 0.42

    # (a)
    a = fig.add_axes([0.0, 0.0, 0.50, 1.0])
    a.set_xlim(0, 4.1)
    a.set_ylim(0, 1.85)
    a.set_aspect('equal')
    a.axis('off')
    fline(a, (0.72, y0), (2.05, y0), arrows=(0.72,), lw=1.1)
    a.text(0.62, y0 - 0.10, r'$\boldsymbol{k},\omega$', fontsize=FS,
           ha='right', va='top')
    dline(a, (2.05, 1.38 - 0.47), (2.05, -0.06))
    a.plot([1.94, 2.16], [-0.06, -0.06], color='k', lw=0.9)
    a.text(2.17, -0.10, r'$-\mathrm{i}V_0$', fontsize=FS, ha='left',
           va='top')
    bubble(a, (2.05, 1.38), 0.47)
    a.text(2.05, 1.38, '$(-1)$', fontsize=FS - 1.5, ha='center',
           va='center')
    a.text(2.62, 1.60, r"$\mathrm{i}G_{\boldsymbol{k}'\nu}$",
           fontsize=FS, ha='left')
    varrow(a, (1.55, 1.42), 0.30, up=True)
    varrow(a, (1.66, 1.42), 0.30, up=False)
    a.text(0.15, 1.68, '(a)', fontsize=FS)

    # (b)
    a = fig.add_axes([0.47, 0.0, 0.53, 1.0])
    a.set_xlim(0, 4.3)
    a.set_ylim(0, 1.85)
    a.set_aspect('equal')
    a.axis('off')
    fline(a, (0.55, y0), (1.30, y0), arrows=(0.65,), lw=1.1)
    a.text(0.45, y0 - 0.10, r'$\boldsymbol{k},\omega$', fontsize=FS,
           ha='right', va='top')
    fline(a, (1.30, y0), (3.85, y0), arrows=(0.5,), lw=1.1)
    ts = np.linspace(0, 1, 100)
    ax_ = 1.30 + 2.55 * ts
    ay = y0 + 1.02 * np.sin(np.pi * ts)
    a.plot(ax_, ay, color='k', lw=1.0, ls=DASH)
    a.text(2.62, 1.52, r'$-\mathrm{i}V_{\boldsymbol{q}}$', fontsize=FS,
           ha='center', va='bottom')
    a.text(2.62, 0.12,
           r'$\mathrm{i}G_{\boldsymbol{k}-\boldsymbol{q},\omega-\nu}$',
           fontsize=FS, ha='center', va='top')
    varrow(a, (2.62, y0 + 0.07), 0.30)
    a.text(0.15, 1.68, '(b)', fontsize=FS)
    save('5.9')


# ---------------------------------------------------------------- 5.10
def fig_5_10():
    fig, ax = plt.subplots(figsize=(4.5, 1.3))
    ax.set_xlim(0, 5.4)
    ax.set_ylim(0, 1.45)
    ax.set_aspect('equal')
    ax.axis('off')
    y0 = 0.52
    fline(ax, (0.35, y0), (4.85, y0), arrows=(0.14, 0.50, 0.88),
          lw=1.1)
    for cx in (1.95, 3.25):
        ax.add_patch(plt.Circle((cx, y0), 0.30, facecolor='0.72',
                                edgecolor='k', lw=0.8, zorder=4))
        ax.text(cx, y0 + 0.42, r'$\mathrm{i}\Sigma_{\boldsymbol{k}\omega}$',
                fontsize=FS, ha='center')
    ax.text(0.90, 0.16, r'$\mathrm{i}G_{\boldsymbol{k}\omega}$',
            fontsize=FS, ha='center')
    ax.text(2.60, 0.16, r'$\mathrm{i}G_{\boldsymbol{k}\omega}$',
            fontsize=FS, ha='center')
    ax.text(4.30, 0.16, r'$\mathrm{i}G_{\boldsymbol{k}\omega}$',
            fontsize=FS, ha='center')
    varrow(ax, (0.35, y0 + 0.05), 0.24)
    varrow(ax, (2.60, y0 + 0.05), 0.24)
    varrow(ax, (4.85, y0 + 0.05), 0.24)
    save('5.10')


# ---------------------------------------------------------------- 5.11
def fig_5_11():
    fig = plt.figure(figsize=(5.7, 3.4))
    W, H = 3.3, 2.0
    y0 = 0.42
    pos = [(0.0, 0.505), (0.335, 0.505), (0.665, 0.505),
           (0.0, 0.0), (0.335, 0.0), (0.665, 0.0)]
    tags = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

    for i, (x0, yf) in enumerate(pos):
        a = fig.add_axes([x0, yf, 0.325, 0.48])
        a.set_xlim(0, W)
        a.set_ylim(0, H)
        a.set_aspect('equal')
        a.axis('off')
        a.text(0.12, 1.80, tags[i], fontsize=FS)

        if i in (0, 1, 3):
            a.text(0.98, y0 - 0.16, r'$\boldsymbol{k},\omega$',
                   fontsize=FS, ha='right', va='top')
        if i == 0:      # 泡泡 + 弦 + 竖直虚线
            fline(a, (0.30, y0), (1.68, y0), arrows=(0.62,), lw=1.1)
            dline(a, (1.68, 1.22 - 0.56), (1.68, -0.02))
            a.plot([1.58, 1.78], [-0.02, -0.02], color='k', lw=0.9)
            bubble(a, (1.68, 1.22), 0.56)
            dline(a, (1.12, 1.22), (2.24, 1.22))
        elif i == 1:    # 泡泡 + 虚线 + 泡泡
            fline(a, (0.30, y0), (1.35, y0), arrows=(0.68,), lw=1.1)
            dline(a, (1.35, 1.22 - 0.56), (1.35, -0.02))
            a.plot([1.25, 1.45], [-0.02, -0.02], color='k', lw=0.9)
            bubble(a, (1.35, 1.22), 0.56)
            dline(a, (1.91, 1.22), (2.35, 1.22))
            bubble(a, (2.90, 1.22), 0.56, arrow='wen')
        elif i == 2:    # 两条交叉虚线弧
            fline(a, (0.35, y0), (3.0, y0), arrows=(0.48, 0.72), lw=1.1)
            for xa, xb in ((0.35, 2.30), (1.05, 3.0)):
                ts = np.linspace(0, 1, 80)
                a.plot(xa + (xb - xa) * ts,
                       y0 + 1.30 * np.sin(np.pi * ts) ** 0.9,
                       color='k', lw=1.0, ls=DASH)
        elif i == 3:    # 泡泡 + 两条竖直虚线
            fline(a, (0.30, y0), (2.15, y0), arrows=(0.35, 0.68), lw=1.1)
            bubble(a, (1.55, 1.30), 0.62)
            for dx in (-0.17, 0.17):
                dline(a, (1.55 + dx * 1.55, 1.30 - 0.59),
                      (1.55 + dx, y0 + 0.01), dash=DASH_S)
        elif i == 4:    # 两条嵌套虚线弧
            fline(a, (0.55, y0), (2.75, y0), arrows=(0.5,), lw=1.1)
            for h in (1.02, 1.42):
                ts = np.linspace(0, 1, 80)
                a.plot(0.55 + 2.2 * ts, y0 + h * np.sin(np.pi * ts),
                       color='k', lw=1.0, ls=DASH)
        else:           # 两条分离虚线弧
            fline(a, (0.40, y0), (2.90, y0), arrows=(0.52,), lw=1.1)
            for xa, xb in ((0.55, 1.60), (1.70, 2.75)):
                ts = np.linspace(0, 1, 80)
                a.plot(xa + (xb - xa) * ts,
                       y0 + 1.05 * np.sin(np.pi * ts),
                       color='k', lw=1.0, ls=DASH)
    save('5.11')


# ---------------------------------------------------------------- 5.12
def fig_5_12():
    fig = plt.figure(figsize=(4.9, 2.55))

    # (a) 直接项
    a = fig.add_axes([0.0, 0.0, 0.50, 1.0])
    a.set_xlim(0, 4.2)
    a.set_ylim(0, 4.3)
    a.set_aspect('equal')
    a.axis('off')
    for x, kbl, ktp in ((1.15, r'$\boldsymbol{k}_1,\omega_1$',
                         r"$\boldsymbol{k}_1,\omega_1'$"),
                        (2.95, r'$\boldsymbol{k}_2,\omega_2$',
                         r"$\boldsymbol{k}_2,\omega_2'$")):
        fline(a, (x, 0.55), (x, 3.75), arrows=(0.24, 0.70), lw=1.1)
        a.text(x, 0.42, kbl, fontsize=FS, ha='center', va='top')
        a.text(x, 3.88, ktp, fontsize=FS, ha='center', va='bottom')
    dline(a, (1.15, 2.15), (2.95, 2.15))
    a.text(2.05, 1.95, r'$-\mathrm{i}V_{0,\nu}$', fontsize=FS,
           ha='center', va='top')
    a.text(0.15, 4.0, '(a)', fontsize=FS)

    # (b) 交换项
    a = fig.add_axes([0.47, 0.0, 0.53, 1.0])
    a.set_xlim(0, 4.6)
    a.set_ylim(0, 4.3)
    a.set_aspect('equal')
    a.axis('off')
    # 下半：竖直费米线
    for x, kl in ((1.15, r'$\boldsymbol{k}_1,\omega_1$'),
                  (3.35, r'$\boldsymbol{k}_2,\omega_2$')):
        fline(a, (x, 0.55), (x, 2.15), arrows=(0.42,), lw=1.1)
        a.text(x, 0.42, kl, fontsize=FS, ha='center', va='top')
    dline(a, (1.15, 2.15), (3.35, 2.15))
    a.text(2.25, 1.95, r'$-\mathrm{i}V_{\boldsymbol{q},\nu}$',
           fontsize=FS, ha='center', va='top')
    # 上半：交叉费米线
    fline(a, (1.15, 2.15), (3.35, 3.85), arrows=(0.80,), lw=1.1)
    fline(a, (3.35, 2.15), (1.15, 3.85), arrows=(0.80,), lw=1.1)
    a.text(1.15, 3.98, r"$\boldsymbol{k}_1,\omega_1'$", fontsize=FS,
           ha='center', va='bottom')
    a.text(3.35, 3.98, r"$\boldsymbol{k}_2,\omega_2'$", fontsize=FS,
           ha='center', va='bottom')
    a.text(0.15, 4.0, '(b)', fontsize=FS)
    save('5.12')


# ---------------------------------------------------------------- 5.13
def fig_5_13():
    fig = plt.figure(figsize=(5.4, 1.7))

    # (a) 相互作用产生粒子-空穴对
    a = fig.add_axes([0.0, 0.0, 0.50, 1.0])
    a.set_xlim(0, 4.2)
    a.set_ylim(0, 1.85)
    a.set_aspect('equal')
    a.axis('off')
    a.plot([0.55, 0.55], [0.62, 1.12], color='k', lw=1.0)      # 端点竖线
    dline(a, (0.55, 0.87), (1.95, 0.87))
    # q,nu 标注虚线箭头
    dline(a, (0.68, 1.25), (1.72, 1.25), dash=DASH_S)
    arr(a, (1.60, 1.25), (1.80, 1.25), lw=1.0, ms=9)
    a.text(1.24, 1.36, r'$\boldsymbol{q},\nu$', fontsize=FS, ha='center')
    a.text(1.10, 0.62, r'$-\mathrm{i}V_{\boldsymbol{q}\nu}$',
           fontsize=FS, ha='center', va='top')
    fline(a, (1.95, 0.87), (3.35, 1.75), arrows=(0.52,), lw=1.1)
    fline(a, (1.95, 0.87), (3.35, 0.0), arrows=(0.50,), lw=1.1)
    a.text(0.20, 1.62, '(a)', fontsize=FS)

    # (b) 粒子-空穴对修正相互作用
    a = fig.add_axes([0.48, 0.0, 0.52, 1.0])
    a.set_xlim(0, 4.4)
    a.set_ylim(0, 1.85)
    a.set_aspect('equal')
    a.axis('off')
    fline(a, (0.75, 1.78), (2.15, 0.90), arrows=(0.44,), lw=1.1)
    fline(a, (0.75, 0.0), (2.15, 0.84), arrows=(0.48,), lw=1.1)
    dline(a, (2.15, 0.87), (3.65, 0.87))
    a.plot([3.65, 3.65], [0.62, 1.12], color='k', lw=1.0)
    dline(a, (2.30, 1.25), (3.35, 1.25), dash=DASH_S)
    arr(a, (3.25, 1.25), (3.45, 1.25), lw=1.0, ms=9)
    a.text(2.92, 1.36, r'$\boldsymbol{q},\nu$', fontsize=FS, ha='center')
    a.text(2.95, 0.62, r'$-\mathrm{i}V_{\boldsymbol{q}\nu}$',
           fontsize=FS, ha='center', va='top')
    a.text(0.20, 1.62, '(b)', fontsize=FS)
    save('5.13')


# ---------------------------------------------------------------- 5.14
def fig_5_14():
    fig = plt.figure(figsize=(5.8, 1.55))
    ym = 0.62

    # 0 阶：竖线-虚线-竖线
    a = fig.add_axes([0.0, 0.0, 0.215, 1.0])
    a.set_xlim(0, 2.15)
    a.set_ylim(0, 1.55)
    a.set_aspect('equal')
    a.axis('off')
    a.plot([0.28, 0.28], [ym - 0.22, ym + 0.22], color='k', lw=1.0)
    dline(a, (0.28, ym), (1.85, ym))
    a.plot([1.85, 1.85], [ym - 0.22, ym + 0.22], color='k', lw=1.0)
    dline(a, (0.45, ym + 0.42), (1.40, ym + 0.42), dash=DASH_S)
    arr(a, (1.30, ym + 0.42), (1.50, ym + 0.42), lw=1.0, ms=9)
    a.text(0.92, ym + 0.54, r'$\boldsymbol{q},\nu$', fontsize=FS,
           ha='center')
    a.text(1.06, ym - 0.28, r'$-\mathrm{i}V_{\boldsymbol{q}\nu}$',
           fontsize=FS, ha='center', va='top')

    def rpa_term(a, nb, xmax):
        a.set_xlim(0, xmax)
        a.set_ylim(0, 1.55)
        a.set_aspect('equal')
        a.axis('off')
        rc = 0.46                      # 泡泡半径
        cxs = [1.62 + i * 1.24 for i in range(nb)]
        xe = xmax - 0.28
        # 左端竖线与虚线
        a.plot([0.28, 0.28], [ym - 0.22, ym + 0.22], color='k', lw=1.0)
        dline(a, (0.28, ym), (cxs[0] - rc, ym))
        a.text(0.28 + 0.35, ym - 0.28,
               r'$-\mathrm{i}V_{\boldsymbol{q}\nu}$', fontsize=FS - 0.5,
               ha='center', va='top')
        # 泡泡与间隔虚线
        for i, cx in enumerate(cxs):
            bubble(a, (cx, ym), rc, arrow='topcw')
            a.text(cx + 0.30, ym + 0.42,
                   r'$\mathrm{i}P^{00}_{\boldsymbol{q}\nu}$',
                   fontsize=FS - 0.5, ha='left')
            if i < nb - 1:
                dline(a, (cx + rc, ym), (cxs[i + 1] - rc, ym))
                a.text((cx + rc + cxs[i + 1] - rc) / 2, ym - 0.28,
                       r'$-\mathrm{i}V_{\boldsymbol{q}\nu}$',
                       fontsize=FS - 0.5, ha='center', va='top')
        # 右端虚线与竖线
        dline(a, (cxs[-1] + rc, ym), (xe, ym))
        a.text((cxs[-1] + rc + xe) / 2, ym - 0.28,
               r'$-\mathrm{i}V_{\boldsymbol{q}\nu}$', fontsize=FS - 0.5,
               ha='center', va='top')
        a.plot([xe, xe], [ym - 0.22, ym + 0.22], color='k', lw=1.0)
        # q,nu 标注虚线箭头（左上，避免与泡泡相碰）
        dline(a, (0.42, ym + 0.42), (cxs[0] - rc - 0.22, ym + 0.42),
              dash=DASH_S)
        arr(a, (cxs[0] - rc - 0.32, ym + 0.42), (cxs[0] - rc - 0.12,
                                                 ym + 0.42), lw=1.0, ms=9)
        a.text(0.85, ym + 0.54, r'$\boldsymbol{q},\nu$', fontsize=FS,
               ha='center')

    a = fig.add_axes([0.215, 0.0, 0.36, 1.0])
    rpa_term(a, 1, 3.75)
    a = fig.add_axes([0.575, 0.0, 0.425, 1.0])
    rpa_term(a, 2, 5.0)
    save('5.14')


# ---------------------------------------------------------------- 5.15
def fig_5_15():
    fig = plt.figure(figsize=(5.3, 2.35))

    # 左：费米海上的衰变示意
    a = fig.add_axes([0.0, 0.0, 0.52, 1.0])
    a.set_xlim(-1.75, 1.75)
    a.set_ylim(-1.5, 1.55)
    a.set_aspect('equal')
    a.axis('off')
    a.add_patch(plt.Circle((0, 0), 1.0, facecolor='0.90', edgecolor='k',
                           lw=1.1))
    # k -> q（左上到左下）
    ak = (-0.72, 0.78)
    aq = (-0.81, -0.86)
    a.add_patch(plt.Circle(ak, 0.055, color='k', zorder=5))
    a.add_patch(plt.Circle(aq, 0.055, color='k', zorder=5))
    fline(a, (-0.69, 0.70), (-0.79, -0.78), arrows=(0.55,), lw=1.0)
    a.text(-0.74, 0.94, r'$\boldsymbol{k}$', fontsize=FS, ha='center')
    a.text(-0.83, -1.02, r'$\boldsymbol{q}$', fontsize=FS, ha='center',
           va='top')
    # k' 空穴 -> k'' 粒子（右侧）
    ah = (1.03, -0.35)
    ap = (1.13, 0.25)
    a.add_patch(plt.Circle(ah, 0.055, facecolor='white', edgecolor='k',
                           lw=1.0, zorder=5))
    a.add_patch(plt.Circle(ap, 0.055, color='k', zorder=5))
    fline(a, (1.03, -0.27), (1.115, 0.17), arrows=(0.55,), lw=1.0)
    a.text(1.16, 0.42, r"$\boldsymbol{k}''$", fontsize=FS, ha='center')
    a.text(1.22, -0.48, r"$\boldsymbol{k}'$", fontsize=FS, ha='left')

    # 右：顶点图
    a = fig.add_axes([0.50, 0.0, 0.50, 1.0])
    a.set_xlim(-0.1, 3.4)
    a.set_ylim(0, 2.4)
    a.set_aspect('equal')
    a.axis('off')
    vx, vy = 1.85, 1.45          # 主顶点
    fline(a, (0.15, vy), (vx, vy), arrows=(0.42,), lw=1.1)
    a.text(0.35, vy + 0.10, r'$\boldsymbol{k}$', fontsize=FS, ha='left')
    # q 出射
    fline(a, (vx, vy), (2.62, 2.22), arrows=(0.62,), lw=1.1)
    a.text(2.68, 2.26, r'$\boldsymbol{q}$', fontsize=FS, ha='left')
    # 相互作用虚线短棒
    dline(a, (vx, vy), (2.02, 0.90), dash=DASH_S)
    v2x, v2y = 2.02, 0.90
    # k'' 入射（箭头指向顶点）
    fline(a, (3.30, v2y), (v2x, v2y), arrows=(0.42,), lw=1.1)
    a.text(2.98, v2y + 0.12, r"$\boldsymbol{k}''$", fontsize=FS,
           ha='center')
    # k' 线（箭头指向顶点）
    fline(a, (2.85, 0.18), (v2x, v2y), arrows=(0.40,), lw=1.1)
    a.text(2.92, 0.10, r"$\boldsymbol{k}'$", fontsize=FS, ha='left',
           va='top')
    save('5.15')


# ---------------------------------------------------------------- 5.16
def fig_5_16():
    fig, ax = plt.subplots(figsize=(3.7, 2.55))
    ax.set_xlim(0, 4.0)
    ax.set_ylim(0, 2.75)
    ax.set_aspect('equal')
    ax.axis('off')
    y0 = 0.42
    # 费米子线
    fline(ax, (0.42, y0), (3.55, y0), arrows=(0.5,), lw=1.1)
    # 大虚线弧（画整条，再用白面圆遮住中段）
    ts = np.linspace(0, 1, 160)
    ax_ = 0.42 + 3.13 * ts
    ay = y0 + 1.62 * np.sin(np.pi * ts) ** 0.82
    ax.plot(ax_, ay, color='k', lw=1.0, ls=DASH, zorder=2)
    # 中央实心圆泡泡
    c, r = (1.99, 1.62), 0.62
    ax.add_patch(plt.Circle(c, r, facecolor='white', edgecolor='k',
                            lw=1.05, zorder=4))
    bubble(ax, c, r, arrow='topcw')
    head(ax, on_circle(c, r, 99), on_circle(c, r, 66), ms=14)
    # 竖直点线
    ax.plot([c[0], c[0]], [-0.05, 2.50], color='k', lw=1.0,
            ls=(0, (1, 2.2)), zorder=3)
    ax.text(1.05, 1.80, r'$-\mathrm{i}V_{\boldsymbol{q}}$', fontsize=FS,
            ha='right')
    ax.text(2.95, 1.80, r'$-\mathrm{i}V_{\boldsymbol{q}}$', fontsize=FS,
            ha='left')
    save('5.16')


# ---------------------------------------------------------------- 5.17
def fig_5_17():
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    fig = plt.figure(figsize=(4.7, 4.0))
    ax = fig.add_subplot(111, projection='3d')
    n = 29
    xs = np.linspace(-np.pi, np.pi, n)
    X, Y = np.meshgrid(xs, xs)
    X, Y = Y, X          # 对称函数，交换使坐标轴方向与原书一致
    Z = -2 * (np.cos(X) + np.cos(Y))
    ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1, color='k', lw=0.32)
    ax.contour(X, Y, Z, levels=11, zdir='z', offset=-4.8, colors='k',
               linewidths=0.5)
    ax.set_xlim(np.pi, -np.pi)   # x: -3 在左后、3 在前（同原书）
    ax.set_ylim(-np.pi, np.pi)   # y: -3 在前、3 在右后（同原书）
    ax.set_zlim(-4.8, 4.2)
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_zticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
    ax.tick_params(labelsize=7.5, pad=-1)
    ax.view_init(elev=25, azim=-120)
    for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
        pane.set_facecolor('white')
        pane.set_edgecolor('k')
        pane.set_linewidth(0.5)
    ax.grid(False)
    save('5.17')


# ---------------------------------------------------------------- 5.18
def fig_5_18():
    fig = plt.figure(figsize=(5.6, 1.5))
    ym = 0.68
    r = 0.44

    # 第一项：单泡泡
    a = fig.add_axes([0.0, 0.0, 0.30, 1.0])
    a.set_xlim(0, 3.1)
    a.set_ylim(0, 1.5)
    a.set_aspect('equal')
    a.axis('off')
    dline(a, (0.30, ym), (1.35, ym), dash=DASH_S)
    arr(a, (1.22, ym), (1.42, ym), lw=1.0, ms=9)
    a.text(0.80, ym + 0.16, r'$\boldsymbol{q},\nu$', fontsize=FS,
           ha='center')
    a.add_patch(plt.Circle((1.85, ym), r, facecolor='none', edgecolor='k',
                           lw=1.05))
    head(a, on_circle((1.85, ym), r, 97), on_circle((1.85, ym), r, 66),
         ms=11)
    for sgn in (-1, 1):
        a.add_patch(plt.Circle((1.85 + sgn * r, ym), 0.045, color='k',
                               zorder=5))
    a.text(2.14, ym + 0.40, r'$\mathrm{i}\Pi^{00}_{\boldsymbol{q},\nu}$',
           fontsize=FS, ha='left')

    def term2(a):
        a.set_xlim(0, 5.6)
        a.set_ylim(0, 1.5)
        a.set_aspect('equal')
        a.axis('off')
        dline(a, (0.30, ym), (1.35, ym), dash=DASH_S)
        arr(a, (1.22, ym), (1.42, ym), lw=1.0, ms=9)
        a.text(0.80, ym + 0.16, r'$\boldsymbol{q},\nu$', fontsize=FS,
               ha='center')
        for cx in (1.85, 3.85):
            a.add_patch(plt.Circle((cx, ym), r, facecolor='none',
                                   edgecolor='k', lw=1.05))
            head(a, on_circle((cx, ym), r, 97), on_circle((cx, ym), r, 66),
                 ms=11)
            for sgn in (-1, 1):
                a.add_patch(plt.Circle((cx + sgn * r, ym), 0.045,
                                       color='k', zorder=5))
            a.text(cx + 0.30, ym + 0.40,
                   r'$\mathrm{i}\Pi^{00}_{\boldsymbol{q},\nu}$',
                   fontsize=FS, ha='left')
        dline(a, (1.85 + r, ym), (3.85 - r, ym))
        a.text(2.85, ym - 0.14, r'$-\mathrm{i}V_{\boldsymbol{q},\nu}$',
               fontsize=FS, ha='center', va='top')
        a.text(5.05, ym, r'$\cdots\ \cdots$', fontsize=FS + 1,
               ha='left', va='center')

    a = fig.add_axes([0.30, 0.0, 0.70, 1.0])
    term2(a)
    save('5.18')


# ---------------------------------------------------------------- 5.19
def fig_5_19():
    fig, ax = plt.subplots(figsize=(5.4, 1.65))
    ax.set_xlim(0, 9.4)
    ax.set_ylim(0, 2.85)
    ax.set_aspect('equal')
    ax.axis('off')
    ym = 1.42
    rr = 0.62
    xa, xb = 3.05, 7.75
    # 虚线入射箭头 q,nu
    dline(ax, (0.75, ym), (2.35, ym), dash=DASH_S)
    arr(ax, (2.22, ym), (2.44, ym), lw=1.0, ms=9)
    ax.text(1.55, ym + 0.20, r'$\boldsymbol{q},\nu$', fontsize=FS,
            ha='center')
    # 梯形图轮廓（左右半圆 + 上下横线）
    th = np.linspace(np.pi / 2, 3 * np.pi / 2, 80)
    ax.plot(xa + rr * np.cos(th), ym + rr * np.sin(th), color='k', lw=1.1)
    th = np.linspace(-np.pi / 2, np.pi / 2, 80)
    ax.plot(xb + rr * np.cos(th), ym + rr * np.sin(th), color='k', lw=1.1)
    ax.plot([xa, xb], [ym + rr, ym + rr], color='k', lw=1.1)
    ax.plot([xa, xb], [ym - rr, ym - rr], color='k', lw=1.1)
    # 顶点圆点
    for x in (xa, xb):
        ax.add_patch(plt.Circle((x, ym), 0.055, color='k', zorder=5))
    # 竖直虚线（相互作用）与标签
    for xd in (xa + 0.42 * (xb - xa), xa + 0.70 * (xb - xa)):
        dline(ax, (xd, ym - rr), (xd, ym + rr), dash=DASH_S)
        ax.text(xd - 0.10, ym + rr - 0.06, r'$-\mathrm{i}U$',
                fontsize=FS, ha='right', va='top')
    # 上下线箭头与 iP 标签
    xsegs = [(xa, xa + 0.42 * (xb - xa)),
             (xa + 0.42 * (xb - xa), xa + 0.70 * (xb - xa)),
             (xa + 0.70 * (xb - xa), xb)]
    for i, (u, v) in enumerate(xsegs):
        fline(ax, (u, ym + rr), (v, ym + rr), arrows=(), lw=1.1)
        head(ax, ((u + v) / 2 - 0.18, ym + rr), ((u + v) / 2 + 0.18,
                                                 ym + rr), ms=11)
        fline(ax, (u, ym - rr), (v, ym - rr), arrows=(), lw=1.1)
        head(ax, ((u + v) / 2 + 0.18, ym - rr), ((u + v) / 2 - 0.18,
                                                 ym - rr), ms=11)
        ax.text((u + v) / 2, ym + rr + 0.14,
                r'$\mathrm{i}\Pi^{00}_{\boldsymbol{q},\nu}$',
                fontsize=FS, ha='center', va='bottom')
    save('5.19')


# ---------------------------------------------------------------- 5.20
def fig_5_20():
    fig, ax = plt.subplots(figsize=(3.15, 3.1))
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.42, 1.48)
    ax.set_aspect('equal')
    ax.axis('off')
    # 外方框（第一布里渊区）
    ax.add_patch(plt.Rectangle((-1, -1), 2, 2, facecolor='none',
                               edgecolor='k', lw=0.9))
    # 细坐标轴
    ax.plot([-1.38, 1.38], [0, 0], color='k', lw=0.7)
    ax.plot([0, 0], [-1.38, 1.42], color='k', lw=0.7)
    # 约化区（菱形，阴影）
    ax.add_patch(plt.Polygon([(1, 0), (0, 1), (-1, 0), (0, -1)],
                             facecolor=GRAY, edgecolor='k', lw=1.0))
    # Q 箭头
    fline(ax, (-0.40, -0.40), (0.44, 0.44), arrows=(0.92,), lw=1.4)
    ax.text(0.47, 0.54, r'$\boldsymbol{Q}$', fontsize=FS + 1)
    save('5.20')


# ---------------------------------------------------------------- 5.21
def fig_5_21():
    fig, ax = plt.subplots(figsize=(4.6, 2.95))
    ax.set_xlim(-1.95, 2.15)
    ax.set_ylim(-1.15, 1.05)
    ax.set_aspect('equal')
    ax.axis('off')

    def P(u, v):
        return (u + 0.62 * v, 0.55 * v)

    # 平面（斜投影平行四边形）+ 前侧薄板
    FL, FR = P(-1, -1), P(1, -1)
    BL, BR = P(-1, 1), P(1, 1)
    t = 0.10
    poly = [FL, FR, (FR[0], FR[1] - t), (FL[0], FL[1] - t)]
    ax.add_patch(plt.Polygon(poly, facecolor='white', edgecolor='k',
                             lw=0.9))
    ax.plot([FL[0], BL[0]], [FL[1], BL[1]], color='k', lw=0.9)
    ax.plot([FR[0], BR[0]], [FR[1], BR[1]], color='k', lw=0.9)
    ax.plot([BL[0], BR[0]], [BL[1], BR[1]], color='k', lw=0.9)

    # 同心椭圆（瞬子等能线）
    for a_ in (0.18, 0.38, 0.58):
        ax.add_patch(Ellipse((0, 0), 2 * a_, 2 * a_ * 0.55,
                                 facecolor='none', edgecolor='k', lw=1.0))

    # 点线坐标轴（x 水平、tau 斜向）
    ax.plot([P(-1, 0)[0], P(1, 0)[0]], [0, 0], color='k', lw=0.9,
            ls=(0, (1, 2.2)))
    tau0, tau1 = P(0, -1), P(0, 1)
    ax.plot([tau0[0], tau1[0]], [tau0[1], tau1[1]], color='k', lw=0.9,
            ls=(0, (1, 2.2)))

    # 中心向上的自旋
    arr(ax, (0, 0.03), (0, 0.34), lw=1.3, ms=11)

    # 中程各方向的自旋投影箭头
    arr(ax, (-0.26, 0.135), (-0.46, 0.265), lw=1.0, ms=9)    # 左上
    arr(ax, (0.13, 0.215), (0.24, 0.40), lw=1.0, ms=9)       # 上（偏 tau 轴）
    arr(ax, (0.25, 0.14), (0.42, 0.25), lw=1.0, ms=9)        # 右上
    arr(ax, (-0.11, -0.06), (-0.28, -0.19), lw=1.0, ms=9)    # 左下
    # 水平轴上径向朝外的箭头
    arr(ax, (-0.50, 0.01), (-0.66, 0.01), lw=1.0, ms=9)
    arr(ax, (-0.80, -0.03), (-0.95, -0.09), lw=1.0, ms=9)
    arr(ax, (0.66, 0.01), (0.83, 0.01), lw=1.0, ms=9)
    arr(ax, (0.92, -0.02), (1.06, -0.11), lw=1.0, ms=9)
    # tau 轴上朝后/前的箭头
    arr(ax, (0.28, 0.25), (0.46, 0.41), lw=1.0, ms=9)
    arr(ax, (0.56, 0.49), (0.66, 0.41), lw=1.0, ms=9)
    # 边角处向下的自旋
    for p, h in ((BL, 0.18), (BR, 0.18), (P(-1, 0), 0.18),
                 (P(0, -1), 0.15)):
        arr(ax, (p[0], p[1] - 0.01), (p[0], p[1] - h), lw=1.0, ms=9)
    arr(ax, (FL[0], FL[1] - t - 0.01), (FL[0], FL[1] - t - 0.17),
        lw=1.0, ms=9)
    save('5.21')


# ----------------------------------------------------------------
ALL = {k: v for k, v in list(globals().items())
       if k.startswith('fig_5_') and callable(v)}
if __name__ == '__main__':
    for key in sorted(ALL):
        fn = ALL[key]
        fn()
        print('done', key.replace('fig_', ''))
