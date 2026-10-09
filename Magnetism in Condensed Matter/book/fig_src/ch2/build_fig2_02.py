# -*- coding: utf-8 -*-
"""Fig 2.2: molar diamagnetic susceptibility of ions vs Z_eff r^2 (log-log).
Ring positions extracted pixel-wise from the original scan; values match
standard ionic susceptibilities to a few percent."""
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

# ion: (log10 x [Z_eff r^2 / m^2], log10 y [|chi_m| / m^3/mol],
#       dx, dy, ha)  label offsets in decades, measured from the scan
IONS = [
    ('Li',  -20.153, -11.058,  0.060, -0.012, 'left'),
    ('Mg',  -19.379, -10.271,  0.075, -0.050, 'left'),
    ('Na',  -19.077, -10.117,  0.056, -0.021, 'left'),
    ('Ca',  -19.093,  -9.872,  0.072,  0.003, 'left'),
    ('F',   -18.845,  -9.930,  0.064, -0.008, 'left'),
    ('K',   -18.737,  -9.738,  0.060,  0.008, 'left'),
    ('Cl',  -18.580,  -9.518,  0.068, -0.019, 'left'),
    ('Sr',  -18.557,  -9.632,  0.060, -0.005, 'left'),
    ('Rb',  -18.329,  -9.563,  0.066,  0.004, 'left'),
    ('Ba',  -18.441,  -9.441,  0.062, -0.011, 'left'),
    ('Cs',  -18.265,  -9.360, -0.015,  0.080, 'center'),
    ('Br',  -18.159,  -9.368,  0.054, -0.012, 'left'),
    ('I',   -18.058,  -9.202,  0.035, -0.032, 'left'),
]

fig, ax = new_fig(4.0, 3.75)

# dotted slope-1 line (from the scan: log y = log x + 8.95)
xl = np.array([-21.3, -17.8])
ax.plot(xl, xl + 8.95, ls=':', color='k', lw=1.1, zorder=1)

for sym, lx, ly, dx, dy, ha in IONS:
    ax.plot(lx, ly, 'o', ms=4.0, mfc='white', mec='k', mew=0.8,
            ls='none', zorder=3)
    if sym in ('Li', 'Na', 'K', 'Rb', 'Cs'):
        ch = '+'
    elif sym in ('F', 'Cl', 'Br', 'I'):
        ch = '-'
    else:
        ch = '2+'
    s = r'$%s^{%s}$' % (sym, ch)
    ax.text(lx + dx, ly + dy, s, ha=ha, va='center', fontsize=7.5, zorder=4)

ax.set_xlim(-21.30, -17.82)
ax.set_ylim(-11.20, -8.95)
ax.set_xticks([-20, -19, -18])
ax.set_xticklabels([r'$10^{-20}$', r'$10^{-19}$', r'$10^{-18}$'])
ax.set_yticks([-11, -10, -9])
ax.set_yticklabels([r'$10^{-11}$', r'$10^{-10}$', r'$10^{-9}$'])
xt_min = [np.log10(m) - 21 for m in range(2, 10)] + \
         [np.log10(m) - 20 for m in range(2, 10)] + \
         [np.log10(m) - 19 for m in range(2, 10)]
yt_min = [np.log10(m) - 11 for m in range(2, 10)] + \
         [np.log10(m) - 10 for m in range(2, 10)]
ax.set_xticks(xt_min, minor=True)
ax.set_yticks(yt_min, minor=True)
ax.tick_params(labelsize=9)
ax.set_xlabel(r'$Z_\mathrm{eff}\ r^2\ \ (\mathrm{m}^2)$')
ax.set_ylabel(r'$\chi_m\ \ (\mathrm{m}^3\,\mathrm{mol}^{-1})$')

save_fig(fig, 'ch2', 'fig2_02')
