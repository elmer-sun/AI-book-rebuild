# -*- coding: utf-8 -*-
"""解析 main.log：把每处 Overfull 映射到 (章节文件, 行号, 溢出pt)，按大小排序输出。
（正则一律不用反斜杠+括号组合，规避工具层转义问题。）"""
import io
import re

LOG = r"E:\AI整理书籍\文小刚\重排本\main.log"

cur = None
rows = []
pat_file1 = "(./chapters/"
pat_file2 = "(/chapters/"
pat_ov = re.compile(r"Overfull .hbox .([0-9.]+)pt too wide. in paragraph at lines ([0-9]+)--([0-9]+)")
for line in io.open(LOG, encoding="utf-8", errors="ignore"):
    for pf in (pat_file1, pat_file2):
        k = line.find(pf)
        if k >= 0:
            seg = line[k + len(pf):]
            cur = seg.split("/")[0].split(")")[0]
    m2 = pat_ov.search(line)
    if m2 and cur:
        rows.append((float(m2.group(1)), cur, int(m2.group(2))))
rows.sort(reverse=True)
for pt, fn, ln in rows[:14]:
    print(f"{pt:7.1f}pt  {fn}:{ln}")
print("总数", len(rows), "| >9pt:", sum(1 for r in rows if r[0] > 9))
