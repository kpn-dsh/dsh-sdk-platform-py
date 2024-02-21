from __future__ import annotations

from pydantic import BaseModel, PositiveInt
from loguru import logger
from typing import assert_never


class Header(BaseModel):
    name: str
    protocol: str
    size: PositiveInt


class Payload(BaseModel):
    data: str


class Trailer(BaseModel):
    data: str
    checksum: PositiveInt


class Test(BaseModel):
    data: str
    checksum: int


Packet = Header | Payload | Trailer


@logger.catch(reraise=True)
def log(packet: Packet):
    # if not isinstance(packet, Packet):
    #     raise Exception("Invalid packet")
    match packet:
        case Header(protocol=protocol, size=size):
            logger.info(f"header {protocol} {size}")
            logger.info(packet.model_dump())
        case Payload(data=data):
            logger.debug(f"payload {data}")
        case Trailer(data=data, checksum=checksum):
            logger.warning(f"trailer {checksum} {data}")
        case _:
            logger.warning("")
            assert_never(packet)
