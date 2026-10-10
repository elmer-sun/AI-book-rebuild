# -*- coding: utf-8 -*-
"""修复 heredoc 造成的 BEL 字符: \\x07 + 'llowbreak' -> \\allowbreak"""
import io
p = r'E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\chapters\ch12.tex'
s = io.open(p, encoding='utf-8').read()
bad = '\x07llowbreak'          # BEL + llowbreak
good = '\\allowbreak'
n = s.count(bad)
s = s.replace(bad, good)
io.open(p, 'w', encoding='utf-8').write(s)
print('fixed', n, 'BEL-allowbreak; remaining backslash-count check:')
print('allowbreak occurrences:', s.count('\\allowbreak'))
