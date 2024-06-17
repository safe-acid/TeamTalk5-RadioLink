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
        self.current_url = None  # Store the current URL
        self.monitor_thread = None
        self.monitor_thread_lock = threading.Lock()

    def start_process(self, url):
        self.current_url = url  # Update the current URL
        self.stop_event.clear()
        self.process = subprocess.Popen(
          [
                'ffmpeg', '-loglevel', 'error', '-fflags', 'nobuffer', '-rtbufsize', '250M',
                '-i', url, '-b:a', '128k', '-filter_complex',
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
        last_output_time = time.time()
        while not self.stop_event.is_set():
            if self.process.poll() is not None or self.player_process.poll() is not None:
                print("Playback finished or encountered an error.")
                self.stop()
                break

            # Check if the process is still outputting data
            output = self.process.stderr.readline()
            if output:
                last_output_time = time.time()
                print(output.strip())

            # Restart if frozen for more than 60 seconds
            if time.time() - last_output_time > 60:
                print("FFmpeg process frozen, restarting...")
                self.restart_process(self.current_url)
                break
            
            time.sleep(1)

    def play(self, url):
        self.start_process(url)
        with self.monitor_thread_lock:
            if self.monitor_thread is not None and self.monitor_thread.is_alive():
                self.monitor_thread.join()  # Wait for the previous monitor thread to exit
            self.monitor_thread = threading.Thread(target=self.monitor_ffmpeg)
            self.monitor_thread.start()

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
        # Ensure volume is within the range of 0 to 100
        volume = max(0, min(int(volume), 100))
        self.current_volume = volume / 100.0  # Convert to 0.0 - 1.0 range for FFmpeg
        print(f"Volume set to: {volume}%")
        if self.current_url:
            self.restart_process(self.current_url)
        else:
            print("No URL currently set. Cannot restart process.")

    def restart_process(self, url):
        self.stop()
        time.sleep(1)  # Give it a moment to properly stop
        self.start_process(url)
        with self.monitor_thread_lock:
            if self.monitor_thread is not None and self.monitor_thread.is_alive():
                self.monitor_thread.join()  # Wait for the previous monitor thread to exit
            self.monitor_thread = threading.Thread(target=self.monitor_ffmpeg)
            self.monitor_thread.start()