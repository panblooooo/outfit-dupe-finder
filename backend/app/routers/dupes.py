from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..services.catalog import attrs_of, all_attribute_pairs
from ..services.similarity import build_vocab, find_dupes

router = APIRouter(prefix="/products", tags=["RF-004, RF-005, RF-006 Pencarian Dupe"])


@router.get("/{product_id}/dupes")
def get_dupes(product_id: int,
              max_price: int = Query(..., gt=0),
              limit: int = Query(3, ge=1, le=5),
              min_score: float = Query(0.5, ge=0, le=1),
              db: Session = Depends(get_db)):
    ref = db.get(models.HighEndProduct, product_id)
    if not ref:
        raise HTTPException(404, "Produk referensi tidak ditemukan")
    if max_price >= ref.harga:
        raise HTTPException(422, "max_price harus lebih kecil dari harga produk referensi")

    D = models.DupeProduct
    cands = db.scalars(select(D).where(
        D.category_id == ref.category_id,
        D.harga < ref.harga,
        D.harga <= max_price)).all()

    pool = [(c, attrs_of(db, "dupe", c.id)) for c in cands]
    attr_map = {c.id: a for c, a in pool}
    ranked = find_dupes(attrs_of(db, "high_end", ref.id), pool,
                        build_vocab(all_attribute_pairs(db)), limit, min_score)

    results = [{
        "rank": i, "id": c.id, "brand_lokal": c.brand_lokal, "nama_produk": c.nama_produk,
        "harga": c.harga, "image_url": c.image_url, "attributes": attr_map[c.id],
        "similarity": {"score": s, "percent": round(s * 100)},
    } for i, (s, c) in enumerate(ranked, 1)]

    return {
        "data": {"reference": {"id": ref.id, "nama_produk": ref.nama_produk, "harga": ref.harga},
                 "results": results},
        "meta": {"count": len(results), "max_price": max_price, "limit": limit, "min_score": min_score},
    }