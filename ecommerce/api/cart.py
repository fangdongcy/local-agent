from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from ..models.models import CartItem, Product
from ..schemas.schemas import CartItemCreate, CartItem as CartItemSchema

router = APIRouter()

@router.post("/cart/items/", response_model=CartItemSchema)
def add_to_cart(cart_item: CartItemCreate, db: Session = Depends(get_db)):
    # 检查商品是否存在
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # 检查库存
    if product.stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    # 创建购物车项
    db_cart_item = CartItem(**cart_item.model_dump())
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

@router.get("/cart/items/", response_model=List[CartItemSchema])
def get_cart_items(db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).all()
    return cart_items

@router.put("/cart/items/{item_id}", response_model=CartItemSchema)
def update_cart_item(item_id: int, cart_item: CartItemCreate, db: Session = Depends(get_db)):
    db_cart_item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    # 检查商品库存
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < cart_item.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    for key, value in cart_item.model_dump().items():
        setattr(db_cart_item, key, value)
    
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

@router.delete("/cart/items/{item_id}")
def remove_from_cart(item_id: int, db: Session = Depends(get_db)):
    db_cart_item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not db_cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(db_cart_item)
    db.commit()
    return {"message": "Item removed from cart successfully"} 