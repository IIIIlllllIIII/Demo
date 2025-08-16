# asyncio
import asyncio
import time

async def count():  # 定义一个协程，async修饰的函数就是协程
    
    print("One")
    await asyncio.sleep(1)  # 挂起协程，等待1秒
    print('Two')

async def main():
    
    await asyncio.gather(count(), count(), count())     # 协程的集合，等待协程执行完成
    
if __name__ == '__main__':
    
    s = time.perf_counter() # 获取当前时间
    asyncio.run(main())     # 运行协程
    elapsed = time.perf_counter() - s
    print(f'{__file__} executed in {elapsed}')