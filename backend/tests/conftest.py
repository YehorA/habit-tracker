import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from dotenv import load_dotenv
import os
from fastapi.testclient import TestClient
from main import app
from database import get_db

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise ValueError("TEST_DATABASE_URL environment variable is not set")

test_engine = create_engine(TEST_DATABASE_URL)

@pytest.fixture
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint"
    )

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_db, None)

    