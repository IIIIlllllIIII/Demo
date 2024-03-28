#MUA(Mail User Agent用户邮件代理): SMTP(Simple Mail Transfer Protocol简单邮件传输协议)发送邮件
import os
import sys
import smtplib
#MIME:(Multipurpose Internet Mail Extensions多用途互联网邮件扩展)这个模块用来发送邮件的，提供了创建不同类型邮件消息的类，如文本、HTML、图像等。
from email.mime.base import MIMEBase    #MIMEbase是基于文件的工具，添加附件的类
from email.mime.text import MIMEText    #MIMEtext是文本工具
from email.mime.multipart import MIMEMultipart  #MIMEmultipart是多部分工具
from email.utils import parseaddr, formataddr   #email.utils.parseaddr用来解析邮件地址，email.utils.formataddr用来格式化邮件地址返回字符串形式，将元组返回成字符串用在msg的Header
from email.header import Header #email.header.Header用来设置邮件头
from email import encoders #email.encoders.encode_base64用来对附件进行编码

def get_psword():
    pswd_path = 'C:/Users/ROG/Desktop/Demo/QQMail_SMTP_pswd.txt'
    with open(pswd_path, 'r', errors='ignore') as f:
        pswd = f.read().strip('\n')
    return pswd

#获取符合邮件格式的收件人地址信息
def _format_addr(s):
    name, addr = parseaddr(s)
    name = Header(name,'utf-8').encode()   #这里的utf-8是编码格式，指的是输出的编码格式，而不是name的编码格式
    return formataddr((name, addr))

#获取收件人地址
def get_name(s):
    name, addr = parseaddr(s)
    name = Header(name, 'utf-8').encode()
    return name    #s.split('<')[1][:1]

#获取收件人姓名
def get_addr(s):
    name, addr = parseaddr(s)
    return addr    #s.split(' <')[0]

#message
def main():
    
    # 设置发件人、收件人、邮件主题
    sender = '明天过后 <1025321720@qq.com>'
    sender_addr = get_addr(sender)
    password = get_psword()
    recv_list = ['阿巴阿巴 <1025321720gjc@gmail.com>']
    receiver = [get_addr(s) for s in recv_list]
    smtp_server = 'smtp.qq.com'
    smtp_port = 465 #465 & 587是QQ邮箱的SMTP端口
    
    # 邮件正文是str格式
    plain = 'Hello, sendby Python...'
    content_format1 = 'plain'
    
    #邮件正文是HTML格式
    html = '<html><body><h1>Hello</h1>' + '<p><img src="cid:0"></p>'+'<p>send by <a href="http://www.python.org">Python</a>...</p>' + '</body></html>'
    content_format2 = 'html'
    
    #创建文本邮件
    msg_content_txt = MIMEText(plain, content_format1, 'utf-8') #其中plain是邮件正文的格式，utf-8是编码格式
    msg_content_html = MIMEText(html, content_format2, 'utf-8') #其中html是邮件正文的格式，utf-8是编码格式
    
    #创建多对象邮件
    msg = MIMEMultipart('mixed')
    alternative_part = MIMEMultipart('alternative')
    
    #传递进Header
    msg['From'] = _format_addr(sender) #只有From是必须的，否则会报错
    msg['To'] = ', '.join([_format_addr(s) for s in recv_list]) #将元组转为字符串
    msg['Subject'] = Header('Python SMTP测试', 'utf-8').encode()
    
    #添加邮件正文
    #alternative_part.attach(msg_content_txt)
    alternative_part.attach(msg_content_html)
    msg.attach(alternative_part)
    msg.attach(msg_content_txt)
    
    #添加附件
    with open(r'C:/Users/rog/Desktop/Demo/CDemo/thumbnail.jpg', 'rb') as f:
        mime = MIMEBase('image', 'jpg', filename='thumbnail.jpg')   #这里的filename是附件的名字
        mime.add_header('Content-Disposition', 'attachment', filename= 'thumbnail.jpg') #这里的filename是附件的名字
        mime.add_header('Content-ID', '<0>')    #这里的content-id是附件在html中引用的标识
        mime.add_header('X-Attachment-Id', '0') #这里Attachment-Id是附件的标识
        mime.set_payload(f.read())
        encoders.encode_base64(mime)    #对附件进行编码
        msg.attach(mime)
    
    try:
        # 建立SMTP_SSL连接
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.set_debuglevel(1)
        
        # 登录SMTP服务器
        server.login(sender_addr, password)
        
        # 发送邮件
        server.sendmail(sender_addr, receiver, msg.as_string())
        print("邮件发送成功！")
    
    except Exception as e:
        print("邮件发送失败:", e)
    
    finally:
        # 关闭SMTP连接
        server.quit()
    
if __name__ == '__main__':
    main()
    
# +- MIMEBase
#    +- MIMEMultipart
#    +- MIMENonMultipart
#       +- MIMEMessage
#       +- MIMEText
#       +- MIMEImage