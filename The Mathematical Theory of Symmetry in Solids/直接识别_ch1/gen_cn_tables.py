# -*- coding: utf-8 -*-
"""Convert corrected table15/16 markdown into Chinese-book tabular files t15/t16."""
import io, re

BS = chr(92)
NL = chr(10)

def md2tabular(src, dst, note_lines):
    s = io.open(src, encoding='utf-8').read()
    rows = [r for r in s.strip().split(NL) if not re.match(r'^\|[\s:|-]+\|$', r)]
    ncol = rows[0].count('|') - 1
    out = []
    out.append('\\noindent\\resizebox{' + BS + 'textwidth}{!}{%')
    out.append('\\begin{tabular}{' + ('|c|' * ncol) + '}')
    out.append('\\hline')
    for r in rows:
        cells = [c.strip() for c in r.strip().strip('|').split('|')]
        cells += [''] * (ncol - len(cells))
        out.append(' & '.join(cells[:ncol]) + ' \\\\ ' + BS + 'hline')
    out.append('\\end{tabular}}')
    if note_lines:
        out.append('')
        out.append('\\parbox{0.92' + BS + 'textwidth}{')
        for nl in note_lines:
            out.append(nl)
        out.append('}')
    io.open(dst, 'w', encoding='utf-8', newline=NL).write(NL.join(out))
    print('written', dst)

note15 = [
    BS + 'textit{' + '表 1.5 的注.} 列标题自左至右依次为：$E$；$C_{2x}, C_{2y}, C_{2z}$；'
    '$C_{4x}^{-}, C_{4y}^{-}, C_{4z}^{-}, C_{4x}^{+}, C_{4y}^{+}, C_{4z}^{+}$；'
    '$C_{31}^{-}, C_{32}^{-}, C_{33}^{-}, C_{34}^{-}, C_{31}^{+}, C_{32}^{+}, C_{33}^{+}, C_{34}^{+}$；'
    '$C_{2a}, C_{2b}, C_{2c}, C_{2d}, C_{2e}, C_{2f}$。行标题相同，顺序一致。'
    '求乘积 $LM$ 时，取行首元素为 $L$ 的一行与列标题为 $M$ 的一列的交叉格。——中译者',
]
note16 = [
    BS + 'textit{' + '表 1.6 的注.} 列标题自左至右依次为：$E$；'
    '$C_{6}^{+}, C_{3}^{+}, C_{2}, C_{3}^{-}, C_{6}^{-}$；'
    "$C'_{21}, C'_{22}, C'_{23}, C''_{21}, C''_{22}, C''_{23}$。行标题相同，顺序一致。"
    '求乘积 $LM$ 时，取行首元素为 $L$ 的一行与列标题为 $M$ 的一列的交叉格。——中译者',
]

md2tabular('table15_md.txt', '../重排本/chapters/t15.tex', note15)
md2tabular('table16_md.txt', '../重排本/chapters/t16.tex', note16)
