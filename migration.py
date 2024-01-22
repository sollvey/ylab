from sqlalchemy import text
from sqlalchemy_utils import create_database, database_exists

from session import db_url, get_session

if not database_exists(db_url):
    create_database(db_url)

with open("init.sql", "r") as file:
    query = file.read()
    with get_session() as session:
        session.execute(text(query))
        session.commit()