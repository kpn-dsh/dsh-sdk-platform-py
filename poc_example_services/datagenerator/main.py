import json
import random
import datetime
import time
import secrets
import os
import sys
import signal

import dsh.dsh_kafka as kafka


def main():
    producer_config = kafka.create_dsh_config()
    PRODUCE_TOPIC = os.environ["PRODUCE_TOPIC"]
    SLEEP_INTERVAL = os.environ["SLEEP_INTERVAL"]

    producer = kafka.create_producer(producer_config)

    signal.signal(signal.SIGTERM, handle_sigterm)

    run = True
    while run:
        data = generate_json_with_bounds()
        kafka.produce_message(producer, data, PRODUCE_TOPIC)
        print(data, "\n")
        time.sleep(float(SLEEP_INTERVAL))


def handle_sigterm(signum, frame):
    print("Receiving sigterm")
    sys.exit(1)


# Define global bounds for values


latitude_bounds = (52090196, 52099196)
longitude_bounds = (4301346, 4305346)
speed_bounds = (50, 70)
heading_bounds = (80, 100)
ambient_air_temperature_bounds = (20.0, 25.0)
session_id = secrets.token_hex(16)


def generate_json_with_bounds():
    # Generate random values within bounds
    latitude = int(random.uniform(*latitude_bounds))
    longitude = int(random.uniform(*longitude_bounds))
    speed = random.uniform(*speed_bounds)
    heading = random.uniform(*heading_bounds)
    ambient_air_temperature = random.uniform(*ambient_air_temperature_bounds)

    # Create a timestamp with the current date and time
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    # Generate the JSON
    data = {
        "session_id": session_id,
        "timestamp": timestamp,
        "data": {
            "latitude": latitude,
            "longitude": longitude,
            "speed": speed,
            "heading": heading,
            "country": "United States",
            "date": datetime.date.today().isoformat(),
            "hour": datetime.datetime.now().hour,
            "ambient_air_temperature": ambient_air_temperature,
            "fog_lights_on": random.choice([True, False]),
            "wiper_state": random.randint(0, 3),
        },
    }

    return json.dumps(data, indent=2)


#
#
# Start
if __name__ == "__main__":
    main()
