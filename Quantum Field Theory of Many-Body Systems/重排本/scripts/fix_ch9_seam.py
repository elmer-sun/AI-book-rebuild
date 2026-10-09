# -*- coding: utf-8 -*-
"""ch9_b→ch9_c 接缝修复：ch9_b 末尾的 keypoints 环境保持开放（删去 \\end{keypoints}），
由 ch9_c 的 %JOIN% 第三条要点接续并闭合。"""
import io

p = r"E:\AI整理书籍\文小刚\重排本\chapters\parts\ch9_b.tex"
s = io.open(p, encoding="utf-8").read()
old = "\\item 共线的 $SU(2)$ 通量把 $SU(2)$ 规范结构破缺为 $U(1)$ 规范结构。\n\\end{keypoints}\n"
assert s.count(old) == 1, "ch9_b 末尾模式未找到"
s = s.replace(old, "\\item 共线的 $SU(2)$ 通量把 $SU(2)$ 规范结构破缺为 $U(1)$ 规范结构。\n")
io.open(p, "w", encoding="utf-8").write(s)
print("ch9_b: 末尾 keypoints 改为开放，待 ch9_c JOIN 闭合")
