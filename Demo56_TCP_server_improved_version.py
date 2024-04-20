import socket
import concurrent.futures
import multiprocessing
import threading

def handle_client(sock, addr):
    """
    处理客户端连接和通信。
    
    参数:
    - sock: 客户端的socket连接。
    - addr: 客户端的地址元组。
    """
    with sock:
        try:
            print('Accept new connection from %s:%s...' % addr)
            sock.send(b'Welcome!')  # 发送欢迎信息
            while True:
                data = sock.recv(1024)  # 接收客户端数据
                if not data or data.decode('utf-8') == 'exit':
                    break
                sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))  # 回复客户端
        except Exception as e:
            print(f'Error handling client {addr}: {e}')
        finally:
            print('Connection from %s:%s closed.' % addr)

def start_server(shutdown_flag):
    """
    启动服务器，监听客户端连接，并处理客户端请求。
    
    参数:
    - shutdown_flag: 一个共享变量，用于控制服务器的关闭。
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('127.0.0.1', 9999))  # 绑定监听地址和端口
        server_socket.listen(5)  # 监听模式，设置最大连接数
        print('Waiting for connection...')
        with concurrent.futures.ThreadPoolExecutor() as executor:  # 使用线程池执行器来异步处理客户端连接
            while not shutdown_flag.value:
                server_socket.settimeout(1.0)  # 设置socket超时时间，避免阻塞
                try:
                    client_socket, addr = server_socket.accept()  # 接受客户端连接
                except socket.timeout:
                    continue    # 超时则继续等待连接
                print('Connected with %s:%s' % addr)
                executor.submit(handle_client, client_socket, addr)  # 提交客户端处理任务
        print('Server closed.')

def read_input(shutdown_flag):
    """
    从用户输入读取命令，用于控制服务器的关闭。
    
    参数:
    - shutdown_flag: 一个共享变量，用于控制服务器的关闭。
    """
    input_text = ''
    while input_text != 'exit':
        input_text = input('Enter "exit" to close the server: \n')
    shutdown_flag.value = True

if __name__ == '__main__':
    # 第一个参数指定共享值的数据类型，这里用'b'表示单字节bool值；第二个参数设定初始值
    shutdown_flag = multiprocessing.Value('b', False)   # 创建一个共享变量，用于控制服务器的关闭

    server_process = multiprocessing.Process(target=start_server, args=(shutdown_flag,))
    server_process.start()
    # 由于在Windows下子进程中运行input()会报错，因此使用线程来处理输入
    input_thread = threading.Thread(target=read_input, args=(shutdown_flag,))
    input_thread.start()

    server_process.join()  # 等待服务器进程结束
    input_thread.join()  # 等待输入线程结束