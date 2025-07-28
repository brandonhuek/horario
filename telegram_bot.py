import requests
import os
import csv
from datetime import datetime

def send_product_to_telegram(product):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    message = f"🌿 <b>{product['name']}</b>\n💰 Precio: {product['price']} €\n\n<a href='{product['permalink']}'>🛒 Comprar ahora</a>"

    image_url = product['images'][0]['src'] if product['images'] else None

    if image_url:
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        data = {
            "chat_id": chat_id,
            "photo": image_url,
            "caption": message,
            "parse_mode": "HTML"
        }
    else:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

    requests.post(url, data=data)

def log_publication(product, method):
    with open("historial.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), product['name'], method, product['permalink']])
        
