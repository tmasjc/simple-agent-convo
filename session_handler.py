from utils.common import logger, redis_client
from utils.utils import summarize
from utils.database import ChatSession, Session

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
        raw_content = redis_client.get(session_id) 
        if raw_content: 
            summary = summarize(raw_content.decode())
            logger.trace(f"Convo Summary: {summary[:300:]}...") # displays the first xx chars only
            session = Session() # insert to database
            record  = session.query(ChatSession).filter(ChatSession.chat_session_id == session_id).first()
            if record:
                record.summary = summary # update summary here
                session.commit()
            else:
                logger.debug(f"No record {session_id} found.")
            session.close()
