# -*- coding: utf-8 -*-
"""ch3: 重建图 3.13 为双列网格布局"""
import io, re

B = chr(92)
NL = chr(10)
p = r'E:\AI整理书籍\磁学\book\ch3.tex'
s = io.open(p, encoding='utf-8').read()

i = s.find('自旋回波效应。')
blk_start = s.rfind(B + 'begin{figure}', 0, i)
blk_end = s.find(B + 'end{figure}', i) + len(B + 'end{figure}')
block = s[blk_start:blk_end]
found = re.findall(r'includegraphics\[width=0\.3' + re.escape(B) + r'textwidth\]\{([a-f0-9]+\.jpg)\}', block)
assert len(found) == 6, 'expected 6 imgs, got %d' % len(found)

LB = '{'
RB = '}'
deg = B + 'circ'
TAU = B + 'tau'

new = B + 'begin{figure}' + NL + B + 'centering' + NL
for k, im in enumerate(found):
    new += B + 'includegraphics[width=0.46' + B + 'textwidth]{' + im + '}'
    new += B + 'hfill' if k % 2 == 0 else B * 2 + NL
cap_cn = ('自旋回波效应。（a）平衡磁化强度初始沿 $z$ 方向、平行于 $B_0$。（b）称该时刻为 '
          '$t=0$：沿 $x$ 轴的 $90' + deg + '$ 脉冲把自旋转入 $xy$ 平面。（c）由于 $z$ 轴方向的'
          '恒定场 $B_0$，自旋在 $xy$ 平面内进动，但因磁场不均匀而速率略异。（d）它们逐渐相互'
          '失相。（e）$t=' + TAU + '$ 时沿 $x$ 轴的 $180' + deg + '$ 脉冲使自旋绕 $x$ 轴转过 '
          '$180' + deg + '$；随后在 $B_0$ 中进动时次序已颠倒。（f）$2' + TAU + '$ 时它们重新聚齐，'
          '产生自旋回波信号——前提是期间没有发生其他弛豫过程。图中画的是两脉冲间隔较短的情形；'
          '若间隔长、自旋在 $180' + deg + '$ 脉冲前已转过若干圈，效应同样成立。')
cap_en = B * 2 + NL + LB + B + 'footnotesize' + B + 'itshape Fig.~3.13 The spin echo effect.' + RB + RB
new += B + 'caption{' + cap_cn + cap_en + '}' + NL + B + 'end{figure}'

s = s.replace(block, new)
io.open(p, 'w', encoding='utf-8').write(s)
print('fig 3.13 rebuilt, block len', len(block), '->', len(new))
