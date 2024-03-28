import os, re

k = '0910-87654321'
result = re.match(r'^(\d{3}|\d{4})-(\d{8})$', k)
if result:
    print('成功')
else:
    print('失败')
print(result)

print(result.group(2))

a = re.match(r'^(\d+?)(0*)$', '102300').groups()
print(a)
telephone_number = '010-10101'
telephone = re.compile(r'^(\d{3})-(\d{3,8})$')
t_match = telephone.match(telephone_number)
print(t_match.group(2))
