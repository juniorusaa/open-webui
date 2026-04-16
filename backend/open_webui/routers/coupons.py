import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from sqlalchemy.orm import Session
from open_webui.internal.db import get_session

from open_webui.models.coupons import (
    CouponModel,
    CouponListResponse,
    CouponResponse,
    CreateCouponForm,
    CreateBulkCouponsForm,
    RedeemCouponForm,
    Coupons,
)

from open_webui.models.users import Users, UserModel
from open_webui.models.groups import Groups

from open_webui.constants import ERROR_MESSAGES

from open_webui.utils.auth import get_admin_user, get_verified_user

log = logging.getLogger(__name__)

router = APIRouter()


############################
# GetCoupons
############################


@router.get('/', response_model=CouponListResponse)
async def get_coupons(
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    user=Depends(get_admin_user),
    db: Session = Depends(get_session),
):
    """Get all coupons (admin only)."""
    result = Coupons.get_coupons(skip=skip, limit=limit, db=db)
    return result


############################
# CreateCoupon
############################


@router.post('/create', response_model=CouponResponse)
async def create_coupon(
    form_data: CreateCouponForm,
    user=Depends(get_admin_user),
    db: Session = Depends(get_session),
):
    """Create a single coupon (admin only)."""
    # Check if code already exists
    existing = Coupons.get_coupon_by_code(form_data.code, db=db)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Coupon code already exists',
        )
    
    coupon = Coupons.insert_coupon(
        code=form_data.code,
        days=form_data.days,
        max_usage=form_data.max_usage,
        note=form_data.note,
        db=db,
    )
    
    if coupon:
        return coupon
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ERROR_MESSAGES.DEFAULT(),
    )


############################
# CreateBulkCoupons
############################


@router.post('/create-bulk', response_model=CouponListResponse)
async def create_bulk_coupons(
    form_data: CreateBulkCouponsForm,
    user=Depends(get_admin_user),
    db: Session = Depends(get_session),
):
    """Create multiple coupons with auto-generated codes (admin only)."""
    if form_data.count < 1 or form_data.count > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Count must be between 1 and 1000',
        )
    
    coupons = Coupons.create_bulk_coupons(
        count=form_data.count,
        days=form_data.days,
        max_usage=form_data.max_usage,
        prefix=form_data.prefix or '',
        note=form_data.note,
        db=db,
    )
    
    return {
        'coupons': coupons,
        'total': len(coupons),
    }


############################
# RedeemCoupon
############################


@router.post('/redeem', response_model=UserModel)
async def redeem_coupon(
    form_data: RedeemCouponForm,
    user=Depends(get_verified_user),
    db: Session = Depends(get_session),
):
    """Redeem a coupon (any authenticated user)."""
    # Get the coupon
    coupon, error = Coupons.redeem_coupon(form_data.code, user.id, db=db)
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )
    
    # Add the coupon's days to the user's expires_at
    updated_user = Users.add_days_to_user(user.id, coupon.days, db=db)
    
    if updated_user:
        return updated_user
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ERROR_MESSAGES.DEFAULT(),
    )


############################
# DeleteCoupon
############################


@router.delete('/{coupon_id}', response_model=bool)
async def delete_coupon(
    coupon_id: str,
    user=Depends(get_admin_user),
    db: Session = Depends(get_session),
):
    """Delete a coupon by ID (admin only)."""
    result = Coupons.delete_coupon_by_id(coupon_id, db=db)
    
    if result:
        return True
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ERROR_MESSAGES.NOT_FOUND,
    )
