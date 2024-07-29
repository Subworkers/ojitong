from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI

class BaseTask(ABC):
    def __init__(self):
        self.llm = self._build_llm()
        self.prompt_template = self._build_template()
        self.parser = self._build_parser()
        self.chain = self._build_chain()

    def _build_llm(self):
        return ChatOpenAI(model="gpt-4o")
    
    @abstractmethod
    def _build_template(self):
        raise NotImplementedError()

    @abstractmethod
    def _build_parser(self):
        raise NotImplementedError()

    @abstractmethod
    def _build_chain(self):
        raise NotImplementedError()

    @abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError()

