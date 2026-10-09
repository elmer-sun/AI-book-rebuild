"""Generate Table 1.6 (622(D6)) from hexagonal-basis Jones symbols (Table 1.4b).
Same convention: cell(row L, col M) = L*M (apply M first). Verified against scan:
row C6+ = [C6+ C3+ C2 C3- C6- E], row C2 dyad block = [C21'' C22'' C23' C21' C22' C23'']. """
import numpy as np

def M(rows):
    return np.array(rows, dtype=int)

D6 = {
    'E':    M([[1,0,0],[0,1,0],[0,0,1]]),
    'C6+':  M([[1,-1,0],[1,0,0],[0,0,1]]),
    'C3+':  M([[0,-1,0],[1,-1,0],[0,0,1]]),
    'C2':   M([[-1,0,0],[0,-1,0],[0,0,1]]),
    'C3-':  M([[-1,1,0],[-1,0,0],[0,0,1]]),
    'C6-':  M([[0,1,0],[-1,1,0],[0,0,1]]),
    "C21'": M([[-1,1,0],[0,1,0],[0,0,-1]]),
    "C22'": M([[1,0,0],[1,-1,0],[0,0,-1]]),
    "C23'": M([[0,-1,0],[-1,0,0],[0,0,-1]]),
    'C21"': M([[1,-1,0],[0,-1,0],[0,0,-1]]),
    'C22"': M([[-1,0,0],[-1,1,0],[0,0,-1]]),
    'C23"': M([[0,1,0],[1,0,0],[0,0,-1]]),
}
ORDER = ['E','C6+','C3+','C2','C3-','C6-',"C21'","C22'","C23'",'C21"','C22"','C23"']
lookup = {str(v.tolist()): k for k, v in D6.items()}
assert len(lookup) == 12

def bk(k):
    if k == 'E':
        return '$E$'
    if k in ('C6+', 'C6-', 'C3+', 'C3-', 'C2'):
        sup = {'C6+': '+', 'C6-': '-', 'C3+': '+', 'C3-': '-', 'C2': ''}[k]
        if sup:
            return '$C_{%s}^{%s}$' % (k[1], sup)
        return '$C_{%s}$' % k[1]
    prime = "'" if k.endswith("'") else "''"
    n = k[2]
    return "$C%s_{2%s}$" % (prime, n)

hdr = '| | ' + ' | '.join(bk(k) for k in ORDER) + ' |'
sep = '|' + '---|' * 13
rows = [hdr, sep]
for L in ORDER:
    cells = [lookup[str((D6[L] @ D6[R]).tolist())] for R in ORDER]
    rows.append('| ' + bk(L) + ' | ' + ' | '.join(bk(c) for c in cells) + ' |')
open('table16_md.txt', 'w', encoding='utf-8').write('\n'.join(rows))
# plain dump for eyeball check
for L in ORDER:
    print(L, [lookup[str((D6[L] @ D6[R]).tolist())] for R in ORDER])
