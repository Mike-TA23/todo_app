# tests/conftest.py
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import get_db
from app.main import app

TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]

test_engine = create_engine(TEST_DATABASE_URL)

@pytest.fixture
def db_session():
    connection = test_engine.connect()
    outer_transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        outer_transaction.rollback()
        connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)