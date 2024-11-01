from flask import Flask, request, render_template, jsonify, send_file
import os
import subprocess

app = Flask(__name__)

# Directorio temporal para guardar los archivos descargados
TEMP_DOWNLOAD_DIR = "C:/Dev/PYTHON/APPS------ANDRES/descargas_youtube/"
os.makedirs(TEMP_DOWNLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        download_type = request.form.get("download_type")
        
        if not url:
            return jsonify({"error": "URL no proporcionada"}), 400

        # Determinar el formato de descarga
        extension = 'mp3' if download_type == 'audio' else 'mp4'
        base_name = 'audio' if download_type == 'audio' else 'video'
        output_file = os.path.join(TEMP_DOWNLOAD_DIR, f"{base_name}.{extension}")

        # Ejecutar el comando de descarga
        format_flag = "bestaudio" if download_type == 'audio' else "best"
        command = f'yt-dlp -f {format_flag} "{url}" -o "{output_file}" --quiet'
        
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if process.returncode != 0:
            return jsonify({"error": "Error al descargar el video: " + process.stderr}), 500

        # Devolver la URL del archivo descargado
        return jsonify({"download_url": f"/download/{os.path.basename(output_file)}"}), 200
    
    return render_template("index.html")

@app.route('/download/<filename>', methods=['GET'])
def serve_file(filename):
    try:
        return send_file(os.path.join(TEMP_DOWNLOAD_DIR, filename), as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)