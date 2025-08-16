from collections import namedtuple
from collections import deque
from collections import defaultdict
from collections import OrderedDict
from collections import ChainMap
import os, argparse
from collections import Counter

Point = namedtuple('Point',['x', 'y'])  #Point类
p = Point(1, 2)
print(p.x, p.y) #可以直接引用
print( isinstance(p, Point))

q = deque(['a', 'b', 'c'])  #double ended queue
q.append('x')
q.appendleft('y')
print(list(q))

dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'
print(dd['key1'])
print(dd['key2'])
print(dd)   #defaultdict(<function <lambda> at 0x000001B5F0480A60>, {'key1': 'abc', 'key2': 'N/A'})
#在上面的示例中，defaultdict的输入是访问一个键，输出是返回对应的值或默认值，返回值是defaultdict对象本身

d = dict([('a', 1), ('b', 2), ('c', 3)])
print(d)
od = OrderedDict(d)
print(od)  # OrderedDict的Key是有序的
od = OrderedDict()
od['x'] = 4
od['z'] = 6
od['y'] = 5
print(od)
print(list(od.keys()))

#用OrderedDict实现一个FIFO的Dict类
class LastUpdatedOrderedDict(OrderedDict):
    
    def __init__(self, capacity):
        super(LastUpdatedOrderedDict, self).__init__()  #继承了父类的__init__
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self._capacity:
            last = self.popitem(last=False) #其中规定last =False为从开头移除，last= True为从结尾移除
            print('remove:', last)
        if containsKey:
            del self[key]
            print('set:', (key, value))
        else:
            print('add:', (key, value))
        OrderedDict.__setitem__(self, key, value)
# 创建一个容量为3的LastUpdatedOrderedDict对象
my_dict = LastUpdatedOrderedDict(3)
# 添加键值对
my_dict['a'] = 1
my_dict['b'] = 2
my_dict['c'] = 3
my_dict['d'] = 4  # 超出容量，会移除最早添加的键值对
# 输出字典内容
print(my_dict)

#ChainMap实现参数的优先级查找
# 构造缺省（默认）参数:
defaults = {
    'color': 'red',
    'user': 'guest'
}
# 构造命令行参数:
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user')
parser.add_argument('-c', '--color')
namespace = parser.parse_args() #调用parse_args()方法解析命令行参数，并将解析后的结果存储在namespace对象中
command_line_args = { k: v for k, v in vars(namespace).items() if v }
# 组合成ChainMap:
combined = ChainMap(command_line_args, os.environ, defaults)
#没有任何参数的时候打印出默认参数，同时传入命令行参数和环境变量，命令行参数的优先级较高
# 打印参数:
print('color=%s' % combined['color'])
print('user=%s' % combined['user'])

#Counter一个简单计数器
c = Counter()
for ch in 'programming':
    c[ch] = c[ch] + 1
print(c)
#Counter是dict的一个子类，上面的结果可以看到每个字符出现的次数