from aiogram.dispatcher.filters.state import StatesGroup, State

class StockStates(StatesGroup):
    waiting_for_symbol = State()           # для кнопки Цена акции
    waiting_for_analysis_symbol = State()  # для кнопки Анализ
    waiting_for_currency_pair = State()    # для кнопки Валюта
    waiting_for_rsi_symbol = State()      # для кнопки RSI ✅
