# -*- coding: utf-8 -*-
"""7.6 答案段 F 系列编号最终校正：文档顺序 103,104,105,106,107"""
import io, re

p = r'E:\AI整理书籍\磁学\book\answers.tex'
s = io.open(p, encoding='utf-8').read()
B = chr(92)
i = s.find(B + 'exer{7.6}')
head, tail = s[:i], s[i:]

n = [103]
def rep(m):
    v = n[-1]
    n.append(v + 1)
    return B + 'tag{F.%d}' % v

tail = re.sub(r'' + re.escape(B) + r'tag\{F\.\d+\}', rep, tail)
# 最后一个无编号的 I 分段情形补 F.107
old = ('I = ' + B + 'begin{cases}' if B + 'begin{cases}' in tail else None)
# 找到 "最终 I cases" 的位置：第二个 cases 块（I = {...} q>2kF / q<2kF）
parts = tail.split(B + 'end{cases}')
if len(parts) >= 3:
    # 在最后一个 end{cases} 后补 \tag{F.107}
    tail = B + 'end{cases}'.join(parts[:-1]) + B + 'end{cases}' + B + 'tag{F.107}' + parts[-1]

s = head + tail
io.open(p, 'w', encoding='utf-8').write(s)
tags = re.findall(r'tag' + B + '{F.([0-9]+)' + B + '}', s)
print('last 8 F tags:', ','.join(tags[-8:]))
