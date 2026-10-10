# -*- coding: utf-8 -*-
"""把各章 \\begin{center}\\includegraphics...\\end{center} 图块包成不可分割 minipage"""
import re, glob, os

os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      '重排本', 'chapters'))
pat = re.compile(
    r'\\begin\{center\}\\includegraphics\[(width=[0-9.]+cm)\]\{(fig\d+\.pdf)\}\\\\(.*?)\\end\{center\}',
    re.S)
n_tot = 0
for f in sorted(glob.glob('ch0*.tex')):
    s = open(f, encoding='utf-8').read()
    s2, n = pat.subn(
        r'\\par\\nopagebreak\\noindent\\begin{minipage}{\\linewidth}\\centering'
        r'\\includegraphics[\1]{\2}\\[0.3em]\3\\end{minipage}\\par\\nopagebreak',
        s)
    if n:
        open(f, 'w', encoding='utf-8').write(s2)
    print(f, n)
    n_tot += n
print('total', n_tot)
