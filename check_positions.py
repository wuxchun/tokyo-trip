#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查旅游费用明细与结算的所有出现位置"""

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

positions = []
pos = -1
while True:
    pos = c.find('旅游费用明细与结算', pos + 1)
    if pos == -1:
        break
    positions.append(pos)

for i, p in enumerate(positions):
    context = c[max(0,p-80):p+120]
    print(f"\n--- 位置 {i+1} (offset={p}) ---")
    print(repr(context[:200]))
