import os
import shutil
import zipfile
import time
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from static.uploads import download_process, zip_files

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
ZIP_FOLDER = 'zips'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(ZIP_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        quality = request.form.get('quality')
        filename = secure_filename(file.filename)
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        file.save(filepath)

        with open(filepath, 'r') as f:
            links = [line.strip() for line in f if line.strip()]

        archive_name = os.path.join(ZIP_FOLDER, f'youtube_batch.zip')
        temp_folder = os.path.join(DOWNLOAD_FOLDER, 'temp')
        os.makedirs(temp_folder, exist_ok=True)

        if quality == 'mp3':
            status = download_process.downloads_mp3(links, temp_folder)
        else:
            status = download_process.downloads_mp4(links, quality, temp_folder)

        zip_files.zip_downloads_file(archive_name, temp_folder)

        # 清除暫存影片
        shutil.rmtree(temp_folder)
        time.sleep(4)
        os.remove(filepath)

        return render_template('index.html', status=status, zip_ready=True)

    return render_template('index.html', status=[], zip_ready=False)

@app.route('/download')
def download():
    return send_file(os.path.join(ZIP_FOLDER, 'youtube_batch.zip'), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
