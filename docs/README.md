
## 🆕 What’s New in v1.0.0

- **Professional UI Redesign**
  - Complete visual overhaul with a new professional dark theme.
  - Consistent styling across all widgets using a dedicated QSS stylesheet.
  - Improved layout with a larger default window size for a better user experience.
- **Enhanced Download Progress**
  - Added a visual progress bar to the "Activity" page for real-time download feedback.
  - The progress bar is updated dynamically by parsing `yt-dlp`'s output.
- **Code Refinements**
  - Removed all inline styling in favor of the new stylesheet.
  - Added object names to widgets for more specific styling.

---

## ⭐ Features

- **Automatic yt‑dlp Updater**  
  Checks GitHub for new yt-dlp releases and replaces your local binary automatically.
- **Multiple Download Modes**  
  - Single Video / MP3  
  - Playlist Video / Playlist MP3  
  - Channel Videos / Channel MP3  
  - Channel Shorts / Shorts MP3
- **Cookie‑Based Login**  
  Import YouTube cookies via “Get cookies.txt Locally” extension for authenticated downloads.
- **Modern PyQt6 GUI**  
  Intuitive sidebar, real‑time status, and scrolling activity log.
- **Flexible Quality Options**  
  Choose best‑available or specific resolutions (8K, 4K, 1080p, etc.); MP3 defaults to 320 kbps.
- **Lightweight & Cross‑Platform**  
  Single‑file app plus assets; runs on Windows, macOS, and Linux (ffmpeg required).

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

### Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

---

## 📋 Roadmap

- [x] Modern PyQt6 GUI
- [x] Multiple Download Modes
- [x] Automatic yt‑dlp Updater

See the [open issues](https://github.com/uikraft-hub/yt-downloader-gui/issues) for a full list of proposed features and known issues.

---

## 📝 Changelog

All notable changes to this project are documented in [CHANGELOG.md](CHANGELOG.md).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

## 🙏 Acknowledgments

* **yt-dlp** for the robust download backend
* **PyQt6** for the modern GUI framework
* **ffmpeg** for audio/video processing
* **GitHub API** for seamless updater integration

---



