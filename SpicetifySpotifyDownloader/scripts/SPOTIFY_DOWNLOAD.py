from flask import Flask, request, render_template_string, jsonify
from flask_cors import CORS
import threading, subprocess, os, time

app = Flask(__name__)
CORS(app)

downloads, output_paths = {}, {}

DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

HTML = """
<!DOCTYPE html>
<html>
<head><title>Spotify Downloader</title></head>
<body>
<h1>Server running ✅</h1>
<h2>Downloads:</h2>
<ul>
{% for track, prog in downloads.items() %}
<li>{{ track }} - {{ prog }}% - {{ output_paths.get(track, "") }}</li>
{% endfor %}
</ul>
</body>
</html>
"""

def download_track(uri):
    downloads[uri] = 0
    output_paths[uri] = DOWNLOAD_FOLDER
    try:
        proc = subprocess.Popen(
            ["python", "-m", "spotdl", "download", uri, "--output", DOWNLOAD_FOLDER],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        while proc.poll() is None:
            for i in range(0, 101, 10):
                downloads[uri] = i
                time.sleep(0.5)
        downloads[uri] = 100
        time.sleep(1)
    finally:
        downloads.pop(uri, None)
        output_paths.pop(uri, None)

@app.route("/")
def status_page():
    return render_template_string(HTML, downloads=downloads, output_paths=output_paths)

@app.route("/status")
def status_api():
    return jsonify({"downloads": downloads, "output_paths": output_paths, "status": "running"})

@app.route("/download")
def download_api():
    uri = request.args.get("uri")
    if uri:
        threading.Thread(target=download_track, args=(uri,), daemon=True).start()
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
