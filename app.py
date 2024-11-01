from flask import Flask, request, redirect, url_for, flash, send_from_directory, jsonify
import subprocess, os, uuid

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Ruta para almacenar los archivos descargados temporalmente
DOWNLOAD_PATH = "temp_downloads"
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

@app.route("/", methods=["POST"])
def download():
    url = request.form.get("url")
    download_type = request.form.get("download_type")

    if url:
        url = url.split('?')[0]
        extension = 'mp3' if download_type == 'audio' else 'mp4'
        base_name = 'audio' if download_type == 'audio' else 'video'
        
        # Crear un nombre de archivo único
        file_name = f"{base_name}_{uuid.uuid4()}.{extension}"
        output_file = os.path.join(DOWNLOAD_PATH, file_name)
        
        # Determinar el formato a descargar
        format_flag = "bestaudio" if download_type == 'audio' else "best"
        command = f'yt-dlp -f {format_flag} "{url}" -o "{output_file}" --quiet'
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        if process.returncode == 0:
            return jsonify({"message": "Descarga exitosa", "file_url": url_for('serve_file', filename=file_name, _external=True)})
        else:
            return jsonify({"error": "Error al descargar el archivo"}), 500
    else:
        return jsonify({"error": "URL no válida"}), 400

@app.route("/download/<filename>")
def serve_file(filename):
    return send_from_directory(DOWNLOAD_PATH, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)