from data.tasks.base_task import BaseTask
from langchain_core.prompts import ChatPromptTemplate
from typing import List
import re

class SelectionNewsTask(BaseTask):
    def _build_template(self):
        prompt = """
        해당 기사 중에서 핵심 주제가 지하철 파업, 지연, 연착, 사고, 노선 연장인 기사들만 뽑아줘.
        행 인덱스 번호만 ,로 구분해서 나열해줘.
        {titles}
        """
        return ChatPromptTemplate.from_template(prompt)

    def _build_parser(self):
        return NumberListParser()

    def _build_chain(self):
        return self.prompt_template | self.llm | self.parser

    def execute(self, titles: List[str]):
        formatted_titles = "\n".join(titles)
        return self.chain.invoke(
            {
                "titles": formatted_titles,
            }
        )

from langchain_core.output_parsers import BaseOutputParser
from langchain_core.exceptions import OutputParserException

class NumberListParser(BaseOutputParser[List[int]]):
    """Custom parser for extracting a list of integers from text."""

    def parse(self, text: str) -> list:
        print(f"Parser Received: {text}.", flush=True)
        try:
            indices = [int(index) for index in re.findall(r'\d+', text)]
        except ValueError:
            raise OutputParserException(
                "NumberListParser expected number list. "
                f"Received: {text}."
            )
        return indices

    @property
    def _type(self) -> str:
        return "number_list_parser"