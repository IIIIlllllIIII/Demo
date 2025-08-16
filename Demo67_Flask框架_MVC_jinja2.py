# MVC(Model-View-Controller 模型-视图-控制器) 通过MVC实现Python代码和HTML代码的分离
# Flask 框架，jinja2 模板引擎
# jinja2模板中用{{...}}标示一个需要替换的变量，用{%...%}标示指令
 
from flask import Flask, request, render_template   # render_template 渲染模板

app = Flask(__name__, template_folder= './HTML_Templates')  # 创建Flask应用，(template模板)通过template_folder参数指定模板文件夹

@app.route('/', methods= ['GET', 'POST'])
def home():
    return render_template('home.html') # 渲染home.html模板

@app.route('/signin', methods= ['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods= ['POST'])
def signin():   
    username = request.form['username']
    password = request.form['password']
    
    if username=='admin' and password=='password':
        return render_template('signin-ok.html', username= username)    #username参数传递给模板，渲染signin-ok.html模板
    return render_template('form.html', message= 'Bad username or password', username= username)

if __name__ == '__main__':
    app.run()   # 运行Flask应用