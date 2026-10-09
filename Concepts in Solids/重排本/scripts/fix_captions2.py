# -*- coding: utf-8 -*-
# \caption*{} 裸数学修复 v2：按 $ 分段，仅替换文本段，迭代到稳定
import io, re

BS = chr(92)
CAP = BS + "caption*{"
FILES = [
    r"E:\AI整理书籍\安德森\重排本\chapters\ch02.tex",
    r"E:\AI整理书籍\安德森\重排本\chapters\ch03.tex",
]

SUBS = [
    ("U 的间隔", "$U$ 的间隔"),
    ("间隔 $U$", "间隔 $U$"),
    ("V_K", "$V_K$"),
    ("E_0", "$E_0$"),
    ("E_k(p)−E_k(s)", "$E_k(p)-E_k(s)$"),
    ("E_k(p)", "$E_k(p)$"),
    ("E_k(s)", "$E_k(s)$"),
    ("U+E(k)", "$U+E(k)$"),
    ("E(k)", "$E(k)$"),
    ("n_j = 1", "$n_j = 1$"),
    ("n_j", "$n_j$"),
    ("k∥", "$k_\\parallel$"),
    ("k⊥", "$k_\\perp$"),
    ("2k_F", "$2k_F$"),
    ("k_F", "$k_F$"),
    ("k−K", "$k-K$"),
    ("k+K", "$k+K$"),
    ("k-K", "$k-K$"),
    ("ω_r", "$\\omega_r$"),
    ("E_F", "$E_F$"),
    ("ΔK", "$\\Delta K$"),
    ("V_K", "$V_K$"),
    ("δ-function", "$\\delta$-function"),
    ("b_jk", "$b_{jk}$"),
    ("b_kj", "$b_{kj}$"),
    ("S_j", "$S_j$"),
    ("S_l", "$S_l$"),
    ("E_n", "$E_n$"),
    ("ħω", "$\\hbar\\omega$"),
    ("ħ/τ", "$\\hbar/\\tau$"),
    ("k_BT", "$k_{\\mathrm{B}}T$"),
    ("E_p(atomic)", "$E_p$(atomic)"),
    ("E_S", "$E_S$"),
    ("σ_j", "$\\sigma_j$"),
    ("b_j 只有两个能级", "$b_j$ 只有两个能级"),
    ("的 b_j 具有", "的 $b_j$ 具有"),
]

def fix_seg(seg):
    for a, b in SUBS:
        if a in seg:
            seg = seg.replace(a, b)
    return seg

def mathify(cap):
    parts = cap.split("$")
    for i in range(0, len(parts), 2):
        parts[i] = fix_seg(parts[i])
    return "$".join(parts)

pat = re.compile(re.escape(CAP) + r"([^}]*)\}")
for fn in FILES:
    s = io.open(fn, encoding="utf-8").read()
    def repl(m):
        return CAP + mathify(m.group(1)) + "}"
    s2 = pat.sub(repl, s)
    io.open(fn, "w", encoding="utf-8").write(s2)
    # 报告仍可能裸露的记号（文本段内的 _ ^）
    bad = []
    for m in pat.finditer(s2):
        segs = m.group(1).split("$")
        for i in range(0, len(segs), 2):
            if re.search(r"[_^]", segs[i]):
                bad.append(segs[i][:60])
    print(fn, "updated; suspicious left:", bad if bad else "none")
