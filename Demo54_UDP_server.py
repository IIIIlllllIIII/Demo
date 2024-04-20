#UDP服务器：闲置20秒后自动停止
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor   # 引入线程池
from collections import defaultdict # 引入字典

client_data = defaultdict(str)  #创建一个字典，用于存储客户端的连接信息
lock = threading.Lock() #创建一个锁
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #SOCK_DGRAM(Socket Datagram数据报)UDP模式，实例化socket
    s.bind(('127.0.0.1', 9999)) #bind the socket to the port
    print('Bind UDP on 9999')
    #用线程池处理
    executor = ThreadPoolExecutor(max_workers= 5)   #创建线程池
    s.settimeout(20)    #设置超时时间
    while True:
        try:
            #接收数据
            data, addr = s.recvfrom(1024)   #这里和TCP不同，UDP不需要建立连接，直接接收数据。用recvfrom()方法接收数据，参数为缓冲区大小。
            print('Received from %s:%s' %addr)
            executor.submit(handle_client_data, s, addr, data)  #没有显式地对其进行处理，也就是没有将其赋值给变量，那么这个Future对象就会被丢弃，不再被使用。
            # 用线程处理数据
            # t = threading.Thread(target= udplink, args=(addr, data))
            # t.start()
        except socket.timeout:    #注意这里是socket的超时错误捕获
            print('Timeout, close the UDP srever.')
            time.sleep(2)
            break
    print(client_data)
       
def handle_client_data(s, addr, data):  
    s.settimeout(20)
    try:    
        with lock:  #加锁防止多线程同时写入数据
            client_data[addr] += data.decode('utf-8')
        response =f'Hello,{client_data[addr]}!'  
        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        with lock:  #加锁防止同时调用s
            s.sendto(response.encode('utf-8'), addr) #发送数据，两个参数分别为要发送的数据和接收数据的地址。
    except Exception as s:  #捕获异常
        print(f'Error in thread: {s}')
        
if __name__ == '__main__':
    main()