from fastapi import FastAPI

#创建web应用
app = FastAPI(title="My Blog")

#定义接口，浏览器访问/api/health时返回ok
@app.get("/api/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True) #reload=true 改代码自动重启