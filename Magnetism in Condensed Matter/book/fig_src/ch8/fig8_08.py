# -*- coding: utf-8 -*-
# 图 8.8 KCuF3 中子散射（Tennant 等 1993）：(a) (E,Q) 轨迹与自旋子连续谱波瓣
#                                   (b) 能量扫描强度（空心圆+误差棒）与非磁背景（虚线）
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

fig, axes = plt.subplots(2, 1, figsize=(3.7, 4.9), sharex=True,
                         gridspec_kw=dict(height_ratios=[1.0, 1.25],
                                          hspace=0.04))
axa, axb = axes
fig.subplots_adjust(left=0.16, right=0.97, top=0.98, bottom=0.10)

# ================= (a) trajectory + continuum lobes =================
m = 4.08 / 75.0                                   # Q/pi per meV
E = np.linspace(0, 77, 10)
axa.plot(E, m * E, 'k-', lw=1.0)

# four continuum-boundary lobes hugging the Q axis, centred at Q/pi = 1..4
for k, Ek in [(1, 45), (2, 55), (3, 65), (4, 80)]:
    phi = np.linspace(0, np.pi, 150)
    axa.plot(Ek * np.sin(phi), k + 0.58 * np.cos(phi), 'k-', lw=1.0)

# bold segments 1,2,3 where the trajectory crosses the lobes
bold = [(18, 26), (35, 42), (50, 62)]
for (e1, e2), lab in zip(bold, ('1', '2', '3')):
    Em = np.linspace(e1, e2, 10)
    axa.plot(Em, m * Em, 'k-', lw=4.5, solid_capstyle='butt')
    axa.text((e1 + e2) / 2 - 1.5, m * (e1 + e2) / 2 + 0.30, lab, fontsize=11)

# arrows down into panel (b)
for (e1, e2), ye in zip(bold, (9.3, 5.6, 5.6)):
    Em = (e1 + e2) / 2
    axa.annotate('', xy=(Em, ye), xycoords=axb.transData,
                 xytext=(Em, m * Em - 0.10), textcoords=axa.transData,
                 arrowprops=dict(arrowstyle='-|>', lw=1.0, color='k'),
                 annotation_clip=False)

axa.set_xlim(0, 122)
axa.set_ylim(0, 4.15)
axa.set_yticks(range(0, 5))
axa.text(115, 3.72, '(a)', fontsize=11, ha='right')
axa.set_ylabel(r'$Q/\pi$', fontsize=12)
axa.tick_params(labelbottom=False)

# ================= (b) intensity scan =================
Ed = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
               18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
               34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
               50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65,
               67, 69, 71, 74, 77, 80, 84, 88, 92, 96, 100, 105, 110, 115, 119])
Id = np.array([9.5, 9.8, 10.2, 10.6, 10.4, 9.6, 8.0, 6.5, 5.8, 5.4, 5.5, 5.2,
               5.6, 6.2, 7.4, 8.8, 10.2, 11.6, 12.6, 13.1, 13.2, 13.0, 12.3,
               11.2, 9.8, 8.4, 7.2, 6.3, 5.5, 4.9, 4.6, 4.4, 4.5, 4.6, 4.7,
               4.9, 5.1, 5.3, 5.4, 5.4, 5.3, 5.1, 4.8, 4.4, 4.0, 3.8, 3.7,
               3.8, 3.9, 4.0, 4.2, 4.3, 4.4, 4.4, 4.5, 4.5, 4.6, 4.6, 4.6,
               4.5, 4.4, 4.2, 4.0, 3.8, 3.6, 3.5, 3.2, 3.0, 2.8, 2.5, 2.3,
               2.1, 1.9, 1.8, 1.7, 1.6, 1.5, 1.5, 1.4, 1.5, 1.4])
err = 0.35 + 0.25 * np.abs(np.sin(2.1 * Ed))
axb.errorbar(Ed, Id, yerr=err, fmt='o', mfc='white', mec='k', ms=3.5,
             ecolor='k', elinewidth=0.7, capsize=1.2, lw=0)

Eb = np.linspace(0, 120, 200)
axb.plot(Eb, 1.65 + 3.45 * np.exp(-Eb / 38.0), 'k--', lw=0.9, dashes=(4, 3))

axb.set_ylim(0, 15.3)
axb.set_yticks([0, 5, 10])
axb.set_xticks(range(0, 121, 20))
axb.set_xlim(0, 122)
axb.text(115, 13.9, '(b)', fontsize=11, ha='right')
axb.set_xlabel(r'Energy Transfer (meV)', fontsize=12, labelpad=1)
axb.set_ylabel(r'Intensity (abs. units)', fontsize=12)

save_fig(fig, 'ch8', 'fig8_08')
