import sys
import os
import math

import psutil
from collections.abc import Iterable
from functools import reduce



  
def make_funcs():
    funcs = []
    x = 0
    for i in range(3):
        def f():
            nonlocal x
            x = x + 1
            return x + i
        funcs.append(f)
    return funcs

f1, f2, f3 = make_funcs()
print(f1())  # 1
print(f2())  # 2
print(f3())  # 3
print(f1())  # 4



def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n

def _not_divisible(n):
    return lambda x: x % n > 0

def primes():
    yield 2
    it = _odd_iter()
    while True:
        n = next(it)
        yield n
        it = filter(_not_divisible(n), it)

L = list(filter(lambda x: x % 2 == 1, range(1, 20)))
print(L)
def main():
    for n in primes():
        if n < 100:
            print(n)
        else:
            break
        
main()
