# -*- coding: utf-8 -*-
"""实验D: 整块恢复(应复现63pt) 实验E: 整块但去\footnote"""
import io, re
base = r'E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本'
s = io.open(base + r'\chapters\ch07.tex', encoding='utf-8').read()
lines = s.split('\n')
head = '\n'.join(lines[:975])
block = '\n'.join(lines[975:1070])   # \begin{xiti} .. \end{xiti}
mode = io.open(base + r'\bisect_mode.txt', encoding='utf-8').read().strip()
if mode == 'E':
    block = re.sub(r'\\footnote\{[^{}]*\}', '', block)
    block = re.sub(r'\\footnote\{(?:[^{}]|\{[^{}]*\})*\}', '', block)
io.open(base + r'\chapters\ch07_bisect.tex', 'w', encoding='utf-8').write(head + '\n' + block + '\n')
print('mode', mode, 'written')
