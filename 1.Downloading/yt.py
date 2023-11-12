import yt_dlp
import time
import os
from pyperclip import paste

def download_video_with_retries(video_url, output_path='.', max_retries=5):
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path + '/%(title)s.%(ext)s',
        'noplaylist': True,
    }
    
    attempt = 0
    while attempt < max_retries:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                break  # If download succeeds, break out of the loop
        except yt_dlp.utils.DownloadError as e:
            attempt += 1
            wait = 2 ** attempt  # Exponential backoff
            print(f"Download failed, retrying in {wait} seconds...")
            time.sleep(wait)
    else:
        print("Max retries reached, download failed.")

os.chdir('D:\Temp\youtube')
# Replace 'YOUR_VIDEO_URL' with the actual URL of the YouTube video you want to download
download_video_with_retries(paste())
os.system('start .')