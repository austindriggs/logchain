# handles communication with the ntfy servrer and allows for manual notifications
# See https://ntfy.sh/ for more information on ntfy and how to set it up.



##############################################################################
# IMPORT ALL LIBRARIES AND MODULES
##############################################################################

import os, requests, time
import yaml
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired



##############################################################################
# SETUP ENV VARIABLES AND FORM CLASS
##############################################################################

NTFY_URL = os.getenv("NTFY_URL", None)
NTFY_TOPIC = os.getenv("NTFY_TOPIC", None)


last_alert_time = {}
ALERT_COOLDOWN = 30 


class ManualAlert(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    priority = IntegerField('Priority', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    submit = SubmitField('Submit')



##############################################################################
# ALERT FUNCTIONS
##############################################################################

def start_ntfy():
    global NTFY_URL, NTFY_TOPIC

    if NTFY_URL is None or NTFY_TOPIC is None:
        print("Error: NTFY_URL and NTFY_TOPIC must be set in environment variables.")
        exit(1)

    try:
        print(f"Starting ntfy at: {NTFY_URL}/{NTFY_TOPIC}")
        send_ntfy("LogChain Alert System Started", 
                    "The LogChain alert system has been initialized and is ready to send notifications.", 
                    priority=3)
    except Exception as e:
        print(f"Error connecting to ntfy: {e}")


def get_ntfy():
    return f"{NTFY_URL}/{NTFY_TOPIC}"


def send_ntfy(title, message, priority, tags=None, click=None, delay=None):
    headers = {
        "Title": title,
        "Priority": str(priority),
    }

    if tags: headers["Tags"] = tags
    if click: headers["Click"] = click
    if delay: headers["Delay"] = delay

    requests.post(
        f"{NTFY_URL}/{NTFY_TOPIC}",
        data=message.encode("utf-8"),
        headers=headers
    )


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '../config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def process_logs(new_logs):
    global last_alert_time
    now = time.time()
    config = load_config()
    
    global_rules = config.get('global_rules', [])
    scoped_rules = config.get('scoped_rules', {})

    for container, logs in new_logs.items():
        if not logs:
            continue
        
        lines = logs.splitlines()
        
        active_scopes = [rules for scope, rules in scoped_rules.items() if scope in container.lower()]
        
        rules_to_check = global_rules
        for scope_list in active_scopes:
            rules_to_check.extend(scope_list)

        for line in lines:
            for rule in rules_to_check:
                keyword = rule['keyword']
                
                if keyword in line:
                    tracker_key = (container, keyword)
                    last_ts = last_alert_time.get(tracker_key, 0)
                    
                    if now - last_ts > ALERT_COOLDOWN:
                        send_ntfy(
                            rule.get('title', 'Log Alert'),
                            f"{container} | {line.strip()}",
                            priority=rule.get('priority', 3)
                        )
                        last_alert_time[tracker_key] = now
