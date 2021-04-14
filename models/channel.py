import orm
from db_manager.db import db, metadata
from pydantic import BaseModel


class ChannelOut(BaseModel):
    channel_record_id: int
    channel_id: str
    guild_id: str


class ChannelIn(BaseModel):
    channel_id: str
    guild_id: str

class ChannelTable(orm.Model):
    __tablename__ = "channels"
    __database__ = db
    __metadata__ = metadata

    channel_record_id = orm.Integer(primary_key=True)
    channel_id = orm.String(max_length=30)
    guild_id = orm.String(max_length=30)
