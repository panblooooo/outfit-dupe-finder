from sqlalchemy import String, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    nama_kategori: Mapped[str] = mapped_column(String(60), unique=True)
    deskripsi: Mapped[str | None] = mapped_column(Text, nullable=True)

class HighEndProduct(Base):
    __tablename__ = "high_end_products"
    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(80))
    nama_produk: Mapped[str] = mapped_column(String(160))
    harga: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[Category] = relationship()

class DupeProduct(Base):
    __tablename__ = "dupe_products"
    id: Mapped[int] = mapped_column(primary_key=True)
    brand_lokal: Mapped[str] = mapped_column(String(80))
    nama_produk: Mapped[str] = mapped_column(String(160))
    harga: Mapped[int] = mapped_column(Integer)
    affiliate_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[Category] = relationship()

class Attribute(Base):
    __tablename__ = "attributes"
    id: Mapped[int] = mapped_column(primary_key=True)
    tipe_atribut: Mapped[str] = mapped_column(String(20))   # bahan, warna, fit, style
    nilai_atribut: Mapped[str] = mapped_column(String(60))
    bobot: Mapped[float] = mapped_column(Float, default=0)

class ProductAttribute(Base):
    __tablename__ = "product_attributes"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_type: Mapped[str] = mapped_column(String(10))   # "high_end" atau "dupe"
    product_id: Mapped[int] = mapped_column(Integer)
    attribute_id: Mapped[int] = mapped_column(ForeignKey("attributes.id"))