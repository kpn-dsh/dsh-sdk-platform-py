from confluent_kafka import Producer, Consumer
import signal
import sys

# Configuration
CONFIG = {
    "PKI_KEY": "../certs/cert.key",
    "PKI_CERT": "../certs/cert.crt",
    "PKI_CACERT": "../certs/ca.crt",
    "TENANT": "training",
    "TOPIC": "scratch.arar.training",
    "BROKER_NAME": "broker",
    "CLIENT_ID": "ns-client",
    "GROUP_ID": "training_broker_6",
    "BROKERS": [
        "broker-0.kafka.training.poc.kpn-dsh.com:9091",
        "broker-1.kafka.training.poc.kpn-dsh.com:9091",
        "broker-2.kafka.training.poc.kpn-dsh.com:9091",
    ],
}


# Main function
def main():
    signal.signal(signal.SIGTERM, handle_sigterm)
    consumer = create_consumer()
    producer = create_producer()
    try:
        produce_message(producer, CONFIG["TOPIC"])
        consume_messages(consumer, CONFIG["TOPIC"])
    except KeyboardInterrupt:
        print("KeyboardInterrupt, exiting...")
        sys.exit(0)
    finally:
        consumer.close()
        producer.close()


# Kafka configuration
def get_kafka_config(consumer=False):
    config = {
        "bootstrap.servers": ",".join(CONFIG["BROKERS"]),
        "client.id": CONFIG["CLIENT_ID"],
        "security.protocol": "ssl",
        "ssl.key.location": CONFIG["PKI_KEY"],
        "ssl.certificate.location": CONFIG["PKI_CERT"],
        "ssl.ca.location": CONFIG["PKI_CACERT"],
    }
    if consumer:
        config["group.id"] = CONFIG["GROUP_ID"]
    return config


# Create Kafka consumer
def create_consumer():
    return Consumer(get_kafka_config(consumer=True))


# Create Kafka producer
def create_producer():
    return Producer(get_kafka_config(consumer=False))


# Produce a message
def produce_message(producer, topic):
    producer.produce(topic=topic, value="{ key: py: hello, world!}")
    producer.flush()


# Consume messages
def consume_messages(consumer, topic):
    consumer.subscribe([topic])
    while True:
        msg = consumer.poll(1.0)
        if msg is not None:
            print("Received message:", msg.value().decode("utf-8"))


# Signal handler
def handle_sigterm(signum, frame):
    print("Received SIGTERM, exiting...")
    sys.exit(1)


if __name__ == "__main__":
    main()
