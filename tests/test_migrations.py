import pytest
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "postgresql://backend_database:74171843-ff5b@10.138.0.4:5432/backend_database"

@pytest.fixture(scope='module')
def setup_database():
    # Create an engine and a session
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Run migrations
    alembic_cfg = Config("/home/aiagent/ai_agents/workspace/53402918-5cbd-477d-bb38-e69f4555b1ad/backend_codebase/alembic.ini")
    command.upgrade(alembic_cfg, 'head')

    yield session

    # Rollback migrations
    command.downgrade(alembic_cfg, 'base')
    session.close()


def test_users_table_exists(setup_database):
    session = setup_database
    result = session.execute(text("SELECT * FROM information_schema.tables WHERE table_name='users'"))
    assert result.rowcount == 1


def test_users_table_columns(setup_database):
    session = setup_database
    result = session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users'"))
    columns = [row[0] for row in result]
    expected_columns = ['id', 'username', 'email', 'password_hash', 'created_at', 'updated_at']
    assert all(column in columns for column in expected_columns)


def test_unique_constraints_on_users_table(setup_database):
    session = setup_database
    # Insert a user
    session.execute(text("INSERT INTO users (username, email, password_hash) VALUES ('testuser', 'test@example.com', 'hashedpassword')"))
    session.commit()
    # Attempt to insert another user with the same username
    with pytest.raises(Exception):
        session.execute(text("INSERT INTO users (username, email, password_hash) VALUES ('testuser', 'test2@example.com', 'hashedpassword')"))
        session.commit()
    # Attempt to insert another user with the same email
    with pytest.raises(Exception):
        session.execute(text("INSERT INTO users (username, email, password_hash) VALUES ('testuser2', 'test@example.com', 'hashedpassword')"))
        session.commit()
