# -*- coding: utf-8 -*-
"""跨行精确搜索：跟踪 display 数学环境（\begin{equation}...\end{equation} 可跨行），
报告环境内所有 \text{} 之外的全角标点。"""
import io, re, sys

p = sys.argv[1]
FW = "，；：（）？！"
lines = io.open(p, encoding="utf-8").read().split("\n")
ENV = r"(equation\*?|align\*?|gather\*?|multline\*?|aligned|gathered|array|cases|split)"
depth = 0
env_line = []
for i, l in enumerate(lines):
    for m in re.finditer(r"\\(begin|end)\{" + ENV + r"\}", l):
        if m.group(1) == "begin":
            depth += 1
            env_line.append(i + 1)
        else:
            depth -= 1
            if env_line:
                env_line.pop()
    if depth > 0:
        # 本行处于环境内：排除 \text{...} 区间与 % 注释
        code = l.split("%")[0] if "% FIG" not in l else l
        spans = []
        for m in re.finditer(r"\\text\s*\{", code):
            d = 1
            j = m.end()
            while j < len(code) and d:
                if code[j] == "{":
                    d += 1
                elif code[j] == "}":
                    d -= 1
                j += 1
            spans.append((m.start(), j))
        # \tag{...} 区间同样排除（tag 内不该有全角，但保险）
        for m in re.finditer(r"\\tag\s*\{", code):
            j = code.find("}", m.end())
            if j > 0:
                spans.append((m.start(), j + 1))
        for m in re.finditer("[" + FW + "]", code):
            if any(a <= m.start() < b for a, b in spans):
                continue
            ctx = code[max(0, m.start() - 40):m.start() + 14]
            print(f"line {i+1} (env from {env_line[-1] if env_line else '?'}): [{m.group(0)}] …{ctx}…")
