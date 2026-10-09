# -*- coding: utf-8 -*-
"""校对修复第二轮：全局搜索替换（parts + chapters 直写文件）"""
import io
import os

ROOT = r"E:\AI整理书籍\齐曼\重排本\chapters"
FILES = []
for d in (os.path.join(ROOT, "parts"), ROOT):
    for f in sorted(os.listdir(d)):
        if f.endswith(".tex"):
            FILES.append(os.path.join(d, f))

n = 0


def fix_all(old, new, expect=1):
    """在所有 tex 文件中替换 old→new，报告命中"""
    global n
    hits = 0
    for p in FILES:
        s = io.open(p, encoding="utf-8").read()
        if old in s:
            c = s.count(old)
            s = s.replace(old, new)
            io.open(p, "w", encoding="utf-8").write(s)
            print("ok [%s] x%d: %s..." % (os.path.basename(p), c, old[:36]))
            hits += c
    if expect and hits == 0:
        print("MISS: %s..." % old[:40])
    n += hits
    return hits


# P1
fix_all("\\propto\\mathcal{E}^{3/2}", "\\propto\\mathcal{E}^{1/2}")
fix_all("如同用高频电\n场", "如同用长波长的高频电场\n")
fix_all("如同用高频电", "如同用长波长的高频电")
# 温度度衍字：ch11_b 末行以"随温度"结束 + ch11_c JOIN"度的变化"
p_b = os.path.join(ROOT, "parts", "ch11_b.tex")
s = io.open(p_b, encoding="utf-8").read()
if s.rstrip("\n").endswith("其中计及能隙随温度"):
    s = s.rstrip("\n")[:-1] + "\n"   # 去掉末尾"度"
    io.open(p_b, "w", encoding="utf-8").write(s)
    print("ok [ch11_b.tex]: 去衍字'度'")
    n += 1
# \AA 残留
fix_all("（5000 \\AA）", "（5000 Å）")
fix_all("5000 \\AA", "5000 Å")
# ch10_f JOIN 补正（ch10_e 末已改"这是其"）
p_f = os.path.join(ROOT, "parts", "ch10_f.tex")
s = io.open(p_f, encoding="utf-8").read()
if "%JOIN%\n果：Heisenberg" in s:
    s = s.replace("%JOIN%\n果：Heisenberg", "%JOIN%\n必然后果：Heisenberg")
    io.open(p_f, "w", encoding="utf-8").write(s)
    print("ok [ch10_f.tex]: JOIN 补正")
    n += 1
# (10.85) 译注
fix_all("\\frac{2/p}{\\ln(1 - 2/p)},\n\\tag{10.85}\n\\end{equation*}",
        "\\frac{2/p}{\\ln(1 - 2/p)},\n\\tag{10.85}\n\\end{equation*}\n"
        "（译注：按准化学近似的标准结果，右端应为 $-2/p\\big/\\ln\\frac{p}{p-2}$，"
        "原书疑漏负号。）")
# P2
fix_all("Ginsburg--Landau", "Ginzburg--Landau")
fix_all("被晶序偏离处净散射的矩阵元的估计", "被对晶体序的偏离所散射的净矩阵元的估计")
fix_all("拥有一罐极低温度", "拥有一团极低温度")
fix_all("能带结构计算（§5.3）", "能带结构计算（§5.3；译注：疑为 §3.3 之误印）")
# P3
fix_all("烦冗", "繁冗")
fix_all("中心对偶力", "中心成对力")
fix_all("积分回归到", "积分后正确地回到")
fix_all("金属薄片、且磁场", "金属薄片，且磁场")
fix_all("闭合轨迹其直径", "闭合轨迹，其直径")
fix_all("是波函数在核处的幅度", "是波函数在核处的模方")
fix_all("Bardeen、Cooper 和Schrieffer", "Bardeen、Cooper 和 Schrieffer")
fix_all("\\mathbf{A}(\\mathbf{r}):$", "\\mathbf{A}(\\mathbf{r})$")

print("TOTAL round2:", n)
