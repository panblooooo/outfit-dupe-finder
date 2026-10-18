from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..services.catalog import attrs_of

router = APIRouter(prefix="/products", tags=["RF-003 Pencarian Produk"])

@router.get("")
def list_products(
    q: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(8, ge=1, le=48),
    db: Session = Depends(get_db)
):
    H = models.HighEndProduct
    stmt = select(H)
    
    if q:
        stmt = stmt.where(
            or_(
                H.nama_produk.ilike(f"%{q}%"),
                H.brand.ilike(f"%{q}%")
            )
        )

    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    rows = db.scalars(stmt.order_by(H.id).offset((page - 1) * per_page).limit(per_page)).all()

    return {
        "data": [
            {
                "id": p.id,
                "brand": p.brand,
                "nama_produk": p.nama_produk,
                "harga": p.harga,
                "image_url": p.image_url
            }
            for p in rows
        ],
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total
        }
    }

@router.get("/{product_id}")
def product_detail(product_id: int, db: Session = Depends(get_db)):
    p = db.get(models.HighEndProduct, product_id)
    if not p:
        raise HTTPException(404, "Produk tidak ditemukan")
    return {
        "id": p.id, "brand": p.brand, "nama_produk": p.nama_produk,
        "harga": p.harga, "image_url": p.image_url,
        "attributes": attrs_of(db, "high_end", p.id),
        "budget_range": {"min": 100_000, "max": p.harga - 1},
    }