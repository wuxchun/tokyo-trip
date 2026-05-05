#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理文件末尾的空字符和多余空行"""

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 删除末尾的空字符
c = c.rstrip('\x00')
# 确保末尾只有一个换行
c = c.rstrip('\n') + '\n'

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"清理完成，文件大小: {len(c)} 字符")
print(f"最后一行: {repr(c[-50:])}")
