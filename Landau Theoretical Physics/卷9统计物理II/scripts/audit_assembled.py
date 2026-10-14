# -*- coding: utf-8 -*-
"""卷9 组装审计 v2：
1) .toc 节号连续性（星号节单独核对）
2) 编译期公式号捕获（eqnums.txt，由 eqhook 生成）vs OCR tag 逐节比对"""
import re, io, os, sys

BASE = r"E:\AI整理书籍\朗道理论物理教程\卷9统计物理II"
RB = os.path.join(BASE, "重排本")

def key(s):
    m = re.match(r"^(\d+)\*?\.(\d+)([a-z]?)$", s)
    if m:
        return (int(m.group(1)), int(m.group(2)), m.group(3))
    return (10 ** 6, 0, s)

# ---- 1) toc ----
toc = io.open(os.path.join(RB, "main.toc"), encoding="utf-8").read()
secs = re.findall(
    r"contentsline \{section\}\{\\numberline \{§?([^}]*)\}([^{}]*)\}\{(\d+)\}", toc)
print("== toc sections:", len(secs))
star_hits = []
main_secs = []
for num, extra, page in secs:
    if "*" in extra or "*" in num:
        star_hits.append((num, extra.strip()[:20], page))
    else:
        main_secs.append(num)
print("   starred:", star_hits)
exp = [str(i) for i in range(1, 92)]
bad = [(i, n) for i, (n, e) in enumerate(zip(main_secs, exp), 1) if n != e]
if len(main_secs) != 91:
    print("   !! main section count %d != 91" % len(main_secs))
    print("   got:", main_secs)
if bad:
    print("   MISMATCH:", bad[:10])
else:
    print("   numbering §1..§91 continuous: OK")

# ---- 2) 公式号捕获文件 vs OCR tags ----
hookf = os.path.join(RB, "eqnums.txt")
if os.path.exists(hookf):
    got = [t[1:] for t in io.open(hookf, encoding="utf-8").read().split()
           if t.startswith("E")]
    # 合并 aux 中手工 \tag 的标签值（equation*+\tag 走 aux）
    aux = io.open(os.path.join(RB, "main.aux"), encoding="utf-8").read()
    for name, num in re.findall(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}", aux):
        if re.match(r"^[0-9]+\*?\.[0-9]+[a-z]?$", num):
            got.append(num)
    md = io.open(os.path.join(BASE, "MinerU", "full_merged.md"), encoding="utf-8").read()
    ocr = re.findall(r"\\tag\{([0-9]+\*?\.[0-9]+[a-z]?)\}", md)
    ocr_set, got_set = set(ocr), set(got)
    print("== captured eq numbers:", len(got), "unique:", len(got_set))
    print("== ocr tags:", len(ocr), "unique:", len(ocr_set))
    miss = sorted(ocr_set - got_set, key=key)
    extra = sorted(got_set - ocr_set, key=key)
    print("   in OCR not in PDF:", len(miss))
    for m in miss:
        print("     -", m)
    print("   in PDF not in OCR:", len(extra))
    for m in extra:
        print("     +", m)
    # 重号检测（同号出现两次）
    from collections import Counter
    dup = [k for k, v in Counter(got).items() if v > 1]
    print("   duplicated numbers in PDF:", len(dup), dup[:20])
else:
    print("(eqnums.txt not found — run hook compile first)")
