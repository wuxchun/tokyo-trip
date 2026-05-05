with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()
print('文件大小:', len(c), '字符')
print('包含旅游费用明细:', '旅游费用明细与结算' in c)
print('包含ECharts:', 'echarts' in c)
print('包含</html>:', '</html>' in c)
print('包含</body>:', '</body>' in c)
print('包含</main>:', '</main>' in c)
# 检查最后500字符
print('\n--- 文件末尾 ---')
print(c[-500:])
