# -*- coding: utf-8 -*-
"""全书校对修复批：P1 全部 + 采纳的 P2/P3（源文件=parts，改后需重装配）"""
import io
import os

ROOT = r"E:\AI整理书籍\齐曼\重排本\chapters\parts"
n = 0


def fix(fn, old, new, must=True):
    global n
    p = os.path.join(ROOT, fn)
    s = io.open(p, encoding="utf-8").read()
    if old not in s:
        print("MISS [%s]: %s..." % (fn, old[:40]))
        return
    s = s.replace(old, new, 1)
    io.open(p, "w", encoding="utf-8").write(s)
    n += 1
    print("ok [%s]: %s..." % (fn, old[:30]))


# ---------- P1 ----------
fix("ch1_a.tex", "$N^{1/3}$ 个原子", "$N^{2/3}$ 个原子")
fix("ch1_b.tex", "$(1\\bar{1}1)$ 代表 $(1,-1,-1)$",
    "$(1\\bar{1}\\bar{1})$ 代表 $(1,-1,-1)$")
fix("ch3_e.tex", "$A_{m;l'm'}$", "$A_{lm;l'm'}$")
fix("ch4_b.tex", "$\\mathcal{N}(\\mathcal{E})\\propto\\mathcal{E}^{3/2}$",
    "$\\mathcal{N}(\\mathcal{E})\\propto\\mathcal{E}^{1/2}$")
fix("ch5_b.tex", "如同用高频电对于长波长的场",
    "正如用长波长的高频电场所测得的那样")
# (11.22) 漏除号
fix("ch11_b.tex", "\\exp\\{-2\\mathcal{N}(\\mathcal{E}_{F})\\,|V|\\}",
    "\\exp\\{-2/\\mathcal{N}(\\mathcal{E}_{F})\\,|V|\\}")
# 温度度（JOIN 缝合衍字）
fix("ch11_c.tex", "其中计及能隙随温度\n", "其中计及能隙随温\n")
# \AA 残留
fix("ch11_c.tex", "（5000 \\AA）", "（5000 Å）")

# ---------- P2 ----------
fix("ch1_a.tex", "倒易三矢组（reciprocal triad）", "倒格子三矢组（reciprocal triad）")
fix("ch1_a.tex", "倒三基矢（reciprocal triad）", "倒格子三矢组（reciprocal triad）")
fix("ch1_a.tex", "Wigner–Seitz 胞（Wigner–Seitz cell）",
    "Wigner–Seitz 原胞（Wigner–Seitz cell）")
fix("ch10_f.tex", "%JOIN%果：Heisenberg", "%JOIN%其必然后果：Heisenberg")
fix("ch10_e.tex", "根据关于破缺对称效应的 \\emph{Goldstone 定理}，这是",
    "根据关于破缺对称效应的 \\emph{Goldstone 定理}，这是其")
# (10.85) 疑漏负号译注
fix("ch10_d.tex", " \\tag{10.85}",
    " \\tag{10.85}%\n（译注：按准化学近似的标准结果，右端应为 $-2/p\\;\\big/\\;\\ln\\frac{p}{p-2}$，"
    "原书疑漏负号。）", must=False)
# Ginsburg → Ginzburg（统一）
fix("ch11_d.tex", "Ginsburg–Landau", "Ginzburg–Landau")
# 第5章病句与译注
fix("ch5_b.tex", "用作传导电子被晶序偏离处净散射的矩阵元的估计",
    "用作估计传导电子被对晶体序的偏离所散射的净矩阵元")
fix("ch5_b.tex", "就好像我们拥有一罐极低温度下的", "就好像我们拥有一团极低温度下的")
fix("ch5_c.tex", "（如 §5.5 中那样）", "（如 §5.6 中那样；原书误印作 §5.5）")
fix("ch5_a.tex", "能带结构计算 (§5.3)", "能带结构计算 (§5.3；译注：疑为 §3.3 之误印)")
# jellium 统一
fix("ch5_c.tex", "正 jellium", "正凝胶")
fix("ch5_c.tex", "背景 jellium 球", "背景凝胶球")
# Hamilton 量 → 哈密顿量
fix("ch5_b.tex", "Hamilton 量", "哈密顿量", must=False)
fix("ch5_b.tex", "Hamilton 量", "哈密顿量", must=False)

# ---------- P3（采纳项） ----------
fix("ch1_c.tex", "烦冗的数学", "繁冗的数学")
fix("ch2_a.tex", "分别计账的", "分别计算的")
fix("ch2_a.tex", "中心对偶力", "中心成对力")
fix("ch4_b.tex", "每颗电子的自由能", "每个电子的自由能")
fix("ch9_c.tex", "这个公式正确地积分回归到", "这个公式积分后正确地回到")
fix("ch9_a.tex", "测量一块非常纯的金属薄片、且磁场平行于其表面时",
    "测量一块非常纯的金属薄片，且磁场平行于其表面时")
fix("ch9_a.tex", "沿一条闭合轨迹其直径随", "沿一条闭合轨迹，其直径随")
fix("ch10_a.tex", "是波函数在核处的幅度", "是波函数在核处的模方")
fix("ch11_c.tex", "\\mathbf{A}(\\mathbf{r}):$", "\\mathbf{A}(\\mathbf{r})$")
fix("ch11_b.tex", "Bardeen、Cooper 和Schrieffer", "Bardeen、Cooper 和 Schrieffer")
# (10.116) 疑指 (10.106) 译注
fix("ch10_e.tex", "第一项就是基态 (10.116) 的能量",
    "第一项就是基态（式 (10.116)；译注：疑为 (10.106) 之误印）的能量")
# 第2章“第 34 页”原书页码译注
fix("ch2_c.tex", "正如图 19(c)（第 34 页）中那样",
    "正如 §2.2 中图 19(c)（原书第 34 页）中那样")

print("TOTAL applied:", n)
