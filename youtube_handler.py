import yt_dlp as youtube_dl

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
