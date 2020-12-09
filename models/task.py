class TaskOut:
    task_id: int
    title: str
    content: str
    deadline: str
    date_assigned: str
    guild_id: str
    role_id: str

    def __init__(self, task_id: int, title: str, content: str, deadline: str, date_assigned: str, guild_id: str, role_id: str) -> None:
        self.task_id = task_id
        self.title = title
        self.content = content
        self.deadline = deadline
        self.date_assigned = date_assigned
        self.guild_id = guild_id
        self.role_id = role_id
    
    def get_attribute(self, attribute: str):
        return getattr(self, attribute)
    
    def to_dict(self) -> dict:
        return {
            "task_id": int(self.task_id),
            "title": str(self.title),
            "content": str(self.content),
            "deadline": str(self.deadline),
            "date_assigned": str(self.date_assigned),
            "guild_id": str(self.guild_id),
            "role_id": str(self.role_id)
        }

class TaskIn:
    title: str
    content: str
    deadline: str
    date_assigned: str
    guild_id: str
    role_id: str

    def __init__(self, title: str, content: str, deadline: str, date_assigned: str, guild_id: str, role_id: str) -> None:
        self.title = title
        self.content = content
        self.deadline = deadline
        self.date_assigned = date_assigned
        self.guild_id = guild_id
        self.role_id = role_id
    
    def get_attribute(self, attribute: str):
        return getattr(self, attribute)
    
    def to_dict(self) -> dict:
        return {
            "title": str(self.title),
            "content": str(self.content),
            "deadline": str(self.deadline),
            "date_assigned": str(self.date_assigned),
            "guild_id": str(self.guild_id),
            "role_id": str(self.role_id)
        }