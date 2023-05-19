class VoteResponse:
    def __init__(self, voter_id: int, term: int, vote_granted: bool):
        self.voter_id = voter_id
        self.vote_granted = vote_granted
        self.term = term

    def to_dict(self):
        return {
            'voter_id': self.voter_id,
            'vote_granted': self.vote_granted,
            'term': self.term
        }
