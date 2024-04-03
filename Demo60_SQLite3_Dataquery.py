import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
 #取出id为1和2的数据
cursor.execute('SELECT * FROM user WHERE id IN (?, ?)', ('1','2'))    #这里要查询两个以上参数有两种写法: id IN (?, ?)和id= ? or id=?

values = cursor.fetchall()    #fetchall()取出所有数据
print(values)

cursor.close()
conn.close()