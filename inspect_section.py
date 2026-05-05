#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查看费用明细 section 的实际内容"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('旅游费用明细与结算')
end = content.find('ECHARTS')

section = content[start:end]
print(f"Section 长度: {len(section)} 字符")
print(f"Section 行数: {section.count(chr(10))} 行")
print()
print("=" * 60)
print(section[:4000])
print("=" * 60)
print("... (中间省略) ...")
print("=" * 60)
if len(section) > 4000:
    print(section[-2000:])
