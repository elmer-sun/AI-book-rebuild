# -*- coding: utf-8 -*-
"""找数学环境（$...$、equation/aligned 等）内的全角标点——Times 缺字形会直接丢字。"""
import io, re, glob, os

BASE = os.path.dirname(os.path.abspath(__file__)) + r"\..\重排本\chapters"
FW = "，；：（）？！"
for f in sorted(glob.glob(os.path.join(BASE, "*.tex"))):
    lines = io.open(f, encoding="utf-8").read().split("\n")
    depth_math = 0
    env_stack = []
    for i, l in enumerate(lines):
        for ch in l:
            pass
        # 粗粒度：逐行判断是否处于 display 环境或行内 $ 内（数学一行内闭合占多数）
        s = l
        # display 环境跟踪
        if re.search(r"\\begin\{(equation|aligned|gather|array|cases|split|multline)", s):
            env_stack.append(1)
        if re.search(r"\\end\{(equation|aligned|gather|array|cases|split|multline)", s):
            if env_stack:
                env_stack.pop()
        in_disp = bool(env_stack)
        # 行内数学：按 $ 计数奇偶
        n_dollar = s.count("$")
        odd = n_dollar % 2 == 1
        if in_disp or odd or depth_math:
            for m in re.finditer("[" + FW + "]", s):
                ctx = s[max(0, m.start() - 30):m.start() + 15]
                print(f"{os.path.basename(f)}:{i+1}: {m.group(0)}  …{ctx}…")
        if odd:
            depth_math = 1 - depth_math
