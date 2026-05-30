from redis import Redis
from rq import Queue

q = Queue(connection=Redis(
    host="localhost",
    port=6379  #mention the port which u have exposed in the docker compose file. 
))