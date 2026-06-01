import os
import telebot
import time
import requests
from alerts_in_ua import Client as AlertsClient
from flask import Flask
from threading import Thread

# --- ДОДАНО: Налаштування фонового веб-сервера ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Сервер працює, бот не спить! 🦾"

def run_server():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    server_thread = Thread(target=run_server)
    server_thread.daemon = True 
    server_thread.start()
# ---------------------------------------------------

# --- ДОДАНО: Витягуємо сікрети зі змінних оточення ---
ALERTS_TOKEN = os.environ.get("ALERTS_TOKEN")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
# -----------------------------------------------------

alerts_client = AlertsClient(token=ALERTS_TOKEN)
alert_status = alerts_client.get_air_raid_alert_status(13).status
print(alert_status)
bot = telebot.TeleBot(BOT_TOKEN)
status = alerts_client.get_air_raid_alert_status(13).status
startv = True if status in ["active", "partly"] else False if status == "no_alert" else False
ifalert = startv
print(ifalert)
bot.send_message(CHAT_ID, 'Бот запущений!')

keep_alive()

a = 1
while True:
    print(a)
    try:
        status = alerts_client.get_air_raid_alert_status(13).status
        alerts = True if status in ["active", "partly"] else False if status == "no_alert" else False
        print(f"ifalest {ifalert} alerts {alerts}")
    except Exception as e:
        bot.send_message(ADMIN_ID, e)
    try:
        #print(type(alerts))
        if alerts != ifalert:
            ifalert = alerts
            if alerts:
                bot.send_message(CHAT_ID, '🚨🚨🚨 УВАГА, лунає сирена!')
            elif not alerts:
                bot.send_message(CHAT_ID, '❗️ Відбій тривоги')
    except Exception as e:
        bot.send_message(ADMIN_ID, e)
    a += 1
    if (a % 20 == 0):
      bot.send_message(ADMIN_ID, f"Я ще живий! Вже {a} ітерація")
    time.sleep(10)
