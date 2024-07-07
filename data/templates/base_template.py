from enum import Enum, auto
from abc import ABC, abstractmethod

class WritingTemplateType(Enum):
    DELAY = auto()
    STRIKE = auto()
    TIMETABLE = auto()
    EXTENSION = auto()


class BaseTemplate(ABC):
    @abstractmethod
    def get_prompt(self) -> str:
        pass
