# -*- coding: utf-8 -*-
"""ch17a 衔接修复：把误排在 §123 末尾的二维散射习题移到 §124 末尾
（原书该题在 §124 题1，§132 题7 引用'§124 的题目中的(1)式'）。"""
import io

p = r"E:\AI整理书籍\朗道理论物理教程\卷3量子力学\重排本\chapters\ch17a.tex"
lines = io.open(p, encoding="utf-8").read().split("\n")
BEGIN = chr(92) + "begin{xiti}"
END = chr(92) + "end{xiti}"
i_begin = next(i for i, l in enumerate(lines) if l.strip() == BEGIN)
i_end = next(i for i, l in enumerate(lines) if l.strip() == END)
block = lines[i_begin:i_end + 1]
assert any("二维情况" in l for l in block), "wrong block"
del lines[i_begin:i_end + 1]
while i_begin < len(lines) and lines[i_begin].strip() == "":
    del lines[i_begin]
i_sec = next(i for i, l in enumerate(lines)
             if l.startswith(chr(92) + "section{散射的幺正条件}"))
lines[i_sec:i_sec] = block + [""]
io.open(p, "w", encoding="utf-8").write("\n".join(lines))
print("OK: xiti block moved before 散射的幺正条件; new file lines:", len(lines))
