# -*- coding: utf-8 -*-
"""把装配后章节文件中的 %FIG{key}: caption 标记替换为占位 figure 环境
（翻译交付阶段用；插图重绘完成后改用 apply_figs.py 换真图）。
用法：python apply_figs_placeholder.py [ch01.tex ...]（缺省全部 ch*.tex）
注意：只处理尚未替换的 %FIG 标记（幂等：替换产物不再含标记）。"""
import io
import os
import re
import sys

BASE = r"E:\AI整理书籍\文小刚\重排本"
CH = os.path.join(BASE, "chapters")

pat = re.compile(r"^%FIG\{([^}]+)\}:\s*(.*)$", re.M)


def clean_cap(key, cap):
    if cap.startswith("{") and cap.endswith("}"):
        cap = cap[1:-1].strip()
    cap = re.sub(rf"^图\s*{re.escape(key)}\s*[　\s]*", "", cap)
    cap = cap.lstrip("．.、 ")
    cap = re.sub(r"（([a-e])）", r"(\1)", cap)
    if not cap:
        cap = "（原书此图无图注。）"
    return cap


def process(fn):
    p = os.path.join(CH, fn)
    s = io.open(p, encoding="utf-8").read()
    n_before = len(pat.findall(s))

    def repl(m):
        key = m.group(1)
        cap = clean_cap(key, m.group(2).strip())
        body = ("\\centering \\vspace{0.5em} {\\large 图 " + key + "}"
                " \\vspace{0.3em}\\\\ （插图重绘中）\\vspace{0.5em}")
        return (
            "\\begin{figure}[H]\n\\centering\n"
            "\\fbox{\\parbox[c][4.2cm][c]{0.72\\textwidth}{" + body + "}}\n"
            f"\\caption*{{图 {key}\\quad {cap}}}\n"
            "\\end{figure}"
        )

    s2 = pat.sub(repl, s)
    if s2 != s:
        io.open(p, "w", encoding="utf-8").write(s2)
    n_left = len(pat.findall(s2))
    print(f"{fn}: replaced {n_before - n_left}; {n_left} markers left")


targets = [a for a in sys.argv[1:] if a.endswith(".tex")] or \
          [f for f in os.listdir(CH) if re.match(r"ch\d+.*\.tex$", f)]
for fn in sorted(targets):
    process(fn)
