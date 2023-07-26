#!/usr/bin/env python

from datetime import datetime
import random
from random import choice
from configparser import ConfigParser
import logging
from confluent_kafka import Producer

from src import pokemon as p

if __name__ == "__main__":
    task_logger = logging.getLogger()
    task_logger.addHandler(logging.StreamHandler())

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read("config.ini")
    config = dict(config_parser["default"])

    # Create Producer instance
    producer = Producer(config, logger=task_logger)

    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(err, msg):
        if err:
            print("ERROR: Message failed delivery: {}".format(err))
        else:
            topic = msg.topic()
            key = msg.key().decode("utf-8")
            value = msg.value().decode("utf-8")

            print(f"[{topic}] : {value.capitalize()} used {key}")
            task_logger.info(f"[{topic}] : Event sent to consumer")

    # Produce data by selecting random values from these lists.
    topic = "pokemon_topic"
    while True:
        pokemon_id = random.choice([x for x in range(1000)])
        pokemon = p.get_pokemon(pokemon_id)
        producer.produce(
            topic,
            pokemon.get("name"),
            pokemon.get("ability"),
            on_delivery=delivery_callback,
        )

        producer.poll(timeout=100)
        producer.flush()
