# 🎵 yt-downloader-gui

**yt-downloader-gui** is a professional, cross-platform desktop application for downloading and managing multimedia content from YouTube through a modern and intuitive graphical user interface.

The project is developed in Python using the PyQt6 framework and integrates powerful tools such as yt-dlp for media downloading and ffmpeg for audio and video processing.

The application is designed with a strong focus on **software architecture, usability, security, and background processing**, making it suitable for **real-world use** as well as **academic evaluation and diploma defense**.

---

## 🎯 Project Goals

The main goal of **yt-downloader-gui** is to demonstrate how a **desktop-based multimedia system** can be built by combining:

- A **modern GUI**
- A **powerful media extraction backend**
- **Threaded background processing**
- **Secure URL validation**
- **Clean, modular software architecture**

All technical complexity is abstracted away from the user.  
The user interacts only with simple UI elements, while all heavy operations are executed safely in the background.

---

## 🧠 How the Application Works (Conceptual Overview)

At a high level, yt-downloader-gui acts as a **controller layer** between the user and two specialized media engines:

- **yt-dlp** – media discovery and downloading  
- **ffmpeg** – audio/video processing and conversion  

### Workflow Overview

1. User enters a **YouTube URL**
2. The application validates the URL
3. The link type is detected automatically:
   - Single video
   - Playlist
   - Channel videos
   - Channel shorts
4. Metadata is extracted **without downloading media**
5. The user selects desired items (if applicable)
6. Downloads are added to a **managed queue**
7. Media is downloaded in **background threads**
8. Progress is parsed and displayed in real time
9. Files are processed and saved locally

The UI **never freezes**, even during long downloads.

---

## ⚙️ Backend Processing & Media Handling

### yt-dlp Responsibilities
- URL validation
- Metadata extraction
- Stream resolution
- Playlist & channel handling
- Download execution

### ffmpeg Responsibilities
- Audio/video stream merging
- MP3 conversion
- Bitrate and quality control
- Encoding parameter management

This separation ensures **high reliability** and **clean Python code**, without reinventing complex media logic.

---

## 🔐 Security & URL Validation

Security is a core design principle.

- Only **trusted YouTube domains** are accepted:
  - `youtube.com`
  - `youtu.be`
  - `music.youtube.com`
- Invalid or unknown URLs are rejected immediately
- yt-dlp performs **additional internal validation**
- No execution of untrusted external files

This approach minimizes the risk of malicious downloads or misuse.

---

## 🎓 Academic & Educational Value

The project follows **best practices in software engineering**, including:

- Modular architecture
- Separation of concerns
- Background threading
- Signal/slot communication
- Clean documentation
- Maintainable code structure

Because of this, **yt-downloader-gui** is ideal for:
- Diploma defense
- University projects
- Software architecture demonstrations
- Python GUI coursework

The system can easily be extended with:
- Download history
- Local media playback
- Preset profiles
- Queue prioritization

---

## 🎨 Professional User Interface

- Modern **dark theme**
- Centralized styling via **QSS**
- Larger default window size
- Clean spacing and layout
- Consistent widget styling
- Dedicated Activity & Download views

All UI styling is **fully separated** from logic.

---

## 📊 Real-Time Download Feedback

- Live **progress bar**
- Real-time activity log
- Console output parsing from yt-dlp
- Automatic scrolling log view
- Clear status indicators per task

---

## ⭐ Features

### 🎯 Download Capabilities
- Single video download
- Single MP3 extraction
- Playlist video download
- Playlist MP3 download
- Channel video download
- Channel MP3 download
- Channel Shorts / Shorts MP3

### 🧠 Smart Playlist & Channel Handling
- Fast metadata extraction
- Interactive selection dialog
- Batch processing
- Managed download queue

### 🔑 Authentication Support
- Cookie-based login
- Age-restricted content
- Members-only videos
- Supports `cookies.txt` from browsers

### 🎚 Quality Control
- Video:
  - Best available
  - Fixed resolutions (8K, 4K, 1080p, etc.)
- Audio:
  - MP3 (default **320 kbps**)

### 🔄 Automatic yt-dlp Updater
- GitHub version check via **:contentReference[oaicite:4]{index=4}**
- Automatic binary replacement
- No manual updates required

### 🖥 Cross-Platform Support
- Windows
- Linux
- macOS

---

## 🧩 Application Architecture

The project follows a **clean modular design**.

| Module | Responsibility |
|------|----------------|
| `main_window.py` | Main application window & signals |
| `ui_manager.py` | UI creation, layout, styling |
| `download_manager.py` | Download logic & queue |
| `login_manager.py` | Cookie-based authentication |
| `updater.py` | Automatic yt-dlp updates |

All download operations run in **separate threads**.

---

## 🔁 Download Workflow (Detailed)

1. URL input
2. Domain validation
3. Mode selection
4. Metadata extraction (`--flat-playlist`, `--dump-json`)
5. User selection (if playlist/channel)
6. Queue creation
7. Download execution
8. Media processing via ffmpeg
9. Progress tracking
10. Automatic queue continuation

---

## 📁 Project Structure


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
- **GitHub**
- **Python 3.10+**
- Supported operating systems:
  - Windows
  - Linux
  - macOS

> ⚠️ **Note:**  
> The application relies on **yt-dlp** and **ffmpeg**, which are already included in the `bin/` directory for Windows builds.  
> On Linux/macOS, **ffmpeg** must be installed and available in the system PATH.

---

## 📥 Installation

### Prerequisites
- **Python 3.10 or newer**
- **GitHub**
- Supported operating systems:
  - Windows
  - Linux
  - macOS

> ⚠️ **Note:**  
> On **Windows**, `yt-dlp` and `ffmpeg` are included in the `bin/` directory.  
> On **Linux/macOS**, `ffmpeg` must be installed and available in the system PATH.

---

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/uikraft-hub/yt-downloader-gui.git

# Navigate to the project directory
cd youtube-mp3-for-diploma

# Install Python dependencies
pip install -r requirements.txt

# Run the application
python src/main.py

```

For more detailed documentation, see our [USAGE.md](USAGE.md)

---

## ⚙️ Configuration

### Cookies (Optional – Authentication Support)

To download:
- Age-restricted videos
- Members-only content
- Private videos (where permitted)

Provide a `cookies.txt` file exported from your browser.

**How it works:**
1. Export cookies using a supported browser extension
2. Place `cookies.txt` in the project root directory **or** select it via the application UI
3. Cookies are passed directly to yt-dlp during download execution

No credentials are stored, transmitted, or logged by the application.


---

## 🤝 Contributing

Contributions are welcome and appreciated.

To contribute to this project:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Commit your changes with clear and descriptive commit messages
4. Push the branch to your fork
5. Open a Pull Request targeting the main branch

Before submitting a contribution, please review:
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`

All contributions should follow the project's coding standards and documentation guidelines.


Please see our [Contributing Guide](CONTRIBUTING.md) for details.

---


## 📋 Roadmap

Planned and completed features for **yt-downloader-gui**:

- [x] Modern PyQt6 graphical user interface
- [x] Multiple download modes (video, audio, playlists, channels)
- [x] Playlist and channel metadata preview
- [x] Cookie-based authentication support
- [x] Automatic yt-dlp updater
- [ ] Download history panel
- [ ] Preset quality and format profiles
- [ ] Integrated media preview player
- [ ] Advanced download queue management
- [ ] Localization and multi-language UI support

See the **Issues** section on GitHub for detailed feature requests and known limitations.


---

## 🛡 Security Policy

Security is a core design principle of **yt-downloader-gui**.

The following security measures are implemented:

- Only trusted **YouTube-related domains** are accepted:
  - `youtube.com`
  - `youtu.be`
  - `music.youtube.com`
- All URLs are validated before processing
- No execution of unknown or external binaries
- Media downloads are handled exclusively by **yt-dlp**
- Audio and video processing is performed via **ffmpeg**
- Cookies (if used) are never stored permanently or transmitted externally
- No user credentials are logged or persisted

If you discover a security vulnerability, please report it responsibly by following the guidelines in **SECURITY.md**.


---

## 🙏 Acknowledgments

This project would not be possible without the following open-source technologies and communities:

- **yt-dlp** – for providing a robust and actively maintained media extraction engine
- **PyQt6** – for the modern, cross-platform graphical user interface framework
- **ffmpeg** – for industry-grade audio and video processing
- **GitHub API** – for enabling automatic update checks and seamless integration

Special thanks to the open-source community for continuous improvements, documentation, and support.


