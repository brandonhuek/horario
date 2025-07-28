
import streamlit as st
import json
from datetime import time

CONFIG_FILE = "config.json"

# Cargar configuración actual
def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"enabled": False, "hour": "10:00"}

# Guardar configuración
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

st.set_page_config(page_title="Panel de Publicación Automática", page_icon="📤")

st.title("📅 Programación Automática de Productos")
st.markdown("Configura el horario en el que se publicará un producto aleatorio con stock en tu canal de Telegram.")

# Mostrar configuración actual
config = load_config()
current_time = time.fromisoformat(config.get("hour", "10:00"))
enabled = config.get("enabled", False)

# Inputs de usuario
st.subheader("⏰ Horario de publicación")
new_time = st.time_input("Selecciona la hora", value=current_time)

st.subheader("⚙️ Activar automatización")
new_enabled = st.checkbox("Activar publicación automática diaria", value=enabled)

# Guardar nueva configuración
if st.button("💾 Guardar configuración"):
    config_to_save = {
        "hour": new_time.strftime("%H:%M"),
        "enabled": new_enabled
    }
    save_config(config_to_save)
    st.success("✅ Configuración guardada correctamente.")
