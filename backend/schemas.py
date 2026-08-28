from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# 创建文章的请求体类型
class PostCreate(BaseModel):
    title: str
    content: str
    tags: list[str] = []  # 前端传标签名列表，默认空，不打标签也能传文章


# 更新文章的请求体类型
# str | None = None --> 类型注解=默认值，这里表示可以是字符串或空，默认空
class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


# 标签的输出模型，让文章能带标签
# Python从上往下执行，TagOut必须在PostOut前面，否则后者执行到的list[TagOut]会报错
class TagOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


# 文章的输出模型，返回给前端的文章数据
# pydantic 默认只读取字典或者另一个 pydantic 对象的数据，接口返回的是 SQLAlchemy 对象
# from_attributes=True 允许 pydantic 从 SQLAlchemy 对象读取属性
class PostOut(BaseModel):
    id: int
    title: str
    content: str
    tags: list[TagOut] = []
    created_at: datetime
    updated_at: datetime
# model_config 用于配置 pydantic 的行为，ConfigDict 为存放模型行为开关的字典
# from_attributes=True: 允许 pydantic 模型从任意对象的属性（attribute）读取数据
    model_config = ConfigDict(from_attributes=True)


# 注册请求体：用户创建模型，前端发出创建用户的数据
# 前端提交的是明文密码
class UserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


# 用户输出模型，后端返回前端的数据，密码不能返回
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# 用户登录模型
class UserLogin(BaseModel):
    username: str
    password: str