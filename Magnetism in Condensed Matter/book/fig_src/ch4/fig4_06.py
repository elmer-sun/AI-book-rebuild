# -*- coding: utf-8 -*-
# 图 4.6 单态-三重态模型：(a) Δ>0, (b) Δ<0 的塞曼分裂；(c) 磁化率
# χ = (2ng²μ_B²/k_BT)/(3+exp(Δ/k_BT))（Bleaney–Bowers 型公式）
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
from mplstyle import save_fig
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(4.6, 5.9))
gs = fig.add_gridspec(2, 2, height_ratios=[0.8, 1.45], hspace=0.10,
                      left=0.13, right=0.95, top=0.99, bottom=0.09)
axa = fig.add_subplot(gs[0, 0])
axb = fig.add_subplot(gs[0, 1])
axc = fig.add_subplot(gs[1, :])

for ax in (axa, axb):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

# ---------------- (a) Δ > 0 : S=0 ground state ----------------
o = (0.34, 0.64)
axa.plot([o[0], 0.74], [o[1], 0.84], 'k-', lw=1.2)
axa.plot([o[0], 0.82], [o[1], o[1]], 'k-', lw=1.2)
axa.plot([o[0], 0.74], [o[1], 0.44], 'k-', lw=1.2)
axa.text(0.76, 0.85, r'$g\mu_\mathrm{B}B$', ha='left', va='bottom')
axa.text(0.84, o[1], '0', ha='left', va='center')
axa.text(0.76, 0.43, r'$-g\mu_\mathrm{B}B$', ha='left', va='top')
axa.text(0.30, o[1], '$S=1$', ha='right', va='center')
axa.plot([o[0], 0.82], [0.14, 0.14], 'k-', lw=1.2)
axa.text(0.30, 0.14, '$S=0$', ha='right', va='center')
axa.text(0.84, 0.14, '0', ha='left', va='center')
axa.text(0.02, 0.95, '(a)', ha='left', va='top')

# ---------------- (b) Δ < 0 : S=1 ground state ----------------
o = (0.34, 0.30)
axb.plot([o[0], 0.82], [0.80, 0.80], 'k-', lw=1.2)
axb.text(0.30, 0.80, '$S=0$', ha='right', va='center')
axb.text(0.84, 0.80, '0', ha='left', va='center')
axb.plot([o[0], 0.74], [o[1], 0.50], 'k-', lw=1.2)
axb.plot([o[0], 0.82], [o[1], o[1]], 'k-', lw=1.2)
axb.plot([o[0], 0.74], [o[1], 0.10], 'k-', lw=1.2)
axb.text(0.76, 0.51, r'$g\mu_\mathrm{B}B$', ha='left', va='bottom')
axb.text(0.84, o[1], '0', ha='left', va='center')
axb.text(0.76, 0.09, r'$-g\mu_\mathrm{B}B$', ha='left', va='top')
axb.text(0.30, o[1], '$S=1$', ha='right', va='center')
axb.text(0.02, 0.95, '(b)', ha='left', va='top')

# ---------------- (c) susceptibility ----------------
x = np.linspace(0.01, 2.5, 3000)
y_plus = 2.0 / (x * (3.0 + np.exp(1.0 / x)))     # Δ>0
y_zero = 0.5 / x                                  # Δ=0
y_minus = 2.0 / (x * (3.0 + np.exp(-1.0 / x)))   # Δ<0

axc.axhline(0, color='k', lw=0.0)  # keep frame complete
axc.plot(x, y_plus, 'k-', lw=1.3, label=r'$\Delta>0$')
axc.plot(x, y_zero, 'k:', lw=1.4, label=r'$\Delta=0$')
axc.plot(x, y_minus, 'k--', lw=1.3, label=r'$\Delta<0$')
ipk = np.argmax(y_plus)
print('peak of Δ>0 curve: y=%.3f at kBT/|Δ|=%.3f' % (y_plus[ipk], x[ipk]))
print('Δ>0 at x=2.5: %.3f ; Δ=0 at 1: %.3f, at 2.5: %.3f ; Δ<0 at 1: %.3f'
      % (y_plus[-1], y_zero[np.argmin(abs(x-1))], y_zero[-1],
         y_minus[np.argmin(abs(x-1))]))

axc.set_xlim(0, 2.5)
axc.set_ylim(0, 1.02)
axc.set_xticks([0, 1, 2])
axc.set_yticks([0.0, 0.5, 1.0])
axc.set_xlabel(r'$k_\mathrm{B}T/|\Delta|$')
axc.set_ylabel(r'$\chi/(ng^2\mu_\mathrm{B}^2)$')
axc.text(0.04, 0.97, '(c)', transform=axc.transAxes, ha='left', va='top')

save_fig(fig, 'ch4', 'fig4_06')
