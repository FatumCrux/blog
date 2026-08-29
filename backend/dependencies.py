from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from db import get_db
from models import User
from security import decode_token

security = HTTPBearer()


# 利用auth.py里面的sub键获取当前用户，用以确认token归属
# 若用户不存在，返回状态码401 Unauthorized，没有认证或认证错误，表示登录失败或者token失效
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    # 若前端携带过期token向后端发起请求(30分钟有效期)，会收到状态码500：服务器遇到无法处理的请求
    # 而token过期导致的异常应该预期收到401
    # 所以这里需要捕获异常，抛出401
    try:
        payload = decode_token(token)
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")
    user = db.query(User).filter(User.username == payload["sub"]).first()
    if user is None:
        raise HTTPException(status_code=401, detail="无效的认证信息")
    return user
