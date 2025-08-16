# tiny_orm_fixed.py
import sqlite3
from datetime import datetime
from typing import Any, Optional

# ---------- Step 1: 字段系统（描述符） ----------
class Field:
    sql_type = "TEXT"

    def __init__(self, *, primary_key=False, default=None, null=True, unique=False, max_length=None):
        self.primary_key = primary_key
        self.default = default          # 可为常量或可调用（如 datetime.utcnow）
        self.null = null
        self.unique = unique
        self.max_length = max_length
        self.name = None                # 由 __set_name__ 或元类赋值

    # 自动记录绑定到类中的属性名（推荐）
    def __set_name__(self, owner, name):
        self.name = name

    # —— 描述符协议：三参签名是关键！——
    def __get__(self, instance, owner):
        if instance is None:
            # 类访问（如 User.name）返回字段对象本身，便于 ORM 做元信息收集/DDL 生成
            return self
        # 实例访问：若未赋值，返回默认值（默认值可为 callable）
        return instance.__dict__.get(self.name, self._default_value())

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.name] = value

    # 默认值：callable 则调用取值，常量直接返回
    def _default_value(self):
        return self.default() if callable(self.default) else self.default

    # 基础校验（子类可重写）
    def validate(self, value: Any):
        if value is None and not self.null and not self.primary_key:
            raise ValueError(f"Field '{self.name}' cannot be NULL")

    # Python↔DB 的转换钩子（子类可重写）
    def to_db(self, value: Any):
        return value

    def to_python(self, value: Any):
        return value

    # 生成 CREATE TABLE 的列定义
    def ddl(self) -> str:
        parts = [f'"{self.name}"', self.sql_type]
        if self.primary_key:
            # SQLite 整型主键的自增语义
            if isinstance(self, IntegerField):
                parts.append("PRIMARY KEY AUTOINCREMENT")
            else:
                parts.append("PRIMARY KEY")
            return " ".join(parts)

        if not self.null:
            parts.append("NOT NULL")
        if self.unique:
            parts.append("UNIQUE")

        # 只有“静态默认值”写入 DDL，callable 只在 Python 层赋默认
        if self.default is not None and not callable(self.default):
            parts.append(f"DEFAULT {self._render_default_literal(self.default)}")
        return " ".join(parts)

    @staticmethod
    def _render_default_literal(v):
        if isinstance(v, bool):
            return "1" if v else "0"
        if isinstance(v, (int, float)):
            return str(v)
        if v is None:
            return "NULL"
        s = str(v).replace("'", "''")
        return f"'{s}'"

class IntegerField(Field):
    sql_type = "INTEGER"
    def validate(self, value):
        if value is None:
            if not self.null and not self.primary_key:
                raise ValueError(f"Field '{self.name}' cannot be NULL")
            return
        if not isinstance(value, int):
            raise TypeError(f"Field '{self.name}' expects int, got {type(value).__name__}")

class StringField(Field):
    sql_type = "TEXT"
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError(f"Field '{self.name}' cannot be NULL")
            return
        if not isinstance(value, str):
            raise TypeError(f"Field '{self.name}' expects str, got {type(value).__name__}")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f"Field '{self.name}' exceeds max_length={self.max_length}")

class BooleanField(Field):
    sql_type = "INTEGER"
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError(f"Field '{self.name}' cannot be NULL")
            return
        if not isinstance(value, bool):
            raise TypeError(f"Field '{self.name}' expects bool, got {type(value).__name__}")
    def to_db(self, value):
        return None if value is None else (1 if value else 0)
    def to_python(self, value):
        if value is None:
            return None
        return bool(value)

class DateTimeField(Field):
    sql_type = "TEXT"
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError(f"Field '{self.name}' cannot be NULL")
            return
        if not isinstance(value, datetime):
            raise TypeError(f"Field '{self.name}' expects datetime, got {type(value).__name__}")
    def to_db(self, value):
        return None if value is None else value.isoformat(timespec="seconds")
    def to_python(self, value):
        if value is None:
            return None
        return datetime.fromisoformat(value)

# ---------- Step 2: 元类收集字段 ----------
class ModelMeta(type):
    def __new__(mcls, name, bases, attrs):
        if name == "Model":
            return super().__new__(mcls, name, bases, attrs)

        # 收集 Field
        fields = {}
        for k, v in list(attrs.items()):
            if isinstance(v, Field):
                # __set_name__ 已经记录 name，这里确保一次
                v.name = v.name or k
                fields[k] = v

        # 若无显式主键，则注入自增 id
        if not any(f.primary_key for f in fields.values()):
            if "id" not in fields:
                id_field = IntegerField(primary_key=True, null=False)
                id_field.name = "id"
                attrs["id"] = id_field
                fields["id"] = id_field

        table_name = attrs.get("__tablename__", name.lower())

        cls = super().__new__(mcls, name, bases, attrs)
        cls._meta = {
            "table_name": table_name,
            "fields": fields,
            "pk_name": next(k for k, f in fields.items() if f.primary_key),
        }
        return cls

# ---------- Step 3: Model 基类 ----------
class Model(metaclass=ModelMeta):
    __connection: Optional[sqlite3.Connection] = None

    # 连接管理
    @classmethod
    def bind(cls, conn: sqlite3.Connection):
        conn.row_factory = sqlite3.Row
        cls.__connection = conn

    @classmethod
    def connection(cls) -> sqlite3.Connection:
        if cls.__connection is None:
            cls.bind(sqlite3.connect(":memory:"))
        return cls.__connection

    # 建表
    @classmethod
    def create_table(cls, *, if_not_exists=True):
        cols = [f.ddl() for f in cls._meta["fields"].values()]
        ine = "IF NOT EXISTS " if if_not_exists else ""
        sql = f'CREATE TABLE {ine}"{cls._meta["table_name"]}" (\n  ' + ",\n  ".join(cols) + "\n)"
        cls.connection().execute(sql)
        cls.connection().commit()

    # 实例化辅助：支持关键字赋值 & 静态默认值预设
    def __init__(self, **kwargs):
        fields = self._meta["fields"]
        for k in kwargs:
            if k not in fields:
                raise AttributeError(f"Unknown field '{k}' for {type(self).__name__}")
        for k, f in fields.items():
            if k in kwargs:
                setattr(self, k, kwargs[k])
            else:
                # 对于“静态默认值”，在构造时直接设入；callable 默认值由 __get__ 惰性提供
                if f.default is not None and not callable(f.default):
                    setattr(self, k, f.default)

    def _as_dict(self):
        d = {}
        for k, f in self._meta["fields"].items():
            d[k] = getattr(self, k)
        return d

    @classmethod
    def _row_to_instance(cls, row: sqlite3.Row):
        if row is None:
            return None
        inst = cls()
        for k, f in cls._meta["fields"].items():
            if k in row.keys():
                setattr(inst, k, f.to_python(row[k]))
        return inst

    # CRUD
    def save(self):
        cls = type(self)
        fields = cls._meta["fields"]
        pk = cls._meta["pk_name"]

        col_names = [k for k in fields if k != pk]
        values = [fields[k].to_db(getattr(self, k)) for k in col_names]

        pk_val = getattr(self, pk, None)
        if pk_val is None:
            placeholders = ",".join("?" for _ in col_names)
            cols_sql = ",".join(f'"{c}"' for c in col_names)
            sql = f'INSERT INTO "{cls._meta["table_name"]}" ({cols_sql}) VALUES ({placeholders})'
            cur = cls.connection().execute(sql, values)
            # 自动主键
            new_id = cur.lastrowid
            setattr(self, pk, new_id)
        else:
            set_clause = ",".join(f'"{c}"=?' for c in col_names)
            sql = f'UPDATE "{cls._meta["table_name"]}" SET {set_clause} WHERE "{pk}"=?'
            cls.connection().execute(sql, values + [pk_val])

        cls.connection().commit()
        return self

    def delete(self):
        cls = type(self)
        pk = cls._meta["pk_name"]
        pk_val = getattr(self, pk, None)
        if pk_val is None:
            raise ValueError("Cannot delete unsaved object (primary key is None).")
        sql = f'DELETE FROM "{cls._meta["table_name"]}" WHERE "{pk}"=?'
        cls.connection().execute(sql, (pk_val,))
        cls.connection().commit()

    # 查询 API（参数化，避免注入）
    @classmethod
    def all(cls, *, order_by: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None):
        sql = f'SELECT * FROM "{cls._meta["table_name"]}"'
        params: list[Any] = []
        if order_by:
            desc = order_by.startswith("-")
            key = order_by[1:] if desc else order_by
            if key not in cls._meta["fields"]:
                raise ValueError(f"Unknown order_by field '{order_by}'")
            sql += f' ORDER BY "{key}" {"DESC" if desc else "ASC"}'
        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)
        if offset is not None:
            sql += " OFFSET ?"
            params.append(offset)
        cur = cls.connection().execute(sql, params)
        return [cls._row_to_instance(r) for r in cur.fetchall()]

    @classmethod
    def filter(cls, **kwargs):
        # 等值过滤：User.filter(name="Alice", active=True)
        for k in kwargs:
            if k not in cls._meta["fields"]:
                raise ValueError(f"Unknown filter field '{k}'")
        where = " AND ".join(f'"{k}"=?' for k in kwargs)
        sql = f'SELECT * FROM "{cls._meta["table_name"]}" WHERE {where}'
        params = [cls._meta["fields"][k].to_db(v) for k, v in kwargs.items()]
        cur = cls.connection().execute(sql, params)
        return [cls._row_to_instance(r) for r in cur.fetchall()]

    @classmethod
    def get(cls, **kwargs):
        rows = cls.filter(**kwargs)
        if not rows:
            raise LookupError(f"{cls.__name__}.get(): no row matches {kwargs}")
        if len(rows) > 1:
            raise LookupError(f"{cls.__name__}.get(): multiple rows match {kwargs}")
        return rows[0]

# ---------- Step 4: 定义模型 & 演示 ----------
# 绑定数据库（示例：内存库；实际可用 sqlite3.connect('orm_demo.db')）
Model.bind(sqlite3.connect(":memory:"))

class User(Model):
    __tablename__ = "users"
    id = IntegerField(primary_key=True, null=False)            # 可省略，系统会自动注入
    name = StringField(null=False, max_length=50, unique=True)
    age = IntegerField(null=True)
    active = BooleanField(null=False, default=True)
    created_at = DateTimeField(null=False, default=datetime.utcnow)  # callable 默认值：Python 层赋值

class Post(Model):
    __tablename__ = "posts"
    id = IntegerField(primary_key=True, null=False)
    author = StringField(null=False)                           # 简化：不做外键；进阶可用 ForeignKey
    title = StringField(null=False, max_length=200)
    content = StringField(null=False)

# 建表
User.create_table()
Post.create_table()

# 写入
u1 = User(name="Alice", age=30).save()
u2 = User(name="Bob", age=18, active=False).save()
p1 = Post(author="Alice", title="Hello ORM", content="We built a tiny ORM!").save()
p2 = Post(author="Alice", title="Metaclass Notes", content="Fields collected in ModelMeta.").save()

# 查询
users = User.all(order_by="age")
only_alice = User.get(name="Alice")
active_users = User.filter(active=True)

# 更新
only_alice.age = 31
only_alice.save()

# 删除
User.get(name="Bob").delete()

# 再查
remaining = User.all(order_by="-age")

# 打印演示
print("Users:", [u._as_dict() for u in users])
print("Active:", [u._as_dict() for u in active_users])
print("Remaining:", [u._as_dict() for u in remaining])
print("Posts by Alice:", [p._as_dict() for p in Post.filter(author="Alice")])
