# -*- coding: utf-8 -*-
"""Locate the PDF page (page_idx) of each footnote marker context via MinerU content_list_v2.json."""
import json, io, glob

BASE = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\MinerU"
DIRS = ["01_p001-160", "02_p161-320", "03_p321-460"]
OFFSET = [0, 160, 320]

def load_blocks():
    blocks = []
    for di, d in enumerate(DIRS):
        c = glob.glob(BASE + "\\" + d + "\\*_content_list_v2.json")[0]
        data = json.load(io.open(c, encoding="utf-8"))
        for pi, page in enumerate(data):
            for block in page:
                if block.get("type") == "paragraph":
                    pc = block.get("content", {}).get("paragraph_content", [])
                    txt = "".join(seg.get("content", "") for seg in pc if isinstance(seg, dict))
                    blocks.append((OFFSET[di] + pi + 1, txt))  # 1-based page = p-NNN
    return blocks

BLOCKS = load_blocks()

def find(snippet):
    return [pg for pg, txt in BLOCKS if snippet in txt]

targets = [
    ("ch07 L203", "成正比①"),
    ("ch07 L294", "发光点的像）①"),
    ("ch07 L298", "情形是例外②"),
    ("ch07 L304", "轴对称的光学系统③"),
    ("ch07 L422", "（图8）①"),
    ("ch07 L487", "式中①"),
    ("ch07 L621", "在光①传播"),
    ("ch07 L722", "艾里函数①"),
    ("ch07 L915", "波面才重要）①"),
    ("ch07 L1006", "公式成立①"),
    ("ch08 L152", "只有一个根"),
    ("ch08 L408", "三级近似下发生"),
    ("ch08 L466", "这时，我们得到①"),
    ("ch08 L578", "产生的势①"),
    ("ch09 L76 ①②", "对时间微分①"),
    ("ch09 L85 ③", "因此③"),
    ("ch09 L269", "的辐射.①"),
    ("ch09 L315", "代表之①"),
    ("ch09 L319", "有效辐射等等②"),
    ("ch09 L323", "偶极矩③"),
    ("ch09 L409", "常数极限①"),
    ("ch09 L418", "都是满足的.①"),
    ("ch09 L428", "进行积分后得到②"),
    ("ch09 L533", "艾里函数①"),
    ("ch09 L594", "我们便得到①"),
    ("ch09 L610", "一个任意解①"),
    ("ch09 L829", "经过简单的计算①"),
    ("ch09 L884", "结果是：①"),
    ("ch09 L910", "时刻的值①"),
    ("ch09 L1039", "计算给出①"),
    ("ch09 L1182", "几乎不偏转"),
    ("ch09 L1395", "参见(73.12)①"),
    ("ch09 L1402", "谱分布公式①"),
    ("ch09 L1411", "常数极限"),
    ("ch09 L1441", "数值计算是便利"),
    ("ch09 L1585", "作稳定运动"),
    ("ch09 L1619", "平均损失如下①"),
    ("ch09 L1679", "不适用了①"),
    ("ch09 L1791", "大很多①"),
    ("ch09 L1869", "横向力"),
    ("ch09 L2079", "进行平均①"),
    ("ch09 L2276", "四次幂成比例①"),
    ("ch09 L2311", "之差①"),
]

for name, snip in targets:
    print(name, "->", find(snip))
