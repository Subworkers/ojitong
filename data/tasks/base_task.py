***REMOVED***
***REMOVED***

class BaseTask(ABC***REMOVED***:
    def __init__(self***REMOVED***:
        self.llm = self._build_llm(***REMOVED***
        self.prompt_template = self._build_prompt(***REMOVED***
        self.parser = self._build_parser(***REMOVED***
        self.chain = self._build_chain(***REMOVED***

    def _build_llm(self***REMOVED***:
        import os
        os.environ["OPENAI_API_KEY"***REMOVED*** = "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"
        return ChatOpenAI(model="gpt-4o"***REMOVED***
    
***REMOVED***
    def _build_prompt(self***REMOVED***:
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


class WritingTask(BaseTask, ABC***REMOVED***:
    def __init__(self, category***REMOVED***:
        self.category = category
        self.prompt_template = self._build_prompt(***REMOVED***
        self.parser = self._build_parser(***REMOVED***
        self.chain = self._build_chain(***REMOVED***

***REMOVED***
    def _build_prompt(self***REMOVED***:
        pass

***REMOVED***
    def _build_parser(self***REMOVED***:
        pass

***REMOVED***
    def _build_chain(self***REMOVED***:
        pass

***REMOVED***
    def execute(self, content***REMOVED***:
        pass
