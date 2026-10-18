from .database import Base, engine, SessionLocal
from . import models as m


def get_attr(db, cache, tipe, nilai):
    """Ambil atau buat nilai atribut (satu baris per pasangan tipe+nilai)."""
    if (tipe, nilai) not in cache:
        row = m.Attribute(tipe_atribut=tipe, nilai_atribut=nilai)
        db.add(row)
        db.flush()
        cache[(tipe, nilai)] = row
    return cache[(tipe, nilai)]


def add_product(db, cache, model, ptype, data, attrs):
    """Simpan produk lalu hubungkan dengan atributnya."""
    p = model(**data)
    db.add(p)
    db.flush()
    for tipe, vals in attrs.items():
        for v in (vals if isinstance(vals, list) else [vals]):
            db.add(m.ProductAttribute(
                product_type=ptype,
                product_id=p.id,
                attribute_id=get_attr(db, cache, tipe, v).id,
            ))
    return p


def run():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    cache = {}

    cats = {n: m.Category(nama_kategori=n) for n in ["Atasan", "Bawahan", "Dress", "Outer"]}
    db.add_all(cats.values())
    db.flush()

    # ===== PRODUK HIGH-END (harga contoh: ganti dengan harga asli) =====
    add_product(db, cache, m.HighEndProduct, "high_end",
        dict(brand="Uniqlo", nama_produk="Work Jacket", harga=799000,
             category_id=cats["Outer"].id, image_url=None),
        {"bahan": "katun twill", "fit": "boxy", "warna": "olive", "style": "utility"})

    add_product(db, cache, m.HighEndProduct, "high_end",
        dict(brand="H&M", nama_produk="Satin Slip Dress", harga=699000,
             category_id=cats["Dress"].id, image_url=None),
        {"bahan": "satin", "fit": "slip", "warna": "merah marun", "style": "elegan"})

    add_product(db, cache, m.HighEndProduct, "high_end",
        dict(brand="Massimo Dutti", nama_produk="Wide Leg Trousers", harga=1799000,
             category_id=cats["Bawahan"].id, image_url=None),
        {"bahan": "crepe", "fit": "wide leg", "warna": "hitam", "style": "formal"})

    # ===== PRODUK DUPE UNTUK WORK JACKET =====
    # DATA SEMENTARA agar sistem bisa dites. Sebelum dikumpulkan, ganti brand_lokal,
    # nama_produk, harga, dan atribut dengan produk ASLI dari Shopee/Tokopedia.
    outer = cats["Outer"].id
    add_product(db, cache, m.DupeProduct, "dupe",
        dict(brand_lokal="ISI_BRAND_LOKAL_A", nama_produk="ISI_NAMA_A", harga=289000,
             affiliate_url=None, category_id=outer, image_url=None),
        {"bahan": "katun twill", "fit": "boxy", "warna": "olive", "style": "workwear"})

    add_product(db, cache, m.DupeProduct, "dupe",
        dict(brand_lokal="ISI_BRAND_LOKAL_B", nama_produk="ISI_NAMA_B", harga=329000,
             affiliate_url=None, category_id=outer, image_url=None),
        {"bahan": "katun canvas", "fit": "boxy", "warna": "olive", "style": "utility"})

    add_product(db, cache, m.DupeProduct, "dupe",
        dict(brand_lokal="ISI_BRAND_LOKAL_C", nama_produk="ISI_NAMA_C", harga=219000,
             affiliate_url=None, category_id=outer, image_url=None),
        {"bahan": "katun twill", "fit": "regular", "warna": "hijau army", "style": "utility"})

    add_product(db, cache, m.DupeProduct, "dupe",
        dict(brand_lokal="ISI_BRAND_LOKAL_D", nama_produk="ISI_NAMA_D", harga=199000,
             affiliate_url=None, category_id=outer, image_url=None),
        {"bahan": "katun canvas", "fit": "slim", "warna": "hitam", "style": "casual"})

    db.commit()
    print("Seed selesai: high-end =", db.query(m.HighEndProduct).count(),
          "| dupe =", db.query(m.DupeProduct).count())
    db.close()


if __name__ == "__main__":
    run()