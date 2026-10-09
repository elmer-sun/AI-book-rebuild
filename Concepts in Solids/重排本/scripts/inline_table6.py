# -*- coding: utf-8 -*-
# ch2_B4b.tex: 表6浮动体嵌入段内（去两侧空行）
import io

p = r"E:\AI整理书籍\安德森\重排本\chapters\parts\ch2_B4b.tex"
s = io.open(p, encoding="utf-8").read()

BS = chr(92)
old = "在这一系列的中段附近，\n\n" + BS + "begin{table}[htbp]"
new = "在这一系列的中段附近，\n" + BS + "begin{table}[htbp]"
assert old in s, "pre-table gap not found"
s = s.replace(old, new, 1)

old2 = BS + "end{table}\n\n% 上句未完"
new2 = BS + "end{table}\n% 上句未完"
assert old2 in s, "post-table gap not found"
s = s.replace(old2, new2, 1)

io.open(p, "w", encoding="utf-8").write(s)
print("table6 inlined into paragraph")
