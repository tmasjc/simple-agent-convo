from utils.database import ChatSession, session_scope
from utils.common import logger

def insert_memory(session_id: str, content: str) -> bool:
    """
    Add new or alter memory of a chat session. 
    
    Args:
    - session_id: uniq id of chat session in database
    - content: chat memory description

    Returns True if successful, False if not.
    """
    with session_scope() as session:
        try:
            record = (
                session.query(ChatSession)
                .filter(ChatSession.chat_session_id == session_id)
                .first()
            )
            record.memory = content
            logger.success(f"Inserted memory for {session_id}...")
            return True
        except Exception as e:
            logger.debug(e)
            return False

def retrieve_latest_memory(var: str, value: str) -> str | None:
    """
    Get latest memory of [var] matches [value] from database.

    Args: 
    - key: one of the string variable of ChatSession class

    Returns memory string or None if not found.
    """
    filter_expression = getattr(ChatSession, var) == value
    with session_scope() as session:
        record = (
            session.query(ChatSession)
            .filter(filter_expression)
            .order_by(ChatSession.id.desc())
            .first()
        )
        # logger.trace(record.id)
        if record:
            return record.memory
        return None
