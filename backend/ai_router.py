# ai_router.py  (GÜNCELLENMİŞ — v2)
# BrewIntelligence — FastAPI Router (AI Endpoints)
# Rol: AI Specialist (Kişi 2) | SWE314 W3: Service Layer + Error Handling
#
# DEĞİŞİKLİKLER (v1 → v2):
#   + ai_db_bridge entegrasyonu: ürün verisini DB'den otomatik çekiyor
#   + ai_rate_limiter entegrasyonu: cache + kota koruması eklendi
#   + /api/ai/status endpoint'i: rate limiter ve cache durumunu gösterir

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlmodel import Session

from ai_service      import get_ai_advice
from ai_db_bridge    import get_product_with_ai_inputs, get_all_products_with_ai_inputs
from ai_rate_limiter import get_advice_with_protection, ai_cache, ai_rate_limiter

# Kişi 3'ün DB bağımlılık fonksiyonu — o yazana kadar stub
try:
    from database import get_session               # Kişi 3'ün dosyası
except ImportError:
    from sqlmodel import create_engine, SQLModel
    _engine = create_engine("sqlite:///./brewintelligence_test.db")

    def get_session():
        with Session(_engine) as session:
            yield session


router = APIRouter(prefix="/api/ai", tags=["AI Analysis"])


# ── Şemalar ───────────────────────────────────────────────────────────────────
class ManualAnalyzeRequest(BaseModel):
    """Manuel veri girişi — DB yokken ya da override için."""
    product_name:  str   = Field(..., example="Ethiopia Yirgacheffe")
    current_stock: int   = Field(..., ge=0, example=120)
    avg_sales:     float = Field(..., ge=0, example=35.5)

class AnalyzeResponse(BaseModel):
    product_name:  str
    advice:        str
    source:        str   # "cache" | "gemini" | "rate_limited"
    cache_hit:     bool
    rate_limited:  bool

class BulkAnalyzeResponse(BaseModel):
    results: list[AnalyzeResponse]
    total:   int


# ── Endpoint 1: Ürün ID'siyle analiz (DB entegreli) ───────────────────────────
@router.get(
    "/analyze/{product_id}",
    response_model=AnalyzeResponse,
    summary="DB'deki ürünü ID ile analiz et",
    description="Kişi 1'in DB'sinden ürün verisini çeker, Gemini ile analiz eder.",
)
async def analyze_by_id(
    product_id: int,
    db: Session = Depends(get_session),
):
    # DB'den ürün + ortalama satış verisini al
    data = get_product_with_ai_inputs(product_id, db)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ürün bulunamadı: id={product_id}",
        )

    result = get_advice_with_protection(
        product_name=data["name"],
        current_stock=data["current_stock"],
        avg_sales=data["avg_sales"],
        _gemini_fn=get_ai_advice,
    )
    return AnalyzeResponse(product_name=data["name"], **result)


# ── Endpoint 2: Manuel analiz (DB gerektirmez) ────────────────────────────────
@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Manuel veri ile analiz et (test / override)",
)
async def analyze_manual(req: ManualAnalyzeRequest):
    result = get_advice_with_protection(
        product_name=req.product_name,
        current_stock=req.current_stock,
        avg_sales=req.avg_sales,
        _gemini_fn=get_ai_advice,
    )
    return AnalyzeResponse(product_name=req.product_name, **result)


# ── Endpoint 3: Tüm ürünler toplu analiz ─────────────────────────────────────
@router.get(
    "/analyze/bulk/all",
    response_model=BulkAnalyzeResponse,
    summary="Tüm ürünleri toplu analiz et",
)
async def analyze_all(db: Session = Depends(get_session)):
    all_products = get_all_products_with_ai_inputs(db)
    if not all_products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veritabanında ürün bulunamadı.",
        )
    if len(all_products) > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Toplu analizde en fazla 20 ürün destekleniyor.",
        )

    results = []
    for p in all_products:
        r = get_advice_with_protection(
            product_name=p["name"],
            current_stock=p["current_stock"],
            avg_sales=p["avg_sales"],
            _gemini_fn=get_ai_advice,
        )
        results.append(AnalyzeResponse(product_name=p["name"], **r))

    return BulkAnalyzeResponse(results=results, total=len(results))


# ── Endpoint 4: Servis durumu ─────────────────────────────────────────────────
@router.get(
    "/status",
    summary="Rate limiter ve cache durumunu göster",
)
async def ai_status():
    """
    Hoca bu endpoint'i Swagger'da açıp görebilir:
    - Kaç istek kaldı (dakika/gün)
    - Cache kaç tavsiye tutuyor
    """
    import os
    return {
        "service":      "BrewIntelligence AI",
        "model":        "gemini-1.5-flash",
        "key_ok":       bool(os.getenv("GEMINI_API_KEY")),
        "rate_limiter": ai_rate_limiter.stats,
        "cache":        ai_cache.stats,
    }


# ── Endpoint 5: Cache temizle (stok güncellenince) ────────────────────────────
@router.delete(
    "/cache/{product_name}",
    summary="Ürün cache'ini temizle",
    description="Stok güncellendiğinde eski AI tavsiyesini geçersiz kıl.",
)
async def invalidate_cache(product_name: str):
    deleted = ai_cache.invalidate(product_name)
    return {"message": f"'{product_name}' için {deleted} cache kaydı silindi."}
