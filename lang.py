# lang.py
LANGUAGES = {
    'window_title': {
        'en': 'SpotiDown',
        'bg': 'SpotiDown',
        'es': 'SpotiDown'
    },
    'service_label': {
        'en': 'Service:',
        'bg': 'Услуга:',
        'es': 'Servicio:'
    },
    'url_label': {
        'en': 'URL (Playlist, Track, or Video):',
        'bg': 'URL (Плейлист, Песен или Видео):',
        'es': 'URL (Playlist, Canción o Video):'
    },
    'start_button': {
        'en': 'Start',
        'bg': 'Старт',
        'es': 'Iniciar'
    },
    'progress_label': {
        'en': 'Log:',
        'bg': 'Прогрес:',
        'es': 'Registro:'
    },
    'lang_label': {
        'en': 'Language:',
        'bg': 'Език:',
        'es': 'Idioma:'
    },
    'download_folder_label': {
        'en': 'Download Folder:',
        'bg': 'Папка за сваляне:',
        'es': 'Carpeta de Descarga:'
    },
    'browse_button': {
        'en': 'Browse...',
        'bg': 'Избери...',
        'es': 'Explorar...'
    },
    'keys_prompt_title': {
        'en': 'API Keys Required',
        'bg': 'Необходими са API Ключове',
        'es': 'Se Requieren Claves de API'
    },
    'keys_prompt_message': {
        'en': 'Please enter your API keys to continue. This is a one-time setup.',
        'bg': 'Моля, въведете вашите API ключове, за да продължите. Това е еднократна настройка.',
        'es': 'Por favor, ingrese sus claves de API para continuar. Esta es una configuración única.'
    },
    'save_keys_button': {
        'en': 'Save and Continue',
        'bg': 'Запази и Продължи',
        'es': 'Guardar y Continuar'
    },
    'downloading_song': {
        'en': 'Downloading:',
        'bg': 'Сваля се:',
        'es': 'Descargando:'
    },
    'song_done': {
        'en': '✓ Done:',
        'bg': '✓ Готово:',
        'es': '✓ Hecho:'
    },
    'song_skipped': {
        'en': '→ Skipped (already exists):',
        'bg': '→ Пропуснато (вече съществува):',
        'es': '→ Omitido (ya existe):'
    },
    'yt_metadata_search': {
        'en': '   -> Searching for metadata for:',
        'bg': '   -> Търсене на метаданни за:',
        'es': '   -> Buscando metadatos para:'
    },
    # --- НОВ ТЕКСТ ---
    'yt_cleaned_title': {
        'en': '   -> Cleaned title for search:',
        'bg': '   -> Почистено заглавие за търсене:',
        'es': '   -> Título limpiado para búsqueda:'
    },
    # --- КРАЙ НА НОВИЯ ТЕКСТ ---
    'yt_metadata_found': {
        'en': '   -> Match found with {}% confidence:',
        'bg': '   -> Намерено съвпадение със {}% сигурност:',
        'es': '   -> Coincidencia encontrada con {}% de confianza:'
    },
    'yt_metadata_not_found': {
        'en': '   -> INFO: Could not find a confident metadata match. Saving with original title.',
        'bg': '   -> ИНФО: Не е намерено достатъчно добро съвпадение. Файлът е запазен с оригиналното заглавие.',
        'es': '   -> INFO: No se encontró una coincidencia de metadatos confiable. Guardando con el título original.'
    },
    'process_finished': {
        'en': '\n--- Finished! ---',
        'bg': '\n--- Процесът приключи! ---',
        'es': '\n--- ¡Proceso Terminado! ---'
    },
    'connecting_spotify': {
        'en': 'Connecting to Spotify API...',
        'bg': 'Свързване със Spotify API...',
        'es': 'Conectando a la API de Spotify...'
    },
    'connecting_genius': {
        'en': 'Connecting to Genius.com API...',
        'bg': 'Свързване с Genius.com API...',
        'es': 'Conectando a la API de Genius.com...'
    },
    'found_tracks': {
        'en': 'Found {} tracks to process.',
        'bg': 'Намерени {} песни за обработка.',
        'es': 'Se encontraron {} canciones para procesar.'
    }
}

def get_string(key, lang_code='en'):
    """Взема текстовия низ за даден ключ и език."""
    return LANGUAGES.get(key, {}).get(lang_code, f"[{key}]")