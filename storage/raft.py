import base64
from math import ceil
from storage.models import Log
import storage.timer
from storage.utils import broadcast, send_to_node
from .tasks import app
import random
from storage.constants import HEARTBEAT_DURATION, ELECTION_DURATION, SELF_UUID, Role
from storage.dto.broadcast_request import BroadcastRequest
from storage.dto.log_request import LogRequest
from storage.dto.log_response import LogResponse
from storage.dto.vote_request import VoteRequest
from storage.dto.vote_response import VoteResponse
from storage.services import add_vote_recieved, append_log, get_acked_length_at, get_all_neighbours_id, get_commit_length, get_current_leader, get_current_role, get_current_term, get_election_timer_id, get_heartbeat_timer_id, get_log, get_sent_length_at, get_vote_received, get_voted_for, save_file, set_acked_length_at, set_commit_length, set_current_leader, set_current_role, set_current_term, set_election_timer_id, set_heartbeat_timer_id, set_log, set_sent_length_at, set_vote_received, set_voted_for


def election_procedure():
    # Called on leader fail or election time out
    # Start election
    set_current_term(get_current_term() + 1)
    set_voted_for(SELF_UUID)
    set_current_role(Role.CANDIDATE)
    set_vote_received(set([SELF_UUID]))

    last_term = 0
    log = get_log()
    if len(log) > 0:
        last_term = log.last().term

    broadcast(
        "/storage/message/vote-request",
        VoteRequest(
            current_term=get_current_term(),
            candidate_id=SELF_UUID,
            log_length=len(log),
            last_term=last_term
        )
    )


def on_receive_vote_request(c_id, c_term, c_log_length, c_log_term):
    print("Vote request received from", c_id + "," + str(c_term) +
          "," + str(c_log_length) + "," + str(c_log_term))
    # Vote on a candidate
    if c_term > get_current_term():
        set_current_term(c_term)
        set_current_role(Role.FOLLOWER)
        set_voted_for(None)

    last_term = 0
    log = get_log()
    if len(log) > 0:
        last_term = log.last().term
    log_ok = ((c_log_term > last_term)
              or (c_log_term == last_term and c_log_length >= len(log)))

    if (c_term == get_current_term()
        and log_ok
            and (get_voted_for() is None or get_voted_for() == c_id)):
        set_voted_for(c_id)
        send_to_node(c_id, "/storage/message/vote-response", VoteResponse(
            voter_id=SELF_UUID,
            term=c_term,
            vote_granted=True
        ))
    else:
        send_to_node(c_id, "/storage/message/vote-response", VoteResponse(
            voter_id=SELF_UUID,
            term=c_term,
            vote_granted=False
        ))


def on_receive_vote_response(voter_id, term, vote_granted):
    print("Vote response received from", voter_id +
          "," + str(term) + "," + str(vote_granted))
    # Collecting vote
    if get_current_role() == Role.CANDIDATE and term == get_current_term() and vote_granted:
        add_vote_recieved(voter_id)
        if len(get_vote_received()) >= ceil((len(get_all_neighbours_id())+2) / 2):
            set_current_role(Role.LEADER)
            set_current_leader(SELF_UUID)
            restart_election_timer()
            for follower in get_all_neighbours_id():
                set_sent_length_at(follower, len(get_log()))
                set_acked_length_at(follower, 0)
                replicate_log(SELF_UUID, follower)
            restart_heartbeat_timer()
        # else:
        #     logging.info("The votes are not enough...")
    elif term > get_current_term():
        set_current_term(term)
        set_current_role(Role.FOLLOWER)
        set_voted_for(None)
        restart_election_timer()


def request_to_broadcast(file_id, file_blob, file_name):
    if get_current_role() == Role.LEADER:
        append_log([Log(
            term=get_current_term(),
            file_blob=file_blob,
            file_name=file_name,
            file_id=file_id
        )])
        set_acked_length_at(SELF_UUID, len(get_log()))
        for follower in get_all_neighbours_id():
            replicate_log(SELF_UUID, follower)
    else:
        # Forward request to currentLeader
        send_to_node(get_current_leader(),
                     f"/storage/message/broadcast-request",
                     BroadcastRequest(
                         file_blob=base64.b64encode(file_blob).decode('utf-8'),
                         file_name=file_name,
                         file_id=file_id
        ))


def heartbeat_procedure():
    if get_current_role() == Role.LEADER:
        for follower in get_all_neighbours_id():
            replicate_log(SELF_UUID, follower)


def replicate_log(leader_id, follower_id):
    prefix_len = get_sent_length_at(follower_id)
    log = get_log()
    suffix = log[prefix_len:]
    prefix_term = 0
    if prefix_len > 0:
        prefix_term = log[prefix_len-1].term
    send_to_node(follower_id, "/storage/message/log-request", LogRequest(
        leader_id=leader_id,
        current_term=get_current_term(),
        prefix_len=prefix_len,
        prefix_term=prefix_term,
        commit_length=get_commit_length(),
        suffix=suffix
    ))


def on_receive_log_request(leader_id, term, prefix_length, prefix_term, leader_commit, suffix):
    print("Log request received from", leader_id + "," + str(term) + "," +
          str(prefix_length) + "," + str(prefix_term) + "," + str(leader_commit) + "," + str(suffix))
    if term > get_current_term():
        set_current_term(term)
        set_voted_for(None)
        restart_election_timer()
    if term == get_current_term():
        set_current_role(Role.FOLLOWER)
        set_current_leader(leader_id)
    log = get_log()
    log_ok = ((len(log) >= prefix_length)
              and (prefix_length == 0 or log[prefix_length-1].term == prefix_term))
    if term == get_current_term() and log_ok:
        append_entries(prefix_length, leader_commit, suffix)
        ack = prefix_length + len(suffix)
        send_to_node(leader_id, "/storage/message/log-response", LogResponse(
            current_term=term,
            node_id=SELF_UUID,
            ack=ack,
            flag=True
        ))
    else:
        send_to_node(leader_id, "/storage/message/log-response", LogResponse(
            current_term=term,
            node_id=SELF_UUID,
            ack=0,
            flag=False
        ))
    restart_election_timer()


def append_entries(prefix_len, leader_commit, suffix):
    if len(suffix) > 0 and len(get_log()) > prefix_len:
        index = min(len(get_log()), prefix_len + len(suffix)) - 1
        if get_log()[index].term != suffix[index - prefix_len].term:
            if prefix_len < 1:
                pass
            else:
                set_log(get_log()[:prefix_len])
    if prefix_len + len(suffix) > len(get_log()):
        for i in range(len(get_log()) - prefix_len, len(suffix)):
            append_log([suffix[i]])
    if leader_commit > get_commit_length():
        for i in range(get_commit_length(), leader_commit):
            apply_log(get_log()[i])
        set_commit_length(leader_commit)


def on_receive_log_response(follower, term, ack, success):
    print("Log response received from", follower + "," +
          str(term) + "," + str(ack) + "," + str(success))
    if term == get_current_term() and get_current_role() == Role.LEADER:
        if success and ack >= get_acked_length_at(follower):
            set_sent_length_at(follower, ack)
            set_acked_length_at(follower, ack)
            commit_log_entries()
        elif get_sent_length_at(follower) > 0:
            set_sent_length_at(follower, get_sent_length_at(follower) - 1)
            replicate_log(SELF_UUID, follower)
    elif term > get_current_term():
        set_current_term(term)
        set_current_role(Role.FOLLOWER)
        set_voted_for(None)
        restart_election_timer()


def commit_log_entries():
    while get_commit_length() < len(get_log()):
        acks = 0
        for follower in get_all_neighbours_id():
            if get_acked_length_at(follower) > get_commit_length():
                acks += 1
        if acks >= ceil((len(get_all_neighbours_id())+1) / 2):
            apply_log(get_log()[get_commit_length()])
            set_commit_length(get_commit_length() + 1)
        else:
            break


def apply_log(log):
    print("========================================================")
    print("Applying log entry: ", log.file_blob)
    print("with file id: ", log.file_id)
    print("========================================================")
    file_memoryview = log.file_blob
    save_file(file_memoryview=file_memoryview,
              file_name=log.file_name, file_id=log.file_id)


def restart_heartbeat_timer():
    task_id = get_heartbeat_timer_id()
    if task_id:
        app.control.revoke(task_id, terminate=True)
    set_heartbeat_timer_id(storage.timer.heartbeat.apply_async(
        countdown=HEARTBEAT_DURATION).id)


def cancel_heartbeat_timer():
    task_id = get_heartbeat_timer_id()
    if task_id:
        app.control.revoke(task_id, terminate=True)


def restart_election_timer():
    task_id = get_election_timer_id()
    if task_id:
        app.control.revoke(task_id, terminate=True)
    set_election_timer_id(storage.timer.election.apply_async(countdown=random.randint(
        ELECTION_DURATION, ELECTION_DURATION+10)).id)


def cancel_election_timer():
    task_id = get_election_timer_id()
    if task_id:
        app.control.revoke(task_id, terminate=True)
