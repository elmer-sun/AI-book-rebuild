# -*- coding: utf-8 -*-
"""一键刷新全书：装配 parts → 真图替换 → 余量占位 → xelatex ×3。
用法：python refresh_book.py   （在 文小刚/重排本/ 下有脚本自身路径即可）"""
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.stdout + r.stderr


def main():
    print("== assemble ==")
    out = run([sys.executable, os.path.join("scripts", "assemble.py")])
    print(out[-500:])
    print("== apply_figs (真图) ==")
    out = run([sys.executable, os.path.join("scripts", "apply_figs.py")])
    print(out[-800:])
    print("== apply_figs_placeholder (余量占位) ==")
    out = run([sys.executable,
               os.path.join("scripts", "apply_figs_placeholder.py")])
    print(out[-800:])
    print("== xelatex x3 ==")
    for i in (1, 2, 3):
        out = run(["xelatex", "-interaction=nonstopmode", "-jobname=main",
                   "main.tex"])
        tail = [l for l in out.splitlines() if "Output written" in l
                or l.startswith("!")]
        print(f"pass{i}:", tail[:3])
    n_err = 0
    log = io_errors = None
    with open("main.log", encoding="utf-8", errors="ignore") as f:
        log = f.read()
    n_err = sum(1 for l in log.splitlines() if l.startswith("!"))
    print(f"== final: {n_err} errors ==")


if __name__ == "__main__":
    main()
