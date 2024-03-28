import socket
import concurrent.futures
import multiprocessing
import threading

def handle_client(sock, addr):
    with sock:
        try:
            print('Accept new connection from %s:%s...' % addr)
            sock.send(b'Welcome!')
            while True:
                data = sock.recv(1024)
                if not data or data.decode('utf-8') == 'exit':
                    break
                sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
        except Exception as e:
            print(f'Error handling client {addr}: {e}')
        finally:
            print('Connection from %s:%s closed.' % addr)

def start_server(shutdown_flag):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('127.0.0.1', 9999))
        server_socket.listen(5)
        print('Waiting for connection...')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while not shutdown_flag.value:
                server_socket.settimeout(1.0)  # 设置超时时间
                try:
                    client_socket, addr = server_socket.accept()
                except socket.timeout:
                    continue    #continue直接跳过之后的语句重新开始while循环
                print('Connected with %s:%s' % addr)
                executor.submit(handle_client, client_socket, addr)
        print('Server closed.')

def read_input(shutdown_flag):
    input_text = ''
    while input_text != 'exit':
        input_text = input('Enter "exit" to close the server: \n')
    shutdown_flag.value = True

if __name__ == '__main__':
    shutdown_flag = multiprocessing.Value('b', False)   #这个Value是一个共享变量，用来通知server进程退出

    server_process = multiprocessing.Process(target=start_server, args=(shutdown_flag,))
    server_process.start()
    #这里input在windows下在子进程里运行会报错EOFError，所以用线程来处理。input()在主进程中执行，然后通过管道等输入子进程中
    input_thread = threading.Thread(target=read_input, args=(shutdown_flag,))
    input_thread.start()

    server_process.join()
    input_thread.join()