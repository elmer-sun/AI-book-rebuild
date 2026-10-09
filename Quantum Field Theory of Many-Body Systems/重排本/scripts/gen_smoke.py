# -*- coding: utf-8 -*-
"""从 main.tex 生成 smoke.tex（同 preamble，只 input 指定章）。
用法：python gen_smoke.py ch01  ->  smoke.tex 里 \input{chapters/ch01}
"""
import io
import os
import re
import sys

BASE = r"E:\AI整理书籍\文小刚\重排本"


def main():
    ch = sys.argv[1] if len(sys.argv) > 1 else "ch01"
    s = io.open(os.path.join(BASE, "main.tex"), encoding="utf-8").read()
    head = s.split("\\begin{document}")[0]
    body = (
        "% 冒烟编译：只编当前章，验证 0 错。用法：xelatex -jobname=smoke smoke.tex ×2\n"
        + head
        + "\\begin{document}\n"
        + "\\frontmatter\n"
        + "% \\tableofcontents\n\n"
        + "\\mainmatter\n"
        + "% 在下行填要冒烟的章：\n"
        + f"\\input{{chapters/{ch}}}\n\n"
        + "\\end{document}\n"
    )
    io.open(os.path.join(BASE, "smoke.tex"), "w", encoding="utf-8").write(body)
    print(f"smoke.tex written (input {ch})")


if __name__ == "__main__":
    main()
