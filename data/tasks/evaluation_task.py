import re
***REMOVED***
from rouge_score import rouge_scorer
***REMOVED***
from langchain_core.prompts import ChatPromptTemplate

from data.tasks.base_task import BaseTask
from data.templates.evaluation_template import GEvalEvaluationTemplate, QGQATemplate

class PairwiseEvaluationTask(BaseTask, ABC***REMOVED***:
    def __init__(self***REMOVED***:
        super(***REMOVED***.__init__(***REMOVED***

    def _build_llm(self***REMOVED***:
        return ChatOpenAI(model="gpt-4o-mini"***REMOVED***

    def _build_chain(self***REMOVED***:
        return self.prompt_template | self.llm | self.parser

***REMOVED***
    def execute(self, hypothesis, reference***REMOVED***:
        pass

class SingleAnswerEvaluationTask(BaseTask, ABC***REMOVED***:
    def __init__(self***REMOVED***:
        super(***REMOVED***.__init__(***REMOVED***

    def _build_llm(self***REMOVED***:
        return ChatOpenAI(model="gpt-4o-mini"***REMOVED***

    def _build_chain(self***REMOVED***:
        return self.prompt_template | self.llm | self.parser

***REMOVED***
    def execute(self, hypothesis***REMOVED***:
        pass


class MetricBasedEvaluationTask(PairwiseEvaluationTask***REMOVED***:
    def _build_template(self***REMOVED***:
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
    def _build_template(self***REMOVED***:
        prompts = QGQATemplate(***REMOVED***.prompt
        return {
            key: ChatPromptTemplate.from_messages(value***REMOVED*** 
            for key, value in prompts.items(***REMOVED***
        ***REMOVED***

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
        answers_news = self.chain["chain_qa_reference"***REMOVED***.invoke({"input": news_content, "question": questions.content***REMOVED******REMOVED***
        detailed_answers_news = [
            self.parser.extract_detailed_answer(questions.content, i+1, ans***REMOVED***
            for i, ans in enumerate(answers_news***REMOVED***
        ***REMOVED***
        # 프롬프트 3을 통해 블로그 기반 답변 생성
        answers_blog = self.chain["chain_qa_hypothesis"***REMOVED***.invoke({"input": blog_content, "question": questions.content***REMOVED******REMOVED***
        detailed_answers_blog = [
            self.parser.extract_detailed_answer(questions.content, i+1, ans***REMOVED***
            for i, ans in enumerate(answers_blog***REMOVED***
        ***REMOVED***

        # 결과 비교 및 평가
        conparison_results = self.evaluate_answers(answers_news, answers_blog, detailed_answers_news, detailed_answers_blog***REMOVED***
        return conparison_results

    def evaluate_answers(self, answers_news, answers_blog, detailed_answers_news, detailed_answers_blog***REMOVED***:
        # Comparing answers from news and blog
        comparison_results = {
            'date_comparison': answers_news[0***REMOVED*** == answers_blog[0***REMOVED***,
            'line_comparison': answers_news[1***REMOVED*** == answers_blog[1***REMOVED***,
            'news_details': f"<뉴스> 발생일시: {detailed_answers_news[0***REMOVED******REMOVED***, 발생노선: {detailed_answers_news[1***REMOVED******REMOVED***",
            'blog_details': f"<블로그> 발생일시: {detailed_answers_blog[0***REMOVED******REMOVED***, 발생노선: {detailed_answers_blog[1***REMOVED******REMOVED***"
        ***REMOVED***
        return comparison_results


from langchain_core.output_parsers import BaseOutputParser
from langchain_core.exceptions import OutputParserException

class AnswerExtractionParser(BaseOutputParser***REMOVED***:
    def parse(self, text***REMOVED***:
        # Using findall to extract all matches of the pattern
        try:
            answers = self.extract_answer(text***REMOVED***
        except ValueError:
            raise OutputParserException(
                "CommaSeparatedIndexParser expected comma-separated integers. ",
                f"Received: {text***REMOVED***."
            ***REMOVED***
        return answers

    def extract_answer(self, text***REMOVED***:
        pattern_answer = re.compile(r"Answer\d+: (\d+***REMOVED***번"***REMOVED***
        return re.findall(pattern_answer, text***REMOVED***

    def extract_detailed_answer(self, text, question_number, answer_number***REMOVED***:
        # 주어진 질문 번호와 답변 번호에 대해 상세한 답변을 추출
        pattern_detailed_answer = "Question{***REMOVED***: .*?\\({***REMOVED***\\***REMOVED***\\s*(.*?***REMOVED***(?=\\(|\\.***REMOVED***"
        pattern = pattern_detailed_answer.format(question_number, answer_number***REMOVED***
        match = re.search(pattern, text, re.DOTALL***REMOVED***
        return match.group(1***REMOVED***.strip(***REMOVED*** if match else ""


# Consistency 항목 제외 SingleAnswer Evaluation 방식이지만,
# GEvalEvaluationTask 단일 클래스로 가져가기 위해 PairwiseEvaluationTask 사용
class GEvalEvaluationTask(PairwiseEvaluationTask***REMOVED***:
    def _build_template(self***REMOVED***:
        prompts = GEvalEvaluationTemplate(***REMOVED***.prompt
        return {
            key: ChatPromptTemplate.from_messages([
                ("system", value***REMOVED***,
                ("user", "{input***REMOVED***"***REMOVED***
            ***REMOVED******REMOVED***
            for key, value in prompts.items(***REMOVED***
        ***REMOVED***

    def _build_parser(self***REMOVED***:
        return ScoreReasonParser(***REMOVED***

    def _build_chain(self***REMOVED***:
        return {
            key: prompt_template | self.llm | self.parser
            for key, prompt_template in self.prompt_template.items(***REMOVED***
        ***REMOVED***

    def execute(self, hypothesis, reference***REMOVED***:
        geval_results = {***REMOVED***

        # Consistency Score - pairwise evaluation 수행
        consistency_eval_result = self.chain["Consistency"***REMOVED***.invoke({"input": f"article reference: {reference***REMOVED***\n blog content: {hypothesis***REMOVED***"***REMOVED******REMOVED***
        geval_results["Consistency"***REMOVED*** = consistency_eval_result

        # Consistency 제외 항목 - SingleAnswer evaluation 수행
        geval_results.update({
            aspect: self.chain[aspect***REMOVED***.invoke({"input": f"blog content: {hypothesis***REMOVED***"***REMOVED******REMOVED*** 
            for aspect in self.prompt_template.keys(***REMOVED*** if aspect != "Consistency"
        ***REMOVED******REMOVED***
        
        return geval_results


from langchain_core.output_parsers import BaseOutputParser
from langchain_core.exceptions import OutputParserException
import re

class ScoreReasonParser(BaseOutputParser***REMOVED***:
    def parse(self, text***REMOVED***:
        pattern_score = re.compile(r"Score: (\d+***REMOVED***"***REMOVED***
        pattern_reason = re.compile(r"Reason: (.****REMOVED***", re.DOTALL***REMOVED***

        match_score = re.search(pattern_score, text***REMOVED***
        match_reason = re.search(pattern_reason, text***REMOVED***

        if match_score:
            score = int(match_score.group(1***REMOVED******REMOVED***
        else:
            raise OutputParserException("No Scores (SCORE ONLY***REMOVED*** score found in the response.", f"Received: {text***REMOVED***."***REMOVED***

        if match_reason:
            reason = match_reason.group(1***REMOVED***.strip(***REMOVED***
        else:
            reason = "Unknown reason"
        return {'score': score, 'reason': reason***REMOVED***
