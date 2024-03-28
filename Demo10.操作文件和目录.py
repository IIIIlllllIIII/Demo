import os

# 获取操作系统的名称
os.name

print(os.path.abspath('.'))  # 获取当前工作目录的绝对路径

# 下面的代码块是关于文件路径操作的示例，但被注释掉了
#os.path.join('C:/Users/rog/Desktop/Demo','Test1')  # 拼接两个路径
#os.mkdir('C:/Users/rog/Desktop/Demo/Test1.txt')  # 创建目录(directory)
#os.rmdir('C:/Users/rog/Desktop/Demo/Test1')  # 删除目录
#os.rename('Test1.txt', 'test1.py')  # 重命名文件
#os.remove('test1.py')  # 删除文件
#print(os.path.splitext('C:/User/rog/Desktop/Demo2.py'))  # 分离文件名和扩展名

# 列出当前目录下的所有文件和目录名
a = [x for x in os.listdir('.')]
print(a)