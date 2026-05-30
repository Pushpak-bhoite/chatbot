# we are going to use 
# It's kind of Queue structure in System Design
# Like FIFO first in first out - our server will take all the request in queue, and serve them one after another as they prepare in FIFO manner. 

# package = Python RQ - https://python-rq.org/ 
# RQ- This actually uses redis in the backend, So we could use redis directly bt it's open source license has been revoked. 
# Valkey - Is an drop in replacement for redis, so we can use valkey in replacement of Redis. 


# so the consumer part is processing all the message(requests)
# & In the Queue, storing all messages(requests)

# In code -
# Client dir = contains all connection information. 
# Queue dir = Where we keep the workers. 