import os
import httpx
from dotenv import load_dotenv

# Cargar la API key desde .env
load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")

API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-3-opus-20240229"  # Puedes cambiar por opus si tienes acceso

HEADERS = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json"
}

# Función para resumir el texto usando Claude con los parámetros especificados, pueden cambiarse
# según tus necesidades o las capacidades de tu cuenta.
def resumir_con_claude(texto: str) -> str:
    prompt = f"summarize the following press release in a range of 100 to 150 words approximately, keep the key details.\n\n{texto}"

    body = {
        "model": MODEL,
        "max_tokens": 300,
        "temperature": 0.3,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
#    Realizar la solicitud a la API
    response = httpx.post(API_URL, headers=HEADERS, json=body, timeout=60)

    if response.status_code == 200:
        data = response.json()
        return data["content"][0]["text"].strip()
    else:
        raise Exception(f"Error al llamar a la API: {response.status_code} - {response.text}")

