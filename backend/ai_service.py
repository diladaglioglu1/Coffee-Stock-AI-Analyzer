# ai_service.py
# BrewIntelligence — AI Integration Layer
# Rol: AI Specialist (Kişi 2) | SWE314 W3: External APIs & Service Layer
# Model: Groq (Llama 3.3) — Gemini'ye drop-in alternatif

import os
from dotenv import load_dotenv
from groq import Groq

# ── W3: Güvenlik — API anahtarını .env'den yükle, koda gömme ──────────────────
load_dotenv()

_API_KEY    = os.getenv("GEMINI_API_KEY")   # .env anahtarı aynı kalıyor
_MODEL_NAME = "llama-3.3-70b-versatile"

_client = Groq(api_key=_API_KEY) if _API_KEY else None


# ── Prompt Engineering ─────────────────────────────────────────────────────────
def _build_prompt(product_name: str, current_stock: int, avg_sales: float) -> str:
    days_remaining = round(current_stock / avg_sales, 1) if avg_sales > 0 else "∞"

    if avg_sales == 0:
        urgency = "SATIŞ YOK"
    elif isinstance(days_remaining, float) and days_remaining < 3:
        urgency = "KRİTİK"
    elif isinstance(days_remaining, float) and days_remaining < 7:
        urgency = "DÜŞÜK"
    elif isinstance(days_remaining, float) and days_remaining > 30:
        urgency = "FAZLA STOK"
    else:
        urgency = "NORMAL"

    return f"""Sen BrewIntelligence sisteminin içinde çalışan, 10 yıllık deneyimli bir kahve dükkanı operasyon danışmanısın.

Dükkan yöneticisine aşağıdaki stok verilerini analiz ederek TÜRKÇE, samimi ve doğrudan bir tavsiye ver.

ÜRÜN   : {product_name}
STOK   : {current_stock} birim
GÜNLÜK SATIŞ (ort.): {avg_sales:.1f} birim/gün
KALAN SÜRE (tahmini): {days_remaining} gün
DURUM  : {urgency}

Kurallar:
- Yanıtın maksimum 4 cümle olsun.
- Matematiksel hesabı kısaca belirt (kaç güne yeter).
- Net bir aksiyon öner: sipariş aç / bekle / kampanya yap / acil sipariş.
- Teknik jargon kullanma, dükkan sahibine konuşur gibi yaz.
- Yanıtın başına "Durum:" veya "Tavsiye:" gibi bir etiket ekleme, direkt başla."""


# ── Ana Servis Fonksiyonu ──────────────────────────────────────────────────────
def get_ai_advice(product_name: str, current_stock: int, avg_sales: float) -> str:
    if not _client:
        return "⚠️ AI servisi yapılandırılmamış. Lütfen .env dosyasına GEMINI_API_KEY ekleyin."

    if current_stock < 0 or avg_sales < 0:
        return "⚠️ Geçersiz stok verisi. Lütfen pozitif değerler girin."

    prompt = _build_prompt(product_name, current_stock, avg_sales)

    try:
        response = _client.chat.completions.create(
            model=_MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "Sen bir kahve dükkanı operasyon danışmanısın. Kısa, net ve samimi Türkçe tavsiyeler veriyorsun."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1800,
        )
        return response.choices[0].message.content.strip()

    except Exception as exc:
        print(f"[ai_service] {type(exc).__name__}: {exc}")
        return "⚠️ AI servisi şu an meşgul veya erişilemiyor. Birkaç dakika sonra tekrar deneyin."


# ── Toplu Analiz ──────────────────────────────────────────────────────────────
def get_bulk_advice(products: list[dict]) -> list[dict]:
    results = []
    for p in products:
        advice = get_ai_advice(
            product_name=p.get("name", "Bilinmeyen Ürün"),
            current_stock=p.get("stock", 0),
            avg_sales=p.get("avg_sales", 0.0),
        )
        results.append({"name": p.get("name"), "advice": advice})
    return results


# ── Geliştirici Testi ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        {"name": "Ethiopia Yirgacheffe",   "stock": 12,  "avg_sales": 42.5},
        {"name": "Brazil Santos Espresso", "stock": 500, "avg_sales": 15.0},
        {"name": "Decaf Colombia",         "stock": 80,  "avg_sales": 8.3},
    ]
    for tc in test_cases:
        print(f"\n{'─'*50}")
        print(f"🫘  {tc['name']} | Stok: {tc['stock']} | Ort. Satış: {tc['avg_sales']}/gün")
        print(f"{'─'*50}")
        print(get_ai_advice(tc["name"], tc["stock"], tc["avg_sales"]))