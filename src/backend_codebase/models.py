from . import db
import uuid
from sqlalchemy import func
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.types import JSON
from datetime import datetime

class GUID(TypeDecorator):
    """Platform-independent GUID type."""
    impl = CHAR(36)

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(pgUUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif not isinstance(value, uuid.UUID):
            return str(uuid.UUID(value))
        else:
            return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(GUID(), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# Similarly update other models...
