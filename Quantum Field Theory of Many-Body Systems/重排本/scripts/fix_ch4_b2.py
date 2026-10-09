# -*- coding: utf-8 -*-
"""ch4_b 第二刀：把仍留在文件顶部的收尾句移到正文末尾。"""
import io

p = r"E:\AI整理书籍\文小刚\重排本\chapters\parts\ch4_b.tex"
s = io.open(p, encoding="utf-8").read()
sent = "为了得到自由费米子的线性响应，我们需要计算密度响应函数 $\\Pi^{00}$。在 $t$--$\\pmb{k}$ 空间中，密度响应函数可以"
i = s.find(sent)
assert i > 0, "ch4_b 未找到收尾句"
head = s[:i]
first_nl = head.find("\n")
assert first_nl >= 0 and head[:first_nl].startswith("%"), "ch4_b 首行应为注释"
rest = s[i + len(sent):]
if rest.startswith("\n\n"):
    rest = rest[1:]          # 连同其后一个空行一并删
elif rest.startswith("\n"):
    rest = "\n"
s = head + rest
s = s.rstrip("\n") + "\n" + sent + "\n"
io.open(p, "w", encoding="utf-8").write(s)
print("ch4_b: 顶部句子已移到正文末尾")
