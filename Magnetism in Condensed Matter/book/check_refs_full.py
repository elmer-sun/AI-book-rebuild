# -*- coding: utf-8 -*-
"""引用闭环检查：正文引用的 图 x.y / 式 (x.y) 是否都有对应编号"""
import io, re, glob

B = chr(92)
import os
os.chdir(r'E:\AI整理书籍\磁学\book')
files = ['ch1.tex', 'ch2.tex', 'ch3.tex', 'ch4.tex', 'ch5.tex', 'ch6.tex',
         'ch7.tex', 'ch8.tex', 'appA.tex', 'appB.tex', 'appC.tex', 'appD.tex',
         'appE.tex', 'answers.tex', 'symbols.tex', 'preface.tex']

all_text = ''
per_file = {}
for f in files:
    s = io.open(f, encoding='utf-8').read()
    per_file[f] = s
    all_text += s

# 已定义编号：tag{} 与 caption 中的 图 x.y / Table x.y / Fig. x.y
tags = set(re.findall(B * 2 + r'tag' + r'\{([^}]*)\}', all_text))
figs = set()
for m in re.findall(r'Fig\.~?([A-Z]+)?\.?\s?(\d+)\.(\d+)', all_text):
    figs.add((m[1], m[2]))
# caption 中文 “图 x.y” 不一定是定义（正文引用也是 图 x.y）——以 Fig. 为准 + 表 Table x.y
tabs = set(re.findall(r'Table\s+([A-Z]+)?\.?\s?(\d+)\.(\d+)', all_text))

# 正文引用：图 x.y（中文）
bad = []
for m in re.finditer(r'图~?(\d+)\.(\d+)', all_text):
    ch, n = m.group(1), m.group(2)
    key = '%s.%s' % (ch, n)
    if (ch, n) not in figs and key not in [t for t in tags]:
        # 检查 tag 形如 6.29
        if key not in tags:
            bad.append('图' + key)

# 式引用：(x.y) 或 式 x.y —— 检查数字型 tag 覆盖
tag_nums = set(tags)
for m in re.finditer(r'式~?\(?(\d+\.\d+)\)?', all_text):
    key = m.group(1)
    if key not in tag_nums:
        bad.append('式' + key)

# 汇总去重
from collections import Counter
c = Counter(bad)
print('可疑引用（引用了但不存在的编号）：')
for k, v in sorted(c.items()):
    print(' ', k, 'x', v)
if not c:
    print('  无 —— 引用闭环通过')
