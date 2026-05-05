#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 index.html 中的费用明细部分：
1. 删除重复的"费用汇总"（保留第一个）
2. 删除重复的"数据分析图表"（保留第一个）
3. 删除重复的"原始费用明细"（保留第二个）
4. 日期格式改为 MM/DD，去掉时间
5. 去掉"折算日元(JPY)"和"折算人民币(CNY)"列
6. 分类列放在金额后面，描述去掉"(CN)"
7. 分类加框并显示不同颜色
8. 对齐方式：日期/描述左对齐，金额右对齐，分类居中
9. 日期和金额列增加排序功能
"""

import re
import pandas as pd

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ========== 1. 找到所有重复区域 ==========
# 找到"旅游费用明细与结算" section 的起始和结束位置
section_start = content.find('<!-- ======= 旅游费用明细与结算 ======= -->')
section_end = content.find('<!-- ==================== ECHARTS 图表脚本 ==================== -->')

print(f"费用明细 section: {section_start} -> {section_end}")

# 在这个 section 内，找到所有重复的内容
section_content = content[section_start:section_end]

# 找到"费用汇总"的第二个出现位置
first_fee_summary = section_content.find('费用汇总')
second_fee_summary = section_content.find('费用汇总', first_fee_summary + 1)
print(f"费用汇总: 第1次={first_fee_summary}, 第2次={second_fee_summary}")

# 找到"数据分析图表"的第二个出现位置
first_chart = section_content.find('数据分析图表')
second_chart = section_content.find('数据分析图表', first_chart + 1)
print(f"数据分析图表: 第1次={first_chart}, 第2次={second_chart}")

# 找到"原始费用明细"的第一个和第二个出现位置
first_table = section_content.find('原始费用明细')
second_table = section_content.find('原始费用明细', first_table + 1)
print(f"原始费用明细: 第1次={first_table}, 第2次={second_table}")

# ========== 2. 删除第二个"费用汇总" ==========
# 第二个费用汇总是从第二个"费用汇总"文本开始到下一个 section 之前
# 找到第二个"费用汇总"所在的 day-card 的开始
second_summary_start = section_content.find('<div class="day-card reveal reveal-delay-4" style="padding: 1.5rem;">', 
                                             second_fee_summary - 200)
# 找到这个 day-card 的结束（下一个 day-card 或 section 结束）
next_section_after_summary = section_content.find('<div class="day-card reveal reveal-delay-5"', second_summary_start)
if next_section_after_summary == -1:
    next_section_after_summary = section_content.find('<!-- 数据图表区 -->', second_summary_start)

print(f"第二个费用汇总: start={second_summary_start}, end={next_section_after_summary}")

# 删除第二个费用汇总
section_content = section_content[:second_summary_start] + section_content[next_section_after_summary:]

# 重新计算位置
first_chart = section_content.find('数据分析图表')
second_chart = section_content.find('数据分析图表', first_chart + 1)
print(f"删除后 数据分析图表: 第1次={first_chart}, 第2次={second_chart}")

# ========== 3. 删除第二个"数据分析图表" ==========
# 找到第二个"数据分析图表"所在的 day-card
second_chart_start = section_content.find('<div class="day-card reveal reveal-delay-5" style="padding: 1.5rem;">',
                                           second_chart - 200)
next_section_after_chart = section_content.find('<div class="day-card reveal reveal-delay-6"', second_chart_start)
if next_section_after_chart == -1:
    next_section_after_chart = section_content.find('<!-- 原始明细表 -->', second_chart_start)

print(f"第二个数据分析图表: start={second_chart_start}, end={next_section_after_chart}")

section_content = section_content[:second_chart_start] + section_content[next_section_after_chart:]

# 重新计算
first_table = section_content.find('原始费用明细')
second_table = section_content.find('原始费用明细', first_table + 1)
print(f"删除后 原始费用明细: 第1次={first_table}, 第2次={second_table}")

# ========== 4. 删除第一个"原始费用明细" ==========
# 找到第一个原始费用明细所在的 day-card
first_table_start = section_content.find('<div class="day-card reveal reveal-delay-6"', first_table - 200)
# 找到第二个原始费用明细的 day-card 开始
second_table_start = section_content.find('<div class="day-card reveal reveal-delay-6"', first_table_start + 1)
if second_table_start == -1:
    second_table_start = section_content.find('<!-- 原始明细表 -->', first_table_start + 1)

print(f"第一个原始费用明细: start={first_table_start}, end={second_table_start}")

section_content = section_content[:first_table_start] + section_content[second_table_start:]

# ========== 5. 重新读取 Excel 数据生成新的表格 ==========
excel_path = r"C:\AI\VS Code\Cline Study\51-travel-2026\旅游费用明细.xlsx"
df = pd.read_excel(excel_path, engine='openpyxl')

JPY_TO_CNY = 0.04347
CNY_TO_JPY = 23.004

amount_col = '金额'
currency_col = '币种'
date_col = '日期'
category_col = '分类'
item_col = '描述(CN)'

df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce')

# 格式化日期 - 去掉时间，只保留 MM/DD
df['日期_格式化'] = pd.to_datetime(df[date_col]).dt.strftime('%m/%d')

# 分类颜色映射
category_colors = {
    '餐饮': '#F8A5B8',
    '交通': '#667eea',
    '门票': '#D4A574',
    '祈福': '#43e97b',
}

# 生成新的表格 HTML - 列顺序：日期 | 描述 | 金额 | 分类
html_table_rows = ""
for _, row in df.iterrows():
    cat = str(row.get(category_col, ''))
    cat_color = category_colors.get(cat, '#94a3b8')
    amt = row[amount_col]
    
    html_table_rows += "<tr>"
    # 日期 - 左对齐
    html_table_rows += f'<td style="text-align:left; white-space:nowrap;">{row["日期_格式化"]}</td>'
    # 描述 - 左对齐，去掉(CN)
    desc = str(row.get(item_col, '')).replace('(CN)', '').strip()
    html_table_rows += f'<td style="text-align:left;">{desc}</td>'
    # 金额 - 右对齐
    html_table_rows += f'<td style="text-align:right; font-family:monospace; white-space:nowrap;">{amt:,.2f}</td>'
    # 分类 - 居中，带颜色框
    html_table_rows += f'<td style="text-align:center;"><span class="cat-badge" style="display:inline-block; padding:2px 10px; border-radius:12px; border:1.5px solid {cat_color}; color:{cat_color}; font-size:0.8rem; font-weight:500;">{cat}</span></td>'
    html_table_rows += "</tr>\n"

# 生成表头
html_table_header = """<tr>
                            <th class="sortable" data-col="date" style="text-align:left; cursor:pointer; white-space:nowrap;">日期 <i class="fa-solid fa-sort" style="font-size:0.7rem; opacity:0.5;"></i></th>
                            <th style="text-align:left;">描述</th>
                            <th class="sortable" data-col="amount" style="text-align:right; cursor:pointer; white-space:nowrap;">金额 <i class="fa-solid fa-sort" style="font-size:0.7rem; opacity:0.5;"></i></th>
                            <th style="text-align:center;">分类</th>
                        </tr>"""

# ========== 6. 替换表格内容 ==========
# 找到表格的 thead 和 tbody
table_start = section_content.find('<table')
table_end = section_content.find('</table>', table_start) + len('</table>')

old_table = section_content[table_start:table_end]

new_table = f"""<table style="width:100%; border-collapse:collapse; font-size:0.85rem;" id="expenseTable">
                    <thead>
                        {html_table_header}
                    </thead>
                    <tbody>
                        {html_table_rows}
                    </tbody>
                </table>"""

section_content = section_content[:table_start] + new_table + section_content[table_end:]

# ========== 7. 添加排序功能的 JavaScript ==========
sort_script = """
    <!-- ==================== 表格排序脚本 ==================== -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var table = document.getElementById('expenseTable');
            if (!table) return;
            
            var headers = table.querySelectorAll('.sortable');
            var tbody = table.querySelector('tbody');
            
            headers.forEach(function(header) {
                header.addEventListener('click', function() {
                    var col = this.getAttribute('data-col');
                    var rows = Array.from(tbody.querySelectorAll('tr'));
                    var isAsc = this.classList.contains('sort-asc');
                    
                    // 重置所有排序图标
                    headers.forEach(function(h) {
                        h.classList.remove('sort-asc', 'sort-desc');
                        var icon = h.querySelector('.fa-sort, .fa-sort-up, .fa-sort-down');
                        if (icon) {
                            icon.className = 'fa-solid fa-sort';
                            icon.style.opacity = '0.5';
                        }
                    });
                    
                    // 设置当前排序方向
                    var newDir = isAsc ? 'desc' : 'asc';
                    this.classList.add(newDir === 'asc' ? 'sort-asc' : 'sort-desc');
                    var icon = this.querySelector('.fa-sort, .fa-sort-up, .fa-sort-down');
                    if (icon) {
                        icon.className = 'fa-solid fa-sort-' + (newDir === 'asc' ? 'up' : 'down');
                        icon.style.opacity = '1';
                    }
                    
                    rows.sort(function(a, b) {
                        var aVal, bVal;
                        var aCell = a.querySelectorAll('td')[col === 'date' ? 0 : 2];
                        var bCell = b.querySelectorAll('td')[col === 'date' ? 0 : 2];
                        
                        if (col === 'date') {
                            // 按日期排序 (MM/DD)
                            aVal = aCell.textContent.trim();
                            bVal = bCell.textContent.trim();
                            var aParts = aVal.split('/');
                            var bParts = bVal.split('/');
                            aVal = parseInt(aParts[0]) * 100 + parseInt(aParts[1]);
                            bVal = parseInt(bParts[0]) * 100 + parseInt(bParts[1]);
                        } else {
                            // 按金额排序
                            aVal = parseFloat(aCell.textContent.replace(/,/g, '').trim()) || 0;
                            bVal = parseFloat(bCell.textContent.replace(/,/g, '').trim()) || 0;
                        }
                        
                        if (newDir === 'asc') {
                            return aVal > bVal ? 1 : -1;
                        } else {
                            return aVal < bVal ? 1 : -1;
                        }
                    });
                    
                    // 重新排列行
                    rows.forEach(function(row) {
                        tbody.appendChild(row);
                    });
                });
            });
        });
    </script>
"""

# 在 </body> 之前插入排序脚本
body_end = section_content.rfind('</body>')
if body_end == -1:
    body_end = section_content.rfind('</html>')

# 更新 content
new_content = content[:section_start] + section_content + content[section_end:]

# 在 </body> 前插入排序脚本
final_body_end = new_content.rfind('</body>')
final_content = new_content[:final_body_end] + sort_script + new_content[final_body_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("\n✅ 修改完成！")

# 验证
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print(f"费用汇总出现次数: {c.count('费用汇总')}")
print(f"数据分析图表出现次数: {c.count('数据分析图表')}")
print(f"原始费用明细出现次数: {c.count('原始费用明细')}")
print(f"包含排序脚本: {'sortable' in c}")
print(f"包含 cat-badge: {'cat-badge' in c}")
print(f"日期格式 MM/DD: {'04/01' in c or '04/02' in c}")
print(f"不包含 (CN): {'(CN)' not in c}")
print(f"不包含 折算日元: {'折算日元' not in c}")
print(f"不包含 折算人民币: {'折算人民币' not in c}")
