# -*- coding: utf-8 -*-
"""ch07 参考文献条目键加方括号，与全书体例一致。"""
import re
p = r'E:\AI整理书籍\Phillips\重排本\chapters\ch07.tex'
t = open(p, encoding='utf-8').read()
t2, n = re.subn(r'\\item \[([A-Z][A-Za-z]{0,3}\d{4})\]', lambda m: '\\item [{[' + m.group(1) + ']}]', t)
open(p, 'w', encoding='utf-8', newline='\n').write(t2)
print('ch07 refs bracketed:', n)
