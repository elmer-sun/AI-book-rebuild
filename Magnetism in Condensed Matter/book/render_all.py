# -*- coding: utf-8 -*-
"""渲染全书页面 PNG 到 render/ 目录，供视觉评审"""
import io, os, sys
import pymupdf

os.chdir(r'E:\AI整理书籍\磁学\book')
os.makedirs('render', exist_ok=True)
doc = pymupdf.open('main.pdf')
n = doc.page_count
step = int(sys.argv[1]) if len(sys.argv) > 1 else 1
count = 0
for i in range(0, n, step):
    pix = doc[i].get_pixmap(matrix=pymupdf.Matrix(1.35, 1.35))
    pix.save('render/p%03d.png' % (i + 1))
    count += 1
print('rendered', count, 'of', n, 'pages')
