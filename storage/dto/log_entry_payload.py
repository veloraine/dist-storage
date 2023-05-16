class LogEntryPayload:
    def __init__(self, file, file_id, file_name):
        self.file = file
        self.file_id = file_id
        self.file_name = file_name

    def to_dict(self):
        return {
            'file': self.file,
            'file_id': self.file_id,
            'file_name': self.file_name
        }
