# -*- coding: utf-8 -*-
"""按 figures_manifest.md 生成占位图 figures/figN-M.pdf（灰底+图号），
   缺哪张补哪张，已存在的（重绘成品）不覆盖。"""
import io, os, re

BASE = r"E:\AI整理书籍\李正中\重排本"
man = io.open(os.path.join(BASE, "figures_manifest.md"), encoding="utf-8").read()
figs = re.findall(r"^\- 图(\d+)\.(\d+)\s+→", man, re.M)
os.makedirs(os.path.join(BASE, "figures"), exist_ok=True)

# 用 matplotlib 生成占位（与重绘脚本同栈）；中文字体用系统雅黑
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

made = 0
for ch, n in figs:
    name = f"fig{ch}-{n}.pdf"
    path = os.path.join(BASE, "figures", name)
    if os.path.exists(path):
        continue
    fig = plt.figure(figsize=(4, 2.6))
    fig.text(0.5, 0.55, f"图 {ch}.{n}", ha="center", va="center", fontsize=14)
    fig.text(0.5, 0.3, "占位图（待重绘）", ha="center", va="center", fontsize=8, color="0.45")
    fig.savefig(path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    made += 1
print("manifest figures:", len(figs), "placeholders made:", made)
