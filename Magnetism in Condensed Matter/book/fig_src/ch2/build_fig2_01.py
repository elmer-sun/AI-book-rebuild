# -*- coding: utf-8 -*-
"""Fig 2.1: RT mass susceptibility of the first 60 elements vs atomic number.
Data point-by-point extracted from the original scan (symlog axis:
5 decades up to +1e-5, linear gap, 2 decades down to -1e-7)."""
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

# (Z, symbol, chi in m^3/kg) from pixel extraction of the scan
DATA = [
    (1, 'H', -2.6e-8), (2, 'He', -6.1e-9), (3, 'Li', 6.4e-9),
    (4, 'Be', -1.29e-8), (5, 'B', -8.9e-9), (6, 'C', -6.2e-9),
    (7, 'N', -1.02e-8), (8, 'O', 1.45e-6), (10, 'Ne', -4.2e-9),
    (11, 'Na', 6.6e-9), (12, 'Mg', 7.0e-9), (13, 'Al', 8.3e-9),
    (14, 'Si', -1.6e-9), (15, 'P', -1.16e-8), (16, 'S', -6.3e-9),
    (18, 'Ar', -7.3e-9), (19, 'K', -6.1e-9), (20, 'Ca', 1.45e-8),
    (22, 'Ti', 1.62e-8), (23, 'V', 1.82e-8), (24, 'Cr', 4.1e-8),
    (25, 'Mn', 1.55e-7), (29, 'Cu', -1.1e-9), (30, 'Zn', -2.0e-9),
    (31, 'Ga', -3.0e-9), (32, 'Ge', -1.5e-9), (33, 'As', -3.9e-9),
    (34, 'Se', -4.0e-9), (36, 'Kr', -5.0e-9), (37, 'Rb', 2.7e-9),
    (38, 'Sr', -2.5e-9), (39, 'Y', 6.9e-8), (40, 'Zr', -5.9e-9),
    (41, 'Nb', 1.95e-8), (42, 'Mo', 5.0e-10), (44, 'Ru', 6.4e-9),
    (45, 'Rh', 1.45e-8), (46, 'Pd', 7.0e-8), (47, 'Ag', -2.6e-9),
    (48, 'Cd', -2.3e-9), (49, 'In', -1.4e-9), (50, 'Sn', -3.3e-9),
    (51, 'Sb', -1.15e-8), (52, 'Te', -4.0e-9), (53, 'I', -4.6e-9),
    (54, 'Xe', -4.3e-9), (55, 'Cs', -2.8e-9), (56, 'Ba', 1.16e-8),
    (57, 'La', 1.32e-8), (58, 'Ce', 1.94e-7), (59, 'Pr', 3.3e-7),
    (60, 'Nd', 4.8e-7),
]

def yplot(chi):
    """Symlog coordinate: decades from the zero line, sign-separated."""
    chi = np.asarray(chi, dtype=float)
    return np.sign(chi) * (np.log10(np.abs(chi)) + 10.0)

fig, ax = new_fig(4.9, 2.9)

Z = [d[0] for d in DATA]
chi = [d[2] for d in DATA]
y = yplot(chi)

# zero line separating para/dia
ax.axhline(0.0, color='k', lw=1.0)

# data points
ax.plot(Z, y, 'o', ms=3.8, color='k', zorder=3)

# element labels below each point
for z, sym, c in DATA:
    ax.text(z, yplot(c) - 0.32, sym, ha='center', va='top', fontsize=6.0)

# Fe Co Ni arrows just below the top frame
for z, name in [(26, 'Fe'), (27, 'Co'), (28, 'Ni')]:
    ax.annotate('', xy=(z, 5.0), xytext=(z, 4.52),
                arrowprops=dict(arrowstyle='-|>', color='k',
                                lw=0.8, mutation_scale=7,
                                shrinkA=0, shrinkB=0))
ax.text(27, 4.40, 'FeCoNi', ha='center', va='top', fontsize=6.0)

# para/dia region text
ax.text(1.6, 0.12, 'paramagnetic', ha='left', va='bottom', fontsize=8)
ax.text(1.6, -0.12, 'diamagnetic', ha='left', va='top', fontsize=8)

# axes
ax.set_xlim(0, 61)
ax.set_ylim(-3.05, 5.05)
ax.set_xticks(range(10, 61, 10))
ax.set_xticks(range(0, 61, 1), minor=True)
yt_maj, ytl = [], []
for t in (-5, -6, -7, -8, -9):          # positive decades
    yt_maj.append(t + 10)
    ytl.append(r'$+10^{%d}$' % t)
for t in (-9, -8, -7):                   # negative decades
    yt_maj.append(-(t + 10))
    ytl.append(r'$-10^{%d}$' % t)
ax.set_yticks(yt_maj)
ax.set_yticklabels(ytl)
yt_min = []
for t in (-5, -6, -7, -8, -9):
    for m in range(2, 10):
        yt_min.append(np.log10(m) + t + 10)
for t in (-9, -8, -7):
    for m in range(2, 10):
        yt_min.append(-(np.log10(m) + t + 10))
ax.set_yticks(yt_min, minor=True)
ax.set_xlabel('Atomic number')
ax.set_ylabel(r'Mass susceptibility (m$^3$ kg$^{-1}$)')

save_fig(fig, 'ch2', 'fig2_01')
