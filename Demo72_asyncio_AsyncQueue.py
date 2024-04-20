# asyncqueue: 基于异步和协程的队列生产者和消费者示例

import asyncio
import itertools as it
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
    for _ in it.repeat(None, n):
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
        q.task_done()

# 主协程：初始化队列，创建生产者和消费者协程，并管理它们的执行
async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    # 创建生产者任务
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    # 创建消费者任务
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
    
    # 等待所有生产者完成
    await asyncio.gather(*producers)
    # 等待消费者处理完所有元素
    await q.join()
    # 取消消费者任务
    for c in consumers:
        c.cancel()

# 通过命令行参数指定生产者和消费者数量，运行主协程
if __name__ == '__main__':
    import argparse
    random.seed(444)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", '--nprod', type= int, default= 5)
    parser.add_argument("-c", '--ncon', type= int, default= 10)
    ns = parser.parse_args()
    start = time.perf_counter()
    asyncio.run(main(**ns.__dict__))
    elapsed = time.perf_counter() - start
    print(f"Program finished in {elapsed:.5f} seconds.")