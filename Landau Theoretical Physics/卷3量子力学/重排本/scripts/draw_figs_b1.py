# -*- coding: utf-8 -*-
"""朗道《量子力学》（卷3）中文重排本 插图重绘 第一批：图1–图12。

每幅一个函数 fig_N()，与原书页面 PNG (原书转换/pages/p-0NN.png) 逐幅比对绘制。
输出：figures/figN.pdf（成品，覆盖占位图）+ figures/preview/figN.png（自检）。
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

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

LW = 1.2       # 主体线宽
LW_AUX = 0.8   # 辅助线宽
FS = 10        # 字号


def _new(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.axis('off')
    return fig, ax


def _save(fig, n):
    for ext, d in (('pdf', FIGDIR), ('png', PREVDIR)):
        fig.savefig(os.path.join(d, 'fig%d.%s' % (n, ext)),
                    bbox_inches='tight', pad_inches=0.03, dpi=220)
    plt.close(fig)


# ---------------------------------------------------------------- 图1 (p071)
def fig_1():
    """图1：有限深直角势阱 U=U0 (x<0), 0 (0<x<a), U0 (x>a)."""
    fig, ax = _new(2.4, 1.6)
    U0 = 1.0
    # 坐标轴
    ax.plot([0, 0], [0, 1.95], 'k-', lw=LW)                    # U(x) 轴
    ax.plot([-1.45, 1.95], [0, 0], 'k-', lw=LW)                # x 轴
    # 势阱
    ax.plot([-1.0, 0], [U0, U0], 'k-', lw=LW)                  # 左台 U0
    ax.plot([1.0, 1.0], [0, U0], 'k-', lw=LW)                  # 右壁 x=a
    ax.plot([1.0, 2.0], [U0, U0], 'k-', lw=LW)                 # 右台
    # 标注
    ax.text(-0.06, 1.9, r'$U(x)$', ha='right', va='center', fontsize=FS)
    ax.text(0.06, U0, r'$U_0$', ha='left', va='bottom', fontsize=FS)
    ax.text(1.0, -0.1, r'$a$', ha='center', va='top', fontsize=FS)
    ax.text(1.97, -0.1, r'$x$', ha='center', va='top', fontsize=FS)
    ax.set_xlim(-1.62, 2.12)
    ax.set_ylim(-0.42, 2.14)
    _save(fig, 1)


# ---------------------------------------------------------------- 图2 (p072)
def fig_2():
    """图2：两侧高度不同的直角势阱 U=U1 (x<0), 0, U2 (x>a), U2>U1（§22 习题2）."""
    fig, ax = _new(2.45, 1.75)
    U1, U2 = 0.55, 1.08
    # 坐标轴
    ax.plot([0, 0], [0, 1.53], 'k-', lw=LW)
    ax.plot([-0.85, 1.7], [0, 0], 'k-', lw=LW)
    # 势阱
    ax.plot([-0.87, 0], [U1, U1], 'k-', lw=LW)                 # 左台 U1
    ax.plot([1.0, 1.0], [0, U2], 'k-', lw=LW)                  # 右壁 x=a
    ax.plot([1.0, 1.7], [U2, U2], 'k-', lw=LW)                 # 右台 U2
    # 标注
    ax.text(-0.06, 1.5, r'$U(x)$', ha='right', va='center', fontsize=FS)
    ax.text(0.06, U1, r'$U_1$', ha='left', va='bottom', fontsize=FS)
    ax.text(0.94, U2, r'$U_2$', ha='right', va='bottom', fontsize=FS)
    ax.text(1.0, -0.08, r'$a$', ha='center', va='top', fontsize=FS)
    ax.text(1.62, -0.08, r'$x$', ha='center', va='top', fontsize=FS)
    ax.set_xlim(-1.02, 1.87)
    ax.set_ylim(-0.32, 1.74)
    _save(fig, 2)


# ---------------------------------------------------------------- 图3 (p079)
def fig_3():
    """图3：莫尔斯势 U=A(e^{-2ax}-2e^{-ax})（§22 习题4）."""
    fig, ax = _new(2.5, 1.5)
    # 曲线（真 Morse 形状，窗口与原书一致：左支止于 U=+0.74）
    Um = 0.74
    t = 1 + np.sqrt(1 + Um)                # e^{-x}=t 时 U=t^2-2t=Um 的左支根
    x_top = -np.log(t)
    x = np.linspace(x_top, 3.0, 601)
    ax.plot(x, np.exp(-2 * x) - 2 * np.exp(-x), 'k-', lw=LW)
    # 坐标轴：竖轴过极小值点 x=0，向下伸到 -A 标号处
    ax.plot([0, 0], [-1.3, 1.28], 'k-', lw=LW)
    ax.plot([-1.9, 2.8], [0, 0], 'k-', lw=LW)
    # 标注
    ax.text(0.07, 1.24, r'$U(x)$', ha='left', va='center', fontsize=FS)
    ax.text(-0.07, -1.22, r'$-A$', ha='right', va='center', fontsize=FS)
    ax.text(2.87, 0, r'$x$', ha='left', va='center', fontsize=FS)
    ax.set_xlim(-2.05, 3.05)
    ax.set_ylim(-1.44, 1.44)
    _save(fig, 3)


# ---------------------------------------------------------------- 图4 (p080)
def fig_4():
    """图4：势阱 U=-U0/cosh^2(ax)（§23 习题5）."""
    fig, ax = _new(2.9, 1.2)
    x = np.linspace(-2.55, 2.95, 601)
    ax.plot(x, -1.0 / np.cosh(x) ** 2, 'k-', lw=LW)
    # 坐标轴：竖轴顶端略高出零线一点
    ax.plot([0, 0], [-1.3, 0.24], 'k-', lw=LW)
    ax.plot([-2.55, 2.95], [0, 0], 'k-', lw=LW)
    # 标注
    ax.text(0.07, 0.24, r'$U(x)$', ha='left', va='bottom', fontsize=FS)
    ax.text(-0.08, -1.16, r'$-U_0$', ha='right', va='center', fontsize=FS)
    ax.text(3.02, 0.02, r'$x$', ha='left', va='bottom', fontsize=FS)
    ax.set_xlim(-2.72, 3.25)
    ax.set_ylim(-1.5, 0.62)
    _save(fig, 4)


# ---------------------------------------------------------------- 图5 (p083)
def fig_5():
    """图5：单调从 0 过渡到 U0 的势场（§25）."""
    fig, ax = _new(2.5, 1.9)
    x = np.linspace(-2.3, 2.55, 401)
    ax.plot(x, 1.0 / (1 + np.exp(-1.6 * x)), 'k-', lw=LW)      # S 形曲线
    ax.plot([0, 2.75], [1.0, 1.0], 'k--', lw=LW_AUX)           # U0 渐近虚线
    # 坐标轴
    ax.plot([0, 0], [0, 1.16], 'k-', lw=LW)
    ax.plot([-2.3, 2.95], [0, 0], 'k-', lw=LW)
    # 标注
    ax.text(0.07, 1.16, r'$U(x)$', ha='left', va='center', fontsize=FS)
    ax.text(-0.07, 1.0, r'$U_0$', ha='right', va='center', fontsize=FS)
    ax.text(3.0, 0, r'$x$', ha='left', va='center', fontsize=FS)
    ax.set_xlim(-2.48, 3.22)
    ax.set_ylim(-0.17, 1.38)
    _save(fig, 5)


# ---------------------------------------------------------------- 图6 (p085)
def fig_6():
    """图6：直角势壁 U=0 (x<0), U0 (x>0)（§25 习题1）."""
    fig, ax = _new(2.2, 1.42)
    U0 = 1.0
    ax.plot([0, 0], [0, 1.5], 'k-', lw=LW)
    ax.plot([-0.72, 2.08], [0, 0], 'k-', lw=LW)
    ax.plot([0, 1.4], [U0, U0], 'k-', lw=LW)                   # U0 台阶
    # 标注
    ax.text(0.07, 1.5, r'$U(x)$', ha='left', va='center', fontsize=FS)
    ax.text(-0.07, U0, r'$U_0$', ha='right', va='center', fontsize=FS)
    ax.text(2.15, 0, r'$x$', ha='left', va='center', fontsize=FS)
    ax.set_xlim(-0.9, 2.38)
    ax.set_ylim(-0.2, 1.7)
    _save(fig, 6)


# ---------------------------------------------------------------- 图7 (p085)
def fig_7():
    """图7：直角势垒 U=U0 (0<x<a)（§25 习题2）."""
    fig, ax = _new(2.25, 1.45)
    U0, a = 1.0, 1.0
    ax.plot([0, 0], [0, 1.52], 'k-', lw=LW)
    ax.plot([-0.55, 1.73], [0, 0], 'k-', lw=LW)
    ax.plot([0, a], [U0, U0], 'k-', lw=LW)                     # 垒顶
    ax.plot([a, a], [0, U0], 'k-', lw=LW)                      # 右壁 x=a
    # 标注
    ax.text(0.07, 1.52, r'$U(x)$', ha='left', va='center', fontsize=FS)
    ax.text(-0.07, U0, r'$U_0$', ha='right', va='center', fontsize=FS)
    ax.text(a + 0.03, -0.07, r'$a$', ha='left', va='top', fontsize=FS)
    ax.text(1.8, -0.02, r'$x$', ha='left', va='center', fontsize=FS)
    ax.set_xlim(-0.73, 2.02)
    ax.set_ylim(-0.3, 1.72)
    _save(fig, 7)


# ---------------------------------------------------------------- 图8 (p087)
def fig_8():
    """图8：势垒 U=U0/cosh^2(ax)（§25 习题4）."""
    fig, ax = _new(2.9, 1.35)
    x = np.linspace(-2.5, 3.0, 601)
    ax.plot(x, 1.0 / np.cosh(x) ** 2, 'k-', lw=LW)
    # 坐标轴
    ax.plot([0, 0], [0, 1.24], 'k-', lw=LW)
    ax.plot([-2.5, 3.0], [0, 0], 'k-', lw=LW)
    # 标注（原书 U0 在峰顶上方、竖轴左侧，U(x) 在竖轴右侧）
    ax.text(0.07, 1.26, r'$U(x)$', ha='left', va='center', fontsize=FS)
    ax.text(-0.07, 1.13, r'$U_0$', ha='right', va='center', fontsize=FS)
    ax.text(3.05, -0.04, r'$x$', ha='left', va='top', fontsize=FS)
    ax.set_xlim(-2.68, 3.32)
    ax.set_ylim(-0.18, 1.44)
    _save(fig, 8)


# ---------------------------------------------------------------- 图9 (p114)
def fig_9():
    """图9：±sin x=ax 的图解法：实线 sin x（cot x<0 相关瓣），虚线 -sin x（§33 习题1）."""
    fig, ax = _new(3.45, 1.2)
    pi = np.pi
    xs = np.linspace(0, pi, 241)
    xd = np.linspace(pi, 2 * pi, 241)
    x3 = np.linspace(2 * pi, 3 * pi, 241)
    ax.plot(xs, np.sin(xs), 'k-', lw=LW)                       # 第一正瓣（实线）
    ax.plot(x3, np.sin(x3), 'k-', lw=LW)                       # 第三正瓣（实线）
    ax.plot(xd, np.sin(xd), 'k--', lw=LW_AUX)                  # 负瓣（虚线）
    # 直线 Oa：y=(2/pi)x，止于第一瓣峰顶略上方
    xe = 1.1 * pi / 2
    ax.plot([0, xe], [0, 2 / pi * xe], 'k-', lw=LW)
    # 坐标轴
    ax.plot([0, 0], [-1.22, 1.3], 'k-', lw=LW)
    ax.plot([0, 3.3 * pi], [0, 0], 'k-', lw=LW)
    # 标注
    ax.text(-0.12, 1.28, r'$y$', ha='right', va='center', fontsize=FS)
    ax.text(3.36 * pi, 0, r'$x$', ha='left', va='center', fontsize=FS)
    ax.text(-0.09, -0.07, r'$O$', ha='right', va='top', fontsize=FS)
    ax.text(xe + 0.05, 2 / pi * xe + 0.04, r'$a$', ha='left', va='bottom', fontsize=FS)
    ax.text(2.4, 0.98, r'$\sin x$', ha='left', va='bottom', fontsize=FS)
    ax.text(1.5 * pi, -1.12, r'$-\sin x$', ha='center', va='top', fontsize=FS)
    ax.set_xlim(-0.88, 3.44 * pi)
    ax.set_ylim(-1.62, 1.62)
    ax.set_aspect('equal')
    _save(fig, 9)


# --------------------------------------------------------------- 图10 (p125)
def fig_10():
    """图10：xi 复平面上绕奇点 xi=0 与 xi=2ikr 的积分回路（§36）."""
    fig, ax = _new(2.6, 1.55)
    yb, yt, cx, R = -0.14, 1.14, 0.98, 0.64
    # 实轴与虚轴（细线）
    ax.plot([-1.15, 1.75], [0, 0], 'k-', lw=LW_AUX)
    ax.plot([0, 0], [-0.72, 1.66], 'k-', lw=LW_AUX)
    # 奇点
    ax.plot([0, 0], [0, 1.0], 'ko', ms=3.2)
    # 回路：下支（xi=0 下方）向右 → 右端半圆 → 上支（xi=2ikr 上方）向左
    ax.plot([-0.95, cx], [yb, yb], 'k-', lw=LW)
    th = np.linspace(-np.pi / 2, np.pi / 2, 121)
    ax.plot(cx + R * np.cos(th), 0.5 + R * np.sin(th), 'k-', lw=LW)
    ax.plot([cx, -0.95], [yt, yt], 'k-', lw=LW)
    # 方向箭头：下支向右、回路右端向上、上支向左
    arr = dict(arrowstyle='-|>', color='k', lw=LW)
    ax.annotate('', xy=(-0.05, yb), xytext=(-0.45, yb), arrowprops=arr)
    ax.annotate('', xy=(cx + R, 0.64), xytext=(cx + R, 0.36), arrowprops=arr)
    ax.annotate('', xy=(0.08, yt), xytext=(0.48, yt), arrowprops=arr)
    # 标注
    ax.text(0.07, 1.04, r'$\xi=2ikr$', ha='left', va='top', fontsize=FS)
    ax.text(0.07, 0.08, r'$\xi=0$', ha='left', va='bottom', fontsize=FS)
    ax.set_xlim(-1.38, 1.95)
    ax.set_ylim(-0.95, 1.9)
    ax.set_aspect('equal')
    _save(fig, 10)


# --------------------------------------------------------------- 图11 (p130)
def fig_11():
    """图11：势 U=A/r^2-B/r（§36 习题3）."""
    fig, ax = _new(2.1, 2.0)
    A, B = 0.25, 1.0
    Um = 1.47                              # 顶部截止值（与原书窗口一致）
    r0 = (-B + np.sqrt(B ** 2 + 4 * Um * A)) / (2 * Um)
    r = np.linspace(r0, 2.9, 801)
    ax.plot(r, A / r ** 2 - B / r, 'k-', lw=LW)
    # 坐标轴：竖轴向上超过曲线顶端、向下过极小值
    ax.plot([0, 0], [-1.47, 1.75], 'k-', lw=LW)
    ax.plot([0, 3.2], [0, 0], 'k-', lw=LW)                     # r 轴（零线）
    # 标注
    ax.text(0.06, 1.72, r'$U(r)$', ha='left', va='center', fontsize=FS)
    ax.text(3.27, 0, r'$r$', ha='left', va='center', fontsize=FS)
    ax.set_xlim(-0.28, 3.52)
    ax.set_ylim(-1.66, 1.96)
    _save(fig, 11)


# --------------------------------------------------------------- 图12 (p131)
def fig_12():
    """图12：势 U=A/r^2+B r^2（§36 习题4）."""
    fig, ax = _new(2.35, 1.85)
    A, B = 0.5, 0.5
    Um = 3.64                              # 顶部截止值
    r0 = (0.5 * (2 * Um - np.sqrt((2 * Um) ** 2 - 4))) ** 0.5   # 0.5/r^2+0.5r^2=Um 的小根
    r = np.linspace(r0, 2.6, 801)
    ax.plot(r, A / r ** 2 + B * r ** 2, 'k-', lw=LW)
    # 坐标轴：竖轴向下越过 r 轴一点，向上超过曲线顶端
    ax.plot([0, 0], [-0.55, 3.73], 'k-', lw=LW)
    ax.plot([0, 3.3], [0, 0], 'k-', lw=LW)                     # r 轴
    # 标注（原书 U(r) 在竖轴左侧）
    ax.text(-0.06, 3.6, r'$U(r)$', ha='right', va='center', fontsize=FS)
    ax.text(3.37, 0, r'$r$', ha='left', va='center', fontsize=FS)
    ax.set_xlim(-0.88, 3.6)
    ax.set_ylim(-0.74, 3.94)
    _save(fig, 12)


if __name__ == '__main__':
    for i in range(1, 13):
        globals()['fig_%d' % i]()
        print('fig %d done' % i)
