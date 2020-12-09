class CopypastaOut:
    id: int
    name: str
    content: str
    guild_id: str

    def __init__(self, id: int, name: str, content: str, guild_id: str) -> None:
        self.id = id
        self.name = name
        self.content = content
        self.guild_id = guild_id

    @staticmethod
    def from_dict(obj: dict) -> 'CopypastaOut':
        assert isinstance(obj, dict)
        id = int(obj.get("id"))
        name = str(obj.get("name"))
        content = str(obj.get("content"))
        guild_id = str(obj.get("guild_id"))
        return CopypastaOut(id, name, content, guild_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = int(self.id)
        result["name"] = str(self.name)
        result["content"] = str(self.content)
        result["guild_id"] = str(self.guild_id)
        return result


class CopypastaIn:
    name: str
    content: str
    guild_id: str

    def __init__(self, name: str, content: str, guild_id: str) -> None:
        self.name = name
        self.content = content
        self.guild_id = guild_id

    @staticmethod
    def from_dict(obj: dict) -> 'CopypastaIn':
        assert isinstance(obj, dict)
        name = str(obj.get("name"))
        content = str(obj.get("content"))
        guild_id = str(obj.get("guild_id"))
        return CopypastaIn(name, content, guild_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = str(self.name)
        result["content"] = str(self.content)
        result["guild_id"] = str(self.guild_id)
        return result