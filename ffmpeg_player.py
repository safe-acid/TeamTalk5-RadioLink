import subprocess
import signal
import os
import threading
from config import Config as conf

class FFmpegPlayer:
    def __init__(self):
        self.process = None
        self.player_process = None
        self.stop_event = threading.Event()
        self.max_volume = conf.max_volume
        self.current_url = None

    def start_process(self, url):
        self.current_url = url
        self.stop_event.clear()
        self.process = subprocess.Popen(
            [
                'ffmpeg', '-loglevel', 'error', '-fflags', 'nobuffer', '-rtbufsize', '250M',
                '-i', url, '-b:a', '128k', '-filter_complex',
                f'[0:a]volume={self.max_volume / 100}[a]', '-map', '[a]', '-f', 'wav', 'pipe:1'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid
        )
        self.player_process = subprocess.Popen(
            ['ffplay', '-nodisp', '-autoexit', '-', '-fflags', 'nobuffer', '-rtbufsize', '250M'],
            stdin=self.process.stdout,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=os.setsid
        )
        print("Playing...")

    def play(self, url):
        self.start_process(url)

    def stop(self):
        if self.process:
            try:
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                self.process.wait()
            except Exception as e:
                print(f"Error stopping ffmpeg process: {e}")
            finally:
                self.process = None
        if self.player_process:
            try:
                os.killpg(os.getpgid(self.player_process.pid), signal.SIGTERM)
                self.player_process.wait()
            except Exception as e:
                print(f"Error stopping ffplay process: {e}")
            finally:
                self.player_process = None
        self.stop_event.set()
        print("Playback stopped.")

    def set_volume(self, volume):
        volume = max(0, min(int(volume), self.max_volume))
        self.current_volume = volume / 100.0
        print(f"Volume set to: {volume}%")
        if self.current_url:
            self.restart_process(self.current_url)
        else:
            print("No URL currently set. Cannot restart process.")

    def restart_process(self, url):
        self.stop()
        self.play(url)
