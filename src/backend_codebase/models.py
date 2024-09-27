from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()

class UserInput(Base):
    __tablename__ = 'user_inputs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=True)
    plot = Column(Text, nullable=False)
    setting = Column(Text, nullable=False)
    theme = Column(Text, nullable=False)
    conflict = Column(Text, nullable=False)
    additional_preferences = Column(Text, nullable=True)
