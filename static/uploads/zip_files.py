import shutil
import zipfile
import os


def zip_downloads_file(archive_name, temp_folder):
    # 打包成 zip
    with zipfile.ZipFile(archive_name, 'w') as zipf:
        for root, _, files in os.walk(temp_folder):
            for file in files:
                filepath = os.path.join(root, file)
                zipf.write(filepath, arcname=file)