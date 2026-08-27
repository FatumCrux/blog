from fastapi import FastAPI
from routers.posts import router as posts_router
from db import Base, engine

# 创建 web 应用
app = FastAPI(title="My Blog")
app.include_router(posts_router)

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
