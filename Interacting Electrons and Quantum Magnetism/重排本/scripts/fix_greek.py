# -*- coding: utf-8 -*-
"""修复正文文本模式下的裸希腊字母（中文相邻处）-> LaTeX 命令。"""
import glob, re

GREEKS = {
    'σ': '\\sigma', 'Θ': '\\Theta', 'Υ': '\\Upsilon', 'π': '\\pi',
    'δ': '\\delta', 'ρ': '\\rho', 'χ': '\\chi', 'θ': '\\theta',
    'φ': '\\phi', 'κ': '\\kappa', 'η': '\\eta', 'Σ': '\\Sigma',
    'Γ': '\\Gamma', 'Ω': '\\Omega', 'μ': '\\mu', 'τ': '\\tau',
    'β': '\\beta', 'ζ': '\\zeta', 'ε': '\\epsilon', 'λ': '\\lambda',
    'ω': '\\omega', 'α': '\\alpha', 'γ': '\\gamma', 'ψ': '\\psi',
    'ξ': '\\xi', 'ν': '\\nu', 'Δ': '\\Delta', 'Π': '\\Pi',
    'Φ': '\\Phi', 'Ψ': '\\Psi', 'Λ': '\\Lambda', 'Σ': '\\Sigma',
}

files = sorted(glob.glob('chapters/*.tex')) + ['main.tex']
total = 0
for f in files:
    s = open(f, encoding='utf-8').read()
    keys = ''.join(GREEKS.keys())
    # 裸希腊字母出现在中文语境：前或后是中文字符/中文标点（数学模式内的不会如此）
    pat = re.compile('(?<!\\\\)([' + keys + '])(?=[\\u4e00-\\u9fff\\s（）：、，。；“”]|$)')
    def repl(m):
        return '{$%s$}' % GREEKS[m.group(1)]
    n = len(pat.findall(s))
    if n:
        s2 = pat.sub(repl, s)
        open(f, 'w', encoding='utf-8').write(s2)
        # 报告每种字符
        from collections import Counter
        cnt = Counter(m.group(1) for m in pat.finditer(s))
        print(f, n, dict(cnt))
    total += n
print('total replaced:', total)
