<p align="center">
  <a href="https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases">
    <img src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/.github/pic/SpotiDown.png" alt="SpotiDown Logo" />
  </a>
</p>

<h1 align="center">SpotiDown</h1>
<h3 align="center">Download Spotify Tracks and Playlists with Full Metadata</h3>

<p align="center">
  <a href="#about-the-project">About</a> •
  <a href="#features">Features</a> •
  <a href="#requirements">Requirements</a> •
  <a href="#installation">Installation</a> •
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
- **Rich Metadata:** Automatically embeds tags from Spotify and Genius.com.
- **Fully Automated Setup:** A smart script handles all dependencies for you.
- **Portable & Self-Contained:** Automatically downloads a local copy of FFmpeg. **No manual installation needed!**
- **User-Friendly Interface:** Clean UI with multi-language support, settings menu, and more.

<br>

<h2 id="requirements">Requirements</h2>

There is only **one manual prerequisite** before you can run the application:

-   **Python:** You must have Python (version 3.8 or higher) installed.
    -   You can download it from [**python.org**](https://www.python.org/).
    -   **IMPORTANT:** During the Python installation, you **must** check the box that says **"Add Python to PATH"**. The setup script relies on this.

<p align="center">
  <img src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/.github/pic/python.png" alt="Add Python to PATH checkbox" />
</p>

### What is handled automatically?

You **do not** need to install any of the following yourself. The `start.bat` script will handle them for you:
-   All required Python libraries (`spotipy`, `yt-dlp`, etc.).
-   **FFmpeg:** The script automatically downloads a pre-compiled, portable version. **You do not need Git.**

<br>

<h2 id="installation">Installation</h2>

The installation is designed to be as simple as possible.

### Step 1: Download the Project

1.  Go to the **[Releases Page](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases)** of this repository.
2.  Download the latest `SpotiDown_v1.0.zip` file.
3.  Extract the ZIP file to a permanent folder on your computer (e.g., `C:\Tools\SpotiDown`).

### Step 2: Run the Setup & Launch Script

Inside the extracted folder, simply double-click the **`start.bat`** file. The script will automatically install all dependencies and then launch the application.

<p align="center">
  <img src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/.github/pic/start.png" alt="Automated setup process" />
</p>

This initial setup might take a few minutes depending on your internet speed. All subsequent launches will be instant.

### Step 3: Enter Your API Keys

The first time the app launches, it will prompt you to enter your API keys from Spotify and Genius.com. Once saved, you won't be asked for them again. You can change them later from the "Settings" menu.

<br>

<h2 id="how-to-use">How to Use</h2>

<p align="center">
  <img src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO_NAME/main/.github/pic/app.png" width="600" alt="SpotiDown App Interface" />
</p>

1.  **Launch:** Double-click `start.bat`.
2.  **Set Download Folder:** Click **"Browse..."** to choose where your music will be saved.
3.  **Paste URL:** Copy a link to a Spotify track or playlist and paste it into the URL field.
4.  **Download:** Click the **"Start Download"** button.

<br>

<h2 id="troubleshooting--faq">Troubleshooting & FAQ</h2>

**Q: The setup script (black window) shows an error and closes.**
**A:** This is usually due to a network issue or a firewall/antivirus blocking the script.
-   Make sure you have a stable internet connection.
-   Try running `start.bat` as an Administrator (right-click -> "Run as administrator").
-   Check if your antivirus software is blocking PowerShell or the download of FFmpeg.

**Q: I downloaded a song, but the lyrics don't show up in my phone's music app.**
**A:** **This is expected behavior for many default phone music players.** Modern streaming apps are designed to **ignore local metadata** and fetch lyrics from their own online servers. To see the embedded lyrics, use a player that prioritizes local files, such as **AIMP** or **Musicolet** (free on Google Play Store).

<br>

<h2 id="disclaimer">Disclaimer</h2>

This software is provided for educational purposes only. Downloading copyrighted material may be illegal in your country. The developer assumes no responsibility for your actions. Please support the artists by buying their music and streaming on official platforms.