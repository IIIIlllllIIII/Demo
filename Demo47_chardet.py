#chardet(Character Encoding Detection)字符编码检测，用于检测文本字符串的字符编码。根据文本内容推测出最可能的字符编码，例如 UTF-8、GBK、ISO-8859-1 等，以帮助解决文本编码不明确的问题。
import chardet

with open('test.txt', 'rb') as f:
    data_1 = f.read()
result = chardet.detect(data_1)   #返回一个dict
print('Detected Encoding: ', result['encoding'])
print('Confidence: ', result['confidence'])
print(result['language'])

data_2 = '离离原上草，一岁一枯荣。'.encode('gbk')
print(chardet.detect(data_2))

data_3 = '离离原上草，一岁一枯荣。'.encode('utf-8')
print(chardet.detect(data_3))   #这里最后输出字典中language为空是因为chardet只能检测特定编码

data_4 = '最新の主要ニュース'.encode('euc-jp')
print(chardet.detect(data_4))
6
#chardet对短字符判断不准确
data='望远烬'.encode('gbk')
print(chardet.detect(data))
