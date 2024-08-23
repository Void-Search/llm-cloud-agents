import spellchecker as SpellChecker
import language_tool_python
from langdetect import detect
from processing_strategy import ProcessingStrategy
from context import Context

# Concrete Strategies

class NoOpStrategy(ProcessingStrategy):
    def process(self, context: Context) -> Context:
        lang = detect(context.text)
        context.set_metadata('language', lang)
        return context

class FormattingStrategy(ProcessingStrategy):
    def process(self, context: Context) -> Context:
        context.text = context.text.strip()
        context.text = context.text[0].upper() + context.text[1:]
        return context

class SpellCheckStrategy(ProcessingStrategy):
    def __init__(self):
        self.spell_checker = None

    def process(self, context: Context) -> Context:
        self.spell_checker = SpellChecker.SpellChecker(language=context.get_metadata('language', "en"))
        words = context.text.split()
        checked_words = []
        for word in words:
            if not self.spell_checker.unknown(word):
                correction = self.spell_checker.correction(word)
                if correction is not None:
                    checked_words.append(correction)
        # convert list into string
        context.text = ' '.join(checked_words)
        return context

class GrammarCheckStrategy(ProcessingStrategy):
    def __init__(self):
        self.grammar_checker = language_tool_python.LanguageTool('en-US')

    def process(self, context: Context) -> Context:
        self.grammar_checker.language = context.get_metadata('language','en-US')
        matches = self.grammar_checker.check(context.text)
        context.text = language_tool_python.utils.correct(context.text, matches)
        return context

class TextTruncationStrategy(ProcessingStrategy):
    def __init__(self, max_length: int):
        self.max_length = max_length

    def process(self, context: Context) -> Context:
        if len(context.text) > self.max_length:
            context.text = context.text[:self.max_length - 3] + "..."
        return context

