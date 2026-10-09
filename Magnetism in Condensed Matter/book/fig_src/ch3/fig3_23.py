# -*- coding: utf-8 -*-
# Fig 3.23 muSR: (a) layout of the mu+ beam, sample S, forward/back detectors,
# transverse field H (into page); (b) back/forward count rates N_B (dotted) and
# N_F (solid) oscillating in opposite phase about their smooth average (dashed);
# (c) asymmetry A(t) = a0 exp(-lambda t) cos(w_mu t).
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
from mplstyle import save_fig

plt.rcParams.update({'hatch.linewidth': 0.7})

fig = plt.figure(figsize=(5.2, 4.9))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.92],
                      left=0.03, right=0.985, top=0.985, bottom=0.05,
                      wspace=0.24, hspace=0.30)

# ---------------- (a) schematic ----------------
axa = fig.add_subplot(gs[0, :])
axa.set_xlim(0, 4.0)
axa.set_ylim(0, 1.95)
axa.set_aspect('equal')
axa.axis('off')

axa.text(0.05, 1.80, '(a)', fontsize=11)
# mu+ stop point and spin direction (initial spin opposite to beam)
axa.add_patch(Circle((0.42, 0.95), 0.075, fc='black', ec='black'))
axa.text(0.42, 1.14, r'$\mu^+$', ha='center', fontsize=11)
axa.annotate('', xy=(0.03, 0.95), xytext=(0.33, 0.95),
             arrowprops=dict(arrowstyle='-|>', lw=1.3, color='black'))
# beam arrow to the sample
axa.annotate('', xy=(1.93, 0.95), xytext=(0.55, 0.95),
             arrowprops=dict(arrowstyle='-|>', lw=1.3, color='black'))
# sample
axa.add_patch(Circle((2.16, 0.95), 0.17, fc='white', ec='black', lw=0.9))
axa.text(2.16, 0.95, 'S', ha='center', va='center', fontsize=11)
# detectors: back (B) on the left, forward (F) on the right
for (x0, y0, lab) in [(1.18, 1.30, 'B'), (2.72, 1.30, 'F'),
                      (1.12, 0.12, 'B'), (2.68, 0.12, 'F')]:
    axa.add_patch(Rectangle((x0, y0), 0.58, 0.58, fc='white', ec='black',
                            hatch='///', lw=0.8))
    axa.text(x0 + 0.29, y0 + 0.29, lab, ha='center', va='center', fontsize=11,
             bbox=dict(fc='white', ec='none', pad=1.2))
# transverse field into the page
axa.text(2.16, 0.52, r'$\otimes$', ha='center', va='center', fontsize=13)
axa.text(2.16, 0.16, r'$H$', ha='center', va='center', fontsize=11, style='italic')

# ---------------- (b) count rates ----------------
axb = fig.add_subplot(gs[1, 0])
t = np.linspace(0, 8, 800)
tau, a0, om = 3.5, 0.45, 2 * np.pi * 0.10
avg = np.exp(-t / tau) / (1 + a0)
NB = avg * (1 + a0 * np.cos(om * t))
NF = avg * (1 - a0 * np.cos(om * t))
axb.plot(t, NB, ls=':', lw=1.6, color='black')
axb.plot(t, NF, ls='-', lw=1.2, color='black')
axb.plot(t, avg, ls='--', lw=0.9, color='0.45')
axb.set_xlim(0, 8.6)
axb.set_ylim(-0.05, 1.32)
axb.axis('off')
# bottom axis with arrow, label t
axb.annotate('', xy=(8.6, -0.05), xytext=(0, -0.05),
             arrowprops=dict(arrowstyle='-|>', lw=0.8, color='black'))
axb.text(8.62, -0.05, r'$t$', fontsize=11, va='center')
axb.text(0.12, 1.14, '(b)', fontsize=11)
axb.text(2.55, 1.00, r'$N_{\rm B}(t)$', fontsize=11)
axb.plot([2.50, 1.42], [0.97, 0.60], lw=0.6, color='black')
axb.text(3.35, 0.62, r'$N_{\rm F}(t)$', fontsize=11)
axb.plot([3.30, 2.45], [0.60, 0.335], lw=0.6, color='black')

# ---------------- (c) asymmetry ----------------
axc = fig.add_subplot(gs[1, 1])
t2 = np.linspace(0, 5.5, 600)
A = 0.92 * np.exp(-t2 / 7.5) * np.cos(2 * np.pi * 0.55 * t2)
axc.plot(t2, A, lw=1.2, color='black')
axc.set_xlim(-0.25, 6.35)
axc.set_ylim(-1.35, 1.95)
axc.axis('off')
axc.annotate('', xy=(6.35, 0), xytext=(-0.25, 0),
             arrowprops=dict(arrowstyle='-|>', lw=0.8, color='black'))
axc.annotate('', xy=(0, 1.45), xytext=(0, -1.35),
             arrowprops=dict(arrowstyle='-|>', lw=0.8, color='black'))
axc.text(6.40, -0.13, r'$t$', fontsize=11)
axc.text(-0.15, 1.58, r'$A(t)$', fontsize=11)
axc.text(-0.9, 1.80, '(c)', fontsize=11)

save_fig(fig, 'ch3', 'fig3_23')
