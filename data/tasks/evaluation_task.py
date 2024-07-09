import re
***REMOVED***
from rouge_score import rouge_scorer
***REMOVED***
from langchain_core.prompts import ChatPromptTemplate

from data.tasks.base_task import BaseTask
from data.templates.evaluation_template import QGQATemplate

class PairwiseEvaluationTask(BaseTask, ABC***REMOVED***:
    def __init__(self***REMOVED***:
        super(***REMOVED***.__init__(***REMOVED***

    def _build_llm(self***REMOVED***:
        import os
        os.environ["OPENAI_API_KEY"***REMOVED*** = "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"
        return ChatOpenAI(model="gpt-3.5-turbo-0125"***REMOVED***

    def _build_chain(self***REMOVED***:
        return self.prompt_template | self.llm | self.parser

***REMOVED***
    def execute(self, hypothesis, reference***REMOVED***:
        pass


class MetricBasedEvaluationTask(PairwiseEvaluationTask***REMOVED***:
    def _build_prompt(self***REMOVED***:
        # Define summarizing prompt
        return ChatPromptTemplate.from_messages([
            ("system", "You are talented at summarizing text without missing any important information."***REMOVED***,
            ("user", "Read this article and summarize in 3-5 sentences ONLY in Korean. Article: {article***REMOVED***, Summary :"***REMOVED***
        ***REMOVED******REMOVED***

    def execute(self, hypothesis, reference***REMOVED***:
        # Generate summaries for reference and generated content
        content_summary = self.chain.invoke({"article": hypothesis***REMOVED******REMOVED*** # blog content
        reference_summary = self.chain.invoke({"article": reference***REMOVED******REMOVED*** # news reference

        # Calculate the ROUGE score for summaries
        scorer = rouge_scorer.RougeScorer(['rouge1'***REMOVED***, use_stemmer=True***REMOVED***
        rouge_summary = scorer.score(reference_summary["text"***REMOVED***, content_summary["text"***REMOVED******REMOVED***

        return rouge_summary['rouge1'***REMOVED***.recall


class QGQAEvaluationTask(PairwiseEvaluationTask***REMOVED***:
    def _build_prompt(self***REMOVED***:
        return QGQATemplate(***REMOVED***.get_prompt(***REMOVED***

    def _build_parser(self***REMOVED***:
        return AnswerExtractionParser(***REMOVED***

    def _build_chain(self***REMOVED***:
        return {
            "chain_qg": self.prompt_template["qg"***REMOVED*** | self.llm,
            "chain_qa_reference": self.prompt_template["qa_reference"***REMOVED*** | self.llm | self.parser,
            "chain_qa_hypothesis": self.prompt_template["qa_hypothesis"***REMOVED*** | self.llm | self.parser
        ***REMOVED***

    def execute(self, news_content, blog_content***REMOVED***:
        # 프롬프트 1을 통해 질문 생성
        questions = self.chain["chain_qg"***REMOVED***.invoke({"input": news_content***REMOVED******REMOVED***
        # 프롬프트 2를 통해 뉴스 기반 답변 생성
        answers_news = self.chain["chain_qa_reference"***REMOVED***.invoke({"input": news_content, "question": questions***REMOVED******REMOVED***
        # 프롬프트 3을 통해 블로그 기반 답변 생성
        answers_blog = self.chain["chain_qa_hypothesis"***REMOVED***.invoke({"input": blog_content, "question": questions***REMOVED******REMOVED***

        # 결과 비교 및 평가
        return self.evaluate_answers(answers_news, answers_blog***REMOVED***

    def evaluate_answers(self, answers_news, answers_blog***REMOVED***:
        # Comparing answers from news and blog
        comparison_results = {
            'date': answers_news[0***REMOVED*** == answers_blog[0***REMOVED***,
            'line': answers_news[1***REMOVED*** == answers_blog[1***REMOVED***
        ***REMOVED***

        return comparison_results


from langchain_core.output_parsers import BaseOutputParser
from langchain_core.exceptions import OutputParserException

class AnswerExtractionParser(BaseOutputParser***REMOVED***:
    def parse(self, text***REMOVED***:
        # Using findall to extract all matches of the pattern
        pattern = re.compile(r"Answer\d+: (\d+***REMOVED***번"***REMOVED***
        try:
            indices = re.findall(pattern, text***REMOVED***
        except ValueError:
            raise OutputParserException(
                "CommaSeparatedIndexParser expected comma-separated integers. "
                "Received: {text***REMOVED***."
            ***REMOVED***
        return indices