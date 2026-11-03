from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

router = APIRouter(tags=["RF-008 Pengalihan Affiliate Link"])


@router.get("/go/{dupe_id}")
def go_to_store(dupe_id: int, ref: int | None = Query(None), db: Session = Depends(get_db)):
    """Catat klik lalu alihkan pengguna ke e-commerce mitra."""
    dupe = db.get(models.DupeProduct, dupe_id)
    if not dupe or not dupe.affiliate_url:
        raise HTTPException(404, "Tautan produk tidak tersedia")
    db.add(models.AffiliateClick(dupe_id=dupe.id, reference_id=ref))
    db.commit()
    return RedirectResponse(dupe.affiliate_url, status_code=302)


@router.get("/stats/clicks")
def click_stats(db: Session = Depends(get_db)):
    """Rekap jumlah klik per produk dupe (nantinya khusus admin)."""
    rows = db.execute(select(models.AffiliateClick.dupe_id, func.count())
                      .group_by(models.AffiliateClick.dupe_id)).all()
    return [{"dupe_id": d, "total_klik": n} for d, n in rows]