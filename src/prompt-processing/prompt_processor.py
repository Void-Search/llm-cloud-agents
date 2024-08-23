from concrete_strategies import NoOpStrategy
from processor_decorator import FormattingDecorator, SpellCheckDecorator, GrammarCheckDecorator
from context import Context

class PromptProcessor:
    def __init__(self):
        self.base_processor = NoOpStrategy()

    def add_formatting(self):
        self.base_processor = FormattingDecorator(self.base_processor)
        return self

    def add_spell_check(self):
        self.base_processor = SpellCheckDecorator(self.base_processor)
        return self

    def add_grammar_check(self):
        self.base_processor = GrammarCheckDecorator(self.base_processor)
        return self

    def process(self, text: str) -> str:
        context = Context(text)
        processed_context = self.base_processor.process(context)
        return processed_context.text

# Usage example
if __name__ == "__main__":
    processor = (PromptProcessor()
                 .add_formatting()
                 .add_spell_check()
                 .add_grammar_check())
    long_text = "This is a verry long text with some misspeled words and grammer issues. " * 10
    result = processor.process(long_text)
    print(result)