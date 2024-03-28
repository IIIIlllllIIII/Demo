import random, time, queue  # 导入需要使用的模块：random、time、queue
from multiprocessing.managers import BaseManager  # 从 multiprocessing.managers 模块导入 BaseManager 类

# 创建任务队列和结果队列
task_queue = queue.Queue()
result_queue = queue.Queue()

# 定义 QueueManager 类，用于管理任务队列和结果队列
class QueueManager(BaseManager):
    pass

# 定义获取任务队列的函数
def get_task_queue():
    return task_queue

# 定义获取结果队列的函数
def get_result_queue():
    return result_queue

# 将获取任务队列和结果队列的函数注册到 QueueManager 类中
QueueManager.register('get_task_queue', callable=get_task_queue)
QueueManager.register('get_result_queue', callable=get_result_queue)

if __name__ == '__main__':
    # 创建 QueueManager 实例，指定地址和认证密钥
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
    # 启动 QueueManager 实例
    manager.start()
    # 获取任务队列和结果队列
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    # 将任务放入任务队列
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)

    print('Try get results.')
    # 从结果队列中获取结果
    for i in range(10):
        r = result.get(timeout=10000)
        print('Result: %s' % r)

    # 关闭 QueueManager 实例
    manager.shutdown()
    print('Master exit.')
