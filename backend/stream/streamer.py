import pafy
import cv2
import time
import subprocess
from configparser import ConfigParser
from threading import Event
import traceback
import logging
from threading import Thread

from util.watchdog import Watchdog


logger = logging.getLogger('main_logger')


class Streamer(Thread):
    def __init__(self, api_key, source_url, dest_url):
        Thread.__init__(self)
        self.set_api_key(api_key)
        self.stream_stop_event = Event()
        self.stream_start_event = Event()
        self.source_url = source_url
        self.dest_url = dest_url

    def set_api_key(self, api_key):
        pafy.set_api_key(api_key)

    def start_streaming(self, dest_url, width, height):
        command = ['ffmpeg',
                   '-y',
                   '-f', 'rawvideo',
                   '-vcodec', 'rawvideo',
                   '-pix_fmt', 'bgr24',
                   '-s', f'{width}x{height}',
                   '-re',
                   '-i', '-',
                   '-c:v', 'libx264',
                   '-pix_fmt', 'yuv420p',
                   '-preset', 'ultrafast',
                   '-f', 'flv',
                   f'{dest_url}']
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, shell=False)
        return proc

    def stop_video_stream(self):
        self.stream_stop_event.set()

    def check_start_stream(self):
        try:
            watchdog = Watchdog(10)
            while not self.stream_start_event.is_set():
                logger.info('Check stream start.')
                time.sleep(1)
            logger.info('Success stream start.')
        except Watchdog:
            raise TimeoutError
        finally:
            watchdog.stop()

    def start_video_stream(self, source_url, dest_url):
        video = pafy.new(source_url)
        best = video.getbest(preftype="mp4")

        if video.duration != '00:00:00':
            logger.error('This video is not live stream.')
            return

        try:
            cap = cv2.VideoCapture(best.url)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            streaming_process = self.start_streaming(dest_url, width, height)
            self.check_start_stream()

            while not self.stream_stop_event.is_set():
                ret, frame = cap.read()
                if not ret:
                    logger.warning('Frame is empty.')
                    break
                streaming_process.stdin.write(frame.tobytes())

                if not self.stream_start_event.is_set():
                    self.stream_start_event.set()

        except Exception:
            traceback.print_exc()
        finally:
            streaming_process.stdin.close()
            streaming_process.terminate()
            cap.release()
            logger.warning('Terminate stream process.')

    def run(self):
        self.start_video_stream(self.source_url, self.dest_url)
