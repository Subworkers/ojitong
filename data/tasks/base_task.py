from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI

class BaseTask(ABC):
    def __init__(self):
        self.llm = self._build_llm()
        self.prompt_template = self._build_prompt()
        self.parser = self._build_parser()
        self.chain = self._build_chain()

    def _build_llm(self):
        return ChatOpenAI(model="gpt-4o")
    
    @abstractmethod
    def _build_prompt(self):
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


class WritingTask(BaseTask, ABC):
    def __init__(self, category):
        self.category = category
        self.prompt_template = self._build_prompt()
        self.parser = self._build_parser()
        self.chain = self._build_chain()

    @abstractmethod
    def _build_prompt(self):
        pass

    @abstractmethod
    def _build_parser(self):
        pass

    @abstractmethod
    def _build_chain(self):
        pass

    @abstractmethod
    def execute(self, content):
        pass
