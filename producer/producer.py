import json
import os
import random
import time

import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")


def connect_to_rabbitmq():
    credentials = pika.PlainCredentials(
        RABBITMQ_USER,
        RABBITMQ_PASSWORD
    )

    while True:
        try:
            print("🔄 Connecting to RabbitMQ...", flush=True)

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

            print("✅ Connected!", flush=True)

            return connection, channel

        except pika.exceptions.AMQPConnectionError:
            print("❌ RabbitMQ unavailable. Retrying in 5 seconds...", flush=True)
            time.sleep(5)


connection, channel = connect_to_rabbitmq()

order_id = 100

while True:
    try:
        order_id += 1

        message = {
            "order_id": order_id,
            "customer": "Sai",
            "amount": random.randint(100, 1000)
        }

        channel.basic_publish(
            exchange="events",
            routing_key="email",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )

        print(f"📤 Published: {message}", flush=True)

        time.sleep(5)

    except (
        pika.exceptions.AMQPConnectionError,
        pika.exceptions.StreamLostError
    ):
        print("⚠️ Connection lost. Reconnecting...", flush=True)
        connection, channel = connect_to_rabbitmq()