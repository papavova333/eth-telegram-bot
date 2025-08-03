import time
import requests
import telebot
import os
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)

def get_eth_data():
    url = 'https://api.coingecko.com/api/v3/coins/ethereum'
    r = requests.get(url).json()
    price = r['market_data']['current_price']['usd']
    vol = r['market_data']['total_volume']['usd']
    change = r['market_data']['price_change_percentage_24h']
    return price, vol, change

def send_eth_update():
    price, vol, change = get_eth_data()
    status = "⬇️ ПРОБИТ уровень $3500" if price < 3500 else "🟢 УДЕРЖАН уровень $3500"
    message = (
        f"📊 ETH Update:\n"
        f"Цена: ${price:,.2f}\n"
        f"Объём (24ч): ${vol:,.0f}\n"
        f"Изменение за 24ч: {change:.2f}%\n"
        f"{status}"
    )
    bot.send_message(CHAT_ID, message)

def periodic_sender():
    while True:
        try:
            send_eth_update()
        except Exception as e:
            print(f"Ошибка: {e}")
        time.sleep(3 * 60 * 60)

threading.Thread(target=periodic_sender, daemon=True).start()

bot.polling()
