# -*- coding: utf-8 -*-
"""把 symbols.tex 按原书 i-iv 页拆成 4 个 tabular（可分页）。"""
import io, re

BS = chr(92)
path = r'E:\AI整理书籍\李正中\重排本\chapters\symbols.tex'
s = io.open(path, encoding='utf-8').read()

# 还原 heredoc 造成的损坏
s = s.replace(BS + 'parigbreak', BS + 'par' + BS + 'bigbreak')

# 若已是多 tabular（先前跑过），先还原为单 tabular 结构
if s.count(BS + 'begin{tabular}') > 1:
    s = s.replace(CLOSE := (BS + 'end{tabular}' + '\n}\n' + BS + 'par' + BS + 'bigbreak' + '\n'), '@SEP@')
    s = s.replace(OPENB := ('{' + BS + 'small\n' + BS + 'begin{tabular}{@{}p{0.46' + BS + 'textwidth}@{}p{0.50' + BS + 'textwidth}@{}}\n'), '')
    body = s.replace('@SEP@', '\n')
    # 去掉残留的首个 begin tabular 与末尾 end
else:
    body = s

print('has multiple:', s.count(BS + 'begin{tabular}'))
io.open(path + '.bak', 'w', encoding='utf-8').write(s)
