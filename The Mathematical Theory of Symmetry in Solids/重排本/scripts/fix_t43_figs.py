# -*- coding: utf-8 -*-
"""修复 ch4_s5.tex 中表 4.3 图块的结构。"""
import io

p = r'E:\AI整理书籍\群论\重排本\chapters\ch4_s5.tex'
lines = io.open(p, encoding='utf-8').read().split('\n')

# 找到 p1..p4 四个 includegraphics 的位置
idx = {}
for i, l in enumerate(lines):
    for t in ('p1', 'p2', 'p3', 'p4'):
        if 'c4_t43_%s.png' % t in l:
            idx[t] = i

# 情况：p1 图块后有重复 \end{figure}；p4 图块缺 \end{figure}
# 1) 删除紧跟在 p1 图块 end{figure} 后的重复 end{figure}
j = idx['p1']
while not lines[j].strip().startswith('\\end{figure}'):
    j += 1
if lines[j + 1].strip().startswith('\\end{figure}'):
    del lines[j + 1]
    idx = {k: (v if v < j else v - 1) for k, v in idx.items()}

# 2) 给 p4 补 end{figure}
k = idx['p4']
while not lines[k].strip().startswith('\\caption'):
    k += 1
if not lines[k + 1].strip().startswith('\\end{figure}'):
    lines.insert(k + 1, '\\end{figure}')

io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('fixed ok')
