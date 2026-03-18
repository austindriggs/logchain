# https://flask.palletsprojects.com/en/stable/quickstart/

from flask import Flask, render_template
import log

app = Flask(__name__)

@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/alert/')
def alert():
    return render_template('alert.html')


@app.route('/')
def index():
    container_logs = log.get_logs()
    return render_template('index.html', logs=container_logs)


if __name__ == '__main__':
    # 0.0.0.0 allows the app to be accessible from outside the container
    # Port 5000 is the default Flask port, but it can be changed if needed
    # debug=True enables auto-reloading and better error messages during development, NOT production
    app.run(host='0.0.0.0', port=5000, debug=True)