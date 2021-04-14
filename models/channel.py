from pydantic import BaseModel

class ChannelOut(BaseModel):
    channel_record_id: int
    channel_id: str
    guild_id: str


class ChannelIn(BaseModel):
    channel_id: str
    guild_id: str
