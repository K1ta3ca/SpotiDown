# downloader.py
import os
import threading
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TRCK, TDRC, USLT, SYLT
import lyricsgenius
from lang import get_string

class DownloaderThread(threading.Thread):
    def __init__(self, spotify_url, keys, lang, log_callback, finish_callback, download_path):
        super().__init__()
        self.spotify_url = spotify_url
        self.keys = keys
        self.lang = lang
        self.log = log_callback
        self.on_finish = finish_callback
        self.download_path = download_path
        self.daemon = True

    def run(self):
        try:
            ffmpeg_path = os.path.join(os.getcwd(), 'ffmpeg', 'bin')
            if not os.path.exists(os.path.join(ffmpeg_path, 'ffmpeg.exe')):
                self.log("ERROR: FFmpeg not found. Please re-run start.bat to install it automatically.")
                raise FileNotFoundError("FFmpeg executable not found in the expected path.")

            self.log(get_string('connecting_spotify', self.lang))
            auth_manager = SpotifyClientCredentials(client_id=self.keys['spotify_id'], client_secret=self.keys['spotify_secret'])
            sp = spotipy.Spotify(auth_manager=auth_manager)

            self.log(get_string('connecting_genius', self.lang))
            genius = lyricsgenius.Genius(self.keys['genius_token'], verbose=False, remove_section_headers=True, timeout=15)

            tracks_to_process = []
            if "playlist" in self.spotify_url:
                results = sp.playlist_tracks(self.spotify_url)
                playlist_items = results['items']
                while results['next']:
                    results = sp.next(results)
                    playlist_items.extend(results['items'])
                for item in playlist_items:
                    if item['track']: tracks_to_process.append(item['track'])
            elif "track" in self.spotify_url:
                track_info = sp.track(self.spotify_url)
                tracks_to_process.append(track_info)
            
            self.log(get_string('found_tracks', self.lang).format(len(tracks_to_process)))

            if not os.path.exists(self.download_path):
                os.makedirs(self.download_path)

            for track in tracks_to_process:
                if not track: continue
                
                original_track_name = track['name']
                artist_name = track['artists'][0]['name']
                
                log_name = f"{artist_name} - {original_track_name}"
                safe_filename = "".join([c for c in log_name if c.isalnum() or c in (' ', '-')]).rstrip()
                mp3_filepath = os.path.join(self.download_path, f"{safe_filename}.mp3")

                if os.path.exists(mp3_filepath):
                    self.log(f"{get_string('song_skipped', self.lang)} {log_name}")
                    continue
                
                # --- ТУК ЗАПОЧВА НОВАТА ЛОГИКА ЗА ГРЕШКИ ---
                try:
                    # Стъпка 1: Сваляне
                    self.log(f"{get_string('downloading_song', self.lang)} {log_name}")
                    search_query = f"{artist_name} - {original_track_name} audio"
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
                        'outtmpl': os.path.join(self.download_path, f"{safe_filename}.%(ext)s"),
                        'default_search': 'ytsearch1:', 'quiet': True, 'noprogress': True, 'ffmpeg_location': ffmpeg_path
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([search_query])

                    # Стъпка 2: Добавяне на метаданни (вече сваленият файл е сигурен)
                    self.add_metadata(mp3_filepath, track, genius)
                    self.log(f"{get_string('song_done', self.lang)} {log_name}")

                except Exception as download_error:
                    # Този блок ще се изпълни САМО ако свалянето се провали
                    self.log(f"!! CRITICAL DOWNLOAD ERROR for '{log_name}': {download_error}")
                    if os.path.exists(mp3_filepath):
                        try:
                            os.remove(mp3_filepath)
                            self.log(f"   -> Corrupted file deleted. The song will be retried on next run.")
                        except OSError as e:
                            self.log(f"   -> FAILED TO DELETE corrupted file: {e}")
                    continue # Продължаваме към следващата песен
                # --- КРАЙ НА НОВАТА ЛОГИКА ---

        except Exception as e:
            self.log(f"CRITICAL ERROR (outside song loop): {e}")
        finally:
            self.log(get_string('process_finished', self.lang))
            self.on_finish()

    def add_metadata(self, mp3_filepath, track, genius):
        # --- ТУК Е ВТОРАТА ЧАСТ ОТ ПРОМЯНАТА ---
        audio = MP3(mp3_filepath, ID3=ID3)
        if audio.tags is None: audio.add_tags()

        original_track_name = track['name']
        masked_track_name = original_track_name + '\u200B'
        artist_name = track['artists'][0]['name']
        album_name = track['album']['name']

        # Добавяме основните тагове
        audio.tags.add(TIT2(encoding=3, text=masked_track_name))
        audio.tags.add(TPE1(encoding=3, text=artist_name))
        audio.tags.add(TALB(encoding=3, text=album_name))

        # Опитваме да добавим обложка в отделен try-except блок
        try:
            if track['album']['images']:
                album_art_url = track['album']['images'][0]['url']
                response = requests.get(album_art_url, timeout=10)
                if response.status_code == 200:
                    audio.tags.delall('APIC')
                    audio.tags.add(APIC(encoding=3, mime=response.headers.get('Content-Type', 'image/jpeg'), type=3, desc='Cover', data=response.content))
        except Exception as art_error:
            self.log(f"   -> INFO: Could not fetch album art: {art_error}")

        # Опитваме да добавим текст в отделен try-except блок
        try:
            song = genius.search_song(original_track_name, artist_name)
            if song and song.lyrics:
                cleaned_lyrics = song.lyrics.strip()
                if cleaned_lyrics:
                    audio.tags.delall('USLT'); audio.tags.delall('SYLT')
                    audio.tags.add(USLT(encoding=3, lang='eng', desc='Lyrics', text=cleaned_lyrics))
                    audio.tags.add(SYLT(encoding=3, lang='eng', format=2, type=1, desc='Lyrics', text=[(cleaned_lyrics, 0)]))
            else:
                self.log(f"   -> INFO: Lyrics not found on Genius.com.")
        except Exception as lyrics_error:
            self.log(f"   -> INFO: Error fetching lyrics: {lyrics_error}")
        
        # Запазваме файла с каквато информация сме успели да съберем
        audio.save(v2_version=3)