#TCP编程
import socket, ssl

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #AF_INET(Address Family Internet Protocol)代表ipv4，SOCK_STREAM代表tcp。
s = ssl.wrap_socket(s1)    #ssl.wrap_socket()(wrap包裹)函数可以将普通的socket包装成SSL安全套接字，实现对数据的加密和身份验证。
s.connect(('www.sina.com.cn', 443))  #因为是ssl链接，所以要连接到新浪的433端口，这里是一个tuple

s.send(b'GET / HTTP/1.1\r\nHost:www.sina.com.cn\r\nConnection:close\r\n\r\n')   #发送数据
#接收数据
buffer = []
while True:
    #每次最多接收1K字节：
    d = s.recv(1024)    #d是字节类型
    if d:
        buffer.append(d)    #将收到的数据放到buffer列表中
    else:
        break
data = b''.join(buffer)     #这里的buffer是一个byte类型的数组，所以用b''.join()将它转换为一个byte类型的字符串
#关闭连接
s.close()

header, html = data.split(b'\r\n\r\n', 1)   #将HTTP的请求头(header)和请求体(html)分割，只分割一次。
print(header.decode('utf-8'))
with open('sina.html', 'wb') as f:  #将html写入文件
    #f.write(data)
    f.write(html)