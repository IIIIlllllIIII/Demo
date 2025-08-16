#SQLAlchemy(alchemy炼金术；表示将某些东西转化为另一种形式的过程)
from sqlalchemy import Column, String, MetaData, ForeignKey, create_engine
# (ORM: Object-Relational Mapping&Mapper对象关系映射)把数据库表和python类进行映射，从而实现数据的持久化操作
from sqlalchemy.orm import sessionmaker, relationship
# (ext: extension拓展)sqlalchemy.ext.declarative是SQLAlchemy的声明式扩展模块，作用是导入基类
from sqlalchemy.ext.declarative import declarative_base 
import os, sqlite3

# 清理脚本目录中的数据库文件
def clean_db():
    db_file = os.path.join(os.path.dirname(__file__), 'test.db')
    if os.path.isfile(db_file):
        os.remove(db_file)
    return db_file.replace('\\', '/')

# 创建元数据对象
test_db = MetaData()
# 创建基类
Base = declarative_base(metadata= test_db)
print(type(Base))
    
# 定义CommonMixin:
class CommonMixin:
    id = Column(String(20), primary_key= True)
    name = Column(String(20))
    
#定义User对象
class User(Base, CommonMixin):
    # 表名
    __tablename__ = 'user'
    # 表的字段(这里继承自CommonMixin)
    # name = Column(String(20))
    # 与Book对象的关系, backref='user'表示反向引用, 用Book.user.(xxx)调用User中的属性
    books = relationship('Book', backref= 'user')
    
# 定义Book对象
class Book(Base, CommonMixin):
    __tablename__ = 'book'
    # “多”的一方的book表是通过外键关联到user表的:
    user_id = Column(String(20), ForeignKey('user.id'))
        
def main():
        
    try:
        # 初始化数据库的连接, SQLAlchemy用一个字符串表示连接信息('数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名')
        engine = create_engine(f'sqlite:///{clean_db()}')
        # 创建session，bind表示绑定
        DBSession = sessionmaker(bind= engine) 
        # 创建session
        session = DBSession()
        
        # 创建表，这里metadata.create_all()方法
        Base.metadata.create_all(engine)
        # custom_metadata = MetaData()
        # Base.metadata.create_all(engine, metadata=custom_metadata) 
        # 这里可以通过在最开始创建不同的MetaData实例，并将继承自该元数据创建的基类的类，来在engine中创建不同的表
        
        # 创建新User对象
        new_user = User(id= '5', name= 'Bob')
        
        # 创建新的Book对象, 这里注意一定要添加user_id，才能从User中查询
        new_book = Book(id= '1', user_id = 5, name= 'Bob_book')
        
        #添加到session，这里想要同时添加多个可以用tuple或list
        session.add_all([new_user, new_book])
        #提交保存到数据库：
        session.commit()
        
        # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
        user = session.query(User).filter(User.id== '5').one()
        book = session.query(Book).filter(Book.id== '1').one()
        
        print('type:', type(user))
        print('name:', user.name)
        print('book:', book.name)
        for book in user.books:
            print('Query from User book_name:', book.name)
        
    except Exception as e:
        print(f'错误是：{e}')
        
    finally:
        print('Close session.')    
        #关闭session
        session.close()
        
if __name__ == '__main__':
    main()
