import sys, os
import json

d = dict(name = 'Bob', age = 20, score = 88)
e = {"name":'Tom', "age": 30, "score":99}
a = json.dumps(e)
print(a)
b = json.loads(a)
print(b)
#json为""，dictory为''或""

class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score
s = Student('Bob', 20, 88)

js = json.dumps(s, default = lambda obj: obj.__dict__)
print(js)
ds = json.loads(js) #先将javascript object notation转换成dictory格式
print(ds)
cs = Student(ds['name'], ds['age'], ds['score'])
print(cs)
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])
print(json.loads(js, object_hook = dict2student))