from abc import ABC, abstractmethod

class RequestBuilder:
    def __init__(self):
        self.payload = {}

    def add_model(self, model):
        self.payload['model'] = model
        return self

    def add_prompt(self, prompt):
        self.payload['prompt'] = prompt
        return self

    def add_option(self, key, value):
        self.payload[key] = value
        return self

    def build(self):
        return self.payload
    