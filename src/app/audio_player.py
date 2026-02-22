from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
import os


class AudioPlayer:

    def __init__(self):
        self.audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self.audio_output)
        self.current_file = None

    def load(self, file_path: str):
        if not os.path.exists(file_path):
            return

        self.current_file = file_path
        self.player.setSource(QUrl.fromLocalFile(file_path))

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def set_position(self, position):
        self.player.setPosition(position)

    def get_position(self):
        return self.player.position()

    def get_duration(self):
        return self.player.duration()
