# Flask框架
from flask import Flask
from flask import request

app = Flask(__name__)   # 创建一个Flask应用实例

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'

@app.route('/signin', methods=['GET'])
def signin_form():
    # 其中form标签标示表单 action='/signin'标示要提交的地址URL，method属性标示请求方式，GET表示浏览器发送GET请求，POST表示浏览器发送POST请求
    # <p>为paragraph标签，表示段落；input标签表示输入框，type属性表示输入框的类型，password表示密码框；
    return '''<form action="/signin" method="post">
              <p><input name="username"></p>
              <p><input name="password" type="password"></p>
              <p><button type="submit">Sign In</button></p>
              </form>'''
              
# 浏览器发送POST请求时，表单数据封装在flask框架的request.form中，如果要获取表单数据，可以request.form['name']获取
@app.route('/signin', methods=['POST'])
def signin():
    if request.form['username']=='admin' and request.form['password']=='password':
        return '<h3>Hello, admin!</h3>'
    return '<h3>Bad username or password.</h3>'

if __name__ == '__main__':
    app.run(port= 8000) # 通过run()传递port参数，指定端口号8000