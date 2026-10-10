# -*- coding: utf-8 -*-
"""二分定位 p149 空隙：实验A - 保留xiti开头到习题1题干，删其余"""
import io, re
p = r'E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\chapters\ch07_bisect.tex'
s = io.open(r'E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\chapters\ch07.tex', encoding='utf-8').read()
lines = s.split('\n')
# xiti 在行976（索引975）
head = '\n'.join(lines[:975])
xiti_start = lines[975]          # \begin{xiti}
rest = '\n'.join(lines[976:])    # 空行 + \noindent{习题1}...
# 只保留到第一个题干结束（"透明的屏上切出."）
m = re.search(r'(\\noindent\{\\heiti 习题1\}.*?切出\.)', rest, re.S)
assert m, 'pattern fail'
kept = xiti_start + '\n\n' + m.group(1) + '\n\\end{xiti}\n'
io.open(p, 'w', encoding='utf-8').write(head + '\n' + kept)
print('ch07_bisect.tex written, xiti block reduced')
