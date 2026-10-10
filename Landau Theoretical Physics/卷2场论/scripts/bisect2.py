# -*- coding: utf-8 -*-
"""实验B/C: 逐段加回，定位空隙元凶"""
import io, re
base = r'E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本'
s = io.open(base + r'\chapters\ch07.tex', encoding='utf-8').read()
lines = s.split('\n')
rest = '\n'.join(lines[976:])

# 解 段落（到 图13 minipage 之前）
m_jie = re.search(r'(\\noindent\{\\heiti 习题1\}.*?切出\..*?)\n\n(\\par\\nopagebreak\\noindent\\begin\{minipage\})', rest, re.S)
assert m_jie, 'jie fail'
jie_part = m_jie.group(1)

# fig13 minipage 块
m_fig = re.search(r'(\\par\\nopagebreak\\noindent\\begin\{minipage\}\{\\linewidth\}\\centering\\includegraphics\[width=4\.5cm\]\{fig13\.pdf\}.*?\\end\{minipage\}\\par\\nopagebreak)', rest, re.S)
assert m_fig, 'fig fail'
fig_part = m_fig.group(1)

head = '\n'.join(lines[:975])
xiti_start = lines[975]

which = io.open(base + r'\bisect_mode.txt', encoding='utf-8').read().strip()
if which == 'B':
    kept = xiti_start + '\n\n' + jie_part + '\n\\end{xiti}\n'
elif which == 'C':
    kept = xiti_start + '\n\n' + jie_part + '\n\n' + fig_part + '\n\\end{xiti}\n'
else:
    raise SystemExit('mode?')
io.open(base + r'\chapters\ch07_bisect.tex', 'w', encoding='utf-8').write(head + '\n' + kept)
print('mode', which, 'written')
