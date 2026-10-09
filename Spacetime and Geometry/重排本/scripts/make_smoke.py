# -*- coding: utf-8 -*-
"""生成冒烟编译壳：复制 main.tex 导言区，只 \\input 指定章节。
用法：python scripts/make_smoke.py ch00_front ch01 ...  -> smoke.tex
ch00_front 保持原书顺序（前言在目录前），其余章排在目录后。
"""
import io
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    mainsrc = io.open(os.path.join(BASE, "main.tex"), encoding="utf-8").read()
    head, _ = mainsrc.split(r"\begin{document}", 1)
    front = [a for a in args if a.startswith("ch00")]
    rest = [a for a in args if not a.startswith("ch00")]
    body = "\\begin{document}\n\\frontmatter\n"
    for a in front:
        body += f"\\input{{chapters/{a}}}\n"
    body += "\\tableofcontents\n"
    for a in rest:
        body += f"\\input{{chapters/{a}}}\n"
    body += "\n\\end{document}\n"
    io.open(os.path.join(BASE, "smoke.tex"), "w", encoding="utf-8").write(
        head + body)
    print("smoke.tex <-", args or "(toc only)")

if __name__ == "__main__":
    main()
