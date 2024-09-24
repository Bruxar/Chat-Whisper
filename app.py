import streamlit as st
import time
import re
from youtube_handler import download_audio_from_youtube
from whisper_handler import transcribe_audio_with_whisper
from openai_analysis import analyze_transcription

# Función para reiniciar el chat
def reset_chat():
    st.rerun()  # Recargar la aplicación

def clean_message():
    st.session_state.messages = []  # Vaciar los mensajes en el estado de la sesión

# Función para validar si el input es una URL
def is_valid_url(url):
    # Expresión regular para validar URL
    url_regex = re.compile(r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$')
    return re.match(url_regex, url) is not None

# Interfaz con Streamlit
def main():
    st.title("🎧 Transcribe y Analiza")

    # Botón para reiniciar el chat
    if st.button("🔄 Reiniciar Chat"):
        reset_chat()

    # Inicializar mensajes si no existen en el estado de la sesión
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "processing" not in st.session_state:
        st.session_state.processing = False  # Indicar si hay un proceso en curso

    # Renderizar mensajes previos
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Deshabilitar el input si se está procesando un video
    if not st.session_state.processing:
        # Entrada de URL de YouTube en formato chat
        youtube_url = st.chat_input("Introduce la URL del video de YouTube")
        
        if youtube_url:
            # Validar si el input es una URL válida
            if is_valid_url(youtube_url):
                # Limpiar el historial del chat antes de procesar
                clean_message()  # Vaciar los mensajes en el estado de la sesión
                st.session_state.messages.append({"role": "system", "content": "🧹 El chat ha sido limpiado."})
                st.session_state.valid_url = youtube_url  # Guardar la URL válida en el estado de la sesión
                st.rerun()  # Volver a ejecutar la aplicación con el chat limpio
            else:
                # Mostrar mensaje de error si no es una URL válida
                error_message = "⚠️ Por favor, introduce una URL de YouTube válida."
                st.session_state.messages.append({"role": "assistant", "content": error_message})
                with st.chat_message("assistant"):
                    st.markdown(error_message)

    # Bloquear el chat input cuando se está procesando
    else:
        st.write("⏳ Procesando... Por favor espera.")
        
    # Después de recargar, continuar el proceso solo si hay una URL válida
    if "valid_url" in st.session_state and not st.session_state.processing:
        youtube_url = st.session_state.valid_url
        
        # Definir el archivo de salida sin extensión .mp3
        output_path = './content/audio'

        # Bloquear la entrada de mensajes mientras se procesa
        st.session_state.processing = True

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

        # Desbloquear la entrada de mensajes
        st.session_state.processing = False

if __name__ == "__main__":
    main()
