import time
import random
import math
from datetime import datetime

conditions = [
    ("SUNNY", 5, 15),
    ("PARTLY_CLOUDY", 20, 50),
    ("CLOUDY", 60, 90),
    ("OVERCAST", 90, 100)
]

t = 0  # time variable for day/night cycle

def daylight_factor(t):
    # sin wave: 0 (night) → 1 (peak sun)
    return max(0, math.sin(t))

while True:
    # simulate sun position
    sun = daylight_factor(t)

    # determine day/night
    is_day = sun > 0.05
    time_of_day = "DAY" if is_day else "NIGHT"

    # pick cloud condition
    condition, min_cloud, max_cloud = random.choice(conditions)
    cloud_cover = random.randint(min_cloud, max_cloud)

    # expected solar yield calculation
    if not is_day:
        expected_yield = 0
    else:
        # base yield from sun intensity
        base = sun * 100

        # reduce based on clouds
        cloud_factor = (100 - cloud_cover) / 100

        expected_yield = int(base * cloud_factor * random.uniform(0.9, 1.1))

    timestamp = datetime.utcnow().isoformat()

    print(
        f"{timestamp} CLOUD time={time_of_day} condition={condition} "
        f"cloud_cover={cloud_cover}% expected_yield={expected_yield}%",
        flush=True
    )

    t += 0.1
    time.sleep(3)