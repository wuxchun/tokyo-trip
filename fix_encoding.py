#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 index.html 的编码问题。
原始文件是 UTF-16 LE with BOM。
使用 Python 的 utf-16 编码读取和写入，让 Python 自动处理 BOM。
"""

import os

index_path = r"C:\AI\VS Code\Cline Study\51-travel-2026\index.html"

# 1. 检查原始文件编码
with open(index_path, 'rb') as f:
    raw = f.read(10)
print(f"原始文件前10字节: {raw.hex()}")
print(f"BOM: {raw[:2].hex()}")

# 2. 用 utf-16 读取（Python 自动处理 BOM）
with open(index_path, 'r', encoding='utf-16') as f:
    content = f.read()

print(f"\n读取成功！文件共 {len(content)} 个字符")
print(f"前200字符: {content[:200]}")
print(f"\n包含'东京': {'东京' in content}")
print(f"包含'2026 东京': {'2026 东京' in content}")

# 3. 检查标题
import re
title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
if title_match:
    print(f"标题: {title_match.group(1)}")

# 4. 用 utf-16 写回（Python 自动添加 BOM）
with open(index_path, 'w', encoding='utf-16') as f:
    f.write(content)

# 5. 验证写回后的文件
with open(index_path, 'rb') as f:
    raw2 = f.read(10)
print(f"\n写回后文件前10字节: {raw2.hex()}")
print(f"BOM: {raw2[:2].hex()}")

# 6. 再次读取验证
with open(index_path, 'r', encoding='utf-16') as f:
    content2 = f.read()
print(f"再次读取成功！文件共 {len(content2)} 个字符")
print(f"包含'东京': {'东京' in content2}")
print(f"包含'2026 东京': {'2026 东京' in content2}")

print("\n✅ 编码修复完成！")
