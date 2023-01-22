# pripabox-ModelCLS


Url for prediction:  http://127.0.0.1:8000/predict

Method: **Post**

 request.py
A script is given for the post request, which takes as an parameter a **.png** or **.jpg** file. Any other extension is not accepted. 


## Docker

```
cd existing_repo
docker-compose up
```

## Queue

A docker compose service "queues" run a script, that consume requests and send results by rabbitmq queues.

Script params should be placed in `.env` file (can be specified in docker-compose config) or in `docker-compose.yaml` directly.

```lombok.config
RABBITMQ_USER=user
RABBITMQ_PASSWORD=password
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672

RABBITMQ_CONSUME_QUEUE=to_ai
RABBITMQ_PRODUCE_QUEUE=from_ai
```
