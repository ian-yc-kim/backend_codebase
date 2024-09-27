from sqlalchemy import Column, String, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import JSON
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class UserInput(Base):
    __tablename__ = 'user_inputs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    plot = Column(Text, nullable=False)
    setting = Column(Text, nullable=False)
    theme = Column(Text, nullable=False)
    conflict = Column(Text, nullable=False)
    additional_preferences = Column(JSON, nullable=True)
    ai_generated_content = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
