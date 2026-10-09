# -*- coding: utf-8 -*-
"""ch2.tex 替换 v4：纯逐行处理 + 完整性断言"""
import io
import json
import os
import re

os.chdir(r'E:\AI整理书籍\磁学\book')
report = json.load(open('fig_inventory/ch2_report.json', encoding='utf-8'))

# hash -> ('swap', pdf) | ('delete',)
mapping = {}
for it in report:
    if it['verdict'] != 'redraw':
        continue
    srcs = it['src'].split('+')
    for k, h in enumerate(it['images']):
        key = h[:-4] if h.endswith('.jpg') else h
        if k < len(srcs):
            mapping[key] = ('swap', srcs[k])
        else:
            mapping[key] = ('delete',)

s = io.open('ch2.tex', encoding='utf-8').read()
B = chr(92)
n_begin = s.count(B + 'begin{figure}')
n_end = s.count(B + 'end{figure}')
assert n_begin == n_end == 16, (n_begin, n_end)

out_lines = []
n_swap = n_del = 0
for ln in s.split('\n'):
    hm = re.search(r'\\includegraphics\[[^\]]*\]\{([a-f0-9]{20,})\.jpg\}', ln)
    if not hm:
        out_lines.append(ln)
        continue
    key = hm.group(1)
    act = mapping.get(key)
    if act is None:
        out_lines.append(ln)   # keep 的扫描图
        continue
    if act[0] == 'swap':
        out_lines.append(ln.replace('{%s.jpg}' % key, '{%s.pdf}' % act[1]))
        n_swap += 1
    else:
        n_del += 1
        if out_lines and re.search(r'\\\\(\[[^\]]*\])?\s*$', out_lines[-1]):
            out_lines[-1] = re.sub(r'\\\\(\[[^\]]*\])?\s*$', '', out_lines[-1])
        continue

s2 = '\n'.join(out_lines)
assert s2.count(B + 'begin{figure}') == 16
assert s2.count(B + 'end{figure}') == 16
left = re.findall(r'includegraphics\[[^\]]*\]\{([a-f0-9]{20,})\.jpg\}', s2)
assert len(left) == 3, left
io.open('ch2.tex', 'w', encoding='utf-8', newline='\n').write(s2)
print('v4 OK: swapped=%d deleted=%d keep=%d lines %d->%d' %
      (n_swap, n_del, len(left), s.count('\n'), s2.count('\n')))
