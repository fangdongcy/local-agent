from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..database.database import get_db
from ..models.models import Coupon, UserCoupon, User
from ..schemas.schemas import CouponCreate, Coupon as CouponSchema, UserCoupon as UserCouponSchema
from .auth import get_current_user

router = APIRouter()

@router.post("/coupons/", response_model=CouponSchema)
def create_coupon(coupon: CouponCreate, db: Session = Depends(get_db)):
    db_coupon = Coupon(**coupon.model_dump())
    db.add(db_coupon)
    db.commit()
    db.refresh(db_coupon)
    return db_coupon

@router.get("/coupons/", response_model=List[CouponSchema])
def read_coupons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    coupons = db.query(Coupon).offset(skip).limit(limit).all()
    return coupons

@router.post("/coupons/{coupon_code}/claim", response_model=UserCouponSchema)
def claim_coupon(
    coupon_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 检查优惠券是否存在且有效
    coupon = db.query(Coupon).filter(Coupon.code == coupon_code).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    
    if not coupon.is_active:
        raise HTTPException(status_code=400, detail="Coupon is not active")
    
    if datetime.utcnow() < coupon.start_date or datetime.utcnow() > coupon.end_date:
        raise HTTPException(status_code=400, detail="Coupon is not valid at this time")
    
    # 检查用户是否已经领取过
    existing_user_coupon = db.query(UserCoupon).filter(
        UserCoupon.user_id == current_user.id,
        UserCoupon.coupon_id == coupon.id
    ).first()
    
    if existing_user_coupon:
        raise HTTPException(status_code=400, detail="You have already claimed this coupon")
    
    # 创建用户优惠券
    user_coupon = UserCoupon(
        user_id=current_user.id,
        coupon_id=coupon.id
    )
    db.add(user_coupon)
    db.commit()
    db.refresh(user_coupon)
    return user_coupon

@router.get("/users/me/coupons", response_model=List[UserCouponSchema])
def read_user_coupons(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return current_user.coupons 