import asyncio
import json

from rabbitmq import connect_rabbitmq, declare_exchange, declare_queue


async def consume(loader):
    connection = await connect_rabbitmq()
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=50)

        exchange = await declare_exchange(channel)
        queue = await declare_queue(channel, exchange)

        print("Ожидание сообщений...")
        async with queue.iterator() as messages:
            async for message in messages:
                async with message.process(requeue=False):
                    row = json.loads(message.body)
                    await asyncio.to_thread(loader.load_rows, [row])