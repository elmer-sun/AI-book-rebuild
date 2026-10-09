# -*- coding: utf-8 -*-
"""Round-2 fixes for chapter 2:
1. citation asterisks in ch2_s*.tex (*a/*b/*c/*d single-letter patterns only,
   never touching math)
2. rewrite the scan-placeholder block in ch2_s3.tex with correct page mapping
   and unnumbered captions (caption*)
3. wrap Table 2.8 with its heading in a table[H]
4. raggedbottom in main.tex
"""
import io, re, os

BS = chr(92)

# ---------- 1. citation asterisks (single letters) ----------
for p in ['chapters/ch2_s1.tex', 'chapters/ch2_s2.tex', 'chapters/ch2_s3.tex', 'chapters/ch2_s4.tex']:
    s = io.open(p, encoding='utf-8').read()
    n0 = s.count('*')
    for ch in 'abcdef':
        s = s.replace('*%s*' % ch, BS + 'textsuperscript{' + ch + '}')
    s = s.replace('*p*', BS + 'textit{p}')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print(p, 'asterisks', n0, '->', s.count('*'))

# ---------- 2. rewrite scan block in ch2_s3 ----------
p = 'chapters/ch2_s3.tex'
s = io.open(p, encoding='utf-8').read()
start_marker = '\\begin{figure}[H]\n\\centering\n\\includegraphics[width=0.86\\textwidth]{c2_t22_p1.png}'
end_marker = '\\caption{\\textbf{表 2.7}\\ $O(3)$ 的表示 $\\mathscr{D}^{l}$ 与点群表示的相容表（原书扫描页，占位，待重新排版）。}\n\\end{figure}'
i0 = s.find(start_marker)
i1 = s.find(end_marker)
assert i0 != -1 and i1 != -1, 'scan block not found'
i1 += len(end_marker)

def fig(png, cap):
    return ('\\begin{figure}[H]\n\\centering\n\\includegraphics[width=0.86\\textwidth]{' +
            png + '}\n\\caption*{' + cap + '}\n\\end{figure}\n')

block = ''
block += fig('c2_t22_p1.png', '表 2.2（第一部分）：$1\\ (C_{1})$、$\\bar{1}\\ (C_{i})$、$2\\ (C_{2})$、$m\\ (C_{1h})$、$mm2\\ (C_{2v})$、$222\\ (D_{2})$、$2/m\\ (C_{2h})$ 的特征标表（原书扫描占位）。')
block += fig('c2_t22_p2.png', '表 2.2（第二部分）：$4\\ (C_{4})$、$\\bar{4}\\ (S_{4})$、$4/m\\ (C_{4h})$、$3\\ (C_{3})$、$\\bar{3}\\ (C_{3i})$、$32\\ (D_{3})$、$3m\\ (C_{3v})$、$\\bar{3}m\\ (D_{3d})$、$6\\ (C_{6})$、$\\bar{6}\\ (C_{3h})$、$6/m\\ (C_{6h})$ 的特征标表（原书扫描占位）。')
block += fig('c2_t22_p3.png', '表 2.2（第三部分）：$422\\ (D_{4})$、$4mm\\ (C_{4v})$、$\\bar{4}2m\\ (D_{2d})$、$4/mmm\\ (D_{4h})$、$622\\ (D_{6})$、$6mm\\ (C_{6v})$、$\\bar{6}2m\\ (D_{3h})$、$6/mmm\\ (D_{6h})$、$23\\ (T)$、$m3\\ (T_{h})$、$432\\ (O)$、$\\bar{4}3m\\ (T_{d})$、$m3m\\ (O_{h})$ 的特征标表，以及表 2.3（简并表示的矩阵）的开头（原书扫描占位）。')
block += fig('c2_t23.png', '表 2.3（续）：四方群、三方与六方群简并表示的矩阵（原书扫描占位）。')
block += fig('c2_t24_t25.png', '表 2.3（续）：三方与六方群的矩阵 Key，以及立方群二重简并表示 $E$ 的矩阵（原书扫描占位）。')
block += fig('c2_t25_t26.png', '表 2.3（结尾）与表 2.4（循环群的面谐函数）开头（原书扫描占位）。')
block += fig('c2_t26.png', '表 2.4（续）：循环群的面谐函数（原书扫描占位）。')
block += fig('c2_t27_p1.png', '表 2.4（结尾）及其注，与表 2.5（二面体群的面谐函数）（原书扫描占位）。')
block += fig('c2_t27_p2.png', '表 2.5（续）与表 2.6 的开头：三方、六方及立方群的面谐函数（原书扫描占位）。')
block += fig('c2_t27_p3.png', '表 2.6（续）：立方群与三方、六方群的面谐函数（原书扫描占位）。')
block += fig('c2_t27_p4.png', '表 2.7：$O(3)$ 的表示 $\\mathscr{D}^{l}$ 与点群表示的相容表（第一部分，原书扫描占位）。')
block += fig('c2_t27_p5.png', '表 2.7（第二部分，原书扫描占位）。')
block += fig('c2_t27_p6.png', '表 2.7（第三部分，原书扫描占位）。')
s = s[:i0] + block + s[i1:]
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('scan block rewritten')

# ---------- 3. Table 2.8 heading + table together ----------
p = 'chapters/ch2_s4.tex'
s = io.open(p, encoding='utf-8').read()
old = "\\textbf{表 2.8}\\quad \\textit{简并点群表示的} $[\\Delta]^{2}$ \\textit{与} $\\{\\Delta\\}^{2}$"
assert old in s, 't28 heading not found'
s = s.replace(old, '\\begin{table}[H]\n\\centering\n' + old, 1)
old2 = '\\smallskip\n\\noindent\\textit{表 2.8 的注.}'
assert old2 in s, 't28 note anchor not found'
s = s.replace(old2, '\\end{table}\n\n\\smallskip\\noindent\\textit{表 2.8 的注.}', 1)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('table 2.8 wrapped')

# ---------- 4. raggedbottom ----------
p = 'main.tex'
s = io.open(p, encoding='utf-8').read()
if 'raggedbottom' not in s:
    s = s.replace('\\clubpenalty=10000', '\\raggedbottom\n\\clubpenalty=10000')
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('raggedbottom added')
