import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_API_KEY = os.getenv("GROQ_API_KEY")
_MODEL_NAME = "llama-3.3-70b-versatile"

_client = Groq(api_key=_API_KEY) if _API_KEY else None


def _build_prompt(product_name: str, current_stock: float, avg_sales: float) -> str:
    days_remaining = round(current_stock / avg_sales, 1) if avg_sales > 0 else "∞"

    if avg_sales == 0:
        urgency = "NO SALES"
    elif isinstance(days_remaining, float) and days_remaining < 3:
        urgency = "CRITICAL"
    elif isinstance(days_remaining, float) and days_remaining < 7:
        urgency = "LOW"
    elif isinstance(days_remaining, float) and days_remaining > 30:
        urgency = "OVERSTOCK"
    else:
        urgency = "NORMAL"

    return f"""You are an experienced inventory analyst for a coffee shop.

Analyze the following product and provide a practical but analytical recommendation.

Product: {product_name}
Current stock: {current_stock} units
Average daily sales: {avg_sales:.1f} units/day
Estimated days remaining: {days_remaining}
Urgency level: {urgency}

Your answer must:
- explain what the stock level means in operational terms
- mention how long the stock is expected to last
- state whether the business should reorder, wait, monitor, or run a promotion
- explain the business risk briefly
- be 5 to 7 sentences long
- sound professional and useful for a shop manager

Do not use bullet points.
Do not write only one-line advice.
Write in clear English.
"""


def get_ai_advice(product_name: str, current_stock: float, avg_sales: float) -> str:
    if not _client:
        return "⚠️ AI service is not configured. Please add GROQ_API_KEY to your .env file."

    if current_stock < 0 or avg_sales < 0:
        return "⚠️ Invalid stock data. Please provide positive values."

    prompt = _build_prompt(product_name, current_stock, avg_sales)

    try:
        response = _client.chat.completions.create(
            model=_MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional inventory analyst for a coffee shop. "
                        "Provide analytical, specific, and operationally useful stock recommendations. "
                        "Avoid overly short answers."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.5,
            max_tokens=350,
        )
        return response.choices[0].message.content.strip()

    except Exception as exc:
        print(f"[ai_service] {type(exc).__name__}: {exc}")
        return "⚠️ AI service is currently unavailable. Please try again in a few minutes."


def get_bulk_advice(products: list[dict]) -> list[dict]:
    results = []
    for p in products:
        advice = get_ai_advice(
            product_name=p.get("name", "Unknown Product"),
            current_stock=p.get("current_stock", 0),
            avg_sales=p.get("avg_daily_sales", 0.0),
        )
        results.append({"name": p.get("name"), "advice": advice})
    return results


if __name__ == "__main__":
    test_cases = [
        {"name": "Ethiopia Beans", "stock": 12, "avg_sales": 42.5},
        {"name": "Brazil Santos", "stock": 500, "avg_sales": 15.0},
        {"name": "Decaf Colombia", "stock": 80, "avg_sales": 8.3},
    ]
    for tc in test_cases:
        print(f"\n{'─'*50}")
        print(f"☕  {tc['name']} | Stock: {tc['stock']} | Avg Sales: {tc['avg_sales']}/day")
        print(f"{'─'*50}")
        print(get_ai_advice(tc['name'], tc['stock'], tc['avg_sales']))
