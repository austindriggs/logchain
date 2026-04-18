# captures docker logs, filters them, and returns them as called
# right now, this is scheduled for SCAN_INTERVAL_MINUTES or every 10 minutes



##############################################################################
# IMPORT MODULES AND SETUP DICTIONARY
##############################################################################

import sys, os
import datetime
import docker
from apscheduler.schedulers.background import BackgroundScheduler

import detect

captured_logs = {}
SCAN_INTERVAL_MINUTES = os.getenv("SCAN_INTERVAL_MINUTES", 1)



##############################################################################
# LOG FUNCTIONS AND SCHEDULER
##############################################################################

def remove_excluded_containers(containers):
    # eventually this will get configured from the yaml file
    containers = [c for c in containers if c.name != 'logchain']
    return containers


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
                new_logs[container.name] = container.logs().decode('utf-8')
            except Exception as e:
                print(f"Error getting logs for {container.name}: {e}")

        captured_logs = new_logs
    
    except Exception as e:
        captured_logs = {}
        print(f"Error in background log capture: {e}")

    detect.check_solar_alerts(captured_logs)
    
    return captured_logs



# this runs as soon as 'import log' happens in app.py
def scheduled_job():
    get_logs()

    import chain  # runtime import avoids circular import
    chain.add_block()

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=scheduled_job,
    trigger="interval",
    minutes=SCAN_INTERVAL_MINUTES
)
scheduler.start()
