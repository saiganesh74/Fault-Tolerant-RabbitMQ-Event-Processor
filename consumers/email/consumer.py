import json
import os

import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

credentials = pika.PlainCredentials(
    RABBITMQ_USER,
    RABBITMQ_PASSWORD
)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )
)

channel = connection.channel()

channel.exchange_declare(
    exchange="events",
    exchange_type="direct",
    durable=True
)

channel.queue_declare(
    queue="email_queue",
    durable=True
)

channel.queue_bind(
    exchange="events",
    queue="email_queue",
    routing_key="email"
)

print("📩 Waiting for messages...")


def process_message(ch, method, properties, body):
    message = json.loads(body)

    print("\n📨 New Message Received")
    print(message)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue="email_queue",
    on_message_callback=process_message,
    auto_ack=False
)

channel.start_consuming()