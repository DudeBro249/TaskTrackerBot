class ChannelOut:
    channel_record_id: int
    channel_id: str
    guild_id: str

    def __init__(self, channel_record_id: int, channel_id: str, guild_id: str) -> None:
        self.channel_record_id = channel_record_id
        self.channel_id = channel_id
        self.guild_id = guild_id

    @staticmethod
    def from_dict(obj: dict) -> 'ChannelIn':
        channel_record_id = int(obj.get("channel_record_id"))
        channel_id = str(obj.get("channel_id"))
        guild_id = str(obj.get("guild_id"))
        return ChannelIn(channel_record_id, channel_id, guild_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["channel_record_id"] = int(self.channel_record_id)
        result["channel_id"] = str(self.channel_id)
        result["guild_id"] = str(self.guild_id)
        return result



class ChannelIn:
    channel_id: str
    guild_id: str

    def __init__(self, channel_id: str, guild_id: str) -> None:
        self.channel_id = channel_id
        self.guild_id = guild_id

    @staticmethod
    def from_dict(obj: dict) -> 'ChannelIn':
        channel_id = str(obj.get("channel_id"))
        guild_id = str(obj.get("guild_id"))
        return ChannelIn(channel_id, guild_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["channel_id"] = str(self.channel_id)
        result["guild_id"] = str(self.guild_id)
        return result