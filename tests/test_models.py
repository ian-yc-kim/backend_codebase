import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.backend_codebase.models import Base, UserInput

DATABASE_URL = "postgresql://backend_database:74171843-ff5b@10.138.0.4:5432/backend_database"

@pytest.fixture(scope='module')
def engine():
    return create_engine(DATABASE_URL)

@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def dbsession(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_user_inputs_model(dbsession):
    new_input = UserInput(
        user_id=None,
        plot="A plot",
        setting="A setting",
        theme="A theme",
        conflict="A conflict",
        additional_preferences={"key": "value"}
    )
    dbsession.add(new_input)
    dbsession.commit()
    assert new_input.id is not None
