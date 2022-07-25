from flask import Flask, render_template, request, Response, jsonify
from configparser import ConfigParser
import time

from util.logger import set_default_logger
from util.watchdog import Watchdog
from stream.streamer import Streamer


# init logger
logger = set_default_logger('main_logger')

# init config
parser = ConfigParser()
parser.read('../config.ini')
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
    channel_name = params['channel_name']  # HLS connection name
    youtube_url = params['youtube_url']  # source youtube url

    # set streamer
    watchdog = Watchdog(30)
    try:
        streamer = Streamer(api_key=api_key)
        streamers[channel_name] = streamer
        streamer.start(youtube_url, f'{dest_url}/{channel_name}')

        # check start stream
        while True:
            if streamer.check_start_stream():
                break
    except Watchdog:
        return Response("Error start stream (timeout)", status_code=500)
    except Exception:
        return Response("Error start stream", status_code=500)
    finally:
        watchdog.stop()
    return Response("Success start stream", status_code=200)


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
        return Response("Error stop stream", status_code=500)
    return Response("Success stop stream", status_code=200)


@app.route('/streams', methods=['GET'])
def get_streams():
    return Response(jsonify([name for name in streamers.keys()]), status_code=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)
