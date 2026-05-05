#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确修复 index.html 中的费用明细部分。
基于实际文件结构：
- 第一个 section: 费用汇总 + 数据分析图表 + </section>
- 第二个 section: 费用汇总 + 数据分析图表 + 原始明细表

保留：第一个 section 的费用汇总 + 数据分析图表 + 第二个 section 的原始明细表
"""

import pandas as pd

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ========== 找到两个 section 的边界 ==========
first_section_start = content.find('<!-- ======= 旅游费用明细与结算 ======= -->')
second_section_start = content.find('<!-- ======= 旅游费用明细与结算 ======= -->', first_section_start + 1)

# 第一个 section 结束
first_section_end = content.find('</section>', first_section_start)
# 第二个 section 结束
second_section_end = content.find('</section>', second_section_start)

print(f"第一个 section: {first_section_start} -> {first_section_end}")
print(f"第二个 section: {second_section_start} -> {second_section_end}")

# ========== 提取需要保留的部分 ==========
# 第一个 section 的内容
first_section = content[first_section_start:first_section_end + len('</section>')]

# 第二个 section 中的原始明细表部分
second_section = content[second_section_start:second_section_end + len('</section>')]
table_start_in_second = second_section.find('<!-- 原始明细表 -->')
table_part = second_section[table_start_in_second:]

print(f"\n第一个 section 长度: {len(first_section)}")
print(f"原始明细表部分长度: {len(table_part)}")

# ========== 构建新的 section ==========
# 从第一个 section 中去掉 </section> 标签
first_section_body = first_section[:first_section.rfind('</section>')]

new_section = first_section_body + "\n\n" + table_part

# ========== 替换到 content 中 ==========
# 找到 ECHARTS 脚本的开始位置
echarts_start = content.find('<!-- ==================== ECHARTS 图表脚本 ==================== -->')

# 从 first_section_start 到 echarts_start 之间的内容全部替换为 new_section
new_content = content[:first_section_start] + new_section + content[echarts_start:]

# ========== 重新读取 Excel 数据生成新表格 ==========
excel_path = r"C:\AI\VS Code\Cline Study\51-travel-2026\旅游费用明细.xlsx"
df = pd.read_excel(excel_path, engine='openpyxl')

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

new_table = f"""<table style="width:100%; border-collapse:collapse; font-size:0.85rem;" id="expenseTable">
                    <thead>
                        {html_table_header}
                    </thead>
                    <tbody>
                        {html_table_rows}
                    </tbody>
                </table>"""

# 替换表格
table_start = new_content.find('<table', first_section_start)
table_end = new_content.find('</table>', table_start) + len('</table>')
new_content = new_content[:table_start] + new_table + new_content[table_end:]

# ========== 添加排序脚本 ==========
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

body_end = new_content.rfind('</body>')
final_content = new_content[:body_end] + sort_script + new_content[body_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("\n✅ 修改完成！")

# 验证
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print(f"费用汇总出现次数: {c.count('费用汇总')}")
print(f"数据分析图表出现次数: {c.count('数据分析图表')}")
print(f"原始费用明细出现次数: {c.count('原始费用明细')}")
print(f"旅游费用明细与结算出现次数: {c.count('旅游费用明细与结算')}")
print(f"包含排序脚本: {'sortable' in c}")
print(f"包含 cat-badge: {'cat-badge' in c}")
print(f"日期格式 MM/DD: {'04/01' in c or '04/02' in c}")
print(f"不包含 (CN): {'(CN)' not in c}")
print(f"不包含 折算日元: {'折算日元' not in c}")
print(f"不包含 折算人民币: {'折算人民币' not in c}")
print(f"包含 人均花费: {'人均花费' in c}")
