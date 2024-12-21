from flask import Flask, render_template, request, send_file, redirect, url_for
from yt_dlp import YoutubeDL
import ffmpeg
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Download directory
DOWNLOAD_DIR = "C:/Users/koush/OneDrive/Desktop/MyDownloader/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        format = request.form.get("format")
        if not url:
            return render_template("index.html", error="Please provide a URL.")

        try:
            ydl_opts = {
                'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
                'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio'
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_name = ydl.prepare_filename(info)

                if format == 'mp3':
                    output_file = file_name.rsplit('.', 1)[0] + '.mp3'
                    (
                        ffmpeg
                        .input(file_name)
                        .output(output_file, format='mp3', codec='libmp3lame')
                        .run()
                    )
                    file_name = output_file
            
            return send_file(file_name, as_attachment=True)

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
