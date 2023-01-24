import os
import json
import base64
import logging
import sys 

import pika

from logger import setup_logger

from dotenv import load_dotenv
load_dotenv()

from db.base import engine


logger = logging.getLogger("queues")
USER = str(os.getenv('RABBITMQ_USER'))
PASSWORD = str(os.getenv('RABBITMQ_PASSWORD'))
HOST = str(os.getenv('RABBITMQ_HOST'))
PORT = int(os.getenv('RABBITMQ_PORT'))
CONSUME_QUEUE = str(os.getenv('RABBITMQ_CONSUME_QUEUE'))
PRODUCE_QUEUE = str(os.getenv('RABBITMQ_PRODUCE_QUEUE'))

credentials = pika.PlainCredentials(USER, PASSWORD)
conn_params = pika.ConnectionParameters(host=HOST, port=PORT, credentials=credentials)



def send_to_queue(data):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')) # conn_params

    channel = connection.channel()
    channel.queue_declare(queue=CONSUME_QUEUE)
    
    
    message = json.dumps(data)
    channel.basic_publish(exchange='',
                        routing_key=CONSUME_QUEUE,
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode=2,  # make message persistent
                        ))

    print(f" [x] sent file {data['photo_id']} to queue")

    connection.close() # do we close it every time?


path = 'images/'
data = {}

for root, dirs, files in os.walk(path, topdown=False):
    counter = 0
    for name in files:
        with open(os.path.join(root, name,), 'rb') as f:
            
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
            data['image'] = img_b64
            data['photo_id'] = counter

            send_to_queue(data)
            logger.debug(f"Data sent: image_id = {data['photo_id']}")

            counter += 1


def main(counter): # counter is used to know when to close rabbit connection
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    channel.queue_declare(queue=PRODUCE_QUEUE)

    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            logger.debug(f"Returned data: {data['photo_id']}, {data['label']}")
            channel.basic_ack(delivery_tag=method.delivery_tag)
            print('!', type(data['photo_id']), type(data['label']))
            query_data = (None, data['label'])
            query = "INSERT INTO Photo VALUES(?, ?)"
            engine.execute(query, query_data)

            # logger.debug('Data saved:', data['photo_id'], data['label'])
            logger.debug(f"Data saved: {data['photo_id']}, {data['label']}")
            
        except Exception as e:
            logger.exception('Error', e)
            # https://stackoverflow.com/questions/24333840/rejecting-and-requeueing-a-rabbitmq-task-when-prefetch-count-1
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

        # if counter - 1 == int(data['photo_id']):
        #     channel.stop_consuming()


    channel.basic_consume(queue=PRODUCE_QUEUE, on_message_callback=callback)

    logger.info('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()



if __name__ == '__main__':
    try:
        setup_logger()
        main(counter)
        # uvicorn.run("platform:queues", port=8000, host='0.0.0.0', reload=True)
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)

