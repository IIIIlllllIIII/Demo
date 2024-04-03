#SQLite数据库,SQLite占位符是"?"
import sqlite3

conn = sqlite3.connect('test.db') #实例化连接对象
cursor = conn.cursor()    #实例化游标对象
#创建user表
#cursor.execute('create table user (id varchar(20) primary key , name varchar(20))')    #execute执行
cursor.execute('insert into user (id, name) values (\'3\', \'Jerry\')')   #插入一条数据('2', 'Bob')
row_count = cursor.rowcount  #返回插入的行数,这里的rowcount是一个属性表示行数
print(row_count) #打印插入的行数

conn.commit()   #提交事务
cursor.close()  #关闭游标
conn.close()    #关闭连接