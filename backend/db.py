from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# 数据库连接串，切换数据库时仅修改该行
# 通用 url 格式"数据库(协议)://主机/路径，sqlite 无主机，所以直接 3 个/
DATABASE_URL = "sqlite:///./blog.db"

# 引擎：连接数据库，开放多线程。sqlite 默认单线程("check_same_thread": True)，
# FastAPI 需要多线程，所以 False
# sqlite 就一个文件，多线程同时读写可能会锁住，但博客够用了；
# 不够还可以直接切成 PostgreSQL——话又说回来，反正最后都得切，先将就着
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 创建会话。不自动提交：该模式已移除，保留参数是为了兼容老代码，设置为 True 会报错；
# 不自动冲刷：查询之前写数据不安全，容易产生意外
# flush 冲刷：把内存中的数据写入数据库，比如改了一个数据但未确认提交，
# 此时查询数据库，autoflush 就会把这个未确认的数据先写入数据库，再返回查询
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 总表，所有模型都继承 Base，登记后面会创建的表
# DeclarativeBase：通用模板，自动登记后面创建的所有表，只有登记后才能创建表
# 现在不需要写东西，也不知道写啥东西，但不能为空，所以先用 pass 占位
class Base(DeclarativeBase):
    pass


# 每次请求自动打开会话，用完自动关闭
# yield：生成器关键字，让函数变成生成器函数，调用时得到一个生成器对象，
# 暂停 get_db() 的执行，把 db 交给路由调用，下次继续从这里执行
# 生成器：python 里面的一个可迭代对象，不会一次计算出所有结果，只有在需要用到时才会产出
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
