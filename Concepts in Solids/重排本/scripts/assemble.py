# -*- coding: utf-8 -*-
# 装配脚本：从 chapters/parts/ 重建 ch02.tex / ch03.tex（幂等）
# tail 块约定：%--XXX-TAIL-- 标记行之后的内容属于上一小节的收尾，
# 直到第一个 \section 或 \subsection 命令行为止。
import io, os

PARTS = r"E:\AI整理书籍\安德森\重排本\chapters\parts"
OUT   = r"E:\AI整理书籍\安德森\重排本\chapters"

def read(fn):
    return io.open(os.path.join(PARTS, fn), encoding="utf-8").read()

def split_tail(text, marker):
    """返回 (tail, main)。tail = 标记行（必须行首）后到第一个结构命令前；main = 其余。"""
    import re as _re
    m = _re.search(_re.escape(marker) + r"\s*\n", text)
    if not m:
        raise SystemExit(f"marker {marker} not found at line start")
    i = m.start()
    after = text[m.end():]
    lines = after.split("\n")
    tail, rest, in_tail = [], [], False
    started = False
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

CH2 = [
    ("ch2_A1.tex",  None),
    ("ch2_A2a.tex", None),
    ("ch2_A2b.tex", None),
    ("ch2_B1a.tex", "%--A2-TAIL--"),
    ("ch2_B1b.tex", None),
    ("ch2_B2.tex",  None),
    ("ch2_B3.tex",  None),
    ("ch2_B4a.tex", None),
    ("ch2_B4b.tex", None),
    ("ch2_C12.tex", "%--B4-TAIL--"),
    ("ch2_C34.tex", None),
    ("ch2_C5.tex",  None),
]

CH3 = [
    ("ch3_A.tex",  None),
    ("ch3_B1.tex", None),
    ("ch3_B2a.tex", None),
    ("ch3_B2b.tex", None),
    ("ch3_C.tex",  None),
    ("ch3_D1a.tex", "%--C-TAIL--"),
    ("ch3_D1b.tex", None),
    ("ch3_D1c.tex", None),
    ("ch3_D2.tex", "%--D1-TAIL--"),
    ("ch3_D3.tex", "%--D2-TAIL--"),
    ("ch3_D4.tex", "%--D3-TAIL--"),
]

def assemble(order, outfile, chapter_title):
    blocks = []  # (text, join_flag)
    missing = [f for f, m in order if not os.path.exists(os.path.join(PARTS, f))]
    if missing:
        return missing
    for fn, marker in order:
        t = read(fn)
        lines = t.split("\n")
        if lines and lines[0].startswith("%"):
            lines = lines[1:]
        t = "\n".join(lines).strip("\n")
        pieces = []
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
    header = (f"% 本文件由 scripts/assemble.py 自动装配，勿手改（改 parts/ 后重跑）\n"
              f"% {chapter_title}\n")
    io.open(os.path.join(OUT, outfile), "w", encoding="utf-8").write(header + "\n" + body + "\n")
    njoin = sum(1 for _, j in blocks if j)
    print(f"wrote {outfile}: {len(blocks)} blocks ({njoin} joined), {body.count(chr(10))+1} lines")
    return None

m2 = assemble(CH2, "ch02.tex", "第2章 单电子理论")
m3 = assemble(CH3, "ch03.tex", "第3章 元激发")
print("missing ch3:", m3 if m3 else "none")
