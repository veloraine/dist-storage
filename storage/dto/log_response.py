class LogResponse:
    def __init__(self, node_id, current_term, ack, flag):
        self.node_id = node_id
        self.current_term = current_term
        self.ack = ack
        self.flag = flag

    def to_dict(self):
        return {
            'node_id': self.node_id,
            'current_term': self.current_term,
            'ack': self.ack,
            'flag': self.flag
        }
