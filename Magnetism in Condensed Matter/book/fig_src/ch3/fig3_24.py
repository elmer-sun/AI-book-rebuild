# -*- coding: utf-8 -*-
# Fig 3.24 Larmor frequencies: f = (gamma/2pi) B on log-log axes for electron,
# muon and proton; right axis shows the corresponding period tau = 1/f
# (reversed scale), top axis the field in gauss.
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.6, 4.3)
fig.subplots_adjust(left=0.13, right=0.87, top=0.90, bottom=0.11)

B = np.logspace(-5, 1, 200)
ax.loglog(B, 2.80e4 * B, color='black', lw=1.1)      # electron  28.0 GHz/T
ax.loglog(B, 1.355e2 * B, color='black', lw=1.1)     # muon      135.5 MHz/T
ax.loglog(B, 4.258e1 * B, color='black', lw=1.1)     # proton    42.58 MHz/T

ax.set_xlim(1e-5, 10)
ax.set_ylim(1e-3, 1e3)
# dotted grid at each decade and at the 2 and 5 positions (as in the print)
ax.grid(True, which='major', ls=':', lw=0.55, color='0.55')
ax.grid(False, which='minor')
for e in range(-6, 2):
    for m in (2, 5):
        x = m * 10.0 ** e
        if 1e-5 < x < 10:
            ax.axvline(x, ls=':', lw=0.35, color='0.75')
        y = m * 10.0 ** e
        if 1e-3 < y < 1e3:
            ax.axhline(y, ls=':', lw=0.35, color='0.75')
ax.set_xlabel(r'$B$ (T)')
ax.set_ylabel(r'$f$ (MHz)')

# labels along the lines (square log canvas -> 45 degrees)
for x0, g, lab in [(4.5e-4, 2.80e4, 'electron'),
                   (1.8e-3, 1.355e2, 'muon'),
                   (3.2e-2, 4.258e1, 'proton')]:
    ax.text(x0, g * x0, lab, rotation=45, ha='center', va='center',
            fontsize=11, bbox=dict(fc='white', ec='none', pad=1.0))

# top axis: B in gauss
tax = ax.secondary_xaxis('top', functions=(lambda x: x * 1e4,
                                           lambda x: x / 1e4))
tax.set_xticks([1, 10, 100, 1000, 1e4, 1e5])
tax.set_xlabel(r'$B$ (G)')
# right axis: tau = 1/f in microseconds (increases downward)
rax = ax.secondary_yaxis('right', functions=(lambda f: 1.0 / f,
                                             lambda tau: 1.0 / tau))
rax.set_yticks([1e-2, 1e-1, 1, 10, 100])
rax.set_yticklabels(['0.01', '0.1', '1', '10', '100'])
rax.set_ylabel(r'$\tau$ ($\mu$s)')

save_fig(fig, 'ch3', 'fig3_24')
