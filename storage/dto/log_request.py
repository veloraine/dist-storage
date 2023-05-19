from django.forms import model_to_dict

from storage.utils import log_to_dict


class LogRequest:
    def __init__(self, leader_id, current_term, prefix_len, prefix_term, commit_length, suffix):
        self.leader_id = leader_id
        self.current_term = current_term
        self.prefix_len = prefix_len
        self.prefix_term = prefix_term
        self.commit_length = commit_length
        self.suffix = suffix

    def to_dict(self):
        return {
            'leader_id': self.leader_id,
            'current_term': self.current_term,
            'prefix_len': self.prefix_len,
            'prefix_term': self.prefix_term,
            'commit_length': self.commit_length,
            'suffix': [log_to_dict(log) for log in self.suffix]
        }
