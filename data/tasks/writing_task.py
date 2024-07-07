from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import LLMChain
from langchain.memory import ConversationSummaryBufferMemory

from data.tasks.base_task import BaseTask
from data.templates.writing_template import WritingTemplateFactory

class WritingTask(BaseTask):
    def __init__(self, category):
        self.category = category
        self.prompt_content = self._generate_prompt_content(self.category)
        super().__init__()

    def _generate_prompt_content(self, category):
        return WritingTemplateFactory.get_template(category).get_prompt()
    
    def _build_prompt(self):
        return ChatPromptTemplate.from_template(self.prompt_content)

    def _build_parser(self):
        return StrOutputParser()
    
    def _build_chain(self):
        return self.prompt_template | self.llm | self.parser

    def execute(self, source_content):
        response = self.chain.invoke({"content": source_content})
        return response


class ChainingTask(WritingTask):
    def __init__(self, category):
        self._memory = None
        super().__init__(category)
        self.chain_list = self._define_chain_list()

    def _build_prompt(self):
        return ChatPromptTemplate(template=self.prompt_content, messages=[
            SystemMessagePromptTemplate.from_template(self._system_message()),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(self._human_message())
        ])

    def _system_message(self):
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
        Your blog posts should end with the forms -어요, -이에요/예요, -(이)여요, -(이)요.
        
        Hallucination:
        You always generate blog posts based on verifiable factual statements.
        You speak mainly about factual information related to subways and do not add information about subways on your own.
        """

    def _human_message(self):
        user_message_placeholder = "{question}"
        return user_message_placeholder

    def _define_chain_list(self):
        # 카테고리에 따라 chain_list를 정의
        chain_list = {
            "지연": ["지연/사고 일시", "지연/사고 노선", "지연/사고 이유"],
            "파업": ["파업 일시", "파업 노선", "파업 이유"],
            "연장": ["연장 노선"],
        }
        return chain_list.get(self.category, [])

    @property
    def memory(self):
        if not self._memory:
            self._memory = self._build_memory()
        return self._memory

    def _build_memory(self):
        return ConversationSummaryBufferMemory(llm=self.llm, max_token_limit=100, memory_key="chat_history", return_messages=True)

    def _build_chain(self):
        return LLMChain(llm=self.llm, prompt=self.prompt_template, memory=self.memory)
    
    def execute(self, source_content):
        self.chain({"question": "subway information(article) :" + source_content + " Just REVIEW subway " + self.category + " information"})
        for i in self.chain_list:
            self.chain({"question": "Using the provided information \n write " + i + ":"})
        self.chain({"question": "블로그 글 작성해줘"})
        self.chain({"question": f"1. 뉴스기사의 내용을 학습해 2. 뉴스 기사의 {','.join(self.chain_list)}를 학습해 3. 학습한 뉴스기사와 블로그글을 비교해 4.블로그 글에 틀린 정보가 있다면 수정해 뉴스기사: " + source_content + "블로그 글 :"})
        response = self.chain({"question": self.prompt_content})
        return response

