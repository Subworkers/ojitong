from data.templates.base_template import BaseTemplate
from langchain_core.prompts import ChatPromptTemplate

class QGQATemplate(BaseTemplate***REMOVED***:
    @property
    def template(self***REMOVED***:
        if not hasattr(self, '_template'***REMOVED***:
            self._template = {
                "qg": self._generate_questions_prompt(***REMOVED***,
                "qa_reference": self._answer_questions_from_news_prompt(***REMOVED***,
                "qa_hypothesis": self._answer_questions_from_blog_prompt(***REMOVED***
            ***REMOVED***
            self._template = {key: self.clean_whitespace_template(value***REMOVED*** for key, value in self._template.items(***REMOVED******REMOVED***
        return self._template

    def clean_whitespace_template(self, prompt_template***REMOVED***:
        cleaned_messages = [
            (role, self.clean_whitespace(message***REMOVED******REMOVED***
            for role, message in prompt_template.messages
        ***REMOVED***
        return ChatPromptTemplate.from_messages(cleaned_messages***REMOVED***

    def _generate_questions_prompt(self***REMOVED***:
        return ChatPromptTemplate.from_messages([
            ("system", "You are an AI trained to generate insightful questions from a given article."***REMOVED***,
            ("user", """
                1. Read the article about current Seoul subway news.
                2. Find out what is the main incident related with subway in the article.
                3. Find the date that this article was issued
                4. Find every date-related expression in the article.
                5. Compare 3 and 4, and find out the date the incident was occured.
                6. Find every expression related to line of subway in the article.
                7. Find out which line the incident is about.
                8. Create 2 questions to identify the main points of the news (date of the incident, subway line of the incident***REMOVED***. The questions should be 5-way multiple choice questions where you have to choose one of the choices from 1 to 5. One of the options must be “Unknown” and the selection for the “Date of Event” question must be in the format 2018년 3월 18일. Hint is provided with every questions
                
                Example Question: 'Where did the subway incident occur? (1***REMOVED*** Gangnam Station (2***REMOVED*** Seongsu Station (3***REMOVED*** Suyu Station (4***REMOVED*** Ankguk Station (5***REMOVED*** Unknown.',
                Example Hint: ''
                News Article: {input***REMOVED***
                """
            ***REMOVED***,
            (
                "system", """
                Generate 2 questions. All responses should be in Korean ONLY. Use the template provided for formatting.
                
                Template:
                Question1: {{***REMOVED******REMOVED***,
                Hint1: {{***REMOVED******REMOVED***,
                Question2: {{***REMOVED******REMOVED***,
                Hint2: {{***REMOVED******REMOVED***
                """
            ***REMOVED***
        ***REMOVED******REMOVED***

    def _answer_questions_from_news_prompt(self***REMOVED***:
        return ChatPromptTemplate.from_messages([
            ("system", "You read a news article and answer a question accurately based on what you read."***REMOVED***, # 페르소나 부여
            ("user", """
                You read a news article like this:
                1. Read the article about current Seoul subway news.
                2. Find out what is the main incident related with subway in the article.
                3. Find the date that this article was issued
                4. Find every date-related expression in the article.
                5. Compare 3 and 4, and find out the date the incident was occured.
                6. Find every expression related to line of subway in the article.
                7. Find out which line the incident is about.
                Then you answer a question accurately based on what you read.
                
                Example: '1번, 5번, 4번'
                News Article: {input***REMOVED***
                Questions: {question***REMOVED***
            """***REMOVED***,
            ("system", "Template(MUST FOLLOW***REMOVED***: Answer1: {{answer_1***REMOVED******REMOVED***번, Answer2: {{answer_2***REMOVED******REMOVED***번"***REMOVED***
        ***REMOVED******REMOVED***

    def _answer_questions_from_blog_prompt(self***REMOVED***:
        return ChatPromptTemplate.from_messages([
            ("system", "You read a blog article and answer a question accurately based on what you read."***REMOVED***, # 페르소나 부여
            ("user", """
                You read a blog article like this:
                1. Read the blog about current Seoul subway news.
                2. Find out what is the main incident related with subway in the article.
                3. Find the date that this article was issued
                4. Find every date-related expression in the article.
                5. Compare 3 and 4, and find out the date the incident was occured.
                6. Find every expression related to line of subway in the article.
                7. Find out which line the incident is about.
                Then you answer a question accurately based on what you read.
            
                Example: '1번, 5번, 4번'
                Blog Article: {input***REMOVED***
                Questions: {question***REMOVED***
            """***REMOVED***,
            ("system", """"Template(MUST FOLLOW***REMOVED***: Answer1: {{answer_1***REMOVED******REMOVED***번, Answer2: {{answer_2***REMOVED******REMOVED***번"""***REMOVED***
        ***REMOVED******REMOVED***