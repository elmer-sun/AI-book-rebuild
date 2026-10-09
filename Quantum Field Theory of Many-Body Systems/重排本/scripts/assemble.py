# -*- coding: utf-8 -*-
# 装配脚本（文小刚项目）：从 chapters/parts/ 重建 chapters/chNN.tex（幂等）。
# 约定与齐曼/卡罗尔项目一致：
#   - parts 文件首行 % 注释会被剥掉；
#   - 文件顶部 %--XX-TAIL-- 标记行之后、第一个 \section/\subsection 之前的
#     内容属于上一文件的收尾，装配时移到上一块之后；
#   - 块开头 %JOIN% 表示与上一块末段直接缝合（不加空行/不分段）。
import io
import os
import re

PARTS = r"E:\AI整理书籍\文小刚\重排本\chapters\parts"
OUT = r"E:\AI整理书籍\文小刚\重排本\chapters"

CHAPTERS = [
    ("front_a.tex", None, "ch00_front.tex", "前言"),
    ("ch1_a.tex", None, "ch01.tex", "第1章 引言"),
    ("ch2_a.tex", None, None, None),
    ("ch2_b.tex", "%--A-TAIL--", None, None),
    ("ch2_c.tex", "%--B-TAIL--", None, None),
    ("ch2_d.tex", "%--C-TAIL--", None, None),
    ("ch2_e.tex", "%--D-TAIL--", "ch02.tex", "第2章 量子力学的路径积分表述"),
    ("ch3_a.tex", None, None, None),
    ("ch3_b.tex", "%--A-TAIL--", None, None),
    ("ch3_c.tex", "%--B-TAIL--", None, None),
    ("ch3_d.tex", "%--C-TAIL--", None, None),
    ("ch3_e.tex", "%--D-TAIL--", None, None),
    ("ch3_f.tex", "%--E-TAIL--", None, None),
    ("ch3_g.tex", "%--F-TAIL--", "ch03.tex", "第3章 相互作用玻色子系统"),
    ("ch4_a.tex", None, None, None),
    ("ch4_b.tex", "%--A-TAIL--", None, None),
    ("ch4_c.tex", "%--B-TAIL--", None, None),
    ("ch4_d.tex", "%--C-TAIL--", "ch04.tex", "第4章 自由费米子系统"),
    ("ch5_a.tex", None, None, None),
    ("ch5_b.tex", "%--A-TAIL--", None, None),
    ("ch5_c.tex", "%--B-TAIL--", None, None),
    ("ch5_d.tex", "%--C-TAIL--", None, None),
    ("ch5_e.tex", "%--D-TAIL--", "ch05.tex", "第5章 相互作用费米子系统"),
    ("ch6_a.tex", None, None, None),
    ("ch6_b.tex", "%--A-TAIL--", "ch06.tex", "第6章 量子规范理论"),
    ("ch7_a.tex", None, None, None),
    ("ch7_b.tex", "%--A-TAIL--", None, None),
    ("ch7_c.tex", "%--B-TAIL--", None, None),
    ("ch7_d.tex", "%--C-TAIL--", None, None),
    ("ch7_e.tex", "%--D-TAIL--", "ch07.tex", "第7章 量子霍尔态理论"),
    ("ch8_a.tex", None, None, None),
    ("ch8_b.tex", "%--A-TAIL--", "ch08.tex", "第8章 拓扑序与量子序——超越朗道理论"),
    ("ch9_a.tex", None, None, None),
    ("ch9_b.tex", "%--A-TAIL--", None, None),
    ("ch9_c.tex", "%--B-TAIL--", None, None),
    ("ch9_d.tex", "%--C-TAIL--", None, None),
    ("ch9_e.tex", "%--D-TAIL--", None, None),
    ("ch9_f.tex", "%--E-TAIL--", None, None),
    ("ch9_g.tex", "%--F-TAIL--", "ch09.tex", "第9章 自旋液体与量子序的平均场理论"),
    ("ch10_a.tex", None, None, None),
    ("ch10_b.tex", "%--A-TAIL--", None, None),
    ("ch10_c.tex", "%--B-TAIL--", None, None),
    ("ch10_d.tex", "%--C-TAIL--", None, None),
    ("ch10_e.tex", "%--D-TAIL--", "ch10.tex", "第10章 弦凝聚——光与费米子的统一"),
    ("bib_a.tex", None, "ch11_bib.tex", "文献目录"),
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
        # 代理惯例：首行注释后可能还有若干"块边界备注"注释行，然后才是 %JOIN%。
        # 跳过普通注释行；遇到 %JOIN% 行则置 JOIN 并从其后的正文开始。
        join_head = False
        k = 0
        while k < len(lines):
            s2 = lines[k].strip()
            if s2.startswith("%JOIN%"):
                join_head = True
                k += 1
                break
            if s2.startswith("%"):
                k += 1
                continue
            break
        if join_head:
            lines = lines[k:]
        t = "\n".join(lines).strip("\n")
        if marker:
            tail, main = split_tail(t, marker)
            pieces = [("tail", tail), ("main", main)]
        else:
            pieces = [("main", t)]
        for kind, txt in pieces:
            join = join_head and kind == "main"
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
