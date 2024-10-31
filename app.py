from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import subprocess
import os
app = Flask(__name__)
app.secret_key = "supersecretkey"
output_path = "C:/Dev/PYTHON/APPS------ANDRES/descargas_youtube/"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        download_type = request.form.get("download_type")
        if url:
            url = url.split('?')[0]
            extension = 'mp3' if download_type == 'audio' else 'mp4'
            counter = 1
            while True:
                output_file = os.path.join(output_path, f"{counter}.{extension}")
                if not os.path.exists(output_file):
                    break
                counter += 1
            format_flag = "bestaudio" if download_type == 'audio' else "best"
            command = f'yt-dlp -f {format_flag} "{url}" -o "{output_file}" --quiet'
            process = subprocess.run(command, shell=True, capture_output=True, text=True)
            if process.returncode == 0:
                flash(f"{download_type.capitalize()} descargado con éxito como {os.path.basename(output_file)}.", "success")
                return redirect(url_for("download_file", filename=os.path.basename(output_file)))
            else:
                flash("Error al descargar el archivo.", "error")
        else:
            flash("Por favor ingresa una URL válida.", "error")
        return redirect(url_for("index"))
    return render_template("index5.html")

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(output_path, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)