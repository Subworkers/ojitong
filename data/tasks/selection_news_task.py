from data.tasks.base_task import BaseTask
from langchain_core.prompts import ChatPromptTemplate
from typing import List

class SelectionNewsTask(BaseTask***REMOVED***:
    def _build_template(self***REMOVED***:
        prompt = """
        해당 기사 중에서 핵심 주제가 지하철 파업, 지연, 연착, 사고, 노선 연장인 기사들만 뽑아서 행 인덱스 번호만 [,***REMOVED***로 구분해서 나열해줘:
        {titles***REMOVED***
        """
        return ChatPromptTemplate.from_template(prompt***REMOVED***

    def _build_parser(self***REMOVED***:
        return CommaSeparatedIndexParser(***REMOVED***

    def _build_chain(self***REMOVED***:
        return self.prompt_template | self.llm | self.parser

    def execute(self, titles: List[str***REMOVED******REMOVED***:
        formatted_titles = "\n".join(titles***REMOVED***
        return self.chain.invoke(
            {
                "titles": formatted_titles,
            ***REMOVED***
        ***REMOVED***

from langchain_core.output_parsers import BaseOutputParser
from langchain_core.exceptions import OutputParserException

class CommaSeparatedIndexParser(BaseOutputParser[list***REMOVED******REMOVED***:
    """Custom parser for extracting indices from comma-separated strings."""

    def parse(self, text: str***REMOVED*** -> list:
        try:
            indices = [int(index.strip(***REMOVED******REMOVED*** for index in text.split(','***REMOVED******REMOVED***
        except ValueError:
            raise OutputParserException(
                "CommaSeparatedIndexParser expected comma-separated integers. "
                "Received: {text***REMOVED***."
            ***REMOVED***
        return indices

    @property
    def _type(self***REMOVED*** -> str:
        return "comma_separated_index_parser"