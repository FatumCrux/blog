from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models  # noqa F401：No Quality Assuarance 触发模型登记的副作用，故意留着不删  F401:错误码：import未被使用
from db import Base, engine
from routers.auth import router as auth_router
from routers.posts import router as posts_router
from routers.tags import router as tags_router

# 创建 web 应用
app = FastAPI(title="My Blog")

# 添加CORS(跨域资源共享)中间件
# 前端从文章列表点进文章详情时，浏览器从5173端口(前端)跨域请求到8000端口(后端)
# 启用CORS，否则请求会被拦截
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，注意这里等买了域名之后要改成自己的域名
    allow_methods=["*"],  # 允许所有方法(get/post/put/delete)
    allow_headers=["*"],  # 允许所有请求头，比如Authorization
)
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
