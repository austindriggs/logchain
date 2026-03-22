import requests
import os
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired


NTFY_URL, NTFY_TOPIC = None, None


class ManualAlert(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    priority = IntegerField('Priority', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    submit = SubmitField('Submit')


# get env variables
def start_ntfy():
    global NTFY_URL, NTFY_TOPIC

    try:
        load_dotenv()
        NTFY_URL = os.getenv("NTFY_URL")
        NTFY_TOPIC = os.getenv("NTFY_TOPIC")
    except Exception as e:
        print(f"Error starting ntfy: {e}")
    
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


# verify ntfy url and topic
def get_ntfy():
    return f"{NTFY_URL}/{NTFY_TOPIC}"


# basic function to send a notification through ntfy
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
