import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# Carrega as variáveis do .env localizado junto deste script
load_dotenv(Path(__file__).resolve().parent / ".env")

# Recupera a chave de API
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Chave GEMINI_API_KEY não encontrada.")

# Cria o cliente Gemini
client = genai.Client(api_key=api_key)

# Envia uma primeira mensagem ao modelo
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Olá! Responda em português e diga brevemente o que você pode fazer."
)

print("RESPOSTA DO GEMINI:")
print(response.text)