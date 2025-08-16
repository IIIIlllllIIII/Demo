import psutil # pip install psutil
import time
import os
import sys

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1, percpu= True)    #interval间隔单位秒
    print("CPU usage: ", cpu_usage)
    return cpu_usage
def get_ram_usage():
    ram_usage = psutil.virtual_memory().percent
    print("RAM usage: ", ram_usage)
    return ram_usage
def get_disk_usage():
    disk_usage = psutil.disk_usage('/').percent
    print("Disk usage: ", disk_usage)
    return disk_usage
def get_network_usage():
    network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    print("Network usage: ", network_usage)

if __name__ == '__main__':
    while True:
        print(psutil.cpu_count(logical= False))
        print(psutil.cpu_times())
        print(psutil.virtual_memory())
        print('Disk_partitions:', psutil.disk_partitions())
        get_cpu_usage()
        get_ram_usage()
        get_disk_usage()
        get_network_usage()
        #print('Net_IO_counters: ', psutil.net_io_counters())    #获取网络读写字节/包的个数
        #print('Net_If_addrs: ', psutil.net_if_addrs())     #Interface（接口）获取网络接口和IP地址信息
        #print('Net_If_stats: ' ,psutil.net_if_stats())  #statistic网络接口统计信息
        #print('Net_connections: ', psutil.net_connections())    #获取网络接口和网络连接信息
        print('PIDs: ', psutil.pids())
        p = psutil.Process(3472)
        #print(p.name(), p.exe(), p.cwd(), p.cmdline(), p.ppid(), p.children(), p.status(), p.username(), p.create_time(), p.cpu_times(), p.memory_info(), p.open_files(), p.connections(), p.num_threads(), p.environ())    # p.terminal()只在类unix上可用
        
        
        time.sleep(1)

