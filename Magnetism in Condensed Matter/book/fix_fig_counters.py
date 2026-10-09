# -*- coding: utf-8 -*-
"""图号对齐 v2：用 find 定位 figure 环境，比对英文图注编号并插 setcounter"""
import io, re

B = chr(92)
NL = chr(10)
d = r'E:\AI整理书籍\磁学\book' + B

files = ['ch1.tex', 'ch2.tex', 'ch3.tex', 'ch4.tex', 'ch5.tex', 'ch6.tex',
         'ch7.tex', 'ch8.tex', 'appB.tex', 'appC.tex', 'appD.tex']

pat_num = re.compile(r'Fig\.~?([A-Z]+)?\.?\s?(\d+)\.(\d+)')
beg = B + 'begin{figure}'
end = B + 'end{figure}'

total = 0
for f in files:
    path = d + f
    s = io.open(path, encoding='utf-8').read()
    inserts = []   # (position, text)
    counters = {}
    pos = 0
    while True:
        a = s.find(beg, pos)
        if a < 0:
            break
        b = s.find(end, a)
        block = s[a:b]
        nm = pat_num.search(block)
        pos = b + len(end)
        if not nm:
            continue
        letter = nm.group(1) or ''
        book_ch = nm.group(2)
        book_n = int(nm.group(3))
        key = letter + book_ch
        used = counters.get(key, 0) + 1
        counters[key] = used
        if used != book_n:
            inserts.append((a, B + 'setcounter{figure}{' + str(book_n - 1) + '}' + NL))
            counters[key] = book_n
            total += 1
            print(f, ':', key + '.' + str(book_n), 'auto', used, '-> set', book_n - 1)
    if inserts:
        for a, txt in reversed(inserts):
            s = s[:a] + txt + s[a:]
        io.open(path, 'w', encoding='utf-8').write(s)
print('total insertions:', total)
