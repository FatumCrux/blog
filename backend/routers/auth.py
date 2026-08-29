from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models import User
from schemas import UserCreate, UserOut, UserLogin
from security import hash_password, verify_password, create_access_token

# 使用APIRouter创建路由对象
router = APIRouter(prefix="/auth", tags=["auth"])


# 接口1：注册。先检查用户注册名是否存在，如果已经存在则提示换一个。
# 用户名不存在就新建一个用户对象，存入用户的用户名、邮箱和密码hash值，然后加入会话、写入数据库、刷新
# 前端发出注册请求，使用UserCreate请求模型，后端返回用户信息，响应体使用用户信息模型UserOut，返回用户信息实例user
@router.post("/register", response_model=UserOut, status_code=201)
def user_register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="邮箱已存在")
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# 接口2：登录。先检查用户名是否存在，再检查密码是否正确(对比hash)
# 任一有错都提示“用户名或密码错误”，避免黑客通过提示词获取信息
# 成功登录后生成token
@router.post("/login", status_code=200)
def user_login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if verify_password(user_data.password, user.password_hash):
        token = create_access_token({"sub": user.username})  # sub：JWT标准字段，存放用户名，解token时能知道这个token是谁的
    else:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return {
        # token_type: 表明token用法；bearer: 仅限持有者本人可以使用这个token
        # 前端解析时，会在后续每个请求的请求头上携带Bearer + token
        "access_token": token, "token_type": "bearer"
    }
