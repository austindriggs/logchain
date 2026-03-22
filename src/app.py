# This is the main app file for Flask to serve everything.
# It handles page routing, loaading env variables, form validation, and other basic functions.
# See https://flask.palletsprojects.com/en/stable/quickstart/ for some useful information.


##############################################################################
# IMPORT MODULES AND LOAD ENV VARIABLES
##############################################################################

# imported libraries
import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm, CSRFProtect
from flask_bootstrap import Bootstrap5
import secrets

# load from .env file
load_dotenv()

# import local modules
import log, alert


##############################################################################
# INITIALIZE FLASK APP AND HANDLE FORM SECRET KEY
##############################################################################

app = Flask(__name__)


foo = secrets.token_urlsafe(16)
app.secret_key = foo
csrf = CSRFProtect(app)
bootstrap = Bootstrap5(app)


##############################################################################
# FLASK APP ROUTING AND PAGE HANDLING
##############################################################################

@app.route('/about/')
def about_page():
    return render_template('about.html')


@app.route('/alert/', methods=['GET', 'POST'])
def alert_page():
    manual_alert_form = alert.ManualAlert()
    if manual_alert_form.validate_on_submit():
        title = manual_alert_form.title.data
        message = manual_alert_form.message.data
        priority = manual_alert_form.priority.data
        author = manual_alert_form.author.data

        full_message = f"{message}\n\nAuthor: {author}"
        alert.send_ntfy(title, full_message, priority)

        return redirect(url_for('alert_page'))

    return render_template('alert.html', ntfy_address=alert.get_ntfy(), manual_alert_form=manual_alert_form)


@app.route('/')
def index_page():
    container_logs = log.get_logs()
    return render_template('index.html', logs=container_logs)


if __name__ == '__main__':
    # 0.0.0.0 allows the app to be accessible from outside the container
    # Port 5000 is the default Flask port, but it can be changed if needed (especially in the docker-compose.yml)
    # debug=True enables auto-reloading and better error messages during development, NOT production
    app.run(host='0.0.0.0', port=5000, debug=True)
