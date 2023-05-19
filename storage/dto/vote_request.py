class VoteRequest:
    def __init__(self, current_term: int, candidate_id: int, log_length: int, last_term: int):
        self.candidate_id = candidate_id
        self.current_term = current_term
        self.log_length = log_length
        self.last_term = last_term

    def to_dict(self):
        return {
            'candidate_id': self.candidate_id,
            'current_term': self.current_term,
            'log_length': self.log_length,
            'last_term': self.last_term
        }
