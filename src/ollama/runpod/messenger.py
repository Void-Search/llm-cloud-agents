from requestbuilder import RequestBuilder


class Messenger:
    def __init__(self, strategy):
        self.strategy = strategy

    def send_message(self, model, prompt, **kwargs):
        builder = RequestBuilder()
        builder.add_model(model)
        builder.add_prompt(prompt)
        for key, value in kwargs.items():
            builder.add_option(key, value)
        payload = builder.build()
        return self.strategy.send(payload)
        