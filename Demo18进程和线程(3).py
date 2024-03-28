import subprocess

'''print('$ nsloookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org'])
print('Exit code:', r)
'''
print('$ nslookup')
p = subprocess.Popen(['nslookup'], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
output, err = p.communicate(b'set q=mx\npyton.org\nexit\n') #这里的comunicate用语输入并获得输出和错误，返回的是一个tuple
try:
    decoded_output = output.decode('utf-8')
except UnicodeDecodeError:
    decoded_output = output.decode('latin-1', errors='ignore')  # 使用latin-1编码并忽略无法解码的字节序列

print('Exit code:',p.returncode)