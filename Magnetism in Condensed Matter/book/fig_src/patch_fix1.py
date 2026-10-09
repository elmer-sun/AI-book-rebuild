# -*- coding: utf-8 -*-
"""第一轮修正：箭头方向/针头粗细/倾斜方向/标签避让"""
import os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ch1'))

BS = chr(92)  # backslash


def patch(fname, old, new):
    s = open(fname, encoding='utf-8').read()
    assert old in s, (fname, old[:50])
    open(fname, 'w', encoding='utf-8').write(s.replace(old, new, 1))
    print('ok', fname)


# ---- fig1_01: (a) 椭圆右端下沉、电流箭头到底部、dS 指向右上；(b) 箭头到底部
patch('fig1_01.tex',
      BS + 'draw[postaction={decorate,decoration={markings,' + chr(10) +
      '  mark=at position 0.62 with {' + BS + 'arrow[line width=0.8pt]{>}}}}]' + chr(10) +
      '  (0,0) ellipse (1.05 and 0.36);',
      BS + 'draw[rotate=-14,postaction={decorate,decoration={markings,' + chr(10) +
      '  mark=at position 0.74 with {' + BS + 'arrow[line width=0.8pt]{>}}}}]' + chr(10) +
      '  (0,0) ellipse (1.05 and 0.36);')
patch('fig1_01.tex',
      BS + 'draw[->,line width=1.0pt] (0,0) -- (-0.5,1.5)',
      BS + 'draw[->,line width=1.0pt] (0,0) -- (0.42,1.5)')
patch('fig1_01.tex',
      'mark=at position 0.68 with {' + BS + 'arrow[line width=0.9pt]{>}}',
      'mark=at position 0.74 with {' + BS + 'arrow[line width=0.9pt]{>}}')

# ---- fig1_03 / fig1_04: 偶极针头改细长
patch('fig1_03.tex',
      BS + 'draw[line width=1.7pt,-{Stealth[length=9.5mm,width=4.2mm]}]' + chr(10) +
      '  (0,0) -- (52:2.05);',
      BS + 'draw[line width=1.5pt,-{Stealth[length=7.5mm,width=3.4mm]}]' + chr(10) +
      '  (0,0) -- (52:2.1);')
patch('fig1_04.tex',
      BS + 'draw[line width=1.7pt,-{Stealth[length=8.5mm,width=3.8mm]}] (0,0) -- (1.28,1.92);',
      BS + 'draw[line width=1.5pt,-{Stealth[length=7mm,width=3.2mm]}] (0,0) -- (1.28,1.92);')

# ---- fig1_05: v 箭头从电子处出发
patch('fig1_05.tex',
      BS + 'draw[->,line width=1.1pt] (55:1.55) ++ (-0.12,0.09) -- ++ (-0.72,0.63)',
      BS + 'draw[->,line width=1.1pt] (55:1.55) -- ++ (-0.72,0.63)')

# ---- fig1_06: 椭球右端上翘
patch('fig1_06.tex', BS + 'begin{scope}[rotate=-16]',
      BS + 'begin{scope}[rotate=14]')

# ---- fig1_08: 标签避让
patch('fig1_08.tex', BS + 'node at (1.82,0.24) {$1$};',
      BS + 'node at (1.7,0.34) {$1$};')
patch('fig1_08.tex', BS + 'node at (0.94,0.22) {' + BS + '$' + BS + 'phi$};',
      BS + 'node at (1.02,0.38) {' + BS + '$' + BS + 'phi$};')

print('all patched')
