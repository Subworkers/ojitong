from data.templates.base_template import BaseTemplate
from langchain_core.prompts import ChatPromptTemplate

class QGQATemplate(BaseTemplate):
    def get_prompt(self):
        return {
            "qg": self._generate_questions_prompt(),
            "qa_reference": self._answer_questions_from_news_prompt(),
            "qa_hypothesis": self._answer_questions_from_blog_prompt()
        }

    def _generate_questions_prompt(self):
        return ChatPromptTemplate.from_messages([
            ("system", "You are an AI trained to generate insightful questions from a given article."),
            ("user", """
                1. Read the article about current Seoul subway news.
                2. Find out what is the main incident related with subway in the article.
                3. Find the date that this article was issued
                4. Find every date-related expression in the article.
                5. Compare 3 and 4, and find out the date the incident was occured.
                6. Find every expression related to line of subway in the article.
                7. Find out which line the incident is about.
                8. Create 2 questions to identify the main points of the news (date of the incident, subway line of the incident). The questions should be 5-way multiple choice questions where you have to choose one of the choices from 1 to 5. One of the options must be “Unknown” and the selection for the “Date of Event” question must be in the format 2018년 3월 18일. Hint is provided with every questions
                
                Example Question: 'Where did the subway incident occur? (1) Gangnam Station (2) Seongsu Station (3) Suyu Station (4) Ankguk Station (5) Unknown.',
                Example Hint: ''
                News Article: {input}
                """
            ),
            (
                "system", """
                Generate 2 questions. All responses should be in Korean ONLY. Use the template provided for formatting.
                
                Template:
                Question1: {{}},
                Hint1: {{}},
                Question2: {{}},
                Hint2: {{}}
                """
            )
        ])

    def _answer_questions_from_news_prompt(self):
        return ChatPromptTemplate.from_messages([
            ("system", "You read a news article and answer a question accurately based on what you read."), # 페르소나 부여
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
                News Article: {input}
                Questions: {question}
            """),
            ("system", "Template(MUST FOLLOW): Answer1: {{answer_1}}번, Answer2: {{answer_2}}번")
        ])

    def _answer_questions_from_blog_prompt(self):
        return ChatPromptTemplate.from_messages([
            ("system", "You read a blog article and answer a question accurately based on what you read."), # 페르소나 부여
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
                Blog Article: {input}
                Questions: {question}
            """),
            ("system", """"Template(MUST FOLLOW): Answer1: {{answer_1}}번, Answer2: {{answer_2}}번""")
        ])