from datetime import date
import random

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from sqlalchemy import func

from database import get_session
from models import Product, Sale, Waste

try:
    from ai_rate_limiter import ai_cache
except ImportError:
    ai_cache = None

router = APIRouter(prefix="/api/stock", tags=["Stock Simulation"])


def generate_today_sale_quantity(product_name: str) -> float:
    weekday = date.today().weekday()
    is_weekend = weekday >= 5

    if product_name in ["Oat Milk", "Almond Milk", "Soy Milk"]:
        return random.randint(45, 70) if is_weekend else random.randint(18, 30)

    if product_name in [
        "Espresso Beans",
        "House Blend Beans",
        "Colombia Beans",
        "Ethiopia Beans",
        "Decaf Beans",
    ]:
        return random.randint(30, 50) if is_weekend else random.randint(15, 25)

    if product_name in [
        "Caramel Syrup",
        "Vanilla Syrup",
        "Hazelnut Syrup",
        "Chocolate Syrup",
    ]:
        return random.randint(10, 20) if is_weekend else random.randint(5, 12)

    if product_name in ["Paper Filters", "Coffee Cups", "Coffee Lids", "Sugar Packets"]:
        return random.randint(40, 65) if is_weekend else random.randint(20, 35)

    if product_name in ["Matcha Powder", "Cocoa Powder"]:
        return random.randint(8, 18) if is_weekend else random.randint(4, 10)

    if product_name == "Ice Cubes":
        return random.randint(50, 80) if is_weekend else random.randint(20, 40)

    if product_name == "Whole Milk":
        return random.randint(35, 55) if is_weekend else random.randint(20, 30)

    return random.randint(10, 20) if is_weekend else random.randint(5, 10)


def generate_waste_quantity(product_name: str) -> float:
    if product_name in ["Whole Milk", "Oat Milk", "Almond Milk", "Soy Milk"]:
        return random.randint(0, 3)

    if product_name == "Ice Cubes":
        return random.randint(0, 4)

    if "Syrup" in product_name:
        return random.randint(0, 1)

    return random.randint(0, 2)


@router.post("/simulate-day")
def simulate_one_day(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()

    if not products:
        raise HTTPException(status_code=404, detail="No products found.")

    results = []

    for product in products:
        requested_sale_qty = generate_today_sale_quantity(product.name)
        requested_waste_qty = generate_waste_quantity(product.name)

        initial_stock = product.current_stock

        actual_sold_qty = min(initial_stock, requested_sale_qty)
        remaining_after_sale = initial_stock - actual_sold_qty
        actual_waste_qty = min(remaining_after_sale, requested_waste_qty)

        product.current_stock = initial_stock - actual_sold_qty - actual_waste_qty

        if actual_sold_qty > 0:
            unit_price = round(product.unit_cost * random.uniform(1.8, 2.4), 2)
            sale = Sale(
                product_id=product.id,
                quantity=actual_sold_qty,
                date=date.today(),
                unit_price=unit_price,
            )
            session.add(sale)

        if actual_waste_qty > 0:
            waste = Waste(
                product_id=product.id,
                quantity=actual_waste_qty,
                date=date.today(),
                reason="Daily spoilage / operational waste",
            )
            session.add(waste)

        if ai_cache:
            ai_cache.invalidate(product.name)

        results.append({
            "product_id": product.id,
            "product_name": product.name,
            "sold": actual_sold_qty,
            "waste": actual_waste_qty,
            "new_stock": product.current_stock,
            "actual_reduction": actual_sold_qty + actual_waste_qty,
        })

    session.commit()

    return {
        "message": "One day simulation completed successfully.",
        "results": results,
    }

@router.post("/restock/{product_id}")
def restock_product(product_id: int, quantity: float, session: Session = Depends(get_session)):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0.")

    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    product.current_stock += quantity

    if ai_cache:
        ai_cache.invalidate(product.name)

    session.commit()
    session.refresh(product)

    return {
        "message": f"{product.name} restocked successfully.",
        "product_id": product.id,
        "product_name": product.name,
        "new_stock": product.current_stock,
    }

@router.post("/reset-stocks")
def reset_stocks(session: Session = Depends(get_session)):
    initial_stocks = {
        "Espresso Beans": 120,
        "House Blend Beans": 100,
        "Colombia Beans": 90,
        "Ethiopia Beans": 80,
        "Decaf Beans": 70,
        "Whole Milk": 60,
        "Oat Milk": 50,
        "Almond Milk": 40,
        "Soy Milk": 40,
        "Caramel Syrup": 25,
        "Vanilla Syrup": 25,
        "Hazelnut Syrup": 20,
        "Chocolate Syrup": 20,
        "Matcha Powder": 15,
        "Cocoa Powder": 20,
        "Sugar Packets": 500,
        "Paper Filters": 300,
        "Coffee Cups": 400,
        "Coffee Lids": 400,
        "Ice Cubes": 100
    }

    products = session.exec(select(Product)).all()

    for product in products:
        if product.name in initial_stocks:
            product.current_stock = initial_stocks[product.name]
            session.add(product)

    session.commit()

    return {"message": "Stocks reset successfully"}

@router.get("/products")
def get_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

@router.get("/dashboard-summary")
def get_dashboard_summary(session: Session = Depends(get_session)):
    total_sales_qty = session.exec(select(func.sum(Sale.quantity))).one() or 0
    total_waste_qty = session.exec(select(func.sum(Waste.quantity))).one() or 0

    critical_products = session.exec(
        select(Product).where(Product.current_stock <= Product.reorder_level)
    ).all()
    critical_count = len(critical_products)

    total_products = len(session.exec(select(Product)).all())

    return {
        "total_sales": round(float(total_sales_qty), 2),
        "total_waste": round(float(total_waste_qty), 2),
        "critical_stock_count": critical_count,
        "total_products": total_products,
        "waste_ratio": round((float(total_waste_qty) / float(total_sales_qty) * 100), 2) if total_sales_qty and total_sales_qty > 0 else 0,
        "critical_items": [p.name for p in critical_products]
    }
