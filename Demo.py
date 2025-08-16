#! -*- coding: utf-8 -*-
import sys
import os
import math
import types
import psutil
from collections.abc import Iterable
from functools import reduce
import functools
import time
from types import MethodType
from enum import Enum, unique

class Student(object):
    __slots__ = ('name', '__gender', 'age')
    def __init__(self, name, gender):
        self.name = name
        self.set_gender(gender)

    def set_gender(self, gender):
        if gender != 'male' and gender != "female":
            raise ValueError('Input gender!')
        else:
         self.__gender = gender
    def get_gender(self):
        return self.__gender
s = Student('Tom', 'male')
s.age = 12
print(f'{s.name}\'s age is {s.age} years old.')

class Screen(object):
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError('Input invalid.')
        self._width = value
    
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError('Input invalid.')
        self._height = value
    
    @property
    def resolution(self):
        return self._height * self._width

# 测试:
s = Screen()
s.width = 1024
s.height = 768
print('resolution =', s.resolution)
if s.resolution == 786432:
    print('测试通过!')
else:
    print('测试失败!')

class FibSeq:
    """基于下标的斐波那契序列视图，限定长度 max_n（项数），无内部可变状态。"""
    def __init__(self, max_n):
        if max_n < 0:
            raise ValueError("max_n must be non-negative")
        self._max_n = max_n

    def __len__(self):
        return self._max_n

    @staticmethod
    def _nth(n: int) -> int:
        # O(n) 逐步推进；若需要更快可换成 O(log n) 快速倍增法
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    def __getitem__(self, key):
        if isinstance(key, int):
            # 支持负索引
            if key < 0:
                key += self._max_n
            if not (0 <= key < self._max_n):
                raise IndexError("index out of range")
            return self._nth(key)

        if isinstance(key, slice):
            start, stop, step = key.indices(self._max_n)
            if step == 0:
                raise ValueError("slice step cannot be zero")
            # 高效切片：从起点一次推进到终点（而不是每个索引都从 0 开算）
            res = []
            if step > 0 and start < stop or step < 0 and start > stop:
                # 先把 F_start 算出来
                a, b = 0, 1
                for _ in range(start):
                    a, b = b, a + b
                # 现在 a = F_start, b = F_{start+1}
                i = start
                need = []
                # 收集需要的下标（考虑负步长时 Python 的标准行为）
                while (step > 0 and i < stop) or (step < 0 and i > stop):
                    need.append(i)
                    i += step
                if not need:
                    return []
                # 若 step=1，线性推进；若 |step|>1，可批量“跳步”推进（这里给出简单版本）
                cur_idx = start
                cur_a, cur_b = a, b
                for t in need:
                    # 从 cur_idx 推到 t
                    while cur_idx < t:
                        cur_a, cur_b = cur_b, cur_a + cur_b
                        cur_idx += 1
                    while cur_idx > t:
                        # 反向回退可用恒等式：F_{k-1} = F_{k+1} - F_k
                        cur_a, cur_b = (cur_b - cur_a), cur_a
                        cur_idx -= 1
                    res.append(cur_a)
            return res

        raise TypeError("Invalid argument type")

    def __iter__(self):
        for i in range(1, self._max_n):
            yield self[i]

for i in FibSeq(5):
    print(i)

print(FibSeq(60)[1:50:5])
def fn(self, name='world'): # 先定义函数
    print('Hello, %s.' % name)

Hello = type('Hello', (object,), dict(hello=fn)) # 创建Hello class
print(Hello.hello)
Hello().hello()

