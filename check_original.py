#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查 index_original.html 的编码和内容"""

# 检查 index_original.html
with open('index_original.html', 'rb') as f:
    raw = f.read(20)
print(f"index_original.html 前20字节: {raw.hex()}")

# 尝试用 UTF-16 读取
with open('index_original.html', 'r', encoding='utf-16') as f:
    c = f.read()
print(f"UTF-16 读取: {len(c)} 字符")
print(f"前200字符: {c[:200]}")

import re
title = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE)
if title:
    print(f"标题: {title.group(1)}")

# 检查 index.html
print("\n--- index.html ---")
with open('index.html', 'rb') as f:
    raw = f.read(20)
print(f"index.html 前20字节: {raw.hex()}")

with open('index.html', 'r', encoding='utf-16') as f:
    c2 = f.read()
print(f"UTF-16 读取: {len(c2)} 字符")
print(f"前200字符: {c2[:200]}")

title2 = re.search(r'<title>(.*?)</title>', c2, re.IGNORECASE)
if title2:
    print(f"标题: {title2.group(1)}")

# 检查 GitHub Pages 上正确的标题应该是什么
# 尝试用 UTF-8 读取 index_original.html
print("\n--- 尝试 UTF-8 读取 index_original.html ---")
with open('index_original.html', 'rb') as f:
    raw_bytes = f.read()
try:
    c_utf8 = raw_bytes.decode('utf-8')
    print(f"UTF-8 读取成功: {len(c_utf8)} 字符")
    print(f"前200字符: {c_utf8[:200]}")
    title_utf8 = re.search(r'<title>(.*?)</title>', c_utf8, re.IGNORECASE)
    if title_utf8:
        print(f"标题(UTF-8): {title_utf8.group(1)}")
except:
    print("UTF-8 解码失败")

# 尝试用 GBK 读取
print("\n--- 尝试 GBK 读取 index_original.html ---")
try:
    c_gbk = raw_bytes.decode('gbk')
    print(f"GBK 读取成功: {len(c_gbk)} 字符")
    print(f"前200字符: {c_gbk[:200]}")
    title_gbk = re.search(r'<title>(.*?)</title>', c_gbk, re.IGNORECASE)
    if title_gbk:
        print(f"标题(GBK): {title_gbk.group(1)}")
except:
    print("GBK 解码失败")
