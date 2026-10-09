# -*- coding: utf-8 -*-
"""Blundell《凝聚态中的磁学》中译重排本：LaTeX → Markdown 导出。
惯例沿用 文小刚/markdown：逐章文件夹、$$…$$ 保留 \\tag、脚注 [^n]、图为 2x PNG。
"""
import json
import os
import re

BOOK = r'E:\AI整理书籍\磁学\book'
SRC = r'E:\AI整理书籍\磁学'
OUT = os.path.join(SRC, 'markdown')

# ---------- 单元定义 ----------
UNITS = [
    # (tex 文件, 输出目录名, H1 标题, 图号前缀, 表号前缀)
    ('__front__', '00_译者说明', '译者说明', None, None),
    ('ch1.tex', '01_引言', '第 1 章　引言', '1', '1'),
    ('ch2.tex', '02_孤立磁矩', '第 2 章　孤立磁矩', '2', '2'),
    ('ch3.tex', '03_环境', '第 3 章　环境', '3', '3'),
    ('ch4.tex', '04_相互作用', '第 4 章　相互作用', '4', '4'),
    ('ch5.tex', '05_磁有序与磁结构', '第 5 章　磁有序与磁结构', '5', '5'),
    ('ch6.tex', '06_有序与对称性破缺', '第 6 章　有序与对称性破缺', '6', '6'),
    ('ch7.tex', '07_金属中的磁性', '第 7 章　金属中的磁性', '7', '7'),
    ('ch8.tex', '08_竞争相互作用与低维性', '第 8 章　竞争相互作用与低维性', '8', '8'),
    ('appA.tex', '09_附录A_电磁学中的单位', '附录 A　电磁学中的单位', 'A', 'A'),
    ('appB.tex', '10_附录B_电磁学', '附录 B　电磁学', 'B', 'B'),
    ('appC.tex', '11_附录C_量子物理与原子物理', '附录 C　量子物理与原子物理', 'C', 'C'),
    ('appD.tex', '12_附录D_磁学中的能量与退磁场', '附录 D　磁学中的能量与退磁场', 'D', 'D'),
    ('appE.tex', '13_附录E_统计力学', '附录 E　统计力学', 'E', 'E'),
    ('answers.tex', '14_附录F_部分习题答案与提示', '附录 F　部分习题答案与提示', 'F', 'F'),
    ('symbols.tex', '15_附录G_符号常数与有用公式', '附录 G　符号、常数与有用公式', 'G', 'G'),
]

# ---------- 图号提取（与 assign_fig_numbers 相同逻辑） ----------

def fig_numbers(texfile):
    src = open(os.path.join(BOOK, texfile), encoding='utf-8').read()
    lines = src.split('\n')
    setc = {}
    for i, ln in enumerate(lines):
        m = re.search(r'\\setcounter\{figure\}\{(\d+)\}', ln)
        if m:
            setc[i] = int(m.group(1))
    nums = []
    cur = 0
    last = -1
    for i, ln in enumerate(lines):
        if '\\begin{figure}' in ln:
            for k in sorted(setc):
                if last < k <= i:
                    cur = setc[k]
                    last = k
            cur += 1
            nums.append(cur)
    return nums

# ---------- 行内清理 ----------

def split_math(line):
    """按 $...$ 切分（跳过 \\$）；返回 [(is_math, text)]"""
    parts = []
    i = 0
    n = len(line)
    buf = ''
    while i < n:
        if line[i] == '\\' and i + 1 < n and line[i + 1] == '$':
            buf += '$'
            i += 2
            continue
        if line[i] == '$':
            parts.append((False, buf))
            buf = '$'
            i += 1
            # 找配对 $
            while i < n:
                if line[i] == '\\' and i + 1 < n and line[i + 1] == '$':
                    buf += '$'
                    i += 2
                    continue
                buf += line[i]
                if line[i] == '$':
                    i += 1
                    break
                i += 1
            parts.append((True, buf))
            buf = ''
            continue
        buf += line[i]
        i += 1
    parts.append((False, buf))
    return parts


def clean_inline(text):
    out = []
    for is_math, seg in split_math(text):
        if is_math:
            out.append(seg)
            continue
        s = seg
        s = re.sub(r'\\emph\{([^{}]*)\}', r'*\1*', s)
        s = re.sub(r'\\textit\{([^{}]*)\}', r'*\1*', s)
        s = re.sub(r'\\textbf\{([^{}]*)\}', r'**\1**', s)
        s = re.sub(r'\\texttt\{([^{}]*)\}', r'`\1`', s)
        s = re.sub(r'\\textsuperscript\{([^{}]*)\}', r'\1', s)
        s = re.sub(r'\\textsc\{([^{}]*)\}', r'\1', s)
        s = re.sub(r'\\underline\{([^{}]*)\}', r'\1', s)
        s = s.replace('\\AA', 'Å')
        s = s.replace('\\S', '§')
        s = s.replace('\\%', '%').replace('\\&', '&')
        s = s.replace('\\_', '_').replace('\\#', '#')
        s = s.replace('\\ldots', '…').replace('\\dots', '…')
        s = s.replace('---', '—').replace('--', '–')
        s = s.replace('~', ' ')
        s = re.sub(r'\\,|\\;|\\!|\\ ', ' ', s)
        s = re.sub(r'\\vspace\{[^}]*\}', '', s)
        s = re.sub(r'\\hspace\{[^}]*\}', '', s)
        s = re.sub(r'\\(kaishu|heiti|songti|fangsong|noindent|centering|small|footnotesize|scriptsize|large|Large|normalsize|raggedright|par)\b', '', s)
        s = re.sub(r'\\zihao\{[^}]*\}', '', s)
        s = re.sub(r'\\mbox\{([^{}]*)\}', r'\1', s)
        s = re.sub(r'\\texorpdfstring\{([^{}]*)\}\{[^{}]*\}', r'\1', s)
        s = re.sub(r'\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}', '', s)
        s = re.sub(r'\\label\{[^}]*\}', '', s)
        s = re.sub(r'\\(thispagestyle|pagestyle|setcounter)\{[^}]*\}\{[^}]*\}', '', s)
        s = s.replace('\\begin{equation*}', '$$').replace('\\end{equation*}', '$$')
        s = s.replace('\\begin{align*}', '$$').replace('\\end{align*}', '$$')
        s = re.sub(r'\\quad|\\qquad', ' ', s)
        out.append(s)
    return ''.join(out)


def extract_group(text, keyword):
    """提取 \keyword{...}（配平花括号），返回 (内容, 去掉该段的文本)"""
    idx = text.find(keyword)
    if idx < 0:
        return None, text
    i = idx + len(keyword)
    depth = 1
    j = i
    while j < len(text) and depth > 0:
        if text[j] == '{':
            depth += 1
        elif text[j] == '}':
            depth -= 1
        j += 1
    return text[i:j - 1], text[:idx] + text[j:]


JOIN_KEYWORDS = ['\\mnote{', '\\bio{', '\\fn{', '\\footnote{']


def join_args(lines):
    """把跨行的 \\mnote/\\bio/\\fn/\\footnote 参数拼到一行（括号配平为止）。"""
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        guard = 0
        while guard < 50:
            need = False
            for kw in JOIN_KEYWORDS:
                start = 0
                while True:
                    idx = ln.find(kw, start)
                    if idx < 0:
                        break
                    depth = 1
                    j = idx + len(kw)
                    while j < len(ln) and depth > 0:
                        if ln[j] == '{':
                            depth += 1
                        elif ln[j] == '}':
                            depth -= 1
                        j += 1
                    if depth > 0:
                        need = True
                        break
                    start = j
            if not need or i + 1 >= len(lines):
                break
            guard += 1
            i += 1
            ln = ln + ' ' + lines[i].strip()
        out.append(ln)
        i += 1
    return out

# ---------- 表格转换 ----------

def tabular_to_md(rows_src):
    """rows_src: tabular 环境体内文本 → markdown 管道表"""
    body = rows_src
    body = re.sub(r'\\(toprule|midrule|bottomrule|hline|cline\{[^}]*\})', '', body)
    raw_rows = [r.strip() for r in body.split('\\\\')]
    rows = []
    for r in raw_rows:
        r = re.sub(r'^\[[^\]]*\]', '', r.strip())   # 行首残留的 \\[6pt]
        if not r:
            continue
        cells = split_cells(r)
        rows.append(cells)
    if not rows:
        return ''
    ncol = max(len(r) for r in rows)
    for r in rows:
        while len(r) < ncol:
            r.append('')
    out = ['| ' + ' | '.join(c.replace('|', '\\|') for c in rows[0]) + ' |',
           '|' + '---|' * ncol]
    for r in rows[1:]:
        out.append('| ' + ' | '.join(c.replace('|', '\\|') for c in r) + ' |')
    return '\n'.join(out)


def split_cells(row):
    """按 & 切分（忽略数学内 & —— 本书的 align 不进 tabular，简单切分即可），
    处理 \\multicolumn{n}{c}{x} → x"""
    cells = []
    for c in row.split('&'):
        c = c.strip()
        m = re.match(r'\\multicolumn\{\d+\}\{[^}]*\}\{(.*)\}$', c, re.S)
        if m:
            c = m.group(1)
        cells.append(clean_inline(c))
    return cells

# ---------- 主转换 ----------

def convert_unit(texfile, outdir, h1, fig_prefix, tab_prefix):
    os.makedirs(outdir, exist_ok=True)
    imgdir = os.path.join(outdir, 'images')
    os.makedirs(imgdir, exist_ok=True)

    if texfile == '__front__':
        src = open(os.path.join(BOOK, 'main.tex'), encoding='utf-8').read()
        m = re.search(r'\\chapter\*\{译者说明\}(.*?)\\input\{preface\}', src, re.S)
        lines = m.group(1).split('\n')
        preface = open(os.path.join(BOOK, 'preface.tex'), encoding='utf-8').read()
        plines = [l for l in preface.split('\n')
                  if not re.match(r'\s*\\(chapter\*|addcontentsline)', l)]
        lines = lines + ['', '# 前言', ''] + plines
        fig_nums, tab_counter = None, [0]
        fig_prefix_eff = None
    else:
        lines = open(os.path.join(BOOK, texfile), encoding='utf-8').read().split('\n')
        preface_lines = None
        fig_nums = fig_numbers(texfile)
        tab_counter = [0]
        fig_prefix_eff = fig_prefix
    lines = join_args(lines)

    out = ['# ' + h1, '']
    fig_idx = [0]
    tab_idx = [0]
    fn_counter = [0]
    pending_fn = []          # (id, text) 待附到段后
    i = 0
    n = len(lines)
    # 章文件以 \chapter 开头，跳过重复标题
    while i < n and (lines[i].startswith('%') or not lines[i].strip()
                     or re.match(r'\\chapter\*?\{', lines[i].strip())):
        m = re.match(r'\\chapter\*?\{(.*)\}\s*$', lines[i].strip())
        if m and texfile != '__front__':
            pass  # 用传入的 h1，跳过
        i += 1

    def flush_para(buf):
        """输出一个段落块并附脚注定义"""
        if buf:
            out.append(''.join(buf).strip())
            out.append('')
        while pending_fn:
            fid, ftext = pending_fn.pop(0)
            out.append(f'[^{fid}]: {ftext}')
            out.append('')

    para_buf = []

    def repl_fn(mo, gidx=2):
        fn_counter[0] += 1
        fid = f'fn{fn_counter[0]}'
        txt = clean_inline(re.sub(r'\s+', ' ', mo.group(gidx)))
        pending_fn.append((fid, txt))
        return f'[^{fid}]'

    def close_para():
        nonlocal para_buf
        flush_para(para_buf)
        para_buf = []

    while i < n:
        raw = lines[i]
        line = raw.strip()

        # ----- 环境起点 -----
        if line.startswith('\\begin{figure}'):
            close_para()
            block = []
            depth = 1
            i += 1
            while i < n and depth > 0:
                depth += lines[i].count('\\begin{figure}') - lines[i].count('\\end{figure}')
                if depth > 0:
                    block.append(lines[i])
                i += 1
            blk = '\n'.join(block)
            imgs = re.findall(r'includegraphics\[[^]]*\]\{([^}]+)\}', blk)
            cap, _ = extract_group(blk, '\\caption{')
            cap = clean_inline(re.sub(r'\s+', ' ', cap or '')).strip()
            for img in imgs:
                name = os.path.splitext(os.path.basename(img))[0]
                pdf = os.path.join(BOOK, 'figs', name + '.pdf')
                png = os.path.join(imgdir, name + '.png')
                if not os.path.exists(png):
                    import pymupdf
                    d = pymupdf.open(pdf)
                    pix = d[0].get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False)
                    pix.save(png)
                    d.close()
                rel = 'images/' + name + '.png'
                if fig_prefix_eff and fig_idx[0] < len(fig_nums):
                    fno = fig_nums[fig_idx[0]]
                else:
                    fno = fig_idx[0] + 1
                fig_idx[0] += 1
                out.append(f'![]({rel})')
                out.append('')
                if fig_prefix_eff:
                    out.append(f'*图 {fig_prefix_eff}.{fno}：{cap}*')
                else:
                    out.append(f'*{cap}*')
                out.append('')
                cap = ''  # 多图共用图注只放一次
            continue

        if line.startswith('\\begin{table}') or line.startswith('\\begin{table}['):
            close_para()
            block = []
            depth = 1
            i += 1
            while i < n and depth > 0:
                depth += lines[i].count('\\begin{table}') - lines[i].count('\\end{table}')
                if depth > 0:
                    block.append(lines[i])
                i += 1
            blk = '\n'.join(block)
            cap, _ = extract_group(blk, '\\caption{')
            cap = clean_inline(re.sub(r'\s+', ' ', cap or '')).strip()
            mt = re.search(r'\\begin\{tabular\}\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}(.*?)\\end\{tabular\}', blk, re.S)
            tbl = tabular_to_md(mt.group(2)) if mt else ''
            if tab_prefix:
                tab_idx[0] += 1
                out.append(f'**表 {tab_prefix}.{tab_idx[0]}　{cap}**')
            elif cap:
                out.append(f'**{cap}**')
            out.append('')
            out.append(tbl)
            out.append('')
            continue

        m_env = re.match(r'\\begin\{(equation|align)(\*)?\}', line)
        if m_env:
            env = m_env.group(1) + (m_env.group(2) or '')
            star = m_env.group(2) or ''
            close_para()
            body = [re.sub(r'\\begin\{(equation|align)(\*)?\}(\[[^\]]*\])?', '', line)]
            i += 1
            while i < n and f'\\end{{{env}}}' not in lines[i]:
                body.append(lines[i])
                i += 1
            last = re.sub(r'\\end\{' + re.escape(env) + r'\}', '', lines[i])
            body.append(last)
            i += 1
            content = '\n'.join(b for b in body).strip()
            if env.startswith('align'):
                content = '\\begin{aligned}\n' + content + '\n\\end{aligned}'
            out.append('$$')
            out.append(content)
            out.append('$$')
            out.append('')
            continue

        if line.startswith('\\begin{example}'):
            close_para()
            arg = re.match(r'\\begin\{example\}\{(.*)\}', line)
            out.append('---')
            out.append('')
            out.append(f'**例 {arg.group(1)}**　' if arg else '**例**　')
            i += 1
            continue
        if line == '\\end{example}':
            # 去掉与正文间多余空行风险，直接收尾
            close_para()
            out.append('---')
            out.append('')
            i += 1
            continue

        if line.startswith('\\begin{itemize}') or line.startswith('\\begin{enumerate}'):
            close_para()
            kind = 'itemize' if 'itemize' in line else 'enumerate'
            i += 1
            k = 1
            while i < n and f'\\end{{{kind}}}' not in lines[i]:
                t = lines[i].strip()
                if t.startswith('\\item'):
                    item = t[len('\\item'):].strip()
                    mark = f'{k}. ' if kind == 'enumerate' else '- '
                    out.append(mark + clean_inline(item))
                    if kind == 'enumerate':
                        k += 1
                elif t:
                    out.append('  ' + clean_inline(t))
                i += 1
            i += 1
            out.append('')
            continue

        if line.startswith('\\begin{quote}'):
            close_para()
            i += 1
            while i < n and '\\end{quote}' not in lines[i]:
                t = lines[i].strip()
                if t and not t.startswith('\\end'):
                    out.append('> ' + clean_inline(t))
                i += 1
            i += 1
            out.append('')
            continue

        if line.startswith('\\begin{center}'):
            close_para()
            block = []
            i += 1
            while i < n and '\\end{center}' not in lines[i]:
                block.append(lines[i])
                i += 1
            i += 1
            blk = '\n'.join(block)
            mt = re.search(r'\\begin\{tabular\}\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}(.*?)\\end\{tabular\}', blk, re.S)
            if mt:
                out.append(tabular_to_md(mt.group(2)))
                out.append('')
            else:
                for bl in block:
                    if bl.strip():
                        out.append(clean_inline(bl.strip()))
                out.append('')
            continue

        # ----- 标题 -----
        m = re.match(r'\\section\*?\{(.*)\}\s*$', line)
        if m:
            close_para()
            out.append('## ' + clean_inline(m.group(1)))
            out.append('')
            i += 1
            continue
        m = re.match(r'\\subsection\*?\{(.*)\}\s*$', line)
        if m:
            close_para()
            out.append('### ' + clean_inline(m.group(1)))
            out.append('')
            i += 1
            continue
        m = re.match(r'\\subsubsection\*?\{(.*)\}\s*$', line)
        if m:
            close_para()
            out.append('#### ' + clean_inline(m.group(1)))
            out.append('')
            i += 1
            continue

        # ----- 边注/小传（bio 先于 mnote，二者可能同现一行） -----
        if '\\bio{' in line or '\\mnote{' in line:
            while '\\bio{' in line:
                txt, line = extract_group(line, '\\bio{')
                close_para()
                txt = txt.replace('\\', ' ').strip()
                out.append('> 〔人物〕' + clean_inline(txt))
                out.append('')
            while '\\mnote{' in line:
                txt, line = extract_group(line, '\\mnote{')
                close_para()
                out.append('> 〔边注〕' + clean_inline(txt))
                out.append('')
            if line.strip():
                para_buf.append(clean_inline(line.strip()) + ' ')
            i += 1
            continue

        # ----- 习题条目 -----
        m = re.match(r'\\exer\{([^}]*)\}\s*(.*)$', line)
        if m:
            close_para()
            para_buf.append(f'**（{m.group(1)}）**　')
            if m.group(2).strip():
                seg = m.group(2)
                seg = re.sub(r'\\fn\{(\d+)\}\{((?:[^{}]|\{[^{}]*\})*)\}', repl_fn, seg)
                seg = re.sub(r'\\footnote\{((?:[^{}]|\{[^{}]*\})*)\}',
                             lambda mo: repl_fn(mo, 1), seg)
                para_buf.append(clean_inline(seg) + ' ')
            i += 1
            continue

        # ----- 空行 -----
        if not line:
            close_para()
            i += 1
            continue

        # ----- 注释行 -----
        if line.startswith('%'):
            i += 1
            continue

        # ----- 普通文本行 -----
        seg = line
        seg = re.sub(r'\\fn\{(\d+)\}\{((?:[^{}]|\{[^{}]*\})*)\}', repl_fn, seg)
        seg = re.sub(r'\\footnote\{((?:[^{}]|\{[^{}]*\})*)\}',
                     lambda mo: repl_fn(mo, 1), seg)
        # 段内裸 \\ 换行
        seg = re.sub(r'\\\\(\[[0-9.]+a-z]{0,8})?$', '', seg)
        para_buf.append(clean_inline(seg) + ' ')
        i += 1

    close_para()

    # 收尾：落盘
    text = '\n'.join(out)
    text = re.sub(r'\n{3,}', '\n\n', text)
    md = os.path.join(outdir, os.path.basename(outdir) + '.md')
    open(md, 'w', encoding='utf-8').write(text)
    return md, fig_idx[0]


def main():
    index = []
    for texfile, outdir_name, h1, fp, tp in UNITS:
        outdir = os.path.join(OUT, outdir_name)
        md, nfigs = convert_unit(texfile, outdir, h1, fp, tp)
        index.append((outdir_name, h1, nfigs))
        print('OK', outdir_name, f'({nfigs} 图)')
    # README
    lines = ['# 《凝聚态中的磁学》中文重排本 · Markdown 版', '',
             '逐章导出自 LaTeX 成品；公式为 $$…$$ LaTeX（保留 \\tag，MathJax 可渲染）；'
             '图为 2x 渲染 PNG。PDF 成品见上级目录。', '']
    for d, h1, nfigs in index:
        lines.append(f'- [{h1}]({d}/{d}.md)（图 {nfigs} 幅）')
    open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('README done')


if __name__ == '__main__':
    main()
