# -*- coding: utf-8 -*-
# 修复 ch2_B4b.tex 中表5/表6 的浮动环境
import io

p = r"E:\AI整理书籍\安德森\重排本\chapters\parts\ch2_B4b.tex"
s = io.open(p, encoding="utf-8").read()

# --- 表 5：修复被污染的头部 ---
bad5 = "\\begin{table}[htbp]\n\\centering\n表 5\n\n{\\bfseries 表~6}\\[5pt]\n\\begin{tabular}{lccccc}"
good5 = "\\begin{table}[htbp]\n\\centering\n{\\bfseries 表~5}\\\\[5pt]\n\\begin{tabular}{lccccc}"
assert bad5 in s, "bad5 pattern not found"
s = s.replace(bad5, good5, 1)

# --- 表 6：center 块 -> table 浮动 + 标题 ---
i = s.find("见表 6")
assert i > 0
b = s.find("\\begin{center}", i)
e = s.find("\\end{center}", i)
assert 0 < b < e
block = s[b:e + len("\\end{center}")]
newblock = ("\\begin{table}[htbp]\n\\centering\n{\\bfseries 表~6}\\\\[5pt]\n"
            + block[len("\\begin{center}"):].lstrip("\n")
            ).replace("\\end{center}", "\\end{table}", 1)
s = s.replace(block, newblock, 1)

io.open(p, "w", encoding="utf-8").write(s)
# 自检打印
i5 = s.find(good5)
print(s[i5:i5+120])
print("...")
i6 = s.find(newblock)
print(newblock[:200])
