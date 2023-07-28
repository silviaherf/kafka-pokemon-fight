#!/usr/bin/env python

import logging
from configparser import ConfigParser
from confluent_kafka import Consumer
import psycopg2
from datetime import datetime
from dotenv import dotenv_values

secrets = dotenv_values("src/.env")

if __name__ == "__main__":
    task_logger = logging.getLogger()
    task_logger.addHandler(logging.StreamHandler())

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read("config.ini")
    config = dict(config_parser["default"])
    config.update(config_parser["consumer"])

    # Create Consumer instance
    consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions=1):
        consumer.assign(partitions)

    # Subscribe to topic
    topic = "pokemon_topic"
    consumer.subscribe([topic], on_assign=reset_offset)

    "connect to postgres"
    conn = psycopg2.connect(
        database="pokemon_kafka",
        user=secrets.get("POSTGRES_USER"),
        password=secrets.get("POSTGRES_PASSWORD"),
        host="127.0.0.1",
        port="5432",
    )
    cursor = conn.cursor()

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting...")
            elif msg.error():
                print(f"ERROR: {msg.error()}")
            else:
                # Extract the (optional) key and value, and print.
                topic = msg.topic()
                key = msg.key().decode("utf-8")
                value = msg.value().decode("utf-8")
                timestamp = datetime.utcfromtimestamp(msg.timestamp()[1] / 1000)

                cursor.execute(
                    "INSERT INTO pokemon_battle (pokemon_name,ability,timestamp) VALUES (%s, %s, %s)",
                    (value, key, timestamp),
                )
                conn.commit()

                print(
                    f"Saved event from topic {topic}: {value.capitalize()} used {key}"
                )
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
