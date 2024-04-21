# asyncqueue: 基于异步和协程的队列生产者和消费者示例

import asyncio
import itertools as it  # 迭代器模块
import os
import random
import time

# 创建一个指定大小的随机字符串
async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()

# 模拟带有随机睡眠时间的操作
async def randsleep(caller= None) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f'{caller} sleeping for {i} seconds.')
    await asyncio.sleep(i)

# 生产者协程：随机生成元素并加入队列
async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):    # 生成None，重复n次，'_'表示忽略，意思是只做循环次数控制
        await randsleep(caller= f"Producer {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Producer {name} added <{i}> to queue.")

# 消费者协程：从队列获取元素并处理
async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller= f'Consumer {name}')
        i, t = await q.get()
        now = time.perf_counter()
        print(f'Consumer {name} got element <{i}>'
              f' in {now-t:0.5f}'
              )
        q.task_done()   #  标记任务完成，队列长度减一

# 主协程：初始化队列，创建生产者和消费者协程，并管理它们的执行
async def main(nprod: int, ncon: int):
    q = asyncio.Queue() # 创建协程中使用的队列
    
    # 创建生产者任务
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    # 创建消费者任务
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
    #这里用asyncio.creat_task创建任务而不是用asyncio.gather是因为它允许你在某些任务还在运行的同时进行其他操作，在任务运行时保持更多的控制或灵活性。
    # 比如下面的c.cancel()和q.jion()就是对这些协程进行单独操作
    
    # 等待所有生产者完成
    await asyncio.gather(*producers)
    # 等待消费者处理完所有元素
    await q.join()
    # 取消消费者任务，生产者自动取消而消费者是个while循环需要主动取消
    for c in consumers:
        c.cancel()

# 通过命令行参数指定生产者和消费者数量，运行主协程
if __name__ == '__main__':
    import argparse    # 命令行解析
    random.seed(444)
    parser = argparse.ArgumentParser() # 创建一个解析器
    parser.add_argument("-p", '--nprod', type= int, default= 5) # 生产者数量
    parser.add_argument("-c", '--ncon', type= int, default= 10) # 消费者数量
    ns = parser.parse_args()    # 解析命令行参数
    start = time.perf_counter() # 获取当前时间
    
    asyncio.run(main(**ns.__dict__))    # 运行main函数
    
    elapsed = time.perf_counter() - start   # 计算程序运行时间
    print(f"Program finished in {elapsed:.5f} seconds.") # 打印程序运行时间