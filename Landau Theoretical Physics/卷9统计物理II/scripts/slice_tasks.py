# -*- coding: utf-8 -*-
"""卷9 OCR 按排版任务分片，带页码锚点 -> 章节OCR/*.md
页码锚点：%%p NNN（PDF物理页），页变化且距上个锚点>=6行时插入。
分片边界 = 任务起始节头（## §N）行号。"""
import os, re, json, glob

REPO = r"E:\AI整理书籍\朗道理论物理教程\卷9统计物理II"
MIN = os.path.join(REPO, "MinerU")
OUT = os.path.join(REPO, "章节OCR")
os.makedirs(OUT, exist_ok=True)

chunks = sorted(glob.glob(os.path.join(MIN, "0*_*", "full.md")))
assert len(chunks) == 3, chunks
OFFSET = {0: 0, 1: 160, 2: 320}

merged, page_of_line = [], []
hash2page = {}
for ci, path in enumerate(chunks):
    cdir = os.path.dirname(path)
    cl = glob.glob(os.path.join(cdir, "*_content_list.json"))[0]
    items = json.load(open(cl, encoding="utf-8"))
    for it in items:
        if it.get("type") == "image":
            h = os.path.basename(it["img_path"].replace("\\", "/"))
            hash2page[h] = it.get("page_idx", -1) + OFFSET[ci]
    lines = open(path, encoding="utf-8").read().replace("\r\n", "\n").split("\n")
    text_items = [it for it in items if it.get("type") == "text"]
    ti, line_pages = 0, [None] * len(lines)
    last = -1
    for i, ln in enumerate(lines):
        s = ln.strip()
        p = None
        im = re.search(r"images/([0-9a-f]+\.jpg)", ln)
        if im:
            p = hash2page.get(im.group(1), None)
        if p is None and s:
            for probe in range(ti, min(ti + 40, len(text_items))):
                t = text_items[probe].get("text", "").strip()
                if t and len(s) >= 12 and (s[:18] == t[:18]):
                    p = text_items[probe].get("page_idx", None)
                    if p is not None:
                        p = p + OFFSET[ci]
                    ti = probe + 1
                    break
        line_pages[i] = p if p is not None else last
        if p is not None:
            last = p
    for i, ln in enumerate(lines):
        merged.append(ln)
        page_of_line.append(line_pages[i])
    merged.append("")
    page_of_line.append(last)

# 任务表：(输出名, 起始节号, 结束节号(含), 任务描述)
TASKS = [
    ("ch01",      1,  6,  "第一章 正常费米液体 §1–6"),
    ("ch02a",     7, 13,  "第二章(前半) §7–13"),
    ("ch02b",    14, 21,  "第二章(后半) §14–21"),
    ("ch03a",    22, 28,  "第三章(前半) §22–28"),
    ("ch03b",    29, 35,  "第三章(后半) §29–35*（含星号节35*）"),
    ("ch04",     36, 38,  "第四章 有限温度时的格林函数 §36–38"),
    ("ch05a",    39, 45,  "第五章(前半) §39–45"),
    ("ch05b",    46, 54,  "第五章(后半) §46–54"),
    ("ch06a",    55, 61,  "第六章(前半) §55–61"),
    ("ch06b",    62, 68,  "第六章(后半) §62–68"),
    ("ch07",     69, 74,  "第七章 磁性 §69–74*（含星号节74*）"),
    ("ch08a",    75, 79,  "第八章(前半) §75–79"),
    ("ch08b",    80, 85,  "第八章(后半) §80–85"),
    ("ch09",     86, 91,  "第九章 流体动力学涨落 §86–91"),
]

def sec_header_line(n):
    """返回正文节头 '## §N' 的行号（TOC 区是纯文本行，不带 ##）"""
    pat = re.compile(r"^#{1,3}\s*§\s*%d\b" % n)
    for i, ln in enumerate(merged):
        if pat.match(ln):
            return i
    return None

starts = []
for name, a, b, desc in TASKS:
    i = sec_header_line(a)
    assert i is not None, (name, a)
    starts.append((name, a, b, desc, i))

for k, (name, a, b, desc, i) in enumerate(starts):
    j = starts[k + 1][4] if k + 1 < len(starts) else len(merged)
    out, last_pg, since = [], -1, 99
    for idx in range(i, j):
        p = page_of_line[idx]
        if p is not None and p != last_pg and since >= 6:
            out.append("%%%%p %03d" % (p + 1))
            last_pg, since = p, 0
        since += 1
        out.append(merged[idx])
    path = os.path.join(OUT, name + ".md")
    open(path, "w", encoding="utf-8").write("\n".join(out))
    tags = re.findall(re.escape(chr(92)) + r"tag\{([0-9a-z.]+)\}", "\n".join(out))
    fns = sum(1 for ln in out for ch in ln if ch in "①②③④⑤⑥⑦⑧⑨⑩")
    print("%-6s 行%5d  p%03d-%03d  tag%3d  圈码行%3d  %s" %
          (name, len(out), page_of_line[i] + 1, page_of_line[j - 1] + 1,
           len(tags), fns, desc))
