import Demo
import sys

print(sys.path)

f = Demo.fast(11, 22)
s = Demo.slow(11, 22, 33)
if f != 33:
    print('测试失败!')
elif s != 7986:
    print('测试失败!')