from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# SỬA: Đổi postgres thành localhost và sửa cú pháp connection string
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://cvuser:cvpass@localhost:5432/cvdb"
)

# Lưu ý:
# - postgresql:// : là driver chuẩn (không phải localhost:://)
# - @localhost    : vì đang chạy PyCharm nên kết nối vào localhost
# - :5432         : port đã map trong docker-compose

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()