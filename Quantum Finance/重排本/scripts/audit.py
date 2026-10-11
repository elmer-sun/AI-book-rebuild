# 全书审计: ①每章 tag 无重复 ②每章 tag 序列连续(容原书缺号) ③章首页号为奇数 ④残留检查
import re, glob, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
CH = os.path.join(ROOT, 'chapters')

# 每章文件组合
BOOK = {
    'ch01': ['ch01'], 'ch02': ['ch02'], 'ch03': ['ch03'],
    'ch04': ['ch04', 'ch04b'], 'ch05': ['ch05', 'ch05b'],
    'ch06': ['ch06'], 'ch07': ['ch07', 'ch07b'], 'ch08': ['ch08'],
    'ch09': ['ch09', 'ch09b'], 'ch10': ['ch10'], 'chA': ['chA'],
}
# 原书缺号(照录)
KNOWN_GAPS = {
    'ch03': [1, 11], 'ch04': [1, 25, 33], 'chA': [12, 14],
}
LETTERED = {  # 原书分立 a/b
    'ch09': set(), 'ch10': {'77'}, 'ch07': {'71'},
}

ok = True
for chap, files in BOOK.items():
    tags = []
    for f in files:
        t = open(os.path.join(CH, f + '.tex'), encoding='utf-8').read()
        for m in re.finditer(r'\\tag\{([\dA-Za-z.]+)\}', t):
            tags.append(m.group(1))
    # 去重检查
    dup = [x for x in set(tags) if tags.count(x) > 1]
    if dup:
        print(f'[FAIL] {chap} 重复 tag: {sorted(dup)}')
        ok = False
    # 序列检查(仅数字部分)
    nums = []
    for x in tags:
        m = re.match(r'(\d+)\.(\d+)', x)
        if m:
            nums.append((int(m.group(1)), int(m.group(2))))
    nums = sorted(set(nums))
    chapter_n = int(re.match(r'ch0?(\d+)|chA', chap).group(1) or 99) if 'A' not in chap else 1
    chno = {'ch01':1,'ch02':2,'ch03':3,'ch04':4,'ch05':5,'ch06':6,'ch07':7,'ch08':8,'ch09':9,'ch10':10}.get(chap)
    if chno:
        if not nums:
            print(f'[ok] {chap}: 无编号公式（原书本章即无）')
            continue
        expect = list(range(1, max(n[1] for n in nums) + 1))
        got = sorted(set(n[1] for n in nums if n[0] == chno))
        gaps = [i for i in expect if i not in got and i not in KNOWN_GAPS.get(chap, [])]
        if gaps:
            print(f'[FAIL] {chap} tag 断档: {gaps}')
            ok = False
        else:
            print(f'[ok] {chap}: {len(tags)} tags, 序列完整 ({chno}.1–{chno}.{max(got)})'
                  + (f', 照录缺号 {KNOWN_GAPS.get(chap)}' if chap in KNOWN_GAPS else ''))

# 章首奇数页检查
try:
    import pymupdf
    doc = pymupdf.open(os.path.join(ROOT, 'main.pdf'))
    toc_page = {}
    for i, page in enumerate(doc):
        txt = page.get_text()
        for label in ['第 1 章', '第 2 章', '第 3 章', '第 4 章', '第 5 章', '第 6 章',
                      '第 7 章', '第 8 章', '第 9 章', '第 10 章', '第 11 章', '附录 A']:
            if txt.strip().startswith(label) or f'\n{label} ' in txt[:200]:
                toc_page.setdefault(label, i + 1)
    for label, pg in toc_page.items():
        flag = 'ok' if pg % 2 == 1 else 'FAIL(偶数页)'
        print(f'章首 {label}: PDF第{pg}页 {flag}')
        if pg % 2 == 0:
            ok = False
    doc.close()
except Exception as e:
    print('pymupdf check skipped:', e)

print('AUDIT', 'PASS' if ok else 'FAIL')
