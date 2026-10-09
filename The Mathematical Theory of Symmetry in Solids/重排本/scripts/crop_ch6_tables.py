# -*- coding: utf-8 -*-
"""第六章大表扫描裁剪：6.5 节的 230 群双值表示表 + 6.1 的表 6.1/6.4/6.6 等。"""
import os
from PIL import Image

SRC = r'E:\AI整理书籍\群论\直接识别_ch6\pages'
DST = r'E:\AI整理书籍\群论\重排本\figures'

def crop(pg, name, x0=0.05, x1=0.95, y0=0.03, y1=0.985, q=72, maxw=1180):
    im = Image.open(os.path.join(SRC, pg)).convert('RGB')
    W, H = im.size
    im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    if im.width > maxw:
        im = im.resize((maxw, int(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(os.path.join(DST, name), quality=q)

# 6.5 的 230 群表：pg49-142 = 书 467-560 = 扫描 480-573（94 页）
tex65 = []
for n in range(480, 574):
    f = 'c6_65_p%03d.jpg' % n
    crop('p%d.png' % n, f)
    tex65.append('\\begin{figure}[H]\n\\centering\n\\includegraphics[width=0.86\\textwidth]{%s}\n\\caption*{原书第 %d 页}\n\\end{figure}' % (f, n - 13))
with open(r'E:\AI整理书籍\群论\重排本\chapters\ch6_65_figs.tex', 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(tex65))

# 6.1 的特征标表（表 6.1-6.4 区域）：pg2-18 = 扫描 433-449（17 页）
tex61 = []
for n in range(433, 450):
    f = 'c6_61_p%02d.jpg' % n
    crop('p%d.png' % n, f)
    cap = '原书第 %d 页' % (n - 13)
    if n == 433:
        cap = '\\textbf{表 6.1}\\ 双值点群的特征标表与矩阵代表（原书第 %d 页起扫描）' % (n - 13)
    tex61.append('\\begin{figure}[H]\n\\centering\n\\includegraphics[width=0.86\\textwidth]{%s}\n\\caption*{%s}\n\\end{figure}' % (f, cap))
with open(r'E:\AI整理书籍\群论\重排本\chapters\ch6_61_figs.tex', 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(tex61))

# 6.2 的对称适配函数表（表 6.5/6.6 区域）：pg19-35 = 扫描 450-466（17 页）
tex62 = []
for n in range(450, 467):
    f = 'c6_62_p%02d.jpg' % n
    crop('p%d.png' % n, f)
    cap = '原书第 %d 页' % (n - 13)
    if n == 450:
        cap = '\\textbf{表 6.5}\\ 双值点群的对称适配函数（原书第 %d 页起扫描）' % (n - 13)
    tex62.append('\\begin{figure}[H]\n\\centering\n\\includegraphics[width=0.86\\textwidth]{%s}\n\\caption*{%s}\n\\end{figure}' % (f, cap))
with open(r'E:\AI整理书籍\群论\重排本\chapters\ch6_62_figs.tex', 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(tex62))

# 6.3/6.4 之间的表 6.7-6.10：pg36-48 = 扫描 467-479（13 页）
tex63 = []
for n in range(467, 480):
    f = 'c6_63_p%02d.jpg' % n
    crop('p%d.png' % n, f)
    cap = '原书第 %d 页' % (n - 13)
    if n == 467:
        cap = '6.3 节的表（\\textbf{表 6.7}--6.10 等，原书第 %d 页起扫描）' % (n - 13)
    tex63.append('\\begin{figure}[H]\n\\centering\n\\includegraphics[width=0.86\\textwidth]{%s}\n\\caption*{%s}\n\\end{figure}' % (f, cap))
with open(r'E:\AI整理书籍\群论\重排本\chapters\ch6_63_figs.tex', 'w', encoding='utf-8', newline='\n') as fh:
    fh.write('\n'.join(tex63))

print('ch6 crops + tex done')
