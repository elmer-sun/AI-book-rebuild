# -*- coding: utf-8 -*-
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\chapters\ch12.tex"
text = open(path, encoding='utf-8').read()
lines = text.split('\n')

section = ''
count = 0
for i, line in enumerate(lines, 1):
    m = re.match(r'\\section\{(.+?)\}', line)
    if m:
        section = m.group(1)
    # circled marks
    for ch in '①②③④':
        for mm in re.finditer(re.escape(ch), line):
            count += 1
            s = max(0, mm.start()-25)
            ctx = line[s:mm.end()+15].replace('\n',' ')
            print(f"{count:02d} L{i:4d} [{ch}] §{section} | …{ctx}…")
    # standalone asterisk footnote: an asterisk attached to Chinese text (not \begin{}, \tag, equation, etc.)
    for mm in re.finditer(r'(?<![\w\\{}$^\d])\*(?![\w{}=])', line):
        ctx = line[max(0,mm.start()-30):mm.end()+20]
        if re.search(r'[\u4e00-\u9fff]', ctx):
            count += 1
            print(f"{count:02d} L{i:4d} [*] §{section} | …{ctx}…")
print("TOTAL", count)
