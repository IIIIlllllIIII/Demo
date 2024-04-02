import os
#print(os.environ)
print(os.path.abspath('.'))     #获取当前工作目录等于os.getcwd()
print(os.getcwd())
print(os.path.abspath(__file__))    #获取当前脚本绝对路径