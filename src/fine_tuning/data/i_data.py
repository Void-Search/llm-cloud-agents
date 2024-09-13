from abc import ABC, abstractmethod
from typing import Any

class IData(ABC):
    @abstractmethod
    def get_data(self) -> Any:
        pass

    @abstractmethod
    def get_data_type(self) -> str:
        pass


    @abstractmethod
    def get_id(self) -> str:
        pass