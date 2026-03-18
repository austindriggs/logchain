import docker
import sys


def remove_excluded_containers(containers):
    # eventually this will get yaml stuff and then remove things
    containers = [c for c in containers if c.name != 'logchain_web']
    return containers


def get_logs():
    all_containers = docker.from_env().containers.list(all=True)
    containers = remove_excluded_containers(all_containers)

    all_logs = {}
    for container in containers:
        print(f"Getting logs for {container.name} ({container.id})")
        try:
            all_logs[container.name] = container.logs().decode('utf-8')
        except Exception as e:
            print(f"Error getting logs for {container.name}: {e}")
        
    return all_logs
