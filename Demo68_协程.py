# 异步IO，协程

# 定义消费者
def consumer():
    
    r = ''
    while True:
        n = yield r # yield r 表示暂停，等待下一次调用，r是上一次调用的返回值，下面的c.send(n)将传入的值赋给n
        if not n:
            return
        print('[CONSUMER] Consuming %s...' %n)
        r = '200 OK'

# 定义生产者
def produce(c):
    
    c.send(None)    # 启动生成器，send(None)表示第一次执行生成器传入的参数为None，协程通过send进行通信
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' %n)
        r = c.send(n)   # 这里的r是consumer的返回值，如果consumer没有返回值，r就是None
        print('[PRODUCER] Consumer return: %s' %r)
    c.close()   # 关闭协程

c = consumer()
produce(c)