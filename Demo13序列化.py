import pickle
import os, sys
d = dict(name = 'Bob', age = 20, score = 88)
a = pickle.dumps(d)
b = pickle.loads(a)
print(b)