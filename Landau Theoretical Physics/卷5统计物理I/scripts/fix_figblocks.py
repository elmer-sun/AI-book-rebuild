# -*- coding: utf-8 -*-
"""卷5：把所有 center 图块统一转为原子 minipage 结构（图与图注不可分离）。"""
import io, re, glob, os

BS = chr(92)
PAT = re.compile(
    re.escape(BS + "begin{center}") +
    r"\s*" + re.escape(BS + "includegraphics[width=") +
    r"([0-9.]+)cm\]\{(fig\d+\.pdf)\}" +
    r"\s*" + re.escape(BS + BS) + r"\{" +
    r"(" + re.escape(BS + "small 图 ") + r"\d+" + r")\}" +
    r"\s*" + re.escape(BS + "end{center}"))

CH = r"E:\AI整理书籍\朗道理论物理教程\卷5统计物理I\重排本\chapters"
total = 0
for f in sorted(glob.glob(os.path.join(CH, "*.tex"))):
    s = io.open(f, encoding="utf-8").read()
    def repl(m):
        w, fig, cap = m.group(1), m.group(2), m.group(3)
        return (BS + "par" + BS + "nopagebreak" + BS + "noindent" +
                BS + "begin{minipage}{" + BS + "linewidth}" + BS + "centering" +
                BS + "includegraphics[width=" + w + "cm]{" + fig + "}" +
                BS + BS + chr(91) + "0.3em" + chr(93) + "{" + cap + "}" +
                BS + "end{minipage}" + BS + "par" + BS + "nopagebreak")
    s2, n = PAT.subn(repl, s)
    if n:
        io.open(f, "w", encoding="utf-8").write(s2)
        print(os.path.basename(f), "converted:", n)
        total += n
print("total converted:", total)
