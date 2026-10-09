# -*- coding: utf-8 -*-
"""图号审计 v2：以冻结 PDF 的图号序列为基准，对比 build PDF，
在 build/*.tex 插入 \\setcounter 复位。"""
import os
import re

import pymupdf

OLD = r'E:\AI整理书籍\磁学\磁学_中译本.pdf'
BUILD = r'E:\AI整理书籍\磁学\recovery\build'
CHS = ['2', '3', '4', '5', '6', '7', '8', 'B', 'C', 'D']


def seq(doc, ch):
    pat = re.compile(r'图%s\.(\d+)?\s*[:：]' % re.escape(ch))
    out = []
    for i in range(doc.page_count):
        for m in pat.finditer(doc[i].get_text()):
            out.append(m.group(1))
    return out


def letter_seq(doc, ch):
    out = []
    pat = re.compile(r'图%s\.(\d+)\s*[:：]' % ch)
    for i in range(doc.page_count):
        for m in pat.finditer(doc[i].get_text()):
            out.append(m.group(1))
    return out


old = pymupdf.open(OLD)
new = pymupdf.open(os.path.join(BUILD, 'main.pdf'))

for ch in CHS:
    want = letter_seq(old, ch)
    got = letter_seq(new, ch)
    if want == got:
        print('图%s OK (%d)' % (ch, len(want)))
        continue
    print('图%s 漂移:\n  期望 %s\n  实际 %s' % (
        ch, ','.join(want), ','.join(got)))
    tex_path = os.path.join(BUILD, ('app' + ch) if ch.isalpha()
                            else ('ch' + ch) + '.tex')
    tex_path = os.path.join(BUILD, ('app%s.tex' % ch) if ch.isalpha()
                            else ('ch%s.tex' % ch))
    tex = open(tex_path, encoding='utf-8').read()
    envs = [m for m in re.finditer(r'\\begin\{figure\}', tex)]
    if len(envs) != len(want):
        print('  !! 环境数 %d != 期望图数 %d，跳过' % (len(envs), len(want)))
        continue
    inserts = []
    counter = 0
    for k, m in enumerate(envs):
        counter += 1
        w = int(want[k])
        if w != counter:
            inserts.append((m.start(), w, counter))
            counter = w
    for pos, w, c in inserts:
        print('  setcounter{%d} (auto=%d) @%d' % (w, c, pos))
    for pos, w, c in sorted(inserts, reverse=True):
        tex = (tex[:pos] + '\\setcounter{figure}{%d}\n' % (w - 1) + tex[pos:])
    open(tex_path, 'w', encoding='utf-8', newline='\n').write(tex)
    print('  -> 已写入 %s' % tex_path)
