# -*- coding: utf-8 -*-
# ch2_B4b.tex: center 块的表 6 改为 table[htbp] 浮动
import io

p = r"E:\AI整理书籍\安德森\重排本\chapters\parts\ch2_B4b.tex"
s = io.open(p, encoding="utf-8").read()

i = s.find("表 6")
assert i > 0, "table caption not found"
# 向前找最近的 \begin{center}
b = s.rfind("\\begin{center}", 0, i)
assert b > 0, "begin{center} not found"
# 向后找配对的 \end{center}
e = s.find("\\end{center}", i)
assert e > 0, "end{center} not found"

block = s[b:e + len("\\end{center}")]
newblock = block.replace("\\begin{center}", "\\begin{table}[htbp]\n\\centering", 1)
# 在 tabular 前插入标题行（若尚无）
if "{\\bfseries 表~6}" not in newblock and "\\bfseries 表 6" not in newblock:
    k = newblock.find("\\begin{tabular}")
    newblock = newblock[:k] + "{\\bfseries 表~6}\\[5pt]\n" + newblock[k:]
newblock = newblock.replace("\\end{center}", "\\end{table}", 1)
# 去掉原 center 内孤立的“表 6”文字行（已用 \bfseries 标题替代）
newblock = newblock.replace("表 6\n\n", "", 1)

s = s.replace(block, newblock, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("done; new block head:")
print(newblock[:220])
