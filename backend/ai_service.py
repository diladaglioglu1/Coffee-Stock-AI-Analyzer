import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_API_KEY = os.getenv("GROQ_API_KEY")
_MODEL_NAME = "llama-3.3-70b-versatile"

_client = Groq(api_key=_API_KEY) if _API_KEY else None
print("API KEY:", _API_KEY)
print("CLIENT:", _client)

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

    return f"""You are an experienced coffee shop operations consultant working inside the BrewIntelligence system.

Analyze the following inventory data and provide a direct, practical recommendation to the shop manager.

PRODUCT        : {product_name}
CURRENT STOCK  : {current_stock} units
AVG DAILY SALES: {avg_sales:.1f} units/day
DAYS REMAINING : {days_remaining} days
STATUS         : {urgency}

Rules:
- Keep your response to maximum 4 sentences.
- Briefly mention the math (how many days stock will last).
- Give a clear action: place order / wait / run promotion / urgent reorder.
- Write in plain English, as if speaking directly to the shop owner.
- Do NOT start with labels like "Status:" or "Recommendation:" — just begin directly."""


def get_ai_advice(product_name: str, current_stock: float, avg_sales: float) -> str:
    if not _client:
        return "⚠️ AI service is not configured. Please add GROQ_API_KEY to your .env file."

    if current_stock < 0 or avg_sales < 0:
        return "⚠️ Invalid stock data. Please provide positive values."

    prompt = _build_prompt(product_name, current_stock, avg_sales)

    print("AI CALL STARTED")

    try:
        response = _client.chat.completions.create(
            model=_MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a coffee shop operations consultant. Provide short, clear, and actionable inventory advice in English."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=500,
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
            current_stock=p.get("stock", 0),
            avg_sales=p.get("avg_sales", 0.0),
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
