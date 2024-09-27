import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend_codebase.models import Base, UserInput

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope='module')
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def db_session(setup_database):
    session = TestingSessionLocal()
    yield session
    session.close()

def test_user_input_model(db_session):
    user_input = UserInput(
        user_id=None,
        plot='A hero saves the day',
        setting='A futuristic city',
        theme='Courage and bravery',
        conflict='An impending disaster',
        additional_preferences={},
        ai_generated_content='The hero overcomes all odds'
    )
    db_session.add(user_input)
    db_session.commit()

    result = db_session.query(UserInput).filter_by(plot='A hero saves the day').first()
    assert result is not None
    assert result.ai_generated_content == 'The hero overcomes all odds'
