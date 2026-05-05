"""
旅游费用明细数据处理脚本
功能：
1. 读取 Excel 数据
2. 汇率换算（1 JPY = 0.04347 CNY）
3. 金额汇总与分摊结算
4. 生成 ECharts 图表 HTML 代码
5. 输出用于追加到 index.html 的 HTML 片段
"""

import openpyxl
import json
from datetime import datetime

# ========== 配置 ==========
EXCEL_FILE = '旅游费用明细.xlsx'
JPY_TO_CNY = 0.04347  # 1 JPY = 0.04347 CNY
CNY_TO_JPY = 23.004   # 1 CNY = 23.004 JPY

# ========== 读取 Excel ==========
wb = openpyxl.load_workbook(EXCEL_FILE)
ws = wb['Sheet1']

records = []
for row in ws.iter_rows(min_row=2, values_only=True):
    date_val, desc_jp, desc_cn, currency, amount_val, category = row
    if date_val is None or amount_val is None or str(amount_val).strip() == '':
        continue
    
    # 处理日期
    if isinstance(date_val, datetime):
        date_str = date_val.strftime('%Y-%m-%d')
    else:
        date_str = str(date_val)
    
    # 处理金额（可能包含公式如 =1800+1500+1350）
    amount_str = str(amount_val).strip()
    if amount_str.startswith('='):
        # 解析公式，如 =1800+1500+1350
        expr = amount_str[1:]  # 去掉等号
        parts = expr.split('+')
        amount = sum(float(p.strip()) for p in parts if p.strip())
    else:
        amount = float(amount_str)
    
    currency = str(currency).strip() if currency else 'JPY'
    category = str(category).strip() if category else '其他'
    desc_cn = str(desc_cn).strip() if desc_cn else ''
    
    records.append({
        'date': date_str,
        'desc_jp': str(desc_jp).strip() if desc_jp else '',
        'desc_cn': desc_cn,
        'currency': currency,
        'amount': amount,
        'category': category
    })

print(f"共读取 {len(records)} 条费用记录\n")

# ========== 汇率换算 ==========
for r in records:
    if r['currency'] == 'JPY':
        r['amount_jpy'] = r['amount']
        r['amount_cny'] = round(r['amount'] * JPY_TO_CNY, 2)
    else:  # CNY
        r['amount_cny'] = r['amount']
        r['amount_jpy'] = round(r['amount'] * CNY_TO_JPY, 2)

# ========== 打印明细 ==========
print(f"{'日期':<12} {'描述':<20} {'币种':<6} {'原金额':<10} {'JPY折算':<12} {'CNY折算':<12} {'分类':<8}")
print("=" * 80)
for r in records:
    print(f"{r['date']:<12} {r['desc_cn']:<20} {r['currency']:<6} {r['amount']:<10.2f} {r['amount_jpy']:<12.2f} {r['amount_cny']:<12.2f} {r['category']:<8}")

# ========== 金额汇总 ==========
total_jpy = sum(r['amount_jpy'] for r in records)
total_cny = sum(r['amount_cny'] for r in records)
print(f"\n{'='*80}")
print(f"日元总费用（全部折算为 JPY）: ¥{total_jpy:,.2f}")
print(f"人民币总费用（全部折算为 CNY）: ¥{total_cny:,.2f}")

# ========== 分摊结算 ==========
relative_pay = total_cny * (2 / 3)
print(f"\n亲戚需转账金额（人民币总费用 * 2/3）: ¥{relative_pay:,.2f}")

# ========== 按日期统计 ==========
from collections import defaultdict
daily_total = defaultdict(float)
for r in records:
    daily_total[r['date']] += r['amount_jpy']

print(f"\n每日费用（JPY）:")
for d in sorted(daily_total.keys()):
    print(f"  {d}: ¥{daily_total[d]:,.2f}")

# ========== 按分类统计 ==========
category_total = defaultdict(float)
for r in records:
    category_total[r['category']] += r['amount_jpy']

print(f"\n分类费用（JPY）:")
for c in sorted(category_total.keys()):
    print(f"  {c}: ¥{category_total[c]:,.2f}")

# ========== 生成 ECharts 图表 HTML ==========

# 准备数据
dates_sorted = sorted(daily_total.keys())
daily_values = [round(daily_total[d], 2) for d in dates_sorted]

cats_sorted = sorted(category_total.keys(), key=lambda x: category_total[x], reverse=True)
cat_values = [round(category_total[c], 2) for c in cats_sorted]

# 生成图表 HTML
chart_html = f"""
<!-- ==================== 旅游费用明细与结算 ==================== -->
<section aria-label="旅游费用明细与结算" style="margin-top: 3rem;">
    <h2 class="section-title reveal reveal-delay-5">
        <i class="fa-solid fa-calculator"></i> 旅游费用明细与结算
    </h2>

    <!-- 费用结算区 -->
    <div class="day-card reveal reveal-delay-5" style="padding: 1.5rem;">
        <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; justify-content: center; text-align: center;">
            <div style="flex: 1; min-width: 160px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; padding: 1.2rem; color: #fff;">
                <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 0.3rem;">日元总计</div>
                <div style="font-size: 1.8rem; font-weight: 900;">¥{total_jpy:,.0f}</div>
                <div style="font-size: 0.75rem; opacity: 0.7;">JPY</div>
            </div>
            <div style="flex: 1; min-width: 160px; background: linear-gradient(135deg, #F8A5B8 0%, #E8829A 100%); border-radius: 16px; padding: 1.2rem; color: #fff;">
                <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 0.3rem;">人民币总计</div>
                <div style="font-size: 1.8rem; font-weight: 900;">¥{total_cny:,.2f}</div>
                <div style="font-size: 0.75rem; opacity: 0.7;">CNY</div>
            </div>
            <div style="flex: 1.5; min-width: 200px; background: linear-gradient(135deg, #FF6B6B 0%, #EE5A24 100%); border-radius: 16px; padding: 1.2rem; color: #fff; box-shadow: 0 4px 20px rgba(238, 90, 36, 0.3);">
                <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 0.3rem;">💰 亲戚需转账金额</div>
                <div style="font-size: 2rem; font-weight: 900;">¥{relative_pay:,.2f}</div>
                <div style="font-size: 0.75rem; opacity: 0.7;">CNY（总费用 × 2/3）</div>
            </div>
        </div>
        <div style="margin-top: 1rem; padding: 0.8rem; background: #FFF8E1; border-radius: 12px; font-size: 0.85rem; color: #795548; text-align: center;">
            <i class="fa-solid fa-info-circle"></i> 汇率：1 JPY = {JPY_TO_CNY} CNY（2026年5月2日） · 费用由我统一垫付，共3人分摊
        </div>
    </div>

    <!-- 图表区 -->
    <div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin-top: 1.5rem;">
        <!-- 柱状图 -->
        <div class="day-card reveal reveal-delay-5" style="flex: 1 1 400px; padding: 1rem;">
            <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--charcoal);">
                <i class="fa-solid fa-chart-bar" style="color: var(--sakura);"></i> 每日费用柱状图
            </h3>
            <div id="dailyChart" style="width: 100%; height: 350px;"></div>
        </div>
        <!-- 玫瑰图 -->
        <div class="day-card reveal reveal-delay-5" style="flex: 1 1 400px; padding: 1rem;">
            <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--charcoal);">
                <i class="fa-solid fa-chart-pie" style="color: var(--sakura);"></i> 分类费用占比（南丁格尔玫瑰图）
            </h3>
            <div id="categoryChart" style="width: 100%; height: 350px;"></div>
        </div>
    </div>

    <!-- 原始明细表 -->
    <div class="day-card reveal reveal-delay-5" style="padding: 1rem; margin-top: 1.5rem; overflow-x: auto;">
        <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.8rem; color: var(--charcoal);">
            <i class="fa-solid fa-table" style="color: var(--sakura);"></i> 费用明细表
        </h3>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
            <thead>
                <tr style="background: var(--sakura-light);">
                    <th style="padding: 0.6rem 0.8rem; text-align: left; border-bottom: 2px solid var(--sakura);">日期</th>
                    <th style="padding: 0.6rem 0.8rem; text-align: left; border-bottom: 2px solid var(--sakura);">描述</th>
                    <th style="padding: 0.6rem 0.8rem; text-align: left; border-bottom: 2px solid var(--sakura);">币种</th>
                    <th style="padding: 0.6rem 0.8rem; text-align: right; border-bottom: 2px solid var(--sakura);">金额</th>
                    <th style="padding: 0.6rem 0.8rem; text-align: right; border-bottom: 2px solid var(--sakura);">折算 JPY</th>
                    <th style="padding: 0.6rem 0.8rem; text-align: right; border-bottom: 2px solid var(--sakura);">折算 CNY</th>
                    <th style="padding: 0.6rem 0.8rem; text-align: left; border-bottom: 2px solid var(--sakura);">分类</th>
                </tr>
            </thead>
            <tbody>
"""

for r in records:
    chart_html += f"""                <tr style="border-bottom: 1px solid var(--light-gray);">
                    <td style="padding: 0.5rem 0.8rem;">{r['date']}</td>
                    <td style="padding: 0.5rem 0.8rem;">{r['desc_cn']}</td>
                    <td style="padding: 0.5rem 0.8rem;">{r['currency']}</td>
                    <td style="padding: 0.5rem 0.8rem; text-align: right;">{r['amount']:,.0f}</td>
                    <td style="padding: 0.5rem 0.8rem; text-align: right;">¥{r['amount_jpy']:,.2f}</td>
                    <td style="padding: 0.5rem 0.8rem; text-align: right;">¥{r['amount_cny']:,.2f}</td>
                    <td style="padding: 0.5rem 0.8rem;"><span class="badge" style="background: var(--sakura-light); color: #B05A6F;">{r['category']}</span></td>
                </tr>
"""

chart_html += f"""                <tr style="background: #FFF8E1; font-weight: 700;">
                    <td colspan="4" style="padding: 0.6rem 0.8rem; text-align: right;">合计</td>
                    <td style="padding: 0.6rem 0.8rem; text-align: right; color: #E8829A;">¥{total_jpy:,.2f}</td>
                    <td style="padding: 0.6rem 0.8rem; text-align: right; color: #E8829A;">¥{total_cny:,.2f}</td>
                    <td style="padding: 0.6rem 0.8rem;"></td>
                </tr>
            </tbody>
        </table>
    </div>
</section>

<!-- ECharts 图表脚本 -->
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {{
    // ===== 每日费用柱状图 =====
    var dailyChart = echarts.init(document.getElementById('dailyChart'));
    var dailyOption = {{
        tooltip: {{
            trigger: 'axis',
            formatter: function(params) {{
                var p = params[0];
                return '<strong>' + p.axisValue + '</strong><br/>总费用：¥' + p.value.toLocaleString() + ' JPY';
            }}
        }},
        grid: {{
            left: '8%',
            right: '5%',
            bottom: '12%',
            top: '8%',
            containLabel: true
        }},
        xAxis: {{
            type: 'category',
            data: {json.dumps(dates_sorted, ensure_ascii=False)},
            axisLabel: {{
                fontSize: 12,
                fontWeight: 'bold',
                color: '#6B5B4F'
            }},
            axisLine: {{ lineStyle: {{ color: '#E8E0D8' }} }}
        }},
        yAxis: {{
            type: 'value',
            name: '日元 (JPY)',
            nameTextStyle: {{ color: '#6B5B4F', fontSize: 11 }},
            axisLabel: {{
                formatter: function(v) {{ return '¥' + v.toLocaleString(); }},
                color: '#6B5B4F'
            }},
            splitLine: {{ lineStyle: {{ color: '#F0EBE5', type: 'dashed' }} }}
        }},
        series: [{{
            type: 'bar',
            data: {json.dumps(daily_values)},
            itemStyle: {{
                borderRadius: [6, 6, 0, 0],
                color: {{
                    type: 'linear',
                    x: 0, y: 0, x2: 0, y2: 1,
                    colorStops: [
                        {{ offset: 0, color: '#F8A5B8' }},
                        {{ offset: 1, color: '#E8829A' }}
                    ]
                }}
            }},
            emphasis: {{
                itemStyle: {{
                    color: '#D4627A'
                }}
            }},
            label: {{
                show: true,
                position: 'top',
                formatter: function(p) {{ return '¥' + p.value.toLocaleString(); }},
                fontSize: 10,
                color: '#6B5B4F'
            }}
        }}]
    }};
    dailyChart.setOption(dailyOption);
    window.addEventListener('resize', function() {{ dailyChart.resize(); }});

    // ===== 分类费用玫瑰图 =====
    var categoryChart = echarts.init(document.getElementById('categoryChart'));
    var categoryOption = {{
        tooltip: {{
            trigger: 'item',
            formatter: function(params) {{
                return '<strong>' + params.name + '</strong><br/>' +
                       '费用：¥' + params.value.toLocaleString() + ' JPY<br/>' +
                       '占比：' + params.percent + '%';
            }}
        }},
        series: [{{
            type: 'pie',
            radius: ['20%', '75%'],
            center: ['50%', '50%'],
            roseType: 'area',
            itemStyle: {{
                borderRadius: 4,
                borderColor: '#fff',
                borderWidth: 2
            }},
            label: {{
                formatter: function(p) {{ return p.name + '\\n¥' + p.value.toLocaleString(); }},
                fontSize: 11,
                fontWeight: 'bold',
                color: '#2D2D2D'
            }},
            labelLine: {{
                lineStyle: {{ color: '#E8E0D8' }}
            }},
            data: [
"""

for i, (cat, val) in enumerate(zip(cats_sorted, cat_values)):
    comma = ',' if i < len(cats_sorted) - 1 else ''
    chart_html += f"""                {{ value: {val}, name: '{cat}' }}{comma}
"""

chart_html += f"""            ],
            color: ['#F8A5B8', '#667eea', '#FFD93D', '#6BCB77', '#FF6B6B', '#A66CFF', '#FF9F43']
        }}]
    }};
    categoryChart.setOption(categoryOption);
    window.addEventListener('resize', function() {{ categoryChart.resize(); }});
}});
</script>
"""

# 输出到文件
with open('expense_section.html', 'w', encoding='utf-8') as f:
    f.write(chart_html)

print(f"\n\nHTML 片段已生成到 expense_section.html")
print(f"总计 {len(records)} 条记录")
print(f"日期范围: {records[0]['date']} ~ {records[-1]['date']}")
