from concrete_strategies import ProcessingStrategy, SpellCheckStrategy, GrammarCheckStrategy, FormattingStrategy
from context import Context


# Base Decorator
class ProcessorDecorator(ProcessingStrategy):
    def __init__(self, wrapped: ProcessingStrategy):
        self.wrapped = wrapped

    def process(self, context: Context) -> Context:
        return self.wrapped.process(context)

# Concrete Decorators
class FormattingDecorator(ProcessorDecorator):
    def process(self, context: Context) -> Context:
        return FormattingStrategy().process(super().process(context))

class SpellCheckDecorator(ProcessorDecorator):
    def process(self, context: Context) -> Context:
        return SpellCheckStrategy().process(super().process(context))

class GrammarCheckDecorator(ProcessorDecorator):
    def process(self, context: Context) -> Context:
        return GrammarCheckStrategy().process(super().process(context))