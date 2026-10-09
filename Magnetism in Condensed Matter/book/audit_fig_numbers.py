# -*- coding: utf-8 -*-
"""图号审计：对每章，用 fig_inventory 的最终图号序列对比 build PDF 里
实际渲染的图号序列；在 build/*.tex 中需要复位的位置插入 \\setcounter。"""
import json
import os
import re

import pymupdf

INV = r'E:\AI整理书籍\磁学\book\fig_inventory'
BUILD = r'E:\AI整理书籍\磁学\recovery\build'
CHAPTERS = {'ch2': 2, 'ch3': 3, 'ch4': 4, 'ch5': 5, 'ch6': 6, 'ch7': 7,
            'ch8': 8, 'appB': None, 'appC': None, 'appD': None}

doc = pymupdf.open(os.path.join(BUILD, 'main.pdf'))
full = ''
page_of = []
for i in range(doc.page_count):
    t = doc[i].get_text()
    page_of.extend([i + 1] * len(t))
    full += t

for base in CHAPTERS:
    inv_path = os.path.join(INV, base + '.json')
    if not os.path.exists(inv_path):
        continue
    items = json.load(open(inv_path, encoding='utf-8'))
    want = [it['fig_no'] for it in items if it['fig_no'] != '?']
    # PDF 里实际渲染的图号序列（图 2.1: ... 形式；附录为 图 B.1）
    ch = base[2:]
    pat = re.compile(r'图%s\.(\d+)\s*:' % re.escape(ch))
    got = [m.group(1) for m in pat.finditer(full)]
    want_n = [w.split('.')[-1] for w in want]
    if [int(g) for g in got] == [int(w) for w in want_n]:
        print('%-5s OK (%d figs)' % (base, len(got)))
        continue
    print('%-5s 漂移: 期望 %s' % (base, ','.join(want_n)))
    print('      实际 %s' % ','.join(got))
    # 在 tex 中定位每个 figure 环境，算出需要 setcounter 的位置
    tex = open(os.path.join(BUILD, base + '.tex'), encoding='utf-8').read()
    envs = [m for m in re.finditer(r'\\begin\{figure\}', tex)]
    # 逐环境确定其“自动编号”= 前面的环境数+1；期望编号来自 inventory
    inserts = []
    counter = 0
    for k, m in enumerate(envs):
        counter += 1
        want_k = want[k] if k < len(want) else None
        if want_k and int(want_k.split('.')[-1]) != counter:
            inserts.append((m.start(), int(want_k.split('.')[-1]), counter))
            counter = int(want_k.split('.')[-1])
    for pos, w, c in inserts:
        print('      插入 setcounter{%d}（自动编号 %d）@%d' % (w, c, pos))
    if inserts:
        for pos, w, c in sorted(inserts, reverse=True):
            tex = (tex[:pos] + '\\setcounter{figure}{%d}\n' % (w - 1)
                   + tex[pos:])
        open(os.path.join(BUILD, base + '.tex'), 'w', encoding='utf-8',
             newline='\n').write(tex)
        print('      -> 已写入')
