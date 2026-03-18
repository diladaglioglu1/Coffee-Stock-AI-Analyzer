from datetime import date, datetime
from sqlmodel import SQLModel, Field


class Supplier(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    contact_email: str
    phone: str
    address: str | None = None


class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    category: str = "General"
    current_stock: float
    unit: str
    unit_cost: float
    supplier_id: int | None = Field(default=None, foreign_key="supplier.id")
    reorder_level: float = 0
    is_active: bool = True


class Sale(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    quantity: float
    date: date
    unit_price: float = 0


class Waste(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    quantity: float
    date: date
    reason: str


class PurchaseOrder(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    supplier_id: int = Field(foreign_key="supplier.id")
    order_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"
    total_cost: float = 0


class PurchaseOrderItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    purchase_order_id: int = Field(foreign_key="purchaseorder.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: float
    unit_cost: float