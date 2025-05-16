import json
import os
from confluent_kafka import Consumer, Producer
from dataclasses import dataclass, fields
from typing import Optional
from loguru import logger


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
            "queue.buffering.max.messages": 0,
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
