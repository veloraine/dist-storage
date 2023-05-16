from django.core.cache import cache
from storage.constants import NEIGHBOURS, Role
from storage.utils import blob_to_file
from .models import CommitLength, CurrentTerm, File, Log, VotedFor


def get_current_role():
    return cache.get('current_role')


def set_current_role(role):
    cache.set('current_role', role)


def set_current_leader(leader):
    cache.set('current_leader', leader)


def get_current_leader():
    return cache.get('current_leader')


def add_vote_recieved(vote):
    votes_received = cache.get('votes_received')
    votes_received.add(vote)
    cache.set('votes_received', votes_received)


def set_vote_received(votes):
    cache.set('votes_received', votes)


def get_vote_received():
    return cache.get('votes_received')


def set_current_term(term):
    m = CurrentTerm.get_solo()
    m.value = term
    m.save()


def get_current_term():
    return CurrentTerm.get_solo().value


def set_voted_for(value):
    m = VotedFor.get_solo()
    m.value = value
    m.save()


def get_voted_for():
    return VotedFor.get_solo().value


def get_log():
    return Log.objects.all().order_by('id')


def set_log(list_of_log_objects):
    Log.objects.all().delete()
    for log_object in list_of_log_objects:
        log_object.save()


def append_log(list_of_log_objects):
    for log_object in list_of_log_objects:
        log_object.save()


def set_sent_length(length):
    cache.set('sent_length', length)


def set_sent_length_at(id, value):
    sent_length = cache.get('sent_length')
    sent_length[id] = value
    cache.set('sent_length', sent_length)


def get_sent_length_at(id):
    sent_length = cache.get('sent_length')
    return sent_length[id]


def get_sent_length():
    return cache.get('sent_length')


def set_acked_length(length):
    cache.set('acked_length', length)


def set_acked_length_at(id, value):
    acked_length = cache.get('acked_length')
    acked_length[id] = value
    cache.set('acked_length', acked_length)


def get_acked_length_at(id):
    acked_length = cache.get('acked_length')
    return acked_length[id]


def get_acked_length():
    return cache.get('acked_length')


def get_commit_length():
    return CommitLength.get_solo().value


def set_commit_length(length):
    m = CommitLength.get_solo()
    m.value = length
    m.save()


def get_all_neighbours_id():
    ids = []
    for neighbour in NEIGHBOURS:
        ids.append(neighbour["id"])
    return ids


def get_election_timer_id():
    return cache.get('election_timer_id')


def set_election_timer_id(task_id):
    cache.set('election_timer_id', task_id)


def get_heartbeat_timer_id():
    return cache.get('heartbeat_timer_id')


def set_heartbeat_timer_id(task_id):
    cache.set('heartbeat_timer_id', task_id)


def init_persistent_variables():
    set_current_term(0)
    set_voted_for(None)
    set_commit_length(0)
    set_log([])


def init_volatile_variables():
    set_current_role(Role.FOLLOWER)
    set_current_leader(None)
    set_vote_received(set())
    set_sent_length(dict())
    set_acked_length(dict())


def save_file(file_blob, file_id, file_name):
    if (File.objects.filter(id=file_id).exists()):
        pass
        # TODO: replace file?
    else:
        file = blob_to_file(file_blob, file_name)
        File.objects.create(id=file_id, uploaded_file=file)


def is_file_id_exists(file_id):
    return File.objects.filter(id=file_id).exists()
