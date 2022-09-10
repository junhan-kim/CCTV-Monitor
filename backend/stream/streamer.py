import logging
import subprocess
import traceback
from multiprocessing import Process, Event
import re

import cv2
import pafy


logger = logging.getLogger('main_logger')


class Streamer(Process):
    def __init__(self, youtube_api_key, source_url, dest_url):
        Process.__init__(self)
        self.set_youtube_api_key(youtube_api_key)
        self.stream_stop_event = Event()
        self.source_url = source_url
        self.dest_url = dest_url
        self.opencv_url = self.convert_source_url_to_opencv_url(source_url)

    def set_youtube_api_key(self, api_key):
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
                   '-max_muxing_queue_size', '1024',
                   '-f', 'flv',
                   '-hide_banner',
                   '-loglevel', 'error',
                   f'{dest_url}']
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, shell=False)
        return proc

    def stop_video_stream(self):
        self.stream_stop_event.set()

    def start_video_stream(self):
        try:
            cap = cv2.VideoCapture(self.opencv_url)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            streaming_process = self.start_streaming(self.dest_url, width, height)
            logger.info('start streaming')

            while not self.stream_stop_event.is_set():
                ret, frame = cap.read()
                if not ret:
                    logger.warning('Frame is empty.')
                else:
                    streaming_process.stdin.write(frame.tobytes())

        except Exception:
            traceback.print_exc()
        finally:
            streaming_process.stdin.close()
            streaming_process.terminate()
            cap.release()
            logger.warning('Terminate stream process.')

    def convert_source_url_to_opencv_url(self, source_url):
        # youtube url
        if re.match('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', source_url):
            logger.info('source: youtube url')
            video = pafy.new(source_url)
            if video.duration != '00:00:00':
                logger.error('This video is not live stream.')
                raise Exception('This video is not live stream.')
            best = video.getbest(preftype="mp4")
            return best.url
        # m3u8 url
        elif re.match('.*m3u8$', source_url):
            logger.info('source: m3u8 url')
            return source_url
        else:
            raise Exception('Source url match Failed')

    def run(self):
        self.start_video_stream()
