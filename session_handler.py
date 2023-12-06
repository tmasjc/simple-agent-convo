from datetime import datetime
from utils.common import logger, redis_client
from utils.utils import summarize
from utils.memory import insert_memory
from utils.vectorize import insert_vector

# connection details
pubsub = redis_client.pubsub()
channel = "pubsub_channel"
pubsub.subscribe(channel)
logger.success("Pub/Sub is active.")

## expect incoming session id, and do content summarization
## update chat session record with memory description
for message in pubsub.listen():
    if message["type"] == "message":
        session_id = message["data"].decode()
        raw_content = redis_client.get(session_id)

        if raw_content:
            memory_description = summarize(raw_content.decode())
            # logger.trace(f"Convo memory: {memory_description[:300:]}...") # displays the first xx chars only
            memory_status = insert_memory(
                session_id=session_id, content=memory_description
            )
            vector_status = insert_vector(
                session_id=session_id, content=memory_description
            )

            if memory_status & vector_status:
                logger.success(f"Session completed at {datetime.now()}")
            else:
                logger.debug(f"Session incomplete: {session_id}")
