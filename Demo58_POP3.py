#POP3(Post Office Protocol version 3邮局协议3)接收邮件
import poplib
#解析邮件所需要的模块
from email.parser import Parser
from email.utils import parseaddr
from email.header import decode_header

import types

# 定义一个函数，用于给POP3_SSL实例动态添加login方法
# def apply_login_method_to_instance(server):
#     def login(email, password):
#         server.user(email)
#         server.pass_(password)
#     # 直接将login方法绑定到实例上
#     server.login = login

# 定义一个函数，用于动态地给POP3_SSL实例添加login方法，之后再创建的实例也可以用
def apply_login_method(instance):
    def login(self, email, password):
        self.user(email)
        self.pass_(password)

    # 将login方法动态绑定到实例上
    instance.login = login.__get__(instance)

def get_psword():
    pswd_path = r'C:\Users\rog\Desktop\Demo/QQMail_SMTP_pswd.txt'
    with open(pswd_path, 'r', errors='ignore') as f:
        pswd = f.read().strip('\n')
    return pswd

def main():
    email = '1025321720@qq.com'
    print(f'Connecting to {email} ...')
    password = get_psword()
    pop3_server = 'pop.qq.com'
    #pop3_port = 995 这里不用传入端口号，自动传入
    
    try:
        server = poplib.POP3_SSL(pop3_server)
        server.set_debuglevel(0)
        # 初始方法
        # server.user(email)
        # server.pass_(password)
        
        # 应用函数，给server实例添加login方法
        apply_login_method(server)
        # 现在可以使用login方法了
        server.login(email, password)
        
        # stat()返回邮件数量和占用空间:
        print('Messages: %s. Size: %s' % server.stat())
        resp, mails, octets = server.list()
        print(mails)
        index = input('请输入要查询第几封邮件：')  # 获取最新一封邮件的下标:
        resp, lines, octets = server.retr(index) #retr(retrieve检索)这里的index是邮件索引号，例如1表示第1封邮件
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        print(msg_content)
        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)
        
    except Exception as e:
        print('邮件接收失败：', e)
    finally:
        server.quit()
        
if __name__ =='__main__':
    main()