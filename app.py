from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import subprocess, os, uuid
app = Flask(__name__)
app.secret_key = "supersecretkey"
# Directorio temporal para almacenar archivos descargados
TEMP_DOWNLOAD_PATH = "temp_downloads/"
os.makedirs(TEMP_DOWNLOAD_PATH, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        download_type = request.form.get("download_type")
        if url:
            url = url.split('?')[0]
            extension = 'mp3' if download_type == 'audio' else 'mp4'
            base_name = 'audio' if download_type == 'audio' else 'video'
            # Generar un nombre de archivo único para cada descarga
            unique_name = f"{base_name}_{uuid.uuid4().hex[:8]}.{extension}"
            output_file = os.path.join(TEMP_DOWNLOAD_PATH, unique_name)

            format_flag = "bestaudio" if download_type == 'audio' else "best"
            command = f'yt-dlp -f {format_flag} "{url}" -o "{output_file}" --quiet'
            process = subprocess.run(command, shell=True, capture_output=True, text=True)

            if process.returncode == 0:
                flash(f"{download_type.capitalize()} descargado con éxito.", "success")
                return render_template("index3.html", download_url=url_for('download_file', filename=unique_name))
            else:
                flash("Error al descargar el archivo.", "error")
        else:
            flash("Por favor ingresa una URL válida.", "error")
    return render_template("index3.html")

# Ruta para la descarga de archivos
@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(TEMP_DOWNLOAD_PATH, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash("El archivo solicitado no existe.", "error")
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)