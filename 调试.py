# import os
# #print(os.environ)
# print(os.path.abspath('.'))     #获取当前工作目录等于os.getcwd()
# print(os.getcwd())
# print(os.path.abspath(__file__))    #获取当前脚本绝对路径


class A:
    def __init__(self):
        print("Init of class A")

class B(A):
    def __init__(self):
        super(B, self).__init__()  # 调用父类 A 的构造方法
        print("Init of class B")

class C(A):
    def __init__(self):
        super(C, self).__init__()  # 调用父类 A 的构造方法
        print("Init of class C")

class D(B, C):
    def __init__(self):
        super(D, self).__init__()  # 调用父类 B 的构造方法
        print("Init of class D")

# 创建子类 D 的实例
d = D()
print(D.__mro__)