from enum import Enum, auto
***REMOVED***

class WritingTemplateType(Enum***REMOVED***:
    DELAY = auto(***REMOVED***
    STRIKE = auto(***REMOVED***
    TIMETABLE = auto(***REMOVED***
    EXTENSION = auto(***REMOVED***


class BaseTemplate(ABC***REMOVED***:
***REMOVED***
    def get_prompt(self***REMOVED*** -> str:
        pass
