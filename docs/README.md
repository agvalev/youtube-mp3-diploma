# 🎵 yt-downloader-gui

**yt-downloader-gui** is a professional desktop application designed for downloading and managing multimedia content from **YouTube** in a secure, structured, and user-friendly way. The application is developed using **Python** and **PyQt6** and provides a complete graphical interface that allows users to download **videos and audio (MP3)** from individual YouTube videos, playlists, and entire channels.

The main objective of the project is to demonstrate the implementation of a **desktop-based multimedia system** that integrates a modern graphical user interface with a powerful backend for network content processing. The application focuses on **usability, modular architecture, background processing, and basic network security**, making it suitable for both real-world use and academic evaluation.

Unlike simple command-line download tools, yt-downloader-gui abstracts all technical complexity behind a clean and intuitive interface. The user interacts only with clearly defined controls such as input fields, buttons, and selection dialogs, while all heavy operations — such as link analysis, metadata extraction, download execution, and audio/video processing — are performed automatically in the background.

---

### 🧠 How the Application Works – High-Level Overview

At a conceptual level, yt-downloader-gui functions as a **controller layer** between the user and two specialized multimedia tools: **yt-dlp** and **ffmpeg**. The graphical interface collects user input, validates it, and translates it into structured commands that are executed safely and efficiently by the backend.

The application workflow begins when the user provides a **YouTube URL**. This URL is analyzed to determine its type:
- single video
- playlist
- channel videos
- channel shorts

Based on the selected download mode, the application dynamically chooses the appropriate processing strategy. For playlists and channels, the system performs a fast metadata scan without downloading the media itself. This allows the user to preview and select specific videos before initiating the actual download process.

All download operations are executed in **separate background threads**, ensuring that the user interface remains fully responsive at all times. Progress information is continuously captured from the download process and displayed visually through a progress bar and detailed activity log.

---

### ⚙️ Backend Processing and Media Handling

The core downloading logic is powered by **yt-dlp**, a robust and actively maintained media extraction tool. yt-dlp is responsible for:
- validating the YouTube URL
- extracting metadata
- resolving video and audio streams
- handling playlists and channel feeds

Once the media streams are downloaded, **ffmpeg** is used to perform all audio and video processing tasks, such as:
- merging video and audio streams
- converting audio to MP3 format
- controlling output quality and encoding parameters

This separation of responsibilities ensures high reliability and industry-grade media handling while keeping the Python application itself clean, readable, and maintainable.

---

### 🔐 Security and URL Validation

To protect the user from downloading content from untrusted or potentially malicious sources, the application includes multiple layers of validation. Only URLs that match known YouTube domains are accepted for processing. Additionally, yt-dlp itself performs strict internal validation and rejects unsupported or unsafe URLs.

By restricting downloads to trusted platforms and avoiding direct file execution from unknown sources, the application significantly reduces the risk of malware exposure during media extraction.

---

### 🎓 Academic and Educational Focus

yt-downloader-gui is intentionally designed following **best practices in software engineering**, including:
- modular code structure
- separation of concerns
- background threading
- signal-based communication
- clear documentation

These characteristics make the project especially suitable for **diploma defense**, as it demonstrates not only functional correctness but also architectural thinking, security awareness, and user-centered design.

The project can be easily extended with additional features such as playlist management, local media playback, or download history, making it a strong foundation for future development.

---

### 🎨 Professional UI Redesign
- Complete visual overhaul with a modern **dark theme**
- Centralized styling using a dedicated **QSS stylesheet**
- Improved layout and spacing with a larger default window size
- Consistent styling across all widgets

### 📊 Enhanced Download Feedback
- Real-time **progress bar** on the Activity page
- Progress parsing directly from `yt-dlp` console output
- Live scrolling activity log

### 🧹 Code Refinements
- Removed inline widget styling
- Added object names for precise QSS targeting
- Clear separation between UI, logic, and background workers

---

## ⭐ Features

### 🎯 Download Capabilities
- **Single Video Download**
- **Single MP3 Extraction**
- **Playlist Video Download**
- **Playlist MP3 Download**
- **Channel Videos Download**
- **Channel MP3 Download**
- **Channel Shorts / Shorts MP3**

### 🧠 Smart Playlist & Channel Handling
- Automatic extraction of video metadata
- Interactive dialog for selecting individual videos
- Batch processing using a managed download queue

### 🔐 Security & URL Validation
- Accepts **only YouTube-related URLs**
  - `youtube.com`
  - `youtu.be`
  - `music.youtube.com`
- Prevents accidental downloads from untrusted or malicious sources
- Additional validation is performed internally by `yt-dlp`

### 🔑 Authentication Support
- Cookie-based login support for:
  - Age-restricted videos
  - Private or members-only content
- Compatible with browser extensions exporting `cookies.txt`

### 🎚 Quality Control
- Video: Best available or fixed resolutions (8K, 4K, 1080p, etc.)
- Audio: MP3 extraction (default **320 kbps**)

### 🔄 Automatic yt-dlp Updater
- Automatically checks GitHub for updates
- Replaces the local `yt-dlp` binary when a new version is available
- No manual updates required

### 🖥 Cross-Platform
- Works on **Windows, Linux, and macOS**
- Uses `ffmpeg` for audio/video processing

---

## 🧩 Application Architecture

The project follows a **modular architecture**, ensuring maintainability and scalability.

| Module | Description |
|------|------------|
| `main_window.py` | Main application window and signal handling |
| `ui_manager.py` | UI creation, layout, and styling |
| `download_manager.py` | Download logic, queue management, yt-dlp integration |
| `login_manager.py` | Cookie-based authentication |
| `updater.py` | Automatic yt-dlp update system |

All download operations are executed in **background threads**, ensuring a responsive user interface.

---

## 🔁 Download Workflow (Step-by-Step)

1. User enters a **YouTube URL**
2. The URL is validated to ensure it belongs to YouTube
3. User selects a download mode (video, MP3, playlist, channel)
4. `yt-dlp` extracts metadata using:
   - `--flat-playlist`
   - `--dump-json`
5. For playlists/channels, the user selects specific videos
6. Selected tasks are added to a **download queue**
7. Media is downloaded via `yt-dlp`
8. Audio/video processing is handled by `ffmpeg`
9. Progress is tracked and displayed in real time
10. Files are saved locally and the queue continues automatically

---


## 📁 Folder Structure

```
yt-downloader-gui/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── RELEASE_TEMPLATE.md
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── assets/
│   ├── screenshots/
│   │   └── screenshot.png
│   └── yt-downloader-gui-logo.ico
├── docs/
│   ├── CHANGELOG.md
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   ├── README.md
│   ├── SECURITY.md
│   ├── STATUS.md
│   └── USAGE.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── download_manager.py
│   │   ├── login_manager.py
│   │   ├── main_window.py
│   │   ├── ui_manager.py
│   │   └── updater.py
│   ├── assets/
│   │   ├── activity.png
│   │   ├── download.png
│   │   ├── style.qss
│   │   └── video-favicon.png
│   ├── bin/
│   │   ├── ffmpeg.exe
│   │   └── yt-dlp.exe
│   ├── build.bat
│   ├── favicon.ico
│   └── main.py
└── tests/
    ├── __init__.py
    ├── test_download_manager.py
    └── test_updater.py

```

---


## 🕹 Usage

### Prerequisites

- GitHub

### Installation

```bash
# Clone the repository
git clone https://github.com/uikraft-hub/yt-downloader-gui.git
```

For more detailed documentation, see our [USAGE.md](USAGE.md)

---

## 🤝 Contributing

Please see our [Contributing Guide](CONTRIBUTING.md) for details.

---


## 📋 Roadmap

- [x] Modern PyQt6 GUI
- [x] Multiple Download Modes
- [x] Automatic yt‑dlp Updater

See the [open issues](https://github.com/uikraft-hub/yt-downloader-gui/issues) for a full list of proposed features and known issues.

---


## 🙏 Acknowledgments

* **yt-dlp** for the robust download backend
* **PyQt6** for the modern GUI framework
* **ffmpeg** for audio/video processing
* **GitHub API** for seamless updater integration


