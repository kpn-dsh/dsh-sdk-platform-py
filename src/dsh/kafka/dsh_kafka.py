import json
import os
from confluent_kafka import Consumer, Producer
from dataclasses import dataclass, fields
from typing import Optional
import logging
import sys
import time

# Set up logging
logger = logging.getLogger("kafka_feed")
loglevel = "DEBUG"
logger.setLevel(loglevel)
logger.addHandler(logging.StreamHandler(sys.stdout))


@dataclass
class Config:
    """
    If tenant_config is set, it will be used to set the servers and group_id.
    otherwise, servers and group_id must be set.
    """

    # tenant_name: str
    # topic: Optional[str] = None
    pki_cacert: str
    pki_key: str
    pki_cert: str
    client_id: str
    group_id: Optional[str] = None
    servers: Optional[str] = None
    tenant_config: Optional[str] = None

    # if tenant_config is set, use it to set servers and group_id
    def __post_init__(self):
        if self.tenant_config:
            json_config = json.loads(self.tenant_config)
            self.servers = ",".join(json_config["brokers"])
            self.group_id = json_config["shared_consumer_groups"][-1]

        if not self.tenant_config and not (self.servers and self.group_id):
            return ValueError(
                "Either tenant_config or servers and group_id must be set"
            )


def create_dsh_config() -> Config:
    dshconfig = Config(
        pki_cacert=os.environ["DSH_PKI_CACERT"],
        pki_key=os.environ["DSH_PKI_KEY"],
        pki_cert=os.environ["DSH_PKI_CERT"],
        client_id=os.environ["MESOS_TASK_ID"],
        tenant_config=os.environ["JSON_TENANT_CONFIG"],
    )
    return dshconfig


def create_producer(config: Config) -> Producer:
    return Producer(
        {
            "bootstrap.servers": config.servers,
            "group.id": config.group_id,
            "client.id": config.client_id,
            "security.protocol": "ssl",
            "ssl.key.location": config.pki_key,
            "ssl.certificate.location": config.pki_cert,
            "ssl.ca.location": config.pki_cacert,
        }
    )


def create_consumer(config: Config) -> Consumer:
    return Consumer(
        {
            "bootstrap.servers": config.servers,
            "group.id": config.group_id,
            "client.id": config.client_id,
            "security.protocol": "ssl",
            "ssl.key.location": config.pki_key,
            "ssl.certificate.location": config.pki_cert,
            "ssl.ca.location": config.pki_cacert,
            "auto.offset.reset": "latest",
        }
    )


def _delivery_report(err, msg):
    """Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush()."""
    if err is not None:
        logger.warning(f"Message delivery failed: {err} \n \n")
    else:
        logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}] \n \n")


# def produce_message(producer: Producer, obj, topic) -> None:
#     print("producing message...")
#     try:
#         # producer.poll(0)
#         producer.produce(topic=topic, value=obj, callback=_delivery_report)
#         # producer.flush()
#         print(f"Message produced: {obj} \n")
#
#     except Exception as e:
#         print(f"exception raised: {e}")


def produce_message(producer: Producer, obj, topic) -> None:
    retries = 3  # Number of retries before giving up
    retry_delay = 1  # Initial retry delay in seconds

    while retries > 0:
        try:
            producer.produce(topic=topic, value=obj, callback=_delivery_report)
            producer.poll(0)  # Poll to handle delivery reports
            print(f"Message produced: {obj} \n")
            return  # Message sent successfully

        except Exception as e:
            print(f"Exception raised: {e}")
            retries -= 1
            if retries > 0:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 1  # Exponential backoff

    print("Failed to send the message after retries.")


def consume_topic(consumer: Consumer, topic: str):
    """
    Example:
        kafka_consumer = create_consumer(kafka_config)

        for message in consume_topic(kafka_consumer, "your_topic"):
            # Your custom logic to handle the consumed message
            print(f"Received message: {message}")
            # Add your own while loop or other conditions to control the message consumption behavior.
    """
    consumer.subscribe([topic])

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            logger.error(f"Consumer error: {msg.error()}")
            continue

        value = msg.value()
        if value is not None:
            yield value
