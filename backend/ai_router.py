from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlmodel import Session

from ai_service      import get_ai_advice
from ai_db_bridge    import get_product_with_ai_inputs, get_all_products_with_ai_inputs
from ai_rate_limiter import get_advice_with_protection, ai_cache, ai_rate_limiter

try:
    from database import get_session              
except ImportError:
    from sqlmodel import create_engine, SQLModel
    _engine = create_engine("sqlite:///./brewintelligence_test.db")

    def get_session():
        with Session(_engine) as session:
            yield session


router = APIRouter(prefix="/api/ai", tags=["AI Analysis"])

class ManualAnalyzeRequest(BaseModel):
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

@router.get(
    "/analyze/{product_id}",
    response_model=AnalyzeResponse,
    summary="Analyze the product in DB with ID",
    description="It pulls product data from Person 1's database and analyzes it with Gemini.",
)
async def analyze_by_id(
    product_id: int,
    db: Session = Depends(get_session),
):
    data = get_product_with_ai_inputs(product_id, db)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The product was not found: id={product_id}",
        )

    result = get_advice_with_protection(
        product_name=data["name"],
        current_stock=data["current_stock"],
        avg_sales=data["avg_sales"],
        _gemini_fn=get_ai_advice,
    )
    return AnalyzeResponse(product_name=data["name"], **result)

@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analyze with manual data (test / override)",
)
async def analyze_manual(req: ManualAnalyzeRequest):
    result = get_advice_with_protection(
        product_name=req.product_name,
        current_stock=req.current_stock,
        avg_sales=req.avg_sales,
        _gemini_fn=get_ai_advice,
    )
    return AnalyzeResponse(product_name=req.product_name, **result)

@router.get(
    "/analyze/bulk/all",
    response_model=BulkAnalyzeResponse,
    summary="Analyze all products in bulk",
)
async def analyze_all(db: Session = Depends(get_session)):
    all_products = get_all_products_with_ai_inputs(db)
    if not all_products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The product was not found in the database.",
        )
    if len(all_products) > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="In batch analysis, a maximum of 20 products are supported.",
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

@router.get(
    "/status",
    summary="Show the rate limiter and cache status",
)
async def ai_status():
    import os
    return {
        "service":      "BrewIntelligence AI",
        "model":        "gemini-1.5-flash",
        "key_ok":       bool(os.getenv("GEMINI_API_KEY")),
        "rate_limiter": ai_rate_limiter.stats,
        "cache":        ai_cache.stats,
    }

@router.delete(
    "/cache/{product_name}",
    summary="Clear the product cache",
    description="Invalidate the old AI recommendation when the stock is updated.",
)
async def invalidate_cache(product_name: str):
    deleted = ai_cache.invalidate(product_name)
    return {"message": f"{deleted} cache records deleted for '{product_name}'."}
