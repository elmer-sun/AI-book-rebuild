# -*- coding: utf-8 -*-
"""合并三块 full.md -> MinerU/full_merged.md，并产出：
   figures_manifest.md（图N->页码+图hash）、脚注页码对照.txt（圈码->页码）
   页码来源：图片行=hash反查content_list(精确)；文本行=content_list文本项首行锚定；
             未锚定行沿承上一已知页。"""
import os, re, json, glob

REPO = r"E:\AI整理书籍\朗道理论物理教程\卷2场论"
MIN = os.path.join(REPO, "MinerU")
chunks = sorted(glob.glob(os.path.join(MIN, "0*_*", "full.md")))
assert len(chunks) == 3, chunks

merged, page_of_line = [], []
hash2page = {}
OFFSET = {0: 0, 1: 160, 2: 320}   # 块内局部页号 -> 全书PDF物理页-1
for ci, path in enumerate(chunks):
    cdir = os.path.dirname(path)
    cl = glob.glob(os.path.join(cdir, "*_content_list.json"))[0]
    items = json.load(open(cl, encoding="utf-8"))
    for it in items:
        if it.get("type") == "image":
            h = os.path.basename(it["img_path"].replace("\\", "/"))
            hash2page[h] = it.get("page_idx", -1) + OFFSET[ci]
    lines = open(path, encoding="utf-8").read().split("\n")
    text_items = [it for it in items if it.get("type") == "text"]
    ti, line_pages = 0, [None] * len(lines)
    last = -1
    for i, ln in enumerate(lines):
        s = ln.strip()
        p = None
        im = re.search(r"images/([0-9a-f]+\.jpg)", ln)
        if im:
            q = hash2page.get(im.group(1), None)
            p = q
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

open(os.path.join(MIN, "full_merged.md"), "w", encoding="utf-8").write("\n".join(merged))

def pg(i):
    p = page_of_line[i]
    return "?" if p is None or p < 0 else f"p{p+1:03d}"

figs = {}
for i, ln in enumerate(merged):
    m = re.match(r"^图\s*(\d+)\s*$", ln.strip())
    if m:
        n = int(m.group(1))
        for j in range(i - 1, max(-1, i - 15), -1):
            im = re.search(r"images/([0-9a-f]+\.jpg)", merged[j])
            if im:
                p = hash2page.get(im.group(1), -1)
                figs.setdefault(n, (f"p{p+1:03d}" if p >= 0 else pg(i), im.group(1)))
                break

rep = ["# 《场论》插图清单（图N → 原书页码 → MinerU裁剪图）", "",
       "- 原书页码=PDF物理页(原书转换/pages/p-NNN.png)。裁剪图在 MinerU/<块>/images/<hash>.jpg。",
       "- 重绘目标：重排本/figures/figN.pdf。多面板合一文件。",
       "- 页码以图片hash反查为准（精确）；图注行在OCR里偶有错位，以页面PNG实况为准。", ""]
for n in sorted(figs):
    p, h = figs[n]
    rep.append(f"- 图{n:>2} → {p} {h[:12]}")
rep.append("")
open(os.path.join(REPO, "重排本", "figures_manifest.md"), "w", encoding="utf-8").write("\n".join(rep))

out = []
for i, ln in enumerate(merged):
    marks = "".join(ch for ch in ln if ch in "①②③④⑤⑥⑦⑧⑨⑩")
    if not marks or ln.strip().startswith("%"):
        continue
    ctx = ln.strip()
    k = min((ln.find(c) for c in marks), default=0)
    if len(ctx) > 70:
        ctx = ln[max(0, k - 45):k + 25]
    out.append(f"行{i+1:>6}  {pg(i)}  标记[{marks}]  …{ctx}…")
open(os.path.join(REPO, "重排本", "脚注页码对照.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
known = sum(1 for p in page_of_line if p is not None and p >= 0)
print("merged lines:", len(merged), " lines with page:", known)
print("figures:", len(figs))
for n in sorted(figs):
    print(f"图{n}: {figs[n][0]} {figs[n][1][:10]}")
print("footnote lines:", len(out), " with page:", sum(1 for l in out if '? ' not in l.split('标记')[0]))
