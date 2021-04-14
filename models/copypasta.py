from pydantic.main import BaseModel

class CopypastaOut(BaseModel):
    id: int
    name: str
    content: str
    guild_id: str


class CopypastaIn(BaseModel):
    name: str
    content: str
    guild_id: str
