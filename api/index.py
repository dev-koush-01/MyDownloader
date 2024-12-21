from flask import Flask, render_template, request, send_file, redirect, url_for
from yt_dlp import YoutubeDL
import ffmpeg
import os
import tempfile

app = Flask(__name__, template_folder="../templates")
app.secret_key = 'your_secret_key'

# Use a temporary directory for downloads
DOWNLOAD_DIR = tempfile.gettempdir()

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
            print(f"Error: {e}")
            return render_template("index.html", error="An error occurred while processing your request.")

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(debug=True, host='0.0.0.0', port=port)
