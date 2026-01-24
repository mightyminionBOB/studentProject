from services.alpha_vantage import (
    get_global_quote,
    get_daily_series,
    get_rsi
)

print("=== PRICE ===")
print(get_global_quote("AAPL"))

print("\n=== DAILY ===")
print(get_daily_series("AAPL"))

print("\n=== RSI ===")
print(get_rsi("AAPL"))
