# -*- coding: utf-8 -*-
"""脚注编号按页校验：从 PDF 文本层提取每页脚注区圈码序列，
校验每页脚注从①起连续编号（①,②,...）。"""
import subprocess, re, sys

pdf = sys.argv[1]
lo, hi = int(sys.argv[2]), int(sys.argv[3])
CIRC = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮"
bad = []
nfn = 0
for p in range(lo, hi + 1):
    r = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-enc", "UTF-8", pdf, "-"],
                       capture_output=True)
    txt = r.stdout.decode("utf-8", "ignore")
    # 脚注区：pdftotext 把脚注排页面文本之后；提取所有圈码出现序列
    marks = [ch for ch in txt if ch in CIRC]
    if not marks:
        continue
    nfn += len(marks)
    # 页面正文+脚注的圈码总序列应为 ①,②,...,⑩ 循环？不——正文标记与脚注区标记各出现一次，
    # 同一页有 n 个脚注则正文 n 个标记 + 脚注区 n 个标记，且都按同序。
    # 校验：序列去半后应形如 ①②..n①②..n 或 ①②..n（仅脚注）——宽松校验：
    # 每个"半序列"须从①连续递增。切分：找递增段。
    seq = [CIRC.index(ch) + 1 for ch in marks]
    # 简单校验：所有局部极大段从1开始
    start_ok = seq[0] == 1
    # 检查第二轮的起点
    runs = []
    prev = 0
    for v in seq:
        if v == 1:
            runs.append([])
        if runs:
            runs[-1].append(v)
        prev = v
    ok = start_ok and all(rr == list(range(1, len(rr) + 1)) for rr in runs)
    if not ok:
        bad.append((p, seq[:14]))
print("pages with marks checked; total marks:", nfn)
print("bad pages:", len(bad))
for p, s in bad[:15]:
    print("  pg", p, s)
