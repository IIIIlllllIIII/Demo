# 
import asyncio
import random

c = (
    '\033[0m',
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)   #其中\033[表示用ANSI转译码表示文本颜色的方法，0表示重置颜色，36表示青色，91表示红色，35表示洋红

async def makerandom(idx: int, threshold: int = 6) -> int:
    # 输出初始状态，这里c[]表示颜色，引用上面的c中的颜色
    print(c[idx + 1] + f'Initiated makerandom{[idx]}. Need more than {threshold}.')
    i = random.randint(0, 10)   # 生成随机数
    # 当随机数小于阈值，则进入循环
    while i <= threshold:
        print(c[idx + 1] + f'makerandom{[idx]} == {i} too low; retrying.')
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    
    print(c[idx + 1] + f'---> Finished makerandom{[idx]} == {i}'+ c[0])
    return i

async def main():
    # 其中'*'是解包操作符，将可迭代对象解包成单独的元素
    res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(3)))
    return res

if __name__ == '__main__':
    
    random.seed(444)    # 设置随机数种子，使每次输出的数相同
    r1, r2, r3 = asyncio.run(main()) # 使用asyncio.run()函数执行协程
    
    print()
    print(f'r1: {r1}, r2: {r2}, r3: {r3}')