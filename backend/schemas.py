from datetime import datetime

from pydantic import BaseModel, ConfigDict


# 创建文章的请求体类型
class PostCreate(BaseModel):
    title: str
    content: str


# 更新文章的请求体类型
# str | None = None --> 类型注解=默认值，这里表示可以是字符串或空，默认空
class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


# 返回给前端的文章数据
# pydantic 默认只读取字典或者另一个 pydantic 对象的数据，接口返回的是 SQLAlchemy 对象
# from_attributes=True 允许 pydantic 从 SQLAlchemy 对象读取属性
# model_config 用于配置 pydantic 的行为，ConfigDict 为存放模型行为开关的字典
class PostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
