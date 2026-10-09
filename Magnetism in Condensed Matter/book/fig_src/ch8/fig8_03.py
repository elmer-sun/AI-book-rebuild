# -*- coding: utf-8 -*-
# 图 8.3 稀释磁性合金 (AuFe) 自旋玻璃：场冷/零场冷磁化率尖峰（Nagata 等 1997 改编）
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.4, 3.5)

# ---------- (a) FC, 2.02% ----------
t1 = np.linspace(4.5, 13, 40)
c1 = 6.50 + 0.012 * (t1 - 4.5)
t2 = np.linspace(13, 14.5, 20)
c2 = 6.60 + 0.10 * ((t2 - 13) / 1.5) ** 1.5
t3 = np.linspace(14.5, 27, 60)
c3 = 3.7 + 3.0 * ((27 - t3) / 12.5) ** 1.35
Ta = np.concatenate([t1, t2, t3]); ca = np.concatenate([c1, c2, c3])

# ---------- (b) ZFC, 2.02% ----------
tb = np.linspace(4.6, 14.5, 45)
cb = 6.70 - 1.0 * ((14.5 - tb) / 9.9) ** 1.7

# ---------- (c) FC, 1.08% ----------
t4 = np.linspace(4.5, 9.5, 30)
c4 = 4.60 + 0.012 * (t4 - 4.5)
t5 = np.linspace(9.5, 10.3, 12)
c5 = 4.66 + 0.14 * ((t5 - 9.5) / 0.8) ** 1.5
t6 = np.linspace(10.3, 27, 60)
c6 = 1.9 + 2.9 * ((27 - t6) / 16.7) ** 1.15
Tc = np.concatenate([t4, t5, t6]); cc = np.concatenate([c4, c5, c6])

# ---------- (d) ZFC, 1.08% ----------
td = np.linspace(4.5, 10.3, 35)
cd = 4.80 - 1.05 * ((10.3 - td) / 5.8) ** 1.7

ax.plot(Ta, ca, 'k-o', ms=2.8, mfc='k', lw=1.0, markevery=(0, 3))
ax.plot(tb, cb, 'k-o', ms=2.8, mfc='k', lw=1.0, markevery=(1, 3))
ax.plot(Tc, cc, 'k-o', ms=2.8, mfc='k', lw=1.0, markevery=(2, 3))
ax.plot(td, cd, 'k-o', ms=2.8, mfc='k', lw=1.0, markevery=(0, 3))

# axis-break slashes near the origin
ax.plot([1.8, 2.6], [-0.16, 0.16], 'k-', lw=0.8, clip_on=False)
ax.plot([2.6, 3.4], [-0.16, 0.16], 'k-', lw=0.8, clip_on=False)

# reversibility (double) arrows on FC low-T plateaux, warming arrows on ZFC
ax.annotate('', xy=(10.0, 6.16), xytext=(6.0, 6.16),
            arrowprops=dict(arrowstyle='<->', lw=0.9))
ax.annotate('', xy=(8.5, 4.26), xytext=(5.5, 4.26),
            arrowprops=dict(arrowstyle='<->', lw=0.9))
ax.annotate('', xy=(10.8, 6.45), xytext=(10.8, 5.80),
            arrowprops=dict(arrowstyle='->', lw=0.9))
ax.annotate('', xy=(8.6, 4.55), xytext=(8.6, 4.00),
            arrowprops=dict(arrowstyle='->', lw=0.9))

ax.text(5.2, 6.85, '(a)', fontsize=11, ha='center')
ax.text(6.0, 5.28, '(b)', fontsize=11, ha='center')
ax.text(5.0, 4.90, '(c)', fontsize=11, ha='center')
ax.text(5.9, 3.34, '(d)', fontsize=11, ha='center')
ax.text(26.7, 4.55, '2.02%', fontsize=10, ha='right')
ax.text(26.7, 1.35, '1.08%', fontsize=10, ha='right')

ax.set_xlim(0, 28)
ax.set_ylim(0, 7.35)
ax.set_xticks([5, 10, 15, 20, 25])
ax.set_yticks(range(0, 8))
ax.set_xlabel(r'$T$ (K)', fontsize=12, labelpad=1)
ax.set_ylabel(r'$\chi$ ($10^{-5}$ emu/g)', fontsize=12)

save_fig(fig, 'ch8', 'fig8_03')
