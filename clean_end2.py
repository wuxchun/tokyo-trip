#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""彻底清理文件末尾的异常字符"""

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 删除所有空字符
c = c.replace('\x00', '')
# 删除反引号
c = c.replace('`', '')
# 确保末尾干净
c = c.rstrip('\n') + '\n'

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print(f"清理完成，文件大小: {len(c)} 字符")
print(f"最后100字符: {repr(c[-100:])}")
print(f"包含空字符: {'\x00' in c}")
print(f"包含反引号: {'`' in c}")
