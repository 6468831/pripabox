Platform app sends base64 representations of images 
from /platform/images folder to a queue, receives 
back their labels and saves them to a database.


## Docker

```
cd existing_repo
docker-compose -f docker-compose-rabbitmq.yml up -d
docker-compose up -d
```

wait a few seconds for the app to trully load 
and check container logs

```
docker logs pripabox_platform_queues_1
```

