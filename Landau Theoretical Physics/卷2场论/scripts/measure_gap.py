# -*- coding: utf-8 -*-
"""测量每页 习题 标题与下一行文字的垂直间距"""
import fitz  # pymupdf

doc = fitz.open(r'E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\main_full.pdf')
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
        # 找"习 题"独立行（heiti 标题）
        if txt in ('习 题', '习题') and i + 1 < len(lines):
            ny0, ny1, ntxt = lines[i + 1]
            gap = ny0 - y1
            flag = ' <-- 异常' if gap > 30 else ''
            print(f'p{pno+1:>3}  习题标题y={y1:6.1f}  下一行y={ny0:6.1f}  gap={gap:5.1f}pt{flag}  下一行: {ntxt[:24]}')
doc.close()
