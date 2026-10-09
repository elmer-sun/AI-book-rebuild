# -*- coding: utf-8 -*-
# 三处接缝修复：B1a/B1b 句子缝合、p068 表3+B.2收尾、p127 B.1(Kohn/Blount)收尾
import io

P = r"E:\AI整理书籍\安德森\重排本\chapters\parts"

def rd(fn):
    return io.open(P + "\\" + fn, encoding="utf-8").read()

def wr(fn, s):
    io.open(P + "\\" + fn, "w", encoding="utf-8").write(s)

# ---- 1. B1a/B1b 缝合 ----
a = rd("ch2_B1a.tex")
old_a = "没有任何一点会被遗漏。这就是所谓的\\emph{第一}"
assert old_a in a, "B1a anchor missing"
a = a.replace(old_a, "没有任何一点会被遗漏。")
wr("ch2_B1a.tex", a)

b = rd("ch2_B1b.tex")
old_b = "布里渊区。如果愿意，"
assert old_b in b, "B1b anchor missing"
b = b.replace(old_b, "这就是所谓的\\emph{第一}布里渊区。如果愿意，", 1)
b = b.replace("% 与本文件首词 “布里渊区。” 合成完整一句（“第一布里渊区”）。",
              "% 首句已与上一文件末句缝合为“这就是所谓的第一布里渊区”。")
wr("ch2_B1b.tex", b)

# ---- 2. ch2_B2.tex 追加 p068 顶部：表 3 + B.2 收尾段 ----
c = rd("ch2_B2.tex")
assert "%--PATCH-B2-TAIL--" not in c
c += "\n% ---- B.2 收尾：表 3 与讨论段（原书 p.53 / PDF p068 顶部，协调者补译） ----\n"
c += r"""\begin{table}[H]
\centering
{\bfseries 表~3}\\[6pt]
\small
\setlength{\tabcolsep}{4.5pt}
\renewcommand{\arraystretch}{1.25}
\begin{tabular}{@{}llllllll@{}}
\toprule
元素 & $r_s$ & $-E_0$ & \shortstack{内聚边界修正\\$E_I-E_0$\ensuremath{,} ev}
 & \shortstack{动能修正\\$m/m^*$} & $E_F$\ensuremath{,} ev
 & \shortstack{未修正内聚能\\$E_I-E_0-E_F$\ensuremath{,} ev}
 & \shortstack{观测内聚能\\ev}\\
\midrule
Li & 3.21 & \shortstack[r]{0.69 ryd =\\9.4 ev} & 4.0 & 0.67 & 1.90 & 2.10 & 1.65\\
Na & 3.96 & \shortstack[r]{0.625 ryd =\\8.5 ev} & 3.15 & 1.02 & 2.0 & 1.15 & 1.20\\
Rb & 5.20 & 6.27 ev & 1.65 & 1.10 & 1.23 & 0.42 & 0.85\\
\bottomrule
\end{tabular}
\end{table}

这张表足以显示各种结果的大致面貌。正如我们所猜想的，Fermi 动能修正大致达到边界修正的二分之一到三分之二，而二者的差按数量级的程度给出金属的结合能。注意，内聚能是问题中最小的能量——它是作为大得多的数字之差被算出来的——这几乎总是如此，也正是结合能计算中困难的主要根源。把能带算准到 0.1 ryd 左右并不难，这对了解能带结构的一般面貌通常已令人满意，因为能带结构的尺度往往是 rydberg 量级，至少也是 0.4 到 0.5 ryd；但结合能却是 0.1 或更小。
"""
wr("ch2_B2.tex", c)

# ---- 3. ch3_B1.tex 追加 p127 顶部 B.1 收尾（Kohn 恒等式证明收束 + Blount） ----
d = rd("ch3_B1.tex")
assert "%--PATCH-B1-TAIL--" not in d
d += "\n% ---- B.1 收尾（原书 p.112 / PDF p127 顶部，协调者补译；承接上式 eM Σ f(Q) = eM） ----\n"
d += r"""（由性质 (c)）；于是它与半径 $R_1$ 无关，正是直接与波包自身相联系的那份电荷。正如我们的物理推理早已告诉我们的，它恰好就是 $e/\kappa$。这样，我们就得到了 Kohn 恒等式的一个物理上的——尽管显然不是严格数学意义上的——证明。实际的证明看来只能借助图微扰论（diagrammatic perturbation theory）来进行。应当认识到：整个 $N{+}1$ 体理论的这套机制确实只在微扰论的界限之内被严格证明——尽管恰恰在这个情形下，我们完全有理由相信微扰论实际上收敛，并且准确地代表了物理实在。

Blount 为此补充了一个颇有意思的结果。实质上，我们迄今为止所做的，正相当于 Bloch 电子的零阶单带理论——亦即有效哈密顿量理论
\begin{equation*}
\mathcal{H} = E(\mathbf{k}) + V(\mathbf{R})
\end{equation*}
Blount 指出，只要把 $N{+}1$ 体波函数 $\Psi_{\mathbf{k}}$ 本质上取作
\begin{equation*}
\Psi_{\mathbf{k}}(\mathbf{r}_1,\ \mathbf{r}_2,\ \ldots\,,\mathbf{r}_{N+1})\ =\ \left\{\mathrm{e}^{i\mathbf{k}\cdot\mathbf{r}_1}\ U_{\mathrm{o}}^{\mathbf{k}}\left(\mathbf{r}_1\ldots\mathbf{r}_{N+1}\right)\right\}\ \text{的反对称化}
\end{equation*}
其中 $U_{\mathrm{o}}^{\mathbf{k}}$ 是其 $N{+}1$ 个粒子变量的完全周期函数，就可以得到 $N{+}1$ 体问题的完整理论。于是 $U_{\mathrm{o}}^{\mathbf{k}}$ 的处理方式与通常波函数的 Bloch 部分十分相像，并且由它出发——利用 Kohn 与 Ambegaokar 的恒等式——例如可以导出关系式
\begin{equation*}
V(\mathbf{r}) = \frac{1}{\kappa}\,V(\mathbf{R})\ +\ \text{量级为}\ \frac{\partial V}{\partial \mathbf{R}}\cdot a\ \text{的修正项}
\end{equation*}
然而，这些修正项与真实单电子情形的修正项颇为不同——这是意料之中的，因为现在 $V$ 既能极化原子芯，也能极化所加入电子的波函数。
"""
wr("ch3_B1.tex", d)

print("3 seam patches applied")
