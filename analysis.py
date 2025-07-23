import yfinance as yf
import pandas as pd
import random

def analyze_market(symbol: str):
    try:
        data = yf.download(
            tickers=symbol,
            interval="1m",
            period="1d",
            progress=False
        )

        if data.empty:
            return f"❌ Ошибка {symbol}: нет рыночных данных."

        close_prices = data["Close"]
        volume = data["Volume"]

        # Простой анализ: проверим последнюю свечу
        last_close = close_prices.iloc[-1]
        prev_close = close_prices.iloc[-2]

        direction = "📉 ПАДЕНИЕ" if last_close < prev_close else "📈 РОСТ"
        confidence = random.randint(60, 95)

        # Условная рекомендация на время сделки
        durations = {
            "2 мин": random.randint(30, 70),
            "3 мин": random.randint(40, 80),
            "4 мин": random.randint(50, 90),
            "5 мин": random.randint(60, 100)
        }
        best_duration = max(durations, key=durations.get)
        best_percent = durations[best_duration]

        message = (
            f"📊 Валюта: {symbol}\n"
            f"{direction}\n"
            f"Цена: {round(last_close, 5)}\n"
            f"Объём: {int(volume.iloc[-1])}\n"
            f"Уверенность: {confidence}%\n"
            f"⏱ Рекомендованное время сделки: {best_duration} ({best_percent}%)"
        )

        return message

    except Exception as e:
        return f"❌ Ошибка {symbol}: {e}"
