#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查 Git 中保存的 index.html 版本"""

import subprocess
import re

# 获取 Git 中最新提交的 index.html
result = subprocess.run(['git', 'show', 'HEAD:index.html'], capture_output=True)
raw_bytes = result.stdout

print(f"Git 版本文件大小: {len(raw_bytes)} 字节")
print(f"前20字节: {raw_bytes[:20].hex()}")

# 尝试 UTF-16 读取
try:
    c = raw_bytes.decode('utf-16')
    print(f"\nUTF-16 解码成功: {len(c)} 字符")
    print(f"前200字符: {c[:200]}")
    title = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE)
    if title:
        print(f"标题: {title.group(1)}")
except:
    print("UTF-16 解码失败")

# 尝试 UTF-8 读取
try:
    c = raw_bytes.decode('utf-8')
    print(f"\nUTF-8 解码成功: {len(c)} 字符")
    print(f"前200字符: {c[:200]}")
    title = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE)
    if title:
        print(f"标题: {title.group(1)}")
except:
    print("UTF-8 解码失败")

# 尝试 GBK 读取
try:
    c = raw_bytes.decode('gbk')
    print(f"\nGBK 解码成功: {len(c)} 字符")
    print(f"前200字符: {c[:200]}")
    title = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE)
    if title:
        print(f"标题: {title.group(1)}")
except:
    print("GBK 解码失败")

# 查看 GitHub Pages 上实际显示的页面
print("\n\n=== 查看 GitHub Pages 上的页面 ===")
import urllib.request
try:
    req = urllib.request.Request('https://wuxchun.github.io/tokyo-trip/')
    with urllib.request.urlopen(req) as resp:
        html_bytes = resp.read()
    print(f"GitHub Pages 返回 {len(html_bytes)} 字节")
    print(f"前20字节: {html_bytes[:20].hex()}")
    
    # 尝试 UTF-8
    try:
        c = html_bytes.decode('utf-8')
        print(f"\nUTF-8 解码成功")
        title = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE)
        if title:
            print(f"标题: {title.group(1)}")
        print(f"前500字符: {c[:500]}")
    except:
        print("UTF-8 解码失败")
        
    # 尝试 UTF-16
    try:
        c = html_bytes.decode('utf-16')
        print(f"\nUTF-16 解码成功")
        title = re.search(r'<title>(.*?)</title>', c, re.IGNORECASE)
        if title:
            print(f"标题: {title.group(1)}")
        print(f"前500字符: {c[:500]}")
    except:
        print("UTF-16 解码失败")
except Exception as e:
    print(f"请求失败: {e}")
