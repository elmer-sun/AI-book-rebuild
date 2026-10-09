# -*- coding: utf-8 -*-
"""习题解答册 → 分章 Markdown（复用重排本的转换器）。"""
import io
import os
import sys

BASE = r"E:\AI整理书籍\文小刚"
sys.path.insert(0, os.path.join(BASE, "重排本", "scripts"))
import export_markdown as em  # noqa: E402

CHAPTERS = [
    ("ch02.tex", "第2章_量子力学的路径积分表述", "量子力学的路径积分表述"),
    ("ch03.tex", "第3章_相互作用玻色子系统", "相互作用玻色子系统"),
    ("ch04.tex", "第4章_自由费米子系统", "自由费米子系统"),
    ("ch05.tex", "第5章_相互作用费米子系统", "相互作用费米子系统"),
    ("ch06.tex", "第6章_量子规范理论", "量子规范理论"),
    ("ch07.tex", "第7章_量子霍尔态理论", "量子霍尔态理论"),
    ("ch08.tex", "第8章_拓扑序与量子序", "拓扑序与量子序——超越朗道理论"),
    ("ch09.tex", "第9章_自旋液体与量子序的平均场理论", "自旋液体与量子序的平均场理论"),
    ("ch10.tex", "第10章_弦凝聚", "弦凝聚——光与费米子的统一"),
]

OUT = os.path.join(BASE, "习题解答", "markdown")
em.OUT = OUT


def main():
    readme = ["# 《多体量子场论》习题解答 · Markdown 版", "",
              "覆盖原书第 2–10 章全部 164 道开放习题；公式为 $$…$$ LaTeX。",
              "PDF 成品见上级目录。", ""]
    total = 0
    for src, d, title in CHAPTERS:
        p = os.path.join(BASE, "习题解答", "chapters", src)
        if not os.path.exists(p):
            print("缺", src)
            continue
        outdir = os.path.join(OUT, d)
        md = em.convert_chapter(p, outdir, title)
        txt = io.open(md, encoding="utf-8").read()
        n = txt.count("## 问题 ")
        total += n
        readme.append(f"- [{title}]({d}/{os.path.basename(md)})（{n} 题）")
        print(f"{d}: {os.path.getsize(md)//1024}KB, {n} 题")
    readme.append("")
    readme.append(f"共 {total} 题。")
    io.open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write(
        "\n".join(readme) + "\n")
    print("合计", total, "题；README written")


if __name__ == "__main__":
    main()
