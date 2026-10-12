# -*- coding: utf-8 -*-
"""judge 修复批次1（卷3）：图块后移一段回填页底空白 + 表10 表题防孤悬。
- ch12 fig32: 移到 S_n=C_nσ_h 公式块之后
- ch12 fig39: 移到 XI 群 O 第二段（很易看出…）之后
- ch17b fig49: 移到 "由此可见…常数" 公式块之后
- ch14 表10: center 表题后加 \nopagebreak
"""
import io, re

BS = chr(92)
FIG = re.compile(
    r"\n" + re.escape(BS + "par" + BS + "nopagebreak" + BS + "noindent" +
                      BS + "begin{minipage}{") + r"[^\n]*?fig(\d+)\.pdf[^\n]*?" +
    re.escape(BS + "end{minipage}" + BS + "par" + BS + "nopagebreak") + r"\n")


def move_fig_after(path, figno, anchor_sub):
    s = io.open(path, encoding="utf-8").read()
    m = None
    for mm in FIG.finditer(s):
        if mm.group(1) == str(figno):
            m = mm
            break
    assert m, f"fig{figno} block not found in {path}"
    block = m.group(0)
    s2 = s[:m.start()] + "\n" + s[m.end():]
    i = s2.find(anchor_sub)
    assert i >= 0, f"anchor not found: {anchor_sub[:30]}"
    j = s2.find(BS + "end{equation}", i)
    assert j >= 0, "no equation end after anchor"
    j = s2.index("\n", j) + 1
    s2 = s2[:j] + block + s2[j:]
    io.open(path, "w", encoding="utf-8").write(s2)
    print(f"{path}: fig{figno} moved after anchor")


def add_nopagebreak_after_center(path, cap_sub):
    s = io.open(path, encoding="utf-8").read()
    old = (BS + "begin{center}\n" + cap_sub + "\n" + BS + "end{center}\n")
    assert old in s, "center caption not found"
    new = old + BS + "nopagebreak" + "\n"
    s = s.replace(old, new)
    io.open(path, "w", encoding="utf-8").write(s)
    print(f"{path}: nopagebreak added after caption")


CH = r"E:\AI整理书籍\朗道理论物理教程\卷3量子力学\重排本\chapters"
move_fig_after(CH + r"\ch12.tex", 32,
               "我们用记号 $S_n$ 代表旋转-反射变换")
move_fig_after(CH + r"\ch12.tex", 39,
               "很易看出，所有的同阶轴是等价的")
move_fig_after(CH + r"\ch17b.tex", 49,
               "由此可见，当有库仑作用存在时")
add_nopagebreak_after_center(CH + r"\ch14.tex",
                             "{\\heiti 表 10}" + BS + "quad $6j$ 符号表")
