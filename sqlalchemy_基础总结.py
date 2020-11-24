from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker

"""
1, 声明映射，创建对象的基类,可以根据基类定义任意数量的映射类。
通过声明系统，已经定义了关于表的信息，成为table metadata; 当声明类时，声明使用了python的元类，是为了在类声明完成后执行其他活动；在这个阶段中，还创建了一个Tale对象，这个table称为metadata；
"""
Base = declarative_base()

"""
2, 与指定数据库建立链接对象，通过create_engine建立连接；

初始化数据库链接；
格式：
    '数据库类型+数据库驱动://用户名:密码@机器地址:端口号/数据库'
如：
    链接postgresql：engine = create_engine("postgresql://username:password@ip:port/dbname)
    
create_engine: 创建新的engine实例；
    参数详解：（选填，可根据需要设置）
        1, case_sensitive=True: 如果为false, 表中的结果列以不区分大小写方式匹配; 即：UserInfo <==> userinfo
        2, creator: 返回db api连接的可调用文件。此创建函数将传递给基础连接池，并将用于创建所有新的数据库连接。使用此函数将忽略url参数中指定的连接参数
        3, echo=False: 如果为True，将输出记录所有的sql语句日志
        4, encoding: 默认utf-8, 字符串编码，在db api之外。
"""
engine  = create_engine("mysql+pymysql://root:123456@localhost:3306/sql_test")

"""
3, 创建链接引擎对象之后，需要获取和指定数据库之间的链接，通过利埃纳杰进行数据增删改查；和数据库之间的链接就是会话；

"""
# 创建一个链接会话对象
DBSession = sessionmaker(bind=engine)
# 实例化session对象
session = DBSession() #
"""
session = DBSession()：创建session对象
new_user = User(xxxx)：创建User对象
session.add(new_user)：添加到session
session.commit()：提交即保存到数据库;刷新对数据库的其余更改，并提交事务。会话引用的连接资源返回连接池。
session.close()：关闭数据库服务
"""

# 2，定义USER对象
class Users(Base):
    __tablename__ = "users"  # 表的名字
    # 表的结构
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

"""添加对象"""

# 1, 添加单条
ed_user = Users(name='ed', fullname="Edjone", nickname="ednickname")
session.add(ed_user)
session.commit()

# 2, 批量添加
our_user = session.add_all([
    Users(name='why', fullname="whying", nickname="wan"),
    Users(name='san', fullname="zhangsan", nickname="zhangsan")
])
our_user.commit()


# """获取对象"""
# ############## 筛选器 #################
# 1, 等值
session.query(Users).filter(Users.id == 1)
# 2, 不等值
session.query(Users).filter(Users.name != 'ed')
# 3, like模糊匹配
session.query(Users).filter(Users.name.like('%ed'))
# 4, ilike与like一样，只是不区分大小写
session.query(Users).filter(Users.name.ilike('%Ed'))
# 5, in
session.query(Users).filter(Users.name.in_(['ed', 'why', 'jack']))
# 6, not in
session.query(Users).filter(~Users.name.in_(['ed', 'why','jack']))
# 7, IS NULL
session.query(Users).filter(Users.name == None)
session.query(Users).filter(Users.name.is_(None))
# 8, is not null:
session.query(Users).filter(Users.name != None)
session.query(Users).filter(Users.name.isnot(None))
# 9, and
session.query(Users).filter(Users.name == "ed" and Users.fullname == "Ed jones")
session.query(Users).filter(Users.name == "ed", Users.fullname == "Ed jones")
session.query(Users).filter(Users.name == "ed").filter(Users.fullname == "Ed jones")
# 10, or
from sqlalchemy import or_
session.query(Users).filter(or_(Users.name == 'ed', Users.name =='why'))
# 11, match
session.query(Users).filter(Users.name.metch("wendy"))


# ############## 方法 #################
# 1, 返回列表
session.query(Users).filter(Users.name.like('%ed')).order_by(Users.id).all()
# 2, 只返回一个；相当于limit 1
session.query(Users).filter_by(name='ed').first()
# 3, 完全获取所有行，如果结果不存在一个对象标识或复合行，引发错误
session.query(Users).one()
# 4, 和one一样，如果没有找到不会引发错误，会返回None
session.query(Users).one_or_none()
# 5, 调用one方法，并在成功时返回行的第一列
session.query(Users).scalar()
# 6, 使用文本字符串查询，通过指定text构造；
from sqlalchemy import text
session.query(Users).filter(text("id < 224")).order_by(text("id")).all()
# 7, 基于字符串的sql，使用冒号绑定参数；要指定值使用params()方法
session.query(Users).filter(text("id < :value and name=:name")).params(value=24, name='fred').order_by(Users.id)
# 8, 完全基于字符串的语句；
stmt = text("select name, id, fullname, nickname from users where name=:name")
stmt = stmt.columns(Users.name, Users.id, Users.fullname, Users.nickname)
session.query(Users).from_statement(stmt).params(name='ed').all()
# 计数,count将正在查询的内容放入子查询中，然后计算其中的行数。
1, session.query(Users).filter(Users.name.like('%ed')).count()

2, from sqlalchemy import func
   session.query(func.count(Users.name), Users.name).group_by(Users.name).all()

3, session.query(func.count('*')).select_from(Users).scalar()
4, session.query(func.count(Users.id)).scalar()
# 根据get筛选
session.query(Users).get(id)


# 创建表；python filename.py
Base.metadata.create_all(engine)
