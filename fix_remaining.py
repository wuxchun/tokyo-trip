#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复剩余问题：
1. 删除 (CN) 后缀
2. 删除"折算日元/人民币"列
3. 添加"人均花费"卡片
"""

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# ========== 1. 删除 (CN) ==========
c = c.replace('(CN)', '')
print(f"(CN) 删除后: {'(CN)' not in c}")

# ========== 2. 删除"折算日元/人民币"列 ==========
# 找到表格中带有"折算日元"或"折算人民币"的行
lines = c.split('\n')
new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if '折算日元' in line or '折算人民币' in line:
        skip_next = True
        continue
    if skip_next:
        skip_next = False
        continue
    new_lines.append(line)
c = '\n'.join(new_lines)
print(f"折算日元: {'折算日元' in c}")
print(f"折算人民币: {'折算人民币' in c}")

# ========== 3. 添加"人均花费"卡片 ==========
# 在"亲戚需转账金额"卡片后面添加
target = 'CNY（总费用 × 2/3）'
if target in c:
    idx = c.find(target) + len(target)
    # 找到这个 div 的结束
    div_end = c.find('</div>', idx)
    # 再往后找 grid 的结束
    div_end2 = c.find('</div>', div_end + 1)
    grid_end = c.find('</div>', div_end2 + 1)
    
    if '人均花费' not in c[div_end:grid_end]:
        human_card = """
                <div style="background:linear-gradient(135deg, #ffecd2, #fcb69f); border-radius:12px; padding:1rem; color:#1a1a2e; text-align:center;">
                    <div style="font-size:0.85rem; opacity:0.8; margin-bottom:0.3rem; font-weight:600;">👤 人均花费</div>
                    <div style="font-size:1.6rem; font-weight:700; color:#8b5cf6;">¥1,392.35</div>
                    <div style="font-size:0.75rem; opacity:0.7;">CNY（总费用 ÷ 3人）</div>
                </div>"""
        c = c[:grid_end] + human_card + "\n            " + c[grid_end:]
        print("✅ 添加了人均花费卡片")
    else:
        print("✅ 人均花费卡片已存在")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("\n=== 最终验证 ===")
print(f"(CN): {'(CN)' in c}")
print(f"折算日元: {'折算日元' in c}")
print(f"折算人民币: {'折算人民币' in c}")
print(f"人均花费: {'人均花费' in c}")
print(f"原始费用明细: {'原始费用明细' in c}")
print(f"cat-badge: {'cat-badge' in c}")
print(f"sortable: {'sortable' in c}")
print(f"05/02: {'05/02' in c}")
print(f"费用汇总: {c.count('费用汇总')}")
print(f"数据分析图表: {c.count('数据分析图表')}")
print(f"旅游费用明细与结算: {c.count('旅游费用明细与结算')}")
