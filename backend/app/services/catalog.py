from sqlalchemy import select
from .. import models


def attrs_of(db, product_type, product_id):
    rows = db.execute(
        select(models.Attribute.tipe_atribut, models.Attribute.nilai_atribut)
        .join(models.ProductAttribute, models.ProductAttribute.attribute_id == models.Attribute.id)
        .where(models.ProductAttribute.product_type == product_type,
               models.ProductAttribute.product_id == product_id)).all()
    out = {}
    for tipe, nilai in rows:
        out.setdefault(tipe, []).append(nilai)
    return out


def all_attribute_pairs(db):
    return db.execute(select(models.Attribute.tipe_atribut, models.Attribute.nilai_atribut)).all()