# -*- coding: utf-8 -*-
import json, io, glob, sys, os
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\MinerU"
DIRS = ["01_p001-160", "02_p161-320", "03_p321-460"]
OFFSET = [0, 160, 320]
snips = sys.argv[1:]
lo, hi = 240, 262
for di, d in enumerate(DIRS):
    c = glob.glob(os.path.join(BASE, d, "*_content_list_v2.json"))[0]
    data = json.load(io.open(c, encoding="utf-8"))
    for pi, page in enumerate(data):
        pg = OFFSET[di] + pi + 1
        if not (lo <= pg <= hi):
            continue
        for block in page:
            t = block.get("type")
            txt = ""
            if t == "paragraph":
                txt = "".join(s.get("content", "") for s in block.get("content", {}).get("paragraph_content", []) if isinstance(s, dict))
            elif t == "page_footnote":
                txt = "[FN] " + "".join(s.get("content", "") for s in block.get("content", {}).get("page_footnote_content", []) if isinstance(s, dict))
            for sn in snips:
                if sn in txt:
                    print(pg, t, "||", txt[:100].replace("\n", " "))
