from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from database import get_session
from models import Sale, Waste, Supplier, PurchaseOrder # Tüm log tabloları

router = APIRouter(prefix="/api/logs", tags=["System Logs & History"])

@router.get("/sales")
def get_sales_history(session: Session = Depends(get_session)):
    """Tüm satış geçmişini en yeniden en eskiye doğru listeler"""
    statement = select(Sale).order_by(Sale.date.desc())
    return session.exec(statement).all()

@router.get("/waste")
def get_waste_history(session: Session = Depends(get_session)):
    """Tüm atık/israf kayıtlarını listeler"""
    statement = select(Waste).order_by(Waste.date.desc())
    return session.exec(statement).all()

@router.get("/suppliers")
def get_suppliers_list(session: Session = Depends(get_session)):
    """Sistemdeki kayıtlı tüm tedarikçileri getirir"""
    return session.exec(select(Supplier)).all()

@router.get("/purchase-orders")
def get_purchase_orders(session: Session = Depends(get_session)):
    """Verilen ham madde siparişlerinin durumunu listeler"""
    statement = select(PurchaseOrder).order_by(PurchaseOrder.order_date.desc())
    return session.exec(statement).all()