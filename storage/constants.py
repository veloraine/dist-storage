from enum import Enum
import os

HEARTBEAT_DURATION = 5
ELECTION_DURATION = 5


class Role(Enum):
    FOLLOWER = 0,
    CANDIDATE = 1,
    LEADER = 2


SELF_UUID = os.environ.get("URL_0")
NEIGHBOURS = [
    {
        "id": os.environ.get("URL_1"),
        "url": os.environ.get("URL_1")
    },
    {
        "id": os.environ.get("URL_2"),
        "url": os.environ.get("URL_2")
    },
    {
        "id": os.environ.get("URL_3"),
        "url": os.environ.get("URL_3")
    },
]
