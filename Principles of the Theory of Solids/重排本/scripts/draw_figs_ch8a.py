# -*- coding: utf-8 -*-
"""
Ziman, Principles of the Theory of Solids, 2nd ed.  Chapter 8 (Optical properties)
Redraw Figs. 136-144 as black-and-white vector figures.

Output: figures/fig_136.pdf ... fig_144.pdf  (+ figures/preview/*.png)
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

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)               # .../重排本
FIGD = os.path.join(ROOT, 'figures')
PREV = os.path.join(FIGD, 'preview')
os.makedirs(PREV, exist_ok=True)


def save(fig, key):
    fig.savefig(os.path.join(FIGD, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, 'fig_%s.png' % key),
                bbox_inches='tight', pad_inches=0.03, dpi=200)
    plt.close(fig)
    print('saved', key)


def arrow(ax, x0, y0, x1, y1, lw=1.2, ms=9, ls='-', zorder=5):
    """straight arrow drawn as annotate (solid head)."""
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), zorder=zorder,
                arrowprops=dict(arrowstyle='-|>', color='black',
                                lw=lw, ls=ls, mutation_scale=ms,
                                shrinkA=0, shrinkB=0))


def smooth(ks, ys, n=400, w=25):
    """dense interpolation + moving-average smoothing of a hand-made curve."""
    t = np.linspace(ks[0], ks[-1], n)
    y = np.interp(t, ks, ys)
    ker = np.ones(w) / w
    ext = np.r_[y[:w][::-1], y, y[-w:][::-1]]
    ys_s = np.convolve(ext, ker, mode='same')[w:-w]
    return t, ys_s


# ----------------------------------------------------------------------------
# Fig. 136  (p.257)  Incident (E1), reflected (E2) and damped transmitted (E0)
#                    waves at normal incidence on a absorbing medium (z > 0).
# ----------------------------------------------------------------------------
def fig_136():
    fig, ax = plt.subplots(figsize=(3.7, 2.45))
    ax.axis('off')
    ax.set_xlim(-0.56, 0.53)
    ax.set_ylim(-0.40, 0.37)
    ax.set_aspect('equal')

    # hatched medium: irregular blob filling z > 0
    th = np.linspace(-np.pi / 2, np.pi / 2, 80)
    xb = 0.46 * np.cos(th) * (1 + 0.05 * np.sin(2.5 * th + 0.8))
    yb = 0.315 * np.sin(th) * (1 + 0.06 * np.sin(3 * th + 2.0))
    blob = np.vstack([np.c_[xb, yb], [[0.0, -0.315]]])
    ax.add_patch(plt.Polygon(blob, closed=True, facecolor='white',
                             edgecolor='black', lw=0.9, hatch='/////',
                             zorder=2))
    ax.plot([0, 0], [-0.315, 0.315], color='black', lw=1.4, zorder=4)

    # z axis (chain-dotted) with arrow, O and z labels
    ax.plot([-0.06, 0.47], [0, 0], color='black', lw=0.7,
            ls=(0, (6, 3, 1, 3)), zorder=3)
    arrow(ax, 0.47, 0, 0.505, 0, lw=0.8, ms=8)
    ax.text(-0.028, 0.012, '$O$', fontsize=11, ha='right', va='bottom')
    ax.text(0.472, -0.016, '$z$', fontsize=11, ha='left', va='top')

    # E2 : reflected wave travelling left (centre line + arrow pointing left)
    x2 = np.linspace(-0.53, 0.0, 400)
    y2 = 0.115 + 0.042 * np.cos(2 * np.pi * (x2 + 0.53) / 0.118)
    ax.plot([-0.53, 0], [0.115, 0.115], color='black', lw=0.7, zorder=3)
    ax.plot(x2, y2, color='black', lw=1.2, zorder=4)
    arrow(ax, -0.505, 0.115, -0.545, 0.115, lw=0.8, ms=8)
    ax.text(-0.235, 0.185, '$E_2$', fontsize=11, ha='center', va='bottom')

    # E1 : incident wave travelling right
    x1 = np.linspace(-0.53, 0.0, 400)
    y1 = -0.175 + 0.105 * np.cos(2 * np.pi * (x1 + 0.53) / 0.15)
    ax.plot([-0.53, 0], [-0.175, -0.175], color='black', lw=0.7, zorder=3)
    ax.plot(x1, y1, color='black', lw=1.2, zorder=4)
    arrow(ax, -0.042, -0.175, -0.004, -0.175, lw=0.8, ms=8)
    ax.text(-0.164, -0.048, '$E_1$', fontsize=11, ha='center', va='bottom')

    # E0 : damped wave inside the medium (about the z axis)
    x0 = np.linspace(0.0, 0.44, 500)
    y0 = 0.155 * np.exp(-x0 / 0.16) * np.cos(2 * np.pi * x0 / 0.095)
    ax.plot(x0, y0, color='black', lw=1.2, zorder=5)
    ax.text(0.092, -0.088, '$E_0$', fontsize=11, ha='left', va='top')

    save(fig, '136')


# ----------------------------------------------------------------------------
# Fig. 137  (p.263)  Dispersion of light: eps(omega) with two resonances.
# ----------------------------------------------------------------------------
def fig_137():
    fig, ax = plt.subplots(figsize=(3.7, 2.55))
    ax.axis('off')
    ax.set_xlim(-0.22, 2.80)
    ax.set_ylim(-1.75, 4.45)

    w1, w2, f1, f2 = 1.0, 2.1, 1.6, 1.0

    def eps(w):
        return 1.0 + f1 / (w1**2 - w**2) + f2 / (w2**2 - w**2)

    for a, b in [(0.0005, 0.9985), (1.0015, 2.0985), (2.1015, 2.72)]:
        w = np.linspace(a, b, 800)
        ax.plot(w, eps(w), color='black', lw=1.3, zorder=4)

    # axes
    ax.plot([0, 0], [-1.60, 4.05], color='black', lw=1.0)
    arrow(ax, 0, 4.05, 0, 4.22, lw=1.0, ms=9)
    ax.plot([0, 2.62], [0, 0], color='black', lw=1.0)
    arrow(ax, 2.62, 0, 2.74, 0, lw=1.0, ms=9)
    ax.text(-0.045, 3.85, r'$\varepsilon(\omega)$', fontsize=11,
            ha='right', va='center')
    ax.text(2.70, -0.30, r'$\omega$', fontsize=11, ha='center', va='top')

    # dashed level eps = 1
    ax.plot([0, 2.74], [1, 1], color='black', lw=0.8, ls=(0, (5, 3)))
    ax.text(-0.045, 1.0, '$1$', fontsize=11, ha='right', va='center')
    ax.text(-0.045, 0.0, '$0$', fontsize=11, ha='right', va='center')
    ax.text(-0.045, eps(0.0005), r'$\varepsilon(0)$', fontsize=11,
            ha='right', va='center')

    # vertical dashed lines at the resonances
    for wj in (w1, w2):
        ax.plot([wj, wj], [-1.72, 4.30], color='black', lw=0.8,
                ls=(0, (5, 3)), zorder=2)
    ax.text(w1 - 0.03, -0.30, r'$\omega_1$', fontsize=11, ha='right', va='top')
    ax.text(w2 - 0.03, -0.30, r'$\omega_2$', fontsize=11, ha='right', va='top')

    save(fig, '137')


# ----------------------------------------------------------------------------
# Fig. 138  (p.264)  Real (n) and imaginary (k) parts of refractive index.
# ----------------------------------------------------------------------------
def fig_138():
    fig = plt.figure(figsize=(3.1, 4.35))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.22, 1.0],
                          hspace=0.42, left=0.16, right=0.97,
                          top=0.99, bottom=0.05)
    wj = 1.0

    # ---- top panel : n(omega) --------------------------------------------
    ax = fig.add_subplot(gs[0])
    ax.axis('off')
    ax.set_xlim(-0.14, 2.38)
    ax.set_ylim(-0.16, 3.35)

    w = np.linspace(0.0005, 0.995, 700)
    n = np.sqrt(1.0 + 1.4 / (wj**2 - w**2))
    ax.plot(w, n, color='black', lw=1.3, zorder=4)
    w = np.linspace(1.32, 2.30, 300)
    n = 1.0 - 0.85 * (1.32 / w)**2.6
    ax.plot(w, n, color='black', lw=1.3, zorder=4)

    ax.plot([wj, wj], [0, 3.30], color='black', lw=0.8, zorder=3)
    ax.plot([0, 2.30], [1, 1], color='black', lw=0.8, ls=(0, (5, 3)))
    ax.plot([0, 0], [0, 3.02], color='black', lw=1.0)
    arrow(ax, 0, 3.02, 0, 3.18, lw=1.0, ms=9)
    ax.plot([0, 2.18], [0, 0], color='black', lw=1.0)
    arrow(ax, 2.18, 0, 2.30, 0, lw=1.0, ms=9)
    ax.text(-0.045, 2.45, r'$n(\omega)$', fontsize=11, ha='right')
    ax.text(-0.045, 1.0, '$1$', fontsize=11, ha='right', va='center')
    ax.text(wj, -0.13, r'$\omega_j$', fontsize=11, ha='center', va='top')
    ax.text(2.26, -0.13, r'$\omega$', fontsize=11, ha='center', va='top')

    # ---- bottom panel : k(omega) -----------------------------------------
    ax = fig.add_subplot(gs[1])
    ax.axis('off')
    ax.set_xlim(-0.14, 2.38)
    ax.set_ylim(-0.16, 1.42)

    ax.plot([wj, wj], [0, 1.40], color='black', lw=1.2, zorder=4)  # spike
    u = np.linspace(0.008, 1.16, 600)
    k = 0.35 / (u + 0.06) * np.maximum(0.0, 1.0 - (u / 1.16)**6)
    ax.plot(wj + u, k, color='black', lw=1.3, zorder=4)

    ax.plot([0, 0], [0, 1.10], color='black', lw=1.0)
    arrow(ax, 0, 1.10, 0, 1.26, lw=1.0, ms=9)
    ax.plot([0, 2.18], [0, 0], color='black', lw=1.0)
    arrow(ax, 2.18, 0, 2.30, 0, lw=1.0, ms=9)
    ax.text(-0.045, 0.82, r'$k(\omega)$', fontsize=11, ha='right')
    ax.text(wj, -0.13, r'$\omega_j$', fontsize=11, ha='center', va='top')
    ax.text(2.26, -0.13, r'$\omega$', fontsize=11, ha='center', va='top')

    save(fig, '138')


# ----------------------------------------------------------------------------
# Fig. 139  (p.264)  Broadening of the dispersion curve:
#                    Re(eps) and broadened Im(eps) peak of width 2*Gamma.
# ----------------------------------------------------------------------------
def fig_139():
    fig, ax = plt.subplots(figsize=(3.5, 3.55))
    ax.axis('off')
    ax.set_xlim(-0.16, 2.66)
    ax.set_ylim(-1.80, 5.30)
    wj = 1.0
    Gam = 0.16
    f = 2.2 * Gam

    def re_eps(w):
        u = wj**2 - w**2
        return 1.0 + f * u / (u**2 + Gam**2 * w**2)

    w = np.linspace(0.0005, 2.55, 1200)
    re = re_eps(w)
    re = np.where(w < wj, re, 1.0 + 2.2 * (re - 1.0))   # deepen negative lobe
    ax.plot(w, re, color='black', lw=1.3, zorder=5)

    # Im(eps): broadened absorption line (stippled tower, dashed outline)
    sig = 0.125
    wt = np.linspace(wj - 3.6 * sig, wj + 3.6 * sig, 600)
    im = 4.10 * np.exp(-((wt - wj)**2) / (2 * sig**2))
    ax.fill_between(wt, 0, im, facecolor='0.84', edgecolor='none', zorder=3)
    ax.plot(wt, im, color='black', lw=1.1, ls=(0, (4, 2.5)), zorder=4)

    # centre chain line at omega_j
    ax.plot([wj, wj], [0, 4.30], color='0.25', lw=0.7,
            ls=(0, (6, 3, 1, 3)), zorder=3)

    # 2*Gamma bracket at the top of the line
    hw = 0.13
    for s in (-1, +1):
        ax.plot([wj + s * hw, wj + s * hw], [4.02, 4.78],
                color='black', lw=1.0)
    arrow(ax, wj - hw + 0.015, 4.62, wj, 4.62, lw=0.9, ms=7)
    arrow(ax, wj + hw - 0.015, 4.62, wj, 4.62, lw=0.9, ms=7)
    ax.text(wj, 4.92, r'$2\Gamma$', fontsize=11, ha='center', va='bottom')

    # axes
    ax.plot([0, 0], [-1.62, 4.42], color='black', lw=1.0)
    arrow(ax, 0, 4.42, 0, 4.58, lw=1.0, ms=9)
    ax.plot([0, 2.48], [0, 0], color='black', lw=1.0)
    arrow(ax, 2.48, 0, 2.60, 0, lw=1.0, ms=9)
    ax.plot([0, 2.58], [1, 1], color='black', lw=0.8, ls=(0, (5, 3)))
    ax.text(-0.045, 1.0, '$1$', fontsize=11, ha='right', va='center')
    ax.text(0.44, 1.74, r'Re $(\varepsilon)$', fontsize=11, ha='center')
    ax.text(1.34, 1.95, r'Im $(\varepsilon)$', fontsize=11, ha='left')
    ax.text(wj - 0.02, -0.24, r'$\omega_j$', fontsize=11, ha='right', va='top')
    ax.text(2.56, -0.24, r'$\omega$', fontsize=11, ha='center', va='top')

    save(fig, '139')


# ----------------------------------------------------------------------------
# Fig. 140  (p.265)  Lorentz correction: spherical cavity in a uniformly
#                    polarized medium; dipoles on the neighbouring atoms.
# ----------------------------------------------------------------------------
def fig_140():
    fig, ax = plt.subplots(figsize=(3.3, 3.2))
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')

    # uniformly polarized medium (hatched square)
    ax.add_patch(plt.Rectangle((0.02, 0.02), 0.96, 0.96, facecolor='white',
                               edgecolor='black', lw=1.0, hatch='//////',
                               zorder=1))
    # spherical cavity (white punch-out)
    cx, cy, r = 0.5, 0.5, 0.245
    ax.add_patch(plt.Circle((cx, cy), r, facecolor='white',
                            edgecolor='none', zorder=2))
    # ring of small upward field arrows along the cavity surface
    for th in np.linspace(0, 2 * np.pi, 34, endpoint=False):
        x = cx + r * np.cos(th)
        y = cy + r * np.sin(th)
        arrow(ax, x, y - 0.018, x, y + 0.018, lw=0.7, ms=6, zorder=4)

    # neighbouring atoms (dipoles): 3x3 grid minus centre
    dip = [0.195, 0.5, 0.805]
    centres = [(x, y) for y in dip for x in dip if (x, y) != (0.5, 0.5)]
    for (x, y) in centres:
        ax.add_patch(plt.Circle((x, y), 0.088, facecolor='none',
                                edgecolor='black', lw=1.1, zorder=5))
        arrow(ax, x, y - 0.050, x, y + 0.052, lw=1.1, ms=8, zorder=6)
    # atom inside the cavity
    ax.add_patch(plt.Circle((cx, cy), 0.088, facecolor='white',
                            edgecolor='black', lw=1.1, zorder=5))
    arrow(ax, cx, cy - 0.050, cx, cy + 0.052, lw=1.1, ms=8, zorder=6)

    save(fig, '140')


# ----------------------------------------------------------------------------
# Fig. 141  (p.270)  Absorption by optical modes:
#                    (a) one-dimensional scheme, (b) three-dimensional scheme.
# ----------------------------------------------------------------------------
def _skeleton_141(ax, nu_top, nu_left=False):
    ax.axis('off')
    ax.set_xlim(-0.60, 0.60)
    ax.set_ylim(-0.17, 1.14)
    ax.set_aspect('equal')
    for x in (-0.5, 0.5):                      # zone boundaries
        ax.plot([x, x], [0, 0.84], color='black', lw=1.0)
    ax.plot([-0.5, 0.5], [0, 0], color='black', lw=1.0)
    ax.text(-0.5, -0.055, 'Z.B.', fontsize=10, ha='center', va='top')
    ax.text(0.5, -0.055, 'Z.B.', fontsize=10, ha='center', va='top')
    ax.text(0, -0.055, '$O$', fontsize=11, ha='center', va='top')
    ax.text(0.24, -0.055, '$q$', fontsize=11, ha='center', va='top')
    arrow(ax, 0, 0, 0, nu_top, lw=0.9, ms=8)
    if nu_left:
        ax.text(-0.025, nu_top + 0.015, r'$\nu$', fontsize=11,
                ha='right', va='bottom')
    else:
        ax.text(0.025, nu_top + 0.015, r'$\nu$', fontsize=11,
                ha='left', va='bottom')


def fig_141():
    fig, axs = plt.subplots(1, 2, figsize=(4.8, 2.45),
                            gridspec_kw=dict(width_ratios=[1.0, 1.16],
                                             wspace=0.10))

    # ---- (a) one-dimensional : one optical + one acoustic branch ----------
    ax = axs[0]
    _skeleton_141(ax, 1.05, nu_left=True)
    x = np.linspace(-0.5, 0.5, 500)
    ax.plot(x, 0.55 + 0.44 * np.cos(np.pi * x), color='black', lw=1.3)
    ax.plot(x, 0.30 * np.sin(np.pi * np.abs(x)), color='black', lw=1.3)
    ax.text(0.30, 0.795, 'Optical', fontsize=10, ha='center')
    ax.text(0.285, 0.135, 'Acoustic', fontsize=10, ha='center')
    ax.text(0, -0.145, '$(a)$', fontsize=11, ha='center', va='top')

    # ---- (b) three-dimensional : three optical + three acoustic ----------
    ax = axs[1]
    _skeleton_141(ax, 1.05)
    x = np.linspace(-0.5, 0.5, 500)
    c2 = np.cos(np.pi * x)**2
    s1 = np.sin(np.pi * np.abs(x))
    for e, p in [(0.63, 1.00), (0.55, 0.955), (0.34, 0.72)]:
        ax.plot(x, e + (p - e) * c2, color='black', lw=1.3)
    for a in (0.33, 0.20, 0.11):
        ax.plot(x, a * s1, color='black', lw=1.3)
    # vertical (vertical-transition) arrows at O onto the optical branches
    for xo, h in [(-0.014, 0.99), (0.0, 0.945), (0.014, 0.71)]:
        arrow(ax, xo, 0, xo, h, lw=1.0, ms=7)
    ax.text(0, -0.145, '$(b)$', fontsize=11, ha='center', va='top')

    save(fig, '141')


# ----------------------------------------------------------------------------
# Fig. 142  (p.270)  Multiphonon absorption:  hbar*omega = hbar*nu_optical
#                    - hbar*nu_acoustic.
# ----------------------------------------------------------------------------
def fig_142():
    fig, ax = plt.subplots(figsize=(3.5, 3.65))
    ax.axis('off')
    ax.set_xlim(-0.62, 0.66)
    ax.set_ylim(-0.18, 1.18)
    ax.set_aspect('equal')

    for x in (-0.5, 0.5):
        ax.plot([x, x], [0, 0.84], color='black', lw=1.0)
    ax.plot([-0.5, 0.5], [0, 0], color='black', lw=1.0)
    ax.text(-0.5, -0.06, 'Z.B.', fontsize=10, ha='center', va='top')
    ax.text(0.5, -0.06, 'Z.B.', fontsize=10, ha='center', va='top')
    ax.text(0, -0.06, '$O$', fontsize=11, ha='center', va='top')
    ax.text(0.155, -0.06, '$q$', fontsize=11, ha='right', va='top')
    arrow(ax, 0.175, -0.058, 0.33, -0.058, lw=0.9, ms=7)
    arrow(ax, 0, 0, 0, 1.09, lw=0.9, ms=8)
    ax.text(0.03, 1.09, r'$\nu$', fontsize=11, ha='left', va='bottom')

    x = np.linspace(-0.5, 0.5, 500)
    c2 = np.cos(np.pi * x)**2
    s1 = np.sin(np.pi * np.abs(x))
    branches = [(0.90, 1.00), (0.75, 0.86), (0.70, 0.79)]      # optical
    acoustic = [0.49, 0.375, 0.25]                             # acoustic
    for e, p in branches:
        ax.plot(x, e + (p - e) * c2, color='black', lw=1.3)
    for a in acoustic:
        ax.plot(x, a * s1, color='black', lw=1.3)

    def opt(i, q):
        e, p = branches[i]
        return e + (p - e) * np.cos(np.pi * q)**2

    q1, q2 = 0.16, 0.28

    # nu_optical : vertical arrow onto the 2nd optical branch at q1
    h1 = opt(1, q1)
    arrow(ax, q1, 0, q1, h1 - 0.008, lw=1.1, ms=8)
    ax.text(q1 + 0.022, 0.44, r'$\nu_{\rm optical}$', fontsize=10,
            ha='left', va='center')
    # dashed level linking nu_optical to the photon arrow
    arrow(ax, q1, h1, q2 - 0.006, h1, lw=0.8, ms=6, ls=(0, (4, 2.5)))

    # photon omega : thick vertical arrow onto the top branch at q2
    h2 = opt(0, q2)
    arrow(ax, q2, 0, q2, h2 - 0.006, lw=2.0, ms=9)
    ax.text(q2 + 0.026, 0.60, r'$\omega$', fontsize=11, ha='left')

    # nu_acoustic : small arrow onto the top acoustic branch (on omega shaft)
    ha = acoustic[0] * np.sin(np.pi * q2)
    arrow(ax, q2, 0, q2, ha, lw=0.9, ms=7)
    ax.text(q2 + 0.026, 0.145, r'$\nu_{\rm acoustic}$', fontsize=10,
            ha='left', va='center')

    save(fig, '142')


# ----------------------------------------------------------------------------
# Fig. 143  (p.272)  Vertical interband transitions in a semiconductor.
# ----------------------------------------------------------------------------
def _bands_143():
    ck = [0.00, 0.08, 0.16, 0.24, 0.32, 0.42, 0.52, 0.62, 0.70,
          0.78, 0.86, 1.00]
    cy = [0.771, 0.762, 0.759, 0.775, 0.829, 0.815, 0.745, 0.668,
          0.62, 0.578, 0.560, 0.555]
    vk = [0.00, 0.10, 0.20, 0.36, 0.50, 0.667, 0.85, 1.00]
    vy = [0.506, 0.455, 0.415, 0.365, 0.300, 0.247, 0.222, 0.212]
    return smooth(ck, cy), smooth(vk, vy)


def fig_143():
    fig, ax = plt.subplots(figsize=(3.6, 3.75))
    ax.axis('off')
    ax.set_xlim(-0.36, 1.05)
    ax.set_ylim(-0.10, 1.13)
    ax.set_aspect('equal')

    (kt, ct), (vt_, vt) = _bands_143()

    # conduction band (stippled in the original -> light grey)
    ax.fill_between(kt, ct, 1.125, facecolor='0.84', edgecolor='none',
                    zorder=1)
    ax.plot(kt, ct, color='black', lw=1.3, zorder=3)
    # valence band (hatched)
    ax.fill_between(vt_, 0, vt, facecolor='white', edgecolor='none',
                    hatch='////', zorder=1)
    ax.plot(vt_, vt, color='black', lw=1.3, zorder=3)

    # frame: energy axis, baseline, zone boundary
    ax.plot([0, 0], [-0.04, 1.00], color='black', lw=1.0)
    arrow(ax, 0, 1.00, 0, 1.07, lw=1.0, ms=9)
    ax.text(-0.025, 1.05, r'$\mathcal{E}$', fontsize=11, ha='right')
    ax.plot([0, 1.0], [0, 0], color='black', lw=1.0)
    arrow(ax, 0.66, 0, 0.74, 0, lw=0.8, ms=7)
    ax.plot([1.0, 1.0], [0, 1.02], color='black', lw=1.0)
    ax.text(0, -0.055, '$O$', fontsize=11, ha='center', va='top')
    ax.text(0.76, -0.055, '$k$', fontsize=11, ha='center', va='top')
    ax.text(1.0, -0.055, 'Z.B.', fontsize=10, ha='center', va='top')

    # vertical interband transitions
    def bandval(t, ks, ys):
        return np.interp(t, ks, ys)
    for k0 in (0.087, 0.367, 0.667, 0.90):
        y0 = bandval(k0, vt_, vt)
        y1 = bandval(k0, kt, ct)
        arrow(ax, k0, y0, k0, y1 - 0.006, lw=1.2, ms=8)
    # excited electron (dot above the 3rd arrow)
    ax.add_patch(plt.Circle((0.664, 0.72), 0.013, color='black', zorder=6))
    ax.text(0.70, 0.45, r'$\hbar\omega$', fontsize=11, ha='left')

    # labels with leader arrow
    ax.text(-0.33, 0.265, 'Valence\nband', fontsize=10, ha='left', va='center')
    arrow(ax, -0.075, 0.247, 0.135, 0.247, lw=0.8, ms=7)
    ax.text(0.50, 0.965, 'Conduction band', fontsize=10, ha='center',
            bbox=dict(facecolor='white', edgecolor='none', pad=1.5))

    save(fig, '143')


# ----------------------------------------------------------------------------
# Fig. 144  (p.274)  (a) Direct transitions do not necessarily give energy
#                    gap;  (b) phonon-assisted transition.
# ----------------------------------------------------------------------------
def _brace_right(ax, x, y0, y1, w=0.035):
    """small curly brace opening to the left (tip pointing at x)."""
    ym = 0.5 * (y0 + y1)
    t = np.linspace(0, 1, 100)
    up = y0 + (ym - y0) * t
    dn = ym + (y1 - ym) * t
    bulge = w * np.sin(np.pi * t)
    # end hooks
    ax.plot([x, x + 0.5 * bulge[1]], [y0, up[1]], color='black', lw=0.9)
    ax.plot([x, x + 0.5 * bulge[1]], [y1, dn[-1] * 0 + y1 - (dn[-1] - dn[-2])],
            color='black', lw=0.9)
    # two arcs meeting at the middle tip
    ax.plot(x + bulge, up, color='black', lw=0.9)
    ax.plot(x + bulge, dn, color='black', lw=0.9)
    ax.plot([x + w, x], [ym, ym], color='black', lw=0.9)


def _panel144(ax, gap=0.37):
    ax.axis('off')
    ax.set_xlim(-0.06, 1.24)
    ax.set_ylim(-0.11, 1.10)
    ax.set_aspect('equal')

    ck = [0.00, 0.06, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.72, 0.82, 1.00]
    cy = [0.97, 0.965, 0.925, 0.795, 0.625, 0.485, 0.405, 0.375, 0.370,
          0.383, 0.405]
    vk = [0.00, 0.05, 0.12, 0.25, 0.40, 0.55, 0.70, 1.00]
    vy = [0.300, 0.312, 0.313, 0.27, 0.155, 0.065, 0.028, 0.018]
    kt, ct = smooth(ck, cy)
    vt_, vt = smooth(vk, vy)

    ax.fill_between(kt, ct, 1.095, facecolor='0.84', edgecolor='none',
                    zorder=1)
    ax.plot(kt, ct, color='black', lw=1.3, zorder=3)
    ax.fill_between(vt_, 0, vt, facecolor='white', edgecolor='none',
                    hatch='////', zorder=1)
    ax.plot(vt_, vt, color='black', lw=1.3, zorder=3)

    ax.plot([0, 0], [-0.04, 0.99], color='black', lw=1.0)
    arrow(ax, 0, 0.99, 0, 1.055, lw=1.0, ms=8)
    ax.text(-0.022, 1.035, r'$\mathcal{E}$', fontsize=11, ha='right')
    ax.plot([0, 1.0], [0, 0], color='black', lw=1.0)
    ax.plot([1.0, 1.0], [0, 1.005], color='black', lw=1.0)
    ax.text(0, -0.055, '$O$', fontsize=11, ha='center', va='top')
    ax.text(0.48, -0.055, '$k$', fontsize=11, ha='center', va='top')
    ax.text(1.0, -0.055, 'Z.B.', fontsize=10, ha='center', va='top')
    return kt, ct, vt_, vt


def fig_144():
    fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.7),
                            gridspec_kw=dict(wspace=0.30))

    def bandval(t, ks, ys):
        return np.interp(t, ks, ys)

    # ---- (a) direct transition:  hbar*omega_0 > E_gap ---------------------
    ax = axs[0]
    kt, ct, vt_, vt = _panel144(ax)
    ax.plot([0, 1.0], [0.37, 0.37], color='black', lw=0.8, ls=(0, (5, 3)),
            zorder=2)
    ax.plot([0, 1.0], [0.30, 0.30], color='black', lw=0.8, ls=(0, (5, 3)),
            zorder=2)
    k0 = 0.30
    arrow(ax, k0, bandval(k0, vt_, vt), k0, bandval(k0, kt, ct) - 0.006,
          lw=1.3, ms=8)
    ax.text(k0 + 0.035, 0.335, r'$\hbar\omega_0$', fontsize=11, ha='left')
    ax.text(-0.022, 0.30, r'$\mathcal{E}_v$', fontsize=11, ha='right',
            va='center')
    _brace_right(ax, 1.015, 0.30, 0.37)
    ax.text(1.115, 0.335, r'$\mathcal{E}_{\rm gap}$', fontsize=11,
            ha='left', va='center')
    ax.text(0.42, -0.145, '$(a)$', fontsize=11, ha='center', va='top')

    # ---- (b) phonon-assisted transition -----------------------------------
    ax = axs[1]
    kt, ct, vt_, vt = _panel144(ax)
    ax.plot([0, 1.0], [0.30, 0.30], color='black', lw=0.8, ls=(0, (5, 3)),
            zorder=2)
    ax.plot([0.055, 1.0], [0.37, 0.37], color='black', lw=0.8,
            ls=(0, (5, 3)), zorder=2)
    k0 = 0.055
    arrow(ax, k0, bandval(k0, vt_, vt), k0, bandval(k0, kt, ct) - 0.006,
          lw=1.5, ms=8)
    ax.text(-0.022, 0.30, r'$\mathcal{E}_v$', fontsize=11, ha='right',
            va='center')
    _brace_right(ax, 0.075, 0.30, 0.37)
    ax.text(0.145, 0.335, r'$\hbar\omega$', fontsize=11, ha='left',
            va='center')
    # phonon wave vector q : dashed relaxation path to the band minimum
    ks = np.linspace(k0, 0.72, 300)
    off = 0.030 * np.sin(np.pi * (ks - k0) / (0.72 - k0))**0.7
    ax.plot(ks, bandval(ks, kt, ct) + off, color='black', lw=1.0,
            ls=(0, (5, 3)), zorder=4)
    ax.annotate('', xy=(0.72, 0.372), xytext=(0.70, bandval(0.70, kt, ct) + 0.012),
                arrowprops=dict(arrowstyle='-|>', color='black', lw=1.0,
                                mutation_scale=8, shrinkA=0, shrinkB=0))
    ax.text(0.40, 0.66, '$q$', fontsize=11, ha='center')
    ax.text(0.42, -0.145, '$(b)$', fontsize=11, ha='center', va='top')

    save(fig, '144')


if __name__ == '__main__':
    for fn in (fig_136, fig_137, fig_138, fig_139, fig_140,
               fig_141, fig_142, fig_143, fig_144):
        fn()
