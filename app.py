import streamlit as st
import yt_dlp as youtube_dl
import whisper
import os

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
    st.title("Transcripción y Análisis de Videos de YouTube con IA")

    # Entrada de URL de YouTube
    youtube_url = st.text_input("Introduce la URL del video de YouTube")

    if st.button("Descargar, Transcribir y Analizar"):
        if youtube_url:
            # Definir el archivo de salida sin extensión .mp3
            output_path = './content/audio'

            # Descargar el audio de YouTube
            st.write("Descargando el audio...")
            download_audio_from_youtube(youtube_url, output_path)
            st.write("Descarga completa.")

            # Transcribir el audio con Whisper
            st.write("Procesando el audio con Whisper...")
            transcription = transcribe_audio_with_whisper(output_path + '.mp3')  # Agregar la extensión para Whisper
            st.write("Transcripción completa:")
            st.write(transcription)

        else:
            st.error("Por favor, introduce una URL válida de YouTube.")

if __name__ == "__main__":
    main()