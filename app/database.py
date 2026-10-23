from os import environ
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
db_url = environ['DATABASE_URL']
engine = create_engine(db_url)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()