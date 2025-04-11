# E-commerce API

这是一个基于FastAPI的电商系统后端API。

## 功能特点

- 商品管理（添加、修改、删除、查询）
- 购物车功能
- RESTful API设计
- 自动API文档

## 安装

1. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行

```bash
uvicorn main:app --reload
```

访问 http://localhost:8000/docs 查看API文档。

## API端点

### 商品管理
- GET /api/v1/products/ - 获取商品列表
- GET /api/v1/products/{product_id} - 获取商品详情
- POST /api/v1/products/ - 创建新商品
- PUT /api/v1/products/{product_id} - 更新商品
- DELETE /api/v1/products/{product_id} - 删除商品

### 购物车
- GET /api/v1/cart/items/ - 获取购物车商品
- POST /api/v1/cart/items/ - 添加商品到购物车
- PUT /api/v1/cart/items/{item_id} - 更新购物车商品
- DELETE /api/v1/cart/items/{item_id} - 从购物车移除商品 