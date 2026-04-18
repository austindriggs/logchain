import time
import yaml
import os
import alert

# Tracking cooldowns: {(container, keyword): timestamp}
last_alert_time = {}
ALERT_COOLDOWN = 30 

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
        
        # 1. Check Scoped Rules (e.g., only if 'solar' is in the name)
        active_scopes = [rules for scope, rules in scoped_rules.items() if scope in container.lower()]
        
        # 2. Check Global Rules
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
                        alert.send_ntfy(
                            rule.get('title', 'Log Alert'),
                            f"{container} | {line.strip()}",
                            priority=rule.get('priority', 3)
                        )
                        last_alert_time[tracker_key] = now

if __name__ == '__main__':
    # For standalone testing
    from . import log
    print("Log Scanner started...")
    process_logs(log.get_logs())
