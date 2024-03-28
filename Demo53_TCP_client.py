#TCP client
import socket

name = [b'Michael', b'Tracy', b'Sarah']
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #实例化socket对象
s.connect(('127.0.0.1', 9999))  #连接服务器
#接收欢迎消息
print(s.recv(1024).decode('utf-8'))
for data in name:
    s.send(data)    #发送数据
    print(s.recv(128).decode('utf-8'))
s.send(b'exit')
s.close
