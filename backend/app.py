from flask import Flask, render_template, request, Response, jsonify
from configparser import ConfigParser
import time
import traceback
from threading import Event

from util.logger import set_default_logger
from util.watchdog import Watchdog
from stream.streamer import Streamer


# init logger
logger = set_default_logger('main_logger')

# init config
parser = ConfigParser()
parser.read('config.ini')
api_key = parser.get('settings', 'api_key')

# init flask app
app = Flask(__name__)

# set default params
dest_url = "rtmp://localhost/live"  # rtmp + application name

# streamers
streamers = {}


@app.route('/', methods=['GET'])
def root():
    return render_template('video_show.html')


@app.route('/stream/start', methods=['POST'])
def start_stream():
    # get_params
    params = request.get_json()
    logger.info(f'params: {params}')
    channel_name = params['channel_name']  # HLS connection name
    youtube_url = params['youtube_url']  # source youtube url

    # set streamer
    watchdog = Watchdog(10)
    try:
        streamer = Streamer(api_key=api_key, source_url=youtube_url, dest_url=f'{dest_url}/{channel_name}')
        streamers[channel_name] = streamer
        streamer.start()

        # check start stream
        timeout_event = Event()
        while not timeout_event.is_set():
            logger.info('check start stream.')
            if streamer.check_start_stream():
                logger.info('Success start stream.')
                break
            time.sleep(1)
    except Watchdog:
        logger.error('TimeoutError')
        traceback.print_exc()
        timeout_event.is_set()
        return Response("Error start stream with timeout.", status=408)
    except Exception:
        logger.error('Exception')
        traceback.print_exc()
        timeout_event.is_set()
        return Response("Error start stream.", status=500)
    finally:
        watchdog.stop()
    return Response("Success start stream.", status=200)


@app.route('/stream/stop', methods=['POST'])
def stop_stream():
    # get_params
    params = request.get_json()
    channel_name = params['channel_name']

    # stop streamer
    try:
        streamer = streamers[channel_name]
        streamer.stop_video_stream()
        streamer.join()
    except Exception:
        return Response("Error stop stream", status=500)
    return Response("Success stop stream", status=200)


@app.route('/streams', methods=['GET'])
def get_streams():
    return Response(jsonify([name for name in streamers.keys()]), status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)
