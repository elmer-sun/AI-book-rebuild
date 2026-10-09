# -*- coding: utf-8 -*-
# Fig 3.26 Paramagnetic saturation (after Henry 1952): magnetic moment per ion
# vs B/T for Gd3+ (J=7/2), Fe3+ (J=5/2) and Cr3+ (J=3/2), all g=2.
# Smooth Brillouin curves M = gJ J B_J(x), x = gJ mu_B J (B/T) / kB,
# with simulated 1.3 K (x) and 4.2 K (o) data points scattered about them.
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
from mplstyle import new_fig, save_fig

MU_B_OVER_K = 0.6717   # mu_B / kB  in K/T


def brillouin(x, J):
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    nz = np.abs(x) > 1e-9
    a = (2 * J + 1) * x[nz] / (2 * J)
    b = x[nz] / (2 * J)
    out[nz] = (2 * J + 1) / (2 * J) / np.tanh(a) - 1 / (2 * J) / np.tanh(b)
    out[~nz] = 0.0
    return out


def moment(y, J, g=2.0):
    return g * J * brillouin(g * MU_B_OVER_K * J * y, J)


ions = [('Gd$^{3+}$', 3.5, 7.0, 2.30, 6.42),
        ('Fe$^{3+}$', 2.5, 5.0, 2.35, 4.50),
        ('Cr$^{3+}$', 1.5, 3.0, 2.60, 2.50)]

fig, ax = new_fig(4.2, 4.9)
fig.subplots_adjust(left=0.15, right=0.97, top=0.97, bottom=0.115)

y = np.linspace(0, 4, 500)
rng = np.random.default_rng(7)
for lab, J, sat, lx, ly in ions:
    ax.plot(y, moment(y, J), color='black', lw=1.3)
    # simulated data points: x = 1.3 K over the whole range, o = 4.2 K at low B/T
    yx = np.array([0.06, 0.12, 0.22, 0.35, 0.55, 0.8, 1.15, 1.6, 2.2, 3.0, 4.0])
    yx = yx * (0.9 + 0.2 * rng.random(yx.size))
    yx[0] = 0.06
    yx[-1] = 4.0
    mx = moment(yx, J) * (1 + 0.02 * rng.standard_normal(yx.size))
    yo = np.linspace(0.15, 1.3, 8) * (0.85 + 0.3 * rng.random(8))
    yo = np.sort(np.clip(yo, 0.12, 1.3))
    mo = moment(yo, J) * (1 + 0.02 * rng.standard_normal(yo.size))
    ax.plot(yx, mx, 'x', color='black', ms=5.5, mew=1.3, fillstyle='none')
    ax.plot(yo, mo, 'o', color='black', ms=5.0, mfc='none', mew=1.2)
    ax.text(lx, ly, lab, fontsize=11)

ax.set_xlim(0, 4)
ax.set_ylim(0, 7)
ax.set_xticks(range(5))
ax.set_yticks(range(8))
ax.set_xlabel(r'$(B/T)$ (tesla/kelvin)')
ax.set_ylabel('Magnetic moment\n(Bohr magnetons/ion)')

handles = [Line2D([], [], marker='x', ls='none', color='black', ms=5.5,
                  mew=1.3, label='T = 1.3K'),
           Line2D([], [], marker='o', ls='none', color='black', ms=5.0,
                  mfc='none', mew=1.2, label='T = 4.2K')]
ax.legend(handles=handles, loc='lower right', bbox_to_anchor=(0.98, 0.06),
          handletextpad=0.4)

save_fig(fig, 'ch3', 'fig3_26')
