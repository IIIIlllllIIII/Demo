import requests
from urllib import request, parse

# 定义请求头，伪装为Chrome浏览器访问
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
parameters = {'q': 'python', 'cat': '1001'}
# Get 请求
r_2 = requests.get('https://www.douban.com/', headers= header)  #豆瓣首页 
r_1 = requests.get('https://www.douban.com/search', headers= header, params=parameters)    # 这里别忘记添加headers，否则会被反爬
print(r_1.status_code)
# print(r_1.text)
print(r_1.encoding)
print(r_1.url)
print(r_1.headers['origin'])    # 直接获取响应头
print(r_1.cookies)
print(r_2.url)
print(r_2.encoding)

# r = requests.get('https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202151330&format=json')
# print(r.json())
print(r_2.content)
# print(r_2.text)

# 用urllib实现
req = request.Request('https://www.douban.com/search')
for k, v in header.items():
    req.add_header(k, v)
with request.urlopen(req, data=  parse.urlencode(parameters).encode('utf-8')) as f:
    data = f.read()
    print(f.status, f.reason)
    print(data.decode('utf-8'))

url_1 = 'https://accounts.douban.com/login'
# 这里默认使用application/x-www-form-urlencoded对POST数据编码
r_3 = requests.post(url_1, data={'form_email': 'abc@example.com', 'form_password': '123456'})
params = {'key': 'value'}
# 如果想传递JSON数据
r_4 = requests.post(url_1, json=params) # 内部自动序列化为JSON
# 上传更复杂参数
upload_files = {'file': open('report.xls', 'rb')}   # 这里用rb
r = requests.post(url_1, files= upload_files)

# 操作cookies
r.cookies['ts']     # 获取cookie，查询ts的值
cs = {'token': '12345', 'status': 'working'}    # 创建cookie字典
r = requests.get(url_1, cookies=cs)

import requests

# 创建Session对象（session会话）
s = requests.Session()
# 可以设置Session的头部，这个头部会在所有的请求中使用
s.headers.update({'User-Agent': 'custom user-agent'})
# 第一个请求
r1 = s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
# 查看服务器设置的cookie
print(r1.cookies)
# 第二个请求将自动使用第一个请求中获得的cookies
r2 = s.get('https://httpbin.org/cookies')
print(r2.text)
# 结束会话
s.close()

# 传递超时
r = requests.get(url_1, timeout= 2.5)    # 2.5秒超时
