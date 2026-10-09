# -*- coding: utf-8 -*-
# Fig 3.25 Crystal field + magnetic field: a level splits into an upper doublet
# {|0>, (|2>+|-2>)/sqrt2} at +6A and a lower triplet {|1>,|-1>,(|2>-|-2>)/sqrt2}
# at -4A about the dotted barycentre (2 x 6A = 3 x 4A keeps the centre of gravity);
# in a field B the |+/-2> combinations repel (level repulsion), |0> stays flat,
# |+/-1> shift linearly.
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.9, 4.35)
fig.subplots_adjust(left=0.03, right=0.99, top=0.99, bottom=0.03)
ax.set_xlim(-0.3, 12.1)
ax.set_ylim(-0.1, 10.6)
ax.axis('off')

E0, Eu, El = 5.35, 8.35, 2.35      # barycentre, upper and lower zero-field levels

# ---------- zero-field part ----------
ax.plot([0.2, 1.7], [E0, E0], color='black', lw=1.1)
ax.plot([1.7, 2.9], [E0, Eu], color='black', lw=0.9)
ax.plot([1.7, 2.9], [E0, El], color='black', lw=0.9)
ax.plot([2.05, 2.78], [E0, E0], ls=':', color='black', lw=0.9)
ax.plot([2.9, 4.3], [Eu, Eu], color='black', lw=3.0)
ax.plot([2.9, 4.3], [El, El], color='black', lw=3.0)
# 6A / 4A double arrows
ax.annotate('', xy=(3.35, Eu), xytext=(3.35, E0),
            arrowprops=dict(arrowstyle='<|-|>', lw=0.8, color='black',
                            mutation_scale=9))
ax.annotate('', xy=(3.35, E0), xytext=(3.35, El),
            arrowprops=dict(arrowstyle='<|-|>', lw=0.8, color='black',
                            mutation_scale=9))
ax.text(3.22, 6.95, r'$6A$', ha='right', fontsize=11)
ax.text(3.22, 3.72, r'$4A$', ha='right', fontsize=11)

# ---------- field part ----------
X = np.linspace(4.3, 9.3, 300)
x = X - 4.3
kr, kf = 0.544, 0.647   # repulsion strength for rising / falling branch
lift_up = np.sqrt((Eu - E0) ** 2 + (kr * x) ** 2) - (Eu - E0)
lift_dn = np.sqrt((E0 - El) ** 2 + (kf * x) ** 2) - (E0 - El)
Eplus = Eu + lift_up    # |2>+|-2>  (rises with upward curvature)
Eminus = El - lift_dn   # |2>-|-2>  (falls with downward curvature)
ax.plot(X, Eplus, color='black', lw=1.2)
ax.plot(X, Eminus, color='black', lw=1.2)
# |0> flat (member of the upper doublet)
ax.plot([4.3, 9.3], [Eu, Eu], color='black', lw=1.1)
# |+/-1> linear
ax.plot([4.3, 9.3], [El, 3.85], color='black', lw=1.1)
ax.plot([4.3, 9.3], [El, 1.30], color='black', lw=1.1)
# B axis
ax.annotate('', xy=(9.9, 0.18), xytext=(6.0, 0.18),
            arrowprops=dict(arrowstyle='-|>', lw=0.8, color='black'))
ax.text(10.05, 0.18, r'$B$', fontsize=11, va='center')

# state labels
ax.text(9.45, 9.80, r'$|2\rangle+|{-2}\rangle$', fontsize=11, va='center')
ax.text(9.45, Eu, r'$|0\rangle$', fontsize=11, va='center')
ax.text(9.45, 3.85, r'$|1\rangle$', fontsize=11, va='center')
ax.text(9.45, 1.30, r'$|-1\rangle$', fontsize=11, va='center')
ax.text(9.45, 0.88, r'$|2\rangle-|{-2}\rangle$', fontsize=11, va='top')

save_fig(fig, 'ch3', 'fig3_25')
