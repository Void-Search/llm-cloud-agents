from concrete_strategies import ProcessingStrategy, SpellCheckStrategy, GrammarCheckStrategy, FormattingStrategy

# Base Decorator
class ProcessorDecorator(ProcessingStrategy):
    def __init__(self, wrapped: ProcessingStrategy):
        self.wrapped = wrapped

    def process(self, text: str) -> str:
        return self.wrapped.process(text)

# Concrete Decorators
class FormattingDecorator(ProcessorDecorator):
    def process(self, text: str) -> str:
        return FormattingStrategy().process(super().process(text))

class SpellCheckDecorator(ProcessorDecorator):
    def process(self, text: str) -> str:
        return SpellCheckStrategy().process(super().process(text))

class GrammarCheckDecorator(ProcessorDecorator):
    def process(self, text: str) -> str:
        return GrammarCheckStrategy().process(super().process(text))