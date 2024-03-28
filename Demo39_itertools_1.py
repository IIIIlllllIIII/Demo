import itertools

natuals = itertools.count(1, 2)     #2为可选参数，间隔为2
for n in natuals:
    print(n)
    if n >20:
        break
    
count = 0
for n in itertools.cycle([1,2,3]):   #cycle的参数为序列
    print(n)
    count += 1
    if count >= 9:
        break

for n in itertools.repeat('A', 3):  
    print(n)
    
for n in itertools.combinations([1, 2, 3, 4], 2):  #返回可迭代对象中所有长度为2的组合
    print(n)        #这里的n输出的是tuple
print(type(itertools.combinations([1, 2, 3, 4], 2)))

na = itertools.count(1)
ns = itertools.takewhile(lambda x: x<10, na)    #这里当判断条件为False的时候从后面的iterator获取的元素直接抛弃不加入队列
print(type(ns))
print(list(ns))

for n in itertools.chain('ABC', 'XYZ'):     #chain链子，串联成一个更大的迭代器
    print(n)

#itertools.gruopby将迭代器中相邻的重复元素放到一起
for key, value in itertools.groupby('AAABBCCCCD'):
    print(key, list(value))
#itertools.groupby只能将连续重复的元素分组在一起，如果要根据其他条件进行分组，需要先对可迭代对象进行排序。
data = [('apple', 'fruit'), ('banana', 'fruit'), ('carrot', 'vegetable'), ('tomato', 'fruit'), ('potato', 'vegetable')]
sorted_data = sorted(data, key=lambda x: x[1])      # 排序
result = itertools.groupby(sorted_data, key=lambda x: x[1])     # 使用groupby函数将元素分组，根据元组的第二个元素进行分组
for key, group in result:
    print(key, list(group))


#作业：计算圆周率公式
def pi(N):
    odd = itertools.count(1, 2)
    sum = 0
    count = 0
    for n in odd:
        sum += ((-1)**count)*4/n
        count += 1
        if count >= N:
            break
    return sum
# 测试:
print(pi(1))
print(pi(10))
print(pi(100))
print(pi(1000))
print(pi(10000))
assert 3.04 < pi(10) < 3.05
assert 3.13 < pi(100) < 3.14
assert 3.140 < pi(1000) < 3.141
assert 3.1414 < pi(10000) < 3.1415
print('ok')