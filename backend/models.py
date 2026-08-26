from datetime import datetime, timezone
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from db import Base

#多对多关联表，一篇文章可以匹配多个标签，一个标签也可以匹配多篇文章
#关联表没有对象，也不需要对象。所以直接实例化，不需要声明为类。但我需要对象，但我也没有对象
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"),primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

#Post表类，表名posts，存放文章的id、标题、内容、上传与修改时间，用tags通过post_tags建立与Tag表的双向关系
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    tags = relationship("Tag", secondary=post_tags, back_populates="posts")

#Tags表类，表名tags，存放tag标签的id和名称，用posts通过post_tags建立与Post表的双向关系
class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")