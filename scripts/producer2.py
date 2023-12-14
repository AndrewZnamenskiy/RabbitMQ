#!/usr/bin/env python
# coding=utf-8

import pika
import json
import random
import time
# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.URLParameters('amqp://guest:guest@localhost:5672/'))
channel = connection.channel()
# Declare an exchange
channel.exchange_declare(exchange='sensor_exchange', exchange_type='direct')
# Prepare a list of divices
devices =[random.randint(0, 100) for i in range(100)]
# Prepare a list of possible routing keys
routing_keys = ['pressure', 'temperature']
while True:
    # Prepare random message in JSON format
    measure=random.choice(routing_keys)
    data = {'device': random.choice(devices), 'measure': measure, 'value': random.randint(0,100)}
    message = json.dumps(data)
    # Send the message to the exchange
    channel.basic_publish(exchange='sensor_exchange', routing_key=measure, body=message)
    print(f' [x] Sent {message}')
    # Sleep for 3 seconds
    time.sleep(3)
channel.close()
connection.close()


