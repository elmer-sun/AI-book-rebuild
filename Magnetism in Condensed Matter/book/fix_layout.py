# -*- coding: utf-8 -*-
import re

# 1) ch7: 修复 \b 退格损坏
s = open('ch7.tex', encoding='utf-8').read()
bs = chr(8)
if bs in s:
    s = s.replace(bs + 'aselineskip', chr(92) + 'baselineskip')
    print('ch7 backspace repaired')
open('ch7.tex', 'w', encoding='utf-8').write(s)
print('ch7 line:', [l for l in open('ch7.tex', encoding='utf-8') if 'enlargethispage' in l])

# 2) appA: 表加 [!ht]
a = open('appA.tex', encoding='utf-8').read()
n = a.count(chr(92) + 'begin{table}' + chr(123) + chr(125))
if n == 0:
    a = a.replace(chr(92) + 'begin{table}', chr(92) + 'begin{table}[!ht]')
    open('appA.tex', 'w', encoding='utf-8').write(a)
print('appA:', [l.strip() for l in open('appA.tex', encoding='utf-8') if 'begin{table}' in l])

# 3) main.tex: 浮动页顶对齐（\@fptop=0）
m = open('main.tex', encoding='utf-8').read()
marker = chr(92) + 'makeatletter'
fix = (chr(92) + 'makeatletter\n'
       + chr(92) + 'setlength{' + chr(92) + '@fptop}{0pt}\n'
       + chr(92) + 'setlength{' + chr(92) + '@fpbot}{0pt plus 1fil}\n'
       + chr(92) + 'makeatother')
if '@fptop' not in m:
    # 插在 \makeatletter 现有块之前（\cleardoublepage 重定义块前）
    idx = m.find(marker)
    m = m[:idx] + fix + '\n' + m[idx:]
    open('main.tex', 'w', encoding='utf-8').write(m)
    print('main.tex fptop fix added')
else:
    print('main.tex already has fptop')
