from flask import Flask, render_template, request, send_from_directory
import os
import yt_dlp
from moviepy.editor import AudioFileClip
app = Flask(__name__)
# Carpeta donde se guardarán las descargas
DOWNLOAD_FOLDER = os.path.join(os.getcwd(),'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form.get('format', 'video')

    # Configuración de yt-dlp
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    }

    # Descargar el video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        video_title = result['title']

    if format_type == 'audio':
        video_file = os.path.join(DOWNLOAD_FOLDER, f"{video_title}.mp4")
        audio_file = os.path.join(DOWNLOAD_FOLDER, f"{video_title}.mp3")

        # Convertir el video a audio usando moviepy
        clip = AudioFileClip(video_file)
        clip.write_audiofile(audio_file)
        clip.close()

        # Opcionalmente, puedes eliminar el archivo de video si no lo necesitas
        os.remove(video_file)

    return f'Download completed! <a href="/downloads/{video_title}.mp3">Download audio</a>'

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)