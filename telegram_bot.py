import requests
import streamlit as st
from datetime import datetime
import csv

def send_product_to_telegram(product):
    bot_token = st.secrets["TELEGRAM_TOKEN"]
    chat_id = st.secrets["TELEGRAM_GROUP"]

    name = product.get("name", "Producto sin nombre")
    price = product.get("price", "Precio no disponible")
    link = product.get("permalink", "#")
    image_url = product.get("images", [{}])[0].get("src", "")

    message = f"🌿 <b>{name}</b>\n💰 Precio: {price} €\n\n<a href='{link}'>🛒 Comprar ahora</a>"

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

    response = requests.post(url, data=data)

    if response.status_code != 200:
        st.error(f"❌ Error al enviar a Telegram: {response.status_code} - {response.text}")
    else:
        st.success(f"✅ Producto enviado a Telegram: {name}")

def log_publication(product, method):
    with open("historial.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), product['name'], method, product['permalink']])

