# 链接协程，协程对象是可等待的，因此另一个协程可以awiat它，这样两个协程就可以同时运行了。
# 因此可以将程序分解成为更小的、可管理的、可回收的协程。
import asyncio
import random
import time

# 部分1：定义了两个异步函数part1和part2，它们模拟了带有延迟的处理过程。
async def part1(n: int) -> int:
    """
    执行第一个异步操作，模拟处理任务。
    
    参数:
    n (int): 任务的标识符。
    
    返回:
    int: 完成后返回的结果字符串。
    """
    i = random.randint(0, 10)
    print(f"part1({n}) sleeping for {i} seconds.")
    await asyncio.sleep(i)
    result = f'result{n} - 1'
    print(f'Returing part1({n}) == {result}')
    return result

async def part2(n: int) -> int:
    """
    执行第二个异步操作，模拟处理任务。
    
    参数:
    n (int): 任务的标识符。
    
    返回:
    int: 完成后返回的结果字符串。
    """
    i = random.randint(0, 10)
    print(f"part2({n}) sleeping for {i} seconds.")
    await asyncio.sleep(i)
    result = f'result{n} - 2'
    print(f'Returing part2({n}) == {result}')
    return result

# 部分2：定义了一个异步函数chain，它顺序地调用part1和part2，并测量总耗时。
async def chain(n: int) -> None:
    """
    顺序执行part1和part2，并测量执行时间。
    
    参数:
    n (int): 任务的标识符。
    """
    start = time.perf_counter()
    p1 = await part1(n)
    p2 = await part2(n)
    end = time.perf_counter() - start
    print(f'-->Chained result{n} => {p2} (took {end:0.2f} seconds).')

# 部分3：定义了主异步函数main，用于启动所有任务。
async def main(*args):
    """
    并行执行chain函数。
    
    参数:
    *args: 传递给chain函数的参数列表。
    """
    await asyncio.gather(*(chain(n) for n in args))

# 部分4：程序入口，根据命令行参数决定执行哪些任务，并测量程序总耗时。
if __name__ == "__main__":
    import sys
    random.seed(444)
    args = [1, 2, 3] if len(sys.argv) == 1 else map(int, sys.argv[1:])  # 获取命令行参数，其中1表示从第二个参数开始，即第一个参数是程序名
    start = time.perf_counter()
    asyncio.run(main(*args))
    end = time.perf_counter() - start
    print(f'Program finished in {end:0.2f} seconds.')