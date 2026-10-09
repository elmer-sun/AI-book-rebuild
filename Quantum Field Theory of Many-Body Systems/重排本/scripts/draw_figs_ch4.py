# -*- coding: utf-8 -*-
# 批次 B3：文小刚《多体量子场论》第4章插图 4.1–4.18（黑白矢量重绘）
# 依据：原书转换/pages/p163–p199（书页 148–184，pNNN = 书页 + 15）
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
    'hatch.linewidth': 0.5,
})

BASE = r"E:\AI整理书籍\文小刚\重排本"
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

DARK = '0.72'    # 深灰填充（原书深阴影）
LIGHT = '0.93'   # 浅灰填充（原书浅阴影）
HATCH = '///'    # 浅阴影的细斜纹
HATCH_E = '0.55'  # 斜纹颜色


def save(key):
    for ext, kw in (('pdf', {}), ('png', {'dpi': 160})):
        plt.savefig(os.path.join(FIGDIR if ext == 'pdf' else PREVDIR,
                                 f'fig_{key}.{ext}'),
                    bbox_inches='tight', pad_inches=0.03, **kw)
    plt.close()


def arr(ax, p, q, lw=1.2, ms=12, style='-|>', **kw):
    """自绘箭头（合同要求 annotate + arrowstyle '-|>'）。"""
    ax.annotate('', xy=q, xytext=p,
                arrowprops=dict(arrowstyle=style, lw=lw,
                                mutation_scale=ms, color='black',
                                shrinkA=0, shrinkB=0, **kw))


def circ_pts(c, r, a0, a1, n=80):
    a = np.linspace(np.deg2rad(a0), np.deg2rad(a1), n)
    return np.column_stack([c[0] + r * np.cos(a), c[1] + r * np.sin(a)])


def lens_patch(ax, c1, c2, r, facecolor='white', zorder=4):
    """两圆交叠区（透镜形）白色填充：4.7(b)/4.14(a)/4.15(a)。"""
    c1 = np.asarray(c1, float); c2 = np.asarray(c2, float)
    d = np.hypot(*(c2 - c1))
    phi = np.arctan2(c2[1] - c1[1], c2[0] - c1[0])
    alpha = np.arccos(d / (2 * r))
    p1 = circ_pts(c1, r, np.rad2deg(phi - alpha), np.rad2deg(phi + alpha), 90)
    p2 = circ_pts(c2, r, np.rad2deg(phi + np.pi - alpha),
                  np.rad2deg(phi + np.pi + alpha), 90)
    poly = np.vstack([p1, p2])
    ax.fill(poly[:, 0], poly[:, 1], facecolor=facecolor,
            edgecolor='none', zorder=zorder)


def light_circle(ax, c, r, z=2):
    ax.add_patch(plt.Circle(c, r, facecolor=LIGHT, edgecolor=HATCH_E,
                            lw=0, hatch=HATCH, zorder=z))


def dark_circle(ax, c, r, z=2):
    ax.add_patch(plt.Circle(c, r, facecolor=DARK, edgecolor='none', zorder=z))


# ---------------------------------------------------------------- 4.1
def fig_4_1():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(4.9, 2.0))
    # 左：抛物线 epsilon_k，费米海
    a = 1.55
    k = np.linspace(-1.16, 1.16, 400)
    a1.plot(k, a * k * k, color='k', lw=1.2)
    mu = 1.0
    for y in np.linspace(0.03, mu - 0.02, 14):   # 费米海横线
        w = np.sqrt(y / a)
        a1.plot([-w, w], [y, y], color='k', lw=0.55)
    a1.plot([0, 0], [-0.18, 2.3], color='k', lw=0.9)          # 竖轴
    a1.annotate('', xy=(1.58, 0), xytext=(-1.35, 0),           # k 轴
                arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
    a1.text(1.58, -0.16, '$k$', ha='center', va='top', fontsize=11)
    a1.text(0.06, 2.16, r'$\epsilon_{\boldsymbol{k}}$', fontsize=11)
    a1.text(-0.09, mu, r'$\mu$', ha='right', va='center', fontsize=11)
    arr(a1, (0.03, mu), (0.76, mu), lw=1.0, ms=13)             # mu -> k_F
    a1.text(0.40, mu + 0.12, r'$k_F$', ha='center', fontsize=11)
    a1.annotate('', xy=(1.22, mu), xytext=(1.22, 0.02),        # E_F 双箭头
                arrowprops=dict(arrowstyle='<|-|>', lw=1.0, color='k',
                                mutation_scale=13))
    a1.text(1.28, 0.5, r'$E_F$', ha='left', va='center', fontsize=11)
    a1.text(-0.56, 1.55, 'Empty', fontsize=11)
    a1.text(0.05, 0.52, 'Filled', fontsize=11,
            bbox=dict(facecolor='white', edgecolor='none', pad=0.6))
    a1.set_xlim(-1.45, 1.85)
    a1.set_ylim(-0.35, 2.45)
    a1.set_aspect('equal')
    a1.axis('off')
    # 右：占据数 n_k 台阶
    a2.add_patch(plt.Rectangle((0, 0), 0.95, 1.0, facecolor='0.88',
                               edgecolor='k', lw=1.0))
    a2.plot([0, 0], [0, 1.34], color='k', lw=0.9)
    a2.annotate('', xy=(1.72, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
    a2.text(1.72, -0.16, '$k$', ha='center', va='top', fontsize=11)
    a2.text(0.05, 1.28, r'$n_{\boldsymbol{k}}$', fontsize=11)
    a2.text(-0.08, 1.0, '1', ha='right', va='center', fontsize=11)
    a2.text(0.95, -0.14, r'$k_F$', ha='center', va='top', fontsize=11)
    a2.text(1.0, 1.2, 'Fermi surface', fontsize=11)
    arr(a2, (1.06, 1.16), (0.98, 1.03), lw=1.0, ms=11)
    a2.set_xlim(-0.25, 1.85)
    a2.set_ylim(-0.35, 1.5)
    a2.set_aspect('equal')
    a2.axis('off')
    save('4.1')


# ---------------------------------------------------------------- 4.2
def fig_4_2():
    fig, ax = plt.subplots(figsize=(2.8, 2.3))
    def eps(k):
        return 0.88 * np.tanh(2.4 * k)
    kd = np.linspace(0, 1.3 * np.pi, 200)
    ax.plot(kd, eps(kd), color='k', lw=1.3)                       # k>0 实线
    km = np.linspace(-1.3 * np.pi, 0, 200)
    ax.plot(km, eps(km), color='k', lw=1.3,
            linestyle=(0, (5, 4)))                                # k<0 虚线
    for kd0 in (0.42, 0.75, 1.25):                                # 能级（圆点）
        ax.plot(kd0, eps(kd0), 'o', ms=6.5, color='k')
    ax.plot([0, 0], [-1.25, 1.32], color='k', lw=0.9)
    ax.plot([-1.42 * np.pi, 1.42 * np.pi], [0, 0], color='k', lw=0.9)
    for s in (-1, 1):
        ax.plot([s * np.pi, s * np.pi], [-0.045, 0.045], color='k', lw=0.9)
        ax.text(s * np.pi, -0.13, r'$-\pi$' if s < 0 else r'$\pi$',
                ha='center', va='top', fontsize=11)
    ax.text(0.11 * np.pi, -0.15, r'$k>0$', ha='left', va='top', fontsize=11)
    ax.text(0.06, 1.2, r'$\epsilon$', fontsize=11)
    ax.set_xlim(-1.5 * np.pi, 1.5 * np.pi)
    ax.set_ylim(-1.42, 1.42)
    ax.set_aspect('equal')
    ax.axis('off')
    save('4.2')


# ---------------------------------------------------------------- 4.3
def fig_4_3():
    fig, ax = plt.subplots(figsize=(4.4, 2.1))
    P = {'i': (0, 0), 'k': (0, 1), 'l': (1, 1), 'j': (1, 0)}

    def panel(off, hops, tag):
        # hops: (编号, 起点, 终点, 标号绝对位置(相对面板))
        pts = {n: (p[0] + off, p[1]) for n, p in P.items()}
        for n, p in pts.items():
            ax.plot(*p, 'o', ms=8, color='k')
        ax.text(pts['k'][0] - 0.09, pts['k'][1] + 0.12,
                r'$\boldsymbol{k}$', fontsize=12)
        ax.text(pts['l'][0] + 0.09, pts['l'][1] + 0.12,
                r'$\boldsymbol{l}$', fontsize=12)
        ax.text(pts['i'][0], pts['i'][1] - 0.2, r'$\boldsymbol{i}$',
                ha='center', va='top', fontsize=12)
        ax.text(pts['j'][0], pts['j'][1] - 0.2, r'$\boldsymbol{j}$',
                ha='center', va='top', fontsize=12)
        for num, s, e, lp in hops:
            s0 = pts[s]
            e0 = pts[e]
            if abs(s0[0] - e0[0]) < 1e-9 and abs(s0[1] - e0[1] - 1) < 1e-9 \
                    and s0[0] + off > 0.5:   # 右侧上行竖箭头微左移
                s0 = (s0[0] - 0.03, s0[1])
            if abs(s0[0] - e0[0]) < 1e-9 and abs(s0[1] - e0[1] + 1) < 1e-9 \
                    and s0[0] + off > 0.5:   # 右侧下行竖箭头微右移
                s0 = (s0[0] + 0.05, s0[1])
                e0 = (e0[0] + 0.05, e0[1])
            arr(ax, s0, e0, lw=1.1, ms=15)
            ax.text(off + lp[0], lp[1], str(num),
                    ha='center', va='center', fontsize=12)
        ax.text(off - 0.55, 1.28, tag, fontsize=13)
    # (a)：1: i->k, 2: j->l, 3: l->i, 4: k->l, 5: l->j
    hops_a = [
        (1, 'i', 'k', (0.10, 0.50)),
        (2, 'j', 'l', (0.82, 0.50)),
        (3, 'l', 'i', (0.60, 0.34)),
        (4, 'k', 'l', (0.50, 1.15)),
        (5, 'l', 'j', (1.16, 0.50)),
    ]
    # (b)：1: i->k, 2: k->l, 3: l->i, 4: j->l, 5: l->j
    hops_b = [
        (1, 'i', 'k', (0.10, 0.50)),
        (2, 'k', 'l', (0.50, 1.15)),
        (3, 'l', 'i', (0.60, 0.34)),
        (4, 'j', 'l', (0.82, 0.50)),
        (5, 'l', 'j', (1.16, 0.50)),
    ]
    panel(0, hops_a, '(a)')
    panel(2.1, hops_b, '(b)')
    ax.set_xlim(-0.75, 3.45)
    ax.set_ylim(-0.42, 1.45)
    ax.set_aspect('equal')
    ax.axis('off')
    save('4.3')


# ---------------------------------------------------------------- 4.4
def fig_4_4():
    fig, ax = plt.subplots(figsize=(2.6, 3.0))
    rx, ry, h = 0.62, 0.13, 1.0
    for s in (1, -1):                                   # 上下锥
        th = np.linspace(0, 2 * np.pi, 200)
        ax.plot(rx * np.cos(th), s * h + ry * np.sin(th), color='k', lw=1.0)
        ax.plot([-rx, 0, rx], [s * h, 0, s * h], color='k', lw=1.0)
    rng = np.random.default_rng(7)
    def stipple(x0, x1, ytop, sgn, n=2400):
        # 楔形撒点：顶点(0,0) 到顶边 [x0,x1]，密度随远离顶点增大，
        # 且始终夹在锥面内部（|x| <= rx*y/h）
        pts = []
        while len(pts) < n:
            u, v = rng.random(2)
            y = v * ytop
            xw = 0.96 * rx * y / ytop
            lo, hi = max(x0, -xw), min(x1, xw)
            if lo >= hi:
                continue
            if rng.random() < 0.18 + 0.82 * (y / ytop) ** 2:
                pts.append((lo + (hi - lo) * u, sgn * y))
        pts = np.array(pts)
        ax.plot(pts[:, 0], pts[:, 1], '.', ms=0.55, color='0.1',
                alpha=0.9, zorder=3)
    stipple(-0.20, 0.42, 0.97, +1)                      # 上锥内楔形
    stipple(0.04, 0.56, 0.97, -1)                       # 下锥内楔形
    ax.set_xlim(-0.85, 0.85)
    ax.set_ylim(-1.35, 1.35)
    ax.set_aspect('equal')
    ax.axis('off')
    save('4.4')


# ---------------------------------------------------------------- 4.5
def fig_4_5():
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    boxes = [(0.5, 1.5, 'Metal L', 1.1), (1.75, 2.75, 'Metal R', 1.35)]
    yb, yt = 0.3, 2.3
    for x0, x1, lab, lev in boxes:
        ax.add_patch(plt.Rectangle((x0, yb), x1 - x0, lev - yb,
                                   facecolor='0.82', edgecolor='none'))
        ax.plot([x0, x0], [yb, yt], color='k', lw=1.0)
        ax.plot([x1, x1], [yb, yt], color='k', lw=1.0)
        ax.plot([x0, x1], [yt, yt], color='k', lw=1.0)
        ax.plot([x0, x1], [lev, lev], color='k', lw=1.0)
        ax.text((x0 + x1) / 2, yt + 0.12, lab, ha='center', fontsize=11)
    ax.plot([0.58, 1.42], [1.35, 1.35], color='k', lw=0.9,   # R 那侧虚线
            linestyle=(0, (5, 4)))
    ax.text(0.02, 1.42, 'Available\nstates', ha='right', va='center',
            fontsize=11)
    ax.annotate('', xy=(1.08, 1.2), xytext=(0.35, 1.33),
                arrowprops=dict(arrowstyle='-|>', lw=1.0, color='k',
                                connectionstyle='arc3,rad=-0.4',
                                mutation_scale=13))
    ax.annotate('', xy=(2.98, 1.38), xytext=(2.98, 1.07),     # V 双箭头
                arrowprops=dict(arrowstyle='<|-|>', lw=1.0, color='k',
                                mutation_scale=8))
    ax.text(3.08, 1.22, r'$V$', fontsize=12, va='center')
    ax.set_xlim(-0.75, 3.35)
    ax.set_ylim(0.1, 2.75)
    ax.set_aspect('equal')
    ax.axis('off')
    save('4.5')


# ---------------------------------------------------------------- 4.6
def fig_4_6():
    fig, ax = plt.subplots(figsize=(4.6, 2.5))
    x = np.linspace(-2.2, 2.2, 600)
    s = x * x / (x * x + 0.16)
    top, bot = 1.0, 0.0
    amp = 0.34
    ax.plot([-2.2, 2.2], [top, top], color='k', lw=0.9)
    ax.plot([-2.2, 2.2], [bot, bot], color='k', lw=0.9)
    ax.plot([0, 0], [-0.12, 1.56], color='k', lw=0.9)
    m = x <= 0                                               # A_{R-} 及其阴影
    ax.fill_between(x[m], top, top + amp * s[m], color='0.86', zorder=1)
    ax.plot(x[m], top + amp * s[m], color='k', lw=1.3, zorder=3)
    m = x >= 0                                               # A_{R+}
    ax.plot(x[m], top + amp * s[m], color='k', lw=1.3, zorder=3)
    m = x <= 0                                               # A_{L-}
    ax.plot(x[m], bot + amp * s[m], color='k', lw=1.3, zorder=3)
    m = x >= 0                                               # A_{L+} 及其阴影
    ax.fill_between(x[m], bot, bot + amp * s[m], color='0.86', zorder=1)
    ax.plot(x[m], bot + amp * s[m], color='k', lw=1.3, zorder=3)
    ax.text(-0.68, 1.47, r'$A_{R-}$', fontsize=12)
    ax.text(0.72, 1.47, r'$A_{R+}$', fontsize=12)
    ax.text(-0.68, 0.47, r'$A_{L-}$', fontsize=12)
    ax.text(0.56, 0.47, r'$A_{L+}$', fontsize=12)
    ax.plot([0.42, 0.42], [-0.035, 0.035], color='k', lw=1.0)
    ax.text(0.42, -0.16, r'$V$', ha='center', va='top', fontsize=12)
    ax.text(2.2, -0.16, r'$\nu$', ha='right', va='top', fontsize=12)
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-0.32, 1.72)
    ax.axis('off')
    save('4.6')


# ---------------------------------------------------------------- 4.7
def fig_4_7():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 2.0),
                                 gridspec_kw={'width_ratios': [1.35, 1]})
    # (a) 竖直面积隧穿结：上下两排格点 + 向下隧穿箭头
    a1.text(0.32, 0.9, '(a)', fontsize=12)
    for y, lab in ((0.62, 'R'), (0.38, 'L')):
        a1.plot([0.55, 3.25], [y, y], color='k', lw=0.9)
        a1.text(0.4, y, lab, ha='right', va='center', fontsize=12)
    xs = np.linspace(0.8, 2.96, 7)
    for x in xs:
        for y in (0.62, 0.38):
            a1.plot(x, y, 'o', ms=5.5, color='k')
    for x in (xs[:-1] + xs[1:]) / 2:
        arr(a1, (x, 0.575), (x, 0.425), lw=1.1, ms=10)
    a1.set_xlim(0.1, 3.45)
    a1.set_ylim(0.2, 0.95)
    a1.set_aspect('equal')
    a1.axis('off')
    # (b) 两片错移的费米面
    r, d = 0.72, 0.6
    dark_circle(a2, (0, 0), r)
    light_circle(a2, (d, 0), r)
    lens_patch(a2, (0, 0), (d, 0), r)                        # 交叠区留白
    a2.add_patch(plt.Circle((0, 0), r, fill=False, edgecolor='k',
                            lw=1.0, zorder=5))
    a2.add_patch(plt.Circle((d, 0), r, fill=False, edgecolor='k',
                            lw=1.0, zorder=5))
    a2.plot([-1.05, 1.7], [0, 0], color='k', lw=0.7, zorder=6)
    a2.plot([d / 2, d / 2], [-0.95, 0.95], color='k', lw=0.7, zorder=6)
    arr(a2, (0, 0), (d, 0), lw=2.2, ms=24, zorder=7)
    a2.text(d + 0.14, 0.22, r'$\boldsymbol{Q}$', fontsize=13, zorder=8,
            bbox=dict(facecolor='white', edgecolor='none', pad=0.5))
    a2.text(-1.0, 0.78, '(b)', fontsize=12)
    a2.set_xlim(-1.1, 1.8)
    a2.set_ylim(-1.0, 1.0)
    a2.set_aspect('equal')
    a2.axis('off')
    save('4.7')


# ---------------------------------------------------------------- 4.8
# 锚点 -> 傅里叶拟合的平滑周期 blob（左上有鼓包，与原书豆形费米面相近）
_THA = np.deg2rad(np.array([0, 25, 50, 75, 100, 125, 150, 180, 210,
                            240, 270, 300, 330], dtype=float))
_RA = np.array([1.00, 1.04, 1.06, 1.10, 1.14, 1.16, 1.09, 1.00,
                0.94, 0.95, 0.98, 1.03, 1.06])
_K = np.arange(0, 6)


def _fourier_fit():
    A = np.column_stack([np.cos(k * _THA) for k in _K]
                        + [np.sin(k * _THA) for k in _K[1:]])
    coef, *_ = np.linalg.lstsq(A, _RA, rcond=None)
    return coef


_COEF = _fourier_fit()


def blob_r(th):
    th = np.atleast_1d(th)
    A = np.column_stack([np.cos(k * th) for k in _K]
                        + [np.sin(k * th) for k in _K[1:]])
    return A @ _COEF


def blob_pts(n=3000):
    th = np.linspace(0, 2 * np.pi, n)
    r = blob_r(th)
    return np.column_stack([r * np.cos(th), r * np.sin(th)])


def fig_4_8():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.6, 2.6))
    xd, yd = np.cos(np.deg2rad(80)), np.sin(np.deg2rad(80))   # x-hat 方向
    nvec = np.array([xd, yd])
    td = np.array([np.cos(np.deg2rad(170)), np.sin(np.deg2rad(170))])
    pts = blob_pts()
    sup = pts @ nvec
    i_t = int(np.argmax(sup))
    p_t = pts[i_t]                               # 切点 = 沿 x-hat 的支撑点
    s_t = sup[i_t]
    line = np.array([p_t - 1.45 * td, p_t + 1.45 * td])
    # ---- (a)
    a1.fill(pts[:, 0], pts[:, 1], facecolor='0.87', edgecolor='k', lw=1.1)
    a1.plot([-1.6, 1.6], [0, 0], color='k', lw=0.7)
    a1.plot([0, 0], [-1.7, 1.7], color='k', lw=0.7)
    a1.plot(line[:, 0], line[:, 1], color='k', lw=0.8)
    arr(a1, (0, 0), p_t, lw=1.1, ms=13)
    a1.text(p_t[0] - 0.42, p_t[1] + 0.26, r'$\boldsymbol{k}_F(\hat{x})$',
            fontsize=12, ha='center')
    tip = 0.86 * s_t * nvec
    arr(a1, (0, 0), tip, lw=1.1, ms=13)
    a1.text(tip[0] + 0.16, tip[1] - 0.06, r'$\hat{x}$', fontsize=12)
    a1.text(-1.62, 1.5, '(a)', fontsize=12)
    a1.set_xlim(-1.8, 1.85)
    a1.set_ylim(-1.8, 1.72)
    a1.set_aspect('equal')
    a1.axis('off')
    # ---- (b) 带平坦段：沿割线切平（保留线下方的大块本体）
    s_cut = s_t - 0.17
    sd = pts @ nvec - s_cut
    mask = sd < 0                      # True = 线下方（本体）
    idx = np.where(mask[:-1] != mask[1:])[0]
    i0, i1 = int(idx[0]), int(idx[-1])     # i0: 本体->帽, i1: 帽->本体
    def interp(i):
        t = sd[i] / (sd[i] - sd[i + 1])
        return pts[i] + t * (pts[i + 1] - pts[i])
    q0, q1 = interp(i0), interp(i1)        # 帽两端 = 平坦段端点
    body = np.vstack([pts[i1 + 1:], pts[:i0 + 1]])
    poly = np.vstack([q1, body, q0])       # 闭合时 q0->q1 为直线（平坦段）
    a2.fill(poly[:, 0], poly[:, 1], facecolor='0.87', edgecolor='k', lw=1.1)
    a2.plot([-1.6, 1.6], [0, 0], color='k', lw=0.7)
    a2.plot([0, 0], [-1.7, 1.7], color='k', lw=0.7)
    a2.plot(line[:, 0], line[:, 1], color='k', lw=0.8)
    tip = s_cut * nvec
    arr(a2, (0, 0), tip, lw=1.1, ms=13)
    a2.text(tip[0] + 0.15, tip[1] + 0.08, r'$\hat{x}$', fontsize=12)
    a2.text(-1.62, 1.5, '(b)', fontsize=12)
    a2.set_xlim(-1.8, 1.85)
    a2.set_ylim(-1.8, 1.72)
    a2.set_aspect('equal')
    a2.axis('off')
    save('4.8')


# ---------------------------------------------------------------- 4.9
def stadium_h(cx=0.0, hw=0.55, hh=0.52, n=90):
    """水平胶囊形：总宽 2*(hw+hh)，高 2*hh。"""
    top = np.column_stack([np.linspace(-hw, hw, n), hh * np.ones(n)])
    right = circ_pts((cx + hw, 0), hh, 90, -90, n)
    bot = np.column_stack([np.linspace(hw, -hw, n), -hh * np.ones(n)])
    left = circ_pts((cx - hw, 0), hh, 270, 90, n)
    return np.vstack([top, right, bot, left])


def fig_4_9():
    fig, ax = plt.subplots(figsize=(3.2, 1.9))
    poly = stadium_h()
    ax.fill(poly[:, 0], poly[:, 1], facecolor='0.85', edgecolor='k', lw=1.1)
    ax.plot([-1.6, 1.6], [0, 0], color='k', lw=0.7)
    ax.plot([0, 0], [-0.82, 0.82], color='k', lw=0.7)
    arr(ax, (0.05, 0), (0.05, 0.56), lw=1.1, ms=13)
    ax.text(0.13, 0.63, r'$\boldsymbol{Q}$', fontsize=13)
    ax.set_xlim(-1.7, 1.7)
    ax.set_ylim(-0.95, 0.98)
    ax.set_aspect('equal')
    ax.axis('off')
    save('4.9')


# ---------------------------------------------------------------- 4.10
def fig_4_10():
    fig, ax = plt.subplots(figsize=(4.3, 2.3))
    x = np.linspace(0, 10.5, 1500)
    lam = 1.5

    def envf(x):
        return 1.25 * np.tanh((x / 0.32) ** 2) / (1 + x / 2.6)
    y = envf(x) * np.sin(2 * np.pi * x / lam)
    ax.plot(x, y, color='k', lw=1.1)
    xe = np.linspace(0.85, 10.5, 300)
    ax.plot(xe, envf(xe), 'k--', lw=0.8, dashes=(4, 3))
    ax.plot(xe, -envf(xe), 'k--', lw=0.8, dashes=(4, 3))
    ax.plot([0, 10.9], [0, 0], 'k--', lw=0.8, dashes=(4, 3))
    ax.plot([0, 0], [-1.25, 1.35], color='k', lw=0.9)
    ax.annotate('', xy=(11.15, -1.25), xytext=(0, -1.25),
                arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
    ax.text(11.15, -1.36, r'$x$', ha='center', va='top', fontsize=12)
    ax.annotate('', xy=(3.35, 0.47), xytext=(4.65, 0.82),
                arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k',
                                mutation_scale=12))
    ax.text(4.72, 0.84, r'$1/x^2$', fontsize=12, va='bottom')
    ax.annotate('', xy=(0.16, 0.18), xytext=(0.52, -0.72),
                arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k',
                                mutation_scale=12))
    ax.text(0.58, -0.80, r'$x^2$', fontsize=12, va='top')
    ax.set_xlim(-0.1, 11.4)
    ax.set_ylim(-1.6, 1.5)
    ax.axis('off')
    save('4.10')


# ---------------------------------------------------------------- 4.11
def fig_4_11():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.4, 2.5),
                                 gridspec_kw={'width_ratios': [1.25, 1]})
    # (a) 粒子–空穴连续区（d>1）
    m, vF = 0.5 * 2, 0.875          # eps_± = k^2/(2m') ± vF k, 2kF=1.75
    def wp(k):
        return 0.5 * k * k / 1.0 + vF * k
    def wm(k):
        return 0.5 * k * k / 1.0 - vF * k
    TOP, KMAX = 2.2, 3.3
    kx = np.linspace(0, 3.3, 500)
    kt = kx[wp(kx) <= TOP][-1]                 # 上边界穿出面板顶处的 k
    kr = np.linspace(1.75, 3.15, 200)          # 下边界 2kF -> 顶
    poly_x = np.concatenate([kx[kx <= kt], kr[::-1], [1.75], [0]])
    poly_y = np.concatenate([wp(kx[kx <= kt]),
                             np.clip(wm(kr), 0, TOP)[::-1], [0], [0]])
    a1.fill(poly_x, poly_y, facecolor='0.90', edgecolor=HATCH_E, lw=0,
            hatch='///', zorder=1)
    kk = np.linspace(0, kt, 200)
    a1.plot(kk, wp(kk), color='k', lw=1.3, zorder=3)
    kr = np.linspace(1.75, 3.15, 200)
    a1.plot(kr, wm(kr), color='k', lw=1.3, zorder=3)
    a1.plot([0, 0], [0, 2.45], color='k', lw=0.9, zorder=4)
    a1.annotate('', xy=(3.5, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k',
                                zorder=4))
    a1.text(3.5, -0.14, r'$k$', ha='center', va='top', fontsize=12)
    a1.text(-0.08, 2.4, r'$\omega$', ha='right', fontsize=12)
    a1.plot([1.75, 1.75], [0, 0.045], color='k', lw=1.0)
    a1.text(1.75, -0.13, r'$2k_F$', ha='center', va='top', fontsize=12)
    a1.plot([0, 0.85], [0, 0.74], color='k', lw=1.6)    # 切线段 eps=vF k
    a1.text(-0.1, 0.62, r'$\epsilon = v_F k$', ha='right', fontsize=12)
    kl = np.linspace(0, 1.05, 60)
    a1.plot(kl, 0.10 * (kl / 1.05) ** 2, color='k', lw=1.6)
    a1.text(0.55, -0.35, r'$\epsilon \ll v_F k$', ha='center', va='top',
            fontsize=12)
    a1.text(-0.45, 2.75, '(a)', fontsize=12)
    a1.set_xlim(-0.55, 3.7)
    a1.set_ylim(-0.55, 2.9)
    a1.set_aspect('equal')
    a1.axis('off')
    # (b) 费米面上的粒子–空穴激发
    a2.add_patch(plt.Circle((0, 0), 1.0, facecolor='0.90',
                            edgecolor=HATCH_E, lw=0, hatch='///', zorder=1))
    a2.add_patch(plt.Circle((0, 0), 1.0, fill=False, edgecolor='k',
                            lw=1.0, zorder=3))
    a2.plot([-1.45, 1.45], [0, 0], color='k', lw=0.7, zorder=4)
    a2.plot([0, 0], [-1.45, 1.45], color='k', lw=0.7, zorder=4)
    a2.plot(0.99 * np.cos(np.deg2rad(8)), 0.99 * np.sin(np.deg2rad(8)),
            'o', ms=8, mfc='white', mec='k', mew=1.3, zorder=6)
    a2.plot(1.18, 0, 'o', ms=7, color='k', zorder=6)
    arr(a2, (1.03, 0.09), (1.13, 0.015), lw=1.3, ms=11)
    a2.text(1.02, -0.28, r'$\epsilon = v_F k$', ha='left', fontsize=12)
    a2.plot(1.05, 0.72, 'o', ms=7, color='k', zorder=6)
    arr(a2, (1.02, 0.17), (1.03, 0.62), lw=1.0, ms=10)
    a2.text(1.20, 0.82, r'$\epsilon \ll v_F k$', ha='left', fontsize=12)
    a2.text(-1.42, 1.42, '(b)', fontsize=12)
    a2.set_xlim(-1.55, 2.5)
    a2.set_ylim(-1.55, 1.55)
    a2.set_aspect('equal')
    a2.axis('off')
    save('4.11')


# ---------------------------------------------------------------- 4.12
def fig_4_12():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 2.1))
    for ax in (a1, a2):
        ax.plot([-1.7, 1.7], [0, 0], color='k', lw=0.9)
        ax.plot([0, 0], [-1.15, 1.15], color='k', lw=0.9)
        ax.text(1.66, -0.14, r'$\omega$', ha='center', va='top', fontsize=12)
        ax.text(0.08, 1.0, r'$\mathrm{Im}\,\Pi^{00}$', fontsize=12)
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.3, 1.3)
        ax.axis('off')
    a1.text(-1.62, 1.12, '(a)', fontsize=12)
    # (a) d=3：线性，端点跳变
    a1.plot([-1, -1], [0, 0.78], color='k', lw=1.3)
    a1.plot([-1, 1], [0.78, -0.78], color='k', lw=1.3)
    a1.plot([1, 1], [-0.78, 0], color='k', lw=1.3)
    # (b) d=2：边缘发散
    a2.text(-1.62, 1.12, '(b)', fontsize=12)
    a2.plot([-1, -1], [0, 1.13], color='k', lw=1.0)
    a2.plot([1, 1], [0, -1.13], color='k', lw=1.0)
    xx = np.linspace(-0.985, 0.985, 800)
    a2.plot(xx, -1.05 * xx / np.sqrt(1 - xx * xx), color='k', lw=1.3)
    a2.set_ylim(-1.3, 1.3)
    save('4.12')


# ---------------------------------------------------------------- 4.13
def fig_4_13():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.6, 2.6))
    # (a) |k|>2kF：两圆分离
    dark_circle(a1, (-0.95, 0), 0.85)
    light_circle(a1, (0.95, 0), 0.85)
    for c in ((-0.95, 0), (0.95, 0)):
        a1.add_patch(plt.Circle(c, 0.85, fill=False, edgecolor='k',
                                lw=1.0, zorder=5))
    a1.plot([-2.15, 2.15], [0, 0], 'k--', lw=0.9, dashes=(5, 3), zorder=6)
    arr(a1, (-0.95, 0), (0.95, 0), lw=2.0, ms=24, zorder=7)
    a1.text(0.66, 0.16, r'$\boldsymbol{k}$', fontsize=13, zorder=8,
            bbox=dict(facecolor='white', edgecolor='none', pad=0.5))
    a1.plot([0, 0], [-1.35, 1.5], color='k', lw=0.9, zorder=6)
    a1.plot([-0.14, -0.14], [-1.35, 1.5], 'k--', lw=0.9, dashes=(5, 3),
            zorder=6)
    a1.text(-0.05, 1.62, r'$\sim\omega$', ha='center', fontsize=12)
    arr(a1, (-0.44, 1.28), (-0.17, 1.28), lw=1.0, ms=11)
    arr(a1, (0.30, 1.28), (0.03, 1.28), lw=1.0, ms=11)
    a1.set_xlim(-2.5, 2.5)
    a1.set_ylim(-1.75, 1.95)
    a1.set_aspect('equal')
    a1.axis('off')
    # (b) Im Pi00：|k|>2kF
    a2.plot([-2.4, 2.4], [0, 0], color='k', lw=0.9)
    a2.plot([0, 0], [-1.3, 1.3], color='k', lw=0.9)
    a2.text(2.36, -0.15, r'$\omega$', ha='center', va='top', fontsize=12)
    a2.text(0.08, 1.08, r'$\mathrm{Im}\,\Pi^{00}$', fontsize=12)
    a2.plot([-0.85, -0.85], [-1.3, 1.3], 'k--', lw=0.9, dashes=(5, 3))
    xa = np.linspace(-2.1, -0.85, 200)
    a2.plot(xa, 0.68 * np.sqrt((-0.85 - xa) / 1.25), color='k', lw=1.3)
    xb = np.linspace(0.85, 2.1, 200)
    a2.plot(xb, -0.68 * np.sqrt((xb - 0.85) / 1.25), color='k', lw=1.3)
    a2.set_xlim(-2.5, 2.5)
    a2.set_ylim(-1.4, 1.45)
    a2.set_aspect('equal')
    a2.axis('off')
    save('4.13')


# ---------------------------------------------------------------- 4.14
def fig_4_14():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.6, 2.6))
    # (a) |k|<2kF：两圆交叠，透镜留白
    dark_circle(a1, (-0.62, 0), 0.85)
    light_circle(a1, (0.62, 0), 0.85)
    lens_patch(a1, (-0.62, 0), (0.62, 0), 0.85)
    for c in ((-0.62, 0), (0.62, 0)):
        a1.add_patch(plt.Circle(c, 0.85, fill=False, edgecolor='k',
                                lw=1.0, zorder=5))
    a1.plot([-2.15, 2.15], [0, 0], 'k--', lw=0.9, dashes=(5, 3), zorder=6)
    arr(a1, (-0.62, 0), (0.62, 0), lw=2.0, ms=24, zorder=7)
    a1.text(0.38, 0.16, r'$\boldsymbol{k}$', fontsize=13, zorder=8,
            bbox=dict(facecolor='white', edgecolor='none', pad=0.5))
    a1.plot([0, 0], [-1.35, 1.5], color='k', lw=0.9, zorder=6)
    a1.plot([-0.14, -0.14], [-1.35, 1.5], 'k:', lw=1.1, zorder=6)
    a1.text(-0.05, 1.62, r'$\sim\omega$', ha='center', fontsize=12)
    arr(a1, (-0.44, 1.28), (-0.17, 1.28), lw=1.0, ms=11)
    arr(a1, (0.30, 1.28), (0.03, 1.28), lw=1.0, ms=11)
    a1.set_xlim(-2.5, 2.5)
    a1.set_ylim(-1.75, 1.95)
    a1.set_aspect('equal')
    a1.axis('off')
    # (b) Im Pi00：|k|<2kF，奇函数 S 形
    a2.plot([-2.4, 2.4], [0, 0], color='k', lw=0.9)
    a2.plot([0, 0], [-1.3, 1.3], color='k', lw=0.9)
    a2.text(2.36, -0.15, r'$\omega$', ha='center', va='top', fontsize=12)
    a2.text(0.08, 1.08, r'$\mathrm{Im}\,\Pi^{00}$', fontsize=12)
    a2.plot([-0.85, -0.85], [-1.3, 1.3], 'k:', lw=1.1)
    w, mo, h = 0.85, 0.42, 0.62
    xi = np.linspace(-w, w, 300)
    a2.plot(xi, -h * np.sin(np.pi * xi / (2 * w)), color='k', lw=1.3)
    xo = np.linspace(-2.15, -w, 60)
    a2.plot(xo, -mo * xo, color='k', lw=1.3)
    xo = np.linspace(w, 2.15, 60)
    a2.plot(xo, -mo * xo, color='k', lw=1.3)
    a2.set_xlim(-2.5, 2.5)
    a2.set_ylim(-1.4, 1.45)
    a2.set_aspect('equal')
    a2.axis('off')
    save('4.14')


def stadium_v(cx, hw=0.40, yh=0.66, n=90):
    """竖直胶囊形：宽 2*hw，总高 2*(yh+hw)。"""
    right = np.column_stack([cx + hw * np.ones(n),
                             np.linspace(-yh, yh, n)])
    top = circ_pts((cx, yh), hw, 0, 180, n)
    left = np.column_stack([cx - hw * np.ones(n),
                            np.linspace(yh, -yh, n)])
    bot = circ_pts((cx, -yh), hw, 180, 360, n)
    return np.vstack([right, top, left, bot])


# ---------------------------------------------------------------- 4.15
def fig_4_15():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.6, 2.7))
    # (a) 嵌套费米面 k=Q：两竖直胶囊交叠，交叠弧区留白
    sl = stadium_v(-0.36)
    sr = stadium_v(0.36)
    a1.fill(sl[:, 0], sl[:, 1], facecolor=DARK, edgecolor='k', lw=1.0,
            zorder=2)
    a1.fill(sr[:, 0], sr[:, 1], facecolor=LIGHT, edgecolor=HATCH_E, lw=0,
            hatch=HATCH, zorder=3)
    lens_patch(a1, (-0.36, 0.66), (0.36, 0.66), 0.40, zorder=4)
    lens_patch(a1, (-0.36, -0.66), (0.36, -0.66), 0.40, zorder=4)
    # 胶囊轮廓
    a1.plot(sl[:, 0], sl[:, 1], color='k', lw=1.0, zorder=5)
    a1.plot(sr[:, 0], sr[:, 1], color='k', lw=1.0, zorder=5)
    a1.plot([-1.15, 1.15], [0, 0], color='k', lw=0.9, zorder=6)
    arr(a1, (-0.36, 0), (0.36, 0), lw=2.0, ms=24, zorder=7)
    a1.text(0.24, 0.17, r'$\boldsymbol{k}$', fontsize=13, zorder=8,
            bbox=dict(facecolor='white', edgecolor='none', pad=0.5))
    a1.plot([0, 0], [-1.4, 1.62], color='k', lw=0.9, zorder=6)
    a1.plot([0.14, 0.14], [-1.4, 1.62], 'k--', lw=0.9, dashes=(5, 3),
            zorder=6)
    a1.text(0.06, 1.78, r'$\sim\omega$', ha='center', fontsize=12)
    arr(a1, (-0.22, 1.44), (-0.03, 1.44), lw=1.0, ms=11)
    arr(a1, (0.38, 1.44), (0.17, 1.44), lw=1.0, ms=11)
    a1.set_xlim(-1.35, 1.35)
    a1.set_ylim(-1.62, 1.98)
    a1.set_aspect('equal')
    a1.axis('off')
    # (b) Im Pi00：k=Q，omega=0 处跳变
    a2.plot([-2.4, 2.4], [0, 0], color='k', lw=0.9)
    a2.plot([0, 0], [-1.45, 1.4], color='k', lw=0.9)
    a2.text(2.36, -0.16, r'$\omega$', ha='center', va='top', fontsize=12)
    a2.text(0.08, 1.2, r'$\mathrm{Im}\,\Pi^{00}$', fontsize=12)
    a2.plot([0.38, 0.38], [-1.45, 1.45], 'k--', lw=0.9, dashes=(5, 3))
    xa = np.linspace(-2.1, 0, 300)
    a2.plot(xa, 0.55 + 0.64 * (-xa) / (0.55 + (-xa)), color='k', lw=1.3)
    xb = np.linspace(0, 2.1, 300)
    a2.plot(xb, -0.5 - 0.64 * xb / (0.55 + xb), color='k', lw=1.3)
    for y0 in (0.55, -0.5):
        a2.plot([-0.06, 0.06], [y0, y0], color='k', lw=1.2)
    a2.set_xlim(-2.5, 2.5)
    a2.set_ylim(-1.55, 1.55)
    a2.set_aspect('equal')
    a2.axis('off')
    save('4.15')


# ---------------------------------------------------------------- 4.16
def cross(ax, x, y, s=0.075, lw=2.0):
    ax.plot([x - s, x + s], [y - s, y + s], color='k', lw=lw)
    ax.plot([x - s, x + s], [y + s, y - s], color='k', lw=lw)


def fig_4_16():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0, 2.4))
    for ax in (a1, a2):
        ax.add_patch(plt.Circle((0, 0), 1.0, fill=False, edgecolor='k',
                                lw=1.1))
        ax.plot([-1.45, 1.45], [0, 0], color='k', lw=0.7)
        ax.plot([0, 0], [-1.45, 1.45], color='k', lw=0.7)
        ax.text(-1.42, 1.14, r'$|z|=1$', fontsize=12)
        ax.set_xlim(-1.65, 1.7)
        ax.set_ylim(-1.6, 1.6)
        ax.set_aspect('equal')
        ax.axis('off')
    a1.text(-1.6, 1.45, '(a)', fontsize=12)
    cross(a1, 0.55, 0.0)                     # 圆内极点
    cross(a1, 1.28, 0.0)                     # 圆外极点
    a2.text(-1.6, 1.45, '(b)', fontsize=12)
    c, s = np.cos(np.deg2rad(57)), np.sin(np.deg2rad(57))
    cross(a2, 1.06 * c, 1.06 * s)            # 圆外
    cross(a2, 0.94 * c, -0.94 * s)           # 圆内
    save('4.16')


# ---------------------------------------------------------------- 4.17
def fig_4_17():
    fig, ax = plt.subplots(figsize=(3.9, 3.8))
    ax.plot([0, 4, 4, 0, 0], [0, 0, 4, 4, 0], color='k', lw=1.5)
    for i in (1, 2, 3):
        ax.plot([i, i], [0, 4], color='k', lw=0.5)
        ax.plot([0, 4], [i, i], color='k', lw=0.5)
    # 小回路：格子单元 x:[1,2], y:[2,3]，逆时针
    ax.plot([1, 2, 2, 1, 1], [2, 2, 3, 3, 2], color='k', lw=1.7)
    arr(ax, (1.62, 3), (1.38, 3), lw=1.7, ms=26)     # 上边向左
    arr(ax, (1.38, 2), (1.62, 2), lw=1.7, ms=26)     # 下边向右
    arr(ax, (1, 2.62), (1, 2.38), lw=1.7, ms=26)     # 左边向下
    arr(ax, (2, 2.38), (2, 2.62), lw=1.7, ms=26)     # 右边向上
    # 大回路 C_k：沿右边界向上
    arr(ax, (4, 0.45), (4, 1.1), lw=1.7, ms=28)
    ax.text(4.16, 0.75, r'$C_{\boldsymbol{k}}$', fontsize=13, va='center')
    ax.text(0, 4.14, r'$2\pi$', ha='center', va='bottom', fontsize=12)
    ax.text(-0.14, 0, '0', ha='right', va='center', fontsize=12)
    ax.text(0, -0.16, '0', ha='center', va='top', fontsize=12)
    ax.text(4, -0.16, r'$2\pi$', ha='center', va='top', fontsize=12)
    # 2pi/L 标注
    ax.annotate('', xy=(-0.3, 3), xytext=(-0.3, 2),
                arrowprops=dict(arrowstyle='<|-|>', lw=1.0, color='k',
                                mutation_scale=16))
    ax.text(-0.46, 2.5, r'$2\pi/L$', ha='right', va='center', fontsize=12)
    ax.annotate('', xy=(2, -0.3), xytext=(1, -0.3),
                arrowprops=dict(arrowstyle='<|-|>', lw=1.0, color='k',
                                mutation_scale=16))
    ax.text(1.5, -0.52, r'$2\pi/L$', ha='center', va='top', fontsize=12)
    ax.set_xlim(-1.15, 4.95)
    ax.set_ylim(-1.0, 4.5)
    ax.set_aspect('equal')
    ax.axis('off')
    save('4.17')


# ---------------------------------------------------------------- 4.18
def fig_4_18():
    fig, ax = plt.subplots(figsize=(4.8, 3.0))
    A = np.array([0.0, 0.0])
    B = np.array([1.9, 0.0])
    D = np.array([0.55, 1.05])
    C = A + (B - A) + (D - A)
    sq = np.array([A, B, C, D, A])
    ax.plot(sq[:, 0], sq[:, 1], color='k', lw=1.1)
    def pos(u, v):
        return A + u * (B - A) + v * (D - A)
    centers = {'tl': pos(0.30, 0.75), 'tr': pos(0.72, 0.75),
               'bl': pos(0.30, 0.30), 'br': pos(0.72, 0.30)}
    for c in centers.values():
        ax.add_patch(Ellipse(c, 0.42, 0.36, fill=True,
                             facecolor='white', edgecolor='k', lw=1.1))
    def arrows(c, spec):
        for p, q in spec:
            arr(ax, (c[0] + p[0], c[1] + p[1]),
                (c[0] + q[0], c[1] + q[1]), lw=1.3, ms=11)
    U = 0.30; D2 = 0.10                     # 水平箭头内外长度
    NEo = ((0.13, 0.19), (0.30, 0.42))      # 外向 NE
    SWo = ((-0.13, -0.19), (-0.30, -0.42))  # 外向 SW
    NEi = ((0.17, 0.20), (0.03, 0.07))      # 内向（指向中心的 NE 对角）
    SWi = ((-0.17, -0.22), (-0.02, -0.05))
    arrows(centers['tl'], [((-U, 0), (-D2, 0)),          # 水平内向
                           ((U, 0), (D2, 0)),
                           ((0, 0.02), (0, -0.24)),      # 中心向下
                           NEo, SWo])
    arrows(centers['tr'], [((-D2, 0), (-U, 0)),          # 水平外向
                           ((D2, 0), (U, 0)),
                           ((0, -0.02), (0, 0.26)),      # 中心向上
                           NEo, SWo])
    arrows(centers['bl'], [((-U, 0), (-D2, 0)),
                           ((U, 0), (D2, 0)),
                           ((0, -0.02), (0, 0.28)),      # 中心向上（越顶）
                           NEi, SWi])
    arrows(centers['br'], [((-D2, 0), (-U, 0)),
                           ((D2, 0), (U, 0)),
                           ((0, 0.04), (0, -0.26)),      # 底部小箭头向下
                           NEi, SWi])
    ax.set_xlim(-0.12, 2.62)
    ax.set_ylim(-0.35, 1.28)
    ax.set_aspect('equal')
    ax.axis('off')
    save('4.18')


ALL = [fig_4_1, fig_4_2, fig_4_3, fig_4_4, fig_4_5, fig_4_6, fig_4_7,
       fig_4_8, fig_4_9, fig_4_10, fig_4_11, fig_4_12, fig_4_13,
       fig_4_14, fig_4_15, fig_4_16, fig_4_17, fig_4_18]

if __name__ == '__main__':
    import sys
    want = sys.argv[1:] or None
    for f in ALL:
        key = f.__name__.replace('fig_', '').replace('_', '.')
        if want and key not in want and f.__name__ not in want:
            continue
        f()
        print('done', key)
