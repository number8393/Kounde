import telebot
from telebot import types
import schedule
import threading
from analysis import analyze_market
from news import get_news
from learn import log_error, learn_from_history

TOKEN = "8094752756:AAFUdZn4XFlHiZOtV-TXzMOhYFlXKCFVoEs"
USER_ID = 5556108366
bot = telebot.TeleBot(TOKEN)

# Кнопки управления
main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.row("📊 Бинарные опционы", "📰 Новости")
main_keyboard.row("🕒 Торговые часы", "🧠 Обучение")

def send_analysis():
    try:
        result = analyze_market()
        bot.send_message(USER_ID, result)
    except Exception as e:
        bot.send_message(USER_ID, f"❌ Ошибка анализа: {str(e)}")
        log_error(str(e))

def run_schedule():
    schedule.every(30).seconds.do(send_analysis)
    while True:
        schedule.run_pending()

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🤖 Привет! Я бот анализа рынка.", reply_markup=main_keyboard)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "📊 Бинарные опционы":
        send_analysis()
    elif message.text == "📰 Новости":
        bot.send_message(message.chat.id, get_news())
    elif message.text == "🕒 Торговые часы":
        bot.send_message(message.chat.id, "📆 Сегодня лучшие часы для торговли: 11:00–15:00 и 20:00–22:00")
    elif message.text == "🧠 Обучение":
        learn_from_history()
        bot.send_message(message.chat.id, "📚 Обучение выполнено. Бот стал умнее.")
    else:
        bot.send_message(message.chat.id, "❓ Не понимаю. Выбери кнопку.")

# Запуск анализа в отдельном потоке
threading.Thread(target=run_schedule, daemon=True).start()
bot.infinity_polling()