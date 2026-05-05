with open('index.html', 'r', encoding='utf-16') as f:
    c = f.read()

# 搜索各种关键词
keywords = ['亲戚需转账', '续转账', '转账', '需支付', 'relative_pay', '2/3', '总费用 × 2/3']
for kw in keywords:
    idx = c.find(kw)
    if idx >= 0:
        print(f'找到 "{kw}" 位置: {idx}')
        print(f'  周围: {c[max(0,idx-20):idx+40]}')
    else:
        print(f'未找到 "{kw}"')

# 检查费用汇总区域
idx = c.find('费用汇总')
if idx >= 0:
    print(f'\n费用汇总区域:')
    print(c[idx:idx+800])
