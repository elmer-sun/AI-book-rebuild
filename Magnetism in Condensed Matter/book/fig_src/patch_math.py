# -*- coding: utf-8 -*-
"""给图源文件补 amsmath/bm（\boldsymbol 需要）"""
import glob
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)) + r'\ch1')
for f in glob.glob('fig1_0*.tex'):
    s = open(f, encoding='utf-8').read()
    if '\\usepackage{bm}' not in s:
        s = s.replace('\\usepackage{fontspec}',
                      '\\usepackage{amsmath}\n\\usepackage{bm}\n\\usepackage{fontspec}', 1)
        open(f, 'w', encoding='utf-8').write(s)
        print('patched', f)
