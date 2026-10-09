# -*- coding: utf-8 -*-
"""把 chapters/parts/*.tex 中文正文里成对的英文直引号 "..." 替换为中文弯引号“...”。
规则：
- 跳过显示数学环境内部（equation*/align*/align/gather*/subequations 等）；
- 跳过 \% 注释行、\\texttt{...} 内部（URL 等不含 " 但保险起见仍处理成对逻辑）；
- 在文本区域内按出现顺序交替替换：第奇数个 " → “，第偶数个 " → ”（逐文件累计，
  假定引号总在段内成对闭合；若某文件结束时状态未闭合则告警）。
"""
import io
import os
import re

BASE = r"E:\AI整理书籍\卡罗尔\重排本\chapters\parts"

MATH_BEGIN = re.compile(r"\\begin\{(equation\*?|align\*?|alignat\*?|gather\*?|multline\*?|eqnarray\*?|displaymath\*?|math)\}")
MATH_END = re.compile(r"\\end\{(equation\*?|align\*?|alignat\*?|gather\*?|multline\*?|eqnarray\*?|displaymath\*?|math)\}")

def process(path):
    s = io.open(path, encoding="utf-8").read()
    lines = s.split("\n")
    in_math = False
    open_state = False  # False -> 下一个 " 是开引号
    n_rep = 0
    for i, ln in enumerate(lines):
        stripped = ln.lstrip()
        if stripped.startswith("%"):
            continue
        if not in_math and MATH_BEGIN.search(ln) and not MATH_END.search(ln):
            in_math = True
        if in_math:
            if MATH_END.search(ln):
                in_math = False
            continue
        if '"' not in ln:
            continue
        out = []
        for ch in ln:
            if ch == '"':
                out.append("“" if not open_state else "”")
                open_state = not open_state
                n_rep += 1
            else:
                out.append(ch)
        lines[i] = "".join(out)
    if open_state:
        print(f"  WARN {os.path.basename(path)}: 引号未闭合（奇数个）")
    if n_rep:
        io.open(path, "w", encoding="utf-8").write("\n".join(lines))
    return n_rep

total = 0
for fn in sorted(os.listdir(BASE)):
    if fn.endswith(".tex"):
        n = process(os.path.join(BASE, fn))
        if n:
            print(f"{fn}: {n} 个直引号已转换")
        total += n
print(f"TOTAL: {total}")
