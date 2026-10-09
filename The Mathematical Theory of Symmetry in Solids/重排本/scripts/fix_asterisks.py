# -*- coding: utf-8 -*-
"""Fix asterisk-leaks and quotes in Chinese chapter files."""
import io, re, glob

files = ['chapters/ch1_s1.tex', 'chapters/ch1_s2.tex', 'chapters/ch1_s3.tex',
         'chapters/ch1_s4.tex', 'chapters/ch1_s5.tex']

for p in files:
    s = io.open(p, encoding='utf-8').read()
    before = s.count('*')
    # citation year suffixes: *a* *b* *c* *d* -> superscript
    for ch in 'abcd':
        s = s.replace('*%s*' % ch, r'\textsuperscript{' + ch + '}')
    # lattice names / other single letters
    s = s.replace('*p*', r'\textit{p}')
    # any remaining *...* italics
    s = re.sub(r'\*([^*\n]+?)\*', lambda m: r'\textit{' + m.group(1) + '}', s)
    # straight quotes around 推导 etc -> Chinese quotes
    s = s.replace('"推导"', '“推导”')
    s = s.replace('"警示"', '“警示”')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print(p, 'asterisks:', before, '->', s.count('*'))
