import time
import traceback
from configparser import ConfigParser

import redis
from flask import Flask, jsonify, render_template, request, make_response
from flask_cors import CORS

from stream.streamer import Streamer
from util.logger import set_default_logger

# init logger
logger = set_default_logger('main_logger')

# init config
parser = ConfigParser()
parser.read('config.ini')
youtube_api_key = parser.get('settings', 'youtube_api_key')

# init flask app
app = Flask(__name__)
CORS(app)

# init redis
rd = redis.Redis(host='redis', port=6379, db=0)

# set default params
dest_url = "rtmp://media_server/live"  # rtmp + application name
streamers = {}


@app.route('/', methods=['GET'])
def root():
    return render_template('video_show.html')


@app.route('/stream/start', methods=['POST'])
def start_stream():
    # get_params
    params = request.get_json()
    logger.info(f'params: {params}')
    channel_name = params['channelName']  # HLS connection name
    source_url = params['sourceUrl']  # source youtube url

    # set streamer
    try:
        streamer = Streamer(source_url=source_url, dest_url=f'{dest_url}/{channel_name}',
                            youtube_api_key=youtube_api_key)
        streamer.start()
        time.sleep(20)  # index.m3u8 생기는데까지 걸리는 지연시간 부여
        streamers[channel_name] = streamer

        # rd.hset('streamers', source_url, channel_name)

    except Exception:
        logger.error('Error start stream from server.')
        traceback.print_exc()
        return make_response('Error start stream from server.', 500)
    return make_response('Success start stream.', 200)


@app.route('/stream/stop', methods=['POST'])
def stop_stream():
    # get_params
    params = request.get_json()
    channel_name = params['channelName']
    logger.info(f'params: {params}')

    # stop streamer
    try:
        streamer = streamers[channel_name]
        streamer.stop_video_stream()
        streamer.join()
        streamers.pop(channel_name)
    except Exception:
        return make_response("Error stop stream", 500)
    return make_response("Success stop stream", 200)


@app.route('/streamers', methods=['GET'])
def get_streamers():
    streamer_names = list(streamers.keys())
    logger.info(f'streamer_names: {streamer_names}')
    res = {'streamers': streamer_names}
    return make_response(jsonify(res), 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989, threaded=True)
