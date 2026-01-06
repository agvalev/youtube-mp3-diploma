"""
Handles the download queue and execution.
"""

import os
import re
import threading
import subprocess
import json
import sys
from typing import Dict, List, Any, Tuple, Optional

from PyQt6.QtWidgets import (
    QMessageBox,
    QDialog,
    QScrollArea,
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtGui import QIcon

class WorkerSignals(QObject):
    """Defines signals available from a running worker thread."""
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    download_complete = pyqtSignal()

class DownloadManager:
    """Handles the download queue and execution."""

    def __init__(self, main_app):
        self.main_app = main_app
        self.signals = WorkerSignals()
        self.signals.error.connect(self._on_playlist_error)
        self.signals.result.connect(self._on_playlist_result)
        self.signals.download_complete.connect(self._on_download_complete)

    def _on_playlist_error(self, error_info: tuple) -> None:
        exctype, value = error_info
        QMessageBox.critical(
            self.main_app, "Error", f"Failed to extract playlist information: {value}"
        )

    def _on_playlist_result(self, result: Any) -> None:
        entries, save_path, mode, title = result
        if not entries:
            QMessageBox.warning(
                self.main_app, "Warning", "No videos found in the playlist."
            )
            return
        # Покажи диалога за избор на видео
        self._show_video_selection_dialog(entries, save_path, mode, title)



    def _on_download_complete(self) -> None:
        self.main_app.downloading = False
        self.main_app.updateProgressSignal.emit(0)
        self.process_queue()

    def add_to_queue(self) -> None:
        url = self.main_app.url_entry.text().strip()
        save_path = self.main_app.path_entry.text().strip()
        mode = self.main_app.mode_combo.currentText()

        if not url or not save_path:
            QMessageBox.critical(
                self.main_app, "Error", "Please enter a URL and select a save path."
            )
            return

        if mode in ["Playlist Video", "Playlist MP3"]:
            self._handle_playlist_download(url, save_path, mode)
        elif mode in ["Channel Videos", "Channel Videos MP3", "Channel Shorts", "Channel Shorts MP3"]:
            self._handle_channel_download(url, save_path, mode)
        else:
            self._handle_single_download(url, save_path, mode)

    def _handle_playlist_download(self, url: str, save_path: str, mode: str) -> None:
        if "list=" not in url:
            QMessageBox.critical(
                self.main_app,
                "Error",
                "The URL does not appear to be a playlist URL.\nPlaylist URLs should contain 'list=' parameter.",
            )
            return
        threading.Thread(
            target=self.process_playlist, args=(url, save_path, mode), daemon=True
        ).start()

    def _handle_channel_download(self, url: str, save_path: str, mode: str) -> None:
        if "youtube.com/@" not in url and "/channel/" not in url:
            QMessageBox.critical(
                self.main_app,
                "Error",
                "The URL does not appear to be a channel URL.\nChannel URLs should contain '@' or '/channel/'.",
            )
            return
        if "?" in url:
            QMessageBox.critical(
                self.main_app,
                "Error",
                "Please use a clean channel URL without query parameters.\nExample: https://www.youtube.com/@channelname",
            )
            return
        threading.Thread(
            target=self.process_channel, args=(url, save_path, mode), daemon=True
        ).start()

    def _handle_single_download(self, url: str, save_path: str, mode: str) -> None:
        task = {
            "url": url,
            "save_path": save_path,
            "mode": mode,
            "audio_quality": (
                self.main_app.audio_quality_default if "MP3" in mode else None
            ),
            "video_quality": (
                self.main_app.video_quality_combo.currentText()
                if "MP3" not in mode
                else "Best Available"
            ),
        }

        self.main_app.download_queue.append(task)
        self.main_app.log_message(f"Task added to queue: {mode}")
        self.process_queue()

    def process_playlist(self, url: str, save_path: str, mode: str) -> None:
        try:
            yt_dlp_path = os.path.join(self.main_app.base_dir, "bin", "yt-dlp.exe")
            cmd = [yt_dlp_path, "--quiet", "--flat-playlist", "--dump-json", url]

            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NO_WINDOW

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                creationflags=creationflags,
            )

            entries = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue

            if not entries:
                QMessageBox.warning(
                    self.main_app, "Warning", "No videos found in the playlist."
                )
                return

        except Exception as e:
            QMessageBox.critical(
                self.main_app, "Error", f"Failed to extract playlist information: {e}"
            )
            return

        # ⚡ Поправка: Винаги подаваме 4 аргумента
        self.signals.result.emit(
            (entries, save_path, mode, "Select Videos from Playlist")
        )

    def process_channel(self, url: str, save_path: str, mode: str) -> None:
        suffix = "/videos" if "Videos" in mode else "/shorts"
        if not url.lower().endswith(suffix):
            url = url.rstrip("/") + suffix

        try:
            yt_dlp_path = os.path.join(self.main_app.base_dir, "bin", "yt-dlp.exe")
            cmd = [yt_dlp_path, "--quiet", "--flat-playlist", "--dump-json", url]

            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NO_WINDOW

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                creationflags=creationflags,
            )

            entries = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue

            if "Shorts" in mode:
                entries = [e for e in entries if "shorts" in e.get("url", "").lower()]
            else:
                entries = [e for e in entries if "shorts" not in e.get("url", "").lower()]

            if not entries:
                content_type = "shorts" if "Shorts" in mode else "videos"
                QMessageBox.warning(
                    self.main_app, "Warning", f"No {content_type} found in the channel."
                )
                return

        except Exception as e:
            QMessageBox.critical(
                self.main_app, "Error", f"Failed to extract channel information: {e}"
            )
            return

        dialog_title = (
            "Select Videos from Channel" if "Videos" in mode else "Select Shorts from Channel"
        )
        # ⚡ Поправка: Винаги подаваме 4 аргумента
        self.signals.result.emit((entries, save_path, mode, dialog_title))

    def _show_video_selection_dialog(
        self, entries: List[Dict], save_path: str, mode: str, title: str
    ) -> None:
        dialog = QDialog(self.main_app)
        dialog.setWindowTitle(title)
        dialog.resize(600, 400)

        dlg_layout = QVBoxLayout(dialog)
        info_label = QLabel(f"Found {len(entries)} videos. Select videos to download:")
        info_label.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        dlg_layout.addWidget(info_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        dlg_layout.addWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)
        scroll_layout = QVBoxLayout(container)

        checkboxes = []
        for entry in entries:
            video_url = entry.get("url")
            if video_url and not video_url.startswith("http"):
                base_url = entry.get("webpage_url", "https://www.youtube.com")
                video_url = base_url.rstrip("/") + "/" + video_url.lstrip("/")

            title = entry.get("title", "Unknown Title")
            cb = QCheckBox(title)

            if self.main_app.video_favicon_pixmap:
                cb.setIcon(QIcon(self.main_app.video_favicon_pixmap))

            cb.setChecked(True)
            scroll_layout.addWidget(cb)
            checkboxes.append((video_url, cb))

        button_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(lambda: [cb.setChecked(True) for _, cb in checkboxes])
        button_layout.addWidget(select_all_btn)

        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(lambda: [cb.setChecked(False) for _, cb in checkboxes])
        button_layout.addWidget(deselect_all_btn)

        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)

        download_btn = QPushButton("Download Selected")
        download_btn.setStyleSheet("font-weight: bold;")
        download_btn.clicked.connect(lambda: self._process_selected_videos(checkboxes, save_path, mode, dialog))
        button_layout.addWidget(download_btn)

        dlg_layout.addLayout(button_layout)
        dialog.exec()

    def _process_selected_videos(
        self, checkboxes: List[Tuple], save_path: str, mode: str, dialog
    ) -> None:
        selected_count = 0
        for video_url, cb in checkboxes:
            if cb.isChecked() and video_url:
                task = {
                    "url": video_url,
                    "save_path": save_path,
                    "mode": mode,
                    "audio_quality": (
                        self.main_app.audio_quality_default if "MP3" in mode else None
                    ),
                    "video_quality": (
                        self.main_app.video_quality_combo.currentText()
                        if "MP3" not in mode
                        else "Best Available"
                    ),
                }
                self.main_app.download_queue.append(task)
                selected_count += 1

        if selected_count == 0:
            QMessageBox.warning(dialog, "Warning", "No videos selected for download.")
            return

        self.main_app.log_message(f"Added {selected_count} videos to download queue")
        dialog.accept()
        self.main_app.ui_manager.switch_page("Activity")
        self.process_queue()

    def process_queue(self) -> None:
        if hasattr(self.main_app, "queue_status_label"):
            self.main_app.queue_status_label.setText(
                f"Queue: {len(self.main_app.download_queue)} pending"
            )

        if not self.main_app.downloading and self.main_app.download_queue:
            task = self.main_app.download_queue.pop(0)
            self.main_app.downloading = True
            threading.Thread(target=self.download_video, args=(task,), daemon=True).start()

    def download_video(self, task: Dict[str, Any]) -> None:
        url = task["url"]
        save_path = task["save_path"]
        mode = task["mode"]
        video_quality = task.get("video_quality", "Best Available")

        self.main_app.update_status(f"Starting download: {os.path.basename(url)}")

        try:
            yt_dlp_path = os.path.join(self.main_app.base_dir, "bin", "yt-dlp.exe")
            ffmpeg_path = os.path.join(self.main_app.base_dir, "bin", "ffmpeg.exe")

            if "Video" in mode and "MP3" not in mode:
                cmd = self._build_video_download_command(yt_dlp_path, ffmpeg_path, url, save_path, video_quality)
            else:
                cmd = self._build_audio_download_command(yt_dlp_path, ffmpeg_path, url, save_path, task.get("audio_quality", "320"))

            creationflags = 0
            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NO_WINDOW
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                universal_newlines=True,
                creationflags=creationflags,
            )

            if process.stdout:
                for line in iter(process.stdout.readline, ""):
                    line = line.strip()
                    if line:
                        self.main_app.log_message(line)
                        progress = self._parse_progress(line)
                        if progress is not None:
                            self.main_app.updateProgressSignal.emit(progress)

            process.wait()

            if process.returncode == 0:
                self.main_app.log_message(f"Download completed: {url}")
            else:
                raise subprocess.CalledProcessError(process.returncode, cmd)

        except Exception as e:
            error_msg = f"Download failed for {url}: {str(e)}"
            self.main_app.log_message(error_msg)
            self.main_app.downloadErrorSignal.emit(e)

        finally:
            self.signals.download_complete.emit()

    def _parse_progress(self, line: str) -> Optional[int]:
        match = re.search(r"\[download\]\s+([0-9.]+)%", line)
        if match:
            try:
                return int(float(match.group(1)))
            except (ValueError, IndexError):
                pass
        return None

    def _build_video_download_command(self, yt_dlp_path: str, ffmpeg_path: str, url: str, save_path: str, video_quality: str) -> List[str]:
        cmd = [
            yt_dlp_path,
            "--ffmpeg-location",
            ffmpeg_path,
            "--no-playlist",
            "--output",
            os.path.join(save_path, "%(title)s.%(ext)s"),
            "--format",
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
            "--merge-output-format",
            "mp4",
            url,
        ]
        if video_quality != "Best Available":
            height = video_quality.split("p")[0]
            cmd[cmd.index("--format") + 1] = f"bestvideo[height<={height}]+bestaudio/merge"
        return cmd

    def _build_audio_download_command(self, yt_dlp_path: str, ffmpeg_path: str, url: str, save_path: str, audio_quality: str) -> List[str]:
        cmd = [
            yt_dlp_path,
            "--ffmpeg-location",
            ffmpeg_path,
            "--no-playlist",
            "--output",
            os.path.join(save_path, "%(title)s.%(ext)s"),
            "--format",
            "bestaudio/best",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--audio-quality",
            audio_quality,
            url,
        ]
        return cmd

    def _show_download_error(self, error: Exception) -> None:
        error_text = str(error)
        QMessageBox.critical(self.main_app, "Download Error", f"Download failed:\n\n{error_text}")
