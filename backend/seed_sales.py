import random
from datetime import date, timedelta

from sqlmodel import Session, select

from database import engine
from models import Product, Sale


def generate_sale_quantity(product_name: str, current_date: date) -> float:
    weekday = current_date.weekday()
    is_weekend = weekday >= 5

    if product_name in ["Oat Milk", "Almond Milk", "Soy Milk"]:
        return random.randint(45, 70) if is_weekend else random.randint(18, 30)

    if product_name in ["Espresso Beans", "House Blend Beans", "Colombia Beans", "Ethiopia Beans", "Decaf Beans"]:
        return random.randint(30, 50) if is_weekend else random.randint(15, 25)

    if product_name in ["Caramel Syrup", "Vanilla Syrup", "Hazelnut Syrup", "Chocolate Syrup"]:
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


def seed_sales():
    with Session(engine) as session:
        existing_sales = session.exec(select(Sale)).first()
        if existing_sales:
            print("Sales data already exists. Skipping sales seed.")
            return

        products = session.exec(select(Product)).all()

        if not products:
            print("No products found. Run init_db.py first.")
            return

        today = date.today()
        start_date = today - timedelta(days=29)

        sales_to_add = []

        for single_date in (start_date + timedelta(days=i) for i in range(30)):
            for product in products:
                quantity = generate_sale_quantity(product.name, single_date)
                unit_price = round(product.unit_cost * random.uniform(1.8, 2.4), 2)

                sales_to_add.append(
                    Sale(
                        product_id=product.id,
                        quantity=quantity,
                        date=single_date,
                        unit_price=unit_price,
                    )
                )

        for sale in sales_to_add:
            session.add(sale)

        session.commit()
        print(f"{len(sales_to_add)} sales records inserted successfully.")


if __name__ == "__main__":
    seed_sales()
