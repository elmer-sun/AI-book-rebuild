# -*- coding: utf-8 -*-
# 装配脚本（齐曼项目）：从 chapters/parts/ 重建 chapters/chNN.tex（幂等）。
# 约定与安德森项目一致：
#   - parts 文件首行 % 注释会被剥掉；
#   - 文件顶部 %--XX-TAIL-- 标记行之后、第一个 \section/\subsection 之前的
#     内容属于上一文件的收尾，装配时移到上一块之后；
#   - 块开头 %JOIN% 表示与上一块末段直接缝合（不加空行/不分段）。
import io
import os
import re

PARTS = r"E:\AI整理书籍\齐曼\重排本\chapters\parts"
OUT = r"E:\AI整理书籍\齐曼\重排本\chapters"

CHAPTERS = [
    ("ch1_a.tex", None, None, None),
    ("ch1_b.tex", "%--A-TAIL--", None, None),
    ("ch1_c.tex", "%--B-TAIL--", None, None),
    ("ch1_d.tex", "%--C-TAIL--", "ch01.tex", "第1章 周期结构"),
    ("ch2_a.tex", None, None, None),
    ("ch2_b.tex", "%--A-TAIL--", None, None),
    ("ch2_c.tex", "%--B-TAIL--", None, None),
    ("ch2_d.tex", "%--C-TAIL--", None, None),
    ("ch2_e.tex", "%--D-TAIL--", "ch02.tex", "第2章 格波"),
    ("ch3_a.tex", None, None, None),
    ("ch3_b.tex", "%--A-TAIL--", None, None),
    ("ch3_c.tex", "%--B-TAIL--", None, None),
    ("ch3_d.tex", "%--C-TAIL--", None, None),
    ("ch3_e.tex", "%--D-TAIL--", "ch03.tex", "第3章 电子态"),
    ("ch4_a.tex", None, None, None),
    ("ch4_b.tex", "%--A-TAIL--", None, None),
    ("ch4_c.tex", "%--B-TAIL--", "ch04.tex", "第4章 固体的静态性质"),
    ("ch5_a.tex", None, None, None),
    ("ch5_b.tex", "%--A-TAIL--", None, None),
    ("ch5_c.tex", "%--B-TAIL--", "ch05.tex", "第5章 电子间相互作用"),
    ("ch6_a.tex", None, None, None),
    ("ch6_b.tex", "%--A-TAIL--", None, None),
    ("ch6_c.tex", "%--B-TAIL--", None, None),
    ("ch6_d.tex", "%--C-TAIL--", "ch06.tex", "第6章 电子动力学"),
    ("ch7_a.tex", None, None, None),
    ("ch7_b.tex", "%--A-TAIL--", None, None),
    ("ch7_c.tex", "%--B-TAIL--", None, None),
    ("ch7_d.tex", "%--C-TAIL--", None, None),
    ("ch7_e.tex", "%--D-TAIL--", "ch07.tex", "第7章 输运性质"),
    ("ch8_a.tex", None, None, None),
    ("ch8_b.tex", "%--A-TAIL--", None, None),
    ("ch8_c.tex", "%--B-TAIL--", None, None),
    ("ch8_d.tex", "%--C-TAIL--", "ch08.tex", "第8章 光学性质"),
    ("ch9_a.tex", None, None, None),
    ("ch9_b.tex", "%--A-TAIL--", None, None),
    ("ch9_c.tex", "%--B-TAIL--", None, None),
    ("ch9_d.tex", "%--C-TAIL--", "ch09.tex", "第9章 费米面"),
    ("ch10_a.tex", None, None, None),
    ("ch10_b.tex", "%--A-TAIL--", None, None),
    ("ch10_c.tex", "%--B-TAIL--", None, None),
    ("ch10_d.tex", "%--C-TAIL--", None, None),
    ("ch10_e.tex", "%--D-TAIL--", None, None),
    ("ch10_f.tex", "%--E-TAIL--", None, None),
    ("ch10_g.tex", "%--F-TAIL--", "ch10.tex", "第10章 磁性"),
    ("ch11_a.tex", None, None, None),
    ("ch11_b.tex", "%--A-TAIL--", None, None),
    ("ch11_c.tex", "%--B-TAIL--", None, None),
    ("ch11_d.tex", "%--C-TAIL--", "ch11.tex", "第11章 超导电性"),
]


def read(fn):
    return io.open(os.path.join(PARTS, fn), encoding="utf-8").read()


def split_tail(text, marker):
    m = re.search(re.escape(marker) + r"\s*\n", text)
    if not m:
        # 上游代理判定"无收尾内容"而未写标记：整文件当作 main，不视为错误
        print(f"  note: marker {marker} absent (no tail) - ok")
        return "", text
    after = text[m.end():]
    lines = after.split("\n")
    tail, rest, started = [], [], False
    for ln in lines:
        s = ln.strip()
        if not started:
            if s.startswith("\\section") or s.startswith("\\subsection"):
                started = True
                rest.append(ln)
            else:
                tail.append(ln)
        else:
            rest.append(ln)
    return "\n".join(tail).strip("\n"), "\n".join(rest).strip("\n")


def assemble(order, outfile, chapter_title):
    blocks = []
    missing = [f for f, m, _, _ in order
               if not os.path.exists(os.path.join(PARTS, f))]
    if missing:
        return missing
    for fn, marker, _, _ in order:
        t = read(fn)
        lines = t.split("\n")
        if lines and lines[0].startswith("%"):
            lines = lines[1:]
        t = "\n".join(lines).strip("\n")
        if marker:
            tail, main = split_tail(t, marker)
            pieces = [("tail", tail), ("main", main)]
        else:
            pieces = [("main", t)]
        for kind, txt in pieces:
            join = False
            if txt.startswith("%JOIN%"):
                join = True
                txt = txt[len("%JOIN%"):].lstrip("\n")
            if txt.strip():
                blocks.append((txt.strip("\n"), join))
    out = []
    for txt, join in blocks:
        if join and out:
            out[-1] = out[-1].rstrip("\n") + "\n" + txt
        else:
            out.append(txt)
    body = "\n\n".join(out)
    header = (" % 本文件由 scripts/assemble.py 自动装配，勿手改（改 parts/ 后重跑）\n"
              f"% {chapter_title}\n")
    io.open(os.path.join(OUT, outfile), "w", encoding="utf-8").write(
        header + "\n" + body + "\n")
    njoin = sum(1 for _, j in blocks if j)
    print(f"wrote {outfile}: {len(blocks)} blocks ({njoin} joined)")
    return None


def main():
    groups = {}
    order = []
    cur = []
    for f, m, out, title in CHAPTERS:
        cur.append((f, m, out, title))
        if out:
            order.append((cur, out, title))
            cur = []
    if cur:
        order.append((cur, None, None))
    for grp, out, title in order:
        miss = assemble(grp, out, title) if out else None
        if out:
            print(f"{out}: {'MISSING ' + str(miss) if miss else 'ok'}")


if __name__ == "__main__":
    main()
