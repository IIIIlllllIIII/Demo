import base64

b64 = base64.b64encode(b'binary string')    #字符数量不为3的倍数需要在最后补足' '(即ASCII编码的：\x00)
#添加了几个' '最后需要在转换成的base64编码后补上几个'='
print(b64)
b_1 = base64.b64decode(b64)
print(b_1)

#base64的urlsafe编码，将+和/分别替换成-和_
b64_1 = base64.b64encode(b'i\xb7\x1d\xfb\xef\xff')  #ASCII中的i+一串二进制数
print(b64_1)
b64_2 = base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff')  #urlsafe输出用base64.urlsafe_b64encode()函数
print(b64_2)
b_2 = base64.urlsafe_b64decode(b64_2)
print(b_2)

#去掉'='的Base64
b64_3 = base64.b64encode(b'abcd')
print(b64_3)

#作业：
def safe_base64_decode(s):
    if len(s) % 4 ==0:
        return base64.b64decode(s)
    else:
        s +='='
        return safe_base64_decode(s)    #递归
def safe_base64_decode(s):
    return base64.b64decode(s + ('===='[len(s)%4:]))    #切片做法，str相加直接用'+'

# 测试:
assert b'abcd' == safe_base64_decode('YWJjZA=='), safe_base64_decode('YWJjZA==')
assert b'abcd' == safe_base64_decode('YWJjZA'), safe_base64_decode('YWJjZA')
print('ok')