# -*- coding: utf-8 -*-
"""ch1.tex：9 幅扫描插图替换为 TikZ 重绘矢量图（figs/fig1_01..09.pdf）"""
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

MAP = {
    'fig1_1_crop.png':  'fig1_01.pdf',
    '8f242ae0347c9791101a70f8a645dffa0ff834fd72e8f25f1600aa1f2b8fb84c.jpg': 'fig1_02.pdf',
    'a53d0fda08806cb81029198aa97a8f187beaa8972dd093d10df14975e3bd4444.jpg': 'fig1_03.pdf',
    '9af02fef8dea2651b67bda0be27c7adb03e00c154847f68eb5ca4d3e7cb8ba14.jpg': 'fig1_04.pdf',
    '2dcdf420affcd83dc88615ef355c02a07b1339d95930eae74d2a79cc4531a5b5.jpg': 'fig1_05.pdf',
    'f974d30edbdf78cb7b8faaf4b421748e952721c880736e1ca7528f0c5e634e97.jpg': 'fig1_06.pdf',
    'c41bd504527ce655e38748e4ae93718def40bdca1bdd3edc488d0c8929160734.jpg': 'fig1_07.pdf',
    'a68eeaf60fa213a996d6d891b7bc63b2122a191b532d86e5fcfef207ca827e6e.jpg': 'fig1_08.pdf',
    '95a0e3d7965d64909e7601611762183f58cfa441fd941a68988f2da51282f673.jpg': 'fig1_09.pdf',
}

s = open('ch1.tex', encoding='utf-8').read()
n = 0
for old, new in MAP.items():
    needle = '{%s}' % old
    assert needle in s, old
    s = s.replace(needle, '{%s}' % new, 1)
    n += 1
open('ch1.tex', 'w', encoding='utf-8').write(s)
print('replaced', n, 'figures in ch1.tex')
