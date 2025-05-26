from dataclasses import dataclass
from mcp.server.fastmcp import Context


class RequestContext:
    def __init__(self, user_id=None, session_id=None, trace_id=None):
        self.user_id = user_id
        self.session_id = session_id
        self.trace_id = trace_id


@dataclass
class AppContext(Context):
    def __init__(self):
        """
        self.mongo = db.init_mongo()
        self.data_dir = filesystem.get_data_dir()
        """
        pass


class LifespanContext:
    def __init__(self):
        """
        self.redis = cache.init_redis()
        self.data_dir = filesystem.get_data_dir()
        """
