class BroadcastRequest:
    def __init__(self, file_id, file_blob, file_name):
        self.file_id = file_id
        self.file_blob = file_blob
        self.file_name = file_name

    def to_dict(self):
        return {
            'file_id': self.file_id,
            'file_blob': self.file_blob,
            'file_name': self.file_name
        }
