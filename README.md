<p align="center">
  <img src="https://i.imgur.com/g7XWz9S.png" width="150" alt="SpotiDown Logo" />
</p>

<h1 align="center">SpotiDown</h1>
<h3 align="center">Download Spotify Tracks and Playlists with Full Metadata</h3>

<p align="center">
  <a href="#about-the-project">About</a> •
  <a href="#features">Features</a> •
  <a href="#how-to-install-and-run">Installation</a> •
  <a href="#how-to-use">How to Use</a> •
  <a href="#troubleshooting--faq">Troubleshooting & FAQ</a> •
  <a href="#disclaimer">Disclaimer</a>
</p>

---

<h2 id="about-the-project">About The Project</h2>

**SpotiDown** is a user-friendly desktop application for Windows that allows you to download any track or entire playlist from Spotify. 

Unlike other downloaders, SpotiDown focuses on enriching your music library by fetching and embedding a rich set of metadata directly into your MP3 files. Each downloaded song comes complete with its high-quality album art, artist and album info, and even full song lyrics, ensuring your offline music library looks great in any music player that properly supports local metadata.

<br>

<h2 id="features">Features</h2>

- **Download Single Tracks or Full Playlists:** Just provide a Spotify URL.
- **High-Quality Audio:** Downloads audio from YouTube and converts it to MP3 (192kbps).
- **Rich Metadata:** Automatically embeds tags from Spotify and Genius.com:
  - High-Resolution Album Art
  - Track Title, Artist, Album Name
  - Full Song Lyrics (in both `USLT` and `SYLT` formats for maximum compatibility)
- **Fully Automated Setup:** A smart script handles all dependencies for you.
- **Portable & Self-Contained:** Automatically downloads a local copy of FFmpeg, no system-wide installation needed.
- **User-Friendly Interface:**
  - Clean UI with multi-language support (EN, BG, ES).
  - First-time setup wizard for API keys.
  - Option to change your download folder.
  - Settings menu to update API keys later.

<br>

<h2 id="how-to-install-and-run">How to Install and Run</h2>

The installation is designed to be as simple as possible.

### Step 1: Download the Project

1.  Go to the **[Releases Page](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases)** of this repository. <!-- ЗАМЕНИ С ТВОЯ ЛИНК -->
2.  Download the latest `SpotiDown_v1.0.zip` file.
3.  Extract the ZIP file to a permanent folder on your computer (e.g., `C:\Tools\SpotiDown`). **Do not run it from the Desktop or Downloads folder, as files might get moved.**

### Step 2: Run the Setup & Launch Script

Inside the extracted folder, simply double-click the **`start.bat`** file.

<p align="center">
  <img src="https://i.imgur.com/yF5g5eR.png" alt="Double-click start.bat" />
</p>

**What happens on the first run?**
A command-line window will appear and perform a one-time setup:
1.  It will check if you have Python installed.
2.  It will create a local Python virtual environment (`.venv` folder) to keep dependencies isolated.
3.  It will install all required Python libraries from `requirements.txt`.
4.  It will **automatically download and set up FFmpeg** for you.
5.  Finally, it will launch the SpotiDown application.

This initial setup might take a few minutes depending on your internet speed. All subsequent launches will be instant.

### Step 3: Enter Your API Keys

The first time the app launches, it will prompt you to enter your API keys. This is necessary to fetch high-quality metadata.

- **Spotify Keys:** Go to your [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) to create an app and get your `Client ID` and `Client Secret`.
- **Genius Key:** Go to [Genius API Clients page](https://genius.com/api-clients) to generate your `Access Token`.

Once saved, these keys will be stored locally in a `config.json` file, and you won't be asked for them again. You can change them later from the "Settings" menu.

<br>

<h2 id="how-to-use">How to Use</h2>

<p align="center">
  <img src="https://i.imgur.com/vHq8Y8L.png" width="600" alt="SpotiDown App Interface" />
</p>

1.  **Launch:** Double-click `start.bat`.
2.  **Set Download Folder:** Click **"Browse..."** to choose where your music will be saved.
3.  **Paste URL:** Copy a link to a Spotify track or playlist and paste it into the URL field.
4.  **Download:** Click the **"Start Download"** button.
5.  **Enjoy:** Your new MP3 files, complete with all metadata, will appear in your chosen folder.

<br>

<h2 id="troubleshooting--faq">Troubleshooting & FAQ</h2>

**Q: The black command window shows an error and closes.**
**A:** This is usually due to a network issue or a firewall/antivirus blocking the script.
- Make sure you have a stable internet connection.
- Try running `start.bat` as an Administrator (right-click -> "Run as administrator").
- Check if your antivirus software is blocking PowerShell or the download of FFmpeg.

**Q: I downloaded a song, but the lyrics don't show up in my music app (e.g., Huawei Music, Samsung Music).**
**A:** **This is expected behavior for many default phone music players.**
- **Why it happens:** Modern streaming-focused apps (like Huawei/Samsung Music, Spotify, Apple Music) are designed to **ignore local metadata** for recognizable songs. Instead, they fetch official, licensed, and time-synced lyrics from their own online servers. They do this for legal reasons and to provide a consistent "karaoke-style" experience.
- **How to verify your file is correct:** The text IS embedded in your file. You can verify this using a dedicated desktop player like **VLC**, **AIMP**, or a tag editor like **Mp3tag**.
- **The Solution:** To see the lyrics on your phone, use a music player app that is designed to prioritize local files and their metadata. Excellent free options include **AIMP** or **Musicolet** from the Google Play Store.

**Q: Do I need to install FFmpeg or Git manually?**
**A:** **No!** The `start.bat` script handles everything for you. It uses built-in Windows PowerShell commands to download a pre-compiled version of FFmpeg on the first run. No manual installation or extra software like Git is required.

**Q: Can I use this on Mac or Linux?**
**A:** The core Python code is cross-platform, but the `start.bat` and `setup.ps1` scripts are for Windows only. To run on Mac/Linux, you would need to manually create a virtual environment, run `pip install -r requirements.txt`, install FFmpeg, and then run `python3 main.py`.

<br>

<h2 id="disclaimer">Disclaimer</h2>

This software is provided for educational purposes only. Downloading copyrighted material may be illegal in your country. The developer assumes no responsibility for your actions. Please support the artists by buying their music and streaming on official platforms.