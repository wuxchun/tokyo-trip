#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复：
1. 删除重复的 section（保留第一个完整的）
2. 添加"原始费用明细"标题
3. 添加"人均花费"卡片
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ========== 1. 删除重复的 section ==========
# 找到所有"旅游费用明细与结算"的位置
positions = []
pos = -1
while True:
    pos = content.find('旅游费用明细与结算', pos + 1)
    if pos == -1:
        break
    positions.append(pos)

print(f"旅游费用明细与结算 位置: {positions}")

# 第一个 section 从第一个注释开始
first_comment = content.find('<!-- ======= 旅游费用明细与结算 ======= -->')
# 第二个 section 从第二个注释开始
second_comment = content.find('<!-- ======= 旅游费用明细与结算 ======= -->', first_comment + 1)

# 找到 ECHARTS 脚本开始
echarts_start = content.find('<!-- ==================== ECHARTS 图表脚本 ==================== -->')

print(f"第一个注释: {first_comment}")
print(f"第二个注释: {second_comment}")
print(f"ECHARTS: {echarts_start}")

# 保留第一个 section 到 ECHARTS 之间的内容
first_section = content[first_comment:echarts_start]

# 检查第一个 section 是否包含"原始明细表"
has_table = '原始明细表' in first_section
print(f"第一个 section 包含原始明细表: {has_table}")

# 检查第二个 section 是否包含"原始明细表"
second_section = content[second_comment:echarts_start] if second_comment > 0 else ""
has_table_second = '原始明细表' in second_section
print(f"第二个 section 包含原始明细表: {has_table_second}")

# 如果第一个 section 没有表格，第二个有，则合并
if not has_table and has_table_second:
    # 找到第一个 section 的 </section> 结束
    first_section_end = first_section.rfind('</section>')
    first_body = first_section[:first_section_end]
    
    # 从第二个 section 中提取原始明细表部分
    table_start = second_section.find('<!-- 原始明细表 -->')
    table_part = second_section[table_start:]
    
    new_section = first_body + "\n\n" + table_part
    content = content[:first_comment] + new_section + content[echarts_start:]
    print("✅ 合并了第一个 section 和第二个 section 的表格")
elif has_table:
    print("✅ 第一个 section 已有表格，无需合并")
else:
    print("⚠️ 两个 section 都没有表格")

# ========== 2. 添加"原始费用明细"标题 ==========
# 在"原始明细表"注释后面添加 h3 标题
target = '<!-- 原始明细表 -->'
if target in content:
    idx = content.find(target)
    # 检查后面是否已经有 h3 标题
    after = content[idx:idx+200]
    if '原始费用明细' not in after:
        replacement = '<!-- 原始明细表 -->\n            <h3 style="font-size:1.1rem; font-weight:700; margin-bottom:1rem; color:var(--charcoal);">\n                <i class="fa-solid fa-table"></i> 原始费用明细\n            </h3>'
        content = content[:idx] + replacement + content[idx + len(target):]
        print("✅ 添加了原始费用明细标题")
    else:
        print("✅ 原始费用明细标题已存在")

# ========== 3. 添加"人均花费"卡片 ==========
# 在费用汇总的 grid 中添加人均花费卡片
# 找到亲戚需转账金额卡片后面的 </div>
target = 'CNY（总费用 × 2/3）'
if target in content:
    idx = content.find(target) + len(target)
    # 找到这个 div 的结束
    div_end = content.find('</div>', idx)
    # 再往后找两个 </div>（一个结束卡片 div，一个结束 grid div）
    div_end2 = content.find('</div>', div_end + 1)
    
    # 检查是否已经有人均花费
    if '人均花费' not in content[div_end:div_end2]:
        # 在 grid 的最后一个卡片后面插入人均花费
        # 找到 grid 的结束 </div>
        grid_end = content.find('</div>', div_end2 + 1)
        
        human_card = """
                <div style="background:linear-gradient(135deg, #ffecd2, #fcb69f); border-radius:12px; padding:1rem; color:#1a1a2e; text-align:center;">
                    <div style="font-size:0.85rem; opacity:0.8; margin-bottom:0.3rem; font-weight:600;">👤 人均花费</div>
                    <div style="font-size:1.6rem; font-weight:700; color:#8b5cf6;">¥1,392.35</div>
                    <div style="font-size:0.75rem; opacity:0.7;">CNY（总费用 ÷ 3人）</div>
                </div>"""
        
        content = content[:grid_end] + human_card + "\n            " + content[grid_end:]
        print("✅ 添加了人均花费卡片")
    else:
        print("✅ 人均花费卡片已存在")

# ========== 4. 删除重复的 section（如果还有） ==========
# 检查是否还有多个"旅游费用明细与结算"
count = content.count('旅游费用明细与结算')
print(f"旅游费用明细与结算 出现次数: {count}")

# 如果还有重复，删除多余的
if count > 2:
    # 找到第二个 section 的开始和结束
    second_start = content.find('<!-- ======= 旅游费用明细与结算 ======= -->', first_comment + 1)
    if second_start > 0:
        # 找到第二个 section 的结束（下一个 </section> 之后）
        second_section_end = content.find('</section>', second_start) + len('</section>')
        # 删除第二个 section
        content = content[:second_start] + content[second_section_end:]
        print("✅ 删除了重复的 section")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n=== 最终验证 ===")
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print(f"原始费用明细: {'原始费用明细' in c}")
print(f"原始明细表: {'原始明细表' in c}")
print(f"人均花费: {'人均花费' in c}")
print(f"cat-badge: {'cat-badge' in c}")
print(f"sortable: {'sortable' in c}")
print(f"05/02: {'05/02' in c}")
print(f"费用汇总: {c.count('费用汇总')}")
print(f"数据分析图表: {c.count('数据分析图表')}")
print(f"旅游费用明细与结算: {c.count('旅游费用明细与结算')}")
print(f"排序脚本: {'表格排序脚本' in c}")
