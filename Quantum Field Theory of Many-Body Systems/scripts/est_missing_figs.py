# -*- coding: utf-8 -*-
"""对 MinerU 漏抓图注的 9 幅图，用装配章节中相邻 %FIG 的页码推算所在页，
把估算写进 figures_manifest.json/md 的备注字段。"""
import io
import json
import os
import re

BASE = r"E:\AI整理书籍\文小刚\重排本"
CH = os.path.join(BASE, "chapters")
JS = os.path.join(BASE, "figures_manifest.json")

MISSING = ["3.9", "3.10", "3.13", "4.17", "5.13", "7.6", "7.17", "9.15", "10.4"]
figdef = re.compile(r"%FIG\{(\d+\.\d+)\}")


def main():
    man = json.load(io.open(JS, encoding="utf-8"))
    pagemap = {r["key"]: r["global_page"] for r in man if r["key"]}

    est = {}
    parts_dir = os.path.join(BASE, "chapters", "parts")
    for fn in sorted(os.listdir(parts_dir)):
        if not re.match(r"ch\d+_[a-z]\.tex$", fn):
            continue
        s = io.open(os.path.join(parts_dir, fn), encoding="utf-8").read()
        keys = figdef.findall(s)
        for i, k in enumerate(keys):
            if k not in MISSING:
                continue
            prev_k = next((x for x in reversed(keys[:i]) if x in pagemap), None)
            next_k = next((x for x in keys[i + 1:] if x in pagemap), None)
            pg = [pagemap[x] for x in (prev_k, next_k) if x]
            lo = max(pg) if pg else 0
            hi = min(pg) + 2 if len(pg) == 2 else (pg[0] + 3 if pg else 0)
            est[k] = (prev_k, next_k, f"p{lo:03d}-p{hi:03d} 之间（全页读图定位）")
            print(k, "->", est[k])

    for r in man:
        if r["key"] in est:
            r["page_est"] = est[r["key"]][2]
    json.dump(man, io.open(JS, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    with io.open(os.path.join(BASE, "MISSING_FIGS.md"), "w",
                 encoding="utf-8") as f:
        f.write("# MinerU 漏抓图注的 9 幅图（页码估算）\n\n")
        f.write("| key | 前邻图 | 后邻图 | 页码估算 |\n|---|---|---|---|\n")
        for k in MISSING:
            pk, nk, pg = est.get(k, ("?", "?", "?"))
            f.write(f"| {k} | {pk} | {nk} | {pg} |\n")
    print("written MISSING_FIGS.md")


if __name__ == "__main__":
    main()
