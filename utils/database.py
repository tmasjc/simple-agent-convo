from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True)
    chat_session_id = Column(String, nullable=False)
    datetime = Column(DateTime, default=datetime.utcnow)
    bot_identifier = Column(String)
    player_identifier = Column(String)
    summary = Column(String)

    def __repr__(self):
        return f"Start new chat session {self.chat_session_id}"


# connect to database
engine = create_engine("sqlite:///records.db")
Base.metadata.create_all(engine)

# construct a new .sessionmaker
Session = sessionmaker(bind=engine)

# wrapper function
def add_session_record(record: ChatSession):
    session = Session()
    new_record = record
    session.add(new_record)
    session.commit()
    session.close()