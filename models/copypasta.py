import orm
from pydantic.main import BaseModel
from db_manager.db import db, metadata

class CopypastaOut(BaseModel):
    id: int
    name: str
    content: str
    guild_id: str


class CopypastaIn(BaseModel):
    name: str
    content: str
    guild_id: str

class CopypastaTable(orm.Model):
    __tablename__ = "copypastas"
    __database__ = db
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    name = orm.String(max_length=30)
    content = orm.String(max_length=1500)
    guild_id = orm.String(max_length=30)
