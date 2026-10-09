# -*- coding: utf-8 -*-
"""Blundell 中译本重绘统一 matplotlib 样式。
用法：
    import sys; sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
    from mplstyle import new_fig, save_fig
    fig, ax = new_fig()          # 单面板，宽约 4.6in
    ...
    save_fig(fig, 'ch5', 'fig5_09')   # 存 figs/fig5_09.pdf + 预览 PNG
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'Times New Roman',
    'mathtext.fontset': 'stix',
    'font.size': 11,
    'axes.linewidth': 0.8,
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.top': True,
    'ytick.right': True,
    'xtick.major.size': 3.5,
    'ytick.major.size': 3.5,
    'xtick.minor.size': 2.0,
    'ytick.minor.size': 2.0,
    'lines.linewidth': 1.2,
    'legend.frameon': False,
    'legend.fontsize': 10,
    'figure.dpi': 120,
})

ROOT = r'E:\AI整理书籍\磁学\book'


def new_fig(w=4.6, h=3.4):
    """单面板图；多面板用 plt.subplots(w=..)或 subplots 自行建。"""
    return plt.subplots(figsize=(w, h))


def save_fig(fig, chapter, name):
    """存 PDF 到 figs/ 并渲染 3x 预览 PNG 到 fig_src/<chapter>/。"""
    import os
    import pymupdf
    pdf = os.path.join(ROOT, 'figs', name + '.pdf')
    fig.savefig(pdf)
    plt.close(fig)
    d = pymupdf.open(pdf)
    pix = d[0].get_pixmap(matrix=pymupdf.Matrix(3, 3), alpha=False)
    pix.save(os.path.join(ROOT, 'fig_src', chapter, name + '.png'))
    d.close()
    print('saved', pdf)
