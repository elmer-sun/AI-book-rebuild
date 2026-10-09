# -*- coding: utf-8 -*-
"""ch2.tex 替换 v2：按环境逐行处理；单 PDF 多面板时删除多余扫描图行"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

report = json.load(open('fig_inventory/ch2_report.json', encoding='utf-8'))
s = open('ch2.tex', encoding='utf-8').read()

BEGIN = '\\begin{figure}'
END = '\\end{figure}'
out = []
pos = 0
n_swap = n_del = 0
while True:
    a = s.find(BEGIN, pos)
    if a < 0:
        out.append(s[pos:])
        break
    b = s.find(END, a)
    block = s[a:b]
    # 该环境对应的报告条目：按块内第一个 hash 找
    m = re.search(r'\{([a-f0-9]{20,})\.jpg\}', block)
    entry = None
    if m:
        for it in report:
            if it['verdict'] == 'redraw' and (m.group(1) in it['images']
                    or m.group(1) + '.jpg' in it['images']):
                entry = it
                break
    if entry:
        srcs = entry['src'].split('+')
        lines = block.split('\n')
        img_idx = 0
        new_lines = []
        for ln in lines:
            hm = re.search(r'\\includegraphics\[[^\]]*\]\{([a-f0-9]{20,})\.jpg\}',
                           ln)
            if hm and img_idx < len(srcs):
                ln = re.sub(r'\{[a-f0-9]{20,}\.jpg\}',
                            '{%s.pdf}' % srcs[img_idx], ln)
                img_idx += 1
                n_swap += 1
                new_lines.append(ln)
            elif hm:
                n_del += 1
                # 删整行；若上一保留行以 \\[...] 结尾则清理
                if new_lines and re.search(r'\\\\(\[[^\]]*\])?\s*$',
                                           new_lines[-1]):
                    new_lines[-1] = re.sub(r'\\\\(\[[^\]]*\])?\s*$', '',
                                           new_lines[-1])
                continue
            else:
                new_lines.append(ln)
        block = '\n'.join(new_lines)
    out.append(s[pos:a])
    out.append(block)
    pos = b
out.append(s[pos:])
s2 = ''.join(out)
open('ch2.tex', 'w', encoding='utf-8', newline='\n').write(s2)
print('swapped %d, deleted %d redundant lines' % (n_swap, n_del))
left = re.findall(r'\\includegraphics\[[^\]]*\]\{([a-f0-9]{20,}\.jpg)\}', s2)
print('保留扫描图 %d 张:' % len(left), left)
