from xml.parsers.expat import ParserCreate  # 其中expat是expat的缩写，expat是Python的一个XML解析器

# 用SAX(Simple API for XML)模式解析XML，XML例子：<a href="/">python</a>
class DefaultSaxHandler(object):    # 三个事件:1.start_element事件,在读取<a href="/">时；2.char_data事件，在读取python时；3.end_element事件，在读取</a>时。
    def start_element(self, name, attrs):
        print('sax:start_element: %s, attrs: %s' %(name, str(attrs)))
    
    def end_element(self, name):
        print('sax:end_element: %s' %name)
    
    def char_data(self, text):
        print('sax:char_data: %s' %text)
xml = r'''<?xml version="1.0"?>
<ol>
    <li><a href="/python">Python</a></li>
    <li><a href="/ruby">Ruby</a></li>
</ol>
'''
#其中的\n也会在使用CharacterDataHandler的时候被识别，所以输出的时候会有空行
handler = DefaultSaxHandler()
parser = ParserCreate()
#将属性和方法连接
parser.StartElementHandler = handler.start_element
parser.EndElementHandler = handler.end_element
parser.CharacterDataHandler = handler.char_data
parser.Parse(xml)

def encode(data):
    # 这里可以编写将字符串编码为 XML 实体的逻辑
    # 例如，将 '&' 替换为 '&amp;'
    return data.replace('&', '&amp;')

def generate_xml():
    L = []
    L.append(r'<?xml version="1.0"?>')
    L.append(r'<root>')
    L.append(encode('some & data'))  # 此处的 encode 函数需要定义或导入
    L.append(r'</root>')
    return ''.join(L)
# 调用函数生成 XML 字符串
xml_string = generate_xml()
print(xml_string)

#作业：请利用SAX编写程序解析高德的XML格式的天气预报，获取天气预报
from xml.parsers.expat import ParserCreate
from urllib import request

class WeatherSaxHandler(object):    # 是类！！！
    # 先定义三个基础参数
    def __init__(self):
        self.city = ''      #城市
        self.pointer = ''   #临时变量用于保存名字
        self.forcast = []   #定义的天气内容
    def start_element(self, name, attrs):
        self.pointer = name
        if name == 'cast':
            self.weather = {
                'date': '',
                'high': '',
                'low': ''
            }   #定义了返回的天气字典包含的内容
    def end_element(self, name):
        if name == 'cast':
            self.forcast.append(self.weather)
        self.pointer = ''
    def char_data(self, text):
        if self.pointer == 'province':
            self.city = text
        elif self.pointer == 'date':
            self.weather['date'] = text
        elif self.pointer == 'daytemp_float':
            self.weather['high'] = text
        elif self.pointer == 'nighttemp_float':
            self.weather['low'] = text
    def toJSON(self):
        return {'city': self.city, 'forecast': self.forcast}
        
def parseXml(xml_str):
    print(xml_str)
    handler = WeatherSaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(xml_str)
    return handler.toJSON()
    
# 测试:
KEY = 'c13af3fa8dc87a1b1e2426a5547ae277'    #从高德申请的KEY
URL = 'https://restapi.amap.com/v3/weather/weatherInfo?city=110101&key=%s&output=xml&extensions=all' % KEY


with request.urlopen(URL, timeout=4) as f:
    data = f.read()
result = parseXml(data.decode('utf-8'))
assert result['city'] == '北京'
print('ok')