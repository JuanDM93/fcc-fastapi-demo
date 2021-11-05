from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import settings


SQLALCHEMY_DATABASE_URL = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    db=settings.DB_NAME
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
while True:
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()
        print("Connected to the database")
        break
    except (Exception, psycopg2.Error) as error:
        print(error)
        print(f"Retrying in {settings.SLEEP_TIME} secs")
        sleep(settings.SLEEP_TIME)
"""
