# -*- coding: utf-8 -*-
"""精确版：跟踪数学环境状态（display env + 行内 $ 奇偶 + \text{ 内排除），
报告数学环境中 \text{} 之外的全角标点。"""
import io, re, os, sys

BASE = sys.argv[1]
FW = "，；：（）？！"
ENV = r"(equation|align|gather|multline|aligned|gathered|array|cases|split|dmath)"
BENV = re.compile(r"\\begin\{" + ENV + r"\}")
EENV = re.compile(r"\\end\{" + ENV + r"\}")
TOPEN = re.compile(r"\\text\s*\{")

for fn in sys.argv[2:]:
    p = os.path.join(BASE, "chapters", fn)
    lines = io.open(p, encoding="utf-8").read().split("\n")
    disp = 0
    inline = 0  # 0 偶 1 奇（跨行持续）
    for i, l in enumerate(lines):
        # 先扫 display 环境增减（同一行可开可闭）
        opens = len(BENV.findall(l))
        closes = len(EENV.findall(l))
        # \text{...} 区间收集（粗略：\text{ 至配对}，假设单层）
        spans = []
        for m in TOPEN.finditer(l):
            depth = 1
            j = m.end()
            while j < len(l) and depth:
                if l[j] == "{":
                    depth += 1
                elif l[j] == "}":
                    depth -= 1
                j += 1
            spans.append((m.start(), j))
        def in_text(pos):
            return any(a <= pos < b for a, b in spans)
        state_disp0 = disp
        # 逐字符扫描
        k = 0
        n_dollar = 0
        # display 增减放在字符循环前处理会失真；改为：本行 display 状态取 (disp) 与 (disp+opens-closes)
        cur_disp = disp
        for m in re.finditer(r"[\$" + FW + r"]", l):
            ch = m.group(0)
            pos = m.start()
            if ch == "$":
                if cur_disp == 0:
                    n_dollar += 1
                continue
            inmath = (cur_disp > 0) or (n_dollar % 2 == 1)
            if inmath and not in_text(pos):
                ctx = l[max(0, pos - 34):pos + 12]
                print(f"{fn}:{i+1}: [{ch}] …{ctx}…")
        disp = disp + opens - closes
        if disp < 0:
            disp = 0
        n_dollar = l.count("$")
        # 行内奇偶延续：若行末处于奇数 $，下一行 inline=1，否则 0
        inline = (disp == 0 and n_dollar % 2 == 1)
        # 简化：把 inline 融进 n_dollar 每行重置 —— 朗道排版中行内公式极少跨行，接受此近似
