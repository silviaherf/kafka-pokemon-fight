#!/usr/bin/env python

import logging
from configparser import ConfigParser
from confluent_kafka import Consumer

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
                print("ERROR: %s".format(msg.error()))
            else:
                # Extract the (optional) key and value, and print.
                topic = msg.topic()
                key = msg.key().decode("utf-8")
                value = msg.value().decode("utf-8")

                print(
                    f"Consumed event from topic {topic}: {value.capitalize()} used {key}"
                )
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
