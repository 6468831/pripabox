import base64
import json
import logging
import os
import sys

import pika

from app import predict
from logger import setup_logger

logger = logging.getLogger("queues")

USER = str(os.getenv('RABBITMQ_USER'))
PASSWORD = str(os.getenv('RABBITMQ_PASSWORD'))
HOST = str(os.getenv('RABBITMQ_HOST'))
PORT = int(os.getenv('RABBITMQ_PORT'))
CONSUME_QUEUE = str(os.getenv('RABBITMQ_CONSUME_QUEUE'))
PRODUCE_QUEUE = str(os.getenv('RABBITMQ_PRODUCE_QUEUE'))

credentials = pika.PlainCredentials(USER, PASSWORD)
conn_params = pika.ConnectionParameters(host=HOST, port=PORT, credentials=credentials)


def send_result(photo_id, label):
    logger.info('Start send result')
    connection = pika.BlockingConnection(conn_params)
    ch = connection.channel()
    data = {
        "photo_id": photo_id,
        "label": label,
    }
    logger.debug('Result data:', data)
    message = json.dumps(data)
    ch.basic_publish(exchange='',
                     routing_key=PRODUCE_QUEUE,
                     body=message,
                     properties=pika.BasicProperties(
                         delivery_mode=2,  # make message persistent
                     ))
    connection.close()
    logger.info('End send result')


def main():
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            logger.debug('Get data:', data)
            image = base64.b64decode(data['image'])

            label = predict(image)
            logger.debug('Predict label:', data)
            send_result(data['photo_id'], label)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            logger.exception('Error', e)
            # https://stackoverflow.com/questions/24333840/rejecting-and-requeueing-a-rabbitmq-task-when-prefetch-count-1
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

    channel.basic_consume(queue=CONSUME_QUEUE, on_message_callback=callback)

    logger.info('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        setup_logger()
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)

