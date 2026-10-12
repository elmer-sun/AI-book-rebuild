# -*- coding: utf-8 -*-
"""ch14 脚注最终校验"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
t = open(r'chapters\ch14.tex', encoding='utf-8').read()
body_lines = [l for l in t.split('\n') if not l.lstrip().startswith('%')]
b = '\n'.join(body_lines)
marks = {m: b.count(m) for m in '①②③④'}
print('正文剩余圈码:', marks, '合计', sum(marks.values()))
fn = t.count('\\footnote{')
print('footnote 数:', fn)
print('全文件花括号平衡:', t.count('{') - t.count('}'))
bad = 0
for i, l in enumerate(t.split('\n'), 1):
    if '\\footnote{' in l and l.count('{') != l.count('}'):
        bad += 1
        print('  不平衡行', i, l[:60])
print('不平衡 footnote 行:', bad)
doc_notes = 0
import pymupdf
doc = pymupdf.open('smokefn_ch14.pdf')
for i in range(340, 404):
    tt = doc[i].get_text()
    for x in tt.split('\n'):
        xs = x.strip()
        if re.match('^[①②③④⑤]', xs):
            doc_notes += 1
print('PDF ch14 范围脚注行合计:', doc_notes)
