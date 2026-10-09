# -*- coding: utf-8 -*-
"""Attach remaining two footnotes."""
import io

BS = chr(92)
TS = BS + 'textsuperscript'
FN = BS + 'footnote'

def patch(p, old, new):
    s = io.open(p, encoding='utf-8').read()
    assert old in s, (p, old[:50])
    s = s.replace(old, new, 1)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

patch('chapters/ch1_s2.tex',
 '式 (1.2.5) 保证了定义 1.2.13 的规则 (i)–(iii) 成立。' + TS + '{' + BS + 'ddag}',
 '式 (1.2.5) 保证了定义 1.2.13 的规则 (i)–(iii) 成立。' + FN + '{群 $' + BS + 'mathbf{H}$ 与 $' + BS + 'mathbf{G}$ 的子群 $' + BS + "mathbf{H}'$（由一切 $(H, E)$，$H " + BS + 'in ' + BS + "mathbf{H}$，组成）同构。若同样定义 $" + BS + "mathbf{K}'$，则按定义 1.2.13 严格地说我们得到的是 $" + BS + "mathbf{G} = " + BS + "mathbf{H}' " + BS + "otimes " + BS + "mathbf{K}'$；但由于 $" + BS + "mathbf{H}$ 与 $" + BS + "mathbf{H}'$、$" + BS + "mathbf{K}$ 与 $" + BS + "mathbf{K}'$ 之间的同构，习惯上仍写作 $" + BS + 'mathbf{G} = ' + BS + 'mathbf{H} ' + BS + 'otimes ' + BS + 'mathbf{K}$。}')

patch('chapters/ch1_s5.tex',
 '所组成的点群。' + TS + '{' + BS + 'ddag} 这正是',
 '所组成的点群。' + FN + '{有些作者用 isomorphous（同晶）一词表示我们这里的 isogonal（同形）。} 这正是')

print('remaining footnotes attached')
