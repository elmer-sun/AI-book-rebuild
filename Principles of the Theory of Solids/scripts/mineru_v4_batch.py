#!/usr/bin/env python3
"""MinerU v4 正式 API（token 版）批量提取：一次提交 13 个分章 PDF，
轮询后把每章的结果 zip 解包到 MinerU/v4/chNN/（含 full.md + images/ +
content_list.json + layout.json）。

用法：
  python mineru_v4_batch.py <TOKEN>            # 提交全部（跳过已解包的章）
  python mineru_v4_batch.py <TOKEN> ch02 ch05  # 只处理指定章

接口：
  POST https://mineru.net/api/v4/file-urls/batch   申请预签名上传 URL
  PUT  <file_url>                                  上传 PDF（无需鉴权头）
  GET  https://mineru.net/api/v4/extract-results/batch/<batch_id>  轮询
  下载 full_zip_url → 解包
"""

import argparse
import io
import json
import os
import sys
import time
import zipfile

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE = "https://mineru.net/api/v4"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPLIT = os.path.join(ROOT, "章节拆分")
OUTDIR = os.path.join(ROOT, "MinerU", "v4")

CHAPTERS = {
    "ch01": "01_周期结构_p015-040.pdf",
    "ch02": "02_格波_p041-090.pdf",
    "ch03": "03_电子态_p091-132.pdf",
    "ch04": "04_固体的静态性质_p133-159.pdf",
    "ch05": "05_电子间相互作用_p160-184.pdf",
    "ch06": "06_电子动力学_p185-224.pdf",
    "ch07": "07_输运性质_p225-268.pdf",
    "ch08": "08_光学性质_p269-305.pdf",
    "ch09": "09_费米面_p306-342.pdf",
    "ch10": "10_磁性_p343-388.pdf",
    "ch11": "11_超导电性_p389-428.pdf",
    "ch12": "12_文献目录_p429-438.pdf",
    "ch13": "13_索引_p439-451.pdf",
}


def req(method, url, token=None, **kw):
    headers = kw.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.request(method, url, headers=headers, timeout=60,
                         verify=False, **kw)
    if r.status_code >= 300:
        raise RuntimeError(f"{method} {url} -> HTTP {r.status_code}: {r.text[:300]}")
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("token", nargs="?", default=None,
                    help="API token（缺省读环境变量 MINERU_TOKEN）")
    ap.add_argument("keys", nargs="*", help="章键（默认全部未完成的）")
    args = ap.parse_args()
    token = (args.token or os.environ.get("MINERU_TOKEN") or "").strip()
    if not token:
        raise SystemExit("no token: pass argv[1] or set MINERU_TOKEN")

    keys = args.keys or list(CHAPTERS)
    todo = []
    for k in keys:
        out = os.path.join(OUTDIR, k)
        if os.path.exists(os.path.join(out, "full.md")):
            print(f"[skip] {k} already extracted")
            continue
        todo.append(k)
    if not todo:
        print("nothing to do")
        return

    os.makedirs(OUTDIR, exist_ok=True)
    files = [{"name": CHAPTERS[k], "is_ocr": True, "data_id": k} for k in todo]
    body = {"enable_formula": True, "enable_table": True,
            "language": "en", "files": files}

    r = req("POST", f"{BASE}/file-urls/batch", token, json=body)
    d = r.json()
    if d.get("code") != 0:
        raise RuntimeError(f"batch apply failed: {d}")
    batch_id = d["data"]["batch_id"]
    urls = d["data"]["file_urls"]
    print(f"batch_id={batch_id}")

    for k, u in zip(todo, urls):
        pdf = os.path.join(SPLIT, CHAPTERS[k])
        with open(pdf, "rb") as f:
            rr = requests.put(u, data=f, timeout=600, verify=False)
        print(f"[put ] {k}: HTTP {rr.status_code}")

    print("polling...")
    done = {}
    t0 = time.time()
    while len(done) < len(todo) and time.time() - t0 < 3600:
        time.sleep(10)
        r = req("GET", f"{BASE}/extract-results/batch/{batch_id}", token)
        d = r.json()
        if d.get("code") != 0:
            raise RuntimeError(f"poll failed: {d}")
        for ent in d["data"]["extract_result"]:
            k = ent.get("data_id")
            st = ent.get("state")
            if k in done:
                continue
            if st == "done":
                done[k] = ent["full_zip_url"]
                print(f"[done] {k}  ({int(time.time()-t0)}s)")
            elif st == "failed":
                done[k] = None
                print(f"[FAIL] {k}: {ent.get('err_msg')}")
        sys.stdout.flush()

    for k, zurl in done.items():
        out = os.path.join(OUTDIR, k)
        os.makedirs(out, exist_ok=True)
        if not zurl:
            continue
        zr = requests.get(zurl, timeout=300, verify=False)
        zf = zipfile.ZipFile(io.BytesIO(zr.content))
        zf.extractall(out)
        n_img = len([x for x in zf.namelist() if "/images/" in x or x.startswith("images/")])
        print(f"[save] {k}: {len(zf.namelist())} files (images≈{n_img}) -> {out}")
    fails = [k for k, v in done.items() if v is None]
    print(f"ALL DONE ok={len(done)-len(fails)} failed={fails}")


if __name__ == "__main__":
    main()
