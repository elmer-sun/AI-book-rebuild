# -*- coding: utf-8 -*-
"""从三段 MinerU content_list(v1) 提取真图块（带英文原图注+页码），
生成全书插图任务表 文小刚/重排本/figures_manifest.md 与 figures_manifest.json。
全局页 = 段内页 + 偏移(0/200/400)；书页 = 全局页 - 15（即 pNNN = 全局页号）。"""
import glob
import io
import json
import os
import re

BOOK = r"E:\AI整理书籍\文小刚"
OUT_MD = os.path.join(BOOK, "重排本", "figures_manifest.md")
OUT_JS = os.path.join(BOOK, "重排本", "figures_manifest.json")

PARTS = [("*24be44ee", 0), ("*595510ad", 200), ("*b5f26360", 400)]
cap_pat = re.compile(r"FIG\.\s*(\d+\.\d+)")


def main():
    rows = []
    for pat, off in PARTS:
        p = glob.glob(os.path.join(BOOK, pat, "*_content_list.json"))[0]
        data = json.load(open(p, encoding="utf-8"))
        for b in data:
            if not (isinstance(b, dict) and b.get("type") == "image"):
                continue
            g = off + b.get("page_idx", -1) + 1  # 1-based 全局 PDF 页
            caps = b.get("image_caption") or []
            cap = " ".join(caps).strip()
            m = cap_pat.search(cap)
            key = m.group(1) if m else None
            rows.append({"key": key, "global_page": g, "shuye": g - 15,
                         "caption_en": cap, "img": b.get("img_path", ""),
                         "part": pat.strip("*")})
    # key 去重（跨段重叠处保留先出现的）
    seen, out = set(), []
    for r in rows:
        if r["key"]:
            if r["key"] in seen:
                continue
            seen.add(r["key"])
        out.append(r)
    keys = [r["key"] for r in out if r["key"]]
    print(f"图块总数 {len(out)}，有编号 {len(keys)}，唯一 key {len(set(keys))}")
    nums = sorted(set(keys), key=lambda x: float(x))
    print("编号范围:", nums[0], "→", nums[-1])

    json.dump(out, io.open(OUT_JS, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    with io.open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# 全书插图任务表（MinerU 自动提取，供插图代理使用）\n\n")
        f.write("key=原书图号；pNNN=原书转换/pages/ 的全局页（=书页+15）；\n")
        f.write("caption_en=原书英文图注（中文图注已在章节 %FIG 标记里）。\n\n")
        f.write("| key | pNNN(书页) | 英文图注（截断） |\n|---|---|---|\n")
        for r in out:
            k = r["key"] or "?"
            c = r["caption_en"][:60].replace("|", "/")
            f.write(f"| {k} | p{r['global_page']:03d} ({r['shuye']}) | {c} |\n")
    print("written:", OUT_MD)
    # 缺号检查
    per_ch = {}
    for k in set(keys):
        ch = k.split(".")[0]
        per_ch.setdefault(ch, []).append(k)
    for ch in sorted(per_ch, key=int):
        ks = sorted(per_ch[ch], key=lambda x: float(x))
        fns = [int(k.split(".")[1]) for k in ks]
        gaps = [n for n in range(min(fns), max(fns) + 1) if n not in fns]
        print(f"ch{ch}: {len(ks)} 幅 ({ks[0]}..{ks[-1]})，缺号: {gaps or '无'}")


if __name__ == "__main__":
    main()
