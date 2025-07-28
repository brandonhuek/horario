
import time
import json
import schedule
from datetime import datetime
from woocommerce_api import get_random_product
from telegram_bot import send_product_to_telegram

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"enabled": False, "hour": "10:00"}

def publicar_producto():
    product = get_random_product()
    if product:
        send_product_to_telegram(product)
        print(f"[{datetime.now()}] ✅ Producto publicado.")
    else:
        print(f"[{datetime.now()}] ⚠️ No se encontró producto con stock.")

def configurar_scheduler():
    config = load_config()
    schedule.clear()
    if config.get("enabled"):
        hour = config.get("hour", "10:00")
        schedule.every().day.at(hour).do(publicar_producto)
        print(f"🕒 Publicación programada diaria a las {hour}.")
    else:
        print("⛔ Automatización desactivada.")

if __name__ == "__main__":
    print("🔄 Iniciando bot de publicación automática...")
    configurar_scheduler()

    while True:
        schedule.run_pending()
        time.sleep(30)
