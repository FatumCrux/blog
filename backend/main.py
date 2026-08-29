from fastapi import FastAPI

import models  # noqa F401：No Quality Assuarance 触发模型登记的副作用，故意留着不删  F401:错误码：import未被使用
from db import Base, engine
from routers.auth import router as auth_router
from routers.posts import router as posts_router
from routers.tags import router as tags_router

# 创建 web 应用
app = FastAPI(title="My Blog")
app.include_router(posts_router, prefix="/api")
app.include_router(tags_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

# 建表：调用 Base.metadata 里的 create_all 方法，通过 engine 建表，
# 且只会创建不存在的表，若表已经存在则跳过
Base.metadata.create_all(bind=engine)


# 定义接口，浏览器访问 /api/health 时返回 ok
@app.get("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)  # reload=true 改代码自动重启
