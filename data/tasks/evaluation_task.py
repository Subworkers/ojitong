import re
from abc import ABC, abstractmethod
from rouge_score import rouge_scorer
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from data.tasks.base_task import BaseTask
from data.templates.evaluation_template import QGQATemplate

class PairwiseEvaluationTask(BaseTask, ABC):
    def __init__(self):
        super().__init__()

    def _build_llm(self):
        import os
        os.environ["OPENAI_API_KEY"] = "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"
        return ChatOpenAI(model="gpt-3.5-turbo-0125")

    def _build_chain(self):
        return self.prompt_template | self.llm | self.parser

    @abstractmethod
    def execute(self, hypothesis, reference):
        pass


class MetricBasedEvaluationTask(PairwiseEvaluationTask):
    def _build_prompt(self):
        # Define summarizing prompt
        return ChatPromptTemplate.from_messages([
            ("system", "You are talented at summarizing text without missing any important information."),
            ("user", "Read this article and summarize in 3-5 sentences ONLY in Korean. Article: {article}, Summary :")
        ])

    def execute(self, hypothesis, reference):
        # Generate summaries for reference and generated content
        content_summary = self.chain.invoke({"article": hypothesis}) # blog content
        reference_summary = self.chain.invoke({"article": reference}) # news reference

        # Calculate the ROUGE score for summaries
        scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
        rouge_summary = scorer.score(reference_summary["text"], content_summary["text"])

        return rouge_summary['rouge1'].recall


class QGQAEvaluationTask(PairwiseEvaluationTask):
    def _build_prompt(self):
        return QGQATemplate().get_prompt()

    def _build_parser(self):
        return AnswerExtractionParser()

    def _build_chain(self):
        return {
            "chain_qg": self.prompt_template["qg"] | self.llm,
            "chain_qa_reference": self.prompt_template["qa_reference"] | self.llm | self.parser,
            "chain_qa_hypothesis": self.prompt_template["qa_hypothesis"] | self.llm | self.parser
        }

    def execute(self, news_content, blog_content):
        # 프롬프트 1을 통해 질문 생성
        questions = self.chain["chain_qg"].invoke({"input": news_content})
        # 프롬프트 2를 통해 뉴스 기반 답변 생성
        answers_news = self.chain["chain_qa_reference"].invoke({"input": news_content, "question": questions.content})
        detailed_answers_news = [
            self.parser.extract_detailed_answer(questions.content, i+1, ans)
            for i, ans in enumerate(answers_news)
        ]
        # 프롬프트 3을 통해 블로그 기반 답변 생성
        answers_blog = self.chain["chain_qa_hypothesis"].invoke({"input": blog_content, "question": questions.content})
        detailed_answers_blog = [
            self.parser.extract_detailed_answer(questions.content, i+1, ans)
            for i, ans in enumerate(answers_blog)
        ]

        # 결과 비교 및 평가
        conparison_results = self.evaluate_answers(answers_news, answers_blog, detailed_answers_news, detailed_answers_blog)
        return conparison_results


    def evaluate_answers(self, answers_news, answers_blog, detailed_answers_news, detailed_answers_blog):
        # Comparing answers from news and blog
        comparison_results = {
            'date_comparison': answers_news[0] == answers_blog[0],
            'line_comparison': answers_news[1] == answers_blog[1],
            'news_details': f"<뉴스> 발생일시: {detailed_answers_news[0]}, 발생노선: {detailed_answers_news[1]}",
            'blog_details': f"<블로그> 발생일시: {detailed_answers_blog[0]}, 발생노선: {detailed_answers_blog[1]}"
        }
        return comparison_results


from langchain_core.output_parsers import BaseOutputParser
from langchain_core.exceptions import OutputParserException

class AnswerExtractionParser(BaseOutputParser):
    def parse(self, text):
        # Using findall to extract all matches of the pattern
        try:
            answers = self.extract_answer(text)
        except ValueError:
            raise OutputParserException(
                "CommaSeparatedIndexParser expected comma-separated integers. ",
                f"Received: {text}."
            )
        return answers

    def extract_answer(self, text):
        pattern_answer = re.compile(r"Answer\d+: (\d+)번")
        return re.findall(pattern_answer, text)

    def extract_detailed_answer(self, text, question_number, answer_number):
        # 주어진 질문 번호와 답변 번호에 대해 상세한 답변을 추출
        pattern_detailed_answer = "Question{}: .*?\\({}\\)\\s*(.*?)(?=\\(|\\.)"
        pattern = pattern_detailed_answer.format(question_number, answer_number)
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ""