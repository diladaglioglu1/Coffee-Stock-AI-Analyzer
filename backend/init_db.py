from database import create_db_and_tables
from models import Product
from database import get_session


def seed_products():

    products = [
        Product(name="Espresso Beans", current_stock=18, unit="kg", unit_cost=520),
        Product(name="House Blend Beans", current_stock=15, unit="kg", unit_cost=480),
        Product(name="Colombia Beans", current_stock=12, unit="kg", unit_cost=540),
        Product(name="Ethiopia Beans", current_stock=10, unit="kg", unit_cost=560),
        Product(name="Decaf Beans", current_stock=8, unit="kg", unit_cost=500),

        Product(name="Whole Milk", current_stock=30, unit="liter", unit_cost=32),
        Product(name="Oat Milk", current_stock=22, unit="liter", unit_cost=45),
        Product(name="Almond Milk", current_stock=18, unit="liter", unit_cost=48),
        Product(name="Soy Milk", current_stock=16, unit="liter", unit_cost=40),

        Product(name="Caramel Syrup", current_stock=14, unit="bottle", unit_cost=85),
        Product(name="Vanilla Syrup", current_stock=13, unit="bottle", unit_cost=82),
        Product(name="Hazelnut Syrup", current_stock=11, unit="bottle", unit_cost=88),
        Product(name="Chocolate Syrup", current_stock=12, unit="bottle", unit_cost=90),

        Product(name="Matcha Powder", current_stock=7, unit="kg", unit_cost=650),
        Product(name="Cocoa Powder", current_stock=9, unit="kg", unit_cost=270),
        Product(name="Sugar Packets", current_stock=400, unit="piece", unit_cost=0.4),

        Product(name="Paper Filters", current_stock=250, unit="piece", unit_cost=1.5),
        Product(name="Coffee Cups", current_stock=300, unit="piece", unit_cost=1.8),
        Product(name="Coffee Lids", current_stock=300, unit="piece", unit_cost=0.9),
        Product(name="Ice Cubes", current_stock=40, unit="kg", unit_cost=12),
    ]

    with get_session() as session:
        for product in products:
            session.add(product)
        session.commit()

    print("Products inserted successfully")


if __name__ == "__main__":
    create_db_and_tables()
    seed_products()