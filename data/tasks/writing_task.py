from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
***REMOVED***
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from langchain.memory import ConversationSummaryBufferMemory

from data.tasks.base_task import BaseTask
from data.templates.writing_template import WritingTemplateFactory

class WritingTask(BaseTask***REMOVED***:
    def __init__(self, category***REMOVED***:
        self.category = category
        self.prompt_content = self._generate_prompt_content(self.category***REMOVED***
        super(***REMOVED***.__init__(***REMOVED***

    def _generate_prompt_content(self, category***REMOVED***:
        return WritingTemplateFactory.get_prompt(category***REMOVED***
    
    def _build_template(self***REMOVED***:
        return ChatPromptTemplate.from_template(self.prompt_content***REMOVED***

    def _build_parser(self***REMOVED***:
        return StrOutputParser(***REMOVED***
    
    def _build_chain(self***REMOVED***:
        return self.prompt_template | self.llm | self.parser

    def execute(self, source_content***REMOVED***:
        response = self.chain.invoke({"content": source_content***REMOVED******REMOVED***
        return response


class ChainingTask(WritingTask***REMOVED***:
    def __init__(self, category***REMOVED***:
        self._memory = None
        super(***REMOVED***.__init__(category***REMOVED***
        self.chain_list = self._define_chain_list(***REMOVED***

    def _build_template(self***REMOVED***:
        return ChatPromptTemplate(template=self.prompt_content, messages=[
            SystemMessagePromptTemplate.from_template(self._system_message(***REMOVED******REMOVED***,
            MessagesPlaceholder(variable_name="chat_history"***REMOVED***,
            HumanMessagePromptTemplate.from_template(self._human_message(***REMOVED******REMOVED***
        ***REMOVED******REMOVED***

    def _system_message(self***REMOVED***:
        return """
        Objective:
        Learn subway information through chaining and use that information to write a coherent and informative blog post using a template.
        
        Basic Setting:
        Your name is Jitong.
        You are a subway information supporter and a Naver Blog Power Blogger.
        You are well-informed about information and value communication with readers.
        Your goal is to help subway users by providing accurate and practical information for convenient and safe subway use.
        
        Features and Activities:
        You read the latest news related to subway, and write blog posts to accurately deliver these in a readable and high-quality manner to readers.
        You alleviate readers' inconveniences and speak empathetically through the blog, understanding the sentiments of subway users.
        
        Communication Style:
        You use professional yet warm and easy-to-understand language.
        You emphasize the ability to explain things in a way that is accessible to all age groups.
        Your blog posts should end with the forms -어요, -이에요/예요, -(이***REMOVED***여요, -(이***REMOVED***요.
        
        Hallucination:
        You always generate blog posts based on verifiable factual statements.
        You speak mainly about factual information related to subways and do not add information about subways on your own.
        """

    def _human_message(self***REMOVED***:
        user_message_placeholder = "{question***REMOVED***"
        return user_message_placeholder

    def _define_chain_list(self***REMOVED***:
        # 카테고리에 따라 chain_list를 정의
        chain_list = {
            "지연": ["지연/사고 일시", "지연/사고 노선", "지연/사고 이유"***REMOVED***,
            "파업": ["파업 일시", "파업 노선", "파업 이유"***REMOVED***,
            "연장": ["연장 노선"***REMOVED***,
        ***REMOVED***
        return chain_list.get(self.category, [***REMOVED******REMOVED***

    @property
    def memory(self***REMOVED***:
        if not self._memory:
            self._memory = self._build_memory(***REMOVED***
        return self._memory

    def _build_memory(self***REMOVED***:
        return ConversationSummaryBufferMemory(llm=self.llm, max_token_limit=100, memory_key="chat_history", return_messages=True***REMOVED***

    def _build_chain(self***REMOVED***:
        return LLMChain(llm=self.llm, prompt=self.prompt_template, memory=self.memory***REMOVED***
    
    def execute(self, source_content***REMOVED***:
        self.chain({"question": "subway information(article***REMOVED*** :" + source_content + " Just REVIEW subway " + self.category + " information"***REMOVED******REMOVED***
        for i in self.chain_list:
            self.chain({"question": "Using the provided information \n write " + i + ":"***REMOVED******REMOVED***
        self.chain({"question": "블로그 글 작성해줘"***REMOVED******REMOVED***
        self.chain({"question": f"1. 뉴스기사의 내용을 학습해 2. 뉴스 기사의 {','.join(self.chain_list***REMOVED******REMOVED***를 학습해 3. 학습한 뉴스기사와 블로그글을 비교해 4.블로그 글에 틀린 정보가 있다면 수정해 뉴스기사: " + source_content + "블로그 글 :"***REMOVED******REMOVED***
        response = self.chain({"question": self.prompt_content***REMOVED******REMOVED***
        return response

