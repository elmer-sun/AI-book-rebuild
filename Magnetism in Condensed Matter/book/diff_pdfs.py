# -*- coding: utf-8 -*-
"""逐页文本比对：recovery/build/main.pdf vs 事故前冻结的 磁学_中译本.pdf"""
import difflib
import re
import sys

import pymupdf

NEW = r'E:\AI整理书籍\磁学\recovery\build\main.pdf'
OLD = r'E:\AI整理书籍\磁学\磁学_中译本.pdf'


def norm(t):
    t = t.replace('\u00ad', '')
    t = re.sub(r'[\s\u3000]+', '', t)
    return t


a = pymupdf.open(NEW)
b = pymupdf.open(OLD)
print('new pages', a.page_count, '| old pages', b.page_count)
bad = []
for i in range(min(a.page_count, b.page_count)):
    ta = norm(a[i].get_text())
    tb = norm(b[i].get_text())
    if ta != tb:
        bad.append(i + 1)
print('差异页数:', len(bad))
print('差异页码:', bad)
limit = int(sys.argv[1]) if len(sys.argv) > 1 else 3
for p in bad[:limit]:
    print('=' * 24, 'page', p)
    ta = norm(a[p - 1].get_text())
    tb = norm(b[p - 1].get_text())
    sm = difflib.SequenceMatcher(None, tb, ta)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        old_seg = tb[i1:i2]
        new_seg = ta[j1:j2]
        print('  [%s] 旧:%r' % (tag, old_seg[:80]))
        print('        新:%r' % new_seg[:80])
