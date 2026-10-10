# -*- coding: utf-8 -*-
"""从 batch 接口抓取已完成文件的 zip 并解包到 MinerU/<name>/（幂等）"""
import os, sys, io, zipfile, requests, urllib3
urllib3.disable_warnings()
BASE = "https://mineru.net/api/v4"
REPO = r"E:\AI整理书籍"
batch = sys.argv[1]
token = open(os.path.join(REPO, "工具", "mineru.token"), encoding="utf-8").read().strip()
outdir = os.path.join(REPO, "朗道理论物理教程", "卷2场论", "MinerU")

d = requests.get(f"{BASE}/extract-results/batch/{batch}",
                 headers={"Authorization": "Bearer " + token}, verify=False, timeout=60).json()
for e in d["data"]["extract_result"]:
    name, st = e["data_id"], e["state"]
    dest = os.path.join(outdir, name)
    if st != "done":
        print(name, "->", st); continue
    if os.path.exists(os.path.join(dest, "full.md")):
        print(name, "-> exists, skip"); continue
    os.makedirs(dest, exist_ok=True)
    url = e["full_zip_url"]
    print(name, "-> downloading", url[:60])
    z = requests.get(url, verify=False, timeout=600)
    zf = zipfile.ZipFile(io.BytesIO(z.content))
    zf.extractall(dest)
    print(name, "-> unpacked", len(zf.namelist()), "files")
