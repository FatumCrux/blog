from fastapi import FastAPI
from db import Base, engine
import models

#创建web应用
app = FastAPI(title="My Blog")
#建表，调用Base.metadata里的create_all方法，通过engine建表，且只会创建不存在的表，若表已经存在则跳过
Base.metadata.create_all(bind=engine)

#定义接口，浏览器访问/api/health时返回ok
@app.get("/api/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True) #reload=true 改代码自动重启