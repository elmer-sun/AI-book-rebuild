# -*- coding: utf-8 -*-
"""中文引号方向修复：
行内（数学环境外）成对的引号若以 U+201D 开头（前引号误作后引号），
按奇偶切换整体翻转为 “…”。
"""
import io
import os
import re

PARTS = r"E:\AI整理书籍\齐曼\重排本\chapters\parts"
DIRECT = [r"E:\AI整理书籍\齐曼\重排本\chapters\ch00_preface.tex",
          r"E:\AI整理书籍\齐曼\重排本\chapters\ch12_bib.tex"]
OPEN, CLOSE = "\u201c", "\u201d"
QUOTE = re.compile(r'["\u201c\u201d]')


def protect_math(line):
    """把 $...$ 片段替换为占位符，返回 (新行, 恢复函数)"""
    store = []

    def stash(m):
        store.append(m.group(0))
        return "\x00M%d\x00" % (len(store) - 1)

    return re.sub(r"\$[^$]+\$", stash, line), lambda s: re.sub(
        r"\x00M(\d+)\x00", lambda m: store[int(m.group(1))], s)


def fix_line(line):
    body, restore = protect_math(line)
    quotes = [(m.start(), m.group(0)) for m in QUOTE.finditer(body)]
    if len(quotes) < 2 or len(quotes) % 2 != 0:
        return line, False
    if quotes[0][1] == OPEN:
        return line, False  # 首引号已是正确的前引号，不动
    chars = list(body)
    for i, (pos, _) in enumerate(quotes):
        chars[pos] = OPEN if i % 2 == 0 else CLOSE
    return restore("".join(chars)), True


def process(path):
    s = io.open(path, encoding="utf-8").read()
    lines = s.split("\n")
    out, nfixed, in_math_env = [], 0, False
    math_env = re.compile(r"\\(begin|end)\{(equation\*?|align\*?|gathered|"
                          r"gather\*?|aligned|array|eqnarray\*?|multline\*?)\}")
    for ln in lines:
        m = math_env.match(ln.strip())
        if m:
            in_math_env = (m.group(1) == "begin")
            out.append(ln)
            continue
        if in_math_env or ln.lstrip().startswith(("%", "\\begin{tabular}",
                                                  "\\includegraphics")):
            out.append(ln)
            continue
        new, changed = fix_line(ln)
        if changed:
            nfixed += 1
        out.append(new)
    if nfixed:
        io.open(path, "w", encoding="utf-8").write("\n".join(out))
    return nfixed


total = 0
targets = [os.path.join(PARTS, f) for f in sorted(os.listdir(PARTS))
           if f.endswith(".tex")] + DIRECT
for path in targets:
    if os.path.exists(path):
        n = process(path)
        if n:
            print("%s: %d lines fixed" % (os.path.basename(path), n))
        total += n
print("TOTAL lines fixed:", total)
