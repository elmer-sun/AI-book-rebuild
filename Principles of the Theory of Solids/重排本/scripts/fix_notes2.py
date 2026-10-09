# -*- coding: utf-8 -*-
"""撤除误插入公式环境的译注，并在正确的公式后重加"""
import io
import os
import re

P = r"E:\AI整理书籍\齐曼\重排本\chapters\parts"
NOTE78 = re.compile(r"%\n（译注：按式 \(7\.78\)[^）]*。）")
NOTE39 = re.compile(r"%\n（译注：按式 \(7\.39\)[^）]*。）")

for fn in ("ch7_a.tex", "ch7_b.tex", "ch7_c.tex", "ch7_d.tex", "ch7_e.tex"):
    p = os.path.join(P, fn)
    s = io.open(p, encoding="utf-8").read()
    s2 = NOTE78.sub("", s)
    s2 = NOTE39.sub("", s2)
    if s2 != s:
        io.open(p, "w", encoding="utf-8").write(s2)
        print("cleaned", fn)

# (7.79) 在 ch7_c：找 \tag{7.79} 所在 equation*，其后加译注
p = os.path.join(P, "ch7_c.tex")
s = io.open(p, encoding="utf-8").read()
k = s.find("\\tag{7.79}")
if k >= 0:
    e = s.find("\\end{equation*}", k)
    note = "\n（译注：按式 (7.78) 代入 (7.20)，第二项似应为 $e\\tau/\\hbar$；原书印作 $e^{2}\\tau$。）"
    if e >= 0 and "译注" not in s[k:e + 20]:
        s = s[:e + len("\\end{equation*}")] + note + s[e + len("\\end{equation*}"):]
        io.open(p, "w", encoding="utf-8").write(s)
        print("note added to (7.79)")

# (7.52) 在 ch7_b：找 \tag{7.52} 所在 equation*，其后加译注
p = os.path.join(P, "ch7_b.tex")
s = io.open(p, encoding="utf-8").read()
k = s.find("\\tag{7.52}")
if k >= 0:
    e = s.find("\\end{equation*}", k)
    note = "\n（译注：按式 (7.51) 的 $\\tau\\propto\\mathcal{E}^{3/2}m^{*1/2}$ 代入 (7.38)、(7.39)，"
    "应为 $\\mu\\propto T^{3/2}m^{*-1/2}$；原书印作 $m^{*3/2}$，疑误。）"
    if e >= 0 and "译注" not in s[k:e + 20]:
        s = s[:e + len("\\end{equation*}")] + note + s[e + len("\\end{equation*}"):]
        io.open(p, "w", encoding="utf-8").write(s)
        print("note added to (7.52)")
print("done")
