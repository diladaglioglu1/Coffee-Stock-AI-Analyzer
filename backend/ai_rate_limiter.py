# ai_rate_limiter.py
# BrewIntelligence — Gemini API Rate Limiter & Cache
# Rol: AI Specialist (Kişi 2) | SWE314 W3: Error Handling & Quota Management
#
# Gemini 1.5 Flash ücretsiz tier limitleri (2024):
#   - 15 istek/dakika (RPM)
#   - 1.000.000 token/dakika (TPM)
#   - 1.500 istek/gün (RPD)
#
# Bu modül iki şey yapar:
#   1. RATE LIMITING  — dakika başına istek sayısını sınırla
#   2. IN-MEMORY CACHE — aynı ürün tekrar sorulursa Gemini'yi çağırma

from __future__ import annotations

import time
import hashlib
from collections import deque
from threading import Lock
from typing import Optional


# ══════════════════════════════════════════════════════════════════════════════
# ── AYARLAR ──────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

RATE_LIMIT_RPM   = 14        # Dakikada max istek (güvenli tampon: 14/15)
RATE_LIMIT_RPD   = 1400      # Günde max istek    (güvenli tampon: 1400/1500)
CACHE_TTL_SECONDS = 300      # Cache süresi: 5 dakika (stok o kadar hızlı değişmez)
CACHE_MAX_SIZE    = 100      # En fazla 100 ürün cache'de tutulsun


# ══════════════════════════════════════════════════════════════════════════════
# ── CACHE ────────────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

class _AICache:
    """
    Basit TTL (Time-To-Live) cache.
    Aynı ürün + aynı stok + aynı satış → Gemini'yi tekrar çağırma.

    Neden in-memory? Üniversite projesi için Redis kurmaya gerek yok.
    Production'da Redis ile değiştir.
    """

    def __init__(self, ttl: int = CACHE_TTL_SECONDS, max_size: int = CACHE_MAX_SIZE):
        self._store:    dict[str, tuple[str, float]] = {}  # key → (value, expire_at)
        self._ttl       = ttl
        self._max_size  = max_size
        self._lock      = Lock()

    def _make_key(self, product_name: str, current_stock: int, avg_sales: float) -> str:
        """Girdi parametrelerinden deterministik cache anahtarı üret."""
        raw = f"{product_name.lower().strip()}:{current_stock}:{avg_sales:.1f}"
        return hashlib.md5(raw.encode()).hexdigest()

    def get(self, product_name: str, current_stock: int, avg_sales: float) -> Optional[str]:
        """Cache'te varsa ve süresi dolmamışsa tavsiyeyi döner, yoksa None."""
        key = self._make_key(product_name, current_stock, avg_sales)
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, expire_at = entry
            if time.time() > expire_at:
                del self._store[key]   # Süresi dolmuş, temizle
                return None
            return value

    def set(self, product_name: str, current_stock: int, avg_sales: float, advice: str) -> None:
        """Tavsiyeyi cache'e yaz."""
        key = self._make_key(product_name, current_stock, avg_sales)
        with self._lock:
            # Max boyuta ulaştıysa en eskiyi sil (basit LRU benzeri)
            if len(self._store) >= self._max_size:
                oldest_key = next(iter(self._store))
                del self._store[oldest_key]
            self._store[key] = (advice, time.time() + self._ttl)

    def invalidate(self, product_name: str) -> int:
        """Bir ürüne ait tüm cache kayıtlarını sil (stok güncellenince çağır)."""
        prefix = hashlib.md5(product_name.lower().strip().encode())
        # Basit yaklaşım: TTL zaten halleder; acil temizleme için tüm store tara
        with self._lock:
            keys_to_delete = [
                k for k, (v, _) in self._store.items()
                if product_name.lower() in v.lower()
            ]
            for k in keys_to_delete:
                del self._store[k]
        return len(keys_to_delete)

    @property
    def stats(self) -> dict:
        with self._lock:
            now = time.time()
            active = sum(1 for _, (_, exp) in self._store.items() if exp > now)
            return {"total_keys": len(self._store), "active_keys": active, "ttl_seconds": self._ttl}


# ══════════════════════════════════════════════════════════════════════════════
# ── RATE LIMITER ──────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

class _RateLimiter:
    """
    Sliding window rate limiter.
    Dakikada RATE_LIMIT_RPM, günde RATE_LIMIT_RPD isteği geçemez.
    """

    def __init__(self, rpm: int = RATE_LIMIT_RPM, rpd: int = RATE_LIMIT_RPD):
        self._rpm         = rpm
        self._rpd         = rpd
        self._minute_window: deque[float] = deque()  # Son 60 sn'deki istek zamanları
        self._day_window:    deque[float] = deque()  # Son 24 saat istek zamanları
        self._lock        = Lock()

    def _clean_window(self, window: deque, window_seconds: float) -> None:
        """Süresi geçmiş kayıtları pencereden temizle."""
        cutoff = time.time() - window_seconds
        while window and window[0] < cutoff:
            window.popleft()

    def check(self) -> tuple[bool, str]:
        """
        İstek yapılabilir mi?

        Returns:
            (True, "")                    — İstek yapılabilir
            (False, "rate_limit_minute")  — Dakika limiti doldu
            (False, "rate_limit_day")     — Günlük limit doldu
        """
        with self._lock:
            now = time.time()
            self._clean_window(self._minute_window, 60)
            self._clean_window(self._day_window, 86400)

            if len(self._day_window) >= self._rpd:
                return False, "rate_limit_day"
            if len(self._minute_window) >= self._rpm:
                return False, "rate_limit_minute"
            return True, ""

    def record(self) -> None:
        """Başarılı istek sonrası sayacı artır."""
        with self._lock:
            now = time.time()
            self._minute_window.append(now)
            self._day_window.append(now)

    @property
    def stats(self) -> dict:
        with self._lock:
            self._clean_window(self._minute_window, 60)
            self._clean_window(self._day_window, 86400)
            return {
                "requests_last_minute": len(self._minute_window),
                "requests_today":       len(self._day_window),
                "rpm_limit":            self._rpm,
                "rpd_limit":            self._rpd,
                "rpm_remaining":        self._rpm - len(self._minute_window),
                "rpd_remaining":        self._rpd - len(self._day_window),
            }


# ══════════════════════════════════════════════════════════════════════════════
# ── SINGELTON INSTANCE'LAR (modül genelinde paylaşılır) ───────────────────────
# ══════════════════════════════════════════════════════════════════════════════

ai_cache        = _AICache()
ai_rate_limiter = _RateLimiter()


# ══════════════════════════════════════════════════════════════════════════════
# ── ANA WRAPPER — ai_service.py'de bunu kullan ───────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

def get_advice_with_protection(
    product_name:  str,
    current_stock: int,
    avg_sales:     float,
    _gemini_fn,           # get_ai_advice fonksiyonunu dışarıdan al (circular import yok)
) -> dict:
    """
    Cache + Rate limiting korumasıyla AI tavsiyesi döner.
    ai_service.py'deki get_ai_advice'ı doğrudan çağırmak yerine bunu kullan.

    Returns:
        {
            "advice":      str,
            "source":      "cache" | "gemini" | "rate_limited",
            "cache_hit":   bool,
            "rate_limited": bool
        }

    Kullanım (ai_router.py içinde):
        from ai_rate_limiter import get_advice_with_protection
        from ai_service import get_ai_advice

        result = get_advice_with_protection(
            product_name, current_stock, avg_sales,
            _gemini_fn=get_ai_advice
        )
    """
    # 1. Cache'e bak
    cached = ai_cache.get(product_name, current_stock, avg_sales)
    if cached:
        return {
            "advice":       cached,
            "source":       "cache",
            "cache_hit":    True,
            "rate_limited": False,
        }

    # 2. Rate limit kontrolü
    allowed, reason = ai_rate_limiter.check()
    if not allowed:
        if reason == "rate_limit_minute":
            msg = "⚠️ AI servisi yoğun, 1 dakika sonra tekrar deneyin."
        else:
            msg = "⚠️ Günlük AI analiz limitine ulaşıldı. Yarın tekrar deneyin."
        return {
            "advice":       msg,
            "source":       "rate_limited",
            "cache_hit":    False,
            "rate_limited": True,
        }

    # 3. Gerçek Gemini çağrısı
    ai_rate_limiter.record()
    advice = _gemini_fn(product_name, current_stock, avg_sales)

    # 4. Başarılıysa cache'e yaz (hata mesajlarını cache'leme)
    if not advice.startswith("⚠️"):
        ai_cache.set(product_name, current_stock, avg_sales, advice)

    return {
        "advice":       advice,
        "source":       "gemini",
        "cache_hit":    False,
        "rate_limited": False,
    }


# ── Geliştirici Testi ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Rate Limiter Stats ===")
    print(ai_rate_limiter.stats)

    print("\n=== Cache Stats ===")
    print(ai_cache.stats)

    # Sahte fonksiyonla test
    call_count = 0
    def fake_gemini(name, stock, avg):
        global call_count
        call_count += 1
        return f"Test tavsiyesi #{call_count} — {name}"

    print("\n=== Cache Test ===")
    r1 = get_advice_with_protection("Test Kahve", 100, 20.0, fake_gemini)
    r2 = get_advice_with_protection("Test Kahve", 100, 20.0, fake_gemini)  # cache hit
    r3 = get_advice_with_protection("Test Kahve", 50, 20.0, fake_gemini)   # farklı stok

    print(f"1. çağrı → source: {r1['source']}, advice: {r1['advice']}")
    print(f"2. çağrı → source: {r2['source']}, advice: {r2['advice']}")  # cache!
    print(f"3. çağrı → source: {r3['source']}, advice: {r3['advice']}")
    print(f"\nGemini toplam çağrıldı: {call_count} kez (2 olmalı, 3 değil)")
