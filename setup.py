import sys
import panel as pn
import bokeh.server.contexts as ctx
import redis
from loguru import logger
logger.level("setuponly", no=38, color="<yellow>")

def session_created(session_context: ctx.BokehSessionContext):
    pass
    
def session_destroyed(session_context: ctx.BokehSessionContext):
    client  = redis.Redis(host='localhost', port=6379, db=0)
    channel = 'pubsub_channel'
    message = f"{session_context.id}"
    logger.log("setuponly", f"Publish to `{channel}` - '{message}'")
    client.publish(channel, message)

# pn.state.on_session_created(session_created)
pn.state.on_session_destroyed(session_destroyed)
