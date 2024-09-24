import whisper

# Función para procesar el audio con Whisper
def transcribe_audio_with_whisper(audio_path):
    model = whisper.load_model("small")  # Cargar el modelo Whisper
    result = model.transcribe(audio_path)
    return result["text"]
