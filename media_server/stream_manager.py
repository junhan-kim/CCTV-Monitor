import subprocess
import re
import datetime
import traceback


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

            requested_date_str = match.group(1)
            # convert date string to date object
            requested_date = datetime.datetime.strptime(
                requested_date_str, '%d/%b/%Y:%H:%M:%S')  # %b : abbreviated month

            channel_name = match.group(2)

            yield {
                'requested_date': requested_date,
                'channel_name': channel_name
            }
    except Exception:
        traceback.print_exc()
        raise StopIteration
    finally:
        proc.terminate()


# params
access_log_path = './logs/access.log'
#####

log_output_generator = LogOutputGenerator(access_log_path)
line_id = 0
last_requested_times = {}  # key: channel_name / value: last requested time

for log_info in log_output_generator:
    requested_date = log_info['requested_date']
    channel_name = log_info['channel_name']
    print(f'[{line_id}] requested_date: {requested_date} / channel_name: {channel_name}')

    # refresh last requested time
    last_requested_times[channel_name] = requested_date
    print(last_requested_times)

    # get

    line_id += 1
