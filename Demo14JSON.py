import json

d = dict(name = 'Bob', age = 20, score = 88)
e = {"name":'Tom', "age": 30, "score":99}
a = json.dumps(e)
print(a)
b = json.loads(a)
print(b)