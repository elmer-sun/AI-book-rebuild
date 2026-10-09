# -*- coding: utf-8 -*-
"""
Redraw Chapter 4 figures of Carroll, "Spacetime and Geometry" as
black-and-white textbook-style vector figures (matplotlib).

Figures:
  fig_4.1  Feynman diagram for electromagnetism (two electron lines +
           vertical wavy photon propagator).                 [book p.166]
  fig_4.2  Feynman diagrams for gravity: electron-electron scattering via
           graviton exchange (coil propagator), and graviton
           self-interaction (four coil branches off a central coil). [p.167]
  fig_4.3  Energy conditions for perfect fluids: six panels showing the
           allowed region in the (rho, p) plane for WEC, NEC, DEC, NDEC,
           SEC and w >= -1.                                  [book p.176]
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'figures')
PRE = os.path.join(OUT, 'preview')
os.makedirs(PRE, exist_ok=True)

BLACK = 'k'
GRAY_FILL = '0.85'


# ----------------------------------------------------------------------
# low-level helpers
# ----------------------------------------------------------------------
def _wavy(ax, p0, p1, amp=0.2, cycles=4.0, lw=1.0, n=800):
    """Sinusoidal (photon) propagator from p0 to p1."""
    x0, y0 = p0
    dx, dy = p1[0] - x0, p1[1] - y0
    L = np.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    t = np.linspace(0.0, 1.0, n)
    q = amp * np.sin(2.0 * np.pi * cycles * t)
    a = L * t
    x = x0 + a * ux + q * nx
    y = y0 + a * uy + q * ny
    ax.plot(x, y, color=BLACK, lw=lw, solid_capstyle='round')


def _coil(ax, p0, p1, r=0.3, turns=4.0, k=0.6, lw=0.95, n=1600):
    """Spring/coil (graviton) propagator from p0 to p1.

    Parametrization: transverse offset r*sin(theta) plus an along-axis
    oscillation r*k*(cos(theta)-1) (tilted-loop projection), which yields
    the open overlapping loops of a wire spring as in the book.
    """
    x0, y0 = p0
    dx, dy = p1[0] - x0, p1[1] - y0
    L = np.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    t = np.linspace(0.0, 1.0, n)
    th = 2.0 * np.pi * turns * t
    q = r * np.sin(th)
    a = L * t + r * k * (np.cos(th) - 1.0)
    x = x0 + a * ux + q * nx
    y = y0 + a * uy + q * ny
    ax.plot(x, y, color=BLACK, lw=lw, solid_capstyle='round')


def _fermion(ax, p0, p1, arrows=((0.45, 1),), lw=1.05):
    """Straight fermion line p0->p1 with mid-line arrowheads.

    arrows: sequence of (fraction_along_line, direction); direction +1
    means the arrow points toward p1, -1 toward p0.
    """
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=BLACK, lw=lw,
            solid_capstyle='round')
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = np.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    for frac, direction in arrows:
        px, py = p0[0] + frac * dx, p0[1] + frac * dy
        s = 0.075 * direction
        ax.annotate('', xy=(px + s * ux, py + s * uy),
                    xytext=(px - s * ux, py - s * uy),
                    arrowprops=dict(arrowstyle='-|>', color=BLACK, lw=0,
                                    mutation_scale=10, shrinkA=0, shrinkB=0))


def _electron_label(ax, xy, above=True):
    s = 0.10 if above else -0.16
    ax.text(xy[0] - 0.08, xy[1] + s, r'$e^-$', ha='right', va='center',
            fontsize=12)


# ----------------------------------------------------------------------
# Figure 4.1 : electromagnetic interaction
# ----------------------------------------------------------------------
def fig_4_1():
    fig = plt.figure(figsize=(3.2, 2.05))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-2.62, 2.85)
    ax.set_ylim(-2.02, 2.02)

    V1, V2 = (0.0, 0.95), (0.0, -0.95)
    A1, A2 = (-2.05, 1.63), (2.15, 1.67)   # upper electron line, L and R
    B1, B2 = (-2.05, -1.63), (2.15, -1.67)  # lower electron line, L and R

    _wavy(ax, V1, V2, amp=-0.23, cycles=4.0)
    ax.text(0.46, 0.0, 'photon', ha='left', va='center', fontsize=11)

    _fermion(ax, A1, V1, arrows=[(0.45, 1)])
    _fermion(ax, V1, A2, arrows=[(0.38, 1)])
    _fermion(ax, B1, V2, arrows=[(0.45, 1)])
    _fermion(ax, V2, B2, arrows=[(0.45, 1)])
    _electron_label(ax, A1, above=True)
    _electron_label(ax, B1, above=False)

    fig.savefig(os.path.join(OUT, 'fig_4.1.pdf'),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRE, 'fig_4.1.png'), dpi=220,
                bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


# ----------------------------------------------------------------------
# Figure 4.2 : gravitational interaction (graviton exchange + self-coupling)
# ----------------------------------------------------------------------
def fig_4_2():
    fig = plt.figure(figsize=(4.8, 2.0))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-2.72, 9.05)
    ax.set_ylim(-2.60, 2.60)

    # ---- left diagram : e- e- scattering via graviton exchange ----
    V1, V2 = (0.0, 0.95), (0.0, -0.95)
    _coil(ax, V1, V2, r=0.48, turns=4.0, k=0.5)
    ax.text(0.88, 0.0, 'graviton', ha='left', va='center', fontsize=11)

    A1, A2 = (-2.05, 1.63), (2.15, 1.67)
    B1, B2 = (-2.05, -1.63), (2.15, -1.67)
    _fermion(ax, A1, V1, arrows=[(0.45, 1)])
    _fermion(ax, V1, A2, arrows=[(0.35, 1)])
    _fermion(ax, B1, V2, arrows=[(0.45, 1)])
    _fermion(ax, V2, B2, arrows=[(0.40, 1)])
    _electron_label(ax, A1, above=True)
    _electron_label(ax, B1, above=False)

    # ---- right diagram : graviton self-interaction ----
    # central coil, short straight stems out of both ends, and two branch
    # springs peeling off left/right from each stem tip (as in the book)
    gx = 6.55
    C1, C2 = (gx, 0.95), (gx, -0.95)
    _coil(ax, C1, C2, r=0.44, turns=4.0, k=0.55)
    S1, S2 = (gx, 1.48), (gx, -1.48)          # stem tips
    ax.plot([C1[0], S1[0]], [C1[1], S1[1]], color=BLACK, lw=1.0)
    ax.plot([C2[0], S2[0]], [C2[1], S2[1]], color=BLACK, lw=1.0)
    for sx, sy in ((-1, 1), (1, 1), (-1, -1), (1, -1)):
        start = (gx, sy * 1.48)
        tip = (gx + sx * 1.95, sy * (1.48 + 0.60))
        _coil(ax, start, tip, r=0.30, turns=5.0, k=0.8)
    ax.text(gx + 0.78, 0.0, 'gravitons', ha='left', va='center', fontsize=11)

    fig.savefig(os.path.join(OUT, 'fig_4.2.pdf'),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRE, 'fig_4.2.png'), dpi=220,
                bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


# ----------------------------------------------------------------------
# Figure 4.3 : energy conditions (six panels)
# ----------------------------------------------------------------------
D = 1.15   # half-width of the diagonal square (shading box)
L = 1.32   # half-length of the drawn coordinate axes


def _panel(ax, polys, solids, label):
    """One energy-condition panel in the (rho, p) plane."""
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-1.62, 1.72)
    ax.set_ylim(-2.16, 1.58)

    # allowed region(s), light gray
    for P in polys:
        ax.add_patch(Polygon(P, closed=True, facecolor=GRAY_FILL,
                             edgecolor='none'))

    # dashed 45-degree reference diagonals (p = -rho and p = +rho)
    for (a, b) in (((-D, D), (D, -D)), ((-D, -D), (D, D))):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=BLACK, lw=0.9,
                dashes=(4.5, 3.0))

    # thick solid region boundaries
    for (a, b) in solids:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=BLACK, lw=1.6,
                solid_capstyle='round')

    # thin coordinate axes with arrowheads
    common = dict(arrowstyle='-|>', color=BLACK, lw=0.9, mutation_scale=9,
                  shrinkA=0, shrinkB=0)
    ax.annotate('', xy=(L, 0), xytext=(-L, 0), arrowprops=dict(common))
    ax.annotate('', xy=(0, L), xytext=(0, -D - 0.08),
                arrowprops=dict(common))
    ax.text(L - 0.02, -0.24, r'$\rho$', ha='center', va='top', fontsize=12)
    ax.text(0.10, L + 0.02, r'$p$', ha='left', va='bottom', fontsize=12)

    ax.text(0.0, -1.80, label, ha='center', va='center', fontsize=11)


def fig_4_3():
    fig = plt.figure(figsize=(4.8, 3.6))
    pw, ph = 0.305, 0.425
    xs = [0.015, 0.355, 0.695]
    ys = [0.515, 0.035]

    O = (0.0, 0.0)
    TL, TR = (-D, D), (D, D)          # top corners of the diagonal square
    BL, BR = (-D, -D), (D, -D)        # bottom corners
    shallow = (D, -D / 3.0)           # p = -rho/3 endpoint (SEC)

    panels = [
        # (a) WEC : rho >= 0 and rho + p >= 0
        ([[(0, 0), (0, D), (D, D), (D, -D)]],
         [(O, (0, D)), (O, BR)],
         '(a) WEC'),
        # (b) NEC : rho + p >= 0
        ([[TL, TR, BR]],
         [(TL, BR)],
         '(b) NEC'),
        # (c) DEC : rho >= 0 and rho >= |p|
        ([[O, (D, D), (D, -D)]],
         [(O, (D, D)), (O, BR)],
         '(c) DEC'),
        # (d) NDEC : rho >= |p|
        ([[O, (D, D), (D, -D)], [O, (-D, D), (-D, -D)]],
         [((-D, D), BR), ((-D, -D), (D, D))],
         '(d) NDEC'),
        # (e) SEC : rho + p >= 0 and rho + 3p >= 0
        ([[(-D, D), O, shallow, (D, D)]],
         [((-D, D), O), (O, shallow)],
         '(e) SEC'),
        # (f) w >= -1 (inequality flips for rho < 0)
        ([[(0, 0), (0, D), (D, D), (D, -D)],
          [(0, 0), (-D, D), (-D, -D), (0, -D)]],
         [((-D, D), BR), (O, (0, -D))],
         r'(f) $w \geq -1$'),
    ]

    for i, (polys, solids, label) in enumerate(panels):
        row, col = divmod(i, 3)
        ax = fig.add_axes([xs[col], ys[row], pw, ph])
        _panel(ax, polys, solids, label)

    fig.savefig(os.path.join(OUT, 'fig_4.3.pdf'),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRE, 'fig_4.3.png'), dpi=220,
                bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


# ----------------------------------------------------------------------
if __name__ == '__main__':
    for f in (fig_4_1, fig_4_2, fig_4_3):
        f()
        print('done:', f.__name__)
