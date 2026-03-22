import docker
from apscheduler.schedulers.background import BackgroundScheduler

import sys
import datetime


captured_logs = {}


# eventually this will get configured from the yaml file
def remove_excluded_containers(containers):
    containers = [c for c in containers if c.name != 'logchain']
    return containers


# get logs for the last minute and return them in a dict of {container_name: logs}
def get_logs():
    global captured_logs
    try:
        all_containers = docker.from_env().containers.list(all=True)
        containers = remove_excluded_containers(all_containers)
        one_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=1)

        new_logs = {}
        for container in containers:
            print(f"Getting logs for {container.name} ({container.id})")
            try:
                new_logs[container.name] = container.logs(since=one_minute_ago).decode('utf-8')
            except Exception as e:
                print(f"Error getting logs for {container.name}: {e}")

        captured_logs = new_logs
    
    except Exception as e:
        captured_logs = {}
        print(f"Error in background log capture: {e}")
            
    return captured_logs


# this runs as soon as 'import log' happens in app.py
scheduler = BackgroundScheduler()
scheduler.add_job(func=get_logs, trigger="interval", minutes=10)
scheduler.start()
get_logs()
