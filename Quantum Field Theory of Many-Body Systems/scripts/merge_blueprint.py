# -*- coding: utf-8 -*-
"""把三段 MinerU 提取的 full.md 合并切成按章蓝本 blueprint/chNN.md。

段界与接缝（已人工核实）：
  段1(m1) 封面→书页185，末行=式(4.4.7)后 θ1θ2 方程，段2 首行"Comparing..."正好续接；
  段2(m2) 书页186→385，末行"...The spinon in the spin"（句中断），
          段3 首行"liquid described by..."接成同句（中间补一个空格）；
  段3(m3) 书页386→505+索引。

产物：blueprint/front.md, ch01..ch10.md, bib.md（INDEX 不收）；
附带每章 \tag 基线与 "Fig. N.M" 引用基线 -> blueprint/_baseline.json。
"""
import glob
import io
import json
import os
import re

BOOK = r"E:\AI整理书籍\文小刚"
OUT = os.path.join(BOOK, "重排本", "blueprint")


def md(seg):
    p = glob.glob(os.path.join(BOOK, seg, "full.md"))[0]
    return io.open(p, encoding="utf-8").read().split("\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    m1, m2, m3 = md("*24be44ee"), md("*595510ad"), md("*b5f26360")

    # 0-based 行界（上面 grep 的 1-based 行号 - 1）
    pieces = {
        "front.md": m1[0:168],
        "ch01.md": m1[168:312],
        "ch02.md": m1[312:2228],
        "ch03.md": m1[2228:4653],
        "ch04.md": m1[4653:] + m2[0:22],
        "ch05.md": m2[22:2065],
        "ch06.md": m2[2065:2839],
        "ch07.md": m2[2839:4629],
        "ch08.md": m2[4629:4898],
        "ch09.md": m2[4898:] + m3[0:1284],
        "ch10.md": m3[1284:2759],
        "bib.md": m3[2759:3123],
    }
    # 接缝2：ch9 跨段句中断（m2 末行 "...in the spin" + m3 首行 "liquid ..."）
    c9 = pieces["ch09.md"]
    k = len(m2[4898:])          # ch09.md 中 m2 尾段的行数；末行下标 k-1，m3 首行下标 k
    c9[k - 1] = c9[k - 1].rstrip() + " " + c9[k].lstrip()
    del c9[k]

    base = {}
    tag_pat = re.compile(r"\\tag\{(\d+\.\d+\.\d+[a-z]?)\}")
    fig_pat = re.compile(r"Fig\.\s*(\d+\.\d+)")
    for name, lines in pieces.items():
        text = "\n".join(lines)
        io.open(os.path.join(OUT, name), "w", encoding="utf-8").write(text)
        ch = name.split(".")[0]
        tags = [m.group(1) for m in tag_pat.finditer(text)]
        figs = sorted(set(m.group(1) for m in fig_pat.finditer(text)))
        base[ch] = {"tags": tags, "fig_refs": figs,
                    "n_tags": len(tags), "n_lines": len(lines)}
        print(f"{name}: {len(lines)} 行, {len(tags)} tags, "
              f"Fig引用 {len(figs)} 个: {','.join(figs[:20])}")

    json.dump(base, io.open(os.path.join(OUT, "_baseline.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=1)
    total = sum(v["n_tags"] for v in base.values())
    print(f"\n合计 {total} 个编号公式")


if __name__ == "__main__":
    main()
