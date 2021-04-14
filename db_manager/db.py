from constants.environment import DATABASE_URL
from databases import Database
import sqlalchemy

db = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

def create_all_tables() -> None:
    engine = sqlalchemy.create_engine(str(db.url))
    metadata.create_all(engine)
