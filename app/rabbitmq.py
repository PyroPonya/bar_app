import aio_pika
import os
import json
from typing import Any

rabbit_connection = None
rabbit_channel = None


async def init_rabbitmq():
    global rabbit_connection, rabbit_channel
    rabbit_connection = await aio_pika.connect_robust(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", 5672))
    )
    rabbit_channel = await rabbit_connection.channel()
    # объявляем очередь
    await rabbit_channel.declare_queue("order_events", durable=True)


async def publish_order_event(order_data: dict):
    if rabbit_channel is None:
        await init_rabbitmq()
    message = aio_pika.Message(body=json.dumps(order_data).encode())
    await rabbit_channel.default_exchange.publish(message, routing_key="order_events")

    # print(f"Order event published: {order_data}")
