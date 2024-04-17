# WSGI(Web Server Gateway Interface服务网关接口)

def application(environ, start_response):   #application函数的返回值是HTTP Body，HTTP的头文件是通过start_response函数返回
    start_response('200 OK', [('Content-Type', 'text/html')]) 
    # 第二个元素是一个元组，用来设置响应头，如需添加更多内容见下例：
    # [('Content-Type', 'text/html'), 
    #   ('Set-Cookie', 'session_id=123456789; Expires=Wed, 21 Oct 2024 07:28:00 GMT; Path=/'), 
    #   ('Set-Cookie', 'user_id=987654321; Expires=Wed, 21 Oct 2024 07:28:00 GMT; Path=/')]
    # body = 
    body ='''
            <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>示例网页</title>
    </head>
    <body>
        <header>
            <h1>Hello, %s!</h1>
            <h1 onclick="change()">欢迎访问示例网页</h1>
        </header>
        <main>
            <p>这是一个简单的示例网页，用于演示基本的 HTML 结构。</p>
            <p>HTML（Hypertext Markup Language）是用于创建网页的标记语言。</p>
            <p>您可以学习更多关于 HTML 的知识，例如：</p>
            <ul>
                <li><a href="https://developer.mozilla.org/zh-CN/docs/Web/HTML">HTML 教程</a></li>
                <li><a href="https://www.w3schools.com/html/">W3Schools HTML 教程</a></li>
            </ul>
        </main>
        <footer>
            <p>© 2024 示例网页</p>
        </footer>
    </body>
    </html>
    '''  %(environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]   #application 函数的返回值是一个字节串列表，每个字节串表示 HTTP 响应主体的一部分。
