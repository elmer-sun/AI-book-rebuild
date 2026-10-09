# -*- coding: utf-8 -*-
"""Attach real footnotes at marker sites in Chinese chapter files."""
import io

BS = chr(92)
TS = BS + 'textsuperscript'
FN = BS + 'footnote'

def patch(p, old, new):
    s = io.open(p, encoding='utf-8').read()
    assert old in s, (p, old[:50])
    s = s.replace(old, new, 1)
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

# s1: Cauchy / Galois footnotes
patch('chapters/ch1_s1.tex',
 '有限群理论始于 Cauchy' + TS + '{' + BS + 'ddag}，',
 '有限群理论始于 Cauchy' + FN + '{1789--1857。}，')
patch('chapters/ch1_s1.tex',
 'Galois' + TS + '{' + BS + 'S} 为该理论增添',
 'Galois' + FN + '{1811--1832。} 为该理论增添')

# s2: Def 1.2.1 (iii) footnote (first dagger gets the note; (iv) keeps dagger mark)
patch('chapters/ch1_s2.tex',
 '(iii) 群中存在唯一的单位元' + TS + '{' + BS + 'ddag} $E$',
 '(iii) 群中存在唯一的单位元' + FN + '{单位元与逆元的唯一性及双侧性并非必须作为公设：由右单位元的存在（$AE = A$）与右逆的存在（$AA^{-1} = E$）连同公理 (i)、(ii) 即足以建立唯一性与双侧性。但这些性质过于基本，许多作者仍将其写入定义。} $E$')

# s2: Def 1.2.13 rule footnote
patch('chapters/ch1_s2.tex',
 '式 (1.2.5) 保证了定义 1.2.13 的规则 (i)–(iii) 成立。' + TS + '{' + BS + 'ddag}',
 '式 (1.2.5) 保证了定义 1.2.13 的规则 (i)–(iii) 成立。' + FN + '{群 $' + BS + 'mathbf{H}$ 与 $' + BS + 'mathbf{G}$ 的子群 $' + BS + "mathbf{H}'$（由一切 $(H, E)$，$H " + BS + 'in ' + BS + "mathbf{H}$，组成）同构。若同样定义 $" + BS + "mathbf{K}'$，则按定义 1.2.13 严格地说我们得到的是 $" + BS + "mathbf{G} = " + BS + "mathbf{H}' " + BS + "otimes " + BS + "mathbf{K}'$；但由于 $" + BS + "mathbf{H}$ 与 $" + BS + "mathbf{H}'$、$" + BS + "mathbf{K}$ 与 $" + BS + "mathbf{K}'$ 之间的同构，习惯上仍写作 $" + BS + 'mathbf{G} = ' + BS + 'mathbf{H} ' + BS + 'otimes ' + BS + 'mathbf{K}$。}')

# s5: isogonal footnote
patch('chapters/ch1_s5.tex',
 '所组成的点群。' + TS + '{' + BS + 'ddag} 这正是',
 '所组成的点群。' + FN + '{有些作者用 isomorphous（同晶）一词表示我们这里的 isogonal（同形）。} 这正是')

print('footnotes attached')
