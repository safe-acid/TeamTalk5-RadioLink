import subprocess
import signal
import os
import threading
import time
import re
from config import Config as conf

class FFmpegPlayer:
    def __init__(self):
        self.process = None
        self.stop_event = threading.Event()
        self.lock = threading.RLock()
        self.max_volume = conf.max_volume
        self.default_volume = max(0, min(int(conf.default_volume), self.max_volume))
        self.current_volume = self.default_volume / 100
        self.current_volume_percent = self.default_volume
        self.current_url = None
        self.audio_sink = getattr(conf, "pulse_sink", "Source")
        self.buffer_seconds = getattr(conf, "stream_buffer_seconds", 10)

    def start_process(self, url):
        with self.lock:
            self.current_url = url
            self.stop_event.clear()
            thread_queue_size = str(max(512, int(self.buffer_seconds) * 512))
            self.process = subprocess.Popen(
                [
                    'ffmpeg',
                    '-hide_banner',
                    '-loglevel', 'warning',
                    '-thread_queue_size', thread_queue_size,
                    '-reconnect', '1',
                    '-reconnect_streamed', '1',
                    '-reconnect_delay_max', '5',
                    '-rw_timeout', '15000000',
                    '-i', url,
                    '-vn',
                    '-filter:a', 'aresample=async=1000:min_hard_comp=0.100:first_pts=0',
                    '-f', 'pulse',
                    self.audio_sink
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                preexec_fn=os.setsid
            )
            self._apply_pulse_volume()
            print("Playing...")

    def play(self, url):
        with self.lock:
            self.stop()
            self.start_process(url)

    def stop(self):
        with self.lock:
            self._stop_process(self.process, "ffmpeg")
            self.process = None
            self.stop_event.set()
            print("Playback stopped.")

    def _stop_process(self, process, name):
        if not process or process.poll() is not None:
            return
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            process.wait(timeout=3)
        except ProcessLookupError:
            pass
        except Exception as e:
            print(f"Error stopping {name} process: {e}")

    def set_volume(self, volume):
        with self.lock:
            volume = max(0, min(int(volume), self.max_volume))
            self.current_volume = volume / 100.0
            self.current_volume_percent = volume
            print(f"Volume set to: {volume}%")
            if self.process and self.process.poll() is None:
                self._apply_pulse_volume()
            elif not self.current_url:
                print("No URL currently set. Cannot set volume.")

    def _apply_pulse_volume(self):
        sink_input = self._find_pulse_sink_input()
        if sink_input is None:
            return
        try:
            subprocess.run(
                ['pactl', 'set-sink-input-volume', sink_input, f'{self.current_volume_percent}%'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False
            )
        except FileNotFoundError:
            pass

    def _find_pulse_sink_input(self):
        if not self.process:
            return None
        player_pid = str(self.process.pid)
        for _ in range(10):
            try:
                result = subprocess.run(
                    ['pactl', 'list', 'sink-inputs'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    check=False
                )
            except FileNotFoundError:
                return None

            current_input = None
            for line in result.stdout.splitlines():
                match = re.match(r'Sink Input #(\d+)', line)
                if match:
                    current_input = match.group(1)
                    continue
                if current_input and f'application.process.id = "{player_pid}"' in line:
                    return current_input
            time.sleep(0.1)
        return None

    def restart_process(self, url):
        with self.lock:
            self.stop()
            self.start_process(url)
