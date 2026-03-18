import pandas as pd
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import yt_dlp
import imageio_ffmpeg
def run():
    print("download start")
    # ========== НАСТРОЙКИ ==========
    CSV_FILE = 'final_file.csv'
    TRACK_COLUMN = 'Track'
    ARTIST_COLUMN = 'Artist'
    DOWNLOAD_FOLDER = 'music'
    MAX_WORKERS = 6
    # ===============================

    # создаём папку
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    # автоматический ffmpeg
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()


    def clean_filename(name):
        """Очистка имени файла"""
        invalid = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid:
            name = name.replace(char, '_')
        return name[:100]


    def download_single_track(track_info):
        """Скачивание одного трека"""
        idx, row = track_info

        track = str(row[TRACK_COLUMN]).strip() if pd.notna(row[TRACK_COLUMN]) else ""

        if ARTIST_COLUMN in row.index and pd.notna(row[ARTIST_COLUMN]):
            artist = str(row[ARTIST_COLUMN]).strip()
            if artist and artist.lower() != 'nan':
                search_query = f"{artist} - {track}"
                filename = f"{artist} - {track}"
            else:
                search_query = track
                filename = track
        else:
            search_query = track
            filename = track

        if not search_query or search_query == 'nan':
            return False, search_query

        filename = clean_filename(filename)

        output_path = os.path.join(DOWNLOAD_FOLDER, f"{filename}.%(ext)s")

        ydl_opts = {
            "format": "bestaudio/best",
            "ffmpeg_location": ffmpeg_path,
            "outtmpl": output_path,
            "default_search": "ytsearch",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }]
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"ytsearch1:{search_query}"])

            return True, search_query

        except Exception:
            return False, search_query


    def main():

        start_time = time.time()

        try:
            df = pd.read_csv(CSV_FILE)
        except Exception as e:
            print("❌ Ошибка чтения CSV:", e)
            return

        print(f"📊 Найдено треков: {len(df)}")
        print(f"🚀 Потоков загрузки: {MAX_WORKERS}")

        track_infos = [(i, row) for i, row in df.iterrows()]

        failed_tracks = []
        success_count = 0

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:

            futures = [executor.submit(download_single_track, info) for info in track_infos]

            for future in tqdm(as_completed(futures), total=len(futures), desc="Скачивание"):
                success, track = future.result()

                if success:
                    success_count += 1
                else:
                    failed_tracks.append(track)

        elapsed = time.time() - start_time

        print("\n" + "=" * 50)
        print("✅ ЗАВЕРШЕНО")
        print(f"⏱️ Время: {elapsed:.1f} сек ({elapsed/60:.1f} мин)")
        print(f"📥 Скачано: {success_count}")
        print(f"❌ Не скачано: {len(failed_tracks)}")
        print(f"📁 Папка: {DOWNLOAD_FOLDER}")

        if failed_tracks:
            print("\n❌ Не удалось скачать:")
            for t in failed_tracks:
                print(" -", t)


    main()