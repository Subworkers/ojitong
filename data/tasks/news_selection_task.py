from data.tasks.base_task import BaseTask
from langchain_core.prompts import ChatPromptTemplate
from typing import List
import re

class SelectionNewsTask(BaseTask***REMOVED***:
    def _build_template(self***REMOVED***:
        prompt = """
        해당 기사 중에서 핵심 주제가 지하철 파업, 지연, 연착, 사고, 노선 연장인 기사들만 뽑아줘.
        행 인덱스 번호만 ,로 구분해서 나열해줘.
        {titles***REMOVED***
        """
        return ChatPromptTemplate.from_template(prompt***REMOVED***

    def _build_parser(self***REMOVED***:
        return NumberListParser(***REMOVED***

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

class NumberListParser(BaseOutputParser[List[int***REMOVED******REMOVED******REMOVED***:
    """Custom parser for extracting a list of integers from text."""

    def parse(self, text: str***REMOVED*** -> list:
        print(f"Parser Received: {text***REMOVED***.", flush=True***REMOVED***
        try:
            indices = [int(index***REMOVED*** for index in re.findall(r'\d+', text***REMOVED******REMOVED***
        except ValueError:
            raise OutputParserException(
                "NumberListParser expected number list. "
                f"Received: {text***REMOVED***."
            ***REMOVED***
        return indices

    @property
    def _type(self***REMOVED*** -> str:
        return "comma_separated_index_parser"