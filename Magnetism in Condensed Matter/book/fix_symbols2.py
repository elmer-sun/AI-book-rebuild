# -*- coding: utf-8 -*-
bs = chr(92)
s = open('symbols.tex', encoding='utf-8').read()
old = (bs + 'begin{table}\n' + bs + 'centering\n' + bs + 'caption{基本常数。'
       + chr(92) + chr(92) + '\n' + '{' + bs + 'footnotesize' + bs + 'itshape Fundamental constants.}}\n')
new = (bs + 'begin{center}\n' + bs + 'smallskip\n'
       + '{基本常数。' + chr(92) + chr(92) + '\n'
       + '{' + bs + 'footnotesize' + bs + 'itshape Fundamental constants.}}\n')
assert old in s, 'pattern not found'
s = s.replace(old, new)
# 结尾 \end{table} -> \end{center}（该环境是文件中最后一个 table）
idx = s.rfind(bs + 'end{table}')
s = s[:idx] + bs + 'end{center}' + s[idx + len(bs + 'end{table}'):]
open('symbols.tex', 'w', encoding='utf-8').write(s)
t = open('symbols.tex', encoding='utf-8').read()
print('tables left:', t.count(bs + 'begin{table}'), '| center pairs:',
      t.count(bs + 'begin{center}'), t.count(bs + 'end{center}'))
