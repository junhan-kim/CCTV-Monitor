from flask import Flask, render_template


app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    render_template('./template/video_show.html')


if __name__ == '__main__':
    app.run(port=8989)
