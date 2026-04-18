import time
import random
import math
from datetime import datetime

def solar_curve(t):
    # simulate sunlight curve (sin wave)
    return max(0, math.sin(t))

t = 0

while True:
    # simulate daylight cycle
    sun = solar_curve(t)

    voltage = round(18 + sun * 6 + random.uniform(-0.5, 0.5), 2)
    current = round(sun * 5 + random.uniform(-0.2, 0.2), 2)
    power = round(voltage * current, 2)

    # simulate faults
    status = "OK"
    if random.random() < 0.05:
        status = "LOW_VOLTAGE"
        voltage -= 5
    elif random.random() < 0.05:
        status = "OVERCURRENT"
        current += 3

    timestamp = datetime.utcnow().isoformat()

    print(f"{timestamp} SOLAR voltage={voltage}V current={current}A power={power}W status={status}", flush=True)

    t += 0.1
    time.sleep(5)