# 对行内公式后紧跟全角冒号且发生断行的位置做 \mbox 绑定
# 输入: (文件, 源码中的唯一锚点串) -> 把 math$： 换成 \mbox{math$：}
import glob, os, re

BS = chr(92)
FIXES = [
    ('chapters/ch03.tex', 'alpha'),      # p60 、α = σ²/2−r (占位, 下方按内容定位)
    ('chapters/ch04b.tex', 'Neumann'),
    ('chapters/ch04b.tex', '无穷多重积分'),
    ('chapters/ch04b.tex', '精确解'),
    ('chapters/ch07.tex', '给定的初始远期利率曲线'),
    ('chapters/ch07.tex', '给定的终末远期利率曲线'),
    ('chapters/ch07.tex', '给定的初始波动率曲线'),
    ('chapters/ch07.tex', '给定的终末波动率曲线'),
    ('chapters/ch09.tex', '不正确'),
    ('chapters/ch10.tex', '的坐标态'),
]

DOLLAR = '$'
COLON = '：'
MBOX_S = BS + 'mbox{'

def bind(text, idx_dollar):
    """把 idx_dollar 处 $ 之后的 ：与整个 math+：绑成 \\mbox"""
    # 向前找配对的 $ 或 \( \[ 开头
    j = idx_dollar - 1
    depth = 0
    start = None
    while j >= 0:
        if text[j] == DOLLAR:
            start = j
            break
        j -= 1
    if start is None:
        return None
    end = text.index(COLON, idx_dollar) + 1
    seg = text[start:end]
    return text[:start] + MBOX_S + seg + '}' + text[end:]

# 逐个处理
targets = [
    ('chapters/ch04b.tex', 'Neumann 边界条件', 2),
    ('chapters/ch04b.tex', '无穷多重积分', 1),
    ('chapters/ch04b.tex', '精确解', 1),
    ('chapters/ch07.tex', '给定的初始远期利率曲线', 1),
    ('chapters/ch07.tex', '给定的终末远期利率曲线', 1),
    ('chapters/ch07.tex', '给定的初始波动率曲线', 1),
    ('chapters/ch07.tex', '给定的终末波动率曲线', 1),
    ('chapters/ch09.tex', '不正确', 1),
    ('chapters/ch10.tex', '的坐标态', 2),
]
# 注意: 绑定对象是 math$： —— 只有当冒号紧跟 $ 结束的数学时才处理
for fn, key, times in targets:
    t = open(fn, encoding='utf-8').read()
    done = 0
    for m in re.finditer(re.escape(key), t):
        if done >= times:
            break
        i = m.end()
        # key 后面(可能隔空格)应紧跟 ：
        while i < len(t) and t[i] in ' ':
            i += 1
        if i < len(t) and t[i] == COLON:
            # 向前找 $
            j = i - 1
            while j >= 0 and t[j] != DOLLAR:
                j -= 1
            if j < 0:
                continue
            # 找配对开 $
            k = j - 1
            while k >= 0 and t[k] != DOLLAR:
                k -= 1
            if k < 0:
                continue
            if 'mbox' in t[k:i]:
                continue
            seg = t[k:i + 1]
            t = t[:k] + MBOX_S + seg + '}' + t[i + 1:]
            done += 1
    open(fn, 'w', encoding='utf-8').write(t)
    print(fn, key, '->', done, 'bound')

# p60 的 、α：在 ch03 找 两个解/、$\alpha
t = open('chapters/ch03.tex', encoding='utf-8').read()
m = re.search(r'[^\n]{0,40}、\$\alpha[^$]*\$', t)
if m:
    print('ch03 spot:', m.group(0)[-60:])
