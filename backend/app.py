import time
import traceback
from configparser import ConfigParser

import redis
from flask import Flask, jsonify, render_template, request, make_response
from flask_cors import CORS

from stream.streamer import Streamer
from util.logger import set_default_logger
from util.id_generate import generate_id_by_uuid

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
rd = redis.Redis(host='redis', port=6379, db=0, charset="utf-8", decode_responses=True)  # db=0 => for streamers

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
    source_url = params['sourceUrl']  # source youtube url

    # set streamer
    try:
        if not rd.exists(source_url):  # 해당 URL에 대한 Streamer가 없다면 생성
            channel_name = generate_id_by_uuid()
            logger.info(f'source_url key not exist in redis. start stream with {channel_name}')
            streamer = Streamer(source_url=source_url, dest_url=f'{dest_url}/{channel_name}',
                                youtube_api_key=youtube_api_key)
            streamer.start()
            time.sleep(20)  # index.m3u8 생기는데까지 걸리는 지연시간 부여
            rd.set(source_url, channel_name)
            streamers[channel_name] = streamer

        channel_name = str(rd.get(source_url))  # 해당 URL에 대한 채널명으로 응답
        logger.info(f'source_url: {source_url} -> channel_name: {channel_name}')

    except Exception:
        logger.error('Error start stream from server.')
        traceback.print_exc()
        return make_response('Error start stream from server.', 500)
    return make_response(jsonify({
        'msg': 'Success start stream.',
        'channelName': channel_name
    }), 200)


# 사용자한테 노출되면 안되는 Endpoint (사용자가 직접 채널 이름을 통해 stream을 종료해선 안됨.)
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
