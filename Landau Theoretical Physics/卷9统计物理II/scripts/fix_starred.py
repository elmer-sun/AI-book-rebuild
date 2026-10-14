# -*- coding: utf-8 -*-
"""星号节改造：\section{X$^{*}$} → \section*{X} + 手写 toc 行；
节内编号公式 equation → equation* + \tag{35*.k}/\tag{74*.k}。
（\thesection 局部重定义方案败于 toc 延迟展开，弃用）"""
import io, re, sys

RB = r"E:\AI整理书籍\朗道理论物理教程\卷9统计物理II\重排本\chapters"
BS = chr(92)

JOBS = [
    ("ch03b.tex", "35", "二维系统的超流性"),
    ("ch07.tex", "74", "自旋哈密顿量的反铁磁态"),
]

for fn, num, title in JOBS:
    path = RB + chr(92) + fn
    s = io.open(path, encoding="utf-8").read()
    # 1) 定位星号节头（现有补丁块）
    m = re.search(
        re.escape(BS + "begingroup") + r".*?" +
        re.escape(BS + "section{" + title + "}"), s, re.S)
    assert m, fn + ": header block not found"
    head_new = (BS + "section*{" + title + "}" + chr(10) +
                BS + "phantomsection" + chr(10) +
                BS + "addcontentsline{toc}{section}" +
                "{\\numberline {§" + num + "*" + "}" + title + "}")
    s = s[:m.start()] + head_new + s[m.end():]
    # 2) 尾部 \endgroup + addtocounter → 仅 \endgroup（equation* 不进计数，无须归位）
    s = s.replace(BS + "endgroup" + chr(10) + BS + "addtocounter{section}{-1}",
                  BS + "endgroup")
    # 3) 区域内编号公式 → equation* + \tag{num*.k}
    beg = s.index(head_new)
    end = s.index(BS + "endgroup", beg)
    region = s[beg:end]
    k = 0
    out = []
    i = 0
    for mm in re.finditer(re.escape(BS + "begin{equation}") + r"(?!\*)|\" + \"", region):
        pass  # placeholder（真实循环如下）
    # 用顺序扫描避免正则回溯坑
    pos = 0
    pattern = re.compile(re.escape(BS + "begin{equation}") + r"(?!\*)" +
                         r"|" + re.escape(BS + "end{equation}") + r"(?!\*)")
    for mm in pattern.finditer(region):
        tok = mm.group(0)
        if tok.startswith(BS + "begin"):
            k += 1
            out.append(region[pos:mm.start()])
            out.append(BS + "begin{equation*}")
        else:
            out.append(region[pos:mm.start()])
            out.append(BS + "tag{" + num + "*." + str(k) + "}" + chr(10) +
                       BS + "end{equation*}")
        pos = mm.end()
    out.append(region[pos:])
    region_new = "".join(out)
    s = s[:beg] + region_new + s[end:]
    io.open(path, "w", encoding="utf-8").write(s)
    print(fn, ": starred eqs tagged =", k)
