
import requests
import random
import streamlit as st

def get_products():
    try:
        url = st.secrets["WOOCOMMERCE_URL"]
        ck = st.secrets["WOOCOMMERCE_CK"]
        cs = st.secrets["WOOCOMMERCE_CS"]
    except KeyError as e:
        raise ValueError(f"🔒 Faltan secretos en Streamlit: {e}")

    # Mostrar en consola para depuración
    print("DEBUG: URL de WooCommerce:", url)

    if not url or not url.startswith(('http://', 'https://')):
        raise ValueError("🚫 La URL de WooCommerce no está configurada correctamente. Debe incluir 'http://' o 'https://'.")

    try:
        response = requests.get(f"{url}/wp-json/wc/v3/products", auth=(ck, cs))
        if response.status_code == 200:
            return response.json()
        else:
            print("⚠️ Error al consultar WooCommerce:", response.status_code, response.text)
    except Exception as e:
        print("❌ Error de conexión con WooCommerce:", str(e))

    return []

def get_random_product():
    products = get_products()
    if products:
        available = [p for p in products if p.get('stock_status') == 'instock']
        if available:
            return random.choice(available)
    return None
