from enum import Enum, auto
from typing import Literal

class PostType(Enum):
    DELAY = auto()
    STRIKE = auto()
    TIMETABLE = auto()
    EXTENSION = auto()
    
class DataType(Enum):
    SOURCE_KNOWLEDGE = "source"