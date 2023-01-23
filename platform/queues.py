import os
import json
import base64
import pika



def send_to_queue(data):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')) # host?

    channel = connection.channel()

    channel.queue_declare(queue='hello')
    message = json.dumps(data)
    channel.basic_publish(exchange='',
                        routing_key='hello',
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

            counter += 1




