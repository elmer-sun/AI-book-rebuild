#!/bin/bash
# 用法: ./scripts/new_chapter.sh chNN  —— 删除占位文件以便 Write 工具创建
rm -f "chapters/$1.tex"
