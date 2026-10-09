# -*- coding: utf-8 -*-
"""编译 fig_src 下所有 standalone TikZ 图源文件：
xelatex 编译 -> PDF 拷入 figs/ -> 渲染 3x 预览 PNG 供目检。"""
import glob
import os
import shutil
import subprocess
import sys

import pymupdf

ROOT = r'E:\AI整理书籍\磁学\book'
only = sys.argv[1] if len(sys.argv) > 1 else ''  # 可传文件名过滤，如 fig1_0

tex_list = sorted(glob.glob(os.path.join(ROOT, 'fig_src', '**', '*.tex'),
                            recursive=True))
fail = 0
for tex in tex_list:
    name = os.path.splitext(os.path.basename(tex))[0]
    if only and only not in name:
        continue
    d = os.path.dirname(tex)
    r = subprocess.run(
        ['xelatex', '-interaction=nonstopmode', '-halt-on-error',
         os.path.basename(tex)],
        cwd=d, capture_output=True, text=True)
    pdf = os.path.join(d, name + '.pdf')
    if r.returncode != 0 or not os.path.exists(pdf):
        print('FAIL', name)
        print(r.stdout[-2500:])
        fail += 1
        continue
    shutil.copy(pdf, os.path.join(ROOT, 'figs', name + '.pdf'))
    doc = pymupdf.open(pdf)
    pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(3, 3), alpha=False)
    pix.save(os.path.join(d, name + '.png'))
    doc.close()
    print('OK', name)
if fail:
    sys.exit(1)
