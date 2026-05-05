#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查 index.html 中的关键内容"""

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("=== 内容检查 ===")
print(f"MM/DD (05/02): {'05/02' in c}")
print(f"(CN): {'(CN)' in c}")
print(f"折算日元: {'折算日元' in c}")
print(f"折算人民币: {'折算人民币' in c}")
print(f"人均花费: {'人均花费' in c}")
print(f"原始费用明细: {'原始费用明细' in c}")
print(f"cat-badge: {'cat-badge' in c}")
print(f"sortable: {'sortable' in c}")
print(f"排序脚本: {'表格排序脚本' in c}")
print(f"费用汇总: {c.count('费用汇总')}")
print(f"数据分析图表: {c.count('数据分析图表')}")
print(f"旅游费用明细与结算: {c.count('旅游费用明细与结算')}")
print(f"文件大小: {len(c)} 字符")
