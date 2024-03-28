import contextlib

#with方法先实例化一个上下文管理器类q，再进行操作
class Query_1(object):
    def __init__(self, name):
        self.name =name
    def __enter__(self):
        print('begin')
        return self    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print('Error')
        else:
            print('End')
    def query(self):
        print('Query info about %s...' %self.name) 
with Query_1('Bob') as q:
    q.query()

#用@contextmanager上下文管理器修饰使用with 
from contextlib import contextmanager

class Query_2(object):
    def __init__(self, name):
        self.name = name
    
    def query(self):
        print('Query info about %s...' %self.name)  
@contextmanager     #这个contextmanager修饰器接受一个generator迭代器
def create_query(name):
    print('Begin')  #只有第一行在__enter__里执行
    q = Query_2(name)
    yield q     #使用yield将q返回给with
    print('End')    #yield语句之后的代码会在退出上下文时执行，相当于__exit__中的代码。
with create_query('Bob') as q:
    q.query()
    
@contextmanager     #通过contextmanager编写generator
def tag(name):
    print('<%s>' %name)     #__enter__
    yield   #控制权交给with，执行with中的语句
    print('<%s>' %name)     #__exit__
with tag('h1'):
    print('hello')
    print('world')
 
from contextlib import closing
from urllib.request import urlopen
#自己定义closing
@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()   #这里的close()方法是thing对象自带的
with closing(urlopen('https://www.python.org')) as page:
    for line in page:
        print(line)
