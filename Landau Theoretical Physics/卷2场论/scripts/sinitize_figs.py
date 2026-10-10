# -*- coding: utf-8 -*-
"""图2/图12 图内标签汉化（原书即中文：绝对未来/绝对过去/绝对分隔；几何影区/照明区）"""
import io

fa = r'E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\scripts\draw_figs_fa.py'
s = io.open(fa, encoding='utf-8').read()
s = s.replace("    # 区域标注（原书中文改为英文）\n"
              "    ax.text(0.10, 0.78, 'absolute future', ha='center', va='center', fontsize=8.5)\n"
              "    ax.text(0.02, -0.84, 'absolute past', ha='center', va='center', fontsize=8.5)\n"
              "    ax.text(-0.82, 0.10, 'absolute', ha='center', va='center', fontsize=8.5)\n"
              "    ax.text(-0.82, -0.12, 'separation', ha='center', va='center', fontsize=8.5)\n"
              "    ax.text(0.84, 0.10, 'absolute', ha='center', va='center', fontsize=8.5)\n"
              "    ax.text(0.84, -0.12, 'separation', ha='center', va='center', fontsize=8.5)",
              "    # 区域标注（照原书中文）\n"
              "    ax.text(0.10, 0.78, '绝对未来', ha='center', va='center', fontsize=8.5)\n"
              "    ax.text(0.02, -0.84, '绝对过去', ha='center', va='center', fontsize=8.5)\n"
              "    ax.text(-0.82, 0.10, '绝对分隔', ha='center', va='center', fontsize=8.5)\n"
              "    ax.text(0.84, 0.10, '绝对分隔', ha='center', va='center', fontsize=8.5)")
io.open(fa, 'w', encoding='utf-8').write(s)

fb = r'E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\scripts\draw_figs_fb.py'
s = io.open(fb, encoding='utf-8').read()
s = s.replace("    # 区域标注（原书为中文\"几何影区/照明区\"，图内不用中文，以英文替代）\n"
              "    ax.text(-2.55, 0.22, 'geometric shadow', ha='center', va='center',\n"
              "            fontsize=7.5)\n"
              "    ax.text(6.3, 0.50, 'illuminated region', ha='center', va='center',\n"
              "            fontsize=7.5)",
              "    # 区域标注（照原书中文）\n"
              "    ax.text(-2.55, 0.22, '几何影区', ha='center', va='center', fontsize=7.5)\n"
              "    ax.text(6.3, 0.50, '照明区', ha='center', va='center', fontsize=7.5)")
io.open(fb, 'w', encoding='utf-8').write(s)
print('patched both scripts')
