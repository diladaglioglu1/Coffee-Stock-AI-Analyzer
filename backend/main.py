from fastapi import FastAPI
from sqlmodel import select

from database import get_session
from models import Product, Sale

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Coffee Inventory API running"}


@app.get("/api/products")
def get_products():
    with get_session() as session:
        products = session.exec(select(Product)).all()

        return [
            {
                "id": p.id,
                "name": p.name,
                "current_stock": p.current_stock,
                "unit": p.unit
            }
            for p in products
        ]


@app.get("/api/analyze/{product_id}")
def analyze_product(product_id: int):

    with get_session() as session:

        product = session.get(Product, product_id)

        if not product:
            return {"error": "Product not found"}

        sales = session.exec(
            select(Sale).where(Sale.product_id == product_id)
        ).all()

        if not sales:
            return {"message": "No sales data"}

        last_7_days_sales = sales[-7:]

        avg_sales = sum(s.quantity for s in last_7_days_sales) / len(last_7_days_sales)

        recommendation = "Stock level OK"

        if product.current_stock < avg_sales * 3:
            recommendation = "Stock may run out soon. Consider ordering more."

        return {
            "product": product.name,
            "current_stock": product.current_stock,
            "average_daily_sales": round(avg_sales, 2),
            "recommendation": recommendation
        }
        