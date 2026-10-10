# -*- coding: utf-8 -*-
"""Dump all page_footnote blocks with pages for ch07-ch09 range."""
import json, io, glob, sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\MinerU"
DIRS = ["01_p001-160", "02_p161-320", "03_p321-460"]
OFFSET = [0, 160, 320]

lo, hi = int(sys.argv[1]), int(sys.argv[2])
for di, d in enumerate(DIRS):
    c = glob.glob(BASE + "\\" + d + "\\*_content_list_v2.json")[0]
    data = json.load(io.open(c, encoding="utf-8"))
    for pi, page in enumerate(data):
        pg = OFFSET[di] + pi + 1
        if not (lo <= pg <= hi):
            continue
        for block in page:
            if block.get("type") == "page_footnote":
                pc = block.get("content", {}).get("page_footnote_content", [])
                if not pc:
                    pc = block.get("content", {}).get("paragraph_content", [])
                txt = "".join(seg.get("content", "") for seg in pc if isinstance(seg, dict))
                print("### p-%03d ###" % pg)
                print(txt)
                print()
