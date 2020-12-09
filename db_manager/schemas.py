import sqlalchemy

metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(length=30), nullable=False),
    sqlalchemy.Column("content", sqlalchemy.String(length=200), nullable=False),
    sqlalchemy.Column("deadline", sqlalchemy.String(length=10), nullable=False),
    sqlalchemy.Column("date_assigned", sqlalchemy.String(length=10), nullable=False),
    sqlalchemy.Column("guild_id", sqlalchemy.String(length=50), nullable=False),
    sqlalchemy.Column("role_id", sqlalchemy.String(length=50), nullable=False)
)

channels = sqlalchemy.Table(
    "channels",
    metadata,
    sqlalchemy.Column("record_id", sqlalchemy.Integer, primary_key=True, nullable=False),
    sqlalchemy.Column("channel_id", sqlalchemy.String(length=50), nullable=False),
    sqlalchemy.Column("guild_id", sqlalchemy.String(length=50), nullable=False)
)

copypastas = sqlalchemy.Table(
    "copypastas",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String(length=60), nullable=False),
    sqlalchemy.Column("content", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("guild_id", sqlalchemy.String(length=50), nullable=False)
)


