#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""删除重复的 section"""

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 位置4是第二个重复 section 的开始
# 从 "===== 旅游费用明细与结算" 开始
dup_start = c.find('===== 旅游费用明细与结算 ======= -->')
if dup_start > 0:
    # 找到这个 section 的结束（</section>）
    dup_end = c.find('</section>', dup_start) + len('</section>')
    print(f"重复 section: {dup_start} -> {dup_end}")
    
    # 删除重复
    c = c[:dup_start] + c[dup_end:]
    print("✅ 删除了重复的 section")

# 修复被破坏的注释
c = c.replace('===== 旅游费用明细与结算 ======= -->', '<!-- ======= 旅游费用明细与结算 ======= -->')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("\n=== 最终验证 ===")
print(f"旅游费用明细与结算: {c.count('旅游费用明细与结算')}")
print(f"费用汇总: {c.count('费用汇总')}")
print(f"数据分析图表: {c.count('数据分析图表')}")
print(f"原始费用明细: {'原始费用明细' in c}")
print(f"原始明细表: {'原始明细表' in c}")
print(f"人均花费: {'人均花费' in c}")
print(f"cat-badge: {'cat-badge' in c}")
print(f"sortable: {'sortable' in c}")
print(f"05/02: {'05/02' in c}")
print(f"排序脚本: {'表格排序脚本' in c}")
