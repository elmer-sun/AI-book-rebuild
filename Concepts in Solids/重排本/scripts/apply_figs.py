# -*- coding: utf-8 -*-
# 把装配后章节文件中的 %FIG{key}: caption 标记替换为 figure 环境
# 用法：python apply_figs.py [ch01.tex ch02.tex ...]（缺省全部 ch0*.tex）
# 规则：figures/fig{key}.pdf 存在才替换；否则保留标记并在清单中警告。
import io, os, re, sys

BASE = r"E:\AI整理书籍\安德森\重排本"
CH = os.path.join(BASE, "chapters")
FIGS = os.path.join(BASE, "figures")

# 每图宽度覆盖（默认 0.72\textwidth）
WIDTH = {
    "1": "0.8", "5": "0.66", "6": "0.6", "7": "0.6", "10": "0.6",
    "29": "0.8", "39": "0.66", "53": "0.66", "54": "0.6",
}

pat = re.compile(r"^%FIG\{([^}]+)\}:\s*(.*)$", re.M)

def process(fn):
    p = os.path.join(CH, fn)
    s = io.open(p, encoding="utf-8").read()
    missing = []
    def repl(m):
        key, cap = m.group(1), m.group(2).strip()
        pdf = f"fig_{key}.pdf"
        if not os.path.exists(os.path.join(FIGS, pdf)):
            missing.append(key)
            return m.group(0)
        w = WIDTH.get(key, "0.72")
        return (
            "\\begin{figure}[H]\n\\centering\n"
            f"\\includegraphics[width={w}\\textwidth]{{{pdf}}}\n"
            f"\\caption*{{{cap}}}\n"
            "\\end{figure}"
        )
    s2 = pat.sub(repl, s)
    if s2 != s:
        io.open(p, "w", encoding="utf-8").write(s2)
    n_left = len(pat.findall(s2))
    return missing, n_left

targets = [a for a in sys.argv[1:] if a.endswith(".tex")] or \
          [f for f in os.listdir(CH) if re.match(r"ch0\d+\.tex$", f)]
for fn in sorted(targets):
    miss, left = process(fn)
    print(f"{fn}: replaced; {left} markers left; missing figs: {sorted(set(miss)) or 'none'}")
