# -*- coding: utf-8 -*-
"""合并四块 full.md -> MinerU/full_merged.md，并产出：
   重排本/figures_manifest.md（图N.M->页码+图hash）、重排本/引用页码对照.txt
   页码来源：图片行=hash反查content_list(精确)；文本行=content_list文本项首行锚定；
             未锚定行沿承上一已知页。
   全书597页按章界分4块；块内局部页号+偏移 0/178/306/409 = 全书PDF物理页-1。"""
import os, re, json, glob

REPO = r"E:\AI整理书籍\李正中"
MIN = os.path.join(REPO, "MinerU")
chunks = sorted(glob.glob(os.path.join(MIN, "0*_*", "full.md")))
assert len(chunks) == 4, chunks
OFFSET = {0: 0, 1: 178, 2: 306, 3: 409}

merged, page_of_line = [], []
hash2page = {}
for ci, path in enumerate(chunks):
    if os.path.getsize(path) == 0:
        continue
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
IMG_RE = re.compile(r"images/([0-9a-f]+\.jpg)")
for i, ln in enumerate(merged):
    m = re.match(r"^图\s*(\d+)\.(\d+)", ln.strip())
    if not m:
        continue
    key = (int(m.group(1)), int(m.group(2)))
    if key in figs:
        continue
    hit = None
    for rng in (range(i - 1, max(-1, i - 15), -1), range(i + 1, min(len(merged), i + 7))):
        for j in rng:
            im = IMG_RE.search(merged[j])
            if im:
                hit = (j, im.group(1))
                break
        if hit:
            break
    if hit:
        j, h = hit
        p = hash2page.get(h, -1)
        figs.setdefault(key, (f"p{p+1:03d}" if p >= 0 else pg(i), h))
    else:
        figs.setdefault(key, ("?" + pg(i), "NO-IMAGE"))

rep = ["# 《固体理论》（李正中，第2版）插图清单（图N.M → 原书页码 → MinerU裁剪图）", "",
       "- 原书页码=PDF物理页(原书转换/pages/p-NNN.png)。裁剪图在 MinerU/<块>/images/<hash>.jpg。",
       "- 重绘目标：重排本/figures/figN-M.pdf。多面板合一文件。",
       "- 页码以图片hash反查为准（精确）；图注行在OCR里偶有错位，以页面PNG实况为准。", ""]
for n in sorted(figs):
    p, h = figs[n]
    rep.append(f"- 图{n[0]}.{n[1]} → {p} {h[:12]}")
rep.append("")
open(os.path.join(REPO, "重排本", "figures_manifest.md"), "w", encoding="utf-8").write("\n".join(rep))

# 文中上标引用 [N]（章末参考文献），转录时对照页码
out = []
for i, ln in enumerate(merged):
    if re.search(r"\[\d{1,2}(?:[,，]\s*\d{1,2})*\]", ln) and not ln.strip().startswith(("#", "-", "|")):
        ctx = ln.strip()
        if len(ctx) > 70:
            k = re.search(r"\[\d{1,2}", ctx)
            k = k.start() if k else 0
            ctx = ctx[max(0, k - 45):k + 25]
        out.append(f"行{i+1:>6}  {pg(i)}  …{ctx}…")
open(os.path.join(REPO, "重排本", "引用页码对照.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")

known = sum(1 for p in page_of_line if p is not None and p >= 0)
print("merged lines:", len(merged), " lines with page:", known)
print("figures:", len(figs))
for n in sorted(figs):
    print(f"图{n[0]}.{n[1]}: {figs[n][0]} {figs[n][1][:10]}")
print("citation lines:", len(out))
