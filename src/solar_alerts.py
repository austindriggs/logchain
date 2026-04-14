# solar_alerts.py
# handles detection of solar-related faults and sends alerts

import time
import alert

# simple debounce to prevent alert spam
last_alert_time = {
    "overcurrent": 0,
    "low_voltage": 0
}

ALERT_COOLDOWN = 30  # seconds


def check_solar_alerts(new_logs):
    global last_alert_time

    now = time.time()

    for container, logs in new_logs.items():
        if not logs:
            continue

        # only monitor solar containers
        if "solar" not in container.lower():
            continue

        # split logs into individual lines
        lines = logs.splitlines()

        for line in lines:

            # OVERCURRENT detection
            if "OVERCURRENT" in line:
                if now - last_alert_time["overcurrent"] > ALERT_COOLDOWN:
                    alert.send_ntfy(
                        "Solar Overcurrent",
                        f"{container} | {line}",
                        priority=5
                    )
                    last_alert_time["overcurrent"] = now

            # LOW VOLTAGE detection
            if "LOW_VOLTAGE" in line:
                if now - last_alert_time["low_voltage"] > ALERT_COOLDOWN:
                    alert.send_ntfy(
                        "Solar Low Voltage",
                        f"{container} | {line}",
                        priority=5
                    )
                    last_alert_time["low_voltage"] = now