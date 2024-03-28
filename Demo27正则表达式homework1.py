import re

def is_valid_email(addr):
    match = re.match(r'^[0-9a-zA-Z\_\.]+@[0-9a-zA-Z\_]+.\w{3}$', addr)
    if match:
        return True
    else:
        return None
def name_of_email(addr):
    re_name = re.compile(r'<?([\w\s]+)?>?[\w\s]*@(\w+\.org)')
    return re_name.match(addr).group(1)


# 测试:
assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
assert name_of_email('tom@voyager.org') == 'tom'
assert is_valid_email('someone@gmail.com')
assert is_valid_email('bill.gates@microsoft.com')
assert not is_valid_email('bob#example.com')
assert not is_valid_email('mr-bob@example.com')
print('ok')