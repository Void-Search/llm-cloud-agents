import requestbuilder


class Messenger:
    def __init__(self, strategy):
        self.strategy = strategy

    def build_message(self, model, prompt, **kwargs):
        builder = builder.RequestBuilder()
        builder.add_model(model)
        builder.add_prompt(prompt)
        for key, value in kwargs.items():
            builder.add_option(key, value)
        return builder.build()

    def send_request(self, payload):
        return self.strategy.send(payload)
        