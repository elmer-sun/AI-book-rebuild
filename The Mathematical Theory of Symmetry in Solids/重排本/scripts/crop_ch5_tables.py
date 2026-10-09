# -*- coding: utf-8 -*-
"""第五章大表扫描裁剪：表5.1 与 5.2 节的 230 群表，并生成对应 tex 片段。"""
import os
from PIL import Image

SRC = r'E:\AI整理书籍\群论\直接识别_ch5\pages'
if not os.path.isdir(SRC):
    # ch5 可能未渲染，直接从章节 PDF 渲染
    from pathlib import Path
    SRC_NEW = r'E:\AI整理书籍\群论\直接识别_ch5\pages'
    os.makedirs(SRC_NEW, exist_ok=True)
    import pymupdf
    pdf = r'E:\AI整理书籍\群论\章节拆分\05_Single-Valued_Reps_230_Space_Groups_p238-430.pdf'
    doc = pymupdf.open(pdf)
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(dpi=183)
        pix.save(os.path.join(SRC_NEW, 'p%03d.png' % (238 + i)))
    SRC = SRC_NEW
    print('rendered ch5 pages:', len(doc))

DST = r'E:\AI整理书籍\群论\重排本\figures'
os.makedirs(DST, exist_ok=True)

def crop(pg, name, x0=0.05, x1=0.95, y0=0.03, y1=0.985, q=72, maxw=1180):
    im = Image.open(os.path.join(SRC, pg)).convert('RGB')
    W, H = im.size
    im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(os.path.join(DST, name), quality=q)
    return name

# 表 5.1：书 226–285 = 扫描 239–298
tex51 = []
for n in range(239, 299):
    f = crop('p%d.png' % n, 'c5_t51_p%02d.jpg' % (n - 238))
    part = n - 238
    cap = '\\textbf{表 5.1}（第 %d 页，共 60 页；原书第 %d 页）' % (part, n - 13)
    if part == 1:
        cap = '\\textbf{表 5.1}\\ 抽象群的定义关系、类、特征标表与矩阵代表（230 个空间群的表示表所需；原书扫描，第 %d 页，共 60 页）' % part
    tex51.append('\\begin{figure}[H]\n\\centering\n\\includegraphics[width=0.86\\textwidth]{%s}\n\\caption*{%s}\n\\end{figure}' % (f, cap))

# 5.2 表格页：书 286–388 = 扫描 299–401
tex52 = []
for n in range(299, 402):
    f = crop('p%d.png' % n, 'c5_52_p%03d.jpg' % n)
    tex52.append('\\begin{figure}[H]\n\\centering\n\\includegraphics[width=0.86\\textwidth]{%s}\n\\caption*{原书第 %d 页}\n\\end{figure}' % (f, n - 13))

io = open
with io(r'E:\AI整理书籍\群论\重排本\chapters\ch5_t51_figs.tex', 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(tex51))
with io(r'E:\AI整理书籍\群论\重排本\chapters\ch5_52_figs.tex', 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(tex52))
print('crops + tex done')
