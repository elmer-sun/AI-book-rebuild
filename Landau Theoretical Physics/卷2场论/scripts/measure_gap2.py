# -*- coding: utf-8 -*-
"""测量 习题 标题上方+下方空隙，全书法"""
import pymupdf

doc = pymupdf.open(r'E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\main_full.pdf')
for pno in range(len(doc)):
    page = doc[pno]
    d = page.get_text('dict')
    lines = []
    for blk in d['blocks']:
        if blk.get('type') != 0:
            continue
        for ln in blk['lines']:
            txt = ''.join(sp['text'] for sp in ln['spans']).strip()
            if txt:
                lines.append((ln['bbox'][1], ln['bbox'][3], txt))
    lines.sort()
    for i, (y0, y1, txt) in enumerate(lines):
        if txt in ('习 题', '习题'):
            above = y0 - lines[i-1][1] if i else 0
            below = lines[i+1][0] - y1 if i + 1 < len(lines) else 0
            mark = ' <--' if below > 30 or above > 40 else ''
            print(f'p{pno+1:>3} above={above:6.1f} below={below:6.1f}{mark}')
doc.close()
