def analyze_period(time_series: dict, days: int) -> dict:
    import pandas as pd
    if "Time Series (Daily)" not in time_series:
        raise ValueError("No time series data")
    data = time_series["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(data, orient="index").astype(float)
    df = df.sort_index(ascending=False).head(days)
    start_price = df.iloc[-1]["4. close"]
    end_price = df.iloc[0]["4. close"]
    change_percent = ((end_price - start_price) / start_price) * 100
    return {
        "min_price": df["4. close"].min(),
        "max_price": df["4. close"].max(),
        "avg_price": df["4. close"].mean(),
        "change_percent": change_percent
    }

def interpret_rsi(rsi_value: float) -> str:
    if rsi_value <= 30:
        return "🟢 RSI указывает на возможную перепроданность (потенциальная покупка)"
    elif rsi_value >= 70:
        return "🔴 RSI указывает на возможную перекупленность (потенциальная продажа)"
    else:
        return "⚪ RSI в нейтральной зоне"
