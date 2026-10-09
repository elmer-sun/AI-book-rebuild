# -*- coding: utf-8 -*-
"""《多体量子场论》中文重排本 → 分章 Markdown 导出器。

输入：重排本/chapters/chNN.tex（装配后的成品章节，含真图 \\includegraphics）
输出：文小刚/markdown/<NN_章名>/<NN_章名>.md + images/fig_X.Y.png（fig_PDF 2x 渲染）

约定（沿用齐曼本）：
  - 公式为 $$...$$ 块（保留 \\tag）；行内 $..$ 原样
  - 图为 ![图 X.Y 图注](images/fig_X.Y.png) + 斜体图注行
  - \\footnote → [^fN] 脚注（定义紧跟所在段落之后）
  - keypoints → 无序列表；smallnote → 引用块
  - 简单 booktabs 表 → 管道表；复杂表保底为 LaTeX 原文块
  - \\pmb → \\boldsymbol（MathJax 兼容）
"""
import glob
import io
import os
import re

BASE = r"E:\AI整理书籍\文小刚"
CH = os.path.join(BASE, "重排本", "chapters")
OUT = os.path.join(BASE, "markdown")

CHAPTERS = [
    ("ch00_front.tex", "00_前言", "前言"),
    ("ch01.tex", "01_引言", "第1章 引言"),
    ("ch02.tex", "02_量子力学的路径积分表述", "第2章 量子力学的路径积分表述"),
    ("ch03.tex", "03_相互作用玻色子系统", "第3章 相互作用玻色子系统"),
    ("ch04.tex", "04_自由费米子系统", "第4章 自由费米子系统"),
    ("ch05.tex", "05_相互作用费米子系统", "第5章 相互作用费米子系统"),
    ("ch06.tex", "06_量子规范理论", "第6章 量子规范理论"),
    ("ch07.tex", "07_量子霍尔态理论", "第7章 量子霍尔态理论"),
    ("ch08.tex", "08_拓扑序与量子序", "第8章 拓扑序与量子序——超越朗道理论"),
    ("ch09.tex", "09_自旋液体与量子序的平均场理论", "第9章 自旋液体与量子序的平均场理论"),
    ("ch10.tex", "10_弦凝聚", "第10章 弦凝聚——光与费米子的统一"),
    ("ch11_bib.tex", "11_文献目录", "文献目录"),
]

MATH_ENVS = ("equation*", "align*", "gather*", "aligned", "array", "cases")


def render_fig_pngs(figpdf, imgdir, key):
    """把 figures/fig_key.pdf 渲染为 images/fig_key.png（2x）。"""
    import fitz
    png = os.path.join(imgdir, f"fig_{key}.png")
    if not os.path.exists(png):
        doc = fitz.open(figpdf)
        pix = doc[0].get_pixmap(matrix=fitz.Matrix(2.2, 2.2), alpha=False)
        pix.save(png)
    return png


def inline_conv(s):
    """行内转换（不在数学环境内的文本段）。"""
    s = re.sub(r"\\emph\{([^{}]*)\}", r"*\1*", s)
    s = re.sub(r"\\textbf\{([^{}]*)\}", r"**\1**", s)
    s = re.sub(r"\\textit\{([^{}]*)\}", r"*\1*", s)
    s = re.sub(r"\\text\{([^{}]*)\}", r"\1", s)
    s = s.replace("\\%", "%").replace("\\&", "&").replace("\\#", "#")
    s = s.replace("\\_", "_").replace("\\quad", "　").replace("\\,", " ")
    s = s.replace("``", '"').replace("''", '"')
    return s


def math_conv(block):
    """数学块：MathJax 兼容化。"""
    b = block.replace("\\pmb", "\\boldsymbol")
    return b


def split_math_parity(lines, i):
    """从 lines[i] 开始收集一个 \\begin{env}...\\end{env} 块（处理嵌套同名环境）。
    返回 (块行列表, 下一索引, env)。"""
    m = re.match(r"\\begin\{([a-zA-Z*]+)\}", lines[i].strip())
    env = m.group(1)
    depth = 1
    j = i + 1
    body = []
    while j < len(lines):
        ln = lines[j]
        if re.match(r"\\begin\{" + re.escape(env) + r"\}", ln.strip()):
            depth += 1
        elif re.match(r"\\end\{" + re.escape(env) + r"\}", ln.strip()):
            depth -= 1
            if depth == 0:
                return body, j + 1, env
        body.append(ln)
        j += 1
    return body, j, env


def normalize(lines):
    """预处理：把挤在同一行里的 \\begin/\\end/\\item 拆成独立行，
    避免单行环境（如 \\begin{keypoints}\\item…）让逐行扫描器吞掉后续内容。"""
    BS = chr(92)
    out = []
    for ln in lines:
        ln = re.sub(r"\\begin\{([a-zA-Z*]+)\}",
                    lambda m: "\n" + BS + "begin{" + m.group(1) + "}", ln)
        ln = re.sub(r"\\end\{([a-zA-Z*]+)\}",
                    lambda m: "\n" + BS + "end{" + m.group(1) + "}", ln)
        ln = re.sub(r"\\item", lambda m: "\n" + BS + "item", ln)
        out.extend(ln.split("\n"))
    return out


def convert_chapter(src, outdir, title):
    os.makedirs(os.path.join(outdir, "images"), exist_ok=True)
    imgdir = os.path.join(outdir, "images")
    lines = normalize(io.open(src, encoding="utf-8").read().split("\n"))
    out = []
    fn_counter = [0]
    footnote_defs = []

    def flush_footnotes():
        """把暂存脚注定义写到刚结束的段落后。"""
        while footnote_defs:
            out.append(footnote_defs.pop(0))
        if out and out[-1] != "":
            pass

    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        s = raw.strip()

        # 注释行
        if s.startswith("%") and not s.startswith("%FIG"):
            i += 1
            continue

        # 数学环境 → $$
        menv = re.match(r"\\begin\{([a-zA-Z*]+)\}", s)
        math_names = ("equation", "align", "gather", "cases", "array",
                      "aligned", "Bmatrix", "pmatrix", "matrix")
        if menv and any(menv.group(1).startswith(e) for e in math_names):
            body, i2, env = split_math_parity(lines, i)
            inner = "\n".join(math_conv(b for b in body) if False else
                              [math_conv(b) for b in body])
            out.append("$$")
            out.append(inner)
            out.append("$$")
            out.append("")
            i = i2
            continue

        # figure 环境
        if s.startswith("\\begin{figure}"):
            body, i2, _ = split_math_parity(lines, i)
            blk = "\n".join(body)
            mk = re.search(r"\\includegraphics\[[^]]*\]\{(fig_[^}]+\.pdf)\}", blk)
            mc = re.search(r"\\caption\*\{(.*?)\}\s*(?:\\label\{[^}]*\})?\s*$",
                           blk, re.S)
            if mk:
                key = mk.group(1)[:-4]
                if key.startswith("fig_"):
                    key = key[4:]
                cap = mc.group(1) if mc else ""
                cap = re.sub(r"\\quad", "　", cap)
                cap = inline_conv(cap).replace("\n", " ").strip()
                cap = re.sub(rf"^图\s*{re.escape(key)}\s*[　\s]*", "", cap)
                cap = cap.lstrip("．.、 ")
                try:
                    render_fig_pngs(os.path.join(BASE, "重排本", "figures",
                                                 f"fig_{key}.pdf"),
                                    imgdir, key)
                    out.append(f"![图 {key} {cap}](images/fig_{key}.png)")
                    out.append("")
                    out.append(f"*图 {key}　{cap}*")
                    out.append("")
                except Exception as e:
                    out.append(f"(图 {key} 渲染失败：{e})")
            i = i2
            continue

        # 章节标题
        m = re.match(r"\\chapter\*?\{(.+)\}", s)
        if m:
            out.append("# " + inline_conv(m.group(1)))
            out.append("")
            i += 1
            continue
        m = re.match(r"\\section\*?\{(.+)\}", s)
        if m:
            flush_footnotes()
            out.append("## " + inline_conv(m.group(1)))
            out.append("")
            i += 1
            continue
        m = re.match(r"\\subsection\*?\{(.+)\}", s)
        if m:
            flush_footnotes()
            out.append("### " + inline_conv(m.group(1)))
            out.append("")
            i += 1
            continue
        m = re.match(r"\\subsubsection\*?\{(.+)\}", s)
        if m:
            flush_footnotes()
            out.append("#### " + inline_conv(m.group(1)))
            out.append("")
            i += 1
            continue

        # （习题解答册）problem 环境 → 引用块题目重述
        if s.startswith("\\begin{problem}"):
            i += 1
            out.append("**题目.**")
            out.append("")
            while i < n and not lines[i].strip().startswith("\\end{problem}"):
                out.append("> " + inline_conv(lines[i].strip()))
                i += 1
            i += 1
            out.append("")
            continue

        # （习题解答册）\solution → 解答引导
        if s.startswith("\\solution"):
            out.append("**解答.**")
            i += 1
            continue

        # keypoints → 列表
        if s.startswith("\\begin{keypoints}"):
            i += 1
            while i < n and not lines[i].strip().startswith("\\end{keypoints}"):
                t = lines[i].strip()
                if t.startswith("\\item"):
                    out.append("- " + inline_conv(t[5:].strip()))
                i += 1
            i += 1
            out.append("")
            continue

        # smallnote → 引用块
        if s.startswith("\\begin{smallnote}"):
            i += 1
            out.append("")
            while i < n and not lines[i].strip().startswith("\\end{smallnote}"):
                out.append("> " + inline_conv(lines[i].strip()))
                i += 1
            i += 1
            out.append("")
            continue

        # 表格：简单 tabular → 管道表，失败则原样 LaTeX 块
        if s.startswith("\\begin{tabular}"):
            body, i2, _ = split_math_parity(lines, i)
            blk = "\n".join(body)
            rows = [r.strip() for r in blk.split("\\\\") if r.strip()]
            pipe = []
            ok = True
            for ri, r in enumerate(rows):
                r = re.sub(r"\\(toprule|midrule|bottomrule|hline)", "", r).strip()
                if not r:
                    continue
                cells = [inline_conv(c.strip()) for c in r.split("&")]
                if any("$" not in c and ("\\" in c) and len(c) > 40 for c in cells):
                    ok = False
                    break
                pipe.append("| " + " | ".join(cells) + " |")
                if ri == 0 and len(rows) > 1:
                    pipe.append("|" + "---|" * len(cells))
            if ok and len(pipe) > 2:
                out.extend(pipe)
                out.append("")
            else:
                out.append("```latex")
                out.extend(body)
                out.append("```")
                out.append("")
            i = i2
            continue

        # 脚注
        if "\\footnote" in s:
            def _fn(mo):
                fn_counter[0] += 1
                k = fn_counter[0]
                footnote_defs.append(f"[^{k}]: {inline_conv(mo.group(1))}")
                return f"[^{k}]"
            # 简单情形：单层花括号（本书脚注内偶有 \\begin{...}，若有则退化为原样）
            if s.count("{") == s.count("}"):
                s2 = re.sub(r"\\footnote\{([^{}]*)\}", _fn, s)
                while s2 != s and "\\footnote" in s2 and s2.count("{") == s2.count("}"):
                    s3 = re.sub(r"\\footnote\{([^{}]*)\}", _fn, s2)
                    if s3 == s2:
                        break
                    s2 = s3
                s = s2

        # 杂命令清理
        for pat in (r"\\markboth\{[^}]*\}\{[^}]*\}", r"\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}",
                    r"\\thispagestyle\{[^}]*\}", r"\\mbox\{\}", r"\\clearpage",
                    r"\\needspace\{[^}]*\}", r"\\vspace\{[^}]*\}", r"\\noindent",
                    r"\\captionsetup[^ ]*", r"\\setcounter\{[^}]*\}\{[^}]*\}"):
            s = re.sub(pat, "", s)
        m = re.match(r"\\epigraphbook\{(.*)\}\{(.*)\}$", s)
        if m:
            out.append("*" + inline_conv(m.group(1)) + "*")
            out.append("")
            out.append("—— " + inline_conv(m.group(2)))
            out.append("")
            i += 1
            continue

        # 普通行
        if s.startswith("\\item"):
            out.append("- " + inline_conv(s[5:].strip()))
        elif s in ("", "\\par"):
            flush_footnotes()
            out.append("")
        else:
            t = inline_conv(s)
            t = re.sub(r"\\begin\{flushleft\}|\\end\{flushleft\}", "", t)
            t = t.replace("\\hfill", "　　")
            out.append(t)
        i += 1

    flush_footnotes()
    # 压缩 3+ 连续空行
    txt = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    mdpath = os.path.join(outdir, os.path.basename(outdir) + ".md")
    io.open(mdpath, "w", encoding="utf-8").write(txt)
    return mdpath


def main():
    readme = ["# 《多体量子场论》中文重排本 · Markdown 版", "",
              "逐章导出自 LaTeX 成品；公式为 $$…$$ LaTeX（保留 \\tag，MathJax 可渲染）；",
              "图为 2x 渲染 PNG。PDF 成品见上级目录。", ""]
    for src, d, title in CHAPTERS:
        p = os.path.join(CH, src)
        if not os.path.exists(p):
            print("缺", src)
            continue
        outdir = os.path.join(OUT, d)
        md = convert_chapter(p, outdir, title)
        n_img = len(glob.glob(os.path.join(outdir, "images", "*.png")))
        readme.append(f"- [{title}]({d}/{os.path.basename(md)})（图 {n_img} 幅）")
        print(f"{d}: {os.path.getsize(md)//1024}KB, {n_img} 图")
    io.open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write(
        "\n".join(readme) + "\n")
    print("README written")


if __name__ == "__main__":
    main()
