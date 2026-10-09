# -*- coding: utf-8 -*-
# 图 8.6 Néel 弛豫时间 tau/tau0 = exp(KV/kBT)：双对数理论曲线（式 8.1）
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.4, 3.6)

x = np.logspace(np.log10(0.05), 2, 500)
ax.loglog(x, np.exp(1.0 / x), 'k-', lw=1.2)

ax.set_xlim(0.05, 100)
ax.set_ylim(1, 1e12)
ax.set_xticks([0.1, 1, 10, 100])
ax.set_yticks(10.0 ** np.arange(0, 13))
ax.set_xlabel(r'$k_BT/KV$', fontsize=12, labelpad=1)
ax.set_ylabel(r'$\tau/\tau_0$', fontsize=12)

save_fig(fig, 'ch8', 'fig8_06')
