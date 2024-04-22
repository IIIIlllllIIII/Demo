# from html.parser import HTMLParser
# from html.entities import name2codepoint

# class MyHTMLParser(HTMLParser):     #定义一个解析HTML的类
#     def handle_starttag(self, tag, attrs):  #起始标签
#         print('<%s>' %tag)
#     def handle_endtag(self, tag):   #结束标签
#         print('</%s>' %tag)
#     def handle_startendtarg(self, tag, attrs):  #自闭合标签：<tag/>
#         print('<%s/>' %tag)
#     def handle_data(self, data):    #HTML中的文本数据
#         print(data)
#     def handle_comment(self, data):     #HTML注释：<!-- 这是一个简单的 HTML 注释 -->
#         print('<!--', data, '-->')
#     def handle_entityref(self, name):   #实体引用：实体引用表示特定字符的别名或实体名称，例如 &amp; 表示 & 字符，&lt; 表示 < 字符。
#         print('&%s;' %name)
#     def handle_entityref(self, name):   #字符引用：字符引用表示特定字符的 Unicode 码点或编码值，如 &#65; 表示字符 A 的 Unicode 码点或者编码值。
#         print('&#%s;' %name)

# parser = MyHTMLParser()
# parser.feed('''<html>
# <head></head>
# <body>
# <!-- test html parser -->
#     <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
# </body></html>''')

#作业：找一个网页，并尝试解析HTML。
from urllib import request
from html.parser import HTMLParser
import re   # regular expression正则表达式
import gzip

def getdata(url):   # 发送一个GET请求到指定的页面，并返回UTF-8格式的HTTP
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    req = request.Request(url, headers= header)
    with request.urlopen(req, timeout= 20) as f:
        data = f.read()
        content_encoding = f.headers.get('Content-Encoding')
        if content_encoding == 'gzip':      # 响应头被压缩了
            data = gzip.decompress(data)    # 先解压
        print(f'Status: {f.status} {f.reason}')     
        print()
    return data.decode('utf-8')

class MyHTMLParser_2(HTMLParser):
    def __init__(self):
        super().__init__()  # 继承父类的构造函数
        self.__pointer = '' # 设置一个私有空字符变量，用于临时存储读取到的标签，并判断是否是所需要的
        self.info = []  # 创建一个列表，用于存储
    def handle_starttag(self, tag, attrs):  # 起始标签
        if ('class', 'event-title') in attrs:
            self.__pointer = 'name'
        elif tag == 'time':
            self.__pointer = 'time'
        elif ('class', 'say_no_more') in attrs:
            self.__pointer = 'year'
        elif ('class', 'event-location') in attrs:
            self.__pointer = 'location'
    def handle_endtag(self, tag):   # 清空临时存储读到的标签
        self.__pointer = ''        
    def handle_data(self, data):    # HTML中的文本数据
        if self.__pointer == 'name':
            self.info.append(f'会议名称：{data}')
        if self.__pointer == 'time':
            self.info.append(f'会议时间：{data}')
        if self.__pointer == 'year':
            if re.match(r'\s\d{4}', data):
                self.info.append(f'会议年份：{data}')
        if self.__pointer == 'location':
            self.info.append(f'会议地点：{data}\n')
def main():
    parser = MyHTMLParser_2()
    URL = 'https://www.python.org/events/python-events/'
    htmldata = getdata(URL)
    parser.feed(htmldata)
    for s in parser.info:
        print(s)
if __name__ == '__main__':
    main()