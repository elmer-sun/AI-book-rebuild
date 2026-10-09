# -*- coding: utf-8 -*-
"""调试：用导出器同款逻辑走一遍 ch10.tex，打印每个 figure 命中/跳过及游标异常。"""
import io
import re

src = r"E:\AI整理书籍\文小刚\重排本\chapters\ch10.tex"
lines = io.open(src, encoding="utf-8").read().split("\n")
i, n = 0, len(lines)
math_names = ("equation", "align", "gather", "cases", "array",
              "aligned", "Bmatrix", "pmatrix", "matrix")
figs = []
while i < n:
    s = lines[i].strip()
    menv = re.match(r"\\begin\{([a-zA-Z*]+)\}", s)
    if menv and any(menv.group(1).startswith(e) for e in math_names):
        env = menv.group(1)
        depth, j = 1, i + 1
        while j < n:
            t = lines[j].strip()
            if t == "\\begin{" + env + "}":
                depth += 1
            if t == "\\end{" + env + "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        print(f"math {env} @{i+1}->{j+1} 行数{len(lines[i:j+1])}")
        i = j + 1
        continue
    if s.startswith("\\begin{figure}"):
        figs.append(i + 1)
        j = i + 1
        while j < n and not lines[j].strip().startswith("\\end{figure}"):
            j += 1
        i = j + 1
        continue
    i += 1
print("figures命中:", figs)
