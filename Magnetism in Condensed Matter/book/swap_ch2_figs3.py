# -*- coding: utf-8 -*-
"""ch2.tex 替换 v3：带完整性断言（环境数、开闭平衡、行数守恒）"""
import json
import os
import io
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

report = json.load(open('fig_inventory/ch2_report.json', encoding='utf-8'))
s = open('ch2.tex', encoding='utf-8').read()

BEGIN = '\\begin{figure}'
END = '\\end{figure}'
n_begin = s.count(BEGIN)
n_end = s.count(END)
n_lines = s.count('\n')
assert n_begin == n_end == 16, (n_begin, n_end)

out = []
pos = 0
n_swap = n_del = 0
while True:
    a = s.find(BEGIN, pos)
    if a < 0:
        out.append(s[pos:])
        break
    b = s.find(END, a)
    assert b > a, (a, b)
    block = s[a:b]
    m = re.search(r'\{([a-f0-9]{20,})\.jpg\}', block)
    entry = None
    if m:
        for it in report:
            if it['verdict'] == 'redraw' and (
                    m.group(1) in it['images']
                    or m.group(1) + '.jpg' in it['images']):
                entry = it
                break
    if entry:
        srcs = entry['src'].split('+')
        lines = block.split('\n')
        img_idx = 0
        new_lines = []
        for ln in lines:
            hm = re.search(
                r'\\includegraphics\[[^\]]*\]\{([a-f0-9]{20,})\.jpg\}', ln)
            if hm and img_idx < len(srcs):
                ln = re.sub(r'\{[a-f0-9]{20,}\.jpg\}',
                            '{%s.pdf}' % srcs[img_idx], ln)
                img_idx += 1
                n_swap += 1
                new_lines.append(ln)
            elif hm:
                n_del += 1
                if new_lines and re.search(r'\\\\(\[[^\]]*\])?\s*$',
                                           new_lines[-1]):
                    new_lines[-1] = re.sub(r'\\\\(\[[^\]]*\])?\s*$', '',
                                           new_lines[-1])
                continue
            else:
                new_lines.append(ln)
        assert img_idx == len(srcs), (entry['fig_no'], img_idx, len(srcs))
        block = '\n'.join(new_lines)
        out.append(s[pos:a])
        out.append(block)
        pos = b
    else:
        out.append(s[pos:b])
        pos = b
out.append(s[pos:])
s2 = ''.join(out)

# ---- 完整性断言
assert s2.count(BEGIN) == 16, s2.count(BEGIN)
open('ch2_out.tex', 'w', encoding='utf-8', newline=chr(10)).write(s2)
left = re.findall(r'\\includegraphics\[[^\]]*\]\{([a-f0-9]{20,}\.jpg)\}', s2)
assert len(left) == 3, left
print('swapped=%d deleted=%d; env 16/16 OK; keep=%d' %
      (n_swap, n_del, len(left)))
open('ch2.tex', 'w', encoding='utf-8', newline='\n').write(s2)
print('written')
