from constants.environment import DATABASE_URL
from databases import Database
import sqlalchemy

db = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

def create_all_tables() -> None:
    """Creates all SQL tables if they do not already exist in the database"""
    engine = sqlalchemy.create_engine(str(db.url))
    metadata.create_all(engine)
