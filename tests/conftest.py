import os
from datetime import date

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

load_dotenv()

TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
DATABASE_URL = os.environ["DATABASE_URL"]
if TEST_DATABASE_URL is None:
    raise RuntimeError(
        "TEST_DATABASE_URL is not set. Add it to .env and point it to the test database."
    )

if make_url(DATABASE_URL) == make_url(TEST_DATABASE_URL):
    raise RuntimeError(
        "TEST_DATABASE_URL must not point to the application database."
    )

# app.database reads DATABASE_URL while it is imported. Setting it here makes
# accidental use of the normal SessionLocal safe inside the pytest process too.
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.database import get_db
from app.main import app
from app.models import Base, TaskModel


test_engine = create_engine(TEST_DATABASE_URL)


@pytest.fixture
def db_session():
    connection = test_engine.connect()
    outer_transaction = connection.begin()

    # Give every test an empty view of all application tables. The deletion is
    # part of the outer transaction, so pre-existing test data is restored by
    # the final rollback.
    for table in reversed(Base.metadata.sorted_tables):
        connection.execute(delete(table))

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

        try:
            if not outer_transaction.is_active:
                raise RuntimeError(
                    "The test's outer transaction ended before fixture cleanup."
                )

            outer_transaction.rollback()
        finally:
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


@pytest.fixture
def task_payload():
    return {
        "title": "Write API tests",
        "text": "Cover every task endpoint",
        "deadline": "2026-12-01",
        "status": "pending",
    }


@pytest.fixture
def task_factory(db_session):
    def create_task(
        *,
        title="Test task",
        text="Test task details",
        deadline="2026-12-01",
        status="pending",
    ):
        task = TaskModel(
            title=title,
            text=text,
            deadline=date.fromisoformat(deadline),
            status=status,
        )
        db_session.add(task)
        db_session.flush()
        db_session.refresh(task)
        return task

    return create_task
