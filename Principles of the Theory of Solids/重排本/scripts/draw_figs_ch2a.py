# -*- coding: utf-8 -*-
"""
Redraw Ziman, Principles of the Theory of Solids (2nd ed.), Chapter 2,
Figs. 16-25 (lattice waves / lattice specific heat).
Black-and-white textbook-style vector figures.

Sources (scan pages, PDF page = book page + 14):
    Fig. 16  p045 (p.31)    Fig. 21  p050 (p.36)
    Fig. 17  p047 (p.33)    Fig. 22  p051 (p.37)
    Fig. 18  p047 (p.33)    Fig. 23  p052 (p.38)
    Fig. 19  p048 (p.34)    Fig. 24  p059 (p.45)
    Fig. 20  p049 (p.35)    Fig. 25  p060 (p.46)

Outputs (written immediately after each figure is drawn):
    figures/fig_{n}.pdf
    figures/preview/fig_{n}.png
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from scipy.interpolate import PchipInterpolator

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE, 'figures')
PREV_DIR = os.path.join(FIG_DIR, 'preview')
os.makedirs(PREV_DIR, exist_ok=True)

DASH = (0, (4, 2.5))


def save(fig, key):
    """Save one figure to PDF + preview PNG immediately."""
    fig.savefig(os.path.join(FIG_DIR, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV_DIR, 'fig_%s.png' % key),
                bbox_inches='tight', pad_inches=0.03, dpi=200)
    plt.close(fig)
    print('saved fig_%s' % key)


def arrow(ax, p0, p1, lw=1.3, ms=11, style='-|>'):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def dim(ax, p0, p1, lw=0.9, ms=8):
    """Double-headed dimension arrow."""
    arrow(ax, p0, p1, lw=lw, ms=ms, style='<|-|>')


def spring(ax, x0, x1, y0=0.0, n=None, amp=0.085, lw=1.1):
    """Zig-zag spring from x0 to x1 at height y0."""
    if n is None:                      # adapt coil count to length
        n = max(6, int(round(abs(x1 - x0) / 0.16)))
    xs = np.linspace(x0, x1, 2 * n + 1)
    ys = y0 + amp * np.where(np.arange(2 * n + 1) % 2 == 1, 1.0, -1.0)
    ys[0] = ys[-1] = y0
    ax.plot(xs, ys, 'k-', lw=lw)


def atom(ax, x, y, r, disp_dx, hatch=True, r_h=None):
    """Atom = dashed equilibrium circle + displaced (hatched) circle."""
    r_h = r if r_h is None else r_h
    ax.add_patch(Circle((x, y), r, fc='none', ec='k', lw=0.9,
                        ls=DASH, zorder=4))
    ax.add_patch(Circle((x + disp_dx, y), r_h, fc='white', ec='k', lw=1.2,
                        hatch='///' if hatch else None, zorder=5))


def lens(ax, xm, ym, L, h, horiz=True, lw=1.0):
    """Almond/lens pair with tips on the line through (xm, ym)."""
    t = np.linspace(-L / 2.0, L / 2.0, 80)
    prof = h * (1.0 - (2.0 * t / L) ** 2)
    for sgn in (1.0, -1.0):
        if horiz:
            ax.plot(xm + t, ym + sgn * prof, 'k-', lw=lw)
        else:
            ax.plot(xm + sgn * prof, ym + t, 'k-', lw=lw)


def hyper_arc(ax, xm, ym, A, B, Um, diag=1, lw=0.9):
    """Branch pair of a hyperbola at a diagonal saddle point.

    diag=+1: arms along the (1,1) direction; diag=-1: along (1,-1).
    """
    u = np.linspace(-Um, Um, 120)
    if diag > 0:
        w = A * np.sqrt(1.0 + (u / B) ** 2)
        for sgn in (1.0, -1.0):
            xs = xm + (u + sgn * w) / np.sqrt(2.0)
            ys = ym + (u - sgn * w) / np.sqrt(2.0)
            ax.plot(xs, ys, 'k-', lw=lw)
    else:
        w = A * np.sqrt(1.0 + (u / B) ** 2)
        for sgn in (1.0, -1.0):
            xs = xm + (u + sgn * w) / np.sqrt(2.0)
            ys = ym + (-u + sgn * w) / np.sqrt(2.0)
            ax.plot(xs, ys, 'k-', lw=lw)


def rosette(ax, cx, cy, r0, e, lw=1.0, n=361):
    """Closed curve r(th) = r0 (1 - e cos 4th): corners on the diagonals
    (flat sides facing the axes) when e > 0; circle when e = 0."""
    th = np.linspace(0.0, 2.0 * np.pi, n)
    r = r0 * (1.0 - e * np.cos(4.0 * th))
    ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), 'k-', lw=lw)


def diamond(ax, cx, cy, r0, e, lw=1.0, n=361):
    """Closed curve r(th) = r0 (1 + e cos 4th): corners on the axes."""
    th = np.linspace(0.0, 2.0 * np.pi, n)
    r = r0 * (1.0 + e * np.cos(4.0 * th))
    ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), 'k-', lw=lw)


# ======================================================================
# Fig. 16  Vibration frequencies of a linear chain  (p.31)
#   (a) chain of atoms on springs, dashed = equilibrium positions
#   (b) nu_q vs q, with the straight line nu = q a sqrt(a/M)
# ======================================================================
def fig_16():
    fig, (axa, axb) = plt.subplots(
        2, 1, figsize=(3.6, 4.7),
        gridspec_kw=dict(height_ratios=[1.0, 1.75]))

    # ---------------- panel (a): the chain ----------------
    a = 2.0                     # lattice spacing of equilibrium sites
    xs = np.array([0.0, a, 2 * a, 3 * a])       # equilibrium positions
    u = np.array([0.30, -0.28, 0.30, 0.55])     # displacements
    r = 0.42

    axa.plot([-1.05, 3 * a + 1.0], [0, 0], 'k-', lw=1.0, zorder=1)
    for k in range(3):          # springs between displaced atoms
        spring(axa, xs[k] + u[k] + r, xs[k + 1] + u[k + 1] - r)
    for k in range(4):
        atom(axa, xs[k], 0.0, r, u[k])
    # spring labels alpha (above the middle of each spring)
    for k in range(3):
        xm = 0.5 * ((xs[k] + u[k] + r) + (xs[k + 1] + u[k + 1] - r))
        axa.text(xm, 0.33, r'$\alpha$', fontsize=12, ha='center')

    # top dimension line: a, a between equilibrium sites
    for x in xs[:3]:
        axa.plot([x, x], [0.50, 0.97], 'k-', lw=0.9)
    dim(axa, (0, 0.78), (a, 0.78))
    dim(axa, (a, 0.78), (2 * a, 0.78))
    axa.text(1.0, 0.90, r'$a$', fontsize=12, ha='center')
    axa.text(3.0, 0.90, r'$a$', fontsize=12, ha='center')

    # displacement dimensions u1 u2 u3
    for k in range(3):
        x0, x1 = sorted((xs[k], xs[k] + u[k]))
        axa.plot([xs[k], xs[k]], [-0.50, -0.74], 'k-', lw=0.9)
        axa.plot([xs[k] + u[k], xs[k] + u[k]], [-0.50, -0.74], 'k-', lw=0.9)
        dim(axa, (x0, -0.65), (x1, -0.65))
        axa.text(x0 - 0.06, -1.06, r'$u_%d$' % (k + 1), fontsize=12)
    axa.text(3.0, -1.62, r'$(a)$', fontsize=12, ha='center')
    axa.set_xlim(-1.15, 7.1)
    axa.set_ylim(-1.85, 1.15)
    axa.set_aspect('equal')
    axa.axis('off')

    # ---------------- panel (b): the dispersion ----------------
    q = 2.0                     # pi/a in data units
    xb = np.linspace(-q, q, 401)
    nu = 2.0 * np.abs(np.sin(np.pi * xb / (2.0 * q)))
    xb2 = np.linspace(-2.7, 2.7, 200)
    nu2 = 2.0 * np.abs(np.sin(np.pi * xb2 / (2.0 * q)))
    sl = np.pi / 2.0                            # tangent slope at q = 0

    axb.plot([-2.75, 2.75], [0, 0], 'k-', lw=1.1)
    arrow(axb, (0, 0.0), (0, 3.05), lw=1.1)
    axb.plot([-q, -q], [0, 2.0], 'k-', lw=0.9)
    axb.plot([q, q], [0, 2.0], 'k-', lw=0.9)
    axb.plot(xb2[nu2 <= 2.0], nu2[nu2 <= 2.0], 'k-', lw=1.3)   # in zone
    out = nu2 > 2.0
    axb.plot(xb2[out], nu2[out], 'k--', lw=1.2)                # outside
    xd = np.array([0.0, 1.50])
    axb.plot(xd, sl * xd, 'k--', lw=1.2)                       # nu = q a sqrt(a/M)
    axb.text(0.10, 2.90, r'$\nu_q$', fontsize=12)
    axb.text(-q, -0.34, r'$-\pi/a$', ha='center')
    axb.text(0.0, -0.34, r'$O$', ha='center')
    axb.text(q, -0.34, r'$\pi/a$', ha='center')
    arrow(axb, (0.35, -0.62), (0.95, -0.62), lw=1.0, ms=9)
    axb.text(0.62, -0.92, r'$q$', ha='center', fontsize=12)
    axb.text(0, -1.45, r'$(b)$', ha='center', fontsize=12)
    # rotated label on the dashed straight line
    axb.text(0.54, 1.31, r'$\nu = qa\sqrt{a/M}$', fontsize=11,
             rotation=57, rotation_mode='anchor', ha='center')
    axb.set_xlim(-2.85, 2.85)
    axb.set_ylim(-1.65, 3.25)
    axb.set_aspect('equal')
    axb.axis('off')
    save(fig, 16)


# ======================================================================
# Fig. 17  Diatomic linear chain  (p.33)
# ======================================================================
def fig_17():
    fig, ax = plt.subplots(figsize=(4.8, 2.15))
    cell = 2.4                  # cell length = 2a, a = 1.2
    r1, r2 = 0.26, 0.16         # radii of M1 (heavy) and M2 (light)
    y0 = 0.0

    spring(ax, -0.55, 7.85, n=None, amp=0.085, lw=1.0)         # one long chain

    # dashed cell boxes
    for i in range(4):
        ax.plot([0.1 + i * cell, 0.1 + i * cell], [-1.02, 1.02],
                'k-', lw=0.9, ls=DASH)
    ax.plot([0.1, 7.3], [1.02, 1.02], 'k-', lw=0.9, ls=DASH)
    ax.plot([0.1, 7.3], [-1.02, -1.02], 'k-', lw=0.9, ls=DASH)

    # displacements of the three cells (dashed = equilibrium)
    du1 = [0.22, -0.18, 0.20]       # M1 of cells 1..3
    du2 = [-0.10, -0.15, 0.12]      # M2 of cells 1..3
    for i in range(3):
        x1 = 0.1 + i * cell + 0.6   # equilibrium site of M1
        x2 = 0.1 + i * cell + 1.8   # equilibrium site of M2
        # M1
        ax.add_patch(Circle((x1, y0), r1, fc='none', ec='k', lw=0.9,
                            ls=DASH, zorder=4))
        ax.add_patch(Circle((x1 + du1[i], y0), r1, fc='white', ec='k',
                            lw=1.2, hatch='///', zorder=5))
        # M2
        ax.add_patch(Circle((x2, y0), r2, fc='none', ec='k', lw=0.9,
                            ls=DASH, zorder=4))
        ax.add_patch(Circle((x2 + du2[i], y0), r2, fc='white', ec='k',
                            lw=1.2, hatch='///', zorder=5))

    # top dimension: a and a between equilibrium sites of cell 1
    for x in (0.7, 1.9, 3.1):
        ax.plot([x, x], [0.42, 0.92], 'k-', lw=0.9)
    dim(ax, (0.7, 0.74), (1.9, 0.74))
    dim(ax, (1.9, 0.74), (3.1, 0.74))
    ax.text(1.3, 0.86, r'$a$', fontsize=12, ha='center')
    ax.text(2.5, 0.86, r'$a$', fontsize=12, ha='center')

    # U1, U2 displacement arrows of cell 1
    ax.plot([0.7, 0.7], [-0.34, -0.58], 'k-', lw=0.9)
    ax.plot([0.92, 0.92], [-0.34, -0.58], 'k-', lw=0.9)
    arrow(ax, (0.7, -0.49), (0.92, -0.49), lw=0.9, ms=8)
    ax.text(0.55, -0.94, r'$U_1$', fontsize=12, ha='center')
    ax.plot([1.9, 1.9], [-0.24, -0.48], 'k-', lw=0.9)
    ax.plot([1.80, 1.80], [-0.24, -0.48], 'k-', lw=0.9)
    arrow(ax, (1.9, -0.39), (1.80, -0.39), lw=0.9, ms=8)
    ax.text(2.04, -0.84, r'$U_2$', fontsize=12, ha='center')

    # spring labels alpha
    for x in (2.42, 3.44, 4.72, 6.31):
        ax.text(x, -0.38, r'$\alpha$', fontsize=12, ha='center')

    # mass labels
    ax.text(4.32, 0.40, r'$M_2$', fontsize=12, ha='center')
    ax.text(6.32, 0.40, r'$M_1$', fontsize=12, ha='center')

    # cell labels
    for i in range(3):
        ax.text(0.1 + i * cell + cell / 2.0, -1.38,
                r'Cell %d' % (i + 1), fontsize=12, ha='center')

    ax.set_xlim(-0.75, 8.05)
    ax.set_ylim(-1.62, 1.12)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 17)


# ======================================================================
# Fig. 18  Vibration frequencies of diatomic chain  (p.33)
# ======================================================================
def fig_18():
    fig, ax = plt.subplots(figsize=(3.4, 3.15))
    x = np.linspace(-1, 1, 401)
    opt = 0.72 + 0.28 * np.cos(np.pi * x / 2.0) ** 2
    ac = 0.36 * np.sin(np.pi * np.abs(x) / 2.0)

    ax.plot([-1.18, 1.18], [0, 0], 'k-', lw=1.1)               # base line
    arrow(ax, (0, 0.0), (0, 1.10), lw=1.1)                     # nu axis
    ax.plot([-1, -1], [0, 0.72], 'k-', lw=0.9)
    ax.plot([1, 1], [0, 0.72], 'k-', lw=0.9)
    ax.plot(x, opt, 'k-', lw=1.3)
    ax.plot(x, ac, 'k-', lw=1.3)
    for y in (0.72, 0.36):                                     # axis ticks
        ax.plot([-0.035, 0.035], [y, y], 'k-', lw=1.0)

    ax.text(0.05, 1.06, r'$\nu$', fontsize=12)
    ax.text(0.10, 0.765, r'Optical', fontsize=11)
    ax.text(0.68, 0.92, r'$\nu_+$', fontsize=12)
    ax.text(0.395, 0.095, r'Acoustic', fontsize=11, rotation=50,
            rotation_mode='anchor')
    ax.text(0.76, 0.19, r'$\nu_-$', fontsize=12)
    ax.text(-1, -0.26, r'$-\pi/2a$', ha='center')
    ax.text(0, -0.26, r'$O$', ha='center')
    ax.text(1, -0.26, r'$\pi/2a$', ha='center')
    arrow(ax, (0.22, -0.50), (0.58, -0.50), lw=1.0, ms=9)
    ax.text(0.40, -0.76, r'$q$', ha='center', fontsize=12)
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-0.90, 1.22)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 18)


# ======================================================================
# Fig. 19  Vibration frequencies, three panels  (p.34)
#   (a) monatomic chain treated as diatomic (reduced zone -pi/2a..pi/2a)
#   (b) same, opened out (repeated zone)   (c) diatomic chain treated
#       as monatomic: gaps appear at +-pi/2a
# ======================================================================
def _panel_frame(ax, xmax, nu_top, nu_label):
    """Bottom axis, central vertical axis, label positions."""
    ax.plot([-xmax, xmax], [0, 0], 'k-', lw=1.0)
    if nu_label:
        arrow(ax, (0, 0), (0, nu_top), lw=1.0, ms=9)
        ax.text(0.06, nu_top - 0.03, r'$\nu$', fontsize=11)
    else:
        ax.plot([0, 0], [0, nu_top], 'k-', lw=0.9)


def fig_19():
    fig, axs = plt.subplots(1, 3, figsize=(4.8, 2.3))

    # ---------------- (a) ----------------
    ax = axs[0]
    xa = np.linspace(-1, 1, 201)
    opt = np.cos(np.pi * xa / 4.0)
    ac = np.abs(np.sin(np.pi * xa / 4.0))
    _panel_frame(ax, 1.0, 1.34, True)
    ax.plot([-1, -1], [0, 1.0], 'k-', lw=0.9)
    ax.plot([1, 1], [0, 1.0], 'k-', lw=0.9)
    ax.plot(xa, opt, 'k-', lw=1.2)
    ax.plot(xa, ac, 'k-', lw=1.2)
    ax.text(-0.10, 1.03, r'$B$', ha='right', fontsize=11)
    ax.text(0.10, 1.03, r"$B'$", ha='left', fontsize=11)
    ax.text(-1.06, 0.87, r'$A$', ha='right', fontsize=9)
    ax.text(-1.06, 0.56, r"$A'$", ha='right', fontsize=9)
    ax.text(1.06, 0.87, r"$A'$", ha='left', fontsize=9)
    ax.text(1.06, 0.56, r'$A$', ha='left', fontsize=9)
    ax.text(-1, -0.30, r'$-\pi/2a$', ha='center', fontsize=9)
    ax.text(0, -0.30, r'$O$', ha='center', fontsize=10)
    ax.text(1, -0.30, r'$\pi/2a$', ha='center', fontsize=9)
    arrow(ax, (0.12, -0.56), (0.48, -0.56), lw=0.9, ms=8)
    ax.text(0.30, -0.82, r'$q$', ha='center', fontsize=11)
    ax.text(0, -1.38, r'$(a)$', ha='center', fontsize=11)
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.55, 1.35)
    ax.set_aspect('equal')
    ax.axis('off')

    # ---------------- (b) ----------------
    ax = axs[1]
    xb = np.linspace(-2, 2, 401)
    nu = np.abs(np.sin(np.pi * xb / 4.0))
    _panel_frame(ax, 2.0, 1.22, True)
    for xv in (-2, -1, 1, 2):
        ax.plot([xv, xv], [0, abs(np.sin(np.pi * xv / 4.0))], 'k-', lw=0.9)
    ax.plot(xb, nu, 'k-', lw=1.2)
    ax.text(-2.08, 1.02, r"$B'$", ha='right', fontsize=11)
    ax.text(2.06, 1.02, r'$B$', ha='left', fontsize=11)
    ax.text(-0.90, 0.53, r"$A'$", ha='left', fontsize=11)
    ax.text(0.90, 0.53, r'$A$', ha='right', fontsize=11)
    for xv, lab in ((-2, r'$-\pi/a$'), (-1, r'$-\pi/2a$'), (0, r'$O$'),
                    (1, r'$\pi/2a$'), (2, r'$\pi/a$')):
        ax.text(xv, -0.30, lab, ha='center', fontsize=5.5)
    arrow(ax, (0.15, -0.62), (0.51, -0.62), lw=0.9, ms=8)
    ax.text(0.33, -0.92, r'$q$', ha='center', fontsize=10)
    ax.text(0, -1.55, r'$(b)$', ha='center', fontsize=11)
    ax.set_xlim(-2.85, 2.85)
    ax.set_ylim(-1.75, 1.42)
    ax.set_aspect('equal')
    ax.axis('off')

    # ---------------- (c) ----------------
    ax = axs[2]
    _panel_frame(ax, 2.0, 1.22, False)
    for xv in (-2, -1, 1, 2):
        top = 1.0 if abs(xv) == 2 else 0.66
        ax.plot([xv, xv], [0, top], 'k-', lw=0.9)
    seg_l = PchipInterpolator([-2.0, -1.72, -1.42, -1.18, -1.0],
                              [1.0, 0.965, 0.845, 0.715, 0.62])
    seg_i = PchipInterpolator([-1.0, -0.72, -0.42, -0.15, 0.0],
                              [0.42, 0.30, 0.165, 0.055, 0.0])
    xl = np.linspace(-2, -1, 80)
    xi = np.linspace(-1, 0, 80)
    ax.plot(xl, seg_l(xl), 'k-', lw=1.2)
    ax.plot(xi, seg_i(xi), 'k-', lw=1.2)
    ax.plot(-xi, seg_i(xi), 'k-', lw=1.2)              # mirror inner
    ax.plot(-xl, seg_l(xl), 'k-', lw=1.2)              # mirror outer
    for xv, lab in ((-2, r'$-\pi/a$'), (-1, r'$-\pi/2a$'), (0, r'$O$'),
                    (1, r'$\pi/2a$'), (2, r'$\pi/a$')):
        ax.text(xv, -0.30, lab, ha='center', fontsize=5.5)
    arrow(ax, (0.15, -0.62), (0.51, -0.62), lw=0.9, ms=8)
    ax.text(0.33, -0.92, r'$q$', ha='center', fontsize=10)
    ax.text(0, -1.55, r'$(c)$', ha='center', fontsize=11)
    ax.set_xlim(-2.85, 2.85)
    ax.set_ylim(-1.75, 1.42)
    ax.set_aspect('equal')
    ax.axis('off')

    fig.subplots_adjust(wspace=0.02)
    save(fig, 19)


# ======================================================================
# Fig. 20  Constant frequency surfaces (cross-sections)  (p.35)
#   (a) isotropic medium: circles L, T1, T2 (T1,T2 nearly degenerate)
#   (b) real crystal: anisotropic, crossing surfaces
# ======================================================================
def fig_20():
    fig, axs = plt.subplots(1, 2, figsize=(4.4, 2.5))

    # ---------------- (a) ----------------
    ax = axs[0]
    ax.plot(0, 0, 'k.', ms=5)
    th = np.linspace(0, 2 * np.pi, 361)
    ax.plot(0.42 * np.cos(th), 0.42 * np.sin(th), 'k-', lw=1.1)
    ax.plot(0.93 * np.cos(th), 0.93 * np.sin(th), 'k-', lw=1.1)
    ax.plot(0.985 * np.cos(th), 0.985 * np.sin(th), 'k-', lw=1.1)
    ax.text(0.24, 0.40, r'$L$', fontsize=12)
    ax.text(0.47, 0.585, r'$T_1$', fontsize=12)
    ax.text(0.68, 0.87, r'$T_2$', fontsize=12)
    ax.text(0, -1.32, r'$(a)$', ha='center', fontsize=11)
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.55, 1.22)
    ax.set_aspect('equal')
    ax.axis('off')

    # ---------------- (b) ----------------
    ax = axs[1]
    ax.plot(0, 0, 'k.', ms=5)
    diamond(ax, 0, 0, 0.24, 0.22, lw=1.1)          # L
    diamond(ax, 0, 0, 0.52, 0.15, lw=1.1)          # T1
    rosette(ax, 0, 0, 0.61, 0.13, lw=1.1)          # T2 (lobes on diagonals)
    ax.text(0.16, 0.23, r'$L$', fontsize=12)
    ax.text(0.35, 0.44, r'$T_1$', fontsize=12)
    ax.text(0.56, 0.67, r'$T_2$', fontsize=12)
    ax.text(0, -1.32, r'$(b)$', ha='center', fontsize=11)
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.55, 1.22)
    ax.set_aspect('equal')
    ax.axis('off')

    fig.subplots_adjust(wspace=0.02)
    save(fig, 20)


# ======================================================================
# Fig. 21  Dispersion of lattice waves in a given direction  (p.36)
# ======================================================================
def fig_21():
    fig, ax = plt.subplots(figsize=(3.3, 2.95))
    L = PchipInterpolator([0.0, 0.15, 0.35, 0.55, 0.75, 0.95, 1.10, 1.20],
                          [0.0, 0.395, 0.665, 0.815, 0.885, 0.865, 0.815, 0.79])
    T1 = PchipInterpolator([0.0, 0.2, 0.45, 0.7, 0.9, 1.05, 1.20],
                           [0.0, 0.265, 0.50, 0.68, 0.78, 0.825, 0.858])
    T2 = PchipInterpolator([0.0, 0.25, 0.5, 0.75, 1.0, 1.20],
                           [0.0, 0.14, 0.27, 0.385, 0.485, 0.545])
    x = np.linspace(0, 1.2, 200)

    ax.plot([0, 0], [0, 1.13], 'k-', lw=1.1)                  # nu axis
    ax.plot([0, 1.30], [0, 0], 'k-', lw=1.1)                  # q axis
    ax.plot([1.20, 1.20], [0, 0.87], 'k-', lw=1.0)            # zone boundary
    ax.plot(x, L(x), 'k-', lw=1.35)
    ax.plot(x, T1(x), 'k-', lw=1.35)
    ax.plot(x, T2(x), 'k-', lw=1.35)

    ax.text(-0.05, 1.10, r'$\nu_q$', ha='right', fontsize=12)
    ax.text(0.27, 0.51, r'$L$', fontsize=12)
    ax.text(0.63, 0.715, r'$T_1$', fontsize=12)
    ax.text(0.775, 0.315, r'$T_2$', fontsize=12)
    ax.text(-0.03, -0.135, r'$O$', ha='center', fontsize=11)
    ax.text(0.52, -0.135, r'$q$', ha='center', fontsize=12)
    ax.text(1.28, -0.135, r'Zone boundary', ha='right', fontsize=11)
    ax.set_xlim(-0.22, 1.42)
    ax.set_ylim(-0.26, 1.24)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 21)


# ======================================================================
# Fig. 22  A branch of the lattice frequency function nu_q in the
#          repeated zone scheme (contour-like pattern)  (p.37)
# ======================================================================
def fig_22():
    fig, ax = plt.subplots(figsize=(3.5, 3.4))

    # thin straight lines through the reciprocal lattice points
    for i in range(-2, 3):
        ax.plot([i, i], [-1.55, 1.55], 'k-', lw=0.5, zorder=1)
        ax.plot([-1.55, 1.55], [i, i], 'k-', lw=0.5, zorder=1)

    # pockets: concentric contours, circles inside, rounded squares outside
    spec = [(0.09, 0.00, 0.8), (0.17, 0.02, 0.8), (0.25, 0.05, 0.8),
            (0.33, 0.09, 0.9), (0.40, 0.11, 0.9), (0.43, 0.10, 1.4)]
    for i in range(-1, 2):
        for j in range(-1, 2):
            for r0, e, lw in spec:
                rosette(ax, i, j, r0, e, lw=lw)

    # almond-shaped pairs at the middle of each axial channel
    for i in range(-2, 2):
        for j in range(-1, 2):
            lens(ax, i + 0.5, j, 0.50, 0.088, horiz=True)
            lens(ax, i + 0.5, j, 0.30, 0.050, horiz=True)
            lens(ax, j, i + 0.5, 0.50, 0.088, horiz=False)
            lens(ax, j, i + 0.5, 0.30, 0.050, horiz=False)

    # crossing arcs near the diagonal saddles
    for i in range(-2, 2):
        for j in range(-2, 2):
            hyper_arc(ax, i + 0.5, j + 0.5, 0.04, 0.30, 0.13, diag=+1)
            hyper_arc(ax, i + 0.5, j + 0.5, 0.04, 0.30, 0.13, diag=-1)

    # reciprocal lattice points
    for i in range(-1, 2):
        for j in range(-1, 2):
            ax.plot(i, j, 'k.', ms=4, zorder=6)

    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.55, 1.55)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 22)


# ======================================================================
# Fig. 23  Ionic crystal with two sublattices (bare "Fig. 23")  (p.38)
# ======================================================================
def fig_23():
    fig, ax = plt.subplots(figsize=(3.3, 3.9))
    r = 0.42

    # grid of thin lines through the sites
    for i in range(6):
        ax.plot([i, i], [0.70, -5.70], 'k-', lw=0.8, zorder=1)
    for j in range(6):
        ax.plot([-0.70, 5.70], [-j, -j], 'k-', lw=0.8, zorder=1)

    # positive ions (hatched, +) at even-even sites
    for i in range(0, 5, 2):
        for j in range(0, 5, 2):
            ax.add_patch(Circle((i, -j), r, fc='white', ec='k', lw=1.2,
                                hatch='///', zorder=3))
            ax.plot([i - 0.16, i + 0.16], [-j, -j], 'k-', lw=1.3, zorder=4)
            ax.plot([i, i], [-j - 0.16, -j + 0.16], 'k-', lw=1.3, zorder=4)
    # negative ions (open, -) at odd-odd sites
    for i in range(1, 4, 2):
        for j in range(1, 6, 2):
            ax.add_patch(Circle((i, -j), r, fc='white', ec='k', lw=1.2,
                                zorder=3))
            ax.plot([i - 0.16, i + 0.16], [-j, -j], 'k-', lw=1.3, zorder=4)

    # arrows
    arrow(ax, (-0.30, 0.62), (2.30, 0.62))                     # l (top)
    ax.text(0.95, 0.80, r'$l$', fontsize=13, ha='center')
    arrow(ax, (-0.62, 0.32), (-0.62, -2.30))                   # l (left)
    ax.text(-0.92, -1.0, r'$l$', fontsize=13, ha='center')
    arrow(ax, (0, 0), (0.80, -0.80), lw=1.1)                   # x
    ax.text(0.20, -0.66, r'$\boldsymbol{x}$', fontsize=12)
    arrow(ax, (1, -1), (2.62, -1))                             # l (row)
    ax.text(1.95, -0.80, r'$l$', fontsize=13, ha='center')
    arrow(ax, (1, -1), (1, -2.62))                             # l (column)
    ax.text(1.22, -1.70, r'$l$', fontsize=13)

    ax.set_xlim(-1.05, 5.95)
    ax.set_ylim(-5.90, 0.95)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 23)


# ======================================================================
# Fig. 24  The Debye law of specific heat  (p.45)
# ======================================================================
def fig_24():
    from scipy.integrate import quad
    fig, ax = plt.subplots(figsize=(3.6, 2.95))

    def cv(x):
        if x < 1e-6:
            return 0.0
        val, _ = quad(lambda z: z**4 * np.exp(z) / (np.exp(z) - 1.0)**2,
                      0.0, 1.0 / x, limit=200)
        return min(1.0, 3.0 * x**3 * val)

    xs = np.linspace(0.0, 2.45, 200)
    ys = np.array([cv(x) for x in xs])
    ys[ys < 0] = 0.0

    ax.plot([0, 0], [-0.02, 1.20], 'k-', lw=1.1)               # axes
    arrow(ax, (0, 1.20), (0, 1.30), lw=1.1)
    ax.plot([0, 2.68], [0, 0], 'k-', lw=1.1)
    arrow(ax, (2.68, 0), (2.78, 0), lw=1.1)
    ax.plot([0, 2.68], [1.0, 1.0], 'k--', lw=1.0)              # 3Nk
    ax.plot(xs, ys, 'k-', lw=1.35)
    ax.plot([1, 1], [-0.045, 0.0], 'k-', lw=1.0)               # tick at 1

    ax.text(-0.09, 0.50, r'$C_V$', ha='right', fontsize=12)
    ax.text(-0.09, 1.0, r'$3Nk$', ha='right', fontsize=12)
    ax.text(1.0, -0.16, r'$1$', ha='center', fontsize=11)
    ax.text(2.72, -0.16, r'$T/\Theta$', ha='right', fontsize=12)
    ax.text(-0.05, -0.16, r'$O$', ha='center', fontsize=11)
    ax.text(0.34, 0.235, r'$T^3$', fontsize=12)
    ax.set_xlim(-0.62, 2.92)
    ax.set_ylim(-0.28, 1.42)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 24)


# ======================================================================
# Fig. 25  (a) the Debye spectrum, (b) a true lattice spectrum (p.46)
# ======================================================================
def fig_25():
    fig, axs = plt.subplots(1, 2, figsize=(4.8, 2.6),
                            gridspec_kw=dict(width_ratios=[1.0, 1.05]))

    # ---------------- (a) Debye spectrum: D(nu) ~ nu^2 ----------------
    ax = axs[0]
    ax.plot([0, 0], [0, 1.16], 'k-', lw=1.1)
    ax.plot([0, 1.42], [0, 0], 'k-', lw=1.1)
    x = np.linspace(0, 1, 200)
    ax.plot(x, x**2, 'k-', lw=1.35)
    ax.text(-0.05, 1.10, r'$\mathcal{D}(\nu)$', ha='right', fontsize=12)
    ax.text(0.30, 0.135, r'$\nu^2$', fontsize=12, rotation=38,
            rotation_mode='anchor')
    ax.text(1.0, -0.17, r'$\nu_D$', ha='center', fontsize=12)
    ax.text(1.40, -0.17, r'$\nu$', ha='right', fontsize=12)
    ax.text(0.35, -1.02, r'$(a)$', ha='center', fontsize=11)
    ax.set_xlim(-0.42, 1.58)
    ax.set_ylim(-1.24, 1.32)
    ax.set_aspect('equal')
    ax.axis('off')

    # ---------------- (b) true lattice spectrum ----------------
    ax = axs[1]
    ax.plot([0, 0], [0, 1.16], 'k-', lw=1.1)
    ax.plot([0, 1.30], [0, 0], 'k-', lw=1.1)
    px = [0.0, 0.10, 0.22, 0.34, 0.45, 0.55, 0.62, 0.68, 0.73, 0.77,
          0.795, 0.805, 0.825, 0.855, 0.90, 0.955, 1.0]
    py = [0.0, 0.012, 0.055, 0.16, 0.33, 0.53, 0.555, 0.475, 0.43, 0.52,
          0.78, 0.92, 0.78, 0.32, 0.16, 0.09, 0.045]
    curve = PchipInterpolator(px, py)
    xb = np.linspace(0, 1.0, 400)
    ax.plot(xb, curve(xb), 'k-', lw=1.2)
    ax.text(-0.05, 1.10, r'$\mathcal{D}(\nu)$', ha='right', fontsize=12)
    ax.text(-0.035, -0.17, r'$O$', ha='center', fontsize=11)
    ax.text(1.28, -0.17, r'$\nu$', ha='right', fontsize=12)
    ax.text(0.55, -1.02, r'$(b)$', ha='center', fontsize=11)
    ax.set_xlim(-0.42, 1.58)
    ax.set_ylim(-1.24, 1.32)
    ax.set_aspect('equal')
    ax.axis('off')

    fig.subplots_adjust(wspace=0.10)
    save(fig, 25)


# ----------------------------------------------------------------------
if __name__ == '__main__':
    for f in (fig_16, fig_17, fig_18, fig_19, fig_20, fig_21, fig_22,
              fig_23, fig_24, fig_25):
        f()
    print('all done')
