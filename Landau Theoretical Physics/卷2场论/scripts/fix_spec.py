# -*- coding: utf-8 -*-
"""修正卷2排版规范.md中的OCR源路径描述"""
import os
os.chdir(r'E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本')
s = open('排版规范.md', encoding='utf-8').read()
old = '- OCR 源：`E:\\AI整理书籍\\朗道理论物理教程\\卷2场论\\MinerU\\原书_卷2场论_高教社中文第5版\\full.md`'
new = ('- OCR 三块已合并为单文件：`E:\\AI整理书籍\\朗道理论物理教程\\卷2场论\\MinerU\\full_merged.md`\n'
       '  （任务单给全局行号区间，用 Read 带 offset/limit 读取）。')
assert old in s, 'pattern not found'
s = s.replace(old, new)
open('排版规范.md', 'w', encoding='utf-8').write(s)
print('fixed')
