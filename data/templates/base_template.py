from enum import Enum, auto
from abc import ABC, abstractmethod
import re
class WritingTemplateType(Enum):
    DELAY = auto()
    STRIKE = auto()
    TIMETABLE = auto()
    EXTENSION = auto()


class BaseTemplate(ABC):
    @abstractmethod
    def prompt(self):
        # prompt content 문자열 반환
        pass

    def clean_whitespace(self, text):
        # Strip whitespace from the start and end of the text, then replace multiple spaces with a single space
        return re.sub(r'\s+', ' ', text.strip())