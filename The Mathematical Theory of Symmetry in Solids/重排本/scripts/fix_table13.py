# -*- coding: utf-8 -*-
"""Fix Table 1.3: split long single-$ element lists so they can wrap inside the
p-column; move the notes parbox outside the table env. Also annotate Example
1.3.5 (book prints '1.3.2 1.3.4' without a conjunction)."""
import io, re

p = 'chapters/ch1_s4.tex'
s = io.open(p, encoding='utf-8').read()

# locate the Table 1.3 tabular block
start = s.find('\\begin{tabular}{|c|c|c|p{0.58')
end = s.find('\\end{tabular}', start) + len('\\end{tabular}')
assert start != -1 and end > start, 'table 1.3 tabular not found'
block = s[start:end]

def split_cell(m):
    content = m.group(1)
    if '=' in content or ',' not in content:
        return m.group(0)
    toks = [t.strip() for t in content.split(',')]
    return ', '.join('$' + t + '$' for t in toks)

new_block = re.sub(r'\$([^$]+)\$', split_cell, block)
s = s[:start] + new_block + s[end:]

# move notes parbox outside the table env
old_notes = None
m = re.search(r'\\smallskip\n\\parbox\{0\.92\\textwidth\}\{\\textit\{表 1\.3 的注\..*?\}\n\\end\{table\}', s, flags=re.S)
assert m, 'notes parbox not found'
notes_inner = re.search(r'\\textit\{表 1\.3 的注\.\s*(.*?)\}\s*$', m.group(0), flags=re.S).group(1)
notes_inner = notes_inner.strip()
s = s[:m.start()] + '\\end{table}\n\n\\noindent\\textit{表 1.3 的注.}\\ ' + notes_inner + s[m.end():]

io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('table 1.3 fixed')

# example 1.3.5 annotation
p = 'chapters/ch1_s3.tex'
s = io.open(p, encoding='utf-8').read()
old = '（见例 1.3.2 1.3.4）'
if old in s:
    s = s.replace(old, '（见例 1.3.2 1.3.4——原书如此）')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print('example 1.3.5 annotated')
