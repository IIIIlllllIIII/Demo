# WSGI(Web Server Gateway Interface)_server

from wsgiref.simple_server import make_server   #wsgiref(Web Server Gateway Interface Reference Library, WSGI参考库)
from Demo64_WSGI_Function import application    # 从当前文件夹下的Demo64_WSGI_Function.py文件导入application函数

# 创建服务器，IP地址为空，端口为8000，处理函数是application
httpd = make_server('', 8000, application)
print('Server HTTP on port 8000...')
# 启动服务器，开始监听请求
httpd.serve_forever()
