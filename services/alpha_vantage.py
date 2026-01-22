import requests
from config.settings import ALPHA_VANTAGE_API_KEY

BASE_URL = "https://www.alphavantage.co/query"

# ---------- Глобальная котировка ----------
def get_global_quote(symbol: str) -> dict:
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

# ---------- Дневная серия ----------
def get_daily_series(symbol: str) -> dict:
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "outputsize": "compact"  # компактный размер данных
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

# ---------- Курс валют ----------
def get_currency_rate(from_currency: str, to_currency: str) -> dict:
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": from_currency,
        "to_currency": to_currency,
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

# ---------- RSI ----------
def get_rsi(symbol: str, interval: str = "daily") -> dict:
    """
    Получение RSI по тикеру.
    interval: 'daily', 'weekly', 'monthly'
    """
    params = {
        "function": "RSI",
        "symbol": symbol,
        "interval": interval,
        "time_period": 14,
        "series_type": "close",
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()
