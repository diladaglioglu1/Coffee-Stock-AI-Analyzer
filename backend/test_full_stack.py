import sys, os, time

GREEN  = "\033[92m"; RED = "\033[91m"; YELLOW = "\033[93m"
BLUE   = "\033[94m"; BOLD = "\033[1m"; RESET = "\033[0m"

passed = failed = 0

def ok(msg):
    global passed; passed += 1
    print(f"  {GREEN}✓{RESET} {msg}")

def fail(msg):
    global failed; failed += 1
    print(f"  {RED}✗{RESET} {msg}")

def section(title):
    print(f"\n{BOLD}{BLUE}{'━'*55}")
    print(f"  {title}")
    print(f"{'━'*55}{RESET}")


section("TEST 1 — Cache: TTL ve Hit/Miss")

from ai_rate_limiter import _AICache

cache = _AICache(ttl=2, max_size=5)  

cache.set("Kahve A", 100, 20.0, "Tavsiye 1")
hit = cache.get("Kahve A", 100, 20.0)
if hit == "Tavsiye 1":
    ok("Cache set/get çalışıyor.")
else:
    fail(f"Cache hit bekleniyordu, gelen: {hit}")

miss = cache.get("Kahve B", 50, 10.0)
if miss is None:
    ok("Cache miss doğru çalışıyor.")
else:
    fail(f"Cache miss bekliyordu, gelen: {miss}")

time.sleep(2.1)
expired = cache.get("Kahve A", 100, 20.0)
if expired is None:
    ok("TTL süresi doldu, cache temizlendi.")
else:
    fail("TTL çalışmıyor, eski veri hâlâ dönüyor!")


section("TEST 2 — Rate Limiter: Pencere Kontrolü")

from ai_rate_limiter import _RateLimiter

limiter = _RateLimiter(rpm=3, rpd=100)  

for i in range(3):
    allowed, reason = limiter.check()
    if allowed:
        limiter.record()
    else:
        fail(f"İlk 3 istek kabul edilmeli, {i+1}. reddedildi!")
        break
else:
    ok("3 istek başarıyla kaydedildi.")

allowed_4th, reason = limiter.check()
if not allowed_4th and reason == "rate_limit_minute":
    ok("4. istek rate limit tarafından engellendi.")
else:
    fail(f"4. istek kabul edilmemeli! allowed={allowed_4th}, reason={reason}")

stats = limiter.stats
if stats["requests_last_minute"] == 3:
    ok(f"İstatistik doğru: {stats['requests_last_minute']} istek/dakika.")
else:
    fail(f"İstatistik yanlış: {stats}")



section("TEST 3 — get_advice_with_protection: Cache + Rate Limit")

from ai_rate_limiter import get_advice_with_protection, _AICache, _RateLimiter


test_cache   = _AICache(ttl=60)
test_limiter = _RateLimiter(rpm=10, rpd=100)

call_count = 0
def mock_gemini(name, stock, avg):
    global call_count; call_count += 1
    return f"Mock tavsiye — {name}"


import ai_rate_limiter as rl_module
orig_cache, orig_limiter = rl_module.ai_cache, rl_module.ai_rate_limiter
rl_module.ai_cache, rl_module.ai_rate_limiter = test_cache, test_limiter

r1 = get_advice_with_protection("Espresso", 80, 15.0, mock_gemini)
r2 = get_advice_with_protection("Espresso", 80, 15.0, mock_gemini) 
r3 = get_advice_with_protection("Espresso", 40, 15.0, mock_gemini)  

if r1["source"] == "gemini" and not r1["cache_hit"]:
    ok("1. istek Gemini'ye gitti.")
else:
    fail(f"1. istek Gemini'ye gitmeliydi: {r1}")

if r2["source"] == "cache" and r2["cache_hit"]:
    ok("2. istek cache'den geldi (Gemini çağrılmadı).")
else:
    fail(f"2. istek cache'den gelmeli: {r2}")

if r3["source"] == "gemini":
    ok("3. istek (farklı stok) Gemini'ye gitti.")
else:
    fail(f"3. istek Gemini'ye gitmeli: {r3}")

if call_count == 2:
    ok(f"Gemini toplam 2 kez çağrıldı (3 değil). ✓")
else:
    fail(f"Gemini {call_count} kez çağrıldı, 2 olmalı!")

# Restore
rl_module.ai_cache, rl_module.ai_rate_limiter = orig_cache, orig_limiter



section("TEST 4 — DB Bridge: Stub Modeller")

from sqlmodel import create_engine, SQLModel, Session
from datetime import date, timedelta

try:
    from ai_db_bridge import Product, Sale, get_avg_daily_sales, get_product_with_ai_inputs

    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db:
      
        p = Product(name="Test Kahve", current_stock=200, unit="g")
        db.add(p)
        db.commit()
        db.refresh(p)

     
        for i in range(7):
            db.add(Sale(
                product_id=p.id,
                quantity=30.0 + i,
                date=date.today() - timedelta(days=i),
            ))
        db.commit()

        avg = get_avg_daily_sales(p.id, db)
        if 30 <= avg <= 37:
            ok(f"Ortalama satış doğru hesaplandı: {avg:.1f}/gün")
        else:
            fail(f"Ortalama satış yanlış: {avg}")

        data = get_product_with_ai_inputs(p.id, db)
        if data and data["name"] == "Test Kahve":
            ok("get_product_with_ai_inputs veriyi doğru döndürdü.")
        else:
            fail(f"Beklenen ürün verisi gelmedi: {data}")

        none_data = get_product_with_ai_inputs(9999, db)
        if none_data is None:
            ok("Olmayan ürün için None döndürüldü.")
        else:
            fail("Olmayan ürün için None bekliyordu!")

except Exception as e:
    fail(f"DB Bridge testi hata verdi: {e}")



section("TEST 5 — Gerçek Gemini API (anahtar varsa)")

from dotenv import load_dotenv
load_dotenv()

if os.getenv("GEMINI_API_KEY"):
    from ai_service import get_ai_advice
    result = get_ai_advice("Colombia Supremo", 25, 38.0)
    if result and not result.startswith("⚠️"):
        ok("Gemini API canlı yanıt verdi!")
        print(f"\n  {YELLOW}── Örnek Tavsiye ──{RESET}")
        print(f"  {result[:120]}...")
    else:
        fail(f"Gemini'den hata geldi: {result}")
else:
    print(f"  {YELLOW}⚠{RESET}  API anahtarı yok, Gemini testi atlandı.")



print(f"\n{BOLD}{'═'*55}")
print(f"  SONUÇ: {GREEN}{passed} geçti{RESET}{BOLD}  |  {RED}{failed} başarısız{RESET}")
print(f"{'═'*55}{RESET}\n")

if failed > 0:
    sys.exit(1)
