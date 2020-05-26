import flask

app = flask.Blueprint('common', __name__)


@app.route('/err', methods=['GET'])
def err():
    raise Exception("error", 505)


@app.route('/', methods=['GET'])
def index():
    return "hi"
    # return flask.render_template('index.html')
