# -*- coding: utf-8 -*-
"""把 build/ch3.tex 的图 3.13 块恢复为事故前的最终形态（2x3 网格）"""
import io
import re

p = r'E:\AI整理书籍\磁学\recovery\build\ch3.tex'
B = chr(92)

s = io.open(p, encoding='utf-8').read()
i = s.find('自旋回波效应。')
blk_start = s.rfind(B + 'begin{figure}', 0, i)
blk_end = s.find(B + 'end{figure}', i) + len(B + 'end{figure}')
block = s[blk_start:blk_end]

imgs = ['4eccdfed5cdb03ca1c3a15e34ca681ec64f5ce189bfee9410cc0541d833d45f6',
        'e6f70a4c19f3c8f5acd40843318cd772606ada0d5cf9fe81b91cd8827a077baf',
        '6ea2358222286fb4ee303f494f68cddee3b76ac37efc72dea6b74b7ee4ea3246',
        'd6280d2b4bffd0e716a364e7f01e5078540b77441be16ef63714539fc101ee9c',
        '419ebeb8df9aa3519bbb9944189c8e7e802b68caf689d2e6c866d925c9ccdcd5',
        '55976c6a2e22105f8adbe3f5dbf1fce1fd743be210c2a7d4bf35f8b8932f2469']
# 校验这 6 张图确实在旧块里
old_imgs = re.findall(r'\{([a-f0-9]{20,})\.jpg\}', block)
assert sorted(old_imgs) == sorted(imgs), (sorted(old_imgs), sorted(imgs))

deg = B + 'circ'
new = (B + 'begin{figure}' + chr(10) + B + 'centering' + chr(10)
       + B + 'includegraphics[width=0.46' + B + 'textwidth]{' + imgs[0]
       + '.jpg}' + B + 'hfill' + B + 'includegraphics[width=0.46' + B
       + 'textwidth]{' + imgs[1] + '.jpg}' + B * 2 + chr(10)
       + B + 'includegraphics[width=0.46' + B + 'textwidth]{' + imgs[2]
       + '.jpg}' + B + 'hfill' + B + 'includegraphics[width=0.46' + B
       + 'textwidth]{' + imgs[3] + '.jpg}' + B * 2 + chr(10)
       + B + 'includegraphics[width=0.46' + B + 'textwidth]{' + imgs[4]
       + '.jpg}' + B + 'hfill' + B + 'includegraphics[width=0.46' + B
       + 'textwidth]{' + imgs[5] + '.jpg}' + B * 2 + chr(10)
       + B + 'caption{自旋回波效应。（a）平衡磁化强度初始沿 $z$ 方向、平行于 '
       + '$B_0$。（b）称该时刻为 $t=0$：沿 $x$ 轴的 $90' + deg + '$ 脉冲把自旋'
       + '转入 $xy$ 平面。（c）由于 $z$ 轴方向的恒定场 $B_0$，自旋在 $xy$ 平面内'
       + '进动，但因磁场不均匀而速率略异。（d）它们逐渐相互失相。（e）$t='
       + B + 'tau$ 时沿 $x$ 轴的 $180' + deg + '$ 脉冲使自旋绕 $x$ 轴转过 $180'
       + deg + '$；随后在 $B_0$ 中进动时次序已颠倒。（f）$2' + B + 'tau$ 时它们'
       + '重新聚齐，产生自旋回波信号——前提是期间没有发生其他弛豫过程。图中画的'
       + '是两脉冲间隔较短的情形；若间隔长、自旋在 $180' + deg + '$ 脉冲前已转过'
       + '若干圈，效应同样成立。' + B * 2 + chr(10)
       + '{' + B + 'footnotesize' + B + 'itshape Fig.~3.13 The spin echo '
       + 'effect.}}' + chr(10)
       + B + 'end{figure}')

s = s.replace(block, new)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('fig 3.13 restored to final 2x3 form')
