from abc import ABC, abstractmethod
from context import Context

# Base Strategy
class ProcessingStrategy(ABC):
    @abstractmethod
    def process(self, context: Context) -> Context:
        pass

