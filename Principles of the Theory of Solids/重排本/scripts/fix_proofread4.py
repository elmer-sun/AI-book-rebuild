# -*- coding: utf-8 -*-
"""校对修复第四轮：第6/7章（全局搜索替换）"""
import io
import os

ROOT = r"E:\AI整理书籍\齐曼\重排本\chapters"
FILES = []
for d in (os.path.join(ROOT, "parts"), ROOT):
    for f in sorted(os.listdir(d)):
        if f.endswith(".tex"):
            FILES.append(os.path.join(d, f))

n = 0


def fix_all(old, new):
    global n
    hits = 0
    for p in FILES:
        s = io.open(p, encoding="utf-8").read()
        if old in s:
            c = s.count(old)
            s = s.replace(old, new)
            io.open(p, "w", encoding="utf-8").write(s)
            print("ok [%s] x%d" % (os.path.basename(p), c))
            hits += c
    if hits == 0:
        print("MISS: %s..." % old[:40])
    n += hits


# P1
fix_all("那么就应当也应当有类似的结果", "那么就应当有类似的结果")
# P2：功函数病句
fix_all("指的是电子离开体材料中的费米能级、被带到离表面相当远处时——",
        "说的是把一个电子从体材料的费米能级带到离表面相当远处所需的能量提升——")
# P2：(7.79) e²τ 译注
fix_all("\\frac{e^{2}\\tau}{\\hbar}",
        "\\frac{e^{2}\\tau}{\\hbar}%\n（译注：按式 (7.78) 代入 (7.20)，此处似应为 $e\\tau/\\hbar$；"
        "原书印作 $e^{2}\\tau$。）")
# P2：(7.52) m^{*3/2} 译注
fix_all("m^{*\\frac{3}{2}}",
        "m^{*\\frac{3}{2}}%\n（译注：按式 (7.39) 应为 $m^{*-1/2}$，原书疑误。）")
# P2：Fermi/费米 统一为中文（与术语表及全书一致）
fix_all("Fermi–Dirac", "费米–狄拉克")
fix_all("Fermi 面", "费米面")
fix_all("Fermi 能级", "费米能级")
fix_all("Fermi 分布", "费米分布")
fix_all("Fermi 统计", "费米统计")
fix_all("Fermi 速度", "费米速度")
fix_all("Fermi 能", "费米能")
# P3
fix_all("等效薛定谔方程", "等效 Schrödinger 方程")
fix_all("薛定谔方程的波包解", "Schrödinger 方程的波包解")
fix_all("薛定谔表述", "Schrödinger 表述")
fix_all("这类类似情形下", "在这类类似的情形下")
fix_all("——事实上，是整整一条激子态的带", "——确切地说，是整整一条激子态的带")
fix_all("占居核心地位", "占据核心地位")
fix_all("在简单的N.F.E. 金属", "在简单的 N.F.E. 金属")
fix_all("要除以在 (5.16) 中定义的介电常数", "要除以在 (5.16) 中定义的介电函数")
fix_all("直到到达 $B$", "直到它到达 $B$")
fix_all("Lorenz 数", "Lorenz 比")
fix_all("动理学方法", "分子运动论方法")
fix_all("动理学公式", "分子运动论公式")
fix_all("受场 $e\\mathbf{E}$ 的作用", "受力 $e\\mathbf{E}$ 的作用")

print("TOTAL round4:", n)
