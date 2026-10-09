# -*- coding: utf-8 -*-
bs = chr(92)
s = open('ch5.tex', encoding='utf-8').read()
old = (bs + 'begin{figure}\n'
       + bs + 'centering\n'
       + bs + 'includegraphics[width=0.4' + bs + 'textwidth]{fig5_18.pdf}\n'
       + bs + 'caption{上：MnO 的磁结构。Mn 离子位于面心立方晶格上；$'
       + bs + 'mathrm{O^{2-}}$ 离子未画出\n'
       + '（见图 4.2）。Mn 离子按自旋态以黑白两色标记。下：$T_{' + bs + 'mathrm{N}}$ 上、下 MnO 的\n'
       + '中子衍射图。取自 C.~G.~Shull, W.~A.~Strauser 与 E.~O.~Wollan, Phys.~Rev., '
       + bs + 'textbf{83},\n333 (1951)。}\n'
       + bs + 'end{figure}')
new = (bs + 'begin{figure}\n'
       + bs + 'centering\n'
       + bs + 'includegraphics[width=0.42' + bs + 'textwidth]{fig5_18.pdf}\n'
       + bs + 'caption{MnO 的磁结构。Mn 离子位于面心立方晶格上；$'
       + bs + 'mathrm{O^{2-}}$ 离子未画出\n'
       + '（见图 4.2）。Mn 离子按自旋态以黑白两色标记。}\n'
       + bs + 'end{figure}\n\n'
       + bs + 'begin{figure}\n'
       + bs + 'centering\n'
       + bs + 'includegraphics[width=0.5' + bs + 'textwidth]{fig5_19.pdf}\n'
       + bs + 'caption{$T_{' + bs + 'mathrm{N}}$ 上、下 MnO 的中子衍射图。取自 C.~G.~Shull,\n'
       + 'W.~A.~Strauser 与 E.~O.~Wollan, Phys.~Rev., ' + bs + 'textbf{83}, 333 (1951)。}\n'
       + bs + 'end{figure}')
assert old in s, 'pattern not found'
s = s.replace(old, new)
open('ch5.tex', 'w', encoding='utf-8').write(s)
print('ch5 5.18/5.19 split done')
