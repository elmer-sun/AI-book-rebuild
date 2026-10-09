# -*- coding: utf-8 -*-
"""删除图注中的英文行（{\footnotesize\itshape Fig.~x.y ...}），只留中文图注。
统计并报告每文件删除数；正文中专有名词括号英文不受影响。"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

FILES = ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8',
         'appB', 'appC', 'appD']

# 形如：\\[可选空行]{\footnotesize\itshape Fig.~x.y ...}}   紧贴 \end{figure}
pat = re.compile(
    r'\\\\\s*\{\s*\\footnotesize\s*\\itshape\s*Fig\.~.*\}\}\s*(?=\\end\{figure\})',
    re.S)

total = 0
for f in FILES:
    if not os.path.exists(f + '.tex'):
        continue
    s = open(f + '.tex', encoding='utf-8').read()
    s2, n = pat.subn('', s)
    if n:
        open(f + '.tex', 'w', encoding='utf-8').write(s2)
    print('%-6s removed %d' % (f, n))
    total += n
print('TOTAL', total)
