# -*- coding: utf-8 -*-
"""Redraw Ziman, Principles of the Theory of Solids, 2nd ed., Chapter 6
figures 109, 110, 111, 119, 120, 121 (black-and-white textbook style)."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, Polygon, FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'figures')
PREV = os.path.join(OUT, 'preview')
os.makedirs(PREV, exist_ok=True)

DASH = (0, (4, 3))        # generic dashed
LDASH = (0, (5, 4))       # long dashed (band edges, level lines)


def save(fig, key):
    fig.savefig(os.path.join(OUT, f'fig_{key}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, f'fig_{key}.png'), bbox_inches='tight', pad_inches=0.03, dpi=200)
    plt.close(fig)
    print('saved fig', key)


def arrow(ax, xy0, xy1, lw=1.1, ms=11, ls='-', rad=0.0):
    """small solid-head arrow"""
    p = dict(arrowstyle='-|>', color='k', lw=lw, mutation_scale=ms,
             shrinkA=0, shrinkB=0)
    if rad:
        p['connectionstyle'] = f'arc3,rad={rad}'
    if ls != '-':
        p['linestyle'] = ls
    ax.annotate('', xy=xy1, xytext=xy0, arrowprops=p)


def electron(ax, x, y, ms=4.4):
    ax.plot([x], [y], 'ko', markersize=ms, zorder=6)


def hole(ax, x, y, r=0.024, ms=6.0):
    """open circle with a horizontal stroke through it"""
    ax.plot([x - 2.4 * r, x + 2.4 * r], [y, y], 'k-', lw=1.0, zorder=6)
    ax.plot([x], [y], marker='o', ms=ms, mfc='white', mec='k', mew=1.0,
            ls='', zorder=7)


def electron_stroked(ax, x, y, r=0.020, ms=5.0):
    """filled dot with a horizontal stroke through it (Fig. 110)"""
    ax.plot([x - 2.4 * r, x + 2.4 * r], [y, y], 'k-', lw=1.0, zorder=6)
    ax.plot([x], [y], 'ko', markersize=ms, zorder=7)


def cr_spline(pts, n=22, closed=False):
    """Catmull-Rom smooth spline through points."""
    pts = np.asarray(pts, float)
    if closed:
        P = np.vstack([pts[-1], pts, pts[0], pts[1]])
        segs = range(1, len(P) - 2)
    else:
        P = np.vstack([pts[0], pts, pts[-1]])
        segs = range(1, len(P) - 2)
    out = []
    for i in segs:
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(pts[-1])
    return np.array(out)


# ----------------------------------------------------------------------
def fig_109():
    """Donor/acceptor levels: occupation, recombination, thermal excitation."""
    fig, axs = plt.subplots(1, 3, figsize=(4.6, 2.0))

    def bands(ax):
        # conduction band (stippled in the book -> light grey)
        ax.add_patch(Rectangle((0, 0.66), 1.0, 0.36, facecolor='0.80',
                               edgecolor='0.80', lw=0.5))
        ax.plot([0, 1], [0.66, 0.66], 'k-', lw=1.5)          # band edge
        ax.plot([0, 1], [0.615, 0.615], 'k-', linestyle=DASH, lw=1.1)   # donors
        ax.plot([0, 1], [0.36, 0.36], 'k-', linestyle=DASH, lw=1.1)     # acceptors
        ax.add_patch(Rectangle((0, 0), 1.0, 0.31, facecolor='white',
                               edgecolor='k', lw=1.2, hatch='///'))  # valence
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.22, 1.04)
        ax.axis('off')

    # (a) both kinds of level occupied
    ax = axs[0]
    bands(ax)
    for xd in np.arange(0.06, 0.85, 0.145):
        electron(ax, xd, 0.615)
    for xa in (0.14, 0.48, 0.82):
        hole(ax, xa, 0.36)
    ax.text(0.5, -0.16, '($a$)', ha='center', va='center')

    # (b) electrons and holes have combined
    ax = axs[1]
    bands(ax)
    for xd in (0.36, 0.63):
        electron(ax, xd, 0.615)
    ax.text(0.5, -0.16, '($b$)', ha='center', va='center')

    # (c) excess electrons thermally excited into the conduction band
    ax = axs[2]
    bands(ax)
    y = 0.82
    electron(ax, 0.26, y)
    arrow(ax, (0.30, y), (0.44, y), lw=1.2, ms=12)
    electron(ax, 0.52, y)
    arrow(ax, (0.56, y), (0.72, y), lw=1.2, ms=12)
    ax.text(0.5, -0.16, '($c$)', ha='center', va='center')

    fig.subplots_adjust(wspace=0.10, left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 109)


# ----------------------------------------------------------------------
def fig_110():
    """Exciton states: bound electron-hole pair in the gap."""
    fig, ax = plt.subplots(figsize=(3.6, 2.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.02)
    ax.axis('off')

    ax.add_patch(Rectangle((0.05, 0.71), 0.90, 0.29, facecolor='0.80',
                           edgecolor='0.80', lw=0.5))
    ax.plot([0.05, 0.95], [0.71, 0.71], 'k-', lw=1.6)
    ax.add_patch(Rectangle((0.05, 0.0), 0.90, 0.40, facecolor='white',
                           edgecolor='k', lw=1.4, hatch='///'))

    # dashed capsule binding electron to hole
    ax.add_patch(FancyBboxPatch((0.4415, 0.418), 0.077, 0.288,
                                boxstyle='round,pad=0.007,rounding_size=0.018',
                                facecolor='none', edgecolor='k', lw=1.3,
                                linestyle=DASH, zorder=4))
    electron_stroked(ax, 0.480, 0.648, r=0.014)
    hole(ax, 0.480, 0.437, r=0.017, ms=5.5)

    save(fig, 110)


# ----------------------------------------------------------------------
def fig_111():
    """(a) Wannier exciton  (b) Frenkel exciton."""
    fig, ax = plt.subplots(figsize=(4.7, 2.75))
    ax.set_xlim(0, 4.7)
    ax.set_ylim(-0.35, 2.45)
    ax.set_aspect('equal')
    ax.axis('off')

    # ---- (a) Wannier exciton -------------------------------------
    C = np.array([1.02, 1.42])
    # irregular hatched blob (the crystal / sea of valence electrons)
    th = np.linspace(0, 2 * np.pi, 240)
    R = 0.92 * (1 + 0.055 * np.sin(3 * th + 0.7)
                + 0.030 * np.cos(5 * th + 2.1)
                + 0.020 * np.sin(7 * th))
    blob = Polygon(np.c_[C[0] + R * np.cos(th), C[1] + R * np.sin(th)],
                   closed=True, facecolor='white', edgecolor='k',
                   lw=1.1, hatch='///')
    ax.add_patch(blob)
    # Bohr orbit of the pair
    r_orb = 0.585
    thc = np.linspace(0, 2 * np.pi, 200)
    ax.plot(C[0] + r_orb * np.cos(thc), C[1] + r_orb * np.sin(thc), 'k-', lw=1.3)
    # sense-of-rotation arrowheads (counter-clockwise)
    for a in np.deg2rad([103, -52]):
        p = C + r_orb * np.array([np.cos(a), np.sin(a)])
        t = np.array([-np.sin(a), np.cos(a)])
        arrow(ax, p - 0.085 * t, p + 0.085 * t, lw=1.15, ms=12)
    # electron (-) and hole (+) on the orbit
    a_e, a_h = np.deg2rad(153), np.deg2rad(-27)
    pe = C + r_orb * np.array([np.cos(a_e), np.sin(a_e)])
    ph = C + r_orb * np.array([np.cos(a_h), np.sin(a_h)])
    electron(ax, *pe, ms=5.2)
    ax.plot([ph[0]], [ph[1]], marker='o', ms=6.5, mfc='white', mec='k',
            mew=1.1, ls='', zorder=7)
    ax.text(*(C + 0.76 * np.array([np.cos(a_e), np.sin(a_e)])), '$-$',
            ha='center', va='center')
    ax.text(*(C + 0.76 * np.array([np.cos(a_h), np.sin(a_h)])), '$+$',
            ha='center', va='center')
    # wave vector of the whole exciton
    arrow(ax, tuple(C), (C[0] + 1.13, C[1]), lw=1.2, ms=13)
    ax.text(C[0] + 0.86, C[1] + 0.09, r'$\mathbf{k}$', ha='center', va='bottom')
    ax.text(1.02, -0.22, '($a$)', ha='center', va='center')

    # ---- (b) Frenkel exciton -------------------------------------
    ra = 0.285
    sp = 0.62
    Cb = np.array([2.93 + sp, 0.78 + sp])       # central atom
    r_o = 0.52                                  # orbit, tucked behind atoms
    thc = np.linspace(0, 2 * np.pi, 200)
    orb_x = Cb[0] + r_o * np.cos(thc)
    orb_y = Cb[1] + r_o * np.sin(thc)
    for i in range(3):
        for j in range(3):
            c = (2.93 + i * sp, 0.78 + j * sp)
            ax.add_patch(Circle(c, ra, facecolor='white', edgecolor='k',
                                lw=1.4, hatch='///', zorder=3))
    ax.plot(orb_x, orb_y, 'k-', lw=1.4, zorder=2)
    a = np.deg2rad(125)                          # rotation arrowhead on orbit
    p = Cb + r_o * np.array([np.cos(a), np.sin(a)])
    t = np.array([-np.sin(a), np.cos(a)])
    arrow(ax, p - 0.08 * t, p + 0.08 * t, lw=1.2, ms=12)
    # excited electron on the orbit, hole left at the atom centre
    a = np.deg2rad(37)
    pe = Cb + r_o * np.array([np.cos(a), np.sin(a)])
    electron(ax, *pe, ms=5.2)
    ph = Cb + np.array([0.05, -0.05])
    ax.plot([ph[0]], [ph[1]], marker='o', ms=5.5, mfc='white', mec='k',
            mew=1.1, ls='', zorder=7)
    # the excitation jumps to the neighbouring atom (dashed arrows)
    far = FancyArrowPatch(tuple(pe + [0.03, -0.03]), (4.12, 1.495),
                          connectionstyle='arc3,rad=-0.25', arrowstyle='-|>',
                          mutation_scale=12, lw=1.15, color='k',
                          linestyle=DASH, zorder=5)
    ax.add_patch(far)
    far2 = FancyArrowPatch(tuple(ph + [0.02, -0.04]), (4.07, 1.16),
                           connectionstyle='arc3,rad=0.30', arrowstyle='-|>',
                           mutation_scale=12, lw=1.15, color='k',
                           linestyle=DASH, zorder=5)
    ax.add_patch(far2)
    ax.text(3.55, -0.22, '($b$)', ha='center', va='center')

    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 111)


# ----------------------------------------------------------------------
def fig_119():
    """Pseudo-atom form factor w_s(K); band structure samples it at g1, g2."""
    fig, ax = plt.subplots(figsize=(4.3, 3.5))
    ax.set_xlim(-0.36, 1.66)
    ax.set_ylim(-0.86, 0.42)
    ax.axis('off')

    # axes
    arrow(ax, (0, -0.83), (0, 0.37), lw=1.3, ms=13)
    arrow(ax, (-0.01, 0), (1.60, 0), lw=1.3, ms=13)
    ax.text(-0.24, 0.315, r'$\mathcal{E}$', ha='center', va='center')
    ax.text(1.585, -0.085, r'$K$', ha='center', va='center')
    ax.text(-0.035, 0.015, '0', ha='right', va='center')

    for g, lab in ((1.0, r'$\mathbf{g}_1$'), (1.22, r'$\mathbf{g}_2$')):
        ax.plot([g, g], [-0.014, 0.014], 'k-', lw=1.2)
        ax.text(g, -0.085, lab, ha='center', va='center')

    ax.text(-0.035, -0.667, r'$-\frac{2}{3}\mathcal{E}_F$',
            ha='right', va='center')

    K = np.linspace(0, 1.45, 300)
    w = 0.18 - 0.4275 * (1 - np.tanh((K - 0.72) / 0.30))
    ax.plot(K, w, 'k-', lw=1.7)

    # screened-out core contribution V'(K) (dashed): straight at small K,
    # then hugging w_s slightly above the plateau
    ax.plot([0.68, 0.965], [-0.205, 0.040], 'k-', linestyle=(0, (5, 3)), lw=1.25)
    K2 = np.linspace(0.965, 1.52, 120)
    w2 = 0.18 - 0.4275 * (1 - np.tanh((K2 - 0.60) / 0.30)) \
        + 0.014 * np.exp(-((K2 - 1.28) / 0.45) ** 2)
    ax.plot(K2, w2, 'k-', linestyle=(0, (5, 3)), lw=1.25)

    # values sampled at reciprocal lattice vectors
    for g in (1.0, 1.22):
        wg = 0.18 - 0.4275 * (1 - np.tanh((g - 0.72) / 0.30))
        ax.plot([g], [wg], marker='x', ms=6.5, mew=1.7, color='k', ls='')

    ax.text(1.30, 0.27, r"$\mathcal{V}'(K)$", ha='center', va='center')
    ax.text(0.80, -0.36, r'$w_s(K)$', ha='left', va='center')

    save(fig, 119)


# ----------------------------------------------------------------------
def fig_120():
    """Repeated-zone scheme: a U-process reduced to an N-process."""
    fig, ax = plt.subplots(figsize=(4.5, 2.4))
    ax.set_xlim(-0.07, 2.07)
    ax.set_ylim(-0.07, 1.07)
    ax.set_aspect('equal')
    ax.axis('off')

    # upper half of the Fermi-surface shape in one zone (u in [-0.035, 1])
    Pup = [(-0.035, 0.513), (0.0, 0.516), (0.03, 0.548), (0.065, 0.61),
           (0.105, 0.685), (0.155, 0.775), (0.215, 0.86), (0.28, 0.93),
           (0.35, 0.98), (0.42, 1.0), (0.49, 0.99), (0.56, 0.965),
           (0.63, 0.93), (0.70, 0.885), (0.765, 0.825), (0.825, 0.75),
           (0.875, 0.675), (0.92, 0.60), (0.955, 0.55), (0.98, 0.525),
           (1.0, 0.512)]
    up = cr_spline(Pup, n=14)
    lo = up[::-1].copy()
    lo[:, 1] = 1 - lo[:, 1]
    S1 = np.vstack([up, lo])                 # closed outline, zone 1
    S2 = S1 + np.array([1.0, 0.0])           # periodic copy, zone 2

    ax.add_patch(Polygon(S1, closed=True, facecolor='0.85', edgecolor='none'))
    ax.add_patch(Polygon(S2, closed=True, facecolor='0.85', edgecolor='none'))
    # boundary: solid inside the first zone, dashed in the repeated zone
    ax.plot(S1[:, 0], S1[:, 1], 'k-', lw=1.4)
    m = S2[:, 0] >= 0.9995
    ax.plot(S2[m, 0], S2[m, 1], 'k-', linestyle=(0, (5, 3)), lw=1.3)

    # zone outlines: first zone solid, repeat zone dashed
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor='none', edgecolor='k', lw=1.7))
    ax.plot([1, 2], [1, 1], 'k-', linestyle=(0, (6, 4)), lw=1.3)
    ax.plot([1, 2], [0, 0], 'k-', linestyle=(0, (6, 4)), lw=1.3)
    ax.plot([2, 2], [0, 1], 'k-', linestyle=(0, (6, 4)), lw=1.3)

    # reciprocal-lattice vector K (dotted mid-line, arrow pointing left)
    ax.plot([0, 1.13], [0.5, 0.5], 'k-', linestyle=(0, (1, 2)), lw=1.1)
    arrow(ax, (0.62, 0.5), (0.50, 0.5), lw=1.2, ms=13)
    ax.text(0.44, 0.545, r'$\mathbf{K}$', ha='center', va='bottom')

    # k' = k + q : the V-shaped dotted path inside the first zone
    ax.plot([0, 0.42, 1.0], [0.5, 0.435, 0.5], 'k-', linestyle=(0, (1, 2)), lw=1.1)
    arrow(ax, (0.21, 0.467), (0.285, 0.4565), lw=1.1, ms=11)
    arrow(ax, (0.60, 0.4505), (0.675, 0.4615), lw=1.1, ms=11)
    ax.text(0.20, 0.385, r"$\mathbf{k'}$", ha='center', va='center')
    ax.text(0.615, 0.385, r'$\mathbf{k}$', ha='center', va='center')

    # phonon wave vector q and final state k' just across the boundary
    ax.text(1.062, 0.556, r'$\mathbf{q}$', ha='left', va='bottom')
    kx = np.array([1.005, 1.12, 1.26, 1.40, 1.52])
    ky = np.array([0.498, 0.487, 0.4775, 0.4745, 0.4755])
    ks = cr_spline(np.c_[kx, ky], n=10)
    ax.plot(ks[:, 0], ks[:, 1], 'k-', linestyle=(0, (5, 3)), lw=1.15)
    arrow(ax, (1.42, 0.4747), (1.50, 0.4753), lw=1.15, ms=12)
    ax.text(1.42, 0.53, r"$\mathbf{k'}$", ha='center', va='bottom')

    save(fig, 120)


# ----------------------------------------------------------------------
def fig_121():
    """(a) density wave; (b) local Fermi level follows; (c) electrons flow
    back, Fermi level constant -> deformation potential."""
    fig = plt.figure(figsize=(4.3, 4.9))
    gs = fig.add_gridspec(3, 1, height_ratios=[1.15, 0.95, 0.80],
                          hspace=0.30, left=0.02, right=0.98,
                          top=0.99, bottom=0.01)

    # ---- (a) lattice density wave, electrons dotted around ----------
    ax = fig.add_subplot(gs[0])
    ax.set_xlim(-0.85, 4.85)
    ax.set_ylim(-1.0, 2.8)
    ax.set_aspect('equal')
    ax.axis('off')
    ra = 0.335
    for c in range(5):
        for r in range(3):
            ctr = (float(c), float(r))
            if c in (1, 3):      # displaced positions (dashed circles)
                dx = 0.30 if c == 1 else -0.30
                ax.add_patch(Circle((c + dx, r), ra, facecolor='none',
                                    edgecolor='k', lw=1.2, linestyle=DASH,
                                    zorder=2))
            ax.add_patch(Circle(ctr, ra, facecolor='white', edgecolor='k',
                                lw=1.6, hatch='///', zorder=3))
    dots = [(0.52, 1.52), (0.98, 1.40), (1.50, 1.50), (2.63, 1.94),
            (3.97, 1.44),
            (-0.50, 0.48), (2.60, 0.98), (3.32, 1.26), (3.50, 0.50),
            (-0.50, -0.48), (0.95, -0.62), (1.42, -0.16), (2.45, -0.10),
            (3.50, -0.16)]
    for d in dots:
        electron(ax, *d, ms=4.0)
    ax.text(2.74, 0.95, r'$e^-$', ha='left', va='center')
    ax.text(2.24, -0.55, r"$e'$", ha='center', va='center')
    ax.text(2.0, -0.88, '($a$)', ha='center', va='center')

    # ---- (b) local Fermi level raised or lowered --------------------
    ax = fig.add_subplot(gs[1])
    ax.set_xlim(-0.04, 1.06)
    ax.set_ylim(-0.18, 1.28)
    ax.axis('off')
    x = np.linspace(0, 1, 300)
    z = 1 - 0.28 * np.exp(-((x - 0.47) / 0.235) ** 2)
    ax.fill_between(x, 0, z, color='0.84', lw=0, zorder=1)
    ax.plot([0, 1], [0, 0], 'k-', lw=1.6, zorder=3)          # E(0) bottom
    ax.plot(x, z, 'k-', lw=1.5, zorder=3)                    # zeta(r) top
    ax.plot([0, 1], [0.85, 0.85], 'k-', linestyle=LDASH, lw=1.15, zorder=2)
    arrow(ax, (0.30, 1.10), (0.452, 0.905), lw=1.15, ms=11, rad=-0.28)
    electron(ax, 0.462, 0.845, ms=3.8)
    arrow(ax, (0.73, 1.115), (0.588, 0.92), lw=1.15, ms=11, rad=0.28)
    electron(ax, 0.578, 0.868, ms=3.8)
    ax.text(0.005, 1.13, r'$\zeta(\mathbf{r})$', ha='left', va='center')
    ax.text(0.01, 0.075, r'$\mathcal{E}(0)$', ha='left', va='center')
    ax.text(0.5, -0.15, '($b$)', ha='center', va='center')

    # ---- (c) electrons flow back: flat zeta, warped band edge -------
    ax = fig.add_subplot(gs[2])
    ax.set_xlim(-0.04, 1.30)
    ax.set_ylim(-0.22, 1.30)
    ax.axis('off')
    yb = 0.14 + 0.34 * np.exp(-((x - 0.5) / 0.26) ** 2)
    ax.fill_between(x, yb, 1.0, color='0.84', lw=0, zorder=1)
    ax.plot([0, 1], [1, 1], 'k-', lw=1.6, zorder=3)          # flat zeta
    ax.plot(x, yb, 'k-', lw=1.5, zorder=3)                   # warped edge
    ax.plot([0, 0], [yb[0], 1.0], 'k-', lw=1.3, zorder=3)
    ax.plot([1, 1], [yb[-1], 1.0], 'k-', lw=1.3, zorder=3)
    ax.plot([0, 1], [0.24, 0.24], 'k-', linestyle=LDASH, lw=1.15, zorder=2)
    ax.plot([1.012, 1.012], [yb[-1], 0.24], 'k-', lw=1.0, zorder=3)
    ax.text(1.045, 0.19, r'$\delta\mathcal{E}(\mathbf{r})$',
            ha='left', va='center')
    ax.text(0.0, 1.075, r'$\zeta$', ha='left', va='center')
    ax.text(0.5, -0.16, '($c$)', ha='center', va='center')

    save(fig, 121)


# ----------------------------------------------------------------------
if __name__ == '__main__':
    for f in (fig_109, fig_110, fig_111, fig_119, fig_120, fig_121):
        f()
