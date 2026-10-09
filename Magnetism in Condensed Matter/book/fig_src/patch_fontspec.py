# -*- coding: utf-8 -*-
"""给 ch1 图源文件补上 fontspec（standalone+tikz 不会自动加载）"""
import glob
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)) + r'\ch1')
for f in glob.glob('fig1_0*.tex'):
    s = open(f, encoding='utf-8').read()
    if 'fontspec' not in s:
        s = s.replace('\\setmainfont',
                      '\\usepackage{fontspec}\n\\setmainfont', 1)
        open(f, 'w', encoding='utf-8').write(s)
        print('patched', f)
