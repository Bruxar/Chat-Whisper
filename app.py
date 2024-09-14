import streamlit as st
import yt_dlp as youtube_dl
import whisper
import os
import time
from openai_analysis import analyze_transcription  # Importar la función de análisis

# Función para descargar el video de YouTube como archivo MP3
def download_audio_from_youtube(youtube_url, output_path='./content/audio'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,  # Sin la extensión .mp3, yt-dlp la agregará automáticamente
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

# Función para procesar el audio con Whisper
def transcribe_audio_with_whisper(audio_path):
    model = whisper.load_model("small")  # Cargar el modelo Whisper
    result = model.transcribe(audio_path)
    return result["text"]

# Interfaz con Streamlit
def main():
    st.title("🎧 Transcribe y Analiza")

    # Inicializar mensajes si no existen en el estado de la sesión
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Renderizar mensajes previos
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de URL de YouTube en formato chat
    if youtube_url := st.chat_input("Introduce la URL del video de YouTube"):
        # Guardar el mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": youtube_url})
        with st.chat_message("user"):
            st.markdown(youtube_url)

        # Definir el archivo de salida sin extensión .mp3
        output_path = './content/audio'

        # Proceso de descarga, transcripción y análisis con loaders
        with st.spinner("📥 Descargando el audio..."):
            time.sleep(2)  # Simulación del tiempo de descarga
            download_audio_from_youtube(youtube_url, output_path)

        with st.spinner("🎙️ Procesando el audio..."):
            time.sleep(2)  # Simulación del tiempo de procesamiento
            transcription = transcribe_audio_with_whisper(output_path + '.mp3')

        with st.spinner("🤖 Analizando la transcripción..."):
            time.sleep(2)  # Simulación del tiempo de análisis
            analysis = analyze_transcription(transcription)

        # Mostrar el análisis en el chat como respuesta de la IA
        with st.chat_message("ai"):
            st.markdown(analysis)
        
        # Guardar el mensaje de la IA en el estado de la sesión
        st.session_state.messages.append({"role": "assistant", "content": analysis})

if __name__ == "__main__":
    main()
