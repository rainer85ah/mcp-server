from dataclasses import dataclass
from mcp.server.fastmcp import Context


class RequestContext:
    def __init__(self, user_id=None, session_id=None, city=None):
        self.user_id = user_id
        self.session_id = session_id
        self.city = city


@dataclass
class AppContext(Context):
    pass
    # sql_db: Database


class LifespanContext:
    def __init__(self):
        """
        self.pg_db = db.init_postgres()
        self.mongo = db.init_mongo()
        self.redis = cache.init_redis()
        self.data_dir = filesystem.get_data_dir()
        """
