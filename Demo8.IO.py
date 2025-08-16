import os
import sys
from io import StringIO

# 使用StringIO创建一个内存中的文件对象f，并向f中写入字符串
f = StringIO()
f.write('Hello')  # 写入"Hello"
f.write(' ')      # 写入一个空格
f.write('World!') # 写入"World!"
print(f.getvalue()) # 打印f中目前的所有内容