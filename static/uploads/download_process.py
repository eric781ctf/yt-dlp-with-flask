import os
import yt_dlp
import time

def downloads_mp3(links, temp_folder):
    status = []
    for link in links:
        try:
            start_time = time.time()
            ydl_opts = {
                'format': 'bestaudio',
                'outtmpl': os.path.join(temp_folder, '%(title)s.%(ext)s'),
                'quiet': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': r'C:\Users\11404669\Documents\ffmpeg-2025-05-01-git-707c04fe06-full_build\bin'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = yt_dlp.YoutubeDL({'quiet': True}).extract_info(link, download=False)
                title = info.get('title', link)
                duration = int(info.get('duration', 0))
                elapsed = round(time.time() - start_time, 2)
                status.append(f'{title} - 下載完成｜影片長度：{duration}秒｜耗時：{elapsed}秒')
        except Exception as e:
            status.append(f'{link} - 下載失敗: {str(e)}')
    return status

def downloads_mp4(links, quality, temp_folder):
    status = []

    format_map = {
        '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
        '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
        '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
    }

    ydl_format = format_map.get(quality, 'best')

    for link in links:
        try:
            start_time = time.time()
            ydl_opts = {
                'format': ydl_format,
                'outtmpl': os.path.join(temp_folder, '%(title)s.%(ext)s'),
                'quiet': True,
                'merge_output_format': 'mp4',
                'ffmpeg_location': r'C:\Users\11404669\Documents\ffmpeg-2025-05-01-git-707c04fe06-full_build\bin'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                title = info.get('title', link)
                duration = int(info.get('duration', 0))
                elapsed = round(time.time() - start_time, 2)
                status.append(f'{title} - 下載完成｜影片長度：{duration}秒｜耗時：{elapsed}秒')
        except Exception as e:
            status.append(f'{link} - 下載失敗: {str(e)}')
    return status
