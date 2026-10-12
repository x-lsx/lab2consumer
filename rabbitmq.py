import configparser
import os
import ssl

import aio_pika
from aio_pika import ExchangeType
from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractQueue

EXCHANGE_NAME = "sqldata"
QUEUE_NAME = "postgres_loader_sqldata"


def _cfg():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "config.ini"))
    return config["rabbitmq"]


async def connect_rabbitmq():
    cfg = _cfg()
    ctx = ssl.create_default_context(cafile=cfg["cafile"])
    return await aio_pika.connect_robust(
        host=cfg["host"],
        port=int(cfg["port"]),
        login=cfg["user"],
        password=cfg["password"],
        ssl=True,
        ssl_context=ctx,
    )


async def declare_exchange(channel: AbstractChannel) -> AbstractExchange:
    return await channel.declare_exchange(
        EXCHANGE_NAME, ExchangeType.FANOUT, durable=True
    )


async def declare_queue(channel: AbstractChannel, exchange: AbstractExchange) -> AbstractQueue:
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.bind(exchange)
    return queue



# import aio_pika
# from aio_pika import ExchangeType
# from aio_pika.abc import AbstractChannel, AbstractExchange, AbstractQueue

# EXCHANGE_NAME = "sqldata"  
# QUEUE_NAME = "postgres_loader_sqldata" 


# async def connect_rabbitmq():
#     return await aio_pika.connect_robust("amqp://guest:guest@localhost:5672/")


# async def declare_exchange(channel: AbstractChannel) -> AbstractExchange:
#     return await channel.declare_exchange(
#         name=EXCHANGE_NAME,
#         type=ExchangeType.FANOUT,
#         durable=True,
#     )


# async def declare_queue(
#     channel: AbstractChannel,
#     exchange: AbstractExchange,
# ) -> AbstractQueue:
#     queue = await channel.declare_queue(name=QUEUE_NAME, durable=True)
#     await queue.bind(exchange)
#     return queue