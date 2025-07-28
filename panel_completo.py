
import streamlit as st
import json
from datetime import datetime, time, date
from woocommerce_api import get_random_product
from telegram_bot import send_product_to_telegram

CONFIG_FILE = "config.json"
LOG_FILE = "historial.txt"

# Cargar configuración
def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"enabled": False, "hour": "10:00", "date": None}

# Guardar configuración
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# Agregar entrada al historial
def log_publicacion(mensaje):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()} - {mensaje}\n")

# Publicar producto manualmente
def publicar_manual():
    product = get_random_product()
    if product:
        send_product_to_telegram(product)
        log_publicacion(f"✅ Producto publicado manualmente: {product['name']}")
        st.success(f"✅ Producto publicado: {product['name']}")
    else:
        log_publicacion("⚠️ Intento fallido: Sin productos con stock")
        st.warning("⚠️ No se encontró ningún producto con stock.")

# INTERFAZ
st.set_page_config(page_title="Panel Completo de Publicación", page_icon="📦")
st.title("📦 Panel de Publicación Telegram + Programación")

config = load_config()
current_time = time.fromisoformat(config.get("hour", "10:00"))
enabled = config.get("enabled", False)
fecha_actual = config.get("date", date.today().isoformat())

# Manejo seguro de fecha
try:
    fecha_por_defecto = date.fromisoformat(fecha_actual)
except:
    fecha_por_defecto = date.today()

# Programar publicación
st.subheader("⏰ Programar publicación automática")
new_time = st.time_input("Selecciona la hora", value=current_time)
new_date = st.date_input("Selecciona la fecha", value=fecha_por_defecto)
new_enabled = st.checkbox("Activar automatización para esa fecha y hora", value=enabled)

if st.button("💾 Guardar configuración"):
    config_to_save = {
        "hour": new_time.strftime("%H:%M"),
        "date": new_date.isoformat(),
        "enabled": new_enabled
    }
    save_config(config_to_save)
    st.success("✅ Configuración guardada correctamente.")

# Publicación manual
st.subheader("📲 Publicar producto ahora mismo")
if st.button("🚀 Publicar manualmente"):
    publicar_manual()

# Ver historial
st.subheader("📜 Historial de publicaciones")
try:
    with open(LOG_FILE, "r") as f:
        logs = f.read()
        st.text_area("Historial", logs, height=200)
except FileNotFoundError:
    st.info("Aún no hay publicaciones registradas.")
