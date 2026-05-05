#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查第一次提交的 index.html"""

import subprocess
import re

# 第一次提交
result = subprocess.run(['git', 'show', 'bbe90da:index.html'], capture_output=True)
raw_bytes = result.stdout

print(f"第一次提交文件大小: {len(raw_bytes)} 字节")
print(f"前50字节: {raw_bytes[:50].hex()}")

# 尝试 UTF-8 解码
try:
    c = raw_bytes.decode('utf-8')
    print(f"\nUTF-8 解码成功: {len(c)} 字符")
    title = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE)
    if title:
        print(f"标题: {title.group(1)}")
    print(f"前500字符: {c[:500]}")
except Exception as e:
    print(f"UTF-8 解码失败: {e}")

# 检查第二次提交
print("\n\n=== 第二次提交 (9eff845) ===")
result2 = subprocess.run(['git', 'show', '9eff845:index.html'], capture_output=True)
raw2 = result2.stdout
print(f"文件大小: {len(raw2)} 字节")
print(f"前20字节: {raw2[:20].hex()}")

try:
    c2 = raw2.decode('utf-8')
    print(f"UTF-8 解码成功: {len(c2)} 字符")
    title2 = re.search(r'<title>(.*?)</title>', c2, re.IGNORECASE)
    if title2:
        print(f"标题: {title2.group(1)}")
except:
    print("UTF-8 解码失败")

try:
    c2 = raw2.decode('utf-16')
    print(f"UTF-16 解码成功: {len(c2)} 字符")
    title2 = re.search(r'<title>(.*?)</title>', c2, re.IGNORECASE)
    if title2:
        print(f"标题: {title2.group(1)}")
except:
    print("UTF-16 解码失败")

# 检查第三次提交 (3aae19c)
print("\n\n=== 第三次提交 (3aae19c) ===")
result3 = subprocess.run(['git', 'show', '3aae19c:index.html'], capture_output=True)
raw3 = result3.stdout
print(f"文件大小: {len(raw3)} 字节")
print(f"前20字节: {raw3[:20].hex()}")

try:
    c3 = raw3.decode('utf-8')
    print(f"UTF-8 解码成功: {len(c3)} 字符")
    title3 = re.search(r'<title>(.*?)</title>', c3, re.IGNORECASE)
    if title3:
        print(f"标题: {title3.group(1)}")
except:
    print("UTF-8 解码失败")

try:
    c3 = raw3.decode('utf-16')
    print(f"UTF-16 解码成功: {len(c3)} 字符")
    title3 = re.search(r'<title>(.*?)</title>', c3, re.IGNORECASE)
    if title3:
        print(f"标题: {title3.group(1)}")
except:
    print("UTF-16 解码失败")
