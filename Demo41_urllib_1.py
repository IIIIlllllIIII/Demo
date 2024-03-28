from urllib import request
#Get
with request.urlopen('https://www.python.org') as f:
    data = f.read()
    print('Status:', f.status, f.reason)    #这里面Status中保存的格式是str形式
    for k, v in f.getheaders():
        print(k, ':', v)    #这里不用转换时是因为Python在HTTP中响应中自动将字节串转换为unicode编码
    #print('Data:', data.decode('utf-8'))   #f.read()在HTTP响应中，除了状态行之外的所有内容，包括响应头部和响应体，都是以字节串的形式返回的。

from urllib import request
url_1 = 'http://www.douban.com'
head = {'User-Agent': 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25'}
req = request.Request(url_1)  #创建了一个HTTP请求对象'req'
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')    #通过add_header向请求对象'req'添加一个自定义的头部信息
#或者这样添加
for key, value in head.items():
    req.add_header(key, value)
with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' %(k, v))
    #print('Data:', f.read().decode('utf-8'))
        
#Post
from urllib import request, parse   #urllib里的parse和argparse不同

print('Login to Webo.cn...')
email = input('Email: ')
passwd = input('Password: ')
url_2 = 'https://passport.weibo.com/sso/signin'
headers = {'Origin': 'https://passport.weibo.cn', 'User-Agent': 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25', 'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F'}
data = [
    ('username', email),
    ('password', passwd),
    ('entry', 'mweibo'),
    ('client_id', ''),
    ('savestate', '1'),
    ('ec', ''),
    ('pagerefer', 'https://passport.weibo.com/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F')
]
login_data = parse.urlencode(data)      #urllib.parse.urlencode()将传入的参数data编为URL格式的字符串用来登陆
req = request.Request(url_2)    #实例化一个req对象
for k, v in headers.items():
    req.add_header(k,v)
with request.urlopen(req, data= login_data.encode('utf-8')) as f:
    print('Status: ', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s, %s' %(k, v))
    #print('Data:', f.read().decode('utf-8'))

#练习：利用urllib读取JSON，然后将JSON解析为Python对象
import json
from urllib import request

def fetch_data(url):
    req = request.Request(url)
    for k, v in headers.items():
        req.add_header(k, v)
    with request.urlopen(req) as f:
        js_data = f.read().decode('utf-8')
        Python_data = json.loads(js_data)
        return Python_data

# 测试
URL = 'http://www.httpbin.org/get'
data = fetch_data(URL)
print(data)
assert data['origin'] == '106.41.235.142'
print('ok')

