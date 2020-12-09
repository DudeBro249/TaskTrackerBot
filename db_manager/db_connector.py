import os
from databases import Database

DATABASE_URI = str(os.getenv('DATABASE_URI'))
db = Database(DATABASE_URI)
