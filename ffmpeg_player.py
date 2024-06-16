import subprocess
import time
import signal
import os
import threading
from config import Config as conf

class FFmpegPlayer:
    def __init__(self):
        self.process = None
        self.player_process = None
        self.current_volume = 1.0  # Default volume (1.0 is 100%)
        self.stop_event = threading.Event()
        self.max_volume = conf.max_volume

    def start_process(self, url):
        self.stop_event.clear()
        self.process = subprocess.Popen(
            [
                'ffmpeg', '-i', url, '-filter_complex',
                f'[0:a]volume={self.current_volume}[a]', '-map', '[a]', '-f', 'wav', 'pipe:1'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid
        )
        self.player_process = subprocess.Popen(
            ['ffplay', '-nodisp', '-autoexit', '-'],
            stdin=self.process.stdout,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid
        )
        print("Playing...")

    def monitor_ffmpeg(self):
        while not self.stop_event.is_set():
            if self.process.poll() is not None or self.player_process.poll() is not None:
                print("Playback finished or encountered an error.")
                self.stop()
                break
            time.sleep(1)

    def play(self, url):
        self.start_process(url)
        self.monitor_thread = threading.Thread(target=self.monitor_ffmpeg)
        self.monitor_thread.start()

    def stop(self):
        if self.process:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            print("Playback stopped.")
        if self.player_process:
            os.killpg(os.getpgid(self.player_process.pid), signal.SIGTERM)
        self.stop_event.set()

    def set_volume(self, volume):
        # Ensure volume is within the range of 0 to max_volume
        volume = max(0.0, min(float(volume), self.max_volume))
        self.current_volume = volume
        print(f"Volume set to: {volume * 100}%")
        self.restart_process()

    def restart_process(self):
        self.stop()
        time.sleep(1)  # Give it a moment to properly stop
        self.start_process()
        self.monitor_thread = threading.Thread(target=self.monitor_ffmpeg)
        self.monitor_thread.start()
