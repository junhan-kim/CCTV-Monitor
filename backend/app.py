from flask import Flask, render_template
from util.logger import set_default_logger


logger = set_default_logger('main_logger')


app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return render_template('video_show.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8989)
