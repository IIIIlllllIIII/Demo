# TCP服务器
# 一个Socket依赖4项：服务器地址、服务器端口、客户端地址、客户端端口来唯一确定一个Socket。
# Python中Socket对象可用于两种不同的目的：1.作为服务器套接字(用于接受连接); 2.作为客户端套接字(用于发起连接)。
import socket
import threading
import time

def tcplink(sock, addr):    # 定义一个函数，用于处理客户端的连接
    sock.setblocking(True)  # 设置阻塞模式，设置为阻塞模式，表示当客户端发送数据时，服务器立即返回数据，而不是等待数据到来。
    start_time = time.time()    # 记录开始时间
    print('Accept new connection from %s:%s...' %addr)  # 打印客户端的连接信息
    sock.send(b'Welcome!')  # 这里的sock是socket的对象，所以能用sock.send()和sock.recv()
    while True:
        data = sock.recv(1024)  # 接收数据，每次1024字节
        time.sleep(1)   # 休眠1秒
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send((('Hello, %s!' %data.decode('utf-8')).encode('utf-8'))) # 向客户端发送返回信息
    sock.close()    # sock.close()调用关闭的是与客户端建立的连接套接字（socket 对象），而不是关闭服务器套接字s。
    print('Connection from %s:%s closed.' %addr)
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # 创建一个socket对象，SOCK_STREAM(Socket Stream流式套接字)表示TCP协议
    s.bind(('127.0.0.1', 9999))     # 绑定IP和端口，小于1024的端口必须使用root用户执行
    s.listen(5) # 监听端口，并设置最大连接数。
    s.setblocking(False)  # 设置为非阻塞模式，在阻塞模式下，下面的while循环会一直等待客户端的连接，直到服务器关闭。
    print('Waiting for connection...')
    start_time = time.time()
# 循环等待客户端的连接
    while True:
        try:
            sock, addr = s.accept() # 阻塞方式等待客户端的连接，返回一个包含连接套接字+客户端地址端口的元组
            print('...connected from:', addr)
            t = threading.Thread(target= tcplink, args= (sock, addr))   # 创建线程，传入参数sock和addr
            t.start()   # 启动线程
        # except BlockingIOError:   # 这里是LINUX下的异常处理
        #     pass 
        except OSError: # windows下的异常处理
            if time.time() - start_time >= 30:  # 30秒后关闭服务器
                print("Server shutting down...")
                time.sleep(5)  # 等待一段时间确保所有连接都关闭
                s.close()   # 关闭服务器
                break  # 触发异常以退出主循环
            # 这也可以用sock.settimeout(30)在阻塞式模式下设置超时时间，从阻塞开始发生的时间开始计算30秒，超过30秒raise异常socket.timeout
            else:
                pass
        except Exception as e:
            pass
    print('Server closed.')
    
if __name__ == '__main__':
    main()