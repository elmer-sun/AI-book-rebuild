# -*- coding: utf-8 -*-
"""三路公式tag审计 + 图像数量审计。
1) 从原书分册PDF文字层提取 (N.M) 编号集合（含引用，应为连续1..max）
2) 从 MinerU full.md 提取 \tag{N.M} 集合
3) 从 重排本/chapters/chNN.tex 提取 \tag{N.M} 集合
比对：文字层∩本章节号 vs MinerU vs tex；输出缺失/多余。
用法: python audit_tags.py
"""
import os, re, sys, glob
import fitz

BASE = os.path.dirname(os.path.abspath(__file__)) + r'\..'
ZOOM = os.path.join(BASE, '原书转换')
MINERU = os.path.join(BASE, 'MinerU')
CHAPTERS = os.path.join(BASE, '重排本', 'chapters')

# 章号 -> (分册PDF名, 章起始书页偏移)  偏移: PDF页 = 书页 + off
PARTS = {
    1:('ch01_Introduction_p015-023',),
    2:('ch02_Noninteracting_electron_gas_p024-029',),
    3:('ch03_Born-Oppenheimer_p030-037',),
    4:('ch04_Second_quantization_p038-044',),
    5:('ch05_Hartree-Fock_p045-050',),
    6:('ch06_Interacting_electron_gas_p051-064',),
    7:('ch07_Local_magnetic_moments_p065-093',),
    8:('ch08_Kondo_problem_p094-128',),
    9:('ch09_Screening_and_plasmons_p129-159',),
    10:('ch10_Bosonization_p160-182',),
    11:('ch11_Electron-lattice_interactions_p183-202',),
    12:('ch12_Superconductivity_p001-069',),
    13:('ch13_Disorder_localization_p070-100',),
    14:('ch14_Quantum_phase_transitions_p101-128',),
    15:('ch15_Quantum_Hall_topological_p129-164',),
    16:('ch16_Mottness_p165-211',),
}

def textlayer_nums(ch):
    name = PARTS[ch][0]
    doc = fitz.open(os.path.join(ZOOM, name + '.pdf'))
    txt = '\n'.join(p.get_text() for p in doc)
    doc.close()
    # 文字层里编号可能带空格 (4. 1) —— 归一化
    txt_n = re.sub(r'\(\s*(\d+)\s*\.\s*(\d+)\s*\)', r'(\1.\2)', txt)
    nums = set()
    for a, b in re.findall(r'\((\d+)\.(\d+)\)', txt_n):
        if int(a) == ch: nums.add(int(b))
    return nums

def mineru_tags(ch):
    name = PARTS[ch][0]
    p = os.path.join(MINERU, name, 'full.md')
    if not os.path.exists(p): return None
    md = open(p, encoding='utf-8').read()
    return set(int(b) for a, b in re.findall(r'\\tag\{(\d+)\.(\d+)\}', md) if int(a) == ch)

def tex_tags(ch):
    p = os.path.join(CHAPTERS, f'ch{ch:02d}.tex')
    if not os.path.exists(p): return None
    t = open(p, encoding='utf-8').read()
    return set(int(b) for a, b in re.findall(r'\\tag\{(\d+)\.(\d+)\}', t) if int(a) == ch)

def fig_counts():
    print('\n== 图片审计（MinerU md 内联图 vs tex includegraphics）==')
    for ch in sorted(PARTS):
        name = PARTS[ch][0]
        md_p = os.path.join(MINERU, name, 'full.md')
        n_md = n_tex = 0
        if os.path.exists(md_p):
            md = open(md_p, encoding='utf-8').read()
            n_md = len(re.findall(r'!\[[^\]]*\]\(images/', md))
        for suf in ['', 'a', 'b', 'c']:
            t_p = os.path.join(CHAPTERS, f'ch{ch:02d}{suf}.tex')
            if os.path.exists(t_p):
                n_tex += len(re.findall(r'\\includegraphics', open(t_p, encoding='utf-8').read()))
        flag = '' if n_md == n_tex else '  <-- 数量不一致'
        print(f'ch{ch:02d}: md图块={n_md}  tex图={n_tex}{flag}')

if __name__ == '__main__':
    print('== 公式tag三路审计 ==')
    for ch in sorted(PARTS):
        tl = textlayer_nums(ch)
        mu = mineru_tags(ch)
        tx = tex_tags(ch)
        contig = set(range(1, max(tl) + 1)) if tl else set()
        gap = contig - tl
        line = f'ch{ch:02d}: 文字层{len(tl)}个(最大{max(tl) if tl else 0})'
        if gap: line += f'  文字层缺号:{sorted(gap)}'
        if mu is None: line += '  MinerU未提取'
        else:
            miss_mu = (tl & contig) - mu
            extra_mu = mu - tl
            if miss_mu: line += f'  OCR漏tag:{sorted(miss_mu)}'
            if extra_mu: line += f'  OCR多tag:{sorted(extra_mu)}'
        if tx is None: line += '  tex未装配'
        else:
            miss_tx = (tl & contig) - tx
            extra_tx = tx - (tl & contig)
            if miss_tx: line += f'  tex缺tag:{sorted(miss_tx)}'
            if extra_tx: line += f'  tex多tag:{sorted(extra_tx)}'
        if not any(x in line for x in ['缺', '多', '未']): line += '  OK'
        print(line)
    fig_counts()
