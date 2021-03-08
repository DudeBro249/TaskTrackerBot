import os
from databases import Database

DATABASE_URL = str(os.getenv('DATABASE_URL'))
db = Database(DATABASE_URL)
