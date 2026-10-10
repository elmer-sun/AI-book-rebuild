# -*- coding: utf-8 -*-
"""ch12: 双反斜杠 \\allowbreak -> 单反斜杠 \allowbreak"""
import io
p = r'E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\chapters\ch12.tex'
s = io.open(p, encoding='utf-8').read()
bad = '\\\\allowbreak'   # 文件中的两个字符: \ \ allowbreak
good = '\\allowbreak'
n = s.count(bad)
s = s.replace(bad, good)
io.open(p, 'w', encoding='utf-8').write(s)
print('fixed', n, '; remaining double:', s.count(bad), '; single now:', s.count(good))
