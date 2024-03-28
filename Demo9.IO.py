import os
import sys
from io import StringIO
from io import BytesIO

# 使用StringIO模拟文件，读取其中的内容并逐行打印
f = StringIO('Hello!\nHi!\nGoodbye!')
while True:
    s = f.readline()  # 读取一行
    if s == '':  # 如果读取的行为空，则退出循环
        break
    print(s.strip())  # 打印去除首尾空白的行
print(f.getvalue())  # 打印整个字符串的内容

# 使用BytesIO处理二进制数据，写入中文并打印
g = BytesIO()
g.write('中文'.encode('Utf-8'))  # 将中文字符串编码为Utf-8并写入BytesIO
print(g.getvalue())  # 打印BytesIO中存储的二进制数据的解码结果