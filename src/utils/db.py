from model import Base
from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import Session

from .logging import get_system_logger
from .config import DatabaseConfig


class SessionMetaData:
    """Class to hold session metadata."""

    def __init__(self):
        self.__transaction_count = 0

    def increment_transaction_counter(self):
        self.__transaction_count += 1

    @property
    def transaction_count(self):
        return self.__transaction_count


internal_logger = get_system_logger()


def after_transaction_handler(session_metadata: "SessionMetaData"):
    def wrapper(s, t):
        internal_logger.debug(f"Transaction {t} committed")
        session_metadata.increment_transaction_counter()

    return wrapper


def get_engine(database_config: DatabaseConfig):
    """Get a new SQLAlchemy engine."""
    engine = create_engine(database_config.connection_url)
    Base.metadata.create_all(engine)
    internal_logger.info("Database tables created/verified")
    return engine


def get_session(engine: Engine) -> tuple[Session, SessionMetaData]:
    """Get a new SQLAlchemy session."""

    # Create all tables if they don't exist
    session = Session(engine)

    session_meta = SessionMetaData()

    event.listen(
        session, "after_transaction_end", after_transaction_handler(session_meta)
    )

    return session, session_meta
