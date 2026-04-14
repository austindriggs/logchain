# This is the main app file for Flask to serve everything.

##############################################################################
# IMPORT MODULES AND LOAD ENV VARIABLES
##############################################################################

import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, jsonify
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap5
import secrets

# load from .env file
load_dotenv()

# import local modules
import log, alert, chain

##############################################################################
# INITIALIZE FLASK APP
##############################################################################

app = Flask(__name__)

app.secret_key = secrets.token_urlsafe(16)
csrf = CSRFProtect(app)
bootstrap = Bootstrap5(app)

##############################################################################
# ROUTES
##############################################################################

@app.route('/')
def index_page():
    # ✅ KEEP your existing layout
    # but REMOVE passing raw logs
    return render_template('index.html')


@app.route('/about/')
def about_page():
    return render_template('about.html')

@app.before_request
def ensure_chain():
    import chain
    if len(chain.get_chain()) == 0:
        chain.add_block()


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

    return render_template(
        'alert.html',
        ntfy_address=alert.get_ntfy(),
        manual_alert_form=manual_alert_form
    )
@app.route('/test-alert/')
def test_alert():
    import alert
    alert.send_ntfy("TEST ALERT", "This is working", priority=5)
    return "sent"

##############################################################################
# API ROUTES (CHAIN DATA)
##############################################################################

@app.route('/api/chain/')
def api_chain():
    return jsonify(chain.get_chain())


@app.route('/api/block/<block_hash>/')
def api_block(block_hash):
    for block in chain.get_chain():
        if block["block_hash"] == block_hash:
            return jsonify(block)
    return jsonify({"error": "Block not found"}), 404

##############################################################################
# RUN APP
##############################################################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)