from __future__ import annotations
from datetime import date, timedelta
from sqlmodel import Session, select, func

try:
    from models import Product, Sale, Waste
except ImportError:
    from sqlmodel import SQLModel, Field
    from typing import Optional

    class Product(SQLModel, table=True):
        id:            Optional[int] = Field(default=None, primary_key=True)
        name:          str
        category:      str           = Field(default="General")
        current_stock: float         = Field(default=0)
        unit:          str           = Field(default="unit")
        unit_cost:     float         = Field(default=0.0)
        supplier_id:   Optional[int] = Field(default=None)
        reorder_level: float         = Field(default=0)
        is_active:     bool          = Field(default=True)

    class Sale(SQLModel, table=True):
        id:         Optional[int] = Field(default=None, primary_key=True)
        product_id: int           = Field(foreign_key="product.id")
        quantity:   float
        date:       date
        unit_price: float         = Field(default=0)

    class Waste(SQLModel, table=True):
        id:         Optional[int] = Field(default=None, primary_key=True)
        product_id: int           = Field(foreign_key="product.id")
        quantity:   float
        date:       date
        reason:     str


def get_avg_daily_sales(product_id: int, db: Session, days: int = 7) -> float:
    cutoff = date.today() - timedelta(days=days)

    result = db.exec(
        select(func.avg(Sale.quantity))
        .where(Sale.product_id == product_id)
        .where(Sale.date >= cutoff)
    ).first()

    return float(result) if result else 0.0


def get_product_with_ai_inputs(product_id: int, db: Session) -> dict | None:
    product = db.get(Product, product_id)
    if not product:
        return None

    avg_sales = get_avg_daily_sales(product_id, db)

    return {
        "id":             product.id,
        "name":           product.name,
        "category":       getattr(product, "category", "General"),
        "current_stock":  product.current_stock,
        "avg_sales":      avg_sales,
        "unit":           getattr(product, "unit", "unit"),
        "reorder_level":  getattr(product, "reorder_level", 0),
    }


def get_all_products_with_ai_inputs(db: Session) -> list[dict]:
    products = db.exec(
        select(Product).where(Product.is_active == True)
    ).all()

    return [
        {
            "id":            p.id,
            "name":          p.name,
            "category":      getattr(p, "category", "General"),
            "current_stock": p.current_stock,
            "avg_sales":     get_avg_daily_sales(p.id, db),
            "unit":          getattr(p, "unit", "unit"),
            "reorder_level": getattr(p, "reorder_level", 0),
        }
        for p in products
    ]


def log_ai_advice(product_id: int, advice: str, db: Session) -> None:
    pass
