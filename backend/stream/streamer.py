import pafy
import cv2
import subprocess
from configparser import ConfigParser
from threading import Event
import traceback
import logging


logger = logging.getLogger('main_logger')


class Streamer:
    def __init__(self):
        self.stream_stop_event = Event()

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

    def start_video_stream(self, source_url, dest_url):
        video = pafy.new(source_url)
        best = video.getbest(preftype="mp4")

        if video.duration != '00:00:00':
            logger.error('This video is not live stream.')
            return

        cap = cv2.VideoCapture(best.url)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        streaming_process = self.start_streaming(dest_url, width, height)

        try:
            while not self.stream_stop_event.is_set():
                ret, frame = cap.read()
                if not ret:
                    logger.warning('Frame is empty.')
                    break
                streaming_process.stdin.write(frame.tobytes())
        except Exception:
            traceback.print_exc()
        finally:
            streaming_process.stdin.close()
            streaming_process.terminate()
            cap.release()
            logger.warning('Terminate stream process.')


if __name__ == '__main__':
    parser = ConfigParser()
    parser.read('../config.ini')

    api_key = parser.get('settings', 'api_key')
    src_url = 'https://www.youtube.com/watch?v=RQA5RcIZlAM'
    # src_url = "https://www.youtube.com/watch?v=1KWmTK-ERR0"
    dest_url = "rtmp://localhost/live/test"

    streamer = Streamer()
    streamer.set_api_key(api_key)
    streamer.start_video_stream(src_url, dest_url)
