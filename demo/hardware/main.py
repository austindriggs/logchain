# main.py (MicroPython on Pico)

import time
import random

def get_voltage():
    return round(random.uniform(18.0, 24.0), 2)

def get_current():
    return round(random.uniform(0.5, 5.0), 2)

def get_power(v, i):
    return round(v * i, 2)

while True:
    voltage = get_voltage()
    current = get_current()
    power = get_power(voltage, current)

    print(f"{time.time()} SOLAR voltage={voltage}V current={current}A power={power}W")

    time.sleep(2)