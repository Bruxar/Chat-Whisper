from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de API desde las variables de entorno
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Función para analizar la transcripción usando GPT-4
def analyze_transcription(transcription):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente que analiza transcripciones de videos de YouTube."},
                {"role": "user", "content": f"Por favor, analiza el siguiente texto: {transcription}"}
            ],
            max_tokens=500,  # Ajusta según tus necesidades
            temperature=0.7  # Ajusta la creatividad de la respuesta
        )
        
        # Extraer el análisis de la respuesta de OpenAI
        return completion.choices[0].message.content
    
    except Exception as e:
        return f"Error al analizar la transcripción: {str(e)}"