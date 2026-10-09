# -*- coding: utf-8 -*-
"""Convert ch1.md (constrained markdown from direct page-image recognition)
into ch1.tex for XeLaTeX.

md constructs handled:
  - HTML comments (stripped)
  - '# 1 Title' -> \chapter, '## 1.x. Title' -> \section
  - $$...$$ display math (with \tag, or \begin{aligned}) -> equation*/align*
  - $...$ inline math (passed through)
  - **bold**, *italic*
  - markdown tables: ncol>=7 wrapped in \resizebox; a table whose header has an
    'Elements' column gets that column as p{0.58\textwidth}
  - '**TABLE x**' label lines open a non-breaking minipage that also swallows
    the italic subtitle line and the following tabular
  - '> ' blockquotes, '- ' itemize
  - '![alt](path)' figures; following 'FIG. x.y. ...' paragraph becomes \caption
  - footnotes: inline markers paired in order with page-end note blocks
"""
import io, re, os

md = io.open('ch1.md', encoding='utf-8').read()

# 0. strip HTML comments
md = re.sub(r'<!--.*?-->', '', md, flags=re.S)

# 1. collect footnote texts (page-end blocks), then remove those blocks
notes = {'D': [], 'S': []}
for m in re.finditer('^([‡§]) (.+)$', md, flags=re.M):
    notes['D' if m.group(1) == '‡' else 'S'].append(m.group(2))
md = re.sub('\n---\n脚注：\n(?:‡[^\\n]+\\n|§[^\\n]+\\n)+', '\n', md)
md = re.sub('\n脚注：\n(?:‡[^\\n]+\\n|§[^\\n]+\\n)+', '\n', md)

# 2. protect display math
disp = []
def keep_disp(m):
    disp.append(m.group(1))
    return '\x02D%d\x02' % (len(disp) - 1)
md = re.sub(r'\$\$(.*?)\$\$', keep_disp, md, flags=re.S)

# 3. protect inline math
inline = []
def keep_inline(m):
    inline.append(m.group(1))
    return '\x02I%d\x02' % (len(inline) - 1)
md = re.sub(r'\$([^$\n]+?)\$', keep_inline, md)

# helpers
def esc_text(s):
    s = s.replace('‡', r'\textsuperscript{\ddag}')
    s = s.replace('§', r'\textsuperscript{\S}')
    s = s.replace('°', r'\textdegree ')
    s = s.replace('&', r'\&').replace('%', r'\%').replace('#', r'\#')
    s = s.replace('×', r'$\times$')
    return s

def latex_text(s):
    s = esc_text(s)
    s = re.sub(r'\*\*(.+?)\*\*', lambda m: r'\textbf{' + m.group(1) + '}', s)
    s = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', lambda m: r'\textit{' + m.group(1) + '}', s)
    return s

def fix_math(s):
    s = s.strip()
    if s.startswith('\\begin{aligned}'):
        inner = s[len('\\begin{aligned}'):-len('\\end{aligned}')]
        return '\\begin{align*}' + inner + '\\end{align*}'
    return s

def restore(s):
    def emit(m):
        content = fix_math(disp[int(m.group(1))])
        if content.startswith('\\begin{align*}'):
            return '\n' + content + '\n'
        return '\n\\begin{equation*}\n' + content + '\n\\end{equation*}\n'
    s = re.sub(r'\x02D(\d+)\x02', emit, s)
    s = re.sub(r'\x02I(\d+)\x02', lambda m: '$' + inline[int(m.group(1))] + '$', s)
    s = s.replace('\\|', '|')
    return s

# 4. pair footnote markers (document order) with note texts
queues = {'D': iter(notes['D']), 'S': iter(notes['S'])}
def sub_marker(m):
    ch = m.group(0)
    key = 'D' if ch == '‡' else 'S'
    try:
        txt = next(queues[key])
    except StopIteration:
        return (r'\textsuperscript{\ddag}' if ch == '‡' else r'\textsuperscript{\S}')
    return r'\footnote{' + latex_text(txt) + '}'
md = re.sub(r'[‡§]', sub_marker, md)

# 5. line-structured conversion
def process_block(text, out, ctx=None):
    if ctx is None:
        ctx = {}
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]

        m = re.match(r'^# (.+)$', line)
        if m:
            title = re.sub(r'^1\s+', '', m.group(1))
            out.append('\\chapter{' + latex_text(title) + '}')
            i += 1
            continue
        m = re.match(r'^## (.+)$', line)
        if m:
            title = re.sub(r'^1\.\d+\.\s*', '', m.group(1))
            out.append('\\section{' + latex_text(title) + '}')
            i += 1
            continue

        if line.startswith('|'):
            tbl = []
            while i < len(lines) and lines[i].startswith('|'):
                tbl.append(lines[i])
                i += 1
            rows = [r for r in tbl if not re.match(r'^\|[\s:|-]+\|$', r)]
            ncol = max(r.count('|') - 1 for r in rows)
            header_cells = [c.strip() for c in rows[0].strip().strip('|').split('|')]
            if any('Elements' in c for c in header_cells):
                colspec = '|c|c|c|p{0.58\\textwidth}|'
            elif any('Meaning' in c for c in header_cells) and ncol == 2:
                colspec = '|p{0.30\\textwidth}|p{0.62\\textwidth}|'
            else:
                colspec = '|' + 'l|' * ncol
            opened_minipage = ctx.get('table', False)
            if wide_table(ncol):
                out.append('\\noindent\\resizebox{\\textwidth}{!}{')
            if opened_minipage:
                out.append('\\centering')
            out.append('\\begin{tabular}{' + colspec + '}')
            out.append('\\hline')
            for r in rows:
                cells = [c.strip() for c in r.strip().strip('|').split('|')]
                cells = [latex_text(c.replace('<br>', '\\newline ')) for c in cells]
                cells += [''] * (ncol - len(cells))
                out.append(' & '.join(cells[:ncol]) + ' \\\\ \\hline')
            out.append('\\end{tabular}')
            if wide_table(ncol):
                out.append('}')
            if opened_minipage:
                out.append('\\end{minipage}')
                ctx['table'] = False
            out.append('\\medskip')
            continue

        m = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)', line)
        if m:
            path = m.group(2)
            out.append('\\begin{figure}[H]')
            out.append('\\centering')
            wide = ('fig1_4' in path) or ('fig1_7' in path) or ('fig1_8' in path)
            width = '0.98\\textwidth' if wide else '0.60\\textwidth'
            out.append('\\includegraphics[width=%s]{%s}' % (width, path))
            cap = []
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            while j < len(lines) and lines[j].strip():
                if cap or re.match(r'^FIG\.', lines[j].strip()):
                    cap.append(lines[j].strip())
                    j += 1
                else:
                    break
            if cap:
                captext = re.sub(r'^FIG\.\s*1\.\d+\.\s*', '', ' '.join(cap))
                out.append('\\caption{' + latex_text(captext) + '}')
            out.append('\\end{figure}')
            i = j
            continue

        if line.startswith('>'):
            quote = []
            while i < len(lines) and lines[i].startswith('>'):
                quote.append(re.sub(r'^> ?', '', lines[i]))
                i += 1
            inner = []
            process_block('\n'.join(quote), inner)
            out.append('\\begin{quote}' + restore('\n'.join(inner)) + '\\end{quote}')
            continue

        if line.startswith('- '):
            out.append('\\begin{itemize}')
            while i < len(lines) and lines[i].startswith('- '):
                out.append('\\item ' + latex_text(lines[i][2:].lstrip()))
                i += 1
            out.append('\\end{itemize}')
            continue

        m = re.match(r'^\*\*TABLE ([\d.]+)\*\*$', line)
        if m:
            out.append('\\begin{minipage}{\\textwidth}')
            out.append('\\centering\\textbf{TABLE ' + m.group(1) + '}')
            ctx['table'] = True
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines) and lines[i].strip() and not lines[i].startswith('|'):
                out.append(latex_text(lines[i].strip()))
                i += 1
            continue

        if line.strip() == '---':
            out.append('\\bigskip\\hrule\\bigskip')
            i += 1
            continue

        if not line.strip() or line.startswith('\x02'):
            out.append(line)
            i += 1
            continue

        para = [line]
        while (i + 1 < len(lines) and lines[i + 1].strip()
               and not re.match(r'^(#|\||!\[|>|- |---$|\*\*TABLE)', lines[i + 1])
               and not lines[i + 1].startswith('\x02')):
            i += 1
            para.append(lines[i])
        out.append(latex_text(' '.join(p.strip() for p in para)))
        i += 1

def wide_table(ncol):
    return ncol >= 7

out = []
process_block(md, out, {'table': False})
body = restore('\n'.join(out))
body = re.sub(r'\n{3,}', '\n\n', body)

preamble = (
    '% Chapter 1 of Bradley & Cracknell, The Mathematical Theory of Symmetry in Solids\n'
    '% Rebuilt from direct page-image recognition (no MinerU). See 直接识别_ch1/工作日志.md\n'
    '\\documentclass[11pt,a4paper,twoside,openright]{book}\n'
    '\\usepackage{amsmath,amssymb}\n'
    '\\usepackage[margin=2.6cm]{geometry}\n'
    '\\usepackage{graphicx}\n'
    '\\usepackage{float}\n'
    '\\usepackage{fontspec}\n'
    '\\setmainfont{TeX Gyre Pagella}\n'
    '\\clubpenalty=10000 \\widowpenalty=10000 \\predisplaypenalty=10000\n'
    '\\setcounter{secnumdepth}{1}\n'
    '\\begin{document}\n'
)

os.makedirs('ch1_build', exist_ok=True)
io.open('ch1_build/ch1.tex', 'w', encoding='utf-8', newline='\n').write(preamble + body + '\n\\end{document}\n')
print('ch1.tex written; notes:', {k: len(v) for k, v in notes.items()})
