# ai_db_bridge.py
# BrewIntelligence — AI ↔ Database Integration Bridge
# Rol: AI Specialist (Kişi 2) — Kişi 1 (DB) ile entegrasyon katmanı
# SWE314 W2: Relational Database + W3: Service Layer
#
# ⚠️  Kişi 1'in models.py'si hazır olduğunda sadece import satırını güncelle.
#     Köprünün geri kalanı değişmez.

from __future__ import annotations

from datetime import date, timedelta
from sqlmodel import Session, select, func

# ── Kişi 1'in modelleri gelince bu bloğu güncelle ─────────────────────────────
# Şu an: Kişi 1 henüz bitirmedi → stub modeller kullanıyoruz (test için).
# Sonra: Aşağıdaki try/except bloğunu sil, sadece gerçek importu bırak:
#
#   from models import Product, Sale, Waste
#
try:
    from models import Product, Sale, Waste          # Kişi 1 hazır olunca
except ImportError:
    # ── STUB MODELLER — sadece test/geliştirme için ───────────────────────────
    from sqlmodel import SQLModel, Field
    from typing import Optional

    class Product(SQLModel, table=True):
        id:            Optional[int] = Field(default=None, primary_key=True)
        name:          str
        current_stock: float         = Field(default=0)
        unit:          str           = Field(default="g")
        unit_cost:     float         = Field(default=0.0)

    class Sale(SQLModel, table=True):
        id:         Optional[int] = Field(default=None, primary_key=True)
        product_id: int           = Field(foreign_key="product.id")
        quantity:   float
        date:       date

    class Waste(SQLModel, table=True):
        id:         Optional[int] = Field(default=None, primary_key=True)
        product_id: int           = Field(foreign_key="product.id")
        quantity:   float
        date:       date
        reason:     str
# ─────────────────────────────────────────────────────────────────────────────


# ── Ortalama Günlük Satış Hesapla ─────────────────────────────────────────────
def get_avg_daily_sales(product_id: int, db: Session, days: int = 7) -> float:
    """
    Son `days` güne ait ortalama günlük satış miktarını döner.
    Kişi 1'in Sale tablosunu kullanır.
    """
    cutoff = date.today() - timedelta(days=days)

    result = db.exec(
        select(func.avg(Sale.quantity))
        .where(Sale.product_id == product_id)
        .where(Sale.date >= cutoff)
    ).first()

    return float(result) if result else 0.0


# ── Ürün + AI Verisi Birleşik Getir ───────────────────────────────────────────
def get_product_with_ai_inputs(product_id: int, db: Session) -> dict | None:
    """
    AI analizi için gereken tüm veriyi hazırlar.

    Returns:
        {"id", "name", "current_stock", "avg_sales", "unit"} veya None
    """
    product = db.get(Product, product_id)
    if not product:
        return None

    avg_sales = get_avg_daily_sales(product_id, db)

    return {
        "id":            product.id,
        "name":          product.name,
        "current_stock": product.current_stock,
        "avg_sales":     avg_sales,
        "unit":          getattr(product, "unit", "birim"),
    }


# ── Tüm Ürünler için Toplu Veri ───────────────────────────────────────────────
def get_all_products_with_ai_inputs(db: Session) -> list[dict]:
    """
    Dashboard'daki tüm ürünleri AI analizine hazır formatta döner.
    """
    products = db.exec(select(Product)).all()

    return [
        {
            "id":            p.id,
            "name":          p.name,
            "current_stock": p.current_stock,
            "avg_sales":     get_avg_daily_sales(p.id, db),
            "unit":          getattr(p, "unit", "birim"),
        }
        for p in products
    ]


# ── AI Sonucunu DB'ye Kaydet (opsiyonel) ──────────────────────────────────────
def log_ai_advice(product_id: int, advice: str, db: Session) -> None:
    """Opsiyonel: Kişi 1 AIAdviceLog modeli eklerse burayı aktif et."""
    pass