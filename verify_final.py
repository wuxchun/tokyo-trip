#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 index.html 的最终状态"""

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("=== 验证结果 ===")
print(f"原始费用明细: {'原始费用明细' in c}")
print(f"原始明细表: {'原始明细表' in c}")
print(f"人均花费: {'人均花费' in c}")
print(f"cat-badge: {'cat-badge' in c}")
print(f"sortable: {'sortable' in c}")
print(f"05/02: {'05/02' in c}")
print(f"05/03: {'05/03' in c}")
print(f"05/04: {'05/04' in c}")
print(f"费用汇总: {c.count('费用汇总')}")
print(f"数据分析图表: {c.count('数据分析图表')}")
print(f"旅游费用明细与结算: {c.count('旅游费用明细与结算')}")
print(f"排序脚本: {'表格排序脚本' in c}")
print(f"文件总大小: {len(c)} 字符")
print(f"文件总行数: {c.count(chr(10)) + 1} 行")
