from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
import uvicorn

from database import get_session, create_db_and_tables
from models import Product, Sale

app = FastAPI(title="Coffee Stock AI Analyzer")

@app.on_event("startup")
def on_startup():
   create_db_and_tables()

@app.get("/")
def root():
    return {"status": "Coffee AI Backend is Ready"}

@app.get("/api/products", response_model=List[Product])
def get_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

@app.get("/api/analyze/{product_id}")
def analyze_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    sales = session.exec(
        select(Sale).where(Sale.product_id == product_id)
    ).all()

    if not sales:
        return {
            "product": product.name,
            "current_stock": product.current_stock,
            "message": "No sales data found for this product."
        }


    last_sales = sales[-7:] if len(sales) >= 7 else sales
    avg_sales = sum(s.quantity for s in last_sales) / len(last_sales)

    recommendation = "Stok Durumu İyi"
    if product.current_stock < avg_sales * 3:
        recommendation = "Stok azalıyor, sipariş vermeyi düşünün!"

    return {
        "product_name": product.name,
        "current_stock": product.current_stock,
        "average_daily_sales": round(avg_sales, 2),
        "recommendation": recommendation
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
