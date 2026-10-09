# -*- coding: utf-8 -*-
"""生成 fig3_08.tex：五条以光子能量对齐的对数标尺。
坐标离线算成字面值，绕开本机 pgfmath 对小宗量 log10 的缺陷。
重跑：python gen_fig3_08.py"""
from math import log10

W = 12.4  # 标尺总长 cm，对应 1 neV - 100 eV（11 个十进位）

def xE(E): return (log10(E)+9)/11*W          # E in eV
def xT(T): return (log10(T)+4.9354)/11*W     # k_B = 8.61733e-5 eV/K
def xC(n): return (log10(n)+5.0934)/11*W     # 1 cm^-1 = 1.23984e-4 eV
def xL(l): return (3.0934-log10(l))/11*W     # lambda in m, hc = 1.23984e-6 eV m
def xF(f): return (log10(f)-5.3834)/11*W     # h = 4.135667e-15 eV s
f3 = lambda x: f'{x:.3f}'

def minors(fn, d0, d1):
    out = []
    for d in range(d0, d1+1):
        for m in range(2, 10):
            x = fn(m*10.0**d)
            if 0.03 < x < W-0.03:
                out.append(f3(x))
    return out

L = []
A = L.append
A(r"""% 图 3.8 电磁波谱：五条以光子能量对齐的对数标尺
% T=E/kB；E(eV)；波数 E/(hc)；波长 c/f；频率 E/h
% 统一映射 x=(log10(E/eV)+9)/11*12.4 cm，覆盖 1 neV - 100 eV（坐标已离线计算为字面值）
\documentclass[tikz,border=5pt]{standalone}
\usetikzlibrary{arrows.meta}
\usepackage{amsmath}
\usepackage{bm}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\begin{document}
\begin{tikzpicture}[line width=0.8pt,>=Stealth,
  lab/.style={above,inner sep=1.5pt,font=\footnotesize}]""")

def row(y, majors, mins, rightlab):
    A('\\draw[line width=0.9] (0,%s) -- (%s,%s);' % (y, W, y))
    A('\\foreach \\xx/\\l in {' + ','.join('%s/{%s}' % (f3(x), l) for x, l in majors) + '}{')
    A('  \\draw (\\xx,%s) -- ++(0,0.14);' % y)
    A('  \\node[lab] at (\\xx,%s+0.15) {\\l};' % y)
    A('}')
    if mins:
        A('\\foreach \\xx in {' + ','.join(mins) + '}{')
        A('  \\draw[line width=0.45] (\\xx,%s) -- ++(0,0.07);' % y)
        A('}')
    A('\\node[anchor=west] at (12.62,%s) {%s};' % (y, rightlab))

# ---------- 行 1：T (K) ----------
y = 0
majors = [(xT(v), l) for v, l in [(1e-5,'$10^{-5}$'),(1e-4,'$10^{-4}$'),(1e-3,'$10^{-3}$'),
          (0.01,'$10^{-2}$'),(0.1,'$0.1$'),(1,'$1$'),(10,'$10$'),(100,'$100$'),
          (1e3,'$10^{3}$'),(1e4,'$10^{4}$'),(1e5,'$10^{5}$'),(1e6,'$10^{6}$')]]
row(y, majors, minors(xT,-5,6), '$T\\;(\\mathrm{K})$')
A('\\draw[line width=0.7] (%s,%s) -- ++(0,1.30);' % (f3(xT(2.7)), y))
A('\\node[above,inner sep=1pt] at (%s,%s) {$T_{\\mathrm{CMB}}$};' % (f3(xT(2.7)), y+1.32))
A('\\draw[line width=0.7] (%s,%s) -- ++(0,0.78);' % (f3(xT(4.2)), y))
A('\\node[lab,anchor=south west,inner sep=1pt] at (%s,%s) {$\\mathrm{He}^4$};' % (f3(xT(4.2)+0.05), y+0.80))
A('\\draw[line width=0.7] (%s,%s) -- ++(0,0.78);' % (f3(xT(77)), y))
A('\\node[lab,anchor=south east,inner sep=1pt] at (%s,%s) {$\\mathrm{N}_2$};' % (f3(xT(77)-0.04), y+0.80))
A('\\draw[line width=0.7] (%s,%s) -- ++(0,0.78);' % (f3(xT(300)), y))
A('\\node[lab,anchor=south west,inner sep=1pt] at (%s,%s) {Room T};' % (f3(xT(300)+0.04), y+0.80))

# ---------- 行 2：E ----------
y = -1.30
majors = [(xE(v), l) for v, l in [(1e-9,'$1\\,$neV'),(1e-8,'$10\\,$neV'),(1e-7,'$0.1\\,\\mu$eV'),
          (1e-6,'$1\\,\\mu$eV'),(1e-5,'$10\\,\\mu$eV'),(1e-4,'$0.1\\,$meV'),(1e-3,'$1\\,$meV'),
          (0.01,'$10\\,$meV'),(0.1,'$0.1\\,$eV'),(1,'$1\\,$eV')]]
majors.append((xE(10), '$10\\,$eV'))
row(y, majors[:-1], minors(xE,-9,2), '$E$')
A('\\draw (%s,%s) -- ++(0,0.14);' % (f3(xE(10)), y))
A('\\node[lab,anchor=south west,inner sep=1pt] at (%s,%s) {$10\\,$eV};' % (f3(xE(10)+0.012), y+0.15))
A('\\draw[line width=0.7] (%s,%s) -- ++(0,0.62);' % (f3(xE(13.6)), y))
A('\\node[lab] at (%s,%s) {H};' % (f3(xE(13.6)), y+0.64))

# ---------- 行 3：波数 ----------
y = -2.60
majors = [(xC(v), l) for v, l in [(1e-4,'$10^{-4}$'),(1e-3,'$10^{-3}$'),(0.01,'$10^{-2}$'),
          (0.1,'$10^{-1}$'),(1,'$1$'),(10,'$10$'),(100,'$100$'),(1e3,'$10^{3}$'),
          (1e4,'$10^{4}$'),(1e5,'$10^{5}$')]]
row(y, majors, minors(xC,-4,5), '$f\\;(\\mathrm{cm}^{-1})$')
A('\\node[font=\\footnotesize] at (%s,%s) {rotations};' % (f3(xC(1.2)), y+0.62))
A('\\node[font=\\footnotesize] at (%s,%s) {vibrations};' % (f3(xC(20)), y+0.62))
A('\\draw[line width=0.7] (%s,%s) -- ++(0,0.48);' % (f3(xC(1000)), y))
A('\\node[font=\\footnotesize,anchor=south east,inner sep=1pt] at (%s,%s) {C--H bend};' % (f3(xC(1000)-0.06), y+0.56))
A('\\draw[line width=0.7] (%s,%s) -- ++(0,0.48);' % (f3(xC(3000)), y))
A('\\node[font=\\footnotesize,anchor=south west,inner sep=1pt] at (%s,%s) {C--H stretch};' % (f3(xC(3000)+0.06), y+0.62))
A('\\node[font=\\footnotesize,anchor=south west,inner sep=1pt] at (%s,%s) {$\\pi$ bonds};' % (f3(xC(1.5e4)+0.3), y+0.94))
A('\\node[font=\\footnotesize,anchor=south west,inner sep=1pt] at (%s,%s) {$\\sigma$ bonds};' % (f3(xC(2.6e4)+0.8), y+0.70))

# ---------- 行 4：波长 ----------
y = -3.90
majors = [(xL(v), l) for v, l in [(1000,'$1\\,$km'),(100,'$100\\,$m'),(10,'$10\\,$m'),(1,'$1\\,$m'),
          (0.1,'$10\\,$cm'),(0.01,'$1\\,$cm'),(0.001,'$1\\,$mm'),(1e-4,'$0.1\\,$mm'),
          (1e-5,'$10\\,\\mu$m'),(1e-6,'$1\\,\\mu$m'),(1e-7,'$100\\,$nm')]]
row(y, majors, minors(xL,-8,2), '$\\lambda$')
A('\\draw[line width=0.7] (%s,%s) -- ++(0,0.44);' % (f3(xL(7e-7)), y))
A('\\node[lab] at (%s,%s) {R};' % (f3(xL(7e-7)), y+0.50))
A('\\draw[line width=0.7] (%s,%s) -- ++(0,0.44);' % (f3(xL(4e-7)), y))
A('\\node[lab] at (%s,%s) {V};' % (f3(xL(4e-7)), y+0.50))
A('\\draw[line width=0.7] (%s,%s) -- ++(0,0.64);' % (f3(xL(5e-7)), y))
A('\\node[lab] at (%s,%s) {G};' % (f3(xL(5e-7)), y+0.70))

# ---------- 行 5：频率 ----------
y = -5.20
majors = [(xF(v), l) for v, l in [(1e6,'$1\\,$MHz'),(1e7,'$10\\,$MHz'),
          (1e8,'$100\\,$MHz'),(1e9,'$1\\,$GHz'),(1e10,'$10\\,$GHz'),(1e11,'$100\\,$GHz'),
          (1e12,'$1\\,$THz'),(1e13,'$10^{13}$'),(1e14,'$10^{14}$'),(1e15,'$10^{15}$'),(1e16,'$10^{16}$')]]
row(y, majors, minors(xF,5,16), '$f\\;(\\mathrm{Hz})$')
A('\\node[font=\\footnotesize] at (%s,%s) {radio};' % (f3(xF(1e7)), y+0.60))
A('\\node[font=\\footnotesize] at (%s,%s) {microwave};' % (f3(xF(2e10)), y+0.60))
A('\\node[font=\\footnotesize] at (%s,%s) {far IR};' % (f3(xF(1.8e12)), y+0.60))
A('\\node[font=\\footnotesize] at (%s,%s) {near IR};' % (f3(xF(4.5e13)), y+0.60))
A('\\node[font=\\footnotesize] at (%s,%s) {optical};' % (f3(xF(4.5e14)), y+0.60))
A('\\node[font=\\footnotesize,anchor=east] at (%s,%s) {UV};' % (W, y+0.60))

A('\\end{tikzpicture}')
A('\\end{document}')
with open('fig3_08.tex', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(L) + '\n')
print('written, lines =', len(L))
