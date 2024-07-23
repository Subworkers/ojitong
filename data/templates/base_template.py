from enum import Enum, auto
***REMOVED***
import re
class WritingTemplateType(Enum***REMOVED***:
    DELAY = auto(***REMOVED***
    STRIKE = auto(***REMOVED***
    TIMETABLE = auto(***REMOVED***
    EXTENSION = auto(***REMOVED***


class BaseTemplate(ABC***REMOVED***:
***REMOVED***
    def prompt(self***REMOVED***:
        # prompt content 문자열 반환
        pass

    def clean_whitespace(self, text***REMOVED***:
        # Strip whitespace from the start and end of the text, then replace multiple spaces with a single space
        return re.sub(r'\s+', ' ', text.strip(***REMOVED******REMOVED***