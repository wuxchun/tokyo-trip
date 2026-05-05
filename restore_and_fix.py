#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Git 中恢复正确的 UTF-8 版本 index.html，然后重新追加费用明细。
"""

import subprocess
import re
import json
import pandas as pd

# ========== 1. 从第三次提交获取正确的 UTF-8 版本 ==========
print("=== 从 Git 恢复正确的 UTF-8 版本 ===")
result = subprocess.run(['git', 'show', '3aae19c:index.html'], capture_output=True)
raw_bytes = result.stdout

# 用 UTF-8 解码
content = raw_bytes.decode('utf-8')
print(f"恢复成功！文件大小: {len(content)} 字符")

# 验证标题
title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
if title_match:
    print(f"标题: {title_match.group(1)}")

# 验证包含"东京"
print(f"包含'东京': {'东京' in content}")
print(f"包含'春季': {'春季' in content}")

# ========== 2. 读取 Excel 数据 ==========
print("\n=== 读取 Excel 数据 ===")
excel_path = r"C:\AI\VS Code\Cline Study\51-travel-2026\旅游费用明细.xlsx"
df = pd.read_excel(excel_path, engine='openpyxl')

JPY_TO_CNY = 0.04347
CNY_TO_JPY = 23.004

# 识别列
amount_col = '金额'
currency_col = '币种'
date_col = '日期'
category_col = '分类'
item_col = '描述(CN)'

# 计算
df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce')

def calc_jpy(row):
    amt = row[amount_col]
    cur = str(row.get(currency_col, 'JPY')).upper()
    if cur in ['JPY', '日元', '日币', '¥', '']:
        return amt
    else:
        return amt * CNY_TO_JPY

def calc_cny(row):
    amt = row[amount_col]
    cur = str(row.get(currency_col, 'JPY')).upper()
    if cur in ['JPY', '日元', '日币', '¥', '']:
        return amt * JPY_TO_CNY
    else:
        return amt

df['金额_JPY'] = df.apply(calc_jpy, axis=1)
df['金额_CNY'] = df.apply(calc_cny, axis=1)

total_jpy = df['金额_JPY'].sum()
total_cny = df['金额_CNY'].sum()
relative_pay = total_cny * 2 / 3
per_person_cny = total_cny / 3

print(f"日元总费用: ¥{total_jpy:,.2f} JPY")
print(f"人民币总费用: ¥{total_cny:,.2f} CNY")
print(f"亲戚需转账金额: ¥{relative_pay:,.2f} CNY")

# 按日期汇总
df['日期_格式化'] = pd.to_datetime(df[date_col]).dt.strftime('%m/%d')
daily_sum = df.groupby('日期_格式化')['金额_JPY'].sum().reset_index()
daily_sum.columns = ['日期', '总费用_JPY']

# 按类别汇总
category_sum = df.groupby(category_col)['金额_JPY'].sum().reset_index()
category_sum.columns = ['类别', '总费用_JPY']

daily_data = {
    "dates": daily_sum['日期'].tolist(),
    "values": [round(v, 2) for v in daily_sum['总费用_JPY'].tolist()]
}

category_data = {
    "names": category_sum['类别'].tolist(),
    "values": [round(v, 2) for v in category_sum['总费用_JPY'].tolist()]
}

# ========== 3. 生成 HTML 表格 ==========
table_cols = [date_col, item_col, category_col, amount_col, currency_col]
table_cols_extended = table_cols + ['金额_JPY', '金额_CNY']

category_colors = {
    '餐饮': '#F8A5B8',
    '交通': '#667eea',
    '门票': '#D4A574',
    '祈福': '#43e97b',
}

html_table_rows = ""
for _, row in df.iterrows():
    cat = str(row.get(category_col, ''))
    cat_color = category_colors.get(cat, '#94a3b8')
    html_table_rows += "<tr>"
    for col in table_cols_extended:
        val = row[col]
        if col in ['金额_JPY', '金额_CNY']:
            html_table_rows += f'<td class="text-right">¥{val:,.2f}</td>'
        elif col == amount_col:
            html_table_rows += f'<td class="text-right">{val:,.2f}</td>'
        elif col == category_col:
            html_table_rows += f'<td><span class="category-badge" style="border-color:{cat_color};color:{cat_color};">{val}</span></td>'
        else:
            html_table_rows += f'<td>{val}</td>'
    html_table_rows += "</tr>\n"

html_table_header = "<tr>"
for col in table_cols_extended:
    display_name = col
    if col == '金额_JPY':
        display_name = '折算日元(JPY)'
    elif col == '金额_CNY':
        display_name = '折算人民币(CNY)'
    html_table_header += f'<th>{display_name}</th>'
html_table_header += "</tr>"

# ========== 4. 生成要追加的 HTML 内容 ==========
append_html = f"""
    <!-- ======= 旅游费用明细与结算 ======= -->
    <section aria-label="旅游费用明细与结算" style="margin-top: 3rem;">
        <h2 class="section-title reveal reveal-delay-4">
            <i class="fa-solid fa-calculator"></i> 旅游费用明细与结算
        </h2>

        <!-- 费用结算区 -->
        <div class="day-card reveal reveal-delay-4" style="padding: 1.5rem;">
            <h3 style="font-size:1.1rem; font-weight:700; margin-bottom:1rem; color:var(--charcoal);">
                <i class="fa-solid fa-file-invoice-dollar"></i> 费用汇总
            </h3>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:1rem;">
                <div style="background:linear-gradient(135deg, #667eea, #764ba2); border-radius:12px; padding:1rem; color:#fff; text-align:center;">
                    <div style="font-size:0.85rem; opacity:0.8; margin-bottom:0.3rem;">日元总费用（汇率换算后）</div>
                    <div style="font-size:1.6rem; font-weight:700;">¥{total_jpy:,.0f}</div>
                    <div style="font-size:0.75rem; opacity:0.7;">JPY</div>
                </div>
                <div style="background:linear-gradient(135deg, #f093fb, #f5576c); border-radius:12px; padding:1rem; color:#fff; text-align:center;">
                    <div style="font-size:0.85rem; opacity:0.8; margin-bottom:0.3rem;">人民币总费用（汇率换算后）</div>
                    <div style="font-size:1.6rem; font-weight:700;">¥{total_cny:,.2f}</div>
                    <div style="font-size:0.75rem; opacity:0.7;">CNY</div>
                </div>
                <div style="background:linear-gradient(135deg, #43e97b, #38f9d7); border-radius:12px; padding:1rem; color:#1a1a2e; text-align:center; border:2px solid #f8a5b8;">
                    <div style="font-size:0.85rem; opacity:0.8; margin-bottom:0.3rem; font-weight:600;">💰 亲戚需转账金额</div>
                    <div style="font-size:1.8rem; font-weight:900; color:#e74c3c;">¥{relative_pay:,.2f}</div>
                    <div style="font-size:0.75rem; opacity:0.7;">CNY（总费用 × 2/3）</div>
                </div>
                <div style="background:linear-gradient(135deg, #ffecd2, #fcb69f); border-radius:12px; padding:1rem; color:#1a1a2e; text-align:center;">
                    <div style="font-size:0.85rem; opacity:0.8; margin-bottom:0.3rem; font-weight:600;">👤 人均花费</div>
                    <div style="font-size:1.6rem; font-weight:700; color:#8b5cf6;">¥{per_person_cny:,.2f}</div>
                    <div style="font-size:0.75rem; opacity:0.7;">CNY（总费用 ÷ 3人）</div>
                </div>
            </div>
            <div style="margin-top:0.8rem; font-size:0.8rem; color:var(--warm-gray); text-align:center;">
                汇率：1 JPY = {JPY_TO_CNY} CNY &nbsp;|&nbsp; 1 CNY = {CNY_TO_JPY} JPY &nbsp;|&nbsp; 费用由我统一垫付，共3人AA
            </div>
        </div>

        <!-- 数据图表区 -->
        <div class="day-card reveal reveal-delay-5" style="padding: 1.5rem;">
            <h3 style="font-size:1.1rem; font-weight:700; margin-bottom:1rem; color:var(--charcoal);">
                <i class="fa-solid fa-chart-bar"></i> 数据分析图表
            </h3>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
                <div id="dailyChart" style="width:100%; height:350px;"></div>
                <div id="categoryChart" style="width:100%; height:350px;"></div>
            </div>
        </div>

        <!-- 原始明细表 -->
        <div class="day-card reveal reveal-delay-6" style="padding: 0; overflow: hidden;">
            <div style="display:flex; justify-content:space-between; align-items:center; padding:16px 20px; border-bottom:1px solid #eef2f6;">
                <h3 style="font-size:14px; font-weight:600; color:#475569; margin:0;">
                    <i class="fa-solid fa-table"></i> 原始费用明细
                </h3>
                <span style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#94a3b8;">共 {len(df)} 笔记录</span>
            </div>
            <div style="overflow-x: auto;">
                <table style="width:100%; border-collapse:collapse; font-size:0.85rem;">
                    <thead>
                        {html_table_header}
                    </thead>
                    <tbody>
                        {html_table_rows}
                    </tbody>
                </table>
            </div>
        </div>
    </section>
"""

# ========== 5. 追加到 index.html ==========
# 在 </main> 之前插入
insert_pos = content.rfind('</main>')
if insert_pos == -1:
    insert_pos = content.rfind('</body>')

new_content = content[:insert_pos] + append_html + content[insert_pos:]

# 写入为 UTF-8（无 BOM）
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✅ 已成功追加费用明细到 index.html (UTF-8)")

# ========== 6. 生成 ECharts 脚本 ==========
daily_dates_json = json.dumps(daily_data['dates'])
daily_values_json = json.dumps(daily_data['values'])

category_js_data = ""
colors_list = ["#F8A5B8", "#D4A574", "#667eea", "#43e97b", "#f093fb", "#f5576c", "#ffa726", "#26c6da", "#ab47bc", "#ef5350"]
for i, (name, val) in enumerate(zip(category_data['names'], category_data['values'])):
    color = colors_list[i % len(colors_list)]
    category_js_data += f"                        {{ value: {val}, name: '{name}', itemStyle: {{ color: '{color}' }} }},\n"

echarts_script = """
    <!-- ==================== ECHARTS 图表脚本 ==================== -->
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {

            // ===== 每日费用柱状图 =====
            var dailyChart = echarts.init(document.getElementById('dailyChart'));
            var dailyOption = {
                title: {
                    text: '每日费用（JPY）',
                    left: 'center',
                    textStyle: { fontSize: 14, color: '#2D2D2D' }
                },
                tooltip: {
                    trigger: 'axis',
                    formatter: function(params) {
                        return params[0].name + '<br/>费用: ¥' + params[0].value.toLocaleString() + ' JPY';
                    }
                },
                grid: { left: '8%', right: '8%', bottom: '15%', top: '20%' },
                xAxis: {
                    type: 'category',
                    data: """ + daily_dates_json + """,
                    axisLabel: { color: '#666' }
                },
                yAxis: {
                    type: 'value',
                    name: '日元 (JPY)',
                    axisLabel: { formatter: '¥{value}' },
                    splitLine: { lineStyle: { type: 'dashed', color: '#eee' } }
                },
                series: [{
                    type: 'bar',
                    data: """ + daily_values_json + """,
                    itemStyle: {
                        borderRadius: [6, 6, 0, 0],
                        color: {
                            type: 'linear',
                            x: 0, y: 0, x2: 0, y2: 1,
                            colorStops: [
                                { offset: 0, color: '#F8A5B8' },
                                { offset: 1, color: '#E8829A' }
                            ]
                        }
                    },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: '¥{c}',
                        fontSize: 11
                    }
                }]
            };
            dailyChart.setOption(dailyOption);

            // ===== 分类费用玫瑰图 =====
            var categoryChart = echarts.init(document.getElementById('categoryChart'));
            var categoryOption = {
                title: {
                    text: '分类费用占比',
                    left: 'center',
                    textStyle: { fontSize: 14, color: '#2D2D2D' }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function(params) {
                        return params.name + '<br/>费用: ¥' + params.value.toLocaleString() + ' JPY<br/>占比: ' + params.percent.toFixed(1) + '%';
                    }
                },
                series: [{
                    type: 'pie',
                    radius: ['20%', '70%'],
                    center: ['50%', '55%'],
                    roseType: 'area',
                    itemStyle: {
                        borderRadius: 4
                    },
                    label: {
                        formatter: '{b}\\n¥{c} ({d}%)',
                        fontSize: 11
                    },
                    data: [
""" + category_js_data + """                    ]
                }]
            };
            categoryChart.setOption(categoryOption);

            // ===== 响应式 =====
            window.addEventListener('resize', function() {
                dailyChart.resize();
                categoryChart.resize();
            });

        });
    </script>
"""

# 在 </body> 之前插入 ECharts 脚本
with open('index.html', 'r', encoding='utf-8') as f:
    current_content = f.read()

insert_pos_body = current_content.rfind('</body>')
final_content = current_content[:insert_pos_body] + echarts_script + current_content[insert_pos_body:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

print(f"✅ 已成功插入 ECharts 图表脚本到 index.html")

# ========== 7. 验证 ==========
print("\n=== 验证 ===")
with open('index.html', 'rb') as f:
    raw = f.read(10)
print(f"文件前10字节: {raw.hex()}")
print(f"无 BOM: {raw[0] == 0x3c}")  # 应该是 '<' 字符

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()
print(f"文件大小: {len(c)} 字符")
print(f"标题: {re.search(r'<title>(.*?)</title>', c, re.IGNORECASE).group(1)}")
print(f"包含'东京': {'东京' in c}")
print(f"包含'春季': {'春季' in c}")
print(f"包含'亲戚需转账金额': {'亲戚需转账金额' in c}")
print(f"包含'dailyChart': {'dailyChart' in c}")
print(f"包含'categoryChart': {'categoryChart' in c}")
print(f"包含'echarts.min.js': {'echarts.min.js' in c}")
print(f"包含'</html>': {'</html>' in c}")

print(f"\n🎉 所有操作完成！")
