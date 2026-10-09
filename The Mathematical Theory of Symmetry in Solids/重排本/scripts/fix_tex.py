# -*- coding: utf-8 -*-
"""Normalize a chapter .tex written with md-isms into pure LaTeX:
   - $$...$$ (with optional \\tag)  -> \\begin{equation*}...\\end{equation*}
   - runs of '> ' lines             -> \\begin{quote}...\\end{quote}
   - inline ‡ / § markers paired with trailing 脚注： blocks -> \\footnote{...}
Usage: python fix_tex.py file1 [file2 ...]
"""
import io, re, sys

for path in sys.argv[1:]:
    s = io.open(path, encoding='utf-8').read()

    # footnote notes at file end: --- \n 脚注： \n ‡text / §text
    notes = []
    def grab(m):
        notes.extend(re.findall('^([‡§]) (.+)$', m.group(0), flags=re.M))
        return '\n'
    s = re.sub(r'\n---\n脚注：\n(?:[‡§][^\n]+\n?)+', grab, s, flags=re.S)
    s = re.sub(r'\n脚注：\n(?:[‡§][^\n]+\n?)+', '\n', s)

    q = {'‡': iter(t for c, t in notes if c == '‡'),
         '§': iter(t for c, t in notes if c == '§')}
    def sub_marker(m):
        ch = m.group(0)
        try:
            txt = next(q[ch])
        except StopIteration:
            return (r'\textsuperscript{\ddag}' if ch == '‡' else r'\textsuperscript{\S}')
        return r'\footnote{' + txt + '}'
    s = re.sub(r'[‡§]', sub_marker, s)

    # display math
    s = re.sub(r'\$\$(.*?)\$\$', lambda m: '\n\\begin{equation*}\n' + m.group(1).strip() + '\n\\end{equation*}\n', s, flags=re.S)

    # blockquote runs
    lines = s.split('\n')
    out = []
    run = []
    for ln in lines:
        if ln.startswith('>'):
            run.append(ln[1:].lstrip())
        else:
            if run:
                out.append('\\begin{quote}')
                out.extend(run)
                out.append('\\end{quote}')
                run = []
            out.append(ln)
    if run:
        out.append('\\begin{quote}')
        out.extend(run)
        out.append('\\end{quote}')
    s = '\n'.join(out)
    s = re.sub(r'\n{3,}', '\n\n', s)

    io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
    print('normalized', path, '| footnotes:', len(notes))
