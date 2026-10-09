# -*- coding: utf-8 -*-
"""Regenerate Tables 1.5/1.6 markdown + LaTeX with CORRECT labels.
Fixes the bk() subscript bug (C_{4-}^{} instead of C_{4x}^{-}, etc.)
and rewrites the English page files p051.md / p052.md accordingly."""
import io, re
import numpy as np

BS = chr(92)

AX = {'x': 0, 'y': 1, 'z': 2}

def parse(s):
    out, neg = [], False
    for ch in s:
        if ch == '-':
            neg = True
        else:
            out.append(('-' if neg else '') + ch)
            neg = False
    return out

def mat(tokens):
    rows = []
    for t in tokens:
        sign = -1 if t.startswith('-') else 1
        r = [0, 0, 0]
        r[AX[t[-1]]] = sign
        rows.append(r)
    return np.array(rows, dtype=int)

def negate(tokens):
    return [('-' if not t.startswith('-') else '') + t[-1] for t in tokens]

PROPER = {
    'E': 'xyz',
    'C2x': 'x-y-z', 'C2y': '-xy-z', 'C2z': '-x-yz',
    'C4x+': 'x-zy', 'C4y+': 'zy-x', 'C4z+': '-yxz',
    'C4x-': 'xz-y', 'C4y-': '-zyx', 'C4z-': 'y-xz',
    'C31+': 'zxy', 'C32+': '-zx-y', 'C33+': '-z-xy', 'C34+': 'z-x-y',
    'C31-': 'yzx', 'C32-': 'y-z-x', 'C33-': '-yz-x', 'C34-': '-y-zx',
    'C2a': 'yx-z', 'C2b': '-y-x-z', 'C2c': 'z-yx',
    'C2d': '-z-y-x', 'C2e': '-xzy', 'C2f': '-x-z-y',
}
IMPROPER_MAP = {
    'I': 'E',
    'sx': 'C2x', 'sy': 'C2y', 'sz': 'C2z',
    'S4x-': 'C4x+', 'S4y-': 'C4y+', 'S4z-': 'C4z+',
    'S4x+': 'C4x-', 'S4y+': 'C4y-', 'S4z+': 'C4z-',
    'S61-': 'C31+', 'S62-': 'C32+', 'S63-': 'C33+', 'S64-': 'C34+',
    'S61+': 'C31-', 'S62+': 'C32-', 'S63+': 'C33-', 'S64+': 'C34-',
    'sda': 'C2a', 'sdb': 'C2b', 'sdc': 'C2c',
    'sdd': 'C2d', 'sde': 'C2e', 'sdf': 'C2f',
}
M = {k: mat(parse(v)) for k, v in PROPER.items()}
for k, src in IMPROPER_MAP.items():
    M[k] = -M[src]
lookup = {str(v.tolist()): k for k, v in M.items()}
assert len(lookup) == 24 + len(IMPROPER_MAP), 'collision'

ORDER = ['E', 'C2x', 'C2y', 'C2z',
         'C4x-', 'C4y-', 'C4z-', 'C4x+', 'C4y+', 'C4z+',
         'C31-', 'C32-', 'C33-', 'C34-', 'C31+', 'C32+', 'C33+', 'C34+',
         'C2a', 'C2b', 'C2c', 'C2d', 'C2e', 'C2f']

def label(k):
    """Book-correct label for an internal key."""
    if k == 'E':
        return '$E$'
    sup = ''
    if k.endswith('+'):
        sup = '+'; k2 = k[:-1]
    elif k.endswith('-'):
        sup = '-'; k2 = k[:-1]
    else:
        k2 = k
    if k2.startswith('S4'):
        base = 'S_{4' + k2[2] + '}'
    elif k2.startswith('S6'):
        base = 'S_{6' + k2[2] + '}'
    elif k2.startswith('C4'):
        base = 'C_{4' + k2[2] + '}'
    elif k2[:3] in ('C31', 'C32', 'C33', 'C34'):
        base = 'C_{' + k2[1:] + '}'
    elif k2.startswith('C2'):
        base = 'C_{2' + k2[2] + '}'
    else:
        raise ValueError(k)
    if sup:
        return '$' + base + '^{' + sup + '}$'
    return '$' + base + '$'

def table15_rows():
    out = []
    for L in ORDER:
        cells = [lookup[str((M[L] @ M[C]).tolist())] for C in ORDER]
        out.append((label(L), [label(c) for c in cells]))
    return out

rows15 = table15_rows()
hdr = '| | ' + ' | '.join(r[0] for r in rows15) + ' |'
sep = '|' + '---|' * 25
md15 = '\n'.join([hdr, sep] + ['| ' + r[0] + ' | ' + ' | '.join(r[1]) + ' |' for r in rows15])
io.open('table15_md.txt', 'w', encoding='utf-8', newline='\n').write(md15)

# ---- hexagonal (Table 1.6) ----
def H(rows):
    return np.array(rows, dtype=int)
D6 = {
    'E':    H([[1,0,0],[0,1,0],[0,0,1]]),
    'C6+':  H([[1,-1,0],[1,0,0],[0,0,1]]),
    'C3+':  H([[0,-1,0],[1,-1,0],[0,0,1]]),
    'C2':   H([[-1,0,0],[0,-1,0],[0,0,1]]),
    'C3-':  H([[-1,1,0],[-1,0,0],[0,0,1]]),
    'C6-':  H([[0,1,0],[-1,1,0],[0,0,1]]),
    "C21'": H([[-1,1,0],[0,1,0],[0,0,-1]]),
    "C22'": H([[1,0,0],[1,-1,0],[0,0,-1]]),
    "C23'": H([[0,-1,0],[-1,0,0],[0,0,-1]]),
    'C21"': H([[1,-1,0],[0,-1,0],[0,0,-1]]),
    'C22"': H([[-1,0,0],[-1,1,0],[0,0,-1]]),
    'C23"': H([[0,1,0],[1,0,0],[0,0,-1]]),
}
ORDER6 = ['E','C6+','C3+','C2','C3-','C6-',"C21'","C22'","C23'",'C21"','C22"','C23"']
lookup6 = {str(v.tolist()): k for k, v in D6.items()}
assert len(lookup6) == 12

def label6(k):
    if k == 'E':
        return '$E$'
    if k.startswith('C6'):
        return '$C_{6}^{' + ('+' if k[-1] == '+' else '-') + '}$'
    if k.startswith('C3'):
        return '$C_{3}^{' + ('+' if k[-1] == '+' else '-') + '}$'
    if k == 'C2':
        return '$C_{2}$'
    d = k[2]
    prime = "'" if k.endswith("'") else "''"
    return '$C' + prime + '_{2' + d + '}$'

rows16 = []
for L in ORDER6:
    cells = [lookup6[str((D6[L] @ D6[R]).tolist())] for R in ORDER6]
    rows16.append((label6(L), [label6(c) for c in cells]))
hdr = '| | ' + ' | '.join(r[0] for r in rows16) + ' |'
sep = '|' + '---|' * 13
md16 = '\n'.join([hdr, sep] + ['| ' + r[0] + ' | ' + ' | '.join(r[1]) + ' |' for r in rows16])
io.open('table16_md.txt', 'w', encoding='utf-8', newline='\n').write(md16)

# ---- rewrite English page files p051.md / p052.md ----
p51 = """<!-- PDF p.51 / 印刷页 p.38（横排页） -->
<!-- Table 1.5 的 576 个单元格由已核实的 Table 1.4 Jones 符号按群乘法程序生成
     （gen_mult_tables.py），并与扫描件逐块抽查核对：表头顺序、E 的位置、
     C2x/C2y/C2z 块、C4y- 行、C31- 行等均一致。 -->

**TABLE 1.5**

*The group multiplication table for the point group* 432 ($O$)

""" + md15 + '\n'
io.open('md/p051.md', 'w', encoding='utf-8', newline='\n').write(p51)

p52 = """<!-- PDF p.52 / 印刷页 p.39 -->
<!-- Table 1.6 由 Table 1.4(b) 六方 Jones 符号按群乘法程序生成（gen_table16.py），
     与扫描件逐行核对一致（E 的位置、C6+/C3+/C2 行、C2 行方向测试等）。 -->

**TABLE 1.6**

*The group multiplication table for the point group* 622 ($D_{6}$)

""" + md16 + """

exactly similar array of atoms or molecules to the array that he would see if he were to view the crystal from any other of these lattice points. Strictly speaking, in order to obtain complete similarity of the environment of each lattice point it is necessary that a mathematical lattice be of infinite extent. A real crystal clearly cannot contain such an infinite lattice but, remembering the actual sizes of atoms, it will be a close approximation to an infinite lattice. We may illustrate the idea of a lattice with a 2-dimensional example; if the set of points in Fig. 1.6, which are arranged at the

![FIG. 1.6](figures/fig1_6.png)

FIG. 1.6. The square 2-dimensional Bravais lattice, $p$.
"""
io.open('md/p052.md', 'w', encoding='utf-8', newline='\n').write(p52)
print('tables regenerated; p051/p052 updated')
