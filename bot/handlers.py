from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot.keyboards import main_keyboard, period_keyboard
from bot.states import StockStates
from services.alpha_vantage import (
    get_global_quote,
    get_daily_series,
    get_currency_rate,
    get_rsi
)
from services.analytics import (
    analyze_period,
    interpret_rsi
)

# ---------- Команды ----------
async def start_handler(message: types.Message):
    from bot.messages import START_TEXT
    await message.answer(START_TEXT, reply_markup=main_keyboard)

async def help_handler(message: types.Message):
    from bot.messages import HELP_TEXT
    await message.answer(HELP_TEXT)

# ---------- Callback-кнопки ----------
async def price_callback(call: types.CallbackQuery):
    await call.message.answer("Введите тикер акции (например: AAPL):")
    await StockStates.waiting_for_symbol.set()
    await call.answer()

async def analysis_callback(call: types.CallbackQuery):
    await call.message.answer("Введите тикер акции для анализа:")
    await StockStates.waiting_for_analysis_symbol.set()
    await call.answer()

async def currency_callback(call: types.CallbackQuery):
    await call.message.answer("Введите валютную пару (например: USD/EUR):")
    await StockStates.waiting_for_currency_pair.set()
    await call.answer()

async def rsi_callback(call: types.CallbackQuery):
    await call.message.answer("Введите тикер акции для RSI анализа:")
    await StockStates.waiting_for_rsi_symbol.set()
    await call.answer()

# ---------- Ввод тикера (цена) ----------
async def process_price_symbol(message: types.Message, state: FSMContext):
    symbol = message.text.upper()
    try:
        data = get_global_quote(symbol)
        if "Note" in data:
            await message.answer(
                "⏳ Превышен лимит запросов API.\nПопробуйте снова через минуту.",
                reply_markup=main_keyboard
            )
            await state.finish()
            return

        if "Global Quote" not in data or not data["Global Quote"]:
            raise ValueError("Empty Global Quote")

        quote = data["Global Quote"]
        price = quote.get("05. price")
        change = quote.get("10. change percent")
        date = quote.get("07. latest trading day")

        if not price:
            raise ValueError("No price")

        await message.answer(
            f"📈 {symbol}\n"
            f"Цена: {price}$\n"
            f"Изменение: {change}\n"
            f"Дата: {date}\n\n"
            f"⚠️ Не является инвестиционной рекомендацией",
            reply_markup=main_keyboard
        )

    except Exception:
        await message.answer(
            "❌ Не удалось получить данные по акции.\n"
            "Проверьте тикер или попробуйте позже.",
            reply_markup=main_keyboard
        )
    await state.finish()

# ---------- Ввод тикера (анализ) ----------
async def process_analysis_symbol(message: types.Message, state: FSMContext):
    await state.update_data(symbol=message.text.upper())
    await message.answer("Выберите период анализа:", reply_markup=period_keyboard)

async def process_period(call: types.CallbackQuery, state: FSMContext):
    days = int(call.data.split("_")[1])
    data = await state.get_data()
    symbol = data["symbol"]

    try:
        series = get_daily_series(symbol)
        if "Note" in series:
            await call.message.answer(
                "⏳ Превышен лимит запросов API.\nПопробуйте снова через минуту.",
                reply_markup=main_keyboard
            )
            await state.finish()
            await call.answer()
            return

        analytics = analyze_period(series, days)
        await call.message.answer(
            f"📊 Анализ {symbol} за {days} дней\n"
            f"Минимум: {analytics['min_price']:.2f}$\n"
            f"Максимум: {analytics['max_price']:.2f}$\n"
            f"Средняя: {analytics['avg_price']:.2f}$\n"
            f"Изменение: {analytics['change_percent']:.2f}%\n\n"
            f"⚠️ Не является инвестиционной рекомендацией",
            reply_markup=main_keyboard
        )

    except Exception:
        await call.message.answer(
            "❌ Ошибка анализа данных.",
            reply_markup=main_keyboard
        )
    await state.finish()
    await call.answer()

# ---------- Валюта ----------
async def process_currency(message: types.Message, state: FSMContext):
    try:
        from_currency, to_currency = message.text.upper().split("/")
        data = get_currency_rate(from_currency, to_currency)
        if "Note" in data:
            raise ValueError("API limit")

        rate = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]

        await message.answer(
            f"💱 {from_currency}/{to_currency}\nКурс: {rate}\n\n⚠️ Не является инвестиционной рекомендацией",
            reply_markup=main_keyboard
        )

    except Exception:
        await message.answer(
            "❌ Неверный формат или ошибка API.\nИспользуйте формат USD/EUR",
            reply_markup=main_keyboard
        )
    await state.finish()

# ---------- RSI ----------
async def process_rsi_symbol(message: types.Message, state: FSMContext):
    symbol = message.text.upper()
    try:
        rsi_data = get_rsi(symbol)

        # Проверка лимита API
        if "Note" in rsi_data:
            await message.answer(
                "⏳ Превышен лимит запросов API.\nПопробуйте снова через минуту.",
                reply_markup=main_keyboard
            )
            await state.finish()
            return

        # Проверка наличия данных
        if "Technical Analysis: RSI" not in rsi_data:
            raise ValueError("Нет данных RSI для этого тикера")

        rsi_series = rsi_data["Technical Analysis: RSI"]

        # Берём самое последнее значение RSI
        latest_rsi_date = sorted(rsi_series.keys(), reverse=True)[0]
        latest_rsi = float(rsi_series[latest_rsi_date]["RSI"])
        interpretation = interpret_rsi(latest_rsi)

        await message.answer(
            f"📉 {symbol} — RSI\n"
            f"RSI: {latest_rsi:.2f}\n"
            f"{interpretation}\n\n"
            f"⚠️ Не является инвестиционной рекомендацией",
            reply_markup=main_keyboard
        )

    except Exception as e:
        print(f"RSI error: {e}")  # для отладки в консоли
        await message.answer(
            "❌ Не удалось получить RSI по тикеру.\n"
            "Проверьте правильность тикера или попробуйте позже.",
            reply_markup=main_keyboard
        )
    finally:
        await state.finish()


# ---------- Регистрация ----------
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(help_handler, commands=["help"])

    dp.register_callback_query_handler(price_callback, lambda c: c.data == "price")
    dp.register_callback_query_handler(analysis_callback, lambda c: c.data == "analysis")
    dp.register_callback_query_handler(currency_callback, lambda c: c.data == "currency")
    dp.register_callback_query_handler(rsi_callback, lambda c: c.data == "rsi")

    dp.register_message_handler(process_price_symbol, state=StockStates.waiting_for_symbol)
    dp.register_message_handler(process_analysis_symbol, state=StockStates.waiting_for_analysis_symbol)
    dp.register_callback_query_handler(process_period, lambda c: c.data.startswith("period_"), state="*")
    dp.register_message_handler(process_currency, state=StockStates.waiting_for_currency_pair)
    dp.register_message_handler(process_rsi_symbol, state=StockStates.waiting_for_rsi_symbol)
