from __future__ import annotations

from dataclasses import dataclass
from loguru import logger


@dataclass
class Header:
    protocol: str
    size: int


@dataclass
class Payload:
    data: str


@dataclass
class Trailer:
    data: str
    checksum: int


Packet = Header | Payload | Trailer


def match(packet: Packet):
    if not isinstance(packet, Packet):
        raise Exception("Invalid packet")

    match packet:
        case Header(protocol, size):
            logger.info(f"header {protocol} {size}")
        case Payload(data):
            logger.debug("payload {data}")
        case Trailer(data, checksum):
            logger.info(f"trailer {checksum} {data}")
