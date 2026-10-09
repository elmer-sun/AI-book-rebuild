# -*- coding: utf-8 -*-
"""补齐历史排版修正：ch2/ch3 宽表 \small、ch3 3.43 resizebox、漏掉的措辞修正"""
import io
import os

B = chr(92)
NL = chr(10)
BUILD = r'E:\AI整理书籍\磁学\recovery\build'

# ---- ch2：两张宽表加 \small
p = os.path.join(BUILD, 'ch2.tex')
s = io.open(p, encoding='utf-8').read()
for marker in ('tabular}{lccccccc}', 'tabular}{lcccccc}'):
    old = B + 'begin{' + marker
    new = B + 'small' + NL + B + 'begin{' + marker
    if new not in s and old in s:
        s = s.replace(old, new, 1)
        print('ch2 small <-', marker)
io.open(p, 'w', encoding='utf-8', newline=NL).write(s)

# ---- ch3：宽表 + 例3.3 表 + 3.43 resizebox
p = os.path.join(BUILD, 'ch3.tex')
s = io.open(p, encoding='utf-8').read()
old = B + 'begin{' + 'tabular}{lcccccccc}'
new = B + 'small' + NL + B + 'begin{' + 'tabular}{lcccccccc}'
if new not in s and old in s:
    s = s.replace(old, new, 1)
    print('ch3 small <- lcccccccc')
old = B + 'center' + NL + B + 'begin{tabular}{lccccc}'
new = B + 'center' + NL + B + 'small' + NL + B + 'begin{tabular}{lccccc}'
if new not in s and old in s:
    s = s.replace(old, new, 1)
    print('ch3 small <- lccccc')
# 3.43 align* -> center+resizebox
lines = s.split(NL)
for i, l in enumerate(lines):
    if 'tag{3.43}' in l:
        j = i
        while 'begin{align*}' not in lines[j]:
            j -= 1
        k = i
        while 'end{align*}' not in lines[k]:
            k += 1
        block = NL.join(lines[j:k + 1])
        inner = (block.replace(B + 'begin{align*}', '')
                 .replace(B + 'end{align*}', '').strip(NL))
        newblock = (B + 'begin{center}' + NL
                    + B + 'resizebox{0.88' + B + 'textwidth}{!}{$'
                    + B + 'begin{aligned}' + NL + inner + NL
                    + B + 'end{aligned}$}' + NL
                    + B + 'end{center}')
        s = s.replace(block, newblock)
        print('ch3 3.43 -> resizebox')
        break
lines = s.split(NL)
io.open(p, 'w', encoding='utf-8', newline=NL).write(s)

# ---- ch3 漏掉的措辞修正（复查）
fixes = [
    ('singly occupied' + B, '单占据的' + B),
    ('更energetic（更高频）的光子给出更大信号', '能量更高（频率更高）的光子给出更大信号'),
    ('最energetic正电子的角分布', '能量最高的正电子的角分布'),
    ('但不久体力好的领先、 others 落后', '但不久体力好的渐渐领先，其余的人渐渐落后'),
    ('（ recall ' + B + 'B_0' + B + ' 沿 ' + B + 'z' + B + ' 轴）',
     '（回顾 ' + B + 'B_0' + B + ' 沿 ' + B + 'z' + B + ' 轴）'),
]
for old, new in fixes:
    if old in s:
        s = s.replace(old, new)
        print('ch3 措辞 <-', old[:30])
io.open(p, 'w', encoding='utf-8', newline=NL).write(s)
print('done')
