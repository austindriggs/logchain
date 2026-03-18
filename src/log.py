import docker
from apscheduler.schedulers.background import BackgroundScheduler
import sys


captured_logs = {}


def remove_excluded_containers(containers):
    # eventually this will get yaml stuff and then remove things
    containers = [c for c in containers if c.name != 'logchain_web']
    return containers


def get_logs():
    global captured_logs
    try:
        all_containers = docker.from_env().containers.list(all=True)
        containers = remove_excluded_containers(all_containers)

        new_logs = {}
        for container in containers:
            print(f"Getting logs for {container.name} ({container.id})")
            
            try:
                new_logs[container.name] = container.logs().decode('utf-8')
            except Exception as e:
                print(f"Error getting logs for {container.name}: {e}")

        captured_logs = new_logs
    
    except Exception as e:
        print(f"Error in background log capture: {e}")
            
    return captured_logs


# this runs as soon as 'import log' happens in app.py
scheduler = BackgroundScheduler()
scheduler.add_job(func=get_logs, trigger="interval", minutes=1)
scheduler.start()
get_logs()
