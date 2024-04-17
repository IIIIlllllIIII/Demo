import hashlib

MD5 = hashlib.md5() #创建md5对象
MD5.update('Hello World!'.encode('utf-8')) #计算md5值
print(MD5.hexdigest())

db = {
    'michael': 'e10adc3949ba59abbe56e057f20f883e',
    'bob': '878ef96e86145580c38c87f0410ad153',
    'alice': '99b1c2188db85afee403b1536010c2c9'
}
#作业一
def login(user, password):
    pswd = hashlib.md5()
    pswd.update(password.encode('utf-8'))   #计算md5值
    
    if db[user] == pswd.hexdigest():
        return True
    else:
        return False
    
# 测试:
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')
