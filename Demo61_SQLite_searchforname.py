#练习，在SQLite中根据分数段查找指定的名字
import os, sqlite3

#清除之前的test.db文件
db_file = os.path.join(os.path.dirname(__file__), 'test.db')
if os.path.isfile(db_file):
    os.remove(db_file)

# 初始数据:
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
conn.commit()
cursor.close()
conn.close()
    
#返回指定分数区间的名字，按分数从低到高排序
def get_score_in(low, high):
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute(r'SELECT name FROM user WHERE score BETWEEN? AND? ORDER BY score', (low, high))
        values = [name[0] for name in cursor.fetchall()]
        return values
    
    except Exception as e:
        print(e)
    
    finally:
        cursor.close()
        conn.close()
        
# 测试:
assert get_score_in(80, 95) == ['Adam'], get_score_in(80, 95)
assert get_score_in(60, 80) == ['Bart', 'Lisa'], get_score_in(60, 80)
assert get_score_in(60, 100) == ['Bart', 'Lisa', 'Adam'], get_score_in(60, 100)

print('Success.')