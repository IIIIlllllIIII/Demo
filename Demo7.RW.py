import os
import sys
fpath = 'C:/Users/rog/Desktop/Demo/test.txt'  # 指定文件路径

# 打开文件，以追加写入模式打开，忽略所有错误
# 'a+' 模式允许读写操作，errors='ignore' 忽略编码错误
with open(fpath, 'a+', errors='ignore') as f:
    f.write('\nHello World!')  # 向文件末尾写入一行"Hello World!"
    f.seek(0)  # 将文件读取位置指针移至文件开头
    print(f.read())  # 从文件开头读取所有内容并打印