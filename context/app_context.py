from dataclasses import dataclass
from resources.mongodb import MongoDB


@dataclass
class AppContext:
    mongo: MongoDB
