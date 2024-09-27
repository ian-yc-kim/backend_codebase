import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend_codebase.models import Base, UserInput, NovelIteration
import os

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture(scope='module')
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def session(setup_database):
    session = Session()
    yield session
    session.close()


def test_user_input_model(session):
    user_input = UserInput(
        plot='A hero saves the world',
        setting='Futuristic city',
        theme='Courage',
        conflict='Hero vs Villain'
    )
    session.add(user_input)
    session.commit()
    assert user_input.id is not None


def test_novel_iteration_model(session):
    novel_iteration = NovelIteration(
        iteration_number='1',
        content='The hero begins his journey'
    )
    session.add(novel_iteration)
    session.commit()
    assert novel_iteration.id is not None
