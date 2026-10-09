# -*- coding: utf-8 -*-
"""Redraw Chapter 6 figures (Carroll, _Spacetime and Geometry_) as black-white
textbook-style vector figures with matplotlib.

Outputs (key keeps the dot, e.g. fig_6.1):
    figures/fig_6.1.pdf .. figures/fig_6.9.pdf
    figures/preview/fig_6.1.png .. fig_6.9.png   (self-check)
"""
import os
from math import comb

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

BASE = r'E:\AI整理书籍\卡罗尔\重排本'
FIGD = os.path.join(BASE, 'figures')
PREV = os.path.join(FIGD, 'preview')
os.makedirs(PREV, exist_ok=True)


# ---------------------------------------------------------------- utilities
def _script_cmd():
    r"""mathtext has no \mathscr in older versions; fall back to \mathcal."""
    try:
        f = plt.figure()
        f.text(0.5, 0.5, r'$\mathscr{I}$')
        f.canvas.draw()
        plt.close(f)
        return 'mathscr'
    except Exception:
        plt.close('all')
        return 'mathcal'


SCR = '\\' + _script_cmd()


def sI(mark):
    r"""$\mathscr{I}^{\pm}$ (script I of the book)."""
    return '$' + SCR + '{I}^{' + mark + '}$'


def _save(fig, key):
    fig.savefig(os.path.join(FIGD, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, 'fig_%s.png' % key),
                bbox_inches='tight', pad_inches=0.03, dpi=150)
    plt.close(fig)


def _new_ax(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def _dots(ax, pts, ms=3.2, color='k', zorder=3):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    ax.plot(xs, ys, 'o', ms=ms, color=color, zorder=zorder)


def _wavy_v(ax, x, ya, yb, amp=0.05, lam=0.2, lw=1.1, color='k'):
    y = np.linspace(ya, yb, 900)
    ax.plot(x + amp * np.sin(2 * np.pi * (y - ya) / lam), y, color=color, lw=lw)


def _bez(ctrl, n=300):
    """de Casteljau / Bernstein evaluation of a Bezier arc."""
    P = np.array(ctrl, dtype=float)
    k = len(P) - 1
    t = np.linspace(0, 1, n)
    B = np.zeros((n, k + 1))
    for i in range(k + 1):
        B[:, i] = comb(k, i) * t ** i * (1 - t) ** (k - i)
    return B @ P


def _dashed(ax, pts, lw=0.9, color='k'):
    xy = _bez(pts)
    ax.plot(xy[:, 0], xy[:, 1], color=color, lw=lw, dashes=(4, 2.5))


def _arrow_head(ax, tip, tail, color='k', lw=1.0, scale=8):
    ax.annotate('', xy=tip, xytext=tail,
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw,
                                mutation_scale=scale, shrinkA=0, shrinkB=0))


# ------------------------------------------------------------------ fig 6.1
def fig_6_1():
    """Asymptotically flat spacetime: conformal diagram with I+/I-/i0,
    future/past event horizons, dashed rest-of-spacetime region."""
    fig, ax = _new_ax((3.6, 2.0))
    # dashed boundary of the rest of spacetime (half-ellipse through top
    # and bottom vertices of the diamond, bulging left)
    th = np.linspace(np.pi / 2, 3 * np.pi / 2, 500)
    ax.plot(2.05 * np.cos(th), 1.0 * np.sin(th), color='k', lw=1.0,
            dashes=(5, 3))
    # event horizons: two 45-deg lines crossing at the left vertex C=(-1,0)
    ax.plot([-1.38, 0.0], [-0.38, 1.0], color='k', lw=1.1)   # future EH
    ax.plot([-1.41, 0.0], [0.41, -1.0], color='k', lw=1.1)   # past EH
    # null infinity edges of the asymptotically flat diamond
    ax.plot([0, 2], [1, 0], color='k', lw=1.1)
    ax.plot([2, 0], [0, -1], color='k', lw=1.1)
    _dots(ax, [(2, 0)])
    ax.text(2.10, 0, r'$i^0$', fontsize=10, ha='left', va='center')
    ax.text(1.70, 0.64, sI('+'), fontsize=10, ha='left')
    ax.text(1.74, -0.74, sI('-'), fontsize=10, ha='left', va='top')
    ax.text(0.58, 0.50, 'future', fontsize=9.5, ha='left')
    ax.text(0.58, 0.28, 'event horizon', fontsize=9.5, ha='left')
    ax.text(0.58, -0.24, 'past', fontsize=9.5, ha='left')
    ax.text(0.58, -0.44, 'event horizon', fontsize=9.5, ha='left', va='top')
    ax.set_xlim(-2.25, 2.55)
    ax.set_ylim(-1.28, 1.28)
    _save(fig, '6.1')


# ------------------------------------------------------------------ fig 6.2
def fig_6_2():
    """Delta(r) for the Reissner-Nordstrom solutions."""
    fig, ax = plt.subplots(figsize=(3.5, 3.0))
    ax.axis('off')
    ax.set_aspect('auto')
    GM = 1.0

    def Delta(r, s):
        return 1 - 2 * GM / r + s / r ** 2

    r = np.linspace(0.15, 2.60, 900)
    ax.plot(r, Delta(r, 1.6), color='k', lw=1.3)   # (1) GM^2 < p^2+q^2
    ax.plot(r, Delta(r, 0.7), color='k', lw=1.3)   # (2) GM^2 > p^2+q^2
    ax.plot(r, Delta(r, 1.0), color='k', lw=1.3)   # (3) GM^2 = p^2+q^2
    rd = np.linspace(0.42, 2.60, 500)
    ax.plot(rd, Delta(rd, 0.0), color='k', lw=1.2, dashes=(5, 3))
    # axes with arrows
    ytop, ybot, xr = 2.30, -1.40, 3.05
    ax.plot([0, 0], [ybot, ytop], color='k', lw=1.0)
    ax.plot([0, xr], [0, 0], color='k', lw=1.0)
    _arrow_head(ax, (0, 2.42), (0, 2.30))
    _arrow_head(ax, (xr + 0.13, 0), (xr, 0))
    ax.text(0.13, 2.50, r'$\Delta(r)$', fontsize=10, ha='left', va='bottom')
    ax.text(xr + 0.20, 0.0, r'$r$', fontsize=10, ha='left', va='center')
    # x-axis ticks + labels
    for xt, lb in [(0.452, r'$r_-$'), (1.0, r'$GM$'),
                   (1.548, r'$r_+$'), (2.0, r'$2GM$')]:
        ax.plot([xt, xt], [-0.045, 0.045], color='k', lw=0.9)
        ax.text(xt, -0.14, lb, fontsize=10, ha='center', va='top')
    # curve labels with leader lines
    labels = [(0.78, 2.16, r'(1) $GM^2<p^2+q^2$', 0.62, 1.6),
              (0.78, 1.68, r'(2) $GM^2>p^2+q^2$', 0.33, 0.7),
              (0.78, 1.20, r'(3) $GM^2=p^2+q^2$', 0.45, 1.0)]
    for x0, y0, txt, rc, s in labels:
        ax.text(x0, y0, txt, fontsize=9.5, ha='left')
        ax.plot([x0 - 0.03, rc], [y0 - 0.04, Delta(rc, s)],
                color='k', lw=0.6)
    # Schwarzschild dashed-curve label
    ax.plot([1.47, 1.30], [-0.76, Delta(1.30, 0.0)], color='k', lw=0.6)
    ax.text(1.52, -0.80, r'$p=q=0$', fontsize=9.5, ha='left')
    ax.text(2.10, -1.16, '(Schwarzschild)', fontsize=9.5, ha='left')
    ax.set_xlim(-0.08, 3.35)
    ax.set_ylim(-1.42, 2.45)
    _save(fig, '6.2')


# ------------------------------------------------------------------ fig 6.3
def fig_6_3():
    """RN naked singularity (GM^2 < Q^2+P^2): right-half conformal diagram,
    vertical timelike singularity r=0, constant-t curves converging at i0."""
    fig, ax = _new_ax((2.9, 3.2))
    # singularity
    _wavy_v(ax, 0.0, -2.0, 2.0, amp=0.045, lam=0.15, lw=1.1)
    _dots(ax, [(0, 2), (0, -2), (2, 0)])
    # null infinity edges
    ax.plot([0, 2], [2, 0], color='k', lw=1.1)
    ax.plot([0, 2], [-2, 0], color='k', lw=1.1)
    # constant-t slices (exact conformal image), converging at i0
    r = np.linspace(0, 6000, 3000)
    for t0 in (0.0, 0.45, -0.45, 1.375, -1.375):
        T = np.arctan(t0 + r) + np.arctan(t0 - r)
        R = np.arctan(t0 + r) - np.arctan(t0 - r)
        ax.plot(2 * R / np.pi, 2 * T / np.pi, color='k', lw=0.9)
    ax.text(0.0, 2.14, r'$i^+$', fontsize=10, ha='center', va='bottom')
    ax.text(0.0, -2.14, r'$i^-$', fontsize=10, ha='center', va='top')
    ax.text(2.16, 0.0, r'$i^0$', fontsize=10, ha='left', va='center')
    ax.text(1.50, 0.92, sI('+'), fontsize=10, ha='center')
    ax.text(1.50, -0.92, sI('-'), fontsize=10, ha='center', va='top')
    ax.text(-0.14, 0.30, r'$r=0$', fontsize=10, ha='right')
    ax.text(-0.14, -0.18, '(singularity)', fontsize=9.5, ha='right')
    ax.set_xlim(-1.80, 2.65)
    ax.set_ylim(-2.45, 2.45)
    _save(fig, '6.3')


# ------------------------------------------------- chain lattice (fig 6.4/6.8)
def _chain(ax, kerr, lw=1.1):
    cols = (-1.0, 1.0)
    doty = (4, 2, 0, -2, -4, -6)
    # diagonal lattice between the columns
    for y0 in (4, 2, 0, -2, -4, -6):
        ax.plot([-1, 1], [y0, y0 - 2], color='k', lw=lw)
        ax.plot([1, -1], [y0, y0 - 2], color='k', lw=lw)
    # exterior universe triangles (I regions)
    for sx in cols:
        for y0 in (2, -2):
            ax.plot([sx, 2 * sx, sx], [y0, y0 - 1, y0 - 2], color='k', lw=lw)
    # verticals on the columns (wavy r=0 for RN, straight for Kerr)
    wavy = set() if kerr else {(2, 4), (-2, 0), (-6, -4)}
    for sx in cols:
        for seg in [(2, 4), (0, 2), (-2, 0), (-4, -2), (-6, -4)]:
            if seg in wavy:
                _wavy_v(ax, sx, seg[0], seg[1], amp=0.05, lam=0.2, lw=lw)
            else:
                ax.plot([sx, sx], seg, color='k', lw=lw)
    # Kerr: mirror squares across the straight r=0 lines
    if kerr:
        for sx in cols:
            for (ya, yb) in [(4, 2), (0, -2), (-6, -4)]:
                ym = (ya + yb) / 2.0
                ax.plot([sx, 2 * sx, sx], [ya, ym, yb], color='k', lw=lw)
    # dots
    pts = [(sx, y) for sx in cols for y in doty]
    pts += [(-2, 1), (2, 1), (-2, -3), (2, -3)]
    if kerr:
        pts += [(2 * sx, ym) for sx in cols
                for ym in (3.0, -1.0, -5.0)]
    _dots(ax, pts)
    # continuation stubs at top / bottom corner dots
    for sx in cols:
        # upward stubs: outward ray + inward ray (crossing above centre)
        ax.plot([sx, sx * 0.3], [4, 5.3], color='k', lw=lw)
        ax.plot([sx, sx * 1.9], [4, 4.9], color='k', lw=lw)
        if kerr:
            # outward downward continuation of the mirror-square edge
            ax.plot([sx, sx * 1.9], [4, 3.1], color='k', lw=lw)
        ax.plot([sx, sx * 0.3], [-6, -7.3], color='k', lw=lw)
        ax.plot([sx, sx * 1.9], [-6, -6.9], color='k', lw=lw)


def _chain_labels(ax, kerr, fs=9):
    # i +/-/0 labels
    for sx in (-1, 1):
        h = 'right' if sx < 0 else 'left'
        x = sx * 1.16
        for y, t in [(2, r'$i^+$'), (0, r'$i^-$'), (-2, r'$i^+$'),
                     (-4, r'$i^-$')]:
            ax.text(x, y, t, fontsize=fs, ha=h, va='center')
        for y in (1, -3):
            ax.text(sx * 2.16, y, r'$i^0$', fontsize=fs, ha=h, va='center')
    # script-I edge labels (Reissner-Nordstrom chain only)
    if not kerr:
        for x, h in ((-1.84, 'right'), (1.70, 'left')):
            ax.text(x, 1.52, sI('+'), fontsize=fs, ha=h)
            ax.text(x, 0.38, sI('-'), fontsize=fs, ha=h, va='top')
            ax.text(x, -2.42, sI('+'), fontsize=fs, ha=h)
            ax.text(x, -3.58, sI('-'), fontsize=fs, ha=h, va='top')
    # r+ / r- horizon labels
    for x, y, t in [(-0.44, 2.28, '-'), (0.40, 2.28, '-'),
                    (-0.43, -0.28, '-'), (0.43, -0.28, '-'),
                    (-0.40, 1.62, '+'), (0.40, 1.62, '+'),
                    (-0.65, 0.68, '+'), (0.55, 0.68, '+')]:
        ax.text(x, y, r'$r_%s$' % t, fontsize=fs, ha='center')


# ------------------------------------------------------------------ fig 6.4
def fig_6_4():
    """Reissner-Nordstrom GM^2 > p^2+q^2: infinite chain of universes."""
    fig, ax = _new_ax((3.6, 5.2))
    _chain(ax, kerr=False)
    _chain_labels(ax, kerr=False)

    # r = 0 labels (4 wavy singularity segments)
    ax.text(1.13, 2.95, r'$r=0$', fontsize=9, ha='left')
    ax.text(-1.13, -1.00, r'$r=0$', fontsize=9, ha='right', va='center')
    ax.text(-1.13, -5.00, r'$r=0$', fontsize=9, ha='right', va='center')
    ax.text(1.13, -5.00, r'$r=0$', fontsize=9, ha='left', va='center')
    # extra r+/- labels of the lower cells
    for x, y, t in [(-0.52, -1.12, '-'), (0.52, -1.12, '+'),
                    (-0.33, -2.62, '+'), (0.35, -2.62, '+'),
                    (-0.45, -3.62, '+'), (0.40, -3.62, '+')]:
        ax.text(x, y, r'$r_%s$' % t, fontsize=9, ha='center')
    # name of the solution
    ax.text(-4.80, 3.55, 'Reissner\u2013Nordstrom:', fontsize=9, ha='left')
    ax.text(-4.80, 3.20, '$GM^2>p^2+q^2$', fontsize=9, ha='left')

    # dashed r = constant surfaces
    _dashed(ax, [(-1, 0), (-0.55, -1), (-1, -2)])       # region III, left
    _dashed(ax, [(1, 0), (0.56, -1), (1, -2)])          # region III, right
    _dashed(ax, [(-1, -2), (0, -1.25), (1, -2)])        # dome
    ax.plot([-1, 1], [-2, -2], color='k', lw=0.9, dashes=(4, 2.5))
    _dashed(ax, [(-1, -2), (-1.66, -3), (-1, -4)])      # lens, left arc
    _dashed(ax, [(-1, -2), (-0.34, -3), (-1, -4)])      # lens, right arc
    ax.plot([-1, -1], [-2, -4], color='k', lw=0.9, dashes=(4, 2.5))

    # timelike trajectories (grey wiggly worldlines with arrows)
    g, lg = '0.55', '0.5'
    t1 = _bez([(0.62, -3.2), (0.28, -2.4), (0.52, -1.7), (0.30, -1.0),
               (0.55, -0.3), (0.33, 0.4), (0.58, 1.05)])
    ax.plot(t1[:, 0], t1[:, 1], color=g, lw=1.1)
    _arrow_head(ax, (0.58, 1.20), (0.57, 0.98), color=g, lw=0.9)
    t2 = _bez([(0.85, -3.2), (0.66, -2.6), (0.90, -2.0), (0.70, -1.45),
               (0.94, -0.95)])
    ax.plot(t2[:, 0], t2[:, 1], color=g, lw=1.1)
    _arrow_head(ax, (0.96, -0.80), (0.93, -1.02), color=g, lw=0.9)
    ax.plot([1.98, 0.50], [-1.06, -0.55], color=lg, lw=0.6)
    ax.plot([1.98, 0.90], [-1.40, -0.88], color=lg, lw=0.6)
    ax.text(2.04, -1.06, 'timelike', fontsize=9, ha='left', va='center')
    ax.text(2.04, -1.40, 'trajectories', fontsize=9, ha='left', va='center')
    # r = constant surfaces label
    ax.plot([-2.72, -1.45], [-2.25, -2.87], color=lg, lw=0.6)
    ax.text(-4.50, -2.02, '$r=$ constant', fontsize=9, ha='left')
    ax.text(-4.50, -2.36, 'surfaces', fontsize=9, ha='left')

    ax.set_xlim(-5.05, 4.15)
    ax.set_ylim(-7.55, 5.65)
    _save(fig, '6.4')


# ------------------------------------------------------------------ fig 6.5
def fig_6_5():
    """Extremal RN (GM^2 = Q^2+P^2): diamonds strung along r = 0."""
    fig, ax = _new_ax((2.3, 3.7))
    lw = 1.1
    # singularity
    _wavy_v(ax, 0.0, -2.69, 2.70, amp=0.07, lam=0.26, lw=lw)
    # diamond k: L(0,2k), Xt(1,2k+1), R(2,2k), Xb(1,2k-1)
    # D0 (truncated at top)
    ax.plot([0, 0.5], [2, 2.5], color='k', lw=lw)
    ax.plot([1.5, 2], [2.5, 2], color='k', lw=lw)
    ax.plot([2, 1], [2, 1], color='k', lw=lw)
    ax.plot([1, 0], [1, 2], color='k', lw=lw)
    # D1 (complete; thick upper-left edge)
    ax.plot([0, 1], [0, 1], color='k', lw=2.2)
    ax.plot([1, 2], [1, 0], color='k', lw=lw)
    ax.plot([2, 1], [0, -1], color='k', lw=lw)
    ax.plot([1, 0], [-1, 0], color='k', lw=lw)
    # D2 (complete down to its lower corners, cut at y = -2.85)
    ax.plot([0, 1], [-2, -1], color='k', lw=lw)
    ax.plot([1, 2], [-1, -2], color='k', lw=lw)
    ax.plot([2, 1.25], [-2, -2.75], color='k', lw=lw)
    ax.plot([0, 0.75], [-2, -2.75], color='k', lw=lw)
    _dots(ax, [(0, 2), (0, 0), (2, 2), (2, 0), (2, -2)])
    # dashed r = constant surfaces
    _dashed(ax, [(0, 2), (0.68, 1), (0, 0)])
    _dashed(ax, [(1, 1), (0.32, 0), (1, -1)])
    _dashed(ax, [(1, 1), (1.36, 0), (1, -1)])
    ax.plot([1, 1], [1, -1], color='k', lw=0.9, dashes=(4, 2.5))
    # labels
    ax.text(-0.13, 1.05, r'$r=0$', fontsize=9.5, ha='right')
    ax.text(2.12, 2.0, r'$i^0$', fontsize=9.5, ha='left', va='center')
    ax.text(2.12, 0.0, r'$i^0$', fontsize=9.5, ha='left', va='center')
    ax.text(2.12, -2.0, r'$i^0$', fontsize=9.5, ha='left', va='center')
    ax.text(1.72, 1.22, sI('-'), fontsize=9.5, ha='center', va='top')
    ax.text(1.72, 0.60, sI('+'), fontsize=9.5, ha='center')
    ax.text(1.70, -0.55, sI('-'), fontsize=9.5, ha='center', va='top')
    ax.text(1.66, -1.38, sI('+'), fontsize=9.5, ha='center')
    ax.text(1.33, 1.53, r'$r=\infty$', fontsize=9, ha='center', rotation=45)
    ax.text(1.38, -1.64, r'$r=\infty$', fontsize=9, ha='center', rotation=-45)
    ax.text(0.40, -0.70, r'$r=GM$', fontsize=9, ha='center', rotation=-45)
    ax.text(0.58, -1.67, r'$r=GM$', fontsize=9, ha='center', rotation=45)
    ax.set_xlim(-0.75, 2.75)
    ax.set_ylim(-2.85, 2.85)
    _save(fig, '6.5')


# ------------------------------------------------------------------ fig 6.6
def fig_6_6():
    """Ellipsoidal coordinates (r, theta) of flat space (Kerr a->0 limit)."""
    fig, ax = _new_ax((3.5, 2.3))
    # r = constant ellipses (schematic proportions as in the book)
    for a, b in [(1.55, 1.03), (1.36, 0.81), (1.16, 0.60), (0.97, 0.35)]:
        th = np.linspace(0, 2 * np.pi, 400)
        ax.plot(a * np.cos(th), b * np.sin(th), color='k', lw=1.1)
    # theta = constant hyperbola branches: x^2/sin^2 - z^2/cos^2 = a^2
    # each branch is clipped where it exits an oval ~30% beyond the outer
    # ellipse, as in the book
    A2, B2 = 2.0, 1.34
    for deg in (18, 36, 54, 72):
        t = np.radians(deg)
        s, c = np.sin(t), np.cos(t)
        x = np.linspace(s, 2.6, 2000)
        z = c * np.sqrt((x / s) ** 2 - 1.0)
        inside = (x / A2) ** 2 + (z / B2) ** 2 <= 1.0
        stop = np.argmax(~inside)
        if not inside[-1]:
            x, z = x[:stop], z[:stop]
        for sgn in (1, -1):
            ax.plot(sgn * x, z, color='k', lw=1.1)
            ax.plot(sgn * x, -z, color='k', lw=1.1)
    # axis lines (theta = 0 and theta = pi/2)
    ax.plot([0, 0], [-1.72, 1.72], color='k', lw=1.1)
    ax.plot([-2.05, 2.05], [0, 0], color='k', lw=1.1)
    # r = 0 : the disk seen edge-on (thick segment between the foci)
    ax.plot([-1, 1], [0, 0], color='k', lw=2.0, zorder=3)
    _dots(ax, [(-1, 0), (1, 0)], ms=3.5, zorder=4)
    # labels with leaders
    g = '0.5'
    ax.text(-2.77, 1.38, r'$\theta=$ constant', fontsize=9.5, ha='left')
    ax.plot([-1.12, -1.27], [1.32, 1.06], color=g, lw=0.6)
    ax.plot([-1.25, -1.02], [1.26, 1.14], color=g, lw=0.6)
    ax.text(1.80, 1.38, r'$r=$ constant', fontsize=9.5, ha='left')
    ax.plot([1.78, 1.00], [1.34, 0.79], color=g, lw=0.6)
    ax.plot([1.86, 1.35], [1.28, 0.55], color=g, lw=0.6)
    ax.text(-1.28, -1.44, r'$r=0$', fontsize=9.5, ha='right')
    ax.plot([-1.24, -0.75], [-1.36, -0.03], color=g, lw=0.6)
    # a = ring-radius dimension line
    ax.plot([1, 1], [0, -1.63], color=g, lw=0.7)
    ax.annotate('', xy=(1, -1.63), xytext=(0, -1.63),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=0.8,
                                mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text(0.5, -1.47, '$a$', fontsize=10, ha='center')
    ax.set_xlim(-2.95, 3.05)
    ax.set_ylim(-2.05, 1.75)
    _save(fig, '6.6')


# ------------------------------------------------------------------ fig 6.7
def fig_6_7():
    """Kerr horizon structure (side view): stationary limit surface,
    outer/inner event horizons, ergosphere shading, r=0 ring edge-on."""
    fig, ax = _new_ax((3.4, 1.6))
    a_s, b_s = 1.0, 0.47          # stationary limit surface
    a_p, b_p = 0.66, 0.47         # outer event horizon (tangent at poles)
    a_m, b_m = 0.36, 0.26         # inner event horizon
    th = np.linspace(0, 2 * np.pi, 500)
    ax.fill(a_s * np.cos(th), b_s * np.sin(th), color='0.87', zorder=0)
    ax.fill(a_p * np.cos(th), b_p * np.sin(th), color='white', zorder=1)
    for a, b in [(a_s, b_s), (a_p, b_p), (a_m, b_m)]:
        ax.plot(a * np.cos(th), b * np.sin(th), color='k', lw=1.2, zorder=2)
    ax.plot([-0.22, 0.22], [0, 0], color='k', lw=2.0, zorder=3)
    _dots(ax, [(-0.22, 0), (0.22, 0)], ms=3, zorder=4)
    # labels
    g = '0.4'
    ax.text(-1.60, 0.90, 'inner event horizon', fontsize=8.5, ha='left')
    ax.plot([-0.50, -0.29], [0.86, 0.15], color=g, lw=0.6)
    ax.text(-1.60, 0.72, 'outer event horizon', fontsize=8.5, ha='left')
    ax.plot([-0.52, -0.598], [0.70, 0.20], color=g, lw=0.6)
    ax.text(-1.60, 0.50, 'ergosphere', fontsize=8.5, ha='left')
    ax.plot([-0.98, -0.85], [0.47, 0.07], color=g, lw=0.6)
    ax.text(0.74, 0.88, 'stationary limit surface', fontsize=8.5, ha='left')
    ax.plot([0.68, 0.55], [0.86, 0.41], color=g, lw=0.6)
    ax.text(-0.44, 0.22, r'$r_+$', fontsize=9.5, ha='center')
    ax.text(-0.10, 0.15, r'$r_-$', fontsize=9.5, ha='center')
    ax.plot([-0.17, -0.16], [-0.09, -0.005], color=g, lw=0.6)
    ax.text(-0.08, -0.16, r'$r=0$', fontsize=9.5, ha='center', va='top')
    ax.set_xlim(-1.65, 1.98)
    ax.set_ylim(-0.56, 1.03)
    _save(fig, '6.7')


# ------------------------------------------------------------------ fig 6.8
def fig_6_8():
    """Kerr G^2M^2 > a^2: chain like RN but r=0 lines are passable."""
    fig, ax = _new_ax((3.6, 4.8))
    _chain(ax, kerr=True)
    _chain_labels(ax, kerr=True)

    # Kerr caption (two stacked lines, cf. fig_6_4)
    ax.text(-4.95, 3.55, 'Kerr:', fontsize=9, ha='left')
    ax.text(-4.95, 3.20, '$G^2M^2>a^2$', fontsize=9, ha='left')
    # r = 0 labels (rotated, along the straight singularity lines)
    for x, y in [(0.80, 3.0), (-1.22, -1.0), (-1.28, -5.0), (0.80, -5.0)]:
        ax.text(x, y, r'$r=0$', fontsize=9, ha='center', va='center',
                rotation=90)
    # script-I labels with (r = +-inf) / (t = +-inf) annotations
    ann = [(1.72, sI('+'), r'($r=+\infty$)'),
           (0.35, sI('-'), r'($r=+\infty$)'),
           (-0.28, sI('+'), r'($r=-\infty$)'),
           (-1.68, sI('-'), r'($r=-\infty$)'),
           (-2.28, sI('+'), r'($r=+\infty$)'),
           (-3.70, sI('-'), r'($r=+\infty$)')]
    for sx in (-1, 1):
        h = 'right' if sx < 0 else 'left'
        for y, lab, an in ann:
            txt = lab + ' ' + an
            if sx > 0 and abs(y - 1.72) < 0.01:
                txt = lab + ' ' + r'($t=+\infty$)'
            ax.text(sx * 1.62, y, txt, fontsize=8, ha=h, va='center')
    # extra r+/- labels specific to the Kerr chain
    for x, y, t in [(-0.47, -1.60, '-'), (0.47, -1.60, '-'),
                    (-0.47, -2.75, '+'), (0.55, -2.75, '+'),
                    (-0.47, -3.80, '+'), (0.55, -3.80, '+'),
                    (-0.68, 0.57, '+'), (0.68, 0.57, '+')]:
        ax.text(x, y, r'$r_%s$' % t, fontsize=9, ha='center')

    # dashed r = constant surfaces
    _dashed(ax, [(-1, 0), (-0.62, -1), (-1, -2)])
    _dashed(ax, [(-1, -2), (0, -1.22), (1, -2)])
    ax.plot([-1, 1], [-2, -2], color='k', lw=0.9, dashes=(4, 2.5))
    _dashed(ax, [(-1, -2), (-1.66, -3), (-1, -4)])
    _dashed(ax, [(-1, -2), (-0.34, -3), (-1, -4)])
    ax.plot([-1, -1], [-2, -4], color='k', lw=0.9, dashes=(4, 2.5))

    # timelike trajectories crossing the r = 0 lines
    g, lg = '0.55', '0.5'
    t1 = _bez([(0.55, -3.3), (0.30, -2.7), (0.55, -2.1), (0.35, -1.5),
               (0.58, -1.15)])
    ax.plot(t1[:, 0], t1[:, 1], color=g, lw=1.1)
    _arrow_head(ax, (0.59, -1.05), (0.57, -1.25), color=g, lw=0.9)
    t2 = _bez([(1.30, -3.0), (1.52, -2.5), (1.25, -2.0), (1.45, -1.60),
               (1.40, -1.40)])
    ax.plot(t2[:, 0], t2[:, 1], color=g, lw=1.1)
    _arrow_head(ax, (1.41, -1.30), (1.43, -1.50), color=g, lw=0.9)
    ax.plot([2.32, 0.58], [-1.28, -1.45], color=lg, lw=0.6)
    ax.plot([2.32, 1.40], [-1.22, -1.55], color=lg, lw=0.6)
    ax.text(2.38, -1.25, 'timelike trajectories', fontsize=8, ha='left',
            va='center')

    ax.set_xlim(-5.15, 4.95)
    ax.set_ylim(-7.55, 5.65)
    _save(fig, '6.8')


# ------------------------------------------------------------------ fig 6.9
def fig_6_9():
    """Penrose process (top view): split inside the ergosphere."""
    fig, ax = _new_ax((3.4, 2.4))
    th = np.linspace(0, 2 * np.pi, 500)
    ax.fill(np.cos(th), np.sin(th), color='0.87', zorder=0)
    ax.fill(0.36 * np.cos(th), 0.36 * np.sin(th), color='white', zorder=1)
    ax.plot(np.cos(th), np.sin(th), color='k', lw=1.2, zorder=2)
    ax.plot(0.36 * np.cos(th), 0.36 * np.sin(th), color='k', lw=1.2,
            zorder=2)
    # trajectories
    p0 = _bez([(-1.78, -1.07), (-1.30, -1.28), (-0.65, -1.18),
               (-0.15, -1.00), (0.12, -0.94)])
    ax.plot(p0[:, 0], p0[:, 1], color='k', lw=1.1, zorder=3)
    _arrow_head(ax, (-0.70, -1.13), (-0.85, -1.10), lw=0.9)
    p2 = _bez([(0.12, -0.94), (0.03, -0.75), (-0.05, -0.58)])
    ax.plot(p2[:, 0], p2[:, 1], color='k', lw=1.1, zorder=3)
    _arrow_head(ax, (-0.06, -0.55), (-0.03, -0.68), lw=0.9)
    p1 = _bez([(0.12, -0.94), (0.45, -1.13), (0.80, -1.10), (1.30, -0.97)])
    ax.plot(p1[:, 0], p1[:, 1], color='k', lw=1.1, zorder=3)
    _arrow_head(ax, (1.07, -1.00), (0.94, -1.05), lw=0.9)
    # split point (asterisk)
    xs, ys = 0.12, -0.94
    for a in np.radians((90, 30, 150)):
        ax.plot([xs - 0.07 * np.cos(a), xs + 0.07 * np.cos(a)],
                [ys - 0.07 * np.sin(a), ys + 0.07 * np.sin(a)],
                color='k', lw=0.9, zorder=4)
    # labels
    ax.text(0.14, 1.68, '(top view)', fontsize=9, ha='center')
    ax.text(1.18, 1.36, 'stationary limit surface', fontsize=9, ha='left')
    ax.plot([1.14, 0.60], [1.30, 0.82], color='0.5', lw=0.6)
    ax.text(-0.42, 0.87, 'ergosphere', fontsize=9, ha='center')
    ax.text(-1.62, -1.32, r'$p^{(0)\mu}$', fontsize=9.5, ha='center')
    ax.text(0.26, -0.78, r'$p^{(2)\mu}$', fontsize=9.5, ha='left')
    ax.text(1.24, -1.22, r'$p^{(1)\mu}$', fontsize=9.5, ha='center')
    ax.set_xlim(-2.05, 2.75)
    ax.set_ylim(-1.50, 1.92)
    _save(fig, '6.9')


# ---------------------------------------------------------------------- run
if __name__ == '__main__':
    for key, fn in [('6.1', fig_6_1), ('6.2', fig_6_2), ('6.3', fig_6_3),
                    ('6.4', fig_6_4), ('6.5', fig_6_5), ('6.6', fig_6_6),
                    ('6.7', fig_6_7), ('6.8', fig_6_8), ('6.9', fig_6_9)]:
        fn()
        print('fig_%s done' % key)
    print('script-I command used:', SCR)
