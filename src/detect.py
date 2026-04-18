# handles detection of solar-related faults and sends alerts

import time
import os
import alert, log

# Nested dictionary to track cooldowns per container
# Structure: {"container_name": {"overcurrent": timestamp, "low_voltage": timestamp}}
last_alert_time = {}

ALERT_COOLDOWN = 30  # seconds


def check_solar_alerts(new_logs):
    """
    Scans logs for solar-specific faults and triggers alerts via ntfy.
    """
    global last_alert_time
    now = time.time()

    if not isinstance(new_logs, dict):
        print(f"Error: expected dict for logs, got {type(new_logs)}")
        return

    for container, logs in new_logs.items():
        if not logs:
            continue

        if "solar" not in container.lower():
            continue

        if container not in last_alert_time:
            last_alert_time[container] = {
                "overcurrent": 0,
                "low_voltage": 0
            }

        lines = logs.splitlines()

        for line in lines:
            # OVERCURRENT DETECTION
            if "OVERCURRENT" in line:
                time_since = now - last_alert_time[container]["overcurrent"]
                if time_since > ALERT_COOLDOWN:
                    alert.send_ntfy(
                        "Solar Overcurrent",
                        f"{container} | {line.strip()}",
                        priority=5
                    )
                    last_alert_time[container]["overcurrent"] = now

            # LOW VOLTAGE DETECTION
            if "LOW_VOLTAGE" in line:
                time_since = now - last_alert_time[container]["low_voltage"]
                if time_since > ALERT_COOLDOWN:
                    alert.send_ntfy(
                        "Solar Low Voltage",
                        f"{container} | {line.strip()}",
                        priority=4 
                    )
                    last_alert_time[container]["low_voltage"] = now


if __name__ == '__main__':
    print("Solar Alert Producer started")
    
    try:
        # Function call retrieves log dictionary
        current_logs = log.get_logs()
        check_solar_alerts(current_logs)
    except Exception as e:
        print(f"Simulation Error: {e}")
