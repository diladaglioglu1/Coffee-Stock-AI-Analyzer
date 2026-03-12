import random
from datetime import date, timedelta

from sqlmodel import select

from database import get_session
from models import Product, Waste


def generate_waste_quantity(product_name: str) -> float:
    if product_name in ["Whole Milk", "Oat Milk", "Almond Milk", "Soy Milk"]:
        return random.randint(1, 4)

    if product_name in ["Caramel Syrup", "Vanilla Syrup", "Hazelnut Syrup", "Chocolate Syrup"]:
        return random.randint(1, 2)

    if product_name in ["Matcha Powder", "Cocoa Powder"]:
        return random.randint(1, 2)

    return 0


def seed_waste():
    with get_session() as session:
        existing_waste = session.exec(select(Waste)).first()
        if existing_waste:
            print("Waste data already exists. Skipping waste seed.")
            return

        products = session.exec(select(Product)).all()

        if not products:
            print("No products found. Run init_db.py first.")
            return

        today = date.today()
        waste_to_add = []

        for product in products:
            qty = generate_waste_quantity(product.name)

            if qty > 0:
                waste_date = today - timedelta(days=random.randint(1, 10))
                waste_to_add.append(
                    Waste(
                        product_id=product.id,
                        quantity=qty,
                        date=waste_date,
                        reason="expired"
                    )
                )

        for waste in waste_to_add:
            session.add(waste)

        session.commit()
        print(f"{len(waste_to_add)} waste records inserted successfully.")


if __name__ == "__main__":
    seed_waste()