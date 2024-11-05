import yt_dlp
from flask import Flask, render_template, request, send_from_directory
import os
from moviepy.editor import AudioFileClip
os.system("pip install --upgrade pip")
app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

#COOKIE_FILE = os.path.join(app.root_path, 'config', 'cookies.txt')  # Archivo cookies dentro del proyecto

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form.get('format', 'video')
    
    # Configuración de yt-dlp con archivo de cookies
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'), # C:\Dev\PYTHON\APPS------ANDRES\app1\cookies.txt
        #'cookiefile': 'C:/Dev/PYTHON/APPS------ANDRES/app1/cookies.txt'  # Reemplaza con la ruta de tu archivo de cookies
        # 'C:\\Dev\\PYTHON\\APPS------ANDRES\\app1\\cookies.txt'
        'cookiefile': '/opt/render/project/src/config/cookies.txt'

    }

    try:
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

            # Eliminar el archivo de video si no es necesario
            os.remove(video_file)

        return f'Download completed! <a href="/downloads/{video_title}.mp3">Download audio</a>'

    except Exception as e:
        return f"Error: {e}", 500

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)