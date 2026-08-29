from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from models import Tag
from schemas import TagOut

# 使用APIRouter创建路由对象
router = APIRouter(prefix="/tags", tags=["tags"])


# 接口：标签列表
@router.get("/", response_model=list[TagOut])
def list_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()
