"""Generate Table 1.5 (432(O)) and Table 1.6 (622(D6)) multiplication tables
from the Jones symbols of Table 1.4 (transcribed from the scan, p050).
All 24 improper operators are generated as componentwise flips (i.e. I*M) of
their proper partners, which is the book's own row-pairing rule in Table 1.4
(ICn+ = Sn-, IC2 = sigma, IC3+ = S6-, IC6+ = S3-).
Convention: cell(row L, col M) = L*M  (apply M first) - Table 1.1 note (ii).
"""
import numpy as np

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
    return np.array(rows)

def flip(tokens):
    return [('-' if t.startswith('-') else '-') + t[-1] for t in tokens]
    # note: above yields '--x' style; fixed below

def flip2(tokens):
    return [t if not t.startswith('-') else t[1:] for t in tokens]  # not used

def negate(tokens):
    return [('-' if not t.startswith('-') else '') + t[-1] for t in tokens]

def jones(tokens):
    bar = {'x': 'x̄', 'y': 'ȳ', 'z': 'z̄'}
    return ''.join(bar[t[-1]] if t.startswith('-') else t for t in tokens)

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
PROPER_HEX = {
    'E': 'xyz',
    'C6+': 'x-yx', 'C3+': '-yx-y', 'C2': '-x-yz',
    'C3-': 'y-x-x', 'C6-': 'yy-xz'[::-1],
}
# hex proper symbols are 3-token expressions, handled separately below

M = {k: mat(parse(v)) for k, v in PROPER.items()}
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
for k, src in IMPROPER_MAP.items():
    M[k] = -M[src]

lookup = {str(v.tolist()): k for k, v in M.items()}
assert len(lookup) == 24 + len(IMPROPER_MAP), 'collision'

ORDER = ['E', 'C2x', 'C2y', 'C2z',
         'C4x+', 'C4y+', 'C4z+', 'C4x-', 'C4y-', 'C4z-',
         'C31+', 'C32+', 'C33+', 'C34+', 'C31-', 'C32-', 'C33-', 'C34-',
         'C2a', 'C2b', 'C2c', 'C2d', 'C2e', 'C2f']

lines = []
for L in ORDER:
    row = []
    for Rc in ORDER:
        P = M[L] @ M[Rc]
        row.append(lookup[str(P.tolist())])
    lines.append((L, row))

with open('table15.txt', 'w', encoding='utf-8') as f:
    f.write('cols: ' + ' '.join(ORDER) + '\n')
    for L, row in lines:
        f.write(L + ' ' + ' '.join(row) + '\n')
print('written table15.txt, size', len(ORDER))
