# -*- coding: utf-8 -*-
"""把所有含 \\includegraphics 的 center 图块包成原子 minipage（图与图注不可跨页分离）。
幂等：已是 minipage 结构的块跳过。"""
import io, re, glob, os

CH = r"E:\AI整理书籍\李正中\重排本\chapters"
PAT = re.compile(r"\\begin\{center\}\s*((?:(?!\\end\{center\}).)*?\\includegraphics(?:(?!\\end\{center\}).)*?)\s*\\end\{center\}", re.S)
WIDTH = re.compile(r"\\includegraphics\[[^\]]*width\s*=\s*([0-9.]+(?:\\textwidth|[0-9.]*cm))\]")

total = 0
for fn in sorted(glob.glob(os.path.join(CH, "*.tex"))):
    if fn.endswith("symbols.tex"):
        continue
    s = io.open(fn, encoding="utf-8").read()
    made = []
    def repl(m):
        global total
        body = m.group(1)
        if "\\begin{minipage}" in body:
            return m.group(0)  # 已处理
        wm = WIDTH.search(body)
        w = wm.group(1) if wm else "0.8\\textwidth"
        total += 1
        made.append(w)
        return ("\\begin{center}\n\\begin{minipage}{" + w + "}\n\\centering\n"
                + body.strip() + "\n\\end{minipage}\n\\end{center}")
    s2 = PAT.sub(repl, s)
    if s2 != s:
        io.open(fn, "w", encoding="utf-8").write(s2)
        print(f"{os.path.basename(fn)}: {len(made)} blocks -> minipage")
print("TOTAL wrapped:", total)
