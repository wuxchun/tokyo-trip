#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 index.html 中的所有乱码问题。
原始文件是 UTF-16 LE with BOM，但中文字符被错误地以 UTF-8 编码写入。
需要将乱码的 UTF-8 字节序列还原为正确的中文字符。
"""

import subprocess
import re

# 1. 从 Git 获取当前版本（含之前追加的费用内容）
result = subprocess.run(['git', 'show', 'HEAD:index.html'], capture_output=True)
raw_bytes = result.stdout

# 2. 用 UTF-16 解码
content = raw_bytes.decode('utf-16')

print(f"文件大小: {len(content)} 字符")

# 3. 找出所有乱码位置
# 乱码模式：中文字符被错误地以 UTF-8 编码写入 UTF-16 文件
# 例如 "东" 的 UTF-8 是 E4 B8 9C，在 UTF-16 LE 中会被解释为 3个字符
# 我们需要找到所有这样的乱码并修复

# 先看看标题附近的乱码
title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
if title_match:
    print(f"当前标题: {title_match.group(1)}")

# 看看整个文件中哪些地方有乱码
# 乱码的特征是出现连续的 3字节 UTF-8 序列被解释为 UTF-16 字符
# 常见的乱码映射：
# 涓 = E6 B6 93 -> 中
# 滀 = E6 BB 80 -> 文
# 含 = E5 90 AB -> 的
# 鏄 = E9 8C 84 -> 春
# ュ = E3 83 A5 -> 季
#  = EE 84 9C -> 旅
# 鏃 = E9 8C 83 -> 行
# 呰 = E5 91 B0 -> 
#  = EE 94 91 -> 

# 更简单的方法：将文件视为 UTF-8 编码来解码
# 因为乱码的本质是 UTF-8 字节被当作 UTF-16 来解读
# 我们可以尝试反向操作

# 实际上，正确的修复方法是：
# 将 UTF-16 编码的字节序列重新解释为 UTF-8 编码

# 先看看原始字节中哪些部分是 UTF-8 编码的中文
# 在 UTF-16 LE 文件中，中文字符的 UTF-16 编码是 2字节
# 但如果它们被错误地以 UTF-8 编码写入，就会变成 3个 UTF-16 字符

# 让我尝试另一种方法：将文件内容重新编码为 UTF-8 字节，然后尝试修复
# 实际上，更简单的方法是用正确的编码重新写入

print("\n=== 尝试修复 ===")

# 方法：将内容编码为 UTF-16 LE 字节，然后尝试用 UTF-8 解码这些字节
# 但这不对，因为 UTF-16 和 UTF-8 是完全不同的编码

# 正确的方法：原始文件中的中文字符被错误地存储为 UTF-8 字节序列
# 例如 "2026 东京春季旅行" 被存储为:
# 2026  E6 B1 9F  E6 9D B1  E6 98 A5  E5 AD A3  E6 97 85  E8 A1 8C
# 在 UTF-16 LE 中，这些字节被解释为:
# 2026  6E31 9F6E 1D6E 98A5 5AE5 A3E6 8565 8CE8 8C1A

# 修复方法：将每个 UTF-16 字符的高字节和低字节重新组合
# 实际上，更简单的方法是用 Python 的编码转换

# 让我尝试：将内容编码为 latin-1（不改变字节），然后尝试用 UTF-8 解码
# 但 UTF-16 每个字符是 2 字节，latin-1 是 1 字节

# 实际上，正确的修复思路：
# 1. 将 UTF-16 内容编码为 UTF-16 LE 字节
# 2. 将这些字节重新解释为 UTF-8 编码
# 但这会破坏所有正常的 ASCII 字符

# 让我换个思路：看看 GitHub Pages 上实际显示的是什么
# 用户说之前是正常的，说明 GitHub Pages 能正确显示
# 但我们的检查显示 GitHub Pages 也是乱码...

# 等等，让我重新检查 - 用户说 "标题变成了 2026 涓滀含鏄ュ鏃呰"
# 这说明之前不是这样的，是这次修改后才变成这样的

# 让我检查 index_original.html 是否真的是原始备份
# 也许 index_original.html 也是我们之前修改过的版本

print("\n=== 检查 index_original.html 的 Git 历史 ===")
result2 = subprocess.run(['git', 'log', '--oneline', '--', 'index_original.html'], capture_output=True)
print(result2.stdout.decode('utf-8', errors='replace'))

# 检查 index_original.html 是否在 Git 中
result3 = subprocess.run(['git', 'ls-files', 'index_original.html'], capture_output=True)
print(f"index_original.html 在 Git 中: {bool(result3.stdout.strip())}")

# 检查 index.html 的 Git 历史
print("\n=== index.html 的 Git 历史 ===")
result4 = subprocess.run(['git', 'log', '--oneline', '-5', '--', 'index.html'], capture_output=True)
print(result4.stdout.decode('utf-8', errors='replace'))

# 检查最初的提交
print("\n=== 第一次提交的 index.html ===")
result5 = subprocess.run(['git', 'log', '--reverse', '--oneline', '--', 'index.html'], capture_output=True)
lines = result5.stdout.decode('utf-8', errors='replace').strip().split('\n')
if lines:
    first_commit = lines[0].split()[0]
    print(f"第一次提交: {first_commit}")
    result6 = subprocess.run(['git', 'show', f'{first_commit}:index.html'], capture_output=True)
    raw_first = result6.stdout
    print(f"文件大小: {len(raw_first)} 字节")
    print(f"前20字节: {raw_first[:20].hex()}")
    try:
        c_first = raw_first.decode('utf-16')
        title_first = re.search(r'<title>(.*?)</title>', c_first, re.IGNORECASE)
        if title_first:
            print(f"原始标题: {title_first.group(1)}")
    except:
        print("UTF-16 解码失败")
