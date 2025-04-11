from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import products, cart, auth, categories, reviews, coupons
from .database.database import engine
from .models import models

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-commerce API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(cart.router, prefix="/api/v1", tags=["cart"])
app.include_router(categories.router, prefix="/api/v1", tags=["categories"])
app.include_router(reviews.router, prefix="/api/v1", tags=["reviews"])
app.include_router(coupons.router, prefix="/api/v1", tags=["coupons"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the E-commerce API"} 