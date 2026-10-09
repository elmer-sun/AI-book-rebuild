#!/bin/bash
# 卡罗尔项目：免 token Agent API 批量提取（主路线 v4 等 MINERU_TOKEN；本脚本为应急路线）
# 顺序提交避开限流；输出 卡罗尔/MinerU/fallback/<key>.md
cd "E:/AI整理书籍" || exit 1
PY="python"
SCRIPT="mineru_agent_fallback.py"
OUTDIR="卡罗尔/MinerU/fallback"
mkdir -p "$OUTDIR"

declare -A FILES=(
  [00_front]="卡罗尔/章节拆分/00_前言与目录_pVII-XIV.pdf"
  [01]="卡罗尔/章节拆分/01_狭义相对论与平直时空_p001-047.pdf"
  [02]="卡罗尔/章节拆分/02_流形_p048-092.pdf"
  [03]="卡罗尔/章节拆分/03_曲率_p093-150.pdf"
  [04]="卡罗尔/章节拆分/04_引力_p151-192.pdf"
  [05]="卡罗尔/章节拆分/05_史瓦西解_p193-237.pdf"
  [06]="卡罗尔/章节拆分/06_更一般的黑洞_p238-273.pdf"
  [07]="卡罗尔/章节拆分/07_微扰理论与引力辐射_p274-322.pdf"
  [08]="卡罗尔/章节拆分/08_宇宙学_p323-375.pdf"
  [09]="卡罗尔/章节拆分/09_弯曲时空量子场论_p376-422.pdf"
  [10_app]="卡罗尔/章节拆分/10_附录_p423-494.pdf"
  [11_bib]="卡罗尔/章节拆分/11_文献目录_p495-500.pdf"
)
ORDER=(00_front 01 02 03 04 05 06 07 08 09 10_app 11_bib)

for key in "${ORDER[@]}"; do
  f="${FILES[$key]}"
  out="$OUTDIR/$key.md"
  if [ -s "$out" ]; then
    echo "[skip] $key (exists)"
    continue
  fi
  echo "=== $key <- $f ==="
  "$PY" "$SCRIPT" "$f" --ocr --insecure --timeout 1800 -o "$out"
  rc=$?
  echo "--- $key rc=$rc $( [ -s "$out" ] && echo OK || echo FAILED ) ---"
done
echo "ALL DONE"
ls -la "$OUTDIR"
