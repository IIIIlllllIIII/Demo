from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' %(name, os.getpid()))
    start = time.time()
    time.sleep(random.random()*3)
    end = time.time()
    print('Task %s run %0.2f seconds.' %(name, (end - start)))
    
if __name__ == '__main__':
    print('Parent Process %s.' %os.getpid())
    p = Pool(5) #Pool中的参数为同时运行的进程数
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')