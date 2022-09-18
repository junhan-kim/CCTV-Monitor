import subprocess
import re
import datetime
import traceback
import os
from threading import Thread
import time
import requests
import redis

from logger import set_default_logger


logger = set_default_logger('main_logger')
rd = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)


# 채널 명, 요청 시간 등의 정보를 받아옴
def LogOutputGenerator(log_path):
    # tail -f 로 파일에 대한 실시간 로그를 출력하는 프로세스를 올리고, 해당 프로세스의 stdout을 계속해서 읽음
    proc = subprocess.Popen(['tail', '-F', log_path],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        while True:
            line = proc.stdout.readline()  # wait for stdout bytes
            string = line.decode('utf-8').strip()  # decoding to utf-8

            # regex for channel name and requested time
            match = re.search(
                r'\[([0-9]{1,2}/[a-zA-Z]{3}/[0-9]{4}:[0-9]{2}:[0-9]{2}:[0-9]{2}).*/hls/([0-9a-z-]*)/', string)

            try:
                requested_date = match.group(1)
                channel_name = match.group(2)
            except Exception:
                logger.warning(f'match failed in string => {string}')
                continue

            yield {
                'requested_date': requested_date,
                'channel_name': channel_name
            }
    except Exception:
        traceback.print_exc()
        raise StopIteration
    finally:
        proc.terminate()


def get_all_channel_names():
    dir_name = '/mnt/hls'
    return os.listdir(dir_name)


def stop_channel(channel_name):
    url = f'http://localhost:8989/stream/stop'
    res = requests.post(url, json={
        "channelName": channel_name
    })
    if res.status_code == 200:
        logger.info(f'stop channel => {channel_name}')
    else:
        logger.warning(f'failed to stop channel => {channel_name}')


class Cleaner(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.execution_interval = 10
        self.expiry_time_delta = datetime.timedelta(minutes=30, seconds=0)

    def run(self):
        while True:
            logger.info('start clean up channels')
            current_date = datetime.datetime.now()
            channel_names = get_all_channel_names()

            for channel_name in channel_names:
                last_requested_date = datetime.datetime.strptime(
                    rd.hget('last_requested_times', channel_name), '%d/%b/%Y:%H:%M:%S')  # %b : abbreviated month

                if not last_requested_date:
                    logger.info(f'[{channel_name}] last_requested_date not exist')
                    stop_channel(channel_name)

                if current_date > last_requested_date + self.expiry_time_delta:
                    logger.info(
                        f'[{channel_name}] expired requested date. current_date: {current_date} / last_requested_date: {last_requested_date}')
                    stop_channel(channel_name)

            time.sleep(self.execution_interval)


if __name__ == '__main__':
    cleaner = Cleaner()
    cleaner.daemon = True  # kill this thread when main thread is killed
    cleaner.start()

    access_log_path = './logs/access.log'
    log_output_generator = LogOutputGenerator(access_log_path)
    line_id = 0

    for log_info in log_output_generator:
        requested_date = log_info['requested_date']
        channel_name = log_info['channel_name']
        logger.info(f'[{line_id}] requested_date: {requested_date} / channel_name: {channel_name}')

        # refresh last requested time
        rd.hset('last_requested_times', channel_name, requested_date)  # key: channel_name / value: last requested time

        line_id += 1
