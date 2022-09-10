import logging
import subprocess
import traceback
from multiprocessing import Process, Event
import re

import cv2
import pafy


logger = logging.getLogger('main_logger')


class Streamer(Process):
    def __init__(self, source_url, dest_url, youtube_api_key=''):
        Process.__init__(self)

        # check youtube api key
        if youtube_api_key:
            self.set_youtube_api_key(youtube_api_key)
        else:
            if self.is_youtube_url(source_url):
                logger.error('youtube_api_key not exist with youtube source url')
                raise Exception('youtube_api_key not exist with youtube source url.')

        # params
        self.source_url = source_url
        self.dest_url = dest_url
        self.opencv_url = self.convert_source_url_to_opencv_url(source_url)
        logger.info(f'opencv_url: {self.opencv_url}')

        # error handling
        self.stream_stop_event = Event()
        self.err_cnt = 0
        self.max_err_cnt = 1000

        # init stream process
        self.cap = cv2.VideoCapture(self.opencv_url)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.streaming_process = self.init_stream_process(self.dest_url, self.width, self.height)
        self.cap.release()
        logger.info('start stream process')

    def set_youtube_api_key(self, api_key):
        pafy.set_api_key(api_key)

    def is_youtube_url(self, url):
        return re.match('^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$', url)

    def convert_source_url_to_opencv_url(self, source_url):
        # youtube url
        if self.is_youtube_url(source_url):
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

    def init_stream_process(self, dest_url, width, height):
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

    def start_video_stream(self):
        try:
            logger.info('Starting video stream')
            self.cap = cv2.VideoCapture(self.opencv_url)  # since opencv restriction of sharing variable with __init__

            while not self.stream_stop_event.is_set():
                ret, frame = self.cap.read()
                if not ret:
                    self.err_cnt += 1
                    if self.err_cnt % 100 == 0:
                        logger.warning(f'Frame is empty. {self.err_cnt}')
                    if self.err_cnt > self.max_err_cnt:  # set up new VideoCapture
                        self.cap.release()
                        self.cap = cv2.VideoCapture(self.opencv_url)
                        logger.warning('set up new VideoCapture for refresh TCP connection.')
                        self.err_cnt = 0
                else:
                    self.streaming_process.stdin.write(frame.tobytes())
                    self.err_cnt = 0

        except Exception:
            traceback.print_exc()
        finally:
            self.terminate_video_stream()

    def stop_video_stream(self):
        logger.info('Stopping video streaming')
        self.stream_stop_event.set()

    def terminate_video_stream(self):
        self.streaming_process.stdin.close()
        self.streaming_process.terminate()
        self.cap.release()
        logger.warning('Terminate stream process.')

    def run(self):
        self.start_video_stream()
