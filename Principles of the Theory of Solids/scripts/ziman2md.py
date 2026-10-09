# -*- coding: utf-8 -*-
"""齐曼《固体理论原理》重排本 → 分章 Markdown 导出。

用法：python ziman2md.py
输出：齐曼/markdown/<章文件夹>/<章文件夹>.md（插图渲染为各章 images/*.png）
"""
import io
import os
import re
import sys

sys.path.insert(0, r"E:\AI整理书籍\_md_export")
from tex2md import Converter, find_group  # noqa: E402

import pymupdf  # noqa: E402

ROOT = r"E:\AI整理书籍\齐曼\重排本"
OUT = r"E:\AI整理书籍\齐曼\markdown"
FIGS = os.path.join(ROOT, "figures")

CHAPTERS = [
    ("ch00_preface.tex", "前言", 0),
    ("ch01.tex", "第1章_周期结构", 1),
    ("ch02.tex", "第2章_格波", 2),
    ("ch03.tex", "第3章_电子态", 3),
    ("ch04.tex", "第4章_固体的静态性质", 4),
    ("ch05.tex", "第5章_电子间相互作用", 5),
    ("ch06.tex", "第6章_电子动力学", 6),
    ("ch07.tex", "第7章_输运性质", 7),
    ("ch08.tex", "第8章_光学性质", 8),
    ("ch09.tex", "第9章_费米面", 9),
    ("ch10.tex", "第10章_磁性", 10),
    ("ch11.tex", "第11章_超导电性", 11),
    ("ch12_bib.tex", "文献目录", 0),
]

CN_NUM = {1: "第一章", 2: "第二章", 3: "第三章", 4: "第四章", 5: "第五章",
          6: "第六章", 7: "第七章", 8: "第八章", 9: "第九章", 10: "第十章",
          11: "第十一章"}

EPI_RE = re.compile(r"\\epigraphbook\{")


class ZimanConverter(Converter):
    """节编号 1.1/1.2…；题词转居中段。"""

    def __init__(self, ch_n=0):
        super().__init__(book="ziman")
        self.ch_n = ch_n

    def section_title(self, title):
        self.sec_n = getattr(self, "sec_n", 0) + 1
        self.sub_n = 0
        if self.ch_n:
            return "%d.%d %s" % (self.ch_n, self.sec_n, conv_title(title, self))
        return conv_title(title, self)

    def subsection_title(self, title):
        self.sub_n = getattr(self, "sub_n", 0) + 1
        if self.ch_n:
            return "%d.%d.%d %s" % (self.ch_n, self.sec_n, self.sub_n,
                                    conv_title(title, self))
        return conv_title(title, self)


def conv_title(t, c):
    from tex2md import conv_line
    return conv_line(t, c).strip()


def preprocess_epigraphs(tex, warnings):
    r"""\epigraphbook{引文}{作者} → center 环境（转换器可处理）"""
    out = []
    pos = 0
    while True:
        m = EPI_RE.search(tex, pos)
        if not m:
            out.append(tex[pos:])
            break
        try:
            g1_start = m.end() - 1
            quote, i1 = find_group(tex, g1_start)
            j = tex.find("{", i1)
            author, i2 = find_group(tex, j)
        except ValueError:
            warnings.append("epigraph 花括号不平衡")
            out.append(tex[pos:m.end()])
            pos = m.end()
            continue
        out.append(tex[pos:m.start()])
        out.append("\\begin{center}\\itshape %s\\\\ \\textsc{%s}\\end{center}"
                   % (quote, author))
        pos = i2
    return "".join(out)


def render_fig_pngs(tex, img_dir):
    """把 tex 里引用的 figures/fig_N.pdf 渲染为 img_dir/fig_N.png"""
    os.makedirs(img_dir, exist_ok=True)
    names = set()
    for m in re.finditer(r"\\includegraphics\[[^\]]*\]\{([^}]*)\}", tex):
        base = os.path.splitext(os.path.basename(m.group(1).strip()))[0]
        pdf = os.path.join(FIGS, base + ".pdf")
        png = os.path.join(img_dir, base + ".png")
        if base not in names and os.path.exists(pdf) and not os.path.exists(png):
            doc = pymupdf.open(pdf)
            doc[0].get_pixmap(dpi=150).save(png)
            doc.close()
        names.add(base)
    return names


def main():
    os.makedirs(OUT, exist_ok=True)
    all_warn = {}
    for fn, folder, ch_n in CHAPTERS:
        src = os.path.join(ROOT, "chapters", fn)
        tex = io.open(src, encoding="utf-8").read()
        c = ZimanConverter(ch_n)
        tex = c.strip_comments(tex)
        tex = preprocess_epigraphs(tex, c.warnings)
        if ch_n:
            # \chapter{X} → \chapter*{第九章　X}（转换器对星号章只输出标题文本）
            repl = "\\chapter*{%s　" % CN_NUM[ch_n]
            tex = re.sub(r"\\chapter\{", lambda m: repl, tex, count=1)
        tex = c.prelude_footnotes(tex)
        c.walk(tex.split("\n"))
        c.flush_notes()
        md = "\n".join(c.w.lines).rstrip() + "\n"

        outdir = os.path.join(OUT, folder)
        os.makedirs(outdir, exist_ok=True)
        render_fig_pngs(tex, os.path.join(outdir, "images"))
        io.open(os.path.join(outdir, folder + ".md"), "w", encoding="utf-8").write(md)
        all_warn[folder] = c.warnings
        print("%s: %d lines, %d warnings" % (folder, md.count("\n") + 1,
                                             len(c.warnings)))
        for w in c.warnings[:10]:
            print("   !", w)
    print("DONE")


if __name__ == "__main__":
    main()
