from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import os


class AudioPlayer:
    """
    Audio playback module for playing local MP3 files.
    """

    def __init__(self):
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.current_file = None

    def load(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            return
        self.current_file = file_path
        self.player.setSource(QUrl.fromLocalFile(file_path))

    def play(self) -> None:
        if self.current_file:
            self.player.play()

    def pause(self) -> None:
        self.player.pause()

    def stop(self) -> None:
        self.player.stop()
