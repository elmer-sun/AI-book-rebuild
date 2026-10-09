# -*- coding: utf-8 -*-
# 把装配后章节文件中的 %FIG{key}: caption 标记替换为 figure 环境
# 用法：python apply_figs.py [ch01.tex ...]（缺省全部 ch*.tex）
# 规则：figures/fig_{key}.pdf 存在才替换；否则保留标记并在清单中警告。
# key = 原书图号（含点，如 1.1）；图形文件名 fig_1.1.pdf。
import io, os, re, sys

BASE = r"E:\AI整理书籍\卡罗尔\重排本"
CH = os.path.join(BASE, "chapters")
FIGS = os.path.join(BASE, "figures")

# 每图宽度覆盖（默认 0.72\textwidth）；过高/过宽的图在此登记缩放
WIDTH = {}

pat = re.compile(r"^%FIG\{([^}]+)\}:\s*(.*)$", re.M)


def clean_cap(key, cap):
    # 捕获组会把标记的外层花括号带进来（%FIG{k}: {cap}），先剥掉
    if cap.startswith("{") and cap.endswith("}"):
        cap = cap[1:-1].strip()
    # 代理图注若已带"图 N.M"/"图 N.M."前缀则剥离（排版时统一加前缀，避免重复）
    cap = re.sub(rf"^图\s*{re.escape(key)}\s*[　\s]*", "", cap)
    cap = cap.lstrip("．.、 ")
    # 面板括号统一半角：（a）→(a)
    cap = re.sub(r"（([a-c])）", r"(\1)", cap)
    if not cap:
        cap = "（原书此图无图注。）"
    return cap


def process(fn):
    p = os.path.join(CH, fn)
    s = io.open(p, encoding="utf-8").read()
    missing = []

    def repl(m):
        key = m.group(1)
        cap = clean_cap(key, m.group(2).strip())
        pdf = f"fig_{key}.pdf"
        if not os.path.exists(os.path.join(FIGS, pdf)):
            missing.append(key)
            return m.group(0)
        w = WIDTH.get(key, "0.72")
        return (
            "\\begin{figure}[H]\n\\centering\n"
            f"\\includegraphics[width={w}\\textwidth]{{{pdf}}}\n"
            f"\\caption*{{图 {key}\\quad {cap}}}\n"
            "\\end{figure}"
        )

    s2 = pat.sub(repl, s)
    if s2 != s:
        io.open(p, "w", encoding="utf-8").write(s2)
    n_left = len(pat.findall(s2))
    return missing, n_left


targets = [a for a in sys.argv[1:] if a.endswith(".tex")] or \
          [f for f in os.listdir(CH) if re.match(r"ch\d+.*\.tex$", f)]
for fn in sorted(targets):
    miss, left = process(fn)
    print(f"{fn}: replaced; {left} markers left; missing figs: {sorted(set(miss)) or 'none'}")
