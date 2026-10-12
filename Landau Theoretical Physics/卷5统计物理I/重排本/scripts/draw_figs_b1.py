# -*- coding: utf-8 -*-
"""
朗道《统计物理学I》（卷5）中文重排本 插图重绘 第一批：图1-图11
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p-041/062/067/138/142/163/179/193/204/212/216）。
注：图10 实际位于 p-212（清单写 p211 有偏移）。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Rectangle

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = r"E:\AI整理书籍\朗道理论物理教程\卷5统计物理I\重排本"
FIGD = os.path.join(BASE, 'figures')
PRED = os.path.join(FIGD, 'preview')
os.makedirs(PRED, exist_ok=True)

LW_MAIN, LW_AUX = 1.2, 0.8


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


# ---------------------------------------------------------------- 图1
def fig_1():
    """§8 熵涨落示意：S(t) 平台与两次涨落，虚线为 S1"""
    fig, ax = plt.subplots(figsize=(2.6, 2.1))
    plain_axes(ax)
    ax.set_xlim(-1.5, 11.2)
    ax.set_ylim(-1.2, 8.6)

    # 坐标轴
    arrow_axis(ax, 0, 0, 0, 8.3)
    arrow_axis(ax, 0, 0, 10.9, 0)
    ax.text(-0.45, 7.9, r'$S$', fontsize=11, ha='center', va='center')
    ax.text(10.55, -0.55, r'$t$', fontsize=11, ha='center', va='center')

    S_p, S_1 = 6.4, 5.55          # 平台（≈S_max）与虚线 S1
    t1a, t1b = 2.4, 4.6           # 涨落1（触到 S1）
    t2a, t2b = 6.0, 7.4           # 涨落2（低于 S1）
    t = [0.0]
    S = [S_p]
    tt = np.linspace(t1a, t1b, 80)
    t = np.concatenate([t, tt]); S = np.concatenate([S, S_p - 0.85 * np.sin(np.pi * (tt - t1a) / (t1b - t1a)) ** 2])
    tt = np.linspace(t2a, t2b, 80)
    t = np.concatenate([t, tt]); S = np.concatenate([S, S_p - 1.55 * np.sin(np.pi * (tt - t2a) / (t2b - t2a)) ** 2])
    t = np.concatenate([t, [10.6]]); S = np.concatenate([S, [S_p]])
    ax.plot(t, S, 'k-', lw=1.4)

    ax.plot([0, 6.6], [S_1, S_1], 'k--', lw=0.9)          # S1 虚线
    ax.text(-0.25, S_p + 0.35, r'$S_{\max}$', fontsize=10, ha='right', va='center')
    ax.text(0.3, S_1 - 0.62, r'$S_1$', fontsize=10, ha='center', va='center')
    ax.text(3.5, S_1 - 0.62, '1', fontsize=10, ha='center', va='center')
    ax.text(6.25, S_1 - 0.62, '2', fontsize=10, ha='center', va='center')
    save(fig, 1)


# ---------------------------------------------------------------- 图2
def fig_2():
    """§18 焦耳-汤姆孙多孔壁示意"""
    fig, ax = plt.subplots(figsize=(2.4, 0.9))
    plain_axes(ax)
    ax.set_xlim(-0.35, 10.35)
    ax.set_ylim(-0.85, 2.75)
    ax.set_aspect('equal')

    # 气缸上下壁
    ax.plot([0, 10], [1.9, 1.9], 'k-', lw=1.4)
    ax.plot([0, 10], [0, 0], 'k-', lw=1.4)
    # 活塞（双线）
    for xp in (2.0, 7.86):
        ax.plot([xp, xp], [0, 1.9], 'k-', lw=1.1)
        ax.plot([xp + 0.14, xp + 0.14], [0, 1.9], 'k-', lw=1.1)
    # 活塞杆（双线，从开口端到活塞）
    for x0, x1 in ((0.0, 2.0), (8.0, 10.0)):
        for y in (0.84, 1.06):
            ax.plot([x0, x1], [y, y], 'k-', lw=1.0)
    # 多孔壁（斜线阴影）+ 白底字母 a
    ax.add_patch(Rectangle((4.9, 0), 0.55, 1.9, facecolor='white',
                           edgecolor='k', lw=1.1, hatch='//////'))
    ax.add_patch(Rectangle((5.02, 0.68), 0.31, 0.54, facecolor='white',
                           edgecolor='none'))
    ax.text(5.175, 0.95, r'$a$', fontsize=9.5, ha='center', va='center')
    # 压强区标注
    ax.text(3.45, 0.97, r'$P_1$', fontsize=9.5, ha='center', va='center')
    ax.text(6.6, 0.97, r'$P_2$', fontsize=9.5, ha='center', va='center')
    # 流动方向箭头（活塞杆上方）
    ax.annotate('', xy=(1.75, 1.38), xytext=(0.45, 1.38),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0, mutation_scale=9))
    ax.annotate('', xy=(9.55, 1.38), xytext=(8.25, 1.38),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0, mutation_scale=9))
    save(fig, 2)


# ---------------------------------------------------------------- 图3
def fig_3():
    """§20 S_t(E_t) 曲线，a、b、c 与 R_min 构造"""
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(2.95, 2.75))
    plain_axes(ax)
    ax.set_xlim(-1.3, 10.2)
    ax.set_ylim(-1.3, 10.2)

    arrow_axis(ax, 0, 0, 0, 9.9)
    arrow_axis(ax, 0, 0, 10.0, 0)
    ax.text(-0.55, 9.45, r'$S_{\rm t}$', fontsize=11, ha='center', va='center')
    ax.text(9.55, -0.62, r'$E_{\rm t}$', fontsize=11, ha='center', va='center')

    pts = [(2.45, 3.55), (3.0, 4.5), (3.35, 5.0), (3.9, 5.7), (4.6, 6.4),
           (5.4, 7.05), (6.25, 7.5), (7.5, 8.15)]
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    f = PchipInterpolator(xs, ys)
    xx = np.linspace(xs[0], xs[-1], 300)
    ax.plot(xx, f(xx), 'k-', lw=1.4)

    xa, xc, xb = 6.25, 3.35, 6.25
    ya, yc, yb = 7.5, 5.0, 5.0
    ax.plot([xa, xa], [ya, yb], 'k--', lw=0.9)      # a->b 竖直虚线
    ax.plot([xc, xb], [yc, yb], 'k--', lw=0.9)      # c->b 水平虚线
    ax.text(xa - 0.15, ya + 0.35, r'$a$', fontsize=10, ha='center', va='center')
    ax.text(xb + 0.32, yb, r'$b$', fontsize=10, ha='left', va='center')
    ax.text(xc - 0.32, yc, r'$c$', fontsize=10, ha='right', va='center')
    ax.text(xa + 0.22, (ya + yb) / 2 + 0.15, r'$-\Delta S_{\rm t}$',
            fontsize=9.5, ha='left', va='center')
    ax.text((xc + xb) / 2 + 0.3, yc - 0.72, r'$R_{\min}$',
            fontsize=9.5, ha='center', va='center')
    save(fig, 3)


# ---------------------------------------------------------------- 图4
def fig_4():
    """§47 转动比热 c_rot(2TI/hbar^2)"""
    x = np.linspace(0.001, 1.4, 400)
    l = np.arange(0, 260)[:, None]
    w = np.exp(-l * (l + 1) / x) * (2 * l + 1)          # Z(x)
    # 用对数稳定求和
    m = w.max(axis=0); w = w / m
    Z = w.sum(axis=0) * m
    dZ = ((w * l * (l + 1)).sum(axis=0) * m)            # -dZ/du > 0
    f = (dZ / Z) / x                                     # <E>/T
    c = f + x * np.gradient(f, x)                        # c_rot = d<E>/dT
    fig, ax = plt.subplots(figsize=(2.76, 2.5))
    ax.set_xlim(0, 1.4); ax.set_ylim(0, 1.2)
    ax.set_xticks(np.arange(0, 1.41, 0.2))
    ax.set_xticklabels(['0', '', '0.4', '', '0.8', '', '1.2', '1.4'])
    ax.set_yticks(np.arange(0, 1.21, 0.2))
    ax.set_yticklabels(['', '0.2', '0.4', '0.6', '0.8', '1.0', '1.2'])
    ax.tick_params(length=2.5, labelsize=8.5)
    ax.grid(True, lw=0.7, color='k')
    for s in ax.spines.values():
        s.set_linewidth(1.1)
    ax.plot(x, c, 'k-', lw=1.6)
    ax.set_ylabel(r'$c_{\rm rot}$', fontsize=10)
    ax.set_xlabel(r'$\dfrac{2TI}{\hbar^2}$', fontsize=11)
    save(fig, 4)


# ---------------------------------------------------------------- 图5
def fig_5():
    """§49 振动比热 c_vib(T/hbar omega)"""
    u = np.linspace(0.02, 1.4, 500)
    xg = 1.0 / u
    cv = xg ** 2 / (4.0 * np.sinh(xg / 2.0) ** 2)   # 稳定形式
    fig, ax = plt.subplots(figsize=(2.76, 2.5))
    ax.set_xlim(0, 1.4); ax.set_ylim(0, 1.0)
    ax.set_xticks(np.arange(0, 1.41, 0.2))
    ax.set_xticklabels(['%g' % v for v in np.arange(0, 1.41, 0.2)])
    ax.set_yticks(np.arange(0, 1.01, 0.2))
    ax.set_yticklabels(['', '0.2', '0.4', '0.6', '0.8', '1.0'])
    ax.tick_params(length=2.5, labelsize=8.5)
    ax.grid(True, lw=0.7, color='k')
    for s in ax.spines.values():
        s.set_linewidth(1.1)
    ax.plot(u, cv, 'k-', lw=1.6)
    ax.set_ylabel(r'$c_{\rm vib}$', fontsize=10)
    ax.set_xlabel(r'$\dfrac{T}{\hbar\omega}$', fontsize=11)
    save(fig, 5)


# ---------------------------------------------------------------- 图6
def fig_6():
    """§57 T=0 费米阶跃（实线）与 T>0 分布（虚线），T 宽度箭头"""
    fig, ax = plt.subplots(figsize=(2.36, 1.6))
    plain_axes(ax)
    ax.set_xlim(-0.55, 7.85)
    ax.set_ylim(-0.62, 1.85)

    arrow_axis(ax, 0, 0, 0, 1.75)
    arrow_axis(ax, 0, 0, 7.7, 0)
    ax.text(7.35, -0.24, r'$\varepsilon$', fontsize=11, ha='center', va='center')
    ax.text(-0.22, 1.0, '1', fontsize=10, ha='right', va='center')

    mu, T, W = 5.6, 0.4, 1.28          # W = 3.2T：虚线的左右界
    # T=0 阶跃（实线）
    ax.plot([0, mu], [1, 1], 'k-', lw=1.5)
    ax.plot([mu, mu], [1, 0], 'k-', lw=1.5)
    ax.plot([mu, mu + W], [0, 0], 'k-', lw=1.5)
    # T>0 分布（虚线），末端落在横轴上
    xx = np.linspace(mu - W, mu + W, 300)
    n = 1.0 / (np.exp((xx - mu) / T) + 1)
    n[-1] = 0.004
    ax.plot(xx, n, 'k--', lw=1.0, dashes=(5, 2.2))
    # 左虚竖线（T 区间左界）与右短竖线
    ax.plot([mu - W, mu - W], [1.0, -0.42], 'k--', lw=0.9)
    ax.plot([mu + W, mu + W], [0, -0.42], 'k-', lw=0.9)
    # T 双向箭头
    ax.annotate('', xy=(mu + W, -0.32), xytext=(mu - W, -0.32),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=1.0,
                                mutation_scale=11))
    ax.text(mu, -0.13, r'$T$', fontsize=10, ha='center', va='center')
    ax.text(mu - 0.16, 0.14, r'$\varepsilon_{\rm F}$', fontsize=10,
            ha='right', va='center')
    save(fig, 6)


# ---------------------------------------------------------------- 图7
def fig_7():
    """§63 普朗克分布 x^3/(e^x-1)"""
    x = np.linspace(0.001, 8, 500)
    y = x ** 3 / np.expm1(x)
    fig, ax = plt.subplots(figsize=(2.76, 2.55))
    ax.set_xlim(0, 8); ax.set_ylim(0, 1.6)
    ax.set_xticks(np.arange(0, 8.1, 1))
    ax.set_xticklabels(['%g' % v for v in np.arange(0, 9, 1)])
    ax.set_yticks(np.arange(0, 1.61, 0.2))
    ax.set_yticklabels([''] + ['%.1f' % v for v in np.arange(0.2, 1.61, 0.2)])
    ax.tick_params(length=2.5, labelsize=8.5)
    ax.grid(True, lw=0.7, color='k')
    for s in ax.spines.values():
        s.set_linewidth(1.1)
    ax.plot(x, y, 'k-', lw=1.6)
    ax.set_ylabel(r'$\dfrac{x^3}{e^x-1}$', fontsize=11)
    ax.set_xlabel(r'$x$', fontsize=10)
    save(fig, 7)


# ---------------------------------------------------------------- 图8
def fig_8():
    """§66 德拜热容 C/3Nnu 对 T/Theta"""
    def debye_C(x):
        u = 1.0 / x
        n = np.arange(1, 4000)[:, None]
        # integral_0^u z^3/(e^z-1) dz = sum_n (1/n^4)[6 - e^{-nu}(n^3u^3+3n^2u^2+6nu+6)]
        nu = n * u
        tail = np.exp(-nu) * (nu ** 3 + 3 * nu ** 2 + 6 * nu + 6)
        I = ((6.0 - tail) / n ** 4).sum(axis=0)
        D = 3.0 * I / u ** 3
        return 4 * D - 3 * u / np.expm1(u)

    x = np.linspace(0.02, 1.4, 400)
    C = debye_C(x)
    C = np.concatenate([[0.0], C]); x = np.concatenate([[0.0], x])
    fig, ax = plt.subplots(figsize=(2.76, 2.5))
    ax.set_xlim(0, 1.4); ax.set_ylim(0, 1.0)
    ax.set_xticks(np.arange(0, 1.41, 0.2))
    ax.set_xticklabels(['%g' % v for v in np.arange(0, 1.41, 0.2)])
    ax.set_yticks(np.arange(0, 1.01, 0.2))
    ax.set_yticklabels(['', '0.2', '0.4', '0.6', '0.8', '1.0'])
    ax.tick_params(length=2.5, labelsize=8.5)
    ax.grid(True, lw=0.7, color='k')
    for s in ax.spines.values():
        s.set_linewidth(1.1)
    ax.plot(x, C, 'k-', lw=1.6)
    ax.set_ylabel(r'$\dfrac{C}{3N\nu}$', fontsize=11)
    ax.set_xlabel(r'$T/\Theta$', fontsize=10)
    save(fig, 8)


# ---------------------------------------------------------------- 图9
def fig_9():
    """§70 鞍点附近的等频面：双叶双曲面(ω<ω0)、锥面(ω=ω0)、单叶双曲面(ω>ω0)"""
    fig, ax = plt.subplots(figsize=(2.4, 4.35))
    plain_axes(ax)
    ax.set_xlim(-2.75, 2.95)
    ax.set_ylim(-3.75, 3.95)
    ax.set_aspect('equal')
    K = 0.28          # 椭圆纵横比（透视）

    def ell(z0, rx, front=None, lw=1.2):
        """front: None=整圆, 'lower'=实线下半+虚线上半, 'upper'=实线上半+虚线下半"""
        ry = rx * K
        if front is None:
            ax.add_patch(Arc((0, z0), 2 * rx, 2 * ry, theta1=0, theta2=360,
                             lw=lw, color='k'))
        elif front == 'lower':
            ax.add_patch(Arc((0, z0), 2 * rx, 2 * ry, theta1=0, theta2=180,
                             lw=0.9, color='k', ls=(0, (4, 2.5))))
            ax.add_patch(Arc((0, z0), 2 * rx, 2 * ry, theta1=180, theta2=360,
                             lw=lw, color='k'))
        else:
            ax.add_patch(Arc((0, z0), 2 * rx, 2 * ry, theta1=180, theta2=360,
                             lw=0.9, color='k', ls=(0, (4, 2.5))))
            ax.add_patch(Arc((0, z0), 2 * rx, 2 * ry, theta1=0, theta2=180,
                             lw=lw, color='k'))

    def bowl(zv, zr, rr, ls='-'):
        """双叶双曲面一叶：zv 顶点, zr 边缘高度, rr 边缘半径"""
        z = np.linspace(zv, zr, 120)
        r = rr * np.sqrt((z ** 2 - zv ** 2) / (zr ** 2 - zv ** 2))
        for sgn in (1, -1):
            if ls == '-':
                ax.plot(sgn * r, z, 'k-', lw=1.2)
            else:
                ax.plot(sgn * r, z, 'k--', lw=0.9, dashes=(4, 2.5))

    def hourglass(w, zr, rr):
        """单叶双曲面（腰半径 w, 顶部半径 rr 于 zr）"""
        zc = zr / np.sqrt((rr / w) ** 2 - 1)
        z = np.linspace(-zr, zr, 200)
        r = w * np.sqrt(1 + (z / zc) ** 2)
        for sgn in (1, -1):
            ax.plot(sgn * r, z, 'k-', lw=1.2)

    # ---- 虚线部分（锥面轮廓、下叶轮廓、隐藏弧）----
    # 锥面（ω=ω0）轮廓：上圆边 -> 原点 -> 下圆边
    for sx in (1, -1):
        ax.plot([sx * 1.15, 0], [2.4, 0], 'k--', lw=0.9, dashes=(4, 2.5))
        ax.plot([0, sx * 1.15], [0, -2.4], 'k--', lw=0.9, dashes=(4, 2.5))
    bowl(-1.05, -2.8, 0.92, ls='--')                 # 下叶轮廓（隐藏）
    ell(2.15, 1.56, front='lower')                   # 单叶双曲面上缘：背面虚
    ell(-2.15, 1.56, front='lower')                  # 下缘：背面虚
    ell(-2.4, 1.15, front='lower')                   # 下锥面圆：背面虚

    # ---- 实线部分 ----
    bowl(1.05, 2.8, 0.92)                            # ω<ω0 上叶（实）
    ell(2.8, 0.92)                                   # 上叶边缘圆
    ell(2.4, 1.15)                                   # 锥面截面圆（上）
    hourglass(0.56, 2.15, 1.56)                      # ω>ω0 单叶双曲面轮廓
    ell(-2.8, 0.92)                                  # 下叶边缘圆（最下，实）

    # 坐标轴
    ax.plot([0, 0], [-3.55, 3.55], 'k-', lw=0.9)
    arrow_axis(ax, 0, 3.55, 0, 3.9)
    ax.plot([-2.35, 2.35], [0, 0], 'k-', lw=0.9)
    ax.text(-0.5, 3.72, r'$\kappa_z$', fontsize=10, ha='center', va='center')

    # 标注
    ax.text(1.35, 2.8, r'$\omega<\omega_0$', fontsize=10, ha='left', va='center')
    ax.text(1.35, 2.05, r'$\omega=\omega_0$', fontsize=10, ha='left', va='center')
    ax.text(1.72, 1.35, r'$\omega>\omega_0$', fontsize=10, ha='left', va='center')
    save(fig, 9)


# ---------------------------------------------------------------- 图10
def fig_10():
    """§73 负温度：S(E) 单峰曲线"""
    fig, ax = plt.subplots(figsize=(2.56, 1.95))
    plain_axes(ax)
    ax.set_xlim(-1.0, 11.0)
    ax.set_ylim(-1.7, 6.9)

    arrow_axis(ax, 0, 0, 0, 6.7)
    arrow_axis(ax, 0, 0, 10.7, 0)
    ax.text(-0.5, 6.15, r'$S$', fontsize=11, ha='center', va='center')
    ax.text(10.2, 0.5, r'$E$', fontsize=11, ha='center', va='center')

    x0, x1, xp, H = 1.7, 9.85, 4.5, 4.5
    u = np.linspace(0, 1, 400)
    xx = x0 + u * (x1 - x0)
    p, q = 0.75, 1.0
    S = u ** p * (1 - u) ** q
    S = H * S / S.max()
    ax.plot(xx, S, 'k-', lw=1.4)
    ax.plot([xp, xp], [H, 0], 'k--', lw=0.9)

    ax.text(3.35, 1.55, r'$T>0$', fontsize=9, ha='center', va='center')
    ax.text(6.2, 1.5, r'$T<0$', fontsize=9, ha='center', va='center')
    ax.text(1.65, -1.05, r'$T=0+$', fontsize=9, ha='center', va='center')
    ax.text(xp, -1.05, r'$T=\pm\infty$', fontsize=9, ha='center', va='center')
    ax.text(9.6, -1.05, r'$T=0-$', fontsize=9, ha='center', va='center')
    save(fig, 10)


# ---------------------------------------------------------------- 图11
def fig_11():
    """§74 原子相互作用势 U_12(r)"""
    fig, ax = plt.subplots(figsize=(2.17, 2.25))
    plain_axes(ax)
    ax.set_xlim(-1.5, 11.0)
    ax.set_ylim(-3.2, 9.1)

    arrow_axis(ax, 0, 0, 0, 8.6)
    arrow_axis(ax, 0, 0, 10.7, 0)
    ax.text(-0.95, 8.0, r'$U_{12}$', fontsize=11, ha='center', va='center')
    ax.text(9.85, 0.55, r'$r$', fontsize=11, ha='center', va='center')

    from scipy.interpolate import PchipInterpolator
    # 单位：横轴 2r0 = 2.0，纵轴 U0 = 1.9（按原书页面测量）
    pts = [(0.52, 7.9), (0.78, 5.9), (1.05, 4.6), (1.35, 3.3), (1.62, 2.1),
           (1.85, 0.95), (2.0, 0.0), (3.0, -1.5), (4.35, -1.9), (5.5, -1.1),
           (7.0, -0.66), (8.5, -0.41), (10.0, -0.28)]
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    f = PchipInterpolator(xs, ys)
    xx = np.linspace(xs[0], xs[-1], 400)
    ax.plot(xx, f(xx), 'k-', lw=1.3)

    # 2r0 标注：横向双箭头 + 竖线
    ax.plot([2.0, 2.0], [0, -1.5], 'k-', lw=0.9)
    ax.annotate('', xy=(2.0, -0.9), xytext=(0.0, -0.9),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=0.9,
                                mutation_scale=9))
    ax.text(1.0, -2.1, r'$2r_0$', fontsize=9.5, ha='center', va='center')
    # U0 标注：纵向双箭头
    ax.annotate('', xy=(4.35, -1.9), xytext=(4.35, 0.0),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=0.9,
                                mutation_scale=9))
    ax.text(4.72, -0.75, r'$U_0$', fontsize=9.5, ha='left', va='center')
    save(fig, 11)


if __name__ == '__main__':
    for i in range(1, 12):
        globals()[f'fig_{i}']()
        print(f'fig{i} done')
