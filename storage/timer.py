import storage.raft
from storage.constants import ELECTION_DURATION, HEARTBEAT_DURATION
import random
from storage.services import set_election_timer_id, set_heartbeat_timer_id
from .tasks import app


@app.task(ignore_result=True)
def heartbeat():
    storage.raft.heartbeat_procedure()
    set_heartbeat_timer_id(storage.timer.heartbeat.apply_async(
        countdown=HEARTBEAT_DURATION).id)


@app.task(ignore_result=True)
def election():
    storage.raft.election_procedure()
    set_election_timer_id(storage.timer.election.apply_async(countdown=random.randint(
        ELECTION_DURATION, ELECTION_DURATION+10)).id)
