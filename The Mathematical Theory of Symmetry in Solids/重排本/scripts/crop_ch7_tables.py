# -*- coding: utf-8 -*-
"""第七章扫描裁剪：7.2 的表 7.1-7.4、7.3 的表 7.5-7.7、7.5/7.6/7.7 的共表示表。"""
import os
from PIL import Image

SRC = r'E:\AI整理书籍\群论\直接识别_ch7\pages'
if not os.path.isdir(SRC) or len(os.listdir(SRC)) < 110:
    os.makedirs(SRC, exist_ok=True)
    import pymupdf
    pdf = r'E:\AI整理书籍\群论\章节拆分\07_Magnetic_Groups_Corepresentations_p582-694.pdf'
    doc = pymupdf.open(pdf)
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(dpi=183)
        pix.save(os.path.join(SRC, 'p%03d.png' % (582 + i)))
    print('rendered', len(doc))

DST = r'E:\AI整理书籍\群论\重排本\figures'

def crop(pg, name, x0=0.05, x1=0.95, y0=0.03, y1=0.985, q=72, maxw=1180):
    im = Image.open(os.path.join(SRC, pg)).convert('RGB')
    W, H = im.size
    im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(os.path.join(DST, name), quality=q)

groups = [
    # (输出tex, 起扫描页, 止扫描页(含), 首页cap)
    ('ch7_72_figs.tex', 603, 630, '\\textbf{表 7.1}--7.4 与图 7.1--7.4：Shubnikov 群的推导与分类（原书第 590--617 页扫描）'),
    ('ch7_73_figs.tex', 641, 643, '\\textbf{表 7.5}--7.7：共表示的基本表示与因子系统（原书第 628--630 页扫描）'),
    ('ch7_75_figs.tex', 649, 663, '\\textbf{7.5 节的共表示表}：磁点群的不可约共表示（原书第 636--650 页扫描）'),
    ('ch7_76_figs.tex', 665, 677, '\\textbf{7.6 节的共表示表}：磁空间群的不可约共表示（原书第 652--664 页扫描）'),
    ('ch7_77_figs.tex', 679, 694, '\\textbf{7.7 节的表}：$P4\'_{2}/mnm\'$ 的共表示及其直积（原书第 666--689 页扫描）'),
]
for texname, a, b, firstcap in groups:
    out = []
    for n in range(a, b + 1):
        f = 'c7_p%03d.jpg' % n
        crop('p%d.png' % n, f)
        cap = '原书第 %d 页' % (n - 13)
        if n == a:
            cap = firstcap
        out.append('\\begin{figure}[H]\n\\centering\n\\includegraphics[width=0.86\\textwidth]{%s}\n\\caption*{%s}\n\\end{figure}' % (f, cap))
    with open(os.path.join(r'E:\AI整理书籍\群论\重排本\chapters', texname), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(out))
print('ch7 crops + tex done')
