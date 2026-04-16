import time
from typing import Optional

from sqlalchemy.orm import Session
from open_webui.internal.db import Base, JSONField, get_db, get_db_context

from pydantic import BaseModel, ConfigDict
from sqlalchemy import (
    BigInteger,
    Column,
    String,
    Integer,
    JSON,
)

import uuid


####################
# Coupon DB Schema
####################


class Coupon(Base):
    __tablename__ = 'coupon'

    id = Column(String, primary_key=True, unique=True)
    code = Column(String, unique=True, nullable=False, index=True)
    days = Column(Integer, nullable=False)
    max_usage = Column(Integer, default=1)
    current_usage = Column(Integer, default=0)
    note = Column(String, nullable=True)
    created_at = Column(BigInteger, nullable=False)
    used_by = Column(JSON, nullable=True)


class CouponModel(BaseModel):
    id: str
    code: str
    days: int
    max_usage: int
    current_usage: int
    note: Optional[str] = None
    created_at: int  # timestamp in epoch
    used_by: Optional[list[str]] = None

    model_config = ConfigDict(from_attributes=True)


####################
# Forms
####################


class CreateCouponForm(BaseModel):
    code: str
    days: int
    max_usage: int = 1
    note: Optional[str] = None


class CreateBulkCouponsForm(BaseModel):
    count: int
    days: int
    max_usage: int = 1
    prefix: Optional[str] = ''
    note: Optional[str] = None


class RedeemCouponForm(BaseModel):
    code: str


class CouponListResponse(BaseModel):
    coupons: list[CouponModel]
    total: int


class CouponResponse(BaseModel):
    id: str
    code: str
    days: int
    max_usage: int
    current_usage: int
    note: Optional[str] = None
    created_at: int
    used_by: Optional[list[str]] = None


####################
# Coupons Table
####################


def generate_coupon_code(prefix: str = '') -> str:
    """Generate a random uppercase alphanumeric coupon code with optional prefix."""
    import random
    import string
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=8))
    return f'{prefix}{random_part}'


class CouponsTable:
    def insert_coupon(
        self,
        code: str,
        days: int,
        max_usage: int = 1,
        note: Optional[str] = None,
        db: Optional[Session] = None,
    ) -> Optional[CouponModel]:
        """Create a new coupon."""
        try:
            with get_db_context(db) as db:
                id = str(uuid.uuid4())
                coupon = CouponModel(
                    **{
                        'id': id,
                        'code': code.upper(),
                        'days': days,
                        'max_usage': max_usage,
                        'current_usage': 0,
                        'note': note,
                        'created_at': int(time.time()),
                        'used_by': [],
                    }
                )
                result = Coupon(**coupon.model_dump())
                db.add(result)
                db.commit()
                db.refresh(result)
                if result:
                    return coupon
                return None
        except Exception:
            return None

    def create_bulk_coupons(
        self,
        count: int,
        days: int,
        max_usage: int = 1,
        prefix: str = '',
        note: Optional[str] = None,
        db: Optional[Session] = None,
    ) -> list[CouponModel]:
        """Create multiple coupons with auto-generated codes."""
        created_coupons = []
        with get_db_context(db) as db:
            for _ in range(count):
                id = str(uuid.uuid4())
                code = generate_coupon_code(prefix)
                
                # Ensure code is unique
                existing = db.query(Coupon).filter_by(code=code).first()
                attempts = 0
                while existing and attempts < 10:
                    code = generate_coupon_code(prefix)
                    existing = db.query(Coupon).filter_by(code=code).first()
                    attempts += 1
                
                if existing:
                    continue  # Skip if we couldn't generate a unique code
                
                coupon = CouponModel(
                    **{
                        'id': id,
                        'code': code.upper(),
                        'days': days,
                        'max_usage': max_usage,
                        'current_usage': 0,
                        'note': note,
                        'created_at': int(time.time()),
                        'used_by': [],
                    }
                )
                result = Coupon(**coupon.model_dump())
                db.add(result)
                created_coupons.append(coupon)
            
            db.commit()
            return created_coupons

    def get_coupon_by_code(self, code: str, db: Optional[Session] = None) -> Optional[CouponModel]:
        """Get a coupon by its code."""
        try:
            with get_db_context(db) as db:
                coupon = db.query(Coupon).filter_by(code=code.upper()).first()
                return CouponModel.model_validate(coupon) if coupon else None
        except Exception:
            return None

    def get_coupon_by_id(self, id: str, db: Optional[Session] = None) -> Optional[CouponModel]:
        """Get a coupon by its ID."""
        try:
            with get_db_context(db) as db:
                coupon = db.query(Coupon).filter_by(id=id).first()
                return CouponModel.model_validate(coupon) if coupon else None
        except Exception:
            return None

    def get_coupons(
        self,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        db: Optional[Session] = None,
    ) -> dict:
        """Get all coupons with pagination."""
        with get_db_context(db) as db:
            query = db.query(Coupon)
            total = query.count()
            
            if skip is not None:
                query = query.offset(skip)
            if limit is not None:
                query = query.limit(limit)
            
            coupons = query.all()
            return {
                'coupons': [CouponModel.model_validate(coupon) for coupon in coupons],
                'total': total,
            }

    def redeem_coupon(
        self,
        code: str,
        user_id: str,
        db: Optional[Session] = None,
    ) -> tuple[Optional[CouponModel], Optional[str]]:
        """
        Redeem a coupon for a user.
        Returns (coupon, error_message).
        """
        try:
            with get_db_context(db) as db:
                coupon = db.query(Coupon).filter_by(code=code.upper()).first()
                if not coupon:
                    return None, 'Coupon not found'
                
                # Check if max usage reached
                if coupon.current_usage >= coupon.max_usage:
                    return None, 'Coupon usage limit reached'
                
                # Check if user already used this coupon
                used_by = coupon.used_by or []
                if user_id in used_by:
                    return None, 'You have already used this coupon'
                
                # Increment usage and add user to used_by list
                coupon.current_usage += 1
                used_by.append(user_id)
                coupon.used_by = used_by
                
                db.commit()
                db.refresh(coupon)
                
                return CouponModel.model_validate(coupon), None
        except Exception:
            return None, 'Error redeeming coupon'

    def delete_coupon_by_id(self, id: str, db: Optional[Session] = None) -> bool:
        """Delete a coupon by ID."""
        try:
            with get_db_context(db) as db:
                db.query(Coupon).filter_by(id=id).delete()
                db.commit()
                return True
        except Exception:
            return False


Coupons = CouponsTable()
