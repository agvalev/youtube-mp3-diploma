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

from .ui_manager import UIManager
from .download_manager import DownloadManager


class YTDGUI(QMainWindow):
    """
    Main GUI application class for yt-downloader-gui YouTube downloader.
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

        # Load UI icons
        self.ui_manager._load_icons()

        # Build user interface
        self.ui_manager._create_ui()

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

    def _connect_signals(self) -> None:
        """Connect Qt signals for thread-safe GUI updates."""
        self.updateStatusSignal.connect(self._update_status)
        self.logMessageSignal.connect(self._log_message)
        self.updateProgressSignal.connect(self._update_progress)
        self.downloadErrorSignal.connect(self._show_download_error_slot)
        self.download_manager.signals.result.connect(self.download_manager._show_video_selection_dialog)
        self.download_manager.signals.error.connect(self.download_manager._on_playlist_error)

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
        print(f"[yt-downloader-gui] {msg}")

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
