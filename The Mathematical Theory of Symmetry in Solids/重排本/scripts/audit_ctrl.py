# -*- coding: utf-8 -*-
"""审计并修复章节 .tex 中的控制字符（\t \b \r 等历史污染）。"""
import glob, os, re

d = os.path.join(os.path.dirname(__file__), '..', 'chapters')
report = []
for f in sorted(glob.glob(os.path.join(d, '*.tex'))):
    with open(f, 'rb') as fh:
        data = fh.read()
    bad = {}
    for i, b in enumerate(data):
        if b < 32 and b not in (10, 13):
            bad.setdefault(b, 0)
            bad[b] += 1
    if bad:
        report.append((os.path.basename(f), bad))

for name, bad in report:
    print(name, {chr(k): v for k, v in bad.items()})

# 修复已知模式：TAB 紧跟 extwidth / extbf / ext 等（\t 吃掉了反斜杠）
pat = re.compile('\t(ext[a-zA-Z]*)')
for f in sorted(glob.glob(os.path.join(d, '*.tex'))):
    with open(f, 'rb') as fh:
        data = fh.read().decode('utf-8')
    new, n = pat.subn(lambda m: '\\\\' + m.group(1), data)
    if n:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new)
        print('fixed', os.path.basename(f), n, 'tab-escapes')

# 复审：仍残留的控制字符
for f in sorted(glob.glob(os.path.join(d, '*.tex'))):
    with open(f, 'rb') as fh:
        data = fh.read()
    left = sum(1 for b in data if b < 32 and b not in (10, 13))
    if left:
        print('REMAINS', os.path.basename(f), left)
print('done')
