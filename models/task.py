import orm
from db_manager.db import db, metadata
from pydantic import BaseModel


class TaskOut(BaseModel):
    task_id: int
    title: str
    content: str
    deadline: str
    date_assigned: str
    guild_id: str
    role_id: str

class TaskIn(BaseModel):
    title: str
    content: str
    deadline: str
    date_assigned: str
    guild_id: str
    role_id: str

class TaskTable(orm.Model):
    __tablename__ = "tasks"
    __database__ = db
    __metadata__ = metadata

    task_id = orm.Integer(primary_key=True)
    title = orm.String(max_length=40)
    content = orm.String(max_length=500)
    deadline = orm.String(max_length=20)
    date_assigned = orm.String(max_length=20)
    guild_id = orm.String(max_length=30)
    role_id = orm.String(max_length=30)
