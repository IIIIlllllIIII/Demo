#POP3(Post Office Protocol version 3邮局协议3)接收邮件
# +- MIMEBase
#    +- MIMEMultipart
#    +- MIMENonMultipart
#       +- MIMEMessage
#       +- MIMEText
#       +- MIMEImage
import poplib
#解析邮件所需要的模块
from email.parser import Parser
from email.utils import parseaddr
from email.header import decode_header
import types

def print_info(msg, indent= 0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            #get(header, default)是EmailMessage对象的一个方法，尝试从邮件对象 msg 中获取名为 header 的头部字段的值，并且如果找不到这个头部字段，则返回一个空字符串 '' 作为默认值。
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' %(name, addr)
            print('%s%s: %s' %('  '* indent, header, value))
    if (msg.is_multipart()):    #is_multipart()判断是否是MIMEMultipart类型
        #get_payload()获取邮件的MIME内容。是email库中的EmailMessage类的方法，当 msg 是一个非多部分(non-multipart)邮件时，get_payload() 返回的是邮件的主体内容当msg是一个多部分(Multipart)邮件时，返回一个包含多个子消息体的列表。
        parts = msg.get_payload() 
        for n, part in enumerate(parts): #enumerate()函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在，for循环当中。
            print('%spart %s' %('  '* indent, n))
            print('%s--------------------' %('  '* indent))
            print_info(part, indent+1)
    else:
        content_type = msg.get_content_type()   #get_contert_type()用于获取邮件的MIME类型。
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)     #这里设置decode=True表示解码，从Base64转换
            charset = guess_charset(msg)    #这里目的是将base64编码的邮件正文，转换成Unicode。
            if charset:
                content = content.decode(charset)   #decode()方法用于解码字符串，这里的content是邮件的文本内容，decode()方法用于解码字符串，这里的content是邮件的文本内容，decode()方法用于解码字符串，这里的content是邮件的文本内容，decode()方法用于解码字符串，这里的content是邮件的文本内容，decode()方法用于解码字符串，这里的content是邮件的文本内容，decode()方法用于解码字符串，这里的content是邮件的文本内容，decode()方法用于解码字符串，这里的content是邮件的文本内容，decode()方法用于解码字符串，这里的content是邮件的文本内容
            print('%sText: %s' %('  '* indent, content))
        else:
            print('%sAttachment: %s' %('  '* indent, content_type))

def decode_str(s):
    value, charset = decode_header(s)[0]    # 解码decode_header()函数，返回一个列表，列表的每一项都是一个元组第元组的一个元素是解码后的字符串，第二个元素是编码格式
    if charset:
        value = value.decode(charset)
    return value 

def guess_charset(msg):
    charset = msg.get_charset()     #
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

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
        resp, mails, octets = server.list()     #这里resp是状态码，mails是邮件列表，octets是邮件占用的空间
        print(resp)
        print(mails)
        index = input('请输入要查询第几封邮件：')  # 获取最新一封邮件的下标:
        resp, lines, octets = server.retr(index) #retr(retrieve检索)这里的index是邮件索引号，例如1表示第1封邮件
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        # 稍后解析出邮件:
        msg = Parser().parsestr(msg_content)    #返回解析后的邮件对象
        
        return msg  #在try中返回msg
    
    except Exception as e:
        print('邮件接收失败：', e)
    finally:
        server.quit()

        
if __name__ =='__main__':
    print_info(main())
    
