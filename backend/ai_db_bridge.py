from __future__ import annotations
from datetime import date, timedelta
from sqlmodel import Session, select, func
from models import Product, Sale, Waste, Supplier 


def get_avg_daily_sales(product_id: int, db: Session, days: int = 7) -> float:
    cutoff = date.today() - timedelta(days=days)
    total_sales = db.exec(
        select(func.sum(Sale.quantity))
        .where(Sale.product_id == product_id)
        .where(Sale.date >= cutoff)
    ).one() or 0.0

    return float(total_sales / days)


def get_avg_daily_waste(product_id: int, db: Session, days: int = 7) -> float:
    cutoff = date.today() - timedelta(days=days)
    total_waste = db.exec(
        select(func.sum(Waste.quantity))
        .where(Waste.product_id == product_id)
        .where(Waste.date >= cutoff)
    ).one() or 0.0

    return float(total_waste / days)


def get_product_with_ai_inputs(product_id: int, db: Session) -> dict | None:
    product = db.get(Product, product_id)
    if not product:
        return None

    avg_sales = get_avg_daily_sales(product_id, db)
    avg_waste = get_avg_daily_waste(product_id, db)

    return {
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "current_stock": product.current_stock,
        "unit": product.unit,
        "reorder_level": product.reorder_level,
        "avg_daily_sales": round(avg_sales, 2),
        "avg_daily_waste": round(avg_waste, 2),  # AI israfı görsün
        "is_critical": product.current_stock <= product.reorder_level
    }


def get_all_products_with_ai_inputs(db: Session) -> list[dict]:
    products = db.exec(
        select(Product).where(Product.is_active == True)
    ).all()

    return [get_product_with_ai_inputs(p.id, db) for p in products]


def log_ai_advice(product_id: int, advice: str, db: Session) -> None:
    pass
