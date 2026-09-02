from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from dependencies import get_current_user
from models import Post, Tag, User
from schemas import PostCreate, PostOut, PostUpdate

# 使用APIRouter创建路由对象
router = APIRouter(prefix="/posts", tags=["posts"])


# 辅助函数，查询文章，让接口3、4、5都调用，不必反复写同一个功能
# db的值由调用方传入，不带默认值
def get_post_or_404(post_id: int, db: Session):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="文章不存在")
    return post


# 接口1：创建文章(增)
# 装饰器，使用post方法发送请求，声明路径“/”
# 声明响应模型为schema中创建的对象PostOut
# 返回状态 201 Created，即成功处理请求并创建新的资源
# Python中函数本身也是一个对象，可以被传递与接收，装饰器就是传递函数、接收函数的函数
# @:语法糖，将函数传递给装饰器，装饰器返回一个新函数替换原函数，此时调用该函数等价于调用新函数
@router.post("/", response_model=PostOut, status_code=201)
def create_post(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):  # PostCreate是Pydantic请求模型，负责接受和校验前端传的参数
    post = Post(title=post_data.title,
                content=post_data.content,
                author_id=current_user.id
                )  # Post是数据库模型，将请求模型接收的参数存储在数据库中
    # 上传文章时添加标签，如果数据库中存在同名标签，就用现成的标签对象
    # 如果不存在同名标签，就新建标签对象并写入数据库
    for tag_name in post_data.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()  # 判断标签是否存在并将结果存入tag，可以为None，即不存在
        if tag is None:
            tag = Tag(name=tag_name)  # 若不存在则新建Tag实例赋给tag
            db.add(tag)  # 将tag加入会话
        post.tags.append(tag)  # 将tag加入文章中
    db.add(post)  # 将数据加入会话
    db.commit()  # 提交事务，写入数据库
    db.refresh(post)  # 刷新对象，获取相应的值(id、创建时间)
    return post


# 接口2：文章列表(查)
@router.get("/", response_model=list[PostOut])
def list_posts(tag: str | None = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(Post)  # 先查询Post表
    # tag存在，就筛选出包含对应tag的文章
    if tag:
        query = query.filter(Post.tags.any(Tag.name == tag))
    posts = query.offset(skip).limit(limit).all()  # 分页显示，一页10条(默认limit=10)
    return posts


# 接口3：单篇文章详情(查)
@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return get_post_or_404(post_id, db)


# 接口4：修改文章(改)
@router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int,
                post_data: PostUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)
                ):
    post = get_post_or_404(post_id, db)
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="禁止修改他人文章")  # 状态码403 Forbidden: 拒绝授权，禁止访问
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content
    if post_data.tags is not None:
        post.tags.clear()
        for tag_name in post_data.tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if tag is None:
                tag = Tag(name=tag_name)
                db.add(tag)
            post.tags.append(tag)
    db.commit()
    db.refresh(post)
    return post


# 接口5：删除文章(删)
# 返回状态 204 No Content，表示请求成功处理，无内容返回给前端(因为已经删除了)
# FastAPI得到204的状态码时，会直接把响应体丢掉，为了更好的用户体验，此处选择200，后面在前端中用消息体展示响应体
@router.delete("/{post_id}", status_code=200)
def delete_post(post_id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)
                ):
    post = get_post_or_404(post_id, db)
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="禁止删除他人文章")
    db.delete(post)
    db.commit()
    return {"message": "删除成功"}
