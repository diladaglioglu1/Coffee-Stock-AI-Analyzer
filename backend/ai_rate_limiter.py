from __future__ import annotations

import time
import hashlib
from collections import deque
from threading import Lock
from typing import Optional

RATE_LIMIT_RPM = 14
RATE_LIMIT_RPD = 1400
CACHE_TTL_SECONDS = 300
CACHE_MAX_SIZE = 100


class _AICache:

    def __init__(self, ttl: int = CACHE_TTL_SECONDS, max_size: int = CACHE_MAX_SIZE):
        self._store: dict[str, tuple[str, float]] = {}  # key → (value, expire_at)
        self._ttl = ttl
        self._max_size = max_size
        self._lock = Lock()

    def _make_key(self, product_name: str, current_stock: int, avg_sales: float) -> str:
        normalized_name = product_name.lower().strip()
        raw = f"{normalized_name}:{current_stock}:{avg_sales:.1f}"
        hashed = hashlib.md5(raw.encode()).hexdigest()
        return f"{normalized_name}|{hashed}"

    def get(self, product_name: str, current_stock: int, avg_sales: float) -> Optional[str]:
        key = self._make_key(product_name, current_stock, avg_sales)
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            value, expire_at = entry
            if time.time() > expire_at:
                del self._store[key]
                return None
            return value

    def set(self, product_name: str, current_stock: int, avg_sales: float, advice: str) -> None:
        key = self._make_key(product_name, current_stock, avg_sales)
        with self._lock:
            if len(self._store) >= self._max_size:
                oldest_key = next(iter(self._store))
                del self._store[oldest_key]
            self._store[key] = (advice, time.time() + self._ttl)

    def invalidate(self, product_name: str) -> int:
        normalized_name = product_name.lower().strip()
        with self._lock:
            keys_to_delete = [
                k for k in self._store.keys()
                if k.startswith(f"{normalized_name}|")
            ]
            for k in keys_to_delete:
                del self._store[k]
        return len(keys_to_delete)

    @property
    def stats(self) -> dict:
        with self._lock:
            now = time.time()
            active = sum(1 for _, (_, exp) in self._store.items() if exp > now)
            return {
                "total_keys": len(self._store),
                "active_keys": active,
                "ttl_seconds": self._ttl
            }


class _RateLimiter:

    def __init__(self, rpm: int = RATE_LIMIT_RPM, rpd: int = RATE_LIMIT_RPD):
        self._rpm = rpm
        self._rpd = rpd
        self._minute_window: deque[float] = deque()
        self._day_window: deque[float] = deque()
        self._lock = Lock()

    def _clean_window(self, window: deque, window_seconds: float) -> None:
        cutoff = time.time() - window_seconds
        while window and window[0] < cutoff:
            window.popleft()

    def check(self) -> tuple[bool, str]:
        with self._lock:
            self._clean_window(self._minute_window, 60)
            self._clean_window(self._day_window, 86400)

            if len(self._day_window) >= self._rpd:
                return False, "rate_limit_day"
            if len(self._minute_window) >= self._rpm:
                return False, "rate_limit_minute"
            return True, ""

    def record(self) -> None:
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
                "requests_today": len(self._day_window),
                "rpm_limit": self._rpm,
                "rpd_limit": self._rpd,
                "rpm_remaining": self._rpm - len(self._minute_window),
                "rpd_remaining": self._rpd - len(self._day_window),
            }


ai_cache = _AICache()
ai_rate_limiter = _RateLimiter()


def get_advice_with_protection(
    product_name: str,
    current_stock: int,
    avg_sales: float,
    _ai_fn,
) -> dict:

    cached = ai_cache.get(product_name, current_stock, avg_sales)
    if cached:
        return {
            "advice": cached,
            "source": "cache",
            "cache_hit": True,
            "rate_limited": False,
        }

    allowed, reason = ai_rate_limiter.check()
    if not allowed:
        if reason == "rate_limit_minute":
            msg = "⚠️ The AI service is busy. Please try again in 1 minute."
        else:
            msg = "⚠️ Daily AI analysis limit reached. Try again tomorrow."
        return {
            "advice": msg,
            "source": "rate_limited",
            "cache_hit": False,
            "rate_limited": True,
        }

    ai_rate_limiter.record()
    advice = _ai_fn(product_name, current_stock, avg_sales)

    if not advice.startswith("⚠️"):
        ai_cache.set(product_name, current_stock, avg_sales, advice)

    return {
        "advice": advice,
        "source": "groq",
        "cache_hit": False,
        "rate_limited": False,
    }


if __name__ == "__main__":
    print("=== Rate Limiter Stats ===")
    print(ai_rate_limiter.stats)

    print("\n=== Cache Stats ===")
    print(ai_cache.stats)

    call_count = 0

    def fake_ai(name, stock, avg):
        global call_count
        call_count += 1
        return f"Test advice #{call_count} — {name}"

    print("\n=== Cache Test ===")
    r1 = get_advice_with_protection("Test Coffee", 100, 20.0, fake_ai)
    r2 = get_advice_with_protection("Test Coffee", 100, 20.0, fake_ai)
    r3 = get_advice_with_protection("Test Coffee", 50, 20.0, fake_ai)

    print(f"Call 1 → source: {r1['source']}, advice: {r1['advice']}")
    print(f"Call 2 → source: {r2['source']}, advice: {r2['advice']}")
    print(f"Call 3 → source: {r3['source']}, advice: {r3['advice']}")
    print(f"\nTotal AI calls: {call_count} (Expected: 2)")