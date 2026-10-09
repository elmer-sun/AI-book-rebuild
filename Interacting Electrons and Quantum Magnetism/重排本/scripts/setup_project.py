# -*- coding: utf-8 -*-
"""初始化《Interacting Electrons and Quantum Magnetism》中文重排工程。
1) 按章拆分两个提取文件夹的 full.md 到 md/chNN.md
2) 复制插图到 figures/ 并按 figN_N 命名
"""
import os, re, shutil, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 重排本/
BOOK = os.path.dirname(ROOT)                                        # 量子磁性/
F1 = os.path.join(BOOK, '978-1-4612-0869-3.pdf-03d00808-9b5c-4ad1-ad42-3bb81e8d1d27')
F2 = os.path.join(BOOK, '978-1-4612-0869-3.pdf-2d8250b2-2bf0-47cf-98f7-f191880f24fc')
MD = os.path.join(ROOT, 'md')
FIG = os.path.join(ROOT, 'figures')
os.makedirs(MD, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

md1 = open(os.path.join(F1, 'full.md'), encoding='utf-8').read()
md2 = open(os.path.join(F2, 'full.md'), encoding='utf-8').read()
lines1 = md1.split('\n')
lines2 = md2.split('\n')

# ---------- 1. 按章拆分 ----------
# F1 章（level-1 标题行号，1-based）：前置 + Part 标记 + 章
f1_bounds = [
    ('front',   1,    282),   # 扉页/系列页/序言/目录
    ('part1',   283,  289),
    ('ch01',    290,  480),
    ('ch02',    481,  790),
    ('ch03',    791,  1249),
    ('part2',   1250, 1254),
    ('ch04',    1255, 1586),
    ('ch05',    1587, 2014),
    ('ch06',    2015, 2374),
    ('ch07',    2375, 2683),
    ('ch08',    2684, 3085),
    ('ch09',    3086, 3271),
    ('part3',   3272, 3276),
    ('ch10',    3277, 3636),
    ('ch11',    3637, 4197),
    ('ch12',    4198, 4503),
    ('ch13',    4504, 4970),
    ('ch14',    4971, 5162),
    ('ch15',    5163, 5335),
    ('ch16',    5336, 5661),
    ('ch17',    5662, 6025),
    ('ch18_f1', 6026, 6626),
]
f2_bounds = [
    ('ch18_f2', 1,    86),    # 18.3 Exercises + Bibliography（属于第18章）
    ('ch19',    87,   647),
    ('part4',   648,  652),
    ('appA',    653,  866),
    ('appB',    867,  1062),
    ('appC',    1063, 1254),
    ('appD',    1255, 1508),
    ('appE',    1509, 1641),
    ('index',   1642, 1883),
]
for src, bounds in [(lines1, f1_bounds), (lines2, f2_bounds)]:
    for name, a, b in bounds:
        out = os.path.join(MD, name + '.md')
        with open(out, 'w', encoding='utf-8') as f:
            f.write('\n'.join(src[a-1:b]))
print('md split done:', len(os.listdir(MD)), 'files')

# ---------- 2. 图片复制重命名 ----------
FIGMAP = {
    # F1（行号 -> 命名）
    ('F1', 287):  'deco_part1',
    ('F1', 410):  'fig1_1a',
    ('F1', 412):  'fig1_1b',
    ('F1', 501):  'fig2_1',
    ('F1', 581):  'fig2_2',
    ('F1', 731):  'fig2_3a',
    ('F1', 734):  'fig2_3b',
    ('F1', 1033): 'fig3_1',
    ('F1', 1168): 'fig3_2',
    ('F1', 1181): 'fig3_3',
    ('F1', 1252): 'deco_part2',
    ('F1', 1311): 'fig4_1',
    ('F1', 1480): 'fig4_2',
    ('F1', 2447): 'fig7_1',
    ('F1', 2700): 'fig8_1',
    ('F1', 2753): 'fig8_2',
    ('F1', 2776): 'fig8_3',
    ('F1', 2873): 'fig8_4',
    ('F1', 3274): 'deco_part3',
    ('F1', 3371): 'fig10_1',
    ('F1', 3659): 'fig11_1',
    ('F1', 3856): 'fig11_2',
    ('F1', 3893): 'fig11_3',
    ('F1', 4820): 'fig13_1',
    ('F1', 5227): 'fig15_1',
    ('F1', 5800): 'fig17_1',
    ('F1', 5835): 'fig17_2',
    ('F1', 5862): 'fig17_3',
    ('F1', 5915): 'fig17_4',
    ('F1', 5948): 'fig17_5',
    ('F1', 5971): 'fig17_6',
    ('F1', 5974): 'fig17_7',
    ('F1', 6106): 'fig18_1',
    ('F1', 6269): 'fig18_2',
    ('F1', 6416): 'fig18_3',
    ('F2', 353):  'fig19_1',
    ('F2', 386):  'fig19_2',
    ('F2', 509):  'fig19_3',
    ('F2', 650):  'deco_part4',
    ('F2', 1549): 'figE_1',
}
def img_at(lines, ln):  # ln 1-based
    l = lines[ln-1]
    m = re.match(r'!\[\]\(images/([0-9a-f]+)\.(jpg|png)\)', l.strip())
    if not m:
        raise SystemExit('line %d is not an image ref: %r' % (ln, l[:80]))
    return m.group(1), m.group(2)

for (tag, ln), name in FIGMAP.items():
    lines = lines1 if tag == 'F1' else lines2
    folder = F1 if tag == 'F1' else F2
    h, ext = img_at(lines, ln)
    src = os.path.join(folder, 'images', h + '.' + ext)
    dst = os.path.join(FIG, name + '.' + ext)
    shutil.copyfile(src, dst)
print('figures copied:', len(FIGMAP))

# ---------- 3. 校验：图2.1 的题注（L500 后两行） ----------
print('fig2_1 context:', repr('\n'.join(lines1[499:505])))
