# main.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import os
from lang import get_string
from downloader import DownloaderThread

CONFIG_FILE = 'config.json'

class ApiKeysPrompt(tk.Toplevel):
    def __init__(self, parent, lang, current_keys=None):
        super().__init__(parent)
        self.lang = lang
        self.keys = None
        self.transient(parent)
        self.title(get_string('keys_prompt_title', self.lang))
        self.geometry("500x300")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.grab_set()
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(main_frame, text=get_string('keys_prompt_message', self.lang), wraplength=480).pack(pady=10)
        self.spotify_id_var = tk.StringVar()
        self.spotify_secret_var = tk.StringVar()
        self.genius_token_var = tk.StringVar()
        if current_keys:
            self.spotify_id_var.set(current_keys.get('spotify_id', ''))
            self.spotify_secret_var.set(current_keys.get('spotify_secret', ''))
            self.genius_token_var.set(current_keys.get('genius_token', ''))
        self.entries = []
        ttk.Label(main_frame, text="Spotify Client ID:").pack(anchor=tk.W, padx=10)
        spotify_id_entry = ttk.Entry(main_frame, textvariable=self.spotify_id_var, width=70)
        spotify_id_entry.pack(fill=tk.X, padx=10, pady=(0, 5))
        self.entries.append(spotify_id_entry)
        ttk.Label(main_frame, text="Spotify Client Secret:").pack(anchor=tk.W, padx=10)
        spotify_secret_entry = ttk.Entry(main_frame, textvariable=self.spotify_secret_var, width=70)
        spotify_secret_entry.pack(fill=tk.X, padx=10, pady=(0, 5))
        self.entries.append(spotify_secret_entry)
        ttk.Label(main_frame, text="Genius.com Access Token:").pack(anchor=tk.W, padx=10)
        genius_token_entry = ttk.Entry(main_frame, textvariable=self.genius_token_var, width=70)
        genius_token_entry.pack(fill=tk.X, padx=10, pady=(0, 5))
        self.entries.append(genius_token_entry)
        ttk.Button(main_frame, text=get_string('save_keys_button', self.lang), command=self.save).pack(pady=20)
        self.make_context_menu()
        self.wait_window(self)
    def make_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Cut", command=lambda: self.focus_get().event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Copy", command=lambda: self.focus_get().event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Paste", command=lambda: self.focus_get().event_generate("<<Paste>>"))
        for entry in self.entries:
            entry.bind("<Button-3>", self.show_context_menu)
    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)
    def save(self):
        self.keys = {'spotify_id': self.spotify_id_var.get().strip(), 'spotify_secret': self.spotify_secret_var.get().strip(), 'genius_token': self.genius_token_var.get().strip()}
        if all(self.keys.values()): self.destroy()
        else: messagebox.showwarning("Warning", "All fields are required.", parent=self)
    def on_closing(self):
        self.keys = None
        self.destroy()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_lang = 'en'
        self.app_config = self.load_config()
        self.setup_ui()
        self.update_language()
        if not self.app_config.get('api_keys') or not all(self.app_config['api_keys'].values()):
            self.prompt_for_keys()

    def prompt_for_keys(self):
        current_keys = self.app_config.get('api_keys')
        prompt = ApiKeysPrompt(self, self.current_lang, current_keys)
        if prompt.keys:
            self.app_config['api_keys'] = prompt.keys
            self.save_config()
            messagebox.showinfo("Success", "API Keys saved successfully!", parent=self)
        elif not current_keys:
            self.destroy()
            
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, AttributeError): pass
        return {'api_keys': None, 'download_path': 'downloads'}
        
    def save_config(self):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.app_config, f, indent=4, ensure_ascii=False)
            
    def setup_ui(self):
        self.title(get_string('window_title', self.current_lang))
        self.geometry("600x500")
        self.minsize(500, 450)
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Change API Keys", command=self.prompt_for_keys)
        
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill=tk.X, pady=(0, 15))
        self.lang_label = ttk.Label(lang_frame, text=get_string('lang_label', self.current_lang))
        self.lang_label.pack(side=tk.LEFT, padx=(0, 5))
        self.lang_var = tk.StringVar(value='English')
        self.lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=['English', 'Български', 'Español'], state='readonly')
        self.lang_combo.pack(side=tk.LEFT)
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_lang_change)

        service_frame = ttk.Frame(main_frame)
        service_frame.pack(fill=tk.X, pady=(0, 5))
        self.service_label = ttk.Label(service_frame, text=get_string('service_label', self.current_lang))
        self.service_label.pack(side=tk.LEFT, padx=(0, 5))
        self.service_var = tk.StringVar(value='Spotify')
        self.service_combo = ttk.Combobox(service_frame, textvariable=self.service_var, values=['Spotify', 'YouTube'], state='readonly')
        self.service_combo.pack(side=tk.LEFT)

        self.url_label = ttk.Label(main_frame, text=get_string('url_label', self.current_lang))
        self.url_label.pack(anchor=tk.W, pady=(10,0))
        self.url_entry = ttk.Entry(main_frame, width=70)
        self.url_entry.pack(fill=tk.X, pady=(0,10))
        self.make_context_menu_for_entry(self.url_entry)
        
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=5)
        self.folder_label = ttk.Label(folder_frame, text=get_string('download_folder_label', self.current_lang))
        self.folder_label.pack(side=tk.LEFT, anchor=tk.W)
        self.download_path_var = tk.StringVar(value=self.app_config.get('download_path', 'downloads'))
        folder_entry = ttk.Entry(folder_frame, textvariable=self.download_path_var, state='readonly')
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.browse_button = ttk.Button(folder_frame, text=get_string('browse_button', self.current_lang), command=self.browse_folder)
        self.browse_button.pack(side=tk.LEFT)

        self.start_button = ttk.Button(main_frame, text=get_string('start_button', self.current_lang), command=self.start_download)
        self.start_button.pack(pady=15)
        
        self.progress_label = ttk.Label(main_frame, text=get_string('progress_label', self.current_lang))
        self.progress_label.pack(anchor=tk.W)
        self.progress_text = scrolledtext.ScrolledText(main_frame, height=15, state='disabled', wrap=tk.WORD)
        self.progress_text.pack(fill=tk.BOTH, expand=True)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_path_var.set(folder_selected)
            self.app_config['download_path'] = folder_selected
            self.save_config()
            
    def make_context_menu_for_entry(self, entry):
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Cut", command=lambda: entry.event_generate("<<Cut>>"))
        context_menu.add_command(label="Copy", command=lambda: entry.event_generate("<<Copy>>"))
        context_menu.add_command(label="Paste", command=lambda: entry.event_generate("<<Paste>>"))
        entry.bind("<Button-3>", lambda event: context_menu.tk_popup(event.x_root, event.y_root))
        
    def on_lang_change(self, event=None):
        lang_map = {'English': 'en', 'Български': 'bg', 'Español': 'es'}
        self.current_lang = lang_map[self.lang_var.get()]
        self.update_language()
        
    def update_language(self):
        self.title(get_string('window_title', self.current_lang))
        self.lang_label.config(text=get_string('lang_label', self.current_lang))
        self.service_label.config(text=get_string('service_label', self.current_lang))
        self.url_label.config(text=get_string('url_label', self.current_lang))
        self.start_button.config(text=get_string('start_button', self.current_lang))
        self.progress_label.config(text=get_string('progress_label', self.current_lang))
        self.folder_label.config(text=get_string('download_folder_label', self.current_lang))
        self.browse_button.config(text=get_string('browse_button', self.current_lang))
        
    def log_message(self, message):
        self.progress_text.config(state='normal')
        self.progress_text.insert(tk.END, message + "\n")
        self.progress_text.see(tk.END)
        self.progress_text.config(state='disabled')
        self.update_idletasks()
        
    def start_download(self):
        # Проверката за API ключове вече е задължителна за всички операции
        if not self.app_config.get('api_keys') or not all(self.app_config['api_keys'].values()):
            messagebox.showerror("Грешка", "API ключовете не са настроени или са непълни. Моля, въведете ги от менюто 'Settings', за да използвате всички функции.", parent=self)
            return
            
        service = self.service_var.get().lower()
        url = self.url_entry.get().strip()
        if not url:
            return

        self.start_button.config(state='disabled')
        self.clear_log()
        
        download_path = self.download_path_var.get()
        
        downloader = DownloaderThread(url, service, self.app_config['api_keys'], self.current_lang, self.log_message, self.enable_start_button, download_path)
        downloader.start()
        
    def enable_start_button(self):
        self.start_button.config(state='normal')

    def clear_log(self):
        self.progress_text.config(state='normal')
        self.progress_text.delete(1.0, tk.END)
        self.progress_text.config(state='disabled')

if __name__ == "__main__":
    app = App()
    app.mainloop()