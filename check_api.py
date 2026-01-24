import time

from services.alpha_vantage import (
    get_global_quote,
    get_daily_series,
    get_rsi
)

print("=== PRICE ===")
print(get_global_quote("AAPL"))
time.sleep(65) # Запросы к API доступны в режиме – 1 запрос в минуту
print("\n=== DAILY ===")
print(get_daily_series("AAPL"))
time.sleep(65)
print("\n=== RSI ===")
print(get_rsi("AAPL"))
