from sqlmodel import Session, select

from database import create_db_and_tables, engine
from models import Supplier, Product


def seed_suppliers(session: Session):
    existing_supplier = session.exec(select(Supplier)).first()
    if existing_supplier:
        print("Suppliers already exist, skipping supplier seed")
        return

    suppliers = [
        Supplier(
            name="BeanCraft Supply",
            contact_email="sales@beancraft.com",
            phone="555-1001",
            address="Istanbul"
        ),
        Supplier(
            name="MilkFlow Distributors",
            contact_email="orders@milkflow.com",
            phone="555-1002",
            address="Istanbul"
        ),
        Supplier(
            name="SweetSource Syrups",
            contact_email="contact@sweetsource.com",
            phone="555-1003",
            address="Istanbul"
        ),
        Supplier(
            name="Cafe Essentials Co",
            contact_email="support@cafeessentials.com",
            phone="555-1004",
            address="Istanbul"
        ),
    ]

    for supplier in suppliers:
        session.add(supplier)

    session.commit()
    print("Suppliers inserted successfully")


def seed_products(session: Session):
    existing_product = session.exec(select(Product)).first()
    if existing_product:
        print("Products already exist, skipping product seed")
        return

    suppliers = session.exec(select(Supplier)).all()
    supplier_map = {supplier.name: supplier.id for supplier in suppliers}

    products = [
        Product(
            name="Espresso Beans",
            category="Beans",
            current_stock=18,
            unit="kg",
            unit_cost=520,
            supplier_id=supplier_map["BeanCraft Supply"],
            reorder_level=8,
        ),
        Product(
            name="House Blend Beans",
            category="Beans",
            current_stock=15,
            unit="kg",
            unit_cost=480,
            supplier_id=supplier_map["BeanCraft Supply"],
            reorder_level=7,
        ),
        Product(
            name="Colombia Beans",
            category="Beans",
            current_stock=12,
            unit="kg",
            unit_cost=540,
            supplier_id=supplier_map["BeanCraft Supply"],
            reorder_level=6,
        ),
        Product(
            name="Ethiopia Beans",
            category="Beans",
            current_stock=10,
            unit="kg",
            unit_cost=560,
            supplier_id=supplier_map["BeanCraft Supply"],
            reorder_level=5,
        ),
        Product(
            name="Decaf Beans",
            category="Beans",
            current_stock=8,
            unit="kg",
            unit_cost=500,
            supplier_id=supplier_map["BeanCraft Supply"],
            reorder_level=4,
        ),
        Product(
            name="Whole Milk",
            category="Milk",
            current_stock=30,
            unit="liter",
            unit_cost=32,
            supplier_id=supplier_map["MilkFlow Distributors"],
            reorder_level=10,
        ),
        Product(
            name="Oat Milk",
            category="Milk",
            current_stock=22,
            unit="liter",
            unit_cost=45,
            supplier_id=supplier_map["MilkFlow Distributors"],
            reorder_level=8,
        ),
        Product(
            name="Almond Milk",
            category="Milk",
            current_stock=18,
            unit="liter",
            unit_cost=48,
            supplier_id=supplier_map["MilkFlow Distributors"],
            reorder_level=7,
        ),
        Product(
            name="Soy Milk",
            category="Milk",
            current_stock=16,
            unit="liter",
            unit_cost=40,
            supplier_id=supplier_map["MilkFlow Distributors"],
            reorder_level=6,
        ),
        Product(
            name="Caramel Syrup",
            category="Syrup",
            current_stock=14,
            unit="bottle",
            unit_cost=85,
            supplier_id=supplier_map["SweetSource Syrups"],
            reorder_level=5,
        ),
        Product(
            name="Vanilla Syrup",
            category="Syrup",
            current_stock=13,
            unit="bottle",
            unit_cost=82,
            supplier_id=supplier_map["SweetSource Syrups"],
            reorder_level=5,
        ),
        Product(
            name="Hazelnut Syrup",
            category="Syrup",
            current_stock=11,
            unit="bottle",
            unit_cost=88,
            supplier_id=supplier_map["SweetSource Syrups"],
            reorder_level=4,
        ),
        Product(
            name="Chocolate Syrup",
            category="Syrup",
            current_stock=12,
            unit="bottle",
            unit_cost=90,
            supplier_id=supplier_map["SweetSource Syrups"],
            reorder_level=4,
        ),
        Product(
            name="Matcha Powder",
            category="Powder",
            current_stock=7,
            unit="kg",
            unit_cost=650,
            supplier_id=supplier_map["Cafe Essentials Co"],
            reorder_level=3,
        ),
        Product(
            name="Cocoa Powder",
            category="Powder",
            current_stock=9,
            unit="kg",
            unit_cost=270,
            supplier_id=supplier_map["Cafe Essentials Co"],
            reorder_level=4,
        ),
        Product(
            name="Sugar Packets",
            category="Consumable",
            current_stock=400,
            unit="piece",
            unit_cost=0.4,
            supplier_id=supplier_map["Cafe Essentials Co"],
            reorder_level=100,
        ),
        Product(
            name="Paper Filters",
            category="Consumable",
            current_stock=250,
            unit="piece",
            unit_cost=1.5,
            supplier_id=supplier_map["Cafe Essentials Co"],
            reorder_level=80,
        ),
        Product(
            name="Coffee Cups",
            category="Consumable",
            current_stock=300,
            unit="piece",
            unit_cost=1.8,
            supplier_id=supplier_map["Cafe Essentials Co"],
            reorder_level=100,
        ),
        Product(
            name="Coffee Lids",
            category="Consumable",
            current_stock=300,
            unit="piece",
            unit_cost=0.9,
            supplier_id=supplier_map["Cafe Essentials Co"],
            reorder_level=100,
        ),
        Product(
            name="Ice Cubes",
            category="Consumable",
            current_stock=40,
            unit="kg",
            unit_cost=12,
            supplier_id=supplier_map["Cafe Essentials Co"],
            reorder_level=15,
        ),
    ]

    for product in products:
        session.add(product)

    session.commit()
    print("Products inserted successfully")


if __name__ == "__main__":
    create_db_and_tables()

    with Session(engine) as session:
        seed_suppliers(session)
        seed_products(session)