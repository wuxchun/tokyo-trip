with open('index.html', 'rb') as f:
    h = f.read(4)
print('BOM hex:', h.hex())
if h[:2] == b'\xff\xfe':
    print('编码: UTF-16 LE with BOM')
elif h[:3] == b'\xef\xbb\xbf':
    print('编码: UTF-8 with BOM')
else:
    print('编码: 其他')

with open('index.html', 'r', encoding='utf-16') as f:
    c = f.read()
print('文件大小:', len(c), '字符')
print('前100字符:', c[:100])
print()
print('=== 内容验证 ===')
print('亲戚需转账金额:', '亲戚需转账金额' in c)
print('dailyChart:', 'dailyChart' in c)
print('categoryChart:', 'categoryChart' in c)
print('echarts.min.js:', 'echarts.min.js' in c)
print('费用汇总:', '费用汇总' in c)
print('原始费用明细:', '原始费用明细' in c)
print('涉谷Sky:', '涉谷Sky' in c)
print('烤肉:', '烤肉' in c)
print('</html>:', '</html>' in c)
print('旅游费用明细与结算:', '旅游费用明细与结算' in c)
print('¥96,090:', '¥96,090' in c)
print('¥4,177.05:', '¥4,177.05' in c)
print('¥2,784.70:', '¥2,784.70' in c)
