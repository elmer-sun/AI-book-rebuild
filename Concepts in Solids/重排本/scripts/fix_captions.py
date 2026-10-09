# -*- coding: utf-8 -*-
# 修 \caption*{} 中的裸数学记号：给含 _ ^ 的记号包 $...$
import io, re

BS = chr(92)
CAP = BS + "caption*{"

FILES = [
    r"E:\AI整理书籍\安德森\重排本\chapters\ch02.tex",
    r"E:\AI整理书籍\安德森\重排本\chapters\ch03.tex",
    r"E:\AI整理书籍\安德森\重排本\chapters\ch01.tex",
]

# 常见裸记号 -> 数学化（按各图注实际出现的写法逐一映射）
SUBS = [
    (r"V_K", r"$V_K$"),
    (r"能隙为 $V_K$", r"能隙为 $V_K$"),
    (r"E_0", r"$E_0$"),
    (r"E_k(p)−E_k(s)", r"$E_k(p)-E_k(s)$"),
    (r"U+E(k)", r"$U+E(k)$"),
    (r"E(k)", r"$E(k)$"),
    (r"n_j = 1", r"$n_j = 1$"),
    (r"n_j", r"$n_j$"),
    (r"k∥", r"$k_\parallel$"),
    (r"k⊥", r"$k_\perp$"),
    (r"E–k", r"$E$–$k$"),
    (r"E-k", r"$E$–$k$"),
    (r"2k_F", r"$2k_F$"),
    (r"k_F", r"$k_F$"),
    (r"k−K", r"$k-K$"),
    (r"k+K", r"$k+K$"),
    (r"ω_r", r"$\omega_r$"),
    (r"E_F", r"$E_F$"),
    (r"e^{-(1/x)}", r"$e^{-(1/x)}$"),
]

def mathify(cap):
    # 已含成对 $ 的先跳过整段判断：只处理未被 $ 包裹的部分
    parts = cap.split("$")
    out = []
    for i, seg in enumerate(parts):
        if i % 2 == 1:  # 已在数学内
            out.append(seg)
            continue
        for a, b in SUBS:
            if a in seg:
                seg = seg.replace(a, b)
        out.append(seg)
    # 重新拼接：偶数段为文本、奇数段为数学 —— 但替换后文本段里混入了新 $，
    # 直接 join 会破坏配对。改为：把替换都做成成对插入后按顺序 join（$ 数必为偶数个由 SUBS 保证）
    res = ""
    for i, seg in enumerate(out):
        res += seg
        if i < len(out) - 1:
            res += "$"
    return res

for fn in FILES:
    s = io.open(fn, encoding="utf-8").read()
    def repl(m):
        inner = m.group(1)
        if "$" in inner:
            return m.group(0)  # 已有数学的图注不动（避免破坏）
        return CAP + mathify(inner) + "}"
    s2 = re.sub(re.escape(CAP) + r"([^}]*)\}", repl, s)
    if s2 != s:
        io.open(fn, "w", encoding="utf-8").write(s2)
        print(fn, "updated")
    else:
        print(fn, "no change")
