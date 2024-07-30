from data.tasks.base_task import BaseTask
from langchain_core.prompts import ChatPromptTemplate
from typing import List

class SelectionNewsTask(BaseTask):
    def _build_template(self):
        prompt = """
        해당 기사 중에서 핵심 주제가 지하철 파업, 지연, 연착, 사고, 노선 연장인 기사들만 뽑아서 행 인덱스 번호만 [,]로 구분해서 나열해줘:
        {titles}
        """
        return ChatPromptTemplate.from_template(prompt)

    def _build_parser(self):
        return CommaSeparatedIndexParser()

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

class CommaSeparatedIndexParser(BaseOutputParser[list]):
    """Custom parser for extracting indices from comma-separated strings."""

    def parse(self, text: str) -> list:
        try:
            indices = [int(index.strip()) for index in text.split(',')]
        except ValueError:
            raise OutputParserException(
                "CommaSeparatedIndexParser expected comma-separated integers. "
                f"Received: {text}."
            )
        return indices

    @property
    def _type(self) -> str:
        return "comma_separated_index_parser"