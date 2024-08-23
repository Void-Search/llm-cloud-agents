class Context:
    def __init__(self, text: str):
        self.text = text
        self.metadata = {}

    def set_metadata(self, key: str, value: any):
        self.metadata[key] = value

    def get_metadata(self, key: str, default=None):
        return self.metadata.get(key, default)