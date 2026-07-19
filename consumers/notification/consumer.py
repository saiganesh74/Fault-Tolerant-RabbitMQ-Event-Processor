import json
import os
import time

import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")


def connect():
    credentials = pika.PlainCredentials(
        RABBITMQ_USER,
        RABBITMQ_PASSWORD
    )

    while True:
        try:
            print("🔔 Connecting to RabbitMQ...", flush=True)

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
                queue="notification_queue",
                durable=True
            )

            channel.queue_bind(
                exchange="events",
                queue="notification_queue",
                routing_key="notification"
            )

            print("✅ Notification Consumer Connected", flush=True)

            return connection, channel

        except pika.exceptions.AMQPConnectionError:
            print("❌ RabbitMQ unavailable. Retrying...", flush=True)
            time.sleep(5)


connection, channel = connect()


def process_message(ch, method, properties, body):
    message = json.loads(body)

    print("\n🔔 Notification Service", flush=True)
    print(message, flush=True)

    print(
        f"📱 Push notification sent to {message['customer']}",
        flush=True
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue="notification_queue",
    on_message_callback=process_message,
    auto_ack=False
)

print("🔔 Waiting for notifications...", flush=True)

channel.start_consuming()