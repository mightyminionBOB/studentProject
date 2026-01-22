from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = InlineKeyboardMarkup(row_width=2)
main_keyboard.add(
    InlineKeyboardButton("📈 Цена акции", callback_data="price"),
    InlineKeyboardButton("📊 Анализ", callback_data="analysis"),
    InlineKeyboardButton("💱 Валюта", callback_data="currency"),
    InlineKeyboardButton("📉 RSI", callback_data="rsi")
)

period_keyboard = InlineKeyboardMarkup(row_width=3)
period_keyboard.add(
    InlineKeyboardButton("5 дней", callback_data="period_5"),
    InlineKeyboardButton("10 дней", callback_data="period_10"),
    InlineKeyboardButton("30 дней", callback_data="period_30")
)
