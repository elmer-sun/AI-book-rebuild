# -*- coding: utf-8 -*-
"""卡罗尔《时空与几何》重排本 → 分章 Markdown 导出（仿 ziman2md.py）。

用法：python carroll2md.py
输出：卡罗尔/markdown/<章文件夹>/<章文件夹>.md（插图渲染为各章 images/*.png）
"""
import io
import os
import re
import sys

sys.path.insert(0, r"E:\AI整理书籍\_md_export")
from tex2md import Converter, find_group, conv_line, join_paragraph  # noqa: E402

import pymupdf  # noqa: E402

ROOT = r"E:\AI整理书籍\卡罗尔\重排本"
OUT = r"E:\AI整理书籍\卡罗尔\markdown"
FIGS = os.path.join(ROOT, "figures")

CHAPTERS = [
    ("ch00_front.tex", "前言与题词", 0),
    ("ch01.tex", "第1章_狭义相对论与平直时空", 1),
    ("ch02.tex", "第2章_流形", 2),
    ("ch03.tex", "第3章_曲率", 3),
    ("ch04.tex", "第4章_引力", 4),
    ("ch05.tex", "第5章_Schwarzschild解", 5),
    ("ch06.tex", "第6章_更一般的黑洞", 6),
    ("ch07.tex", "第7章_微扰理论与引力辐射", 7),
    ("ch08.tex", "第8章_宇宙学", 8),
    ("ch09.tex", "第9章_弯曲时空量子场论", 9),
    ("ch10_appendix.tex", "附录", 0),
    ("ch11_bib.tex", "文献目录", 0),
]

CN_NUM = {1: "第一章", 2: "第二章", 3: "第三章", 4: "第四章", 5: "第五章",
          6: "第六章", 7: "第七章", 8: "第八章", 9: "第九章"}
APP_LETTERS = "ABCDEFGHIJ"

EPI_RE = re.compile(r"\\epigraphbook\{")

_MATH_BEGIN = re.compile(
    r"\\begin\{(equation\*?|align\*?|alignat\*?|gather\*?|multline\*?|"
    r"eqnarray\*?|displaymath\*?|math)\}")
_MATH_END = re.compile(
    r"\\end\{(equation\*?|align\*?|alignat\*?|gather\*?|multline\*?|"
    r"eqnarray\*?|displaymath\*?|math)\}")


def quads_outside_math(tex):
    """把正文里的 \\quad 换成全角空格；数学环境内部保持原样。"""
    out = []
    in_math = False
    for ln in tex.split("\n"):
        if not in_math and _MATH_BEGIN.search(ln) and not _MATH_END.search(ln):
            in_math = True
        if in_math:
            out.append(ln)
            if _MATH_END.search(ln):
                in_math = False
            continue
        out.append(ln.replace("\\quad", "　"))
    return "\n".join(out)


class CarrollConverter(Converter):
    """主章节编号 N.M；前言/附录/文献目录不编号。"""

    MATH_ENV_RE = re.compile(
        r"\\begin\{(equation\*?|align\*?|alignat\*?|gather\*?|multline\*?)\}")

    def __init__(self, ch_n=0, appendix=False):
        super().__init__(book="carroll")
        self.ch_n = ch_n
        self.appendix = appendix

    def section_title(self, title):
        self.sec_n = getattr(self, "sec_n", 0) + 1
        self.sub_n = 0
        t = conv_line(title, self).strip()
        if self.ch_n:
            return "%d.%d %s" % (self.ch_n, self.sec_n, t)
        return t

    def subsection_title(self, title):
        self.sub_n = getattr(self, "sub_n", 0) + 1
        t = conv_line(title, self).strip()
        if self.ch_n and not self.appendix:
            return "%d.%d.%d %s" % (self.ch_n, self.sec_n, self.sub_n, t)
        return t

    @staticmethod
    def img_alt(cap, name):
        # key 含点号（图 1.1），不能按 '.' 切
        if cap:
            head = re.split(r"[（(　:：,，]", cap)[0].strip()
            if head:
                return head[:30]
        return name

    def take_list(self, lines, i, env, in_list_indent):
        """覆写：列表项内的显示公式块走公式管线（不被拍平成正文）。"""
        inner, i2 = self.collect_env(lines, i, env)
        has_labels = any(re.match(r"\s*\\item\s*\[", x) for x in inner)
        items = []
        text = "\n".join(inner)
        parts = re.split(r"\\item(?![a-zA-Z])", text)[1:]
        for p in parts:
            p = p.strip("\n")
            lab = None
            ml = re.match(r"\s*\[([^\]]*)\]", p)
            if ml:
                lab = ml.group(1)
                p = p[ml.end():]
            items.append((lab, p.strip()))
        base = in_list_indent or ""
        cont = base + ("   " if env != "itemize" else "  ")
        self.w.blank()
        auto_n = 0
        for lab, body in items:
            blocks = [b for b in re.split(r"\n\s*\n", body) if b.strip()]
            first = True
            if lab is None:
                auto_n += 1
            for b in blocks:
                # 把块按行切成 文本段/显示公式段 交替序列
                segs = []  # (kind, text)
                cur = []
                in_math = False
                for ln in b.split("\n"):
                    s = ln.strip()
                    if not in_math and self.MATH_ENV_RE.match(s):
                        if cur:
                            segs.append(("text", "\n".join(cur)))
                            cur = []
                        in_math = True
                        cur = [ln]
                        if _MATH_END.search(s):
                            segs.append(("math", "\n".join(cur)))
                            cur = []
                            in_math = False
                        continue
                    if in_math:
                        cur.append(ln)
                        if _MATH_END.search(s):
                            segs.append(("math", "\n".join(cur)))
                            cur = []
                            in_math = False
                        continue
                    cur.append(ln)
                if cur:
                    segs.append(("text", "\n".join(cur)))
                for kind, seg in segs:
                    if kind == "math":
                        start = len(self.w.lines)
                        self.walk(seg.split("\n"))
                        for k in range(start, len(self.w.lines)):
                            if self.w.lines[k].strip():
                                self.w.lines[k] = cont + self.w.lines[k]
                        self.w.blank()
                        first = False
                        continue
                    t = join_paragraph(seg.split("\n"))
                    t = conv_line(t, self)
                    t = re.sub(r"\s+", " ", t).strip()
                    if not t:
                        continue
                    if has_labels:
                        lbl = lab if lab else "(%d)" % auto_n
                        prefix = ("%s**%s** " % (base, lbl)) if first else cont
                    else:
                        if env == "itemize":
                            prefix = base + "- "
                        else:
                            prefix = base + "%d. " % auto_n
                    self.w.lines.append(prefix + t if first else cont + t)
                    self.w.blank()
                    first = False
        self.w.blank()
        return i2


def preprocess(tex, c):
    """Carroll 特有清理：题词/章星号化/标记清理。"""
    tex = preprocess_epigraphs(tex, c.warnings)
    # 章标题星号化（walk 对星号章只输出标题文本）
    if c.ch_n:
        head = "\\chapter*{%s　" % CN_NUM[c.ch_n]
        tex = re.sub(r"\\chapter\{", lambda m: head, tex, count=1)
    # 附录：\chapter{X} → \chapter*{附录 L　X}（按出现顺序编号）
    if c.appendix:
        k = [0]

        def apprepl(m):
            letter = APP_LETTERS[k[0]]
            k[0] += 1
            return "\\chapter*{附录 %s　" % letter
        tex = re.sub(r"\\chapter\{", apprepl, tex)
    # 杂项命令清理
    tex = re.sub(r"\\markboth\{[^}]*\}\{[^}]*\}", "", tex)
    tex = re.sub(r"\\setcounter\{[a-z]+\}\{[0-9]+\}", "", tex)
    tex = tex.replace("\\nobreak", "").replace("\\mbox{}", "")
    tex = tex.replace("\\textasciitilde{}", "~")
    # \quad → 全角空格：仅正文（跳过数学环境，数学里 KaTeX 原生支持 \quad）
    tex = quads_outside_math(tex)
    tex = tex.replace("\\clearpage", "")
    # 星号节/小节 → 非星号（walk 只识别非星号；编号语义由子类决定）
    tex = re.sub(r"\\section\*\{", lambda m: "\\section{", tex)
    tex = re.sub(r"\\subsection\*\{", lambda m: "\\subsection{", tex)
    return tex


def preprocess_epigraphs(tex, warnings):
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
        quote = quote.replace("\\\\", "\n").replace("&", "\\&")
        out.append("\\begin{center}\\itshape %s\\\\ \\textsc{%s}\\end{center}"
                   % (quote, author))
        pos = i2
    return "".join(out)


def render_fig_pngs(tex, img_dir):
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
        c = CarrollConverter(ch_n, appendix=(fn == "ch10_appendix.tex"))
        tex = c.strip_comments(tex)
        tex = preprocess(tex, c)
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
