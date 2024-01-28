from os import environ
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

path_prefix = "/api/v1"
db_engine = "postgresql+psycopg2"
db_host = environ["DBHOST"]
db_port = environ["DBPORT"]
db_user = environ["DBUSER"]
db_pswd = environ["DBPSWD"]
db_name = environ["DBNAME"]
db_url = f"{db_engine}://{db_user}:{db_pswd}@{db_host}:{db_port}/{db_name}"
db_engine_sync = create_engine(db_url)

@contextmanager
def get_session():
    session = sessionmaker(bind=db_engine_sync, expire_on_commit=True)
    yield session()