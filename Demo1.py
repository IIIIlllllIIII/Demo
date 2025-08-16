# 导入系统和操作系统模块
import sys
import os
import sqlite3

# 定义字段类，用于创建数据库字段
class Field(object):
    def __init__(self, name, column_type):
        """
        初始化字段对象。

        :param name: 字段名
        :param column_type: 字段类型
        """
        self.name = name
        self.column_type = column_type

    def __str__(self):
        """
        返回字段的字符串表示。

        :return: 字段的字符串表示
        """
        return '<%s:%s>' % (self.__class__.__name__, self.name) # 字段的字符串表示格式

# 定义字符串字段类，继承自字段类，设置默认类型为varchar(100)
class StringField(Field):
    def __init__(self, name):
        """
        初始化字符串字段对象。

        :param name: 字段名
        """
        super(StringField, self).__init__(name, 'varchar(100)')

# 定义整数字段类，继承自字段类，设置默认类型为bigint
class IntegerField(Field):
    def __init__(self, name):
        """
        初始化整数字段对象。

        :param name: 字段名
        """
        super(IntegerField, self).__init__(name, 'bigint')

# 定义模型元类，用于在创建类时进行特殊处理
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        """
        创建模型类时的定制逻辑。

        :param cls: 当前元类
        :param name: 类名
        :param bases: 基类列表
        :param attrs: 类属性字典
        :return: 模型类或原始类
        """
        if name == 'Model':
            # 如果定义的是基础模型类，则直接返回
            return type.__new__(cls, name, bases, attrs)

        # 打印发现的模型类信息
        print('Found model: %s' % name)
        # 创建映射字典
        mappings = dict()
        # 遍历属性，寻找字段对象
        for k, v in attrs.items():
            if isinstance(v, Field):
                # 打印字段映射信息
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            # 从属性中移除字段对象，准备设置到__mappings__中
            attrs.pop(k)
        # 设置映射和表名属性
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        # 创建并返回模型类
        return type.__new__(cls, name, bases, attrs)
    

# 定义模型基类，用于定义数据模型
class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        """
        初始化模型对象。

        :param kw: 关键字参数，用于初始化模型属性
        """
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        """
        获取模型属性值。

        :param key: 属性名
        :return: 属性值
        :raises AttributeError: 如果属性不存在
        """
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        """
        设置模型属性值。

        :param key: 属性名
        :param value: 属性值
        """
        self[key] = value

    def save(self):
        """
        保存模型到数据库的方法。
        """
        fields = []
        params = []
        args = []
        # 遍历映射，构建SQL语句的字段和参数部分
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        # 构建并打印SQL语句
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))

# 定义用户模型类，继承自模型基类
class User(Model):
    username = StringField('username')
    email = StringField('email')
    password = StringField('password')

# 创建用户模型实例并保存
u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
u.save()

# ### 类定义时的处理（由元类`ModelMetaclass`执行）
# 1. **类定义阶段**：当你定义一个类如`User`继承自`Model`时，Python解释器在创建这个类之前首先调用元类`ModelMetaclass`的`__new__`方法。这是因为`Model`类定义了`ModelMetaclass`作为其元类。
# 2. **字段识别与提取**：`ModelMetaclass`会检查`User`类中定义的属性，找出所有是`Field`类型的属性（比如`StringField`和`IntegerField`），并将这些信息收集到一个映射（`__mappings__`）中。
# 3. **修改类属性**：元类会移除原类定义中的字段属性，防止它们像普通属性一样被直接访问，并设置额外的属性如`__table__`（用于数据库表名）。
# 4. **完成类的创建**：处理完这些特殊逻辑后，`ModelMetaclass`会正式创建`User`类对象，并返回。

# ### 实例化过程（利用`dict`基类和`Model`类的构造函数）
# 1. **实例化`User`**：当你创建`User`类的实例时，首先调用的是`Model`类的构造函数（`__init__`），因为`User`没有显式定义自己的构造函数。
# 2. **`dict`基类的构造函数**：在`Model`的构造函数中，通过`super()`调用，最终会调用`dict`的构造函数，这使得`Model`实例本质上是一个字典，能够存储以属性名为键，属性值为值的键值对。
# 3. **属性存储**：在调用`dict`的构造函数时，所有传入的关键字参数（如`id=12345, name='Michael', email='test@orm.org', password='my-pwd'`）都被存储在这个字典（即`Model`实例）中。

# ### 属性访问与设置（由`Model`类定义的方法处理）
# - 当访问或设置一个属性时（比如`u.email`），会调用`__getattr__`和`__setattr__`方法（这些在`Model`类中定义），这些方法实际上是在操作底层的字典结构，即通过键值对的方式获取或设置属性值。

# 这种设计使得类的结构定义与实例的行为分离，类结构在类定义时通过元类定制，而实例的行为（如属性的存储和访问）则由`dict`和在`Model`类中定义的方法控制。这为ORM框架提供了极大的灵活性和扩展性。
