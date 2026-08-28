from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship

from db import Base


# 多对多关联表，一篇文章可以匹配多个标签，一个标签也可以匹配多篇文章
# 关联表没有对象，也不需要对象。所以直接实例化，不需要声明为类。但我需要对象，但我也没有对象
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


# Post 表类，表名 posts，存放文章的 id、标题、内容、上传与修改时间，
# 用 tags 通过 post_tags 建立与 Tag 表的双向关系
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    tags = relationship("Tag", secondary=post_tags, back_populates="posts")


# Tags 表类，表名 tags，存放 tag 标签的 id 和名称，
# 用 posts 通过 post_tags 建立与 Post 表的双向关系
class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")


# User表类，用户注册、登录等功能，感觉不是很必要，但是还是先做吧，个人博客也不太需要其他人来注册
# 数据库中不储存明文密码，储存密码的哈希值
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
