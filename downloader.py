# downloader.py
import os
import threading
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TRCK, TDRC, USLT, SYLT
import lyricsgenius
from lang import get_string

try:
    from thefuzz import fuzz
    THEFUZZ_AVAILABLE = True
except ImportError:
    THEFUZZ_AVAILABLE = False

class DownloaderThread(threading.Thread):
    def __init__(self, url, download_type, keys, lang, log_callback, finish_callback, download_path):
        super().__init__()
        self.url = url
        self.download_type = download_type
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
            
            if not os.path.exists(self.download_path):
                os.makedirs(self.download_path)

            sp = None
            genius = None
            if self.keys:
                self.log(get_string('connecting_spotify', self.lang))
                auth_manager = SpotifyClientCredentials(client_id=self.keys['spotify_id'], client_secret=self.keys['spotify_secret'])
                sp = spotipy.Spotify(auth_manager=auth_manager)

                self.log(get_string('connecting_genius', self.lang))
                genius = lyricsgenius.Genius(self.keys['genius_token'], verbose=False, remove_section_headers=True, timeout=15)

            if self.download_type == 'spotify' and sp and genius:
                self.process_spotify_download(ffmpeg_path, sp, genius)
            elif self.download_type == 'youtube':
                self.process_youtube_download(ffmpeg_path, sp, genius)

        except Exception as e:
            self.log(f"CRITICAL ERROR: {e}")
        finally:
            self.log(get_string('process_finished', self.lang))
            self.on_finish()

    def clean_filename(self, filename):
        return "".join([c for c in filename if c.isalnum() or c in (' ', '-')]).rstrip()

    def process_youtube_download(self, ffmpeg_path, sp, genius):
        can_search_metadata = THEFUZZ_AVAILABLE and sp and genius
        if not THEFUZZ_AVAILABLE:
            self.log("WARNING: 'thefuzz' library not found. Cannot search for metadata. Please run start.bat again.")

        initial_ydl_opts = {'quiet': True, 'noprogress': True, 'ignoreerrors': True}
        with yt_dlp.YoutubeDL(initial_ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=False)
            videos = info.get('entries', [info])

            for video in videos:
                if not video: continue
                
                original_title = video['title']
                video_url = video['webpage_url']
                final_filepath = ""
                spotify_track_info = None

                if can_search_metadata:
                    self.log(f"{get_string('yt_metadata_search', self.lang)} '{original_title}'")
                    best_match, best_score = self.find_best_spotify_match(video, sp)
                    
                    if best_match and best_score > 75: # Вдигаме прага за по-голяма сигурност
                        self.log(f"{get_string('yt_metadata_found', self.lang).format(best_score)}")
                        artist_name = best_match['artists'][0]['name']
                        track_name = best_match['name']
                        log_name = f"{artist_name} - {track_name}"
                        self.log(f"   -> {log_name}")
                        
                        safe_filename = self.clean_filename(log_name)
                        final_filepath = os.path.join(self.download_path, f"{safe_filename}.mp3")
                        spotify_track_info = best_match
                    else:
                        self.log(get_string('yt_metadata_not_found', self.lang))
                        safe_filename = self.clean_filename(original_title)
                        final_filepath = os.path.join(self.download_path, f"{safe_filename}.mp3")
                else:
                    safe_filename = self.clean_filename(original_title)
                    final_filepath = os.path.join(self.download_path, f"{safe_filename}.mp3")

                if os.path.exists(final_filepath):
                    self.log(f"{get_string('song_skipped', self.lang)} {os.path.basename(final_filepath).replace('.mp3','')}")
                    continue

                self.log(f"{get_string('downloading_song', self.lang)} {original_title}")
                
                download_ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
                    'outtmpl': final_filepath.replace('.mp3', ''),
                    'quiet': True, 'noprogress': True, 'ffmpeg_location': ffmpeg_path
                }

                try:
                    with yt_dlp.YoutubeDL(download_ydl_opts) as download_ydl:
                        download_ydl.download([video_url])
                    
                    if spotify_track_info and genius:
                        self.add_metadata(final_filepath, spotify_track_info, genius)
                        
                    self.log(f"{get_string('song_done', self.lang)} {os.path.basename(final_filepath).replace('.mp3','')}")
                except Exception as download_error:
                    self.log(f"!! DOWNLOAD ERROR for '{original_title}': {download_error}")
                    if os.path.exists(final_filepath):
                        try: os.remove(final_filepath)
                        except OSError: pass

    # --- ИЗЦЯЛО ПРЕРАБОТЕНА ФУНКЦИЯ ЗА НАМИРАНЕ НА СЪВПАДЕНИЕ ---
    def find_best_spotify_match(self, video_info, sp):
        yt_title = video_info.get('title', '')
        
        # 1. По-агресивно почистване
        clean_title = yt_title.lower()
        clean_title = re.sub(r'\[.*?\]', '', clean_title)
        clean_title = re.sub(r'\(.*?\)', '', clean_title)
        
        junk_words = [
            'official', 'music', 'video', 'audio', 'lyrics', 'lyric', 'hd', '4k', 'hq', 
            'visualizer', 'explicit', 'official video', 'full album', 'extended', 'version'
        ]
        pattern = r'\b(' + '|'.join(junk_words) + r')\b'
        clean_title = re.sub(pattern, '', clean_title, flags=re.IGNORECASE)
        
        # 2. Премахване на специални символи и разделители
        clean_title = re.sub(r'[^\w\s]', ' ', clean_title)
        clean_title = re.sub(r'\s+', ' ', clean_title).strip()
        
        self.log(f"{get_string('yt_cleaned_title', self.lang)} '{clean_title}'")
        if not clean_title: return None, 0

        try:
            # 3. Използваме почистеното заглавие за търсене в Spotify
            results = sp.search(q=clean_title, type='track', limit=10)
            if not results['tracks']['items']: return None, 0

            best_match, best_score = None, 0
            for track in results['tracks']['items']:
                artist_name = track['artists'][0]['name'].lower()
                track_name = track['name'].lower()
                spotify_title = f"{artist_name} {track_name}"
                
                # 4. Използваме най-добрия алгоритъм за сравнение при излишни думи
                score = fuzz.token_set_ratio(clean_title, spotify_title)
                
                # 5. Бонус точки за съвпадение на канал
                channel_name = video_info.get('channel', '').lower()
                if artist_name in channel_name or \
                   f"{artist_name}vevo" in channel_name.replace(' ', ''):
                    score = min(score + 10, 100)
                
                if score > best_score:
                    best_score, best_match = score, track
            
            return best_match, best_score
        except Exception as e:
            self.log(f"   -> Spotify search error: {e}")
            return None, 0

    def process_spotify_download(self, ffmpeg_path, sp, genius):
        tracks_to_process = []
        if "playlist" in self.url:
            results = sp.playlist_tracks(self.url)
            playlist_items = results['items']
            while results['next']:
                results = sp.next(results)
                playlist_items.extend(results['items'])
            for item in playlist_items:
                if item['track']: tracks_to_process.append(item['track'])
        elif "track" in self.url:
            tracks_to_process.append(sp.track(self.url))
        
        self.log(get_string('found_tracks', self.lang).format(len(tracks_to_process)))

        for track in tracks_to_process:
            if not track: continue
            original_track_name = track['name']
            artist_name = track['artists'][0]['name']
            log_name = f"{artist_name} - {original_track_name}"
            safe_filename = self.clean_filename(log_name)
            mp3_filepath = os.path.join(self.download_path, f"{safe_filename}.mp3")

            if os.path.exists(mp3_filepath):
                self.log(f"{get_string('song_skipped', self.lang)} {log_name}")
                continue
            
            try:
                self.log(f"{get_string('downloading_song', self.lang)} {log_name}")
                search_query = f"{artist_name} - {original_track_name} audio"
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
                    'outtmpl': mp3_filepath.replace('.mp3', ''),
                    'default_search': 'ytsearch1:', 'quiet': True, 'noprogress': True, 'ffmpeg_location': ffmpeg_path
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([search_query])

                self.add_metadata(mp3_filepath, track, genius)
                self.log(f"{get_string('song_done', self.lang)} {log_name}")
            except Exception as download_error:
                self.log(f"!! DOWNLOAD ERROR for '{log_name}': {download_error}")
                if os.path.exists(mp3_filepath):
                    try: os.remove(mp3_filepath)
                    except OSError: pass
                continue

    def add_metadata(self, mp3_filepath, track, genius):
        audio = MP3(mp3_filepath, ID3=ID3)
        if audio.tags is None: audio.add_tags()

        original_track_name = track['name']
        artist_name = track['artists'][0]['name']
        album_name = track['album']['name']

        audio.tags.add(TIT2(encoding=3, text=original_track_name))
        audio.tags.add(TPE1(encoding=3, text=artist_name))
        audio.tags.add(TALB(encoding=3, text=album_name))

        try:
            if track['album']['images']:
                album_art_url = track['album']['images'][0]['url']
                response = requests.get(album_art_url, timeout=10)
                if response.status_code == 200:
                    audio.tags.delall('APIC')
                    audio.tags.add(APIC(encoding=3, mime=response.headers.get('Content-Type', 'image/jpeg'), type=3, desc='Cover', data=response.content))
        except Exception as art_error:
            self.log(f"   -> INFO: Could not fetch album art: {art_error}")

        try:
            song = genius.search_song(original_track_name, artist_name)
            if song and song.lyrics:
                cleaned_lyrics = song.lyrics.strip()
                if cleaned_lyrics:
                    audio.tags.delall('USLT')
                    audio.tags.add(USLT(encoding=3, lang='eng', desc='Lyrics', text=cleaned_lyrics))
            else:
                self.log(f"   -> INFO: Lyrics not found on Genius.com.")
        except Exception as lyrics_error:
            self.log(f"   -> INFO: Error fetching lyrics: {lyrics_error}")
        
        audio.save(v2_version=3)