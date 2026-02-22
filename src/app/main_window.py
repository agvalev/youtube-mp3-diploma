"""
Main GUI application class for yt-downloader-gui YouTube downloader.
"""

import os
import sys
import threading
from typing import Dict, List, Any, Optional

from PyQt6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QLineEdit,
    QComboBox,
    QLabel,
    QProgressBar,
    QTextEdit,
    QWidget,
    QStackedWidget,
    QStatusBar,
)
from PyQt6.QtCore import pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QFileDialog
import os
from PyQt6.QtMultimedia import QMediaPlayer


from .ui_manager import UIManager
from .download_manager import DownloadManager
from .audio_player import AudioPlayer



class YTDGUI(QMainWindow):
    """
    Main GUI application class for yt-downloader-gui YouTube downloader.

    This class implements the complete user interface and handles all user interactions,
    download management, and application state.
    """

    # Custom signals for thread-safe GUI updates
    updateStatusSignal = pyqtSignal(str)
    logMessageSignal = pyqtSignal(str)
    updateProgressSignal = pyqtSignal(int)
    downloadErrorSignal = pyqtSignal(object)

    # UI elements (dynamically added by UIManager)
    url_entry: QLineEdit
    path_entry: QLineEdit
    mode_combo: QComboBox
    video_quality_label: QLabel
    video_quality_combo: QComboBox
    progress_bar: QProgressBar
    log_text: QTextEdit
    queue_status_label: QLabel
    video_favicon_pixmap: Optional[QPixmap]
    icons: Dict[str, QIcon]
    sidebar: QWidget
    stack: QStackedWidget
    download_page: QWidget
    activity_page: QWidget
    status_bar: QStatusBar
    mode_var: str  # Stores the current download mode

    def __init__(self, base_dir: str):
        """
        Initialize the main application window and all components.

        Args:
            base_dir: The base directory of the application.
        """
        super().__init__()

        # Window configuration
        self.setWindowTitle("yt-downloader-gui")
        self.resize(800, 600)
        self.base_dir = base_dir

        # Initialize manager components
        self.ui_manager = UIManager(self)
        self.download_manager = DownloadManager(self)

        # Set application icon
        self.ui_manager._set_window_icon()

        # Initialize application state
        self._initialize_state()

        # Initialize audio player
        self.audio_player = AudioPlayer()


        # Load UI icons
        self.ui_manager._load_icons()

        # Build user interface
        self.ui_manager._create_ui()

        self.audio_player.player.positionChanged.connect(self.update_audio_position)
        self.audio_player.player.durationChanged.connect(self.update_audio_duration)
        self.audio_player.player.playbackStateChanged.connect(self.update_play_button)


        if hasattr(self, "audio_slider"):
            self.audio_slider.sliderMoved.connect(
                lambda pos: self.audio_player.set_position(pos)
        )
            
        if hasattr(self, "volume_slider"):
            self.volume_slider.valueChanged.connect(
                lambda value: self.audio_player.audio_output.setVolume(value / 100)
            )



        # Connect signals for thread-safe updates
        self._connect_signals()

        # Initial status
        self.update_status("Ready")

    def _initialize_state(self) -> None:
        """Initialize application state variables."""
        # Download management
        self.download_queue: List[Dict[str, Any]] = []
        self.downloading = False

        # Audio settings
        self.audio_quality_default = "320"

        # Authentication settings
        self.use_cookies = False
        self.cookie_browser = "chrome"
        self.cookie_file: Optional[str] = None

    def _connect_signals(self) -> None:
        """Connect Qt signals for thread-safe GUI updates."""
        self.updateStatusSignal.connect(self._update_status)
        self.logMessageSignal.connect(self._log_message)
        self.updateProgressSignal.connect(self._update_progress)
        self.downloadErrorSignal.connect(self._show_download_error_slot)
        self.download_manager.signals.result.connect(self.on_playlist_result)
        self.download_manager.signals.error.connect(self.on_playlist_error)

    def on_playlist_result(self, result):
        entries, save_path, mode, title = result
        self.download_manager._show_video_selection_dialog(
            entries, save_path, mode, title
        )

    def on_playlist_error(self, error_info):
        exctype, value = error_info
        QMessageBox.critical(
            self, "Error", f"Failed to extract playlist information: {value}"
        )

    def select_save_path(self) -> None:
        """Open folder selection dialog for download location."""
        directory = QFileDialog.getExistingDirectory(self, "Select Download Folder")

        if directory:
            self.path_entry.setText(directory)
            self.update_status("Save path selected")

    def update_status(self, message: str) -> None:
        """Update status bar message (thread-safe)."""
        self.updateStatusSignal.emit(message)

    def _update_status(self, message: str) -> None:
        """Internal method to update status bar in main thread."""
        self.status_bar.showMessage(message)

    def _update_progress(self, value: int) -> None:
        """Internal method to update progress bar in main thread."""
        if hasattr(self, "progress_bar"):
            self.progress_bar.setValue(value)

    def log_message(self, msg: str) -> None:
        """Log message to activity panel and console (thread-safe)."""
        self.logMessageSignal.emit(msg)
        print(f"[yt-downloader-gui] {msg}")  # Also log to console

    def _log_message(self, msg: str) -> None:
        """Internal method to add message to log widget in main thread."""
        if hasattr(self, "log_text"):
            from datetime import datetime
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_msg = f"[{timestamp}] {msg}"
            self.log_text.append(formatted_msg)

    def _show_download_error_slot(self, error: Exception) -> None:
        """Slot method to show download error dialog safely in main thread."""
        self.download_manager._show_download_error(error)


    def play_audio(self):

        # Ако вече има заредена песен → resume
        if self.audio_player.current_file:
            self.audio_player.play()
            self.update_status("Resumed audio")
            return

        # Ако няма заредена → избери файл
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select MP3 File",
            "",
            "Audio Files (*.mp3)"
        )

        if file_path:
            self.audio_player.load(file_path)
            self.audio_player.play()

            # Показва името автоматично
            if hasattr(self, "song_label"):
                self.song_label.setText(os.path.basename(file_path))

            self.update_status("Playing audio")




    def pause_audio(self):
        self.audio_player.pause()
        self.update_status("Audio paused")


    def stop_audio(self):
        self.audio_player.stop()
        self.update_status("Audio stopped")

    def update_audio_position(self, position):
    # Движи слайдера
        if hasattr(self, "audio_slider"):
            self.audio_slider.setValue(position)

    # Обновява времето
        if hasattr(self, "time_label"):
            current = position // 1000
            total = self.audio_player.get_duration() // 1000
            total = max(total, 0)


            self.time_label.setText(
                f"{self.format_time(current)} / {self.format_time(total)}"
            )


    def update_audio_duration(self, duration):
        # Задава максимума на слайдера
        if hasattr(self, "audio_slider"):
            self.audio_slider.setRange(0, duration)


    def format_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02}:{secs:02}"


    def update_play_button(self, state):
        if not hasattr(self, "play_btn"):
            return

        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_btn.setText("⏸ Pause")
        else:
            self.play_btn.setText("▶ Play")

