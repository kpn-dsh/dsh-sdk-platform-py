import os
import sys
import signal

import dsh.kafka.dsh_kafka as kafka


def main():
    consumer_config = kafka.create_dsh_config()
    CONSUME_TOPIC = os.environ["CONSUME_TOPIC"]

    consumer = kafka.create_consumer(consumer_config)
    consumer.subscribe([CONSUME_TOPIC])

    signal.signal(signal.SIGTERM, handle_sigterm)

    while True:
        msg = consumer.poll(1.0)  # start consuming

        if msg is not None:
            print(msg.value())

        # try:
        #     obj = json.loads(msg.value().decode("utf-8"))
        # except Exception as e:
        #     logging.error("Error decoding message: %s", e)
        #     continue


def handle_sigterm(signum, frame):
    print("Receiving sigterm")
    sys.exit(1)


# Start
if __name__ == "__main__":
    main()
