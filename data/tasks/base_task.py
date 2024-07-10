***REMOVED***
***REMOVED***

class BaseTask(ABC***REMOVED***:
    def __init__(self***REMOVED***:
        self.llm = self._build_llm(***REMOVED***
        self.prompt_template = self._build_template(***REMOVED***
        self.parser = self._build_parser(***REMOVED***
        self.chain = self._build_chain(***REMOVED***

    def _build_llm(self***REMOVED***:
        return ChatOpenAI(model="gpt-4o"***REMOVED***
    
***REMOVED***
    def _build_template(self***REMOVED***:
        raise NotImplementedError(***REMOVED***

***REMOVED***
    def _build_parser(self***REMOVED***:
        raise NotImplementedError(***REMOVED***

***REMOVED***
    def _build_chain(self***REMOVED***:
        raise NotImplementedError(***REMOVED***

***REMOVED***
    def execute(self, *args, **kwargs***REMOVED***:
        raise NotImplementedError(***REMOVED***

