from utils.common import logger, redis_client

# connection details
pubsub  = redis_client.pubsub()
channel = 'pubsub_channel'
pubsub.subscribe(channel)
logger.success("Pub/Sub is active.")

## expect incoming session id, and do content summarization
## update chat session record with summary
for message in pubsub.listen():
    if message['type'] == 'message':
        session_id = message['data'].decode()
        logger.success(f"Session id: {session_id}")
        content = redis_client.get(session_id) 
        if content: 
            print(content) # do something with conversation content
